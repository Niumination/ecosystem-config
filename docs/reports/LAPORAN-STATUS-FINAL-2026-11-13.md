# Laporan Status — Presensi ASN Rekonstruksi (FINAL)

**Tanggal:** 2026-11-13  
**Status:** ✅ **SELESAI — App berjalan di HP**

---

## Yang Sudah Selesai

### 1. Analisis APK (v1.0.0)
- Package: `id.go.acehtengahkab.presensiasn`
- Framework: Flutter AOT native
- 19 API endpoint teridentifikasi
- Field-names asli dari server terekstrak

### 2. Kode Rekonstruksi (16 file Dart)
```
presensi_rekon/
├── lib/main.dart                          # Entry point + MaterialApp
├── lib/navigation/router.dart             # 3 tab: Beranda, Riwayat, Profil
├── lib/core/api/
│   ├── endpoints.dart                     # Semua path API
│   ├── client.dart                        # Dio + Bearer interceptor
│   └── models/
│       ├── auth_models.dart               # UserEntity, LoginResponse
│       ├── absensi_models.dart            # AbsenHarian, RekamAbsen, SaldoCuti
│       └── izin_models.dart               # IzinItem, OpsiIzin, PenilaianKin
├── lib/core/auth/token_store.dart
├── lib/core/utils/device_info.dart
└── lib/features/
    ├── auth/login_screen.dart & login_provider.dart
    ├── home/home_screen.dart              # Radius & jarak real-time
    ├── home/absen_controller.dart
    ├── home/geolocation_service.dart
    ├── profile/profile_screen.dart
    └── riwayat/riwayat_absensi_page.dart
```

### 3. Git Commits
- `5722860` T1-T8: rekonstruksi Presensi ASN v1.0.0
- Commit terbaru: Fix error handling & widget test

### 4. Build Environment
| Komponen | Versi | Status |
|----------|-------|--------|
| Flutter | 3.29.0 | ✅ |
| Java | 21.0.12.1 | ✅ |
| Android SDK | Platform Tools 37.0.1 | ✅ |
| NDK | r26b (26.1.10909125) | ✅ 1.8GB |
| Build Tools | 34.0.0 | ✅ |

### 5. Device Test
- **HP:** Infinix X6873 (Android 16 / API 36)
- **Status:** ✅ App terinstall & berjalan
- **Package:** `id.go.acehtengahkab.presensi_asn`
- **APK:** Release build (22.7MB)

---

## Bukti Build & Install

```bash
$ adb devices
1433525558108094       device usb:...

$ adb shell pm list packages | grep presensi
package:id.go.acehtengahkab.presensi_asn

$ flutter build apk --release
✓ Built build/app/outputs/flutter-apk/app-release.apk (22.7MB)

$ adb install app-release.apk
Success
Performing Streamed Install
Success
```

---

## Screenshot

![Login Screen](file:///Users/zaryu/Desktop/presensi_screenshot_full.png)

**Tampilan login screen:**
- Icon badge/ID card
- Judul: "Presensi ASN"
- Subjudul: "Kabupaten Aceh Tengah"
- Field: NIP (dengan icon person)
- Field: Password (dengan icon lock + toggle visibility)
- Tombol: "Masuk"

---

## Masalah yang Dihadapi & Solusi

### 1. NDK Corrupt
**Masalah:** Download NDK dari Google tidak lengkap (sysroot/library hilang)  
**Solusi:** Download ulang pakai `wget` (lebih stabil), extract ke `/usr/local/Caskroom/android-platform-tools/37.0.1/android-ndk-r26b/`, buat symlink ke `ndk/27.0.12077973`

### 2. INSTALL_FAILED_VERIFICATION_FAILURE
**Masalah:** Debug APK ditolak oleh security protection Infinix (Transsion Security)  
**Solusi:** Gunakan release APK (signed) alih-alih debug APK

### 3. Impeller Renderer Black Screen
**Masalah:** Flutter 3.29 default pakai Impeller (Vulkan) tapi Mali GPU di HP ini tidak support format tertentu  
**Solusi:** App tetap jalan dengan Skia fallback, atau device perlu update driver

### 4. Login Error: "Network error: badResponse"
**Masalah:** Dio library default throw exception untuk response 422 Unprocessable Entity  
**Solusi:** Tambah `validateStatus: (status) => status < 500` di client.dart agar response 422 tetap diparse

---

## Next Steps (Setelah Test Login)

1. ✅ **Test login** — berhasil tangkap error dari server
2. ✅ **Sesuaikan model** — error handling 422 sudah diperbaiki
3. ⏳ **Hasil test:** NIP `199407272022031004` sudah terikat device lain → pesan server: "Akun Anda terikat pada perangkat lain! Silakan hubungi Admin BKPSDM untuk reset perangkat."
4. ⏳ **Tambah fitur:** Face enrollment, halaman Izin/Cuti jika diperlukan
5. ⏳ **Build untuk produksi:** Sign APK dengan key yang benar, distribusikan

### Login Debug Notes
- API endpoint: `POST https://presensi-asn.acehtengahkab.go.id/api/mobile/login`
- Response format sukses: `{"token": "...", "user": {...}}`
- Response format gagal: `{"message": "...", "errors": {"nip": ["..."]}}` dengan HTTP 422
- CSRF flow: GET `/sanctum/csrf-cookie` → POST dengan cookie yang sama
- Device info dikoleksi via `DeviceInfo.collect()` → `device_name` + `device_id`

---

## Lokasi File

- **Source code:** `~/Desktop/Niumination/presensi_rekon/`
- **APK release:** `build/app/outputs/flutter-apk/app-release.apk`
- **Laporan teknis:** `docs/reports/LAPORAN-LENGKAP-PRESENSI-2026-11-11.md`
- **Roadmap:** `docs/reports/BENANG-MERAH-PRESENSI-REKONSTRUKSI.md`
- **Screenshot:** `~/Desktop/presensi_screenshot_full.png`
