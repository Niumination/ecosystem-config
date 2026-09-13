---
name: vnc-rfb-debugging
description: "Debug VNC/RFB protocol for macOS Screen Sharing.app."
version: "1.1"
author: Afrizal Munthe (Niumination)
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [debugging, vnc, rfb, screen-sharing]
    related_skills: [systematic-debugging, verification-before-completion]
---

# VNC/RFB Protocol Debugging

## Overview

Debug VNC/RFB protocol integration for macOS Screen Sharing.app compatibility.
Covers common pitfalls, testing patterns, and protocol-specific fixes.

## When to Use

- VNC server not connecting to macOS Screen Sharing.app
- RFB protocol handshake failures
- struct.pack mismatches in binary protocol encoding
- Server name encoding issues (null bytes)
- Data fragmentation in socket.send()
- FramebufferUpdate not receiving complete pixel data

## Common Pitfalls

### 1. struct.pack Mismatch

RFB ServerInit header: `struct.pack('!HHBBBBHH', ...)` = 12 bytes
- H (2 bytes) × 2 = width, height = 4 bytes
- B (1 byte) × 4 = bpp, depth, pad, pad = 4 bytes  
- H (2 bytes) × 2 = name_len (uint32 = 4 bytes), encoding = 4 bytes

**Total: 12 bytes for header**

**WRONG:** `struct.pack('!HHBBBBHHH', ...)` = 13 bytes (extra H field)
**WRONG:** Wrong argument count in pack

**FIX:** Always verify: `assert len(header) == 12` before sending
```python
header = struct.pack('!HHBBBBHH', width, height, bpp, depth, 0, 0, 0, 0)
assert len(header) == 12, f"Expected 12 bytes, got {len(header)}"
```

### 2. Server Name Null Bytes

**WRONG:** `f"Android Screen - {self.device_serial}"` when `device_serial` is `None`
→ produces `"Android Screen - None"` (17 bytes)

**WRONG:** `device_name.encode('utf-8')` then decoding with latin-1 later
→ can produce null bytes if name is malformed

**FIX:** Use latin-1 encoding from the start for VNC protocol compliance
```python
device_name = "Android Screen" if self.device_serial else "Android Device"
name_bytes = device_name.encode('latin-1')  # VNC uses latin-1
server_init += struct.pack('!I', len(name_bytes))
server_init += name_bytes
```

**DEBUGGING NOTE:** If receiving `"ce"` as name (1147500137 bytes claimed), you're parsing at wrong offset. This indicates name_len is being read from wrong position in buffer (likely reading pixel data).

### 3. send() vs sendall()

**WRONG:** `socket.send(data)` — may fragment for large payloads
→ With ~10MB uncompressed RGBX, single send() may not deliver all bytes
→ Client receives partial data, parsing fails

**FIX:** Use `socket.sendall(data)` for RFB protocol messages
```python
# WRONG
client_socket.send(msg)
client_socket.send(screen_data)

# CORRECT - ensures complete transfer
client_socket.sendall(msg)
client_socket.sendall(screen_data)
```

**WHY:** RFB protocol expects complete messages. Partial sends cause client to read incomplete headers, producing garbage parses like name_len=1147500137 (reading pixel data as name length).

### 4. Client Parsing Offset

**WRONG:** Parsing name_len at byte 24, name at byte 28
→ ServerInit = 12 bytes header + 4 bytes name_len + name_bytes
→ Name starts at byte 16, NOT byte 28

**Structure:**
```
Bytes 0-1:   width (uint16)
Bytes 2-3:   height (uint16)
Byte 4:      bpp (uint8)
Byte 5:      depth (uint8)
Bytes 6-11:  padding (6 bytes of zeros)
Bytes 12-15: name length (uint32)
Bytes 16+:   name (name_len bytes)
```

**FIX:** Parse name at offset 12 for length, offset 16 for data
```python
# WRONG - reads pixel data as name length
name_len = int.from_bytes(data[24:28], 'big')  
name = data[28:28+name_len].decode('latin-1')

# CORRECT
name_len = int.from_bytes(data[12:16], 'big')
name = data[16:16+name_len].decode('latin-1')
```

**DEBUGGING:** If name_len is huge (e.g., 1 billion+), you're reading pixel data. Check your parse offsets.

### 5. FramebufferUpdate Message Structure

RFB FramebufferUpdate is THREE separate messages, NOT a single blob:

```
1. FramebufferUpdate header (4 bytes):
   - byte 0: type = 0
   - byte 1: padding = 0  
   - bytes 2-3: number_of_rectangles (uint16)

2. Rectangle header (12 bytes):
   - bytes 0-1: x_position (uint16)
   - bytes 2-3: y_position (uint16)
   - bytes 4-5: width (uint16)
   - bytes 6-7: height (uint16)
   - bytes 8-11: encoding_type (int32)

3. Pixel data (width * height * bytes_per_pixel)
```

**WRONG:** Send header + rectangle + data as single blob
→ Client parses header, expects separate rectangle messages per RFB spec

**WRONG:** Send as single sendall() with all three concatenated
→ Client reads first 4 bytes as header, then tries to parse rectangle from wrong position

**CORRECT:** Send as three separate sendall() calls
```python
# 1. FramebufferUpdate header (4 bytes)
fb_header = struct.pack('!BBH', 0, 0, 1)  # type=0, padding=0, rects=1
client_socket.sendall(fb_header)

# 2. Rectangle header (12 bytes)
rect_header = struct.pack('!HHHHi', 0, 0, w, h, 0)  # Raw encoding type 0
client_socket.sendall(rect_header)

# 3. Pixel data
client_socket.sendall(screen_data)
```

**DEBUGGING:** If client gets "struct.error: unpack requires a buffer of 2 bytes" after receiving FramebufferUpdate, it likely received header but not rectangle header, or vice versa. Check that you're sending separate messages with sendall().

### 6. Testing Pattern with Known-Good Buffer

When debugging RFB parsing, always verify against a known-good buffer first:

```python
import struct
from PIL import Image
import io

# Create test image
img = Image.new('RGB', (100, 100), color='green')
raw_rgbx = img.tobytes('raw', 'RGBX')
print(f"Expected pixel data: {len(raw_rgbx)} bytes")

# Build ServerInit manually and verify structure
name = "Test"
name_bytes = name.encode('latin-1')
server_init = struct.pack('!HHBBBBHH', 100, 100, 32, 24, 0, 0, 0, 0)
server_init += struct.pack('!I', len(name_bytes))
server_init += name_bytes

assert len(server_init) == 12 + 4 + len(name_bytes)
print(f"ServerInit: {len(server_init)} bytes ✓")

# Build FramebufferUpdate manually
fb_header = struct.pack('!BBH', 0, 0, 1)  # 4 bytes (not 3!)
rect_header = struct.pack('!HHHHi', 0, 0, 100, 100, 0)  # 12 bytes
expected_total = len(fb_header) + len(rect_header) + len(raw_rgbx)
print(f"Total message: {expected_total} bytes")
```

**NOTE:** FramebufferUpdate header is 4 bytes (type + 1 padding + 2 bytes num_rects), not 3 bytes.

## Testing Pattern

### Standard Test Flow

```python
data = sock.recv(1024)
print(f'Received: {len(data)} bytes, hex: {data.hex()}')

# Verify ServerInit structure
assert len(data) >= 16, f"Too short: {len(data)}"
width = int.from_bytes(data[0:2], 'big')
height = int.from_bytes(data[2:4], 'big')
name_len = int.from_bytes(data[12:16], 'big')
assert name_len > 0 and name_len < 1000, f"Invalid name_len: {name_len}"
```

### Debugging Large Data Transfers

For large screens (1080×2400 = ~10MB uncompressed), use receive loop with progress:

```python
expected_size = width * height * 4  # RGBX = 4 bytes/pixel
pixel_data = b''
while len(pixel_data) < expected_size:
    chunk = sock.recv(min(65536, expected_size - len(pixel_data)))
    if not chunk:
        break
    pixel_data += chunk
    if len(pixel_data) % 1000000 == 0:
        print(f"Progress: {len(pixel_data)/expected_size*100:.1f}%")
```

### Verify Complete Transfer

```python
if len(pixel_data) == expected_size:
    print("✅ Complete transfer")
else:
    print(f"❌ Incomplete: {len(pixel_data)}/{expected_size}")
    # Check if server used send() instead of sendall()
```

## macOS Screen Sharing.app Integration

- **Protocol:** VNC/RFB 3.3 (macOS) / 3.8 (standard)
- **Address:** `vnc://localhost:5901`
- **Direction:** Mac → Android (Mac is VNC client)
- **Auth:** VNC Authentication (DES challenge-response) — required by macOS
- **Testing:** `open vnc://localhost:5901` or Screen Sharing.app → Connect
- **Status:** ⚠️ **KNOWN INCOMPATIBLE** — see Session Notes

## Session Notes

- `references/session-2026-08-31.md` — Debug session transcript and test results for niu-cast VNC integration (2026-08-31)
- `references/session-2026-09-03.md` — Extended debugging: RFB 3.3 vs 3.7+ handshake, VNC auth, pixel format, first frame — all fixed but macOS still rejects. Conclusion: abandon VNC for macOS Screen Sharing.app. Adapt DroidMirroring-mac architecture instead.