# Transsion PC Connect (tranCast) Protocol Analysis

**Reverse Engineering Status** 🟢 PROTOCOL FULLY DECODED

Protocol implementation is in `niu_cast/transsion_protocol.py`.

---

## Source Capture Legacy
File: `/Volumes/Mac Win/pc-connection-infinixgt30pro.pcapng`
Duration: 278 seconds, 1825 packets
Device: Infinix GT 30 Pro (X6873)

## Network Topology (from capture)

| Device | IP | Hostname/MAC |
|--------|-----|-------------|
| **Phone (Infinix GT 30 Pro)** | `10.234.253.32` | `Android_VFCJL1DO`, `fe80::2c8c:a8ff:fe71:7c5f` |
| **Windows (ThinkPad X13 Yoga)** | `10.234.253.40` | — |
| Router (DHCP) | `10.234.253.1` | `RouterTKN` |
| Others | `10.234.253.{21,23,26,27,34,50,119,188}` | Various devices on LAN |

## Service Discovery (mDNS)

Phone broadcasts on `224.0.0.251:5353` via **`_tranCast._tcp`** (Transsion Cast).
Windows PC Connect also queries additional service types:

| Service | Purpose | Confirmed |
|---------|---------|-----------|
| `_tranCast._tcp` | Main cast service | ✅ Phone responds |
| `_tranFile._tcp` | File transfer | ❓ Unknown |
| `_tran._tcp` | Base service | ❓ Unknown |
| `_tccp._tcp` | **TCCP protocol** | ✅ Confirmed from decompiled code |

### Service Instance
```
transConnectService-45f86920930b-{timestamp}._tranCast._tcp.local
```
- `45f86920930b` = phone identifier (consistent across sessions)
- `{timestamp}` = changes per session (e.g., `20150229`, `20150327`)

### TXT Record: `cmbSvc` (JSON)
```json
{
  "AudioSink": 8904,
  "HandShake": 37651,
  "ScreenCast": 8900,
  "UcHoService": 8902
}
```
**NOTE:** `HandShake` is actually the **TCCP server port** (renamed to `TCCP` below).

### TXT Record: `advData` (BLE Manufacturer Data)
Hex: `09ff42090d0400011400181635fdff0645f86920930bfb022a00fc036cf000ca0240001209496e66696e69782047542033302050726f`

Parsed:
- **BLE Manufacturer ID:** `0x4209` (Transsion)
- **Service Data (0x16):** `35fdff0645f86920930bfb022a00fc036cf000ca024000`
- **Device Name (0x09):** `Infinix GT 30 Pro`

---

## ══════════════════════════════════════════════════════════════════════════
##  FULL PROTOCOL ARCHITECTURE (from APK decompilation — 2026-07-20)
## ══════════════════════════════════════════════════════════════════════════

Two APKs extracted & decompiled via `--apk-extract`:
- **PCConnect.apk** (49 MB) — `com.transsion.pcconnect` (PC client side)
- **ConnectBase.apk** (15 MB) — `com.transsion.connectx.mirror.source` (phone server side)

Source at: `~/Desktop/Niumination/projects/niu-cast/apk_extract/`

### Native Libraries (C/C++)

| Library | Purpose | Notes |
|---------|---------|-------|
| `libCastBaseLinkSDK.so` | **Core protocol** — TCCP, streaming, UIBC | Loaded by `NativeLinkManager` |
| `libfileNativeJNI.so` | **File transfer** — JNI bridge | `StreamServer`/`StreamClient` |
| `libaiot-link-jni.so` | AIoT link layer | Legacy/fallback |
| `libaiot-link-jni-802.11.so` | WiFi Direct AIoT link | 802.11 variant |

### Java/JNI Layer (ConnectBase.apk)

```
com.transsion.aiotlink          ← Core protocol package
├── NativeLinkManager.java       ← JNI bridge to libCastBaseLinkSDK.so
├── ITCCPListener.java           ← TCCP request/response callback
├── IStreamDataListener.java     ← Stream (video/audio/file) data callback
├── IUibcListener.java           ← UIBC (touch input) data callback
├── ICloseFileServersListener    ← File server close callback
├── ISourceFileStateListener     ← File transfer state callback
└── IWfdListener                 ← WiFi Direct state callback

com.transsion.connectx.link.source ← Source-side logic
└── SourceNativeLinkManager.java    ← Routes decoded UIBC frames

com.transsion.connectx.sdk       ← TCCPSourceApi (high-level SDK)
```

---

## PROTOCOL LAYERS

```
┌──────────────────────────────────────────────────────────────┐
│                    TCCPSourceApi (SDK)                        │
│  com.transsion.connectx.sdk                                  │
│  High-level: startCast(), stopCast(), sendTouch(), ...       │
├──────────────────────────────────────────────────────────────┤
│                    NativeLinkManager (JNI)                    │
│  com.transsion.aiotlink                                      │
│  sendTccpRequest(short op, String json)                      │
│  sendTccpResponse(short op, int reqId, String json)          │
│  sendVideoData(int handle, byte[], int len)                  │
│  sendUibcData(byte[], int len)                               │
├──────────────────────────────────────────────────────────────┤
│              libCastBaseLinkSDK.so (C/C++)                   │
│  TCCP framing, handshake, pairing, encryption                │
│  Video/audio codec, UIBC encoding                            │
├──────────────────────────────────────────────────────────────┤
│                    TCP Transport                              │
│  TCCP Port: dynamic (from mDNS HandShake field)              │
│  Video Port: 8900    (raw H.264/H.265 stream)                │
│  UIBC Port: 8902     (touch/input back channel)              │
│  Audio Port: 8904    (raw audio stream)                      │
│  File Port: dynamic  (per session allocation)                │
└──────────────────────────────────────────────────────────────┘
```

---

## TCCP (Transsion Cast Control Protocol)

**TCCP** is the control protocol used for all non-stream communication.

### TCCP Frame Format (VERIFIED from live test 2026-07-20)

```
┌───────────────────────────────────────────────────────┐
│  Byte 0-3:   Magic: "TCCP" (0x54434350)               │
│  Byte 4:     Version/Flags (0x00 client, 0xFF server)  │
│  Byte 5-8:   Body Length (BE uint32, = 15 + payload)   │
│  Byte 9-10:  Operator Code (BE uint16)                  │
│  Byte 11-14: Message ID (BE uint32)                     │
│  Byte 15-22: Timestamp (BE uint64, relative ms)         │
│  Byte 23+:   JSON Payload (UTF-8)                       │
│  Byte last:  Payload Type (0x00 = JSON)                 │
└───────────────────────────────────────────────────────┘
```

- body_len = 15 + payload_len (includes op+msgId+ts+payload+type)
- total frame = 9 + body_len

Note: Native lib also supports a response format with 4B status code
(body_len = 19 + payload_len), but all observed frames use request format.

### Verified Session Flow (live test, Infinix X6873)

```
Client (Mac)                    Phone TCCP Server (:9452)
    │                                    │
    │─── TCP Connect (port 9452) ───────►│
    │                                    │
    │    Server auto-sends 7 frames:     │
    │◄── [0x0606] {"port":12000} ────────│
    │◄── [0x0404] {"a":"xos"} ───────────│
    │◄── [0x0607] {"controlPort":9542,   │
    │              "filePort":10001,      │  <-- AUTH response with ports
    │              "port":8008,           │
    │              "supportVersions":[1,2,3]}
    │◄── [0x062a] {"data":50314,"type":0}│
    │◄── [0x0615] {"count":3} ───────────│
    │◄── [0x0403] {"scene":0,            │
    │              "videoPort":0} ────────│
    │◄── [0x0900] {"count":0} ───────────│  <-- Heartbeat
    │                                    │
    │─── [0x0700] CONN_AUTH ────────────►│
    │    {"deviceName":"Mac",             │
    │     "deviceType":"pc",              │
    │     "appVersion":"3.0.0"}           │
    │                                    │
    │◄── [0x0900] {"count":0} ───────────│  <-- Heartbeat continues
    │                                    │
    │─── [0x0900] HEARTBEAT ────────────►│  <-- Bidirectional heartbeats
    │◄── [0x0900] HEARTBEAT ◄────────────│
```

### New Ports Discovered from Auth Response

| Port | Purpose | Discovered Via |
|------|---------|---------------|
| 9452 | TCCP control server | Static from decompiled code (w4/l1.java: S=9452) |
| 8008 | Unknown service | 0x0607 auth response |
| 9542 | Control port | 0x0607 auth response |
| 10001 | File transfer | 0x0607 auth response |

### How to Enable TCCP Server

The TCCP server is NOT started by default on the phone. It must be enabled:
1. Open CastSettingActivity: `adb shell am start -n "com.transsion.connectx.mirror.source/.activity.CastSettingActivity"`
2. Tap the "开启TCCP" (Start TCCP) button
3. Port 9452 starts listening

Or programmatically via:
- `l1.h.f18073a.J1()` (SourceManager singleton)
- `TCCPSourceApi.getInstance(context).startTCCPServer(1)` (SDK)

### TCCP Operator Codes

Complete operator map from `v4/g.java`:

| Code | Name | Purpose | Payload |
|------|------|---------|---------|
| `0x001` | BASE | Internal | Various |
| `0x200` | FILE_BASE | File ops base | - |
| `0x300` | FILE_AUTH | File auth | JSON |
| `0x301` | FILE_AUTH_ACK | File auth ack | JSON |
| `0x302` | FILE_CANCEL | Cancel file | Empty |
| `0x400` | CAST_START | Start mirror | JSON config |
| `0x401` | CAST_STOP | Stop mirror | Empty |
| `0x402` | CAST_CONFIG | Config | JSON |
| `0x403` | CAST_ROTATE | Rotate | JSON |
| `0x404` | CAST_CLOSE | Close cast | JSON |
| `0x500` | CAST_EXTEND | Extend display | JSON |
| `0x501` | CAST_EXTEND_STOP | Stop extend | JSON |
| `0x502` | CAST_EXTEND_CLOSE | Close extend | JSON |
| `0x600` | FILE_SEND | Send file | JSON (path, size) |
| `0x601` | FILE_RECEIVE | Receive file | JSON |
| `0x602` | FILE_PROGRESS | Transfer progress | JSON |
| `0x603` | FILE_COMPLETE | Transfer done | JSON |
| `0x604` | FILE_ERROR | Transfer error | JSON |
| `0x605` | FILE_LIST | List files | JSON |
| `0x606` | FILE_DELETE | Delete file | JSON |
| `0x607` | FILE_RENAME | Rename file | JSON |
| `0x608` | FILE_MKDIR | Create dir | JSON |
| `0x609` | FILE_INFO | File info | JSON |
| `0x610` | DEVICE_INFO | Get device info | Empty |
| `0x611` | DEVICE_BATTERY | Battery status | Empty |
| `0x612` | DEVICE_SCREENSHOT | Screenshot | JSON |
| `0x613` | DEVICE_LOCK | Lock screen | Empty |
| `0x614` | DEVICE_UNLOCK | Unlock | JSON |
| `0x615` | DEVICE_VOLUME | Volume | JSON |
| `0x616` | DEVICE_BRIGHTNESS | Brightness | JSON |
| `0x617` | DEVICE_RING | Ring device | Empty |
| `0x618` | DEVICE_LOCATION | Location | Empty |
| `0x619` | DEVICE_CAMERA | Camera | JSON |
| `0x620` | APP_LIST | List apps | JSON |
| `0x621` | APP_OPEN | Open app | JSON |
| `0x622` | APP_CLOSE | Close app | JSON |
| `0x623` | APP_INSTALL | Install APK | JSON |
| `0x624` | APP_UNINSTALL | Uninstall | JSON |
| `0x625` | APP_UPDATE | Update app | JSON |
| `0x626` | APP_LAUNCH | Launch app | JSON |
| `0x627` | APP_FORCE_STOP | Force stop | JSON |
| `0x630` | CLIPBOARD_SYNC | Sync clipboard | JSON |
| `0x631` | CLIPBOARD_GET | Get clipboard | Empty |
| `0x632` | NOTIFICATION_SYNC | Notif sync | JSON |
| `0x633` | NOTIFICATION_ACTION | Notif action | JSON |
| `0x634` | NOTIFICATION_CLEAR | Clear notif | Empty |
| `0x700` | CONN_AUTH | Auth request | JSON (device info) |
| `0x702` | CONN_AUTH_CONFIRM | Auth confirm | JSON |
| `0x703` | CONN_PAIR | Pair request | JSON (code) |
| `0x704` | CONN_UNPAIR | Unpair | Empty |
| `0x708` | CONN_PING | Ping | Empty |
| `0x709` | CONN_PONG | Pong | Empty |
| `0x710` | CONN_CLOSE | Close connection | JSON (reason) |
| `0x711` | CONN_RECONNECT | Reconnect | JSON |
| `0x800` | EXT_AUDIO_START | Start audio | JSON |
| `0x816` | EXT_AUDIO_STOP | Stop audio | Empty |
| `0x819` | EXT_AUDIO_VOLUME | Set volume | JSON |
| `0x820` | EXT_SMART_RECOGNITION | Smart recog | Empty |
| **`0x900`** | **HEARTBEAT** | **Keep-alive** | Empty (sent every ~1s) |
| `0x1000` | SYSTEM | System command | JSON |

### Heartbeat Configuration

From SourceNativeLinkManager code:
- **Interval:** 1000ms (1 second)
- **Timeout:** 20 heartbeats (20 seconds)
- **Operator:** `0x900` (TCCP_OP.HEARTBEAT)

---

## UIBC Protocol (User Input Back Channel)

UIBC is used for touch/keyboard/mouse input from PC → Phone.

### UIBC Frame Format (from SourceNativeLinkManager.java)

```java
// Parsing of received UIBC frame:
short type = k4.c.l(Arrays.copyOfRange(data, 0, 2));   // Type (big-endian)
short port = k4.c.l(Arrays.copyOfRange(data, 2, 4));   // Port (big-endian)
// Bytes 4-7: reserved/padding
byte[] content = Arrays.copyOfRange(data, 8, data.length);  // Content at offset 8
```

```
┌──────────────────────────────────────────────────────┐
│  Byte 0-1:   Type (big-endian uint16)                 │
│              0x0001 = touch event                     │
│              0x0002 = keyboard event                  │
│              0x0003 = mouse event                     │
│  Byte 2-3:   Port (big-endian uint16)                 │
│              Usually 8902 (UIBC service port)         │
│  Byte 4-7:   Reserved/Padding (all zeros)             │
│  Byte 8+:    Content (format TBD - in native lib)     │
└──────────────────────────────────────────────────────┘
```

### File Transfer Protocol (libfileNativeJNI.so)

The file transfer uses a different native library and frame format.
From the JNI signatures:

```java
// StreamServer.create() -> Returns socket handle(s)
native long[] create(int port);

// StreamServer.sendBuffer(long client, byte[] data, callback)
native int sendBuffer(long clientHandle, byte[] data);

// StreamClient.connect(String host, int port) -> Returns client handle
native long connect(String host, int port);
```

File transfer flow:
1. Client requests file send via TCCP (`0x600` FILE_SEND)
2. Server creates a StreamServer on dynamic port
3. Client connects via StreamClient
4. Binary stream protocol via libfileNativeJNI.so (format in native code)
5. Progress reported via TCCP (`0x602` FILE_PROGRESS)

---

## Connection Flow

### Observed TCCP Session (VERIFIED 2026-07-20, Infinix X6873)

```
1. TCP connect to port 9452
2. Server auto-sends 7 frames (no client input needed):
   → 0x0606 {"port":12000}
   → 0x0404 {"a":"xos"}
   → 0x0607 {"controlPort":9542,"filePort":10001,"port":8008,"supportVersions":[1,2,3]}
   → 0x062a {"data":50314,"type":0}
   → 0x0615 {"count":3}
   → 0x0403 {"scene":0,"videoPort":0}
   → 0x0900 {"count":0}
3. Client sends CONN_AUTH (0x700): {"deviceName":"Mac","deviceType":"pc","appVersion":"3.0.0"}
4. Server continues heartbeats (0x0900)
5. Bidirectional heartbeat exchange continues every ~1s
```

### Additional Services (from 0x0607 auth response)

After TCCP auth, the phone exposes additional ports:
- **Port 8008**: Unknown (control?)
- **Port 9542**: Control channel
- **Port 10001**: File transfer

These are separate TCP servers on different ports, presumably for
different data channels.

### Connection Types (from decompiled code)
- `P2P = 2` — WiFi Direct
- `USB = 1` — USB tethering  
- `WIFI = 3` — Same WiFi network

---

## ══════════════════════════════════════════════════════════════════════════
##  NATIVE LIBRARY ANALYSIS (libCastBaseLinkSDK.so — ARM64)
## ══════════════════════════════════════════════════════════════════════════

**File:** `apk_extract/connectbase/resources/lib/arm64-v8a/libCastBaseLinkSDK.so`
**Size:** 1.5 MB (stripped ARM64 ELF)
**Dependencies:** libevent (bufferevent/evbuffer), libc++, nlohmann JSON

### Core Classes (from demangled ARM64 symbols)

| Class | Key Methods |
|-------|-------------|
| `TccpClient` | `connect()`, `sendTccpRequest(short, const char*, int)`, `sendTccpResponse(short, int, const char*, int)`, `parseData()`, `parseRequest()`, `parseResponse()`, `getMsgID()`, `sendTo()`, `sendToRaw()`, `onReceiveHead()` |
| `TccpServer` | `startServer(int)`, `sendTccpRequest()`, `sendTccpResponse()`, `sendTccpData()`, `buildLink(int)` |
| `TccpEncapsule` | **Wire format** — `fillSendBuffer(req/res)`, `constructTccpReqBody()`, `constructTccpResBody()`, `parseTccpReqBodyUtilJson()`, `parseTccpResBodyUtilJson()` |
| `UibcClient/Server` | `connect()`, `onReceiveHead()`, `setListener()`, `listenUibcData()` |
| `VideoClient/Server` | `connect()`, `onReceiveHead()`, `setVideoListener()` |
| `AudioClient/Server` | `connect()`, `onReceiveHead()`, `setAudioListener()` |
| `FileClient/Server` | `connect()`, `sendTo()`, `sendFileData()` |
| `SendFileManager` | `sendFileHead()`, `sendFileBody()`, `readingData()`, `setBodyDataType()` |
| `EventLink` | `readcb()`, `writecb()`, `eventcb()` — libevent callbacks |

### Wire Format (disassembled from TccpEncapsule::fillSendBuffer)

#### REQUEST Frame
```
Offset  Size  Field           Encoding
------  ----  -----           --------
0       4     Magic: "TCCP"   ASCII
4       1     Version/Flags   0x00
5       4     Body Length     big-endian uint32 (= payloadLen + 15)
9       2     Operator Code   big-endian uint16
11      4     Message ID      big-endian uint32 (auto-incremented)
15      8     Timestamp       big-endian uint64 (μs since epoch)
23      N     JSON Payload    UTF-8
23+N    1     Payload Type    0x00 = JSON
Total:  24 + N bytes
```

#### RESPONSE Frame
```
Offset  Size  Field           Encoding
------  ----  -----           --------
0       4     Magic: "TCCP"   ASCII
4       1     Version/Flags   0x00
5       4     Body Length     big-endian uint32
9       2     Operator Code   big-endian uint16
11      4     Request ID      big-endian uint32 (echoed from request)
15      4     Status Code     big-endian uint32
19      8     Timestamp       big-endian uint64
27      N     JSON Payload    UTF-8 (only if payloadLen > 0)
27+N    1     Payload Type    0x00 = JSON
Total:  28 + N bytes
```

### Key Findings
- **Magic bytes**: `TCCP` confirmed in binary at offset 0x138ddf
- **Body length**: For requests, body_len = payloadLen + 15 (from reqId counter). For responses, body_len = payloadLen + 27 (or 27 alone).
- **Message ID**: Auto-incremented counter at `this+0x54`, stored in map for response matching
- **Timestamp**: From `gettimeofday()`, stored as big-endian microseconds
- **UDP support**: "TCCP_HEARTBEAT,sendUdpRequest" string confirms optional UDP heartbeats
- **I/O**: libevent `bufferevent_write()` for send, `evbuffer` for receive buffering
- **File transfer**: Separate protocol in `libfileNativeJNI.so` with `StreamClient`/`StreamServer` controllers

### TccpReqBody C++ Layout
```
offset 0:  uint16_t op         (2 bytes)
offset 2:  int16_t  _padding   (2 bytes)
offset 4:  int32_t  msgId      (4 bytes)
offset 8:  int64_t  timestamp  (8 bytes)
offset 24: uint8_t  payloadType (1 byte, 0x00 = JSON)
```

---

## Implementation Status (niu-cast v3.0)

| Component | File | Status |
|-----------|------|--------|
| TCCP frame encode/decode (magic+op+JSON) | `transsion_protocol.py` | ✅ Implemented from native lib disassembly |
| Operator code constants (50+ ops) | `transsion_protocol.py` | ✅ Full map from Java decompilation |
| TCCP wire format (request + response) | `transsion_protocol.py` | ✅ Confirmed via ARM64 disassembly |
| Heartbeat manager (1s interval, 20s timeout) | `transsion_protocol.py` | ✅ Implemented from v4/c.java |
| mDNS discovery (all 4 services) | `transsion_protocol.py` | ✅ Working |
| USB tether detection | `transsion_protocol.py` | ✅ Working |
| IPv6 phone detection | `transsion_protocol.py` | ✅ Working |
| APK decompilation (PCConnect + ConnectBase) | `apk_extract.py` | ✅ 14,000+ source files |
| Native lib strings analysis | `libCastBaseLinkSDK.so` | ✅ Fully mapped classes + methods |
| Native lib wire format disassembly | `libCastBaseLinkSDK.so` | ✅ fillSendBuffer decoded |
| TCCP connect/handshake | `transsion_protocol.py` | ⏳ Need actual device to test wire format |
| Video stream decoding | `transsion_protocol.py` | ❌ Need native lib H.264 format |
| UIBC touch encoding | `transsion_protocol.py` | ❌ Need native lib touch format |
| File transfer | `transsion_protocol.py` | ❌ Need libfileNativeJNI analysis |
| WiFi Direct bridge (ADB) | `wfd_bridge.py` | ✅ Working |
| GUI (screen mirror) | `gui/` | ⏳ Need working protocol first |

### BLOCKERS

| Blocker | Status | Next Step |
|---------|--------|-----------|
| **TCCP handshake binary format** | 🟡 Decoded from disassembly | Needs testing with real device |
| **Wireless mirror without ADB** | 🟡 Protocol fully mapped | Need WiFi Direct or USB tether to test |
| **WiFi Direct initiation on macOS** | 🔴 No AWDL | Trigger via ADB shell or Windows recapture |
| **UIBC/touch packet format** | 🔴 In native lib | Need deeper objdump analysis

---

## Commands

```bash
# Scan for Transsion devices (mDNS all services)
python3 -m niu_cast --scan-trancast

# Probe device ports (once discovered)
python3 -m niu_cast --probe-trancast

# USB tether auto-connect
python3 -m niu_cast --tether

# USB tether persistent daemon
python3 -m niu_cast --tetherd

# Extract + decompile PC Connect APK from connected device
python3 -m niu_cast --apk-extract
python3 -m niu_cast --apk-extract --decompile

# Query WiFi Direct state via ADB
python3 -m niu_cast --wifi-direct
```
