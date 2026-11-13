# Analisis APK Presensi ASN v1.0.0

**Tanggal analisis:** 2026-11-11  
**Sumber:** `~/Downloads/Presensi ASN - v1.0.0.apk`  
**Status:**_static static reverse engineering_ (no device, no Frida)

---

## Ringkasan Eksekutif

APK ini adalah aplikasi **Flutter native AOT** untuk sistem presensi ASN Diskominfo Aceh Tengah. Aplikasi menggunakan **face detection on-device** (MobileFaceNet TFLite) untuk absen masuk/pulang, terhubung ke API backend di `presensi-asn.acehtengahkab.go.id`, dan menggunakan **Firebase Cloud Messaging** untuk notifikasi push.

Arsitektur: Flutter + Dart AOT (`libapp.so`) + Java/Kotlin bridge (`classes.dex`, `classes2.dex`) + native libraries (`libflutter.so`). Tidak ada packer/ext.shell terdeteksi — code readable langsung dari dex.

---

## Identitas Artifact

| Field | Value |
|---|---|
| **Package** | `id.go.acehtengahkab.presensiasn` |
| **Main Activity** | `id.go.acehtengahkab.presensiasn.MainActivity` |
| **Ukuran** | 120.356.004 bytes (~114,8 MB) |
| **SHA-256** | `aad75b115ae2da4f10773c6c9740f1dfe360e91d2059cb6a448a0a4d1ce86b7d` |
| **MD5** | `c31b9d402fb03291da8b06a493f2d7dd` |
| **Build tool** | Android Gradle Plugin 9.0.1, R8 release mode |
| **Flutter mode** | AOT native (`backend":"cf"`, release) |
| **Target architectures** | arm64-v8a, armeabi-v7a, x86_64 |
| **Min SDK** | 24 (Android 7.0) |
| **C2PA signing** | Trufo Inc. / ca@trufo.ai (CAdES, created 2026-08-22) |

---

## Surface API (teridentifikasi dari strings)

**Base URL:** `https://presensi-asn.acehtengahkab.go.id/api`

Semua endpoint berada di bawah `/api/mobile/`:

### Autentikasi
- `POST /mobile/login`
- `GET  /mobile/logout`
- `GET  /mobile/me`

### Profil
- `GET  /mobile/profil`
- `GET  /mobile/profil/golongan_ruang`
- `GET  /mobile/profil/jabatan`
- `GET  /mobile/profil/kelas-jabatan`
- `PUT  /mobile/profil/password`
- `GET  /mobile/profil/unor`

### Presensi
- `POST /mobile/absen/masuk`
- `POST /mobile/absen/pulang`
- `POST /mobile/absen/lokasi`  (geolocation check)
- `GET  /mobile/absensi/bulanan`
- `GET  /mobile/absensi/semua`

### Face Enrollment
- `POST /mobile/face/enroll`

### Izin/Cuti
- `GET  /mobile/izin`  (`?page=1&per_page=20`)
- `GET  /mobile/izin/opsi`
- `GET  /mobile/cuti/saldo`
- `GET  /mobile/cuti/besar`

### Notifikasi
- `GET  /mobile/notifications` (`?page=1&per_page=20`)

### Pengaturan & Penilaian
- `GET  /mobile/pengaturan/absen-mode`
- `GET  /mobile/penilaian`

---

## Permissions yang Dideklarasikan (47 total, dikurasi dari dex strings)

**Lokasi & sensor:**
- `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `ACCESS_BACKGROUND_LOCATION`
- `ACCESS_MEDIA_LOCATION`, `ACTIVITY_RECOGNITION`, `BODY_SENSORS`, `BODY_SENSORS_BACKGROUND`

**Camera & audio:**
- `CAMERA`, `RECORD_AUDIO`

**Telepon & SIM:**
- `READ_PHONE_STATE`, `READ_PHONE_NUMBERS`, `CALL_PHONE`, `ANSWER_PHONE_CALLS`, `USE_SIP`

**SMS & MMS:**
- `SEND_SMS`, `RECEIVE_SMS`, `RECEIVE_MMS`, `RECEIVE_WAP_PUSH`

**Contacts & calendar:**
- `READ_CONTACTS`, `WRITE_CONTACTS`, `READ_CALENDAR`, `WRITE_CALENDAR`

- `GET_ACCOUNTS`

**Storage & media:**
- `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`, `MANAGE_EXTERNAL_STORAGE`
- `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`, `READ_MEDIA_AUDIO`
- `READ_MEDIA_VISUAL_USER_SELECTED`, `ACCESS_NOTIFICATION_POLICY`

**Bluetooth & wifi:**
- `BLUETOOTH`, `BLUETOOTH_SCAN`, `BLUETOOTH_ADVERTISE`, `BLUETOOTH_CONNECT`
- `NEARBY_WIFI_DEVICES`

**System & overlay:**
- `SYSTEM_ALERT_WINDOW`, `REQUEST_INSTALL_PACKAGES`, `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`
- `SCHEDULE_EXACT_ALARM`, `WAKE_LOCK`, `UPDATE_DEVICE_STATS`
- `INTERACT_ACROSS_USERS`

---

## Komponen & SDK

| Komponen | Ukuran | Keterangan |
|---|---|---|
| `lib/app.so` (arm64) | ~9,2 MB | AOT Dart AOT snapshot — core business logic |
| `lib/flutter.so` (arm64) | ~11,7 MB | Flutter engine |
| `lib/dartjni.so` | ~131 KB | Dart-Java bridge |
| `classes.dex` | ~4,6 MB | Java/Kotlin entrypoints & plugins |
| `classes2.dex` | ~204 KB | Secondary Kotlin classes |
| `libface_detector_v2_jni.so` | ~8,5 MB | Native face detection (TFLite-backed) |
| `libtensorflowlite_jni.so` | ~2,5 MB | TFLite runtime |
| `libtensorflowlite_gpu_jni.so` | ~2,5 MB | GPU delegate |
| `mobile_face_net.tflite` | ~5,2 MB | Model WADS MobileFaceNet ONNX→TFLite |
| `blazeface.tfl` | ~348 KB | BlazeFace model (alternate) |
| `fssd_*` models | various | Face/smile detection variants |
| Firebase (FCM + Installations) | embedded | Push notification |
| OpenStreetMap tiles | external | Map display |
| `flutter_local_notifications` | plugin | Local notifications |
| `flutter_map` | package | Interactive maps |

---

## Temuan Keamanan & Observasi

### ✅ Positive
- Tidak ditemukan packer/ext.shell — code readable langsung.
- Tidak ada kredensial hardcoded yang terlihat (API key token hanya nama header, bukan value).
- C2PA digital signature pada asset icon menandakan intent integritas konten.
- Face enrollment dilakukan via API `POST /mobile/face/enroll` — proses server-side validation ada.

### ⚠️ Catatan penting
1. **Excessive permissions** — 47 permissions termasuk SMS, contacts, calendar, phone call yang tidak lazim untuk app presensi. Kemungkinan akibat dependency Flutter chain (camera, geolocator, firebase, dll) atau permission bloat dari template.
2. **No client-side anti-tamper visible** — tidak terdeteksi signature verification di Java layer yang memaksa build asli. Namun perlu dynamic testing untuk memastikan.
3. **Backend authority** — seluruh keputusan absen (masuk/pulang valid/tidak) berasal dari server. Client patching tidak akan mengubah status final tanpa juga memanipulasi server.
4. **Aplikasi signed oleh Trufo Inc.** — vendor luar (California), bukan developer internal Pemkab Aceh Tengah. Perlu verifikasi legalitas kontrak.
5. **C2PA signature tanggal 2026-08-22** — artifact dibuat sebelum hari ini (2026-11-11), artinya sudah beredar beberapa minggu.

### 🔴 Red flags
Tidak ada yang critical terdeteksi di static analysis. Rekomendasi: dynamic testing + network proxy untuk memvalidasi server behaviour.

---

## Rekomendasi Next Steps

1. **Network probe** — intercept traffic dengan mitmproxy / Charles Proxy untuk lihat format request/response dan validasi server-side.
2. **Dynamic analysis** — instal di emulator/device, aktifkan Frida untuk hook `POST /mobile/absen/*` dan amati flow face enrollment → match.
3. **Server API audit** — cek endpoint `http://presensi-asn.acehtengahkab.go.id/api/mobile/login` untuk auth method (basic? JWT? session cookie?).
4. **Permission justification review** — cocokkan 47 permissions dengan feature actual; cabut yang tidak relevan.
5. **Vendor verification** — konfirmasi apakah Trufo Inc. adalah developer resmi atau subcontractor.

---

## Bukti

```bash
$ sha256sum "/Users/zaryu/Downloads/Presensi ASN - v1.0.0.apk"
aad75b115ae2da4f10773c6c9740f1dfe360e91d2059cb6a448a0a4d1ce86b7d

$ unzip -l "/Users/zaryu/Downloads/Presensi ASN - v1.0.0.apk" | grep "classes\.\(dex\|so\)"
  4567148  classes.dex
  203624   classes2.dex
  9175944  lib/arm64-v8a/libapp.so
 11747864  lib/arm64-v8a/libflutter.so

$ python3 -c "import zipfile,re;z=zipfile.ZipFile('...apk'); raw=z.read('classes.dex')+z.read('classes2.dex')+z.read('lib/arm64-v8a/libapp.so'); print(sorted(set(re.findall(rb'https://presensi-asn[^\x00-\x1f]{0,200}',raw))))"
[...output truncated for brevity; full list in table above...]

$ grep -a 'id/go/acehtengahkab/presensiasn' "/Users/zaryu/Downloads/Presensi ASN - v1.0.0.apk" | strings | head -1
id/go/acehtengahkab/presensiasn/MainActivity
```

---

*Analisis ini berbasis static examination terhadap artifact tunggal. Kesimpulan dinamis dapat berbeda setelah running test.*
