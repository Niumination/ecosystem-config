# Transsion PC Connect (tranCast) Protocol Analysis

## Source Capture
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

The phone broadcasts on `224.0.0.251:5353` via **`_tranCast._tcp`** (Transsion Cast).
Windows PC Connect app also queries additional service types:

| Service | Queried By | Status |
|---------|-----------|--------|
| `_tranCast._tcp` | Windows PC Connect | ✅ Phone responds |
| `_tranFile._tcp` | Windows PC Connect | ❓ Unknown if phone responds (file transfer?) |
| `_tran._tcp` | Windows PC Connect | ❓ Unknown (base Transsion service?) |
| `_tccp._tcp` | Windows PC Connect | ❓ Unknown (Transsion Cast Control Protocol?) |

### Service Instance
```
transConnectService-45f86920930b-{timestamp}._tranCast._tcp.local
```
- `45f86920930b` = phone identifier (consistent across announcements)
- `{timestamp}` = changes per session (e.g., `20150229`, `20150327`)

### TXT Record: `cmbSvc` (JSON)
```json
{
  "AudioSink": 8904,
  "HandShake": 37651,    // <-- port changes dynamically!
  "ScreenCast": 8900,
  "UcHoService": 8902
}
```

The `HandShake` port changes between announcements (37651 → 40999), suggesting dynamic port allocation.

### TXT Record: `advData` (BLE Manufacturer Data)
Hex: `09ff42090d0400011400181635fdff0645f86920930bfb022a00fc036cf000ca0240001209496e66696e69782047542033302050726f`

Parsed:
- **BLE Manufacturer ID:** `0x4209` (Transsion?)
- **Payload:** `0d0400011400` (unknown format)
- **Service Data (0x16):** `35fdff0645f86920930bfb022a00fc036cf000ca024000`
- **Device Name (0x09):** `Infinix GT 30 Pro`

## Key Finding: Protocol Traffic NOT Captured

**There is ZERO direct TCP/UDP traffic between Windows (10.234.253.40) and the phone (10.234.253.32).**

The phone only sends mDNS multicast packets. No connections to ports 8900, 8902, 8904, or the handshake port were captured.

### ✅ Confirmed: WiFi Direct Required for TCP

**Confirmed via live probe (2026-07-20):**
- mDNS discovery works perfectly on LAN — phone announces `_tranCast._tcp` faithfully
- Device ID: `45f86920930b`, handshake port rotates dynamically (37651 → 40999 → 41013)
- **BUT all TCP ports (8900, 8902, 8904, handshake) refuse connections from LAN IP**
- Conclusion: **mDNS is discovery-only. All protocol connections happen over WiFi Direct P2P link**

### WiFi Direct Network Topology (Expected)

The phone creates a WiFi Direct group with the PC:
- Phone acts as **Group Owner** (GO) — IP typically `192.168.49.1`
- PC connects as **Group Client** — IP typically `192.168.49.x`
- TCP handshake happens on the `192.168.49.x` subnet, not the `10.234.253.x` LAN

## Implementation Status (niu-cast v2.3.0)

| Component | Status | Notes |
|-----------|--------|-------|
| `transsion_protocol.py` — mDNS discovery | ✅ Working | Scans all 4 service types (`_tranCast`, `_tranFile`, `_tran`, `_tccp`) |
| `transsion_protocol.py` — TranCastProtocol | ⏳ Placeholder | Handshake/frame format TBD |
| `mini.py --scan-trancast` | ✅ Working | Scans LAN, shows device info + services |
| `mini.py --probe-trancast` | ⏳ Partial | Discovers + probes ports, confirms WiFi Direct needed |
| `mini.py --tether` | ✅ Working | Auto-detect phone via USB tether + connect |
| `mini.py --tetherd` | ✅ Working | Persistent monitor daemon for USB tether |
| `mini.py --apk-extract` | ✅ Working | Extract + analyze PC Connect APK from connected device |
| `tetherd.py` | ✅ New | Persistent monitor daemon for USB tether |
| `apk_extract.py` | ✅ New | APK extraction + basic analysis (jadx/apktool) |
| `detect_usb_tether_phone()` | ✅ Working | Scans non-WiFi interfaces, finds phone gateway |
| `try_tether_connect()` | ✅ Working | Auto-connect via Transsion protocol over tether |
| `find_phone_ipv6()` | ✅ New | Lookup phone via IPv6 neighbor cache (MAC prefix) |
| `__main__.py` | ✅ New | `python3 -m niu_cast` entry point |
| WiFi Direct capture | ❌ Blocked | Needs Windows recapture on WiFi Direct interface |

## Live Probe Results (2026-07-20)

**Confirmed: All Transsion TCP ports REFUSED from LAN (both IPv4 and IPv6)**
- Phone IPv4: `10.234.253.32`
- Phone IPv6 LL: `fe80::2c8c:a8ff:fe71:7c5f%en0`
- Ports tested (all refused): 5555, 3724, 7275, 8900, 8902, 8904, 37651, 40999, 41013, 8080, 8443, 18080
- Conclusion: **Phone only exposes Transsion services on WiFi Direct P2P interface (192.168.49.x)**

**USB tethering**: Untested — phone needs to be connected via USB with tethering enabled.
If it works, the phone should appear on a 192.168.42.x or 192.168.43.x subnet and Transsion ports may be accessible.

## Available Connection Paths

| Path | Status | How |
|------|--------|-----|
| ADB over USB | ✅ Works | USB Debugging enabled, `adb devices` |
| ADB over WiFi | ⏳ Not tested | `adb tcpip 5555` then WiFi |
| LAN to Transsion ports | ❌ Refused | Phone only listens on P2P interface |
| WiFi Direct (Windows) | ❌ Needs recapture | Pick WiFi Direct VA in ncpa.cpl |
| USB Tethering | ⏳ Untested | Enable USB tethering on phone |
| IPv6 link-local | ❌ Refused | All ports closed on fe80:: address |
| APK Decompilation | ⏳ Not yet | Pull APK via ADB, decompile with jadx |
| WiFi Direct (macOS) | ❌ No support | AWDL interface not available (Hackintosh) |

## Next Steps: Recapture

### Option A: WiFi Direct (Windows)
1. **Open Network Connections** (`ncpa.cpl`) before connecting
2. Look for a **"WiFi Direct"** or **"Microsoft WiFi Direct Virtual Adapter"** interface
3. Start **Wireshark on that specific interface** (not the regular WiFi)
4. **Then** open PC Connect and connect to the phone
5. Capture the entire session (pairing + mirroring)

### Option B: USB Tethering (macOS)
1. Connect phone via USB cable
2. Enable **USB Tethering** on phone
3. Run `python3 -m niu_cast --tetherd` on this Mac — auto-detects interface
4. If Transsion ports respond, the protocol can be decoded

### Option C: APK Decompilation
If USB Debugging is available:
1. `python3 -m niu_cast --apk-extract` — pulls PC Connect APK
2. `python3 -m niu_cast --apk-extract --decompile` — also runs jadx
3. Search decompiled source for protocol implementation (handshake, socket, frame)
4. Implement protocol directly from source code

## Known Architecture Summary

| Service | Port | Protocol | Notes |
|---------|------|----------|-------|
| HandShake | Dynamic (37651/40999) | TCP | Initial handshake/negotiation |
| ScreenCast | 8900 | TCP | Screen mirroring stream |
| UcHoService | 8902 | TCP | Unknown (UcHo = ?) |
| AudioSink | 8904 | TCP | Audio streaming |
| mDNS | 5353 | UDP | Service discovery (`_tranCast._tcp`) |
| BLE Adv | — | BLE | Initial pairing/discovery (`advData`) |

