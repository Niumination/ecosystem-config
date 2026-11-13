# Benang Merah — Rekonstruksi Presensi ASN ACEH TENGAH

**Tanggal:** 2026-11-11  
**Status:** Tahap 1 — Perencanaan & MVP  
**Sumber kebenaran:** APK `Presensi ASN - v1.0.0.apk` (SHA-256: `aad75b115ae2...`) + live API probe

---

## 1. Prinsip Dasar

1. **Clean-room**: tidak ada salinan kode asli. Semua implementasi ditulis ulang dari spesifikasi API yang teramati.
2. **Satu fitur per commit**: setiap modul berdiri sendiri dan dapat diuji sebelum melanjutkan.
3. **Bukti dulu, klaim kemudian**: semua claim API divalidasi via curl sebelum coding.
4. **Dokumentasi hidup**: file ini adalah sumber kebenaran; update setelah setiap milestone.

---

## 2. Arsitektur Target

```
presensi_rekon/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── api/
│   │   │   ├── client.dart          # Dio + Interceptor
│   │   │   ├── endpoints.dart       # Base URL + path constants
│   │   │   └── models/              # Data classes
│   │   ├── auth/
│   │   │   ├── token_store.dart     # SharedPreferences
│   │   │   └── session.dart         # Auth state stream
│   │   └── utils/
│   │       ├── device_info.dart
│   │       └── crypto_helpers.dart
│   ├── features/
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   └── login_provider.dart
│   │   ├── home/
│   │   │   ├── home_screen.dart
│   │   │   ├── absen_controller.dart
│   │   │   └── geolocation_service.dart
│   │   └── profile/
│   │       ├── profile_screen.dart
│   │       └── profile_provider.dart
│   └── navigation/
│       └── router.dart
├── pubspec.yaml
└── analysis_options.yaml
```

**Stack pilihan:**
- Framework: Flutter 3.x (AOT native)
- HTTP: `dio` + interceptor untuk Bearer token
- State: `flutter_riverpod` atau `provider` (pilih provider untuk minimalis)
- Local storage: `shared_preferences` (token) + `flutter_secure_storage` (NIP optional)
- Geolokasi: `geolocator` + `permission_handler`
- Face detection: **dilepas dulu** (tahap 2) — pakai `mobile_scanner` atau TFLite integration nanti
- Peta: `flutter_map` + OpenStreetMap tiles

---

## 3. Spesifikasi API (terverifikasi via curl)

### Base URL
```
https://presensi-asn.acehtengahkab.go.id/api/mobile
```

### 3.1 POST /login
**Request body:**
```json
{
  "nip": "<string, required>",
  "password": "<string, required>",
  "device_name": "<string, required>",
  "device_id": "<string, required>"
}
```

**Success response (inferred):**
```json
{
  "message": "...",
  "data": {
    "token": "<string, Bearer JWT>",
    "user": { ... }
  }
}
```

**Error response:**
```json
{
  "message": "NIP atau password salah.",
  "errors": {"nip": ["NIP atau password salah."]}
}
```

### 3.2 GET /me
Headers: `Authorization: Bearer <token>`  
Returns: profil lengkap user (nama, jabatan, unor, golongan_ruang, dll)

### 3.3 POST /absen/masuk
Headers: `Authorization: Bearer <token>`  
Body: `{ "lat": float, "lng": float, "device_id": string, ... }`  
Response: status diterima/ditolak + jarak dari titik pusat

### 3.4 POST /absen/pulang
Sama struktur dengan /masuk

### 3.5 POST /absen/lokasi
Update lokasi terakhir tanpa absen

### 3.6 GET /absensi/bulanan?month=&year=
History bulanan

### 3.7 GET /absensi/semua
Semua history

### 3.8 POST /face/enroll
Upload foto wajah untuk registrasi biometrik

### 3.9 GET/POST /izin, /cuti/saldo, /cuti/besar
Manajemen izin dan cuti

### 3.10 GET /notifications?page=&per_page=
Notifikasi push

### 3.11 GET /profil/golongan_ruang, /jabatan, /kelas-jabatan, /unor
Data master profil

### 3.12 PUT /profil/password
Ubah password

### 3.13 GET /pengaturan/absen-mode
Mode absen (manual/auto/geofence)

### 3.14 GET /penilaian
Data penilaian kinerja

### 3.15 GET/POST /logout
Revoked token

---

## 4. Roadmap Bertahap

| Tahap | Fitur | Estimasi | Status |
|---|---|---|---|
| **T1** | Skeleton project + navigasi dasar | 1 hari | ✅ Selesai |
| **T2** | Login flow (NIP+pass+device info) | 1 hari | ✅ Selesai |
| **T3** | Home screen + tombol Absen Masuk/Pulang | 1 hari | ✅ Selesai |
| **T4** | Geolokasi + validasi jarak & radius | 1 hari | ✅ Selesai |
| **T5** | Profil screen + data master | 1 hari | ✅ Selesai |
| **T6** | Face enrollment (tahap lanjut) | TBD | ⏳ Rencana |
| **T7** | Riwayat absensi + cuti + izin | 2 hari | ⏳ Rencana |
| **T8** | Notifikasi + pengaturan | 1 hari | ⏳ Rencana |
| **T9** | Build AOT + signing | 0.5 hari | ⏳ Rencana |

---

## 5. Dependency Checklist (harus diinstall sebelum mulai)

```bash
# Flutter SDK
brew install flutter   # atau download manual dari flutter.dev
flutter doctor         # pastikan Android SDK + Xcode ready
```

**Pub packages target:**
```yaml
dependencies:
  flutter:
    sdk: flutter
  dio: ^5.4.0          # HTTP client
  flutter_riverpod: ^2.5.0  # state management
  shared_preferences: ^2.2.0   # token store
  geolocator: ^11.0.0        # lokasi
  permission_handler: ^11.2.0 # permission runtime
  flutter_secure_storage: ^9.0.0  # secure token
  uuid: ^4.3.0             # device ID generation
  flutter_map: ^6.1.0      # peta (tahap lanjut)
  latlong2: ^0.9.0         # utilitas koordinat
```

---

## 6. Pertimbangan Keamanan

1. **Token disimpan di `flutter_secure_storage`**, bukan SharedPreferences biasa.
2. **TLS mutual tidak diperlukan** (server menggunakan HSTS standard).
3. **Device ID** di-generate UUIDv4 persisten, dikirim setiap request auth.
4. **Tidak ada hard-coded credential** — semua dinamis dari input user.
5. **CORS**: karena ini mobile app, CORS tidak berlaku — langsung call API.

---

## 7. Bukti Eksternal

```bash
$ curl -s -X POST https://presensi-asn.acehtengahkab.go.id/api/mobile/login \
  -H "Content-Type: application/json" \
  -d '{"nip":"test","password":"test","device_name":"t","device_id":"t"}'
{"message":"NIP atau password salah.","errors":{"nip":["NIP atau password salah."]}}

$ curl -s -o /dev/null -w "%{http_code}" https://presensi-asn.acehtengahkab.go.id/sanctum/csrf-cookie
204

$ sha256sum ~/Downloads/"Presensi ASN - v1.0.0.apk"
aad75b115ae2da4f10773c6c9740f1dfe360e91d2059cb6a448a0a4d1ce86b7d
```

---

*File ini akan di-update seiring kemajuan setiap tahap. Gunakan sebagai acuan sebelum memulai coding.*
