---
name: vnc-server-python
description: >
  Implement VNC/RFB server in Python + ADB integration.
---

# VNC Server Python — RFB Protocol + ADB Integration

## Trigger

Gunakan skill ini saat:

- Membuat VNC server dari nol di Python (RFB protocol)
- Screen mirror / screen casting yang targetnya macOS Screen Sharing.app
- Forward mouse/keyboard dari VNC client ke Android via ADB
- RFB version negotiation, ServerInit, atau FramebufferUpdate bermasalah
- Integrasi ADB screen capture dengan VNC frame streaming
- RFB keycode perlu mapping ke Android keycode

---

## RFB Protocol Reference (V3.8)

### Handshake Singkat

1. **Version:** Server → `"RFB 003.008\n"` (12 bytes). Client balas 12 bytes.
2. **Security:** Server → `num_types (1B) + types[]`. PoC: `num=1, type=1`. Client pilih 1 byte.
3. **Auth:** Server → `0x00` (success). Skip untuk PoC.
4. **ClientInit:** Client → `shared_flag (1B) + name_len (4B) + name`.
5. **ServerInit:** Server → `width (2B) + height (2B) + bpp (1B) + depth (1B) + big_endian (1B) + true_color (1B) + rgb_max (3B) + rgb_shift (3B) + padding (3B) + name_len (4B) + name`.

**Struct ServerInit (tanpa name):**
```python
struct.pack('!HHBBBBHH', width, height, bpp, depth, 
            big_endian_flag, true_color_flag,
            red_max, green_max,  # 255 untuk 8-bit
            red_shift, green_shift, blue_shift,  # shift 16/8/0 untuk 24bpp
            padding1, padding2)
```

### FramebufferUpdate

```
message_type (1B) = 0
padding (1B) = 0
number_of_rectangles (2B)
```

Per rect:
```
encoding_type (2B) = 0 (Raw)
x (2B) + y (2B) + width (2B) + height (2B)
pixel_data (w * h * bpp)
```

**PENTING:** Kirim FB header (3B) → rect header (12B) → pixel data. Jangan gabung dalam satu struct.

### Input Events

**KeyEvent (msg_type=3):**
```
type (1B) = 3
down_flag (1B) = 0/1
padding (2B)
keycode (4B)  # RFB virtual keycode
```

**PointerEvent (msg_type=4):**
```
type (1B) = 4
button_mask (1B)  # bit 2 (0x40) = left click
x (2B) + y (2B)
```

Jika `button_mask & 0x40`: kirim tap di (x, y). Jika tidak ada button: skip (ADB tidak support move tanpa click).

---

## RFB → Android Keycode Mapping

```python
rfb_to_android = {
    1: 7, 2: 8, 3: 19, 4: 20, 5: 21, 6: 22, 7: 13, 8: 12,
    9: 15, 10: 14, 11: 92, 12: 93, 13: 67, 14: 66, 15: 4,
    16: 29, 17: 30, 18: 31, 19: 32, 20: 33, 21: 34, 22: 35,
    23: 36, 24: 37, 25: 38, 26: 39, 27: 40, 28: 41, 29: 42,
    30: 43, 31: 44, 32: 45, 33: 46, 34: 47, 35: 48, 36: 49,
    37: 50, 38: 51, 39: 52, 40: 53, 41: 54, 42: 7, 43: 8,
    44: 9, 45: 10, 46: 11, 47: 12, 48: 13, 49: 14, 50: 15,
    51: 16, 65: 97, 66: 98, 67: 99, 68: 100, 69: 101, 70: 102,
    71: 103, 72: 104, 73: 105, 74: 106, 75: 107, 76: 108,
    77: 109, 78: 110, 79: 111, 80: 112, 81: 113, 82: 114,
    83: 115, 84: 116, 85: 117, 86: 118, 87: 119, 88: 120,
    89: 121, 90: 122, 91: 66, 92: 7, 93: 8, 94: 9, 95: 10,
    127: 67
}
# Fallback ASCII: 0x20 <= rfb_keycode <= 0x7E → return keycode
```

---

## ADB Integration

**Screen capture (PNG → raw RGB):**
```python
result = subprocess.run(
    [adb_path, "-s", serial, "shell", "screencap", "-p"],
    capture_output=True, timeout=5
)
# PIL: Image.open(io.BytesIO(result.stdout)).convert('RGBA').tobytes()
```

**Input forwarding:**
```python
# Key: input keyevent <keycode>
# Tap: input tap <x> <y>
# Swipe: input swipe <x1> <y1> <x2> <y2> <duration_ms>
```

---

## VNC Server Skeleton (Minimal)

```python
class VNCAdapter:
    def __init__(self, port=5901, width=1080, height=2400):
        self.port = port
        self.width = width
        self.height = height
        self.running = False
        self.clients = []
    
    def start_server(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen(5)
        self.running = True
        threading.Thread(target=self._accept_loop, daemon=True).start()
    
    def _accept_loop(self):
        while self.running:
            client, addr = self.sock.accept()
            self.clients.append(client)
            threading.Thread(target=self._handle_client, args=(client, addr), daemon=True).start()
    
    def _handle_client(self, client, addr):
        # 1. Version: send "RFB 003.008\n", recv 12B
        # 2. Security: send !BB 1 1, recv 1B
        # 3. Auth: send 0x00
        # 4. ClientInit: recv up to 128B
        # 5. ServerInit: send struct + name
        # 6. Main loop: recv msg_type, handle FB request / KeyEvent / PointerEvent
        pass
    
    def _send_frame(self, client):
        # Kirim FB header + rect header + pixel data
        pass
    
    def _rfb_keycode_to_android(self, rfb_keycode):
        # return rfb_to_android.get(rfb_keycode) or (0x20-0x7E fallback)
        pass
```

---

## Phase-Gated Development

Fitur besar (contoh: VNC mode di niu-cast) → 5 phase, commit per fase:

| Phase | Target | Commit |
|-------|--------|--------|
| 1. PoC | RFB server jalan, koneksi diterima | `feat(vnc): PoC` |
| 2. ADB | Screen capture real → VNC frames | `feat(vnc): ADB integration` |
| 3. Input | Mouse/keyboard dari VNC → ADB | `feat(vnc): input forwarding` |
| 4. GUI | Tab VNC di PyQt5, settings | `feat(vnc): GUI integration` |
| 5. Release | Optional mode di v3.x | `release: v3.7` |

---

## macOS Screen Sharing.app — Known Incompatibility

**Fakta empiris (test 3 Sep 2026):** Setelah fix RFB 3.3/3.8 handshake, VNC Authentication (DES challenge-response), pixel format (BGRX, LE=0, TC=1, shifts 16/8/0), dan kirim frame pertama segera — macOS Screen Sharing.app **TETAP REJECT** dengan error "perangkat lunak tidak compatibel".

**Root cause:** macOS Screen Sharing.app require proprietary VNC extensions yang tidak diimplementasikan oleh Python VNC server pada umumnya:
- Pseudo-encodings macOS-specific (Rect menus, Screen Cursor encoding)
- Strict security handshake negotiation yang berbeda dari VNC clients lain (RealVNC, TigerVNC)
- Kemungkinan butuh "Extended Desktop Size" pseudo-encoding untuk multi-monitor

**Bukti:** VNC server jalan, TCP connect diterima, handshake sampai ServerInit complete — tapi macOS putus koneksi sebelum/saat FramebufferUpdate pertama.

**Implikasi:** Jangan buang waktu debugging VNC server Python untuk macOS Screen Sharing.app. Pendekatan ini **tidak reliable** untuk target macOS native client.

### RFB 3.3 vs 3.7+ Handshake Difference

macOS Screen Sharing.app uses RFB 3.3, which has a **different security handshake** from 3.7+:

**RFB 3.3/3.5 (macOS):**
```
Server → 1 byte: security type (1 = None, 2 = VNC Auth)
If VNC Auth: Server → 16 bytes challenge → Client → 16 bytes response
NO security result sent!
```

**RFB 3.7+ (standard):**
```
Server → 1 byte: num_types → N bytes: types[]
Client → 1 byte: selected type
Server → 4 bytes: security result (0 = OK, 1 = Failed)
```

**CRITICAL:** Sending a security result byte in 3.3 handshake causes macOS to reject the connection. The extra byte shifts all subsequent parsing.

**Alternatives untuk Android → Mac mirroring:**

| Metode | Status | Butuh USB Debugging? | Catatan |
|---|---|---|---|
| `adb pair` + `adb connect` + `scrcpy` | ✅ Bisa test | ❌ (tapi perlu Developer Options aktif) | Android 11+ Wireless Debugging, pairing via QR code di Developer Options |
| Mac Connect Bridge (niu-cast) | ✅ Proven | ✅ (sekali setup) | ADB + scrcpy, jalan di ekosistem |
| joy-connect-for-mac | ⚠️ Build pending | ✅ (sekali) | Swift native app, perlu Xcode (mesin ini hanya punya CommandLineTools) |
| Joy Connect QR (niu-cast) | ⚠️ Experimental | ❌ | Protocol Transsion reverse-engineering, belum stabil |

## Pitfalls

### IndentationError di file besar pasca tambah GUI tab

**Penyebab:** Kode baru (misal tab VNC) disisipkan di dalam `__init__` body (8-space) padahal harusnya class-level (4-space). Transisi dari method-body ke class-method tanpa blank line yang benar bikin Python bingung.

**Gejala:** `IndentationError: unexpected indent` di baris yang seharusnya level class tapi ada di dalam method.

**Debug:**
```bash
python3 -c "import py_compile; py_compile.compile('file.py', doraise=True)"
```

**Fix manual:** Cari baris dengan `def ` yang tidak punya indented block di bawahnya. Cek indentasi sekelilingnya — harus konsisten (4-space untuk class methods, 8-space untuk method body).

**Pencegahan:** Kalau nambah tab di PyQt5, simpan file, test compile, lalu commit sebelum lanjut edit yang lain.

---

## Pitfalls (Lanjutan)

### Name Length di ServerInit

Kirim `len(name.encode('utf-8'))` di struct, bukan `len(name)`. Kalau beda, client disconnect.

### Screen Resolution Change

Kalau device rotate, update width/height. ServerInit bisa dikirim ulang atau client restart koneksi.

### Tanpa ADB Device

- Screen capture → None/null. Handler: kirim black frame atau static placeholder.
- Input → gagal. Handler: skip processing, cek device sebelum handle event.

---

## Verification

### Cek syntax:
```bash
python3 -c "import py_compile; py_compile.compile('file.py', doraise=True)"
```

### Test VNC server:
```bash
python3 -c "
from vnc_adapter import VNCAdapter
vnc = VNCAdapter(port=5902)
vnc.start_server()
import time; time.sleep(2)  # keep alive for testing
"
# Connect via Screen Sharing.app → vnc://localhost:5902
```

### Test ADB integration:
```bash
python3 -c "
import subprocess
result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
print(result.stdout)  # cek device terhubung
"
```

---

*Last updated: 2026-08-31 — dari session niu-cast VNC mode implementation*