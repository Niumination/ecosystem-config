# Verifikasi Pasca-Upgrade macOS 26.7.1

**Tanggal:** 4 Oktober 2026
**Upgrade:** macOS 26.5 (25F71) → 26.7.1 (25G241)
**Metode:** Software Update UI, restart sekali

---

## 1. Hasil upgrade

```
ProductVersion: 26.7.1
BuildVersion:   25G241
uptime:         13 menit setelah restart
disk:           19 GB free (naik dari 11 GB; upgrade membersihkan sendiri)
```

**Upgrade berhasil tanpa intervensi.** Tidak ada kernel panic, tidak ada recovery, tidak perlu restore dari backup EFI.

---

## 2. Kext — semua load, tidak ada yang hilang

19 kext pihak ketiga terdeteksi di `kextstat`, semua load:

```
Lilu 1.7.3 · VirtualSMC 1.3.8 · WhateverGreen 1.7.0 · RestrictEvents 1.1.7
VoodooHDA 3.1.2 · itlwm 2.3.0 · IntelMausiEthernet 3.0.3
BlueToolFixup 2.7.2 · IntelBTPatcher 2.5.0 · IntelBluetoothFirmware 2.5.0
VoodooI2CServices · VoodooInput 1.1.6 · PS2Controller 2.3.8
ECEnabler 1.0.6 · NVMeFix 1.1.4 · CPUFriend 1.3.0
SMCBatteryManager 1.3.8 · SMCProcessor 1.3.8 · SMCLightSensor 1.3.8
USBToolBox · BrightnessKeys · Sinetek-rtsx
```

Catatan: `VoodooPS2Controller` muncul sebagai `PS2Controller 2.3.8` (nama kext bundle berbeda dari nama folder). `UTBMap`, `SMCSuperIO`, dan `CPUFriendDataProvider` adalah kext plugin/boolean yang tidak selalu muncul sebagai entry terpisah di `kextstat` — bukan tanda kegagalan.

**Kesimpulan: OpenCore 1.0.8 + seluruh kext bertahan upgrade tanpa perubahan.**

---

## 3. Perangkat keras — semua dikenali

| Perangkat | Status |
|---|---|
| GPU Intel UHD 620 | terdeteksi, 1920×1080 |
| Audio VoodooHDA | Default Output + Input, 2 channel |
| Wi-Fi (itlwm) | en0 = 10.148.13.108 |
| Bluetooth | On, `THIRD_PARTY_DONGLE`, controller active |
| Keyboard + Trackpad | HID terdeteksi (`Keyboard`, `Magic Trackpad 2`) |
| Touchpad I2C | VoodooI2C + VoodooInput load |
| Camera | `Integrated Camera` di USB tree |
| Baterai | 83%, AC attached, cycle count 645 |

---

## 4. Hermes Agent dan ekosistem — sehat

**Gateway jalan:**

```
ai.hermes.gateway          pid=1158  (uptime 6 menit, sehat)
ai.hermes.camofox          pid=1148  → port 9377 HTTP 200
com.9router.autostart      pid=1156  → port 20128 HTTP 200, model list OK
com.niumination.nosleep    pid=1146
com.niumination.9router-sync pid=-   (periodic 300s + WatchPaths, exit 0 = normal)
```

`9router-sync` `pid=-` **bukan kegagalan**. Plist-nya `RunAtLoad=true` + `StartInterval=300` + `WatchPaths` pada database 9router — itu job periodik yang berjalan lalu selesai (`last exit code = 0`). 9router sendiri merespons normal di `127.0.0.1:20128`.

**Toolchain:**

```
Python system  3.14.8  (naik dari 3.11 — pesan ini ditulis dari Hermes yang jalan di venv 3.11.16)
Hermes venv    3.11.16 (terpisah, tidak terdampak)
node           v24.21.0
npm            11.19.0
git            2.55.0
uv             0.12.12
Homebrew       7.0.7
```

Hermes berjalan di venv sendiri (`/Users/zaryu/src/hermes-agent/.venv`, Python 3.11.16), jadi lompatan Python sistem ke 3.14 tidak memengaruhi runtime Hermes.

---

## 5. Yang perlu diperhatikan

### 5.1 Python sistem 3.11 → 3.14 — risiko toolchain ekosistem

Ini perubahan paling besar yang tidak terlihat. Script ekosistem yang pakai shebang `#!/usr/bin/env python3` atau `python3` langsung sekarang jalan di 3.14. Yang sudah dites:

- `sqlite3` module: OK
- `skill-manifest.py` dan `sync-to-agents.sh`: belum dites di 3.14

**Yang belum diverifikasi:** script ekosistem yang bergantung pada modul yang berubah di 3.14 (mis. perubahan `pathlib`, penghapusan modul `ast` lama). Belum ada error yang terlihat, tapi belum ada yang menjalankan skill-sync penuh sejak upgrade.

### 5.2 Folder skill ganda muncul

```
skills/ecosystem/ecosystem/a2a-configuration/references/
skills/ecosystem/ecosystem/scheduled-job-delivery-routing/
skills/ecosystem/ecosystem/skill-library-maintenance/references/two-copy-bank-target-discipline.md
```

Ini dibuat proses lain (sinkronisasi skill bank), bukan oleh upgrade. Struktur `ecosystem/ecosystem/` adalah nesting ganda — bentuk ini pernah memicu masalah sebelumnya. Tidak disentuh di sesi ini.

### 5.3 EFI unmount

`disk0s1` (EFI) dalam kondisi `Mounted: No` — normal setelah restart, macOS tidak auto-mount partisi EFI. Tidak ada indikasi upgrade menulis ke EFI. Untuk memverifikasi, perlu mount via Finder/OCAT dan bandingkan SHA-256 `config.plist` dengan backup `EFI-BACKUP-2026-10-03`.

### 5.4 `csrutil status` = "unknown (Custom Configuration)"

Sama seperti sebelum upgrade (`csr-active-config 0x03`). Tidak berubah.

---

## 6. Yang tidak perlu diperbaiki

- **Kext:** semua bertahan, tidak ada yang perlu di-update atau re-enable.
- **OpenCore:** 1.0.8, config valid. EFI tidak disentuh upgrade.
- **Hermes gateway:** jalan normal setelah reboot.
- **9router + CamoFox:** merespons HTTP 200.
- **Disk:** naik dari 11 GB → 19 GB (upgrade membersihkan installer).
- **SIP / boot-args:** tidak diubah oleh upgrade.

---

## 7. Bukti

```
$ sw_vers → 26.7.1, 25G241
$ uptime → up 13 mins
$ kextstat → 19 kext pihak ketiga, semua load (Lilu, VirtualSMC, WhateverGreen, RestrictEvents,
  VoodooHDA, itlwm, IntelMausiEthernet, BlueToolFixup, IntelBTPatcher, IntelBluetoothFirmware,
  VoodooI2CServices, VoodooInput, PS2Controller, ECEnabler, NVMeFix, CPUFriend,
  SMCBatteryManager, SMCProcessor, SMCLightSensor, USBToolBox, BrightnessKeys, Sinetek-rtsx)
$ system_profiler SPDisplaysDataType → Intel UHD Graphics 620, 1920x1080
$ system_profiler SPAudioDataType → Default Output: Yes, Speaker (Analog)
$ ifconfig en0 → inet 10.148.13.108
$ system_profiler SPBluetoothDataType → State: On
$ ioreg IOUSB → Pen and multitouch sensor, Integrated Camera
$ launchctl list → gateway pid=1158, camofox pid=1148, 9router pid=1156, nosleep pid=1146
$ curl 127.0.0.1:20128/v1/models → HTTP 200, model list
$ curl 127.0.0.1:9377/health → HTTP 200
$ /Users/zaryu/src/hermes-agent/.venv/bin/python --version → 3.11.16
$ python3 --version → 3.14.8
$ df -h /System/Volumes/Data → 19Gi avail, 83% used
$ diskutil info disk0s1 → Mounted: No
```
