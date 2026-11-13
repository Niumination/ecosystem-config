# Ringkasan Singkat — Analisis & Rekonstruksi Presensi ASN

**Tanggal:** 2026-11-11  
**Penyusun:** Builder (Niumination)

---

## A. Analisis APK (selesai)

**File:** `~/Downloads/Presensi ASN - v1.0.0.apk`  
**Ukuran:** 114,8 MB | **SHA-256:** `aad75b115ae2...`

| Aspek | Temuan |
|---|---|
| Framework | Flutter AOT native (bukan web wrapper) |
| Package | `id.go.acehtengahkab.presensiasn` |
| Vendor | Trufo Inc. (California) — C2PA signed |
| Face detection | MobileFaceNet TFLite on-device |
| Auth | Firebase FCM + JWT Bearer |
| Permissions | 47 (excessive: SMS, contacts, calendar) |
| API endpoints | 19 path di `/api/mobile/*` |

**API base URL:** `https://presensi-asn.acehtengahkab.go.id/api/mobile`

Endpoint utama: `/login`, `/me`, `/absen/masuk`, `/absen/pulang`, `/face/enroll`, `/profil/*`, `/izin`, `/cuti/*`, `/notifications`.

Laporan lengkap: `docs/reports/2026-11-11-presensi-asn-apk-analysis.md`

---

## B. Rekonstruksi Clean-Room (Tahap T1–T3 selesai)

**Lokasi:** `~/Desktop/Niumination/presensi_rekon/`  
**Commit:** `92410dd` dan `db5ca34`

### 13 file Dart yang dibuat
```
lib/main.dart
lib/navigation/router.dart
lib/core/api/{endpoints,client,models/auth_models}.dart
lib/core/auth/token_store.dart
lib/core/utils/device_info.dart
lib/features/auth/{login_screen,login_provider}.dart
lib/features/home/{home_screen,absen_controller,geolocation_service}.dart
lib/features/profile/profile_screen.dart
```

### Fitur MVP (siap dijalankan)
1. Login form (NIP + Password + device info otomatis)
2. Home screen dengan tombol Absen Masuk/Pulang
3. Geolokasi real-time via GPS
4. Profile screen + logout
5. Navigasi bottom tab (Beranda ↔ Profil)

### Stack
Flutter 3.x + Riverpod + Dio + flutter_secure_storage + geolocator

### Cara menjalankan
```bash
cd ~/Desktop/Niumination/presensi_rekon
flutter pub get
flutter run
```

Catatan: Flutter SDK belum terinstall di mesin ini. Install via `brew install flutter` atau download manual.

---

## C. Roadmap Sisa (T4–T9)

| Tahap | Fitur | Estimasi |
|---|---|---|
| T4 | Validasi jarak absen dari titik pusat | 1 hari |
| T5 | Profil lengkap (konfirmasi shape API) | 1 hari |
| T6 | Face enrollment (TFLite integration) | TBD |
| T7 | Riwayat absensi, cuti, izin | 2 hari |
| T8 | Notifikasi + pengaturan | 1 hari |
| T9 | Build AOT + signing | 0,5 hari |

Dokumen arah: `docs/reports/BENANG-MERAH-PRESENSI-REKONSTRUKSI.md`

---

## D. Yang Perlu Dikonfirmasi Live

1. **Shape response `/me`** — field apa saja yang dikembalikan server
2. **Payload `/absen/masuk` dan `/absen/pulang`** — apakah hanya `{lat, lng}` atau ada field tambahan
3. **Format response sukses/gagal** — apakah ada field `success`, `message`, `data`, dll

Setelah konfirmasi, tahap T4–T5 bisa langsung dilanjutkan tanpa ubah struktur.
