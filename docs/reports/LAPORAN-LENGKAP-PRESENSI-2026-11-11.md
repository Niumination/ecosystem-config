# Laporan Lengkap — Analisis & Rekonstruksi Presensi ASN
**Tanggal:** 2026-11-11  
**Status:** Tahap T1–T7a selesai · Flutter SDK masih terinstall

---

## 1. Temuan Kunci dari HP (adb)

### Device
- Infinix X6873 · Android 16 · APK v1.0.0 (sama dengan yang di Downloads)
- SHA-256: `aad75b115ae2da4f10773c6c9740f1dfe360e91d2059cb6a448a0a4d1ce86b7d`

### Field-names asli response server (diambil dari strings `libapp.so`)
```
POST /me → {nip, nama, jabatan, unor, golongan_ruang, kelas_jabatan, foto_url, hp, username}
POST /absen/masuk → {status_masuk, jam_masuk, jarak, radius, in_radius, warning}
POST /absen/pulang → {status_pulang, jam_pulang, jarak, radius, in_radius, warning}
GET  /absensi/bulanan?month=&year= → [ {tanggal, masuk, pulang, izin, sakit, cuti_tahunan, cuti_besar} ]
GET  /cuti/saldo → {saldo_cuti, saldo_cuti_besar, diperhitungkan_cuti_besar}
```

### Error codes & validasi sisi server
| Kondisi | Pesan / kode |
|---|---|
| Lokasi di luar radius | `ERR_LOCATION_OUT_OF_RADIUS` |
| Fake GPS terdeteksi | `"Lokasi simulasi terdeteksi. Nonaktifkan Fake GPS."` |
| GPS belum aktif | `"GPS belum aktif. Aktifkan lokasi perangkat."` |
| Akurasi kurang | `"Belum mendapat lokasi yang cukup akurat dalam 20 detik"` |
| Jam masuk lewat | `"Batas waktu absen masuk sudah lewat."` |
| Window belum buka | `"Absen masuk belum dibuka. Dibuka pukul HH:mm"` |
| Mata tertutup | `"Mata harus terbuka saat melakukan absensi untuk verifikasi keaktifan."` |
| Wajah tidak cocok | `"Wajah tidak dikenali atau tidak cocok."` |

### Firebase Project ID
- **Project:** `presensi-asn-9f5ab`
- **Storage bucket:** `presensi-asn-9f5ab.firebasestorage.app`

---

## 2. Struktur Source Asli (dari package paths di APK)

```
package:presensi_asn/
├── pages/
│   ├── absen_page.dart
│   ├── profil_page.dart
│   ├── riwayat_absensi_page.dart
│   ├── lokasi_absen_page.dart
│   └── izin_page.dart
├── models/
│   ├── izin_revision.dart
│   └── izin_status.dart
└── widgets/
    ├── cuti_besar_info.dart
    └── saldo_cuti_info.dart
```

---

## 3. Progress Kode Rekonstruksi

| Commit | Isi | Status |
|---|---|---|
| `92410dd` | T1–T3: skeleton + login + home + geolokasi dasar | ✅ |
| `db5ca34` | Fix duplikat provider di profile_screen | ✅ |
| `68ca58f` | T4–T5: model lengkap + UI radius/jarak + profilFoto | ✅ |
| `bde983d` | T7a: tab Riwayat Absensi + navigasi 3 tab | ✅ |

**Total file Dart:** 16 files  
**Direktori:** `~/Desktop/Niumination/presensi_rekon/`

### Yang sudah ada
- Login (NIP + password + device info otomatis)
- Home: tombol Masuk/Pulang, info GPS akurasi & usia, card radius + jarak real-time
- Riwayat: list absensi bulanan per tanggal
- Profil: NIP, nama, jabatan, unor, golongan, hp, email, foto
- Auth token disimpan aman di `flutter_secure_storage`
- Semua endpoint API lengkap 19 path

### Yang masih perlu ditambahkan
- **Face enrollment** (camera + upload foto + Face Match) — butuh TFLite integration
- **Halaman Izin/Cuti** — model sudah ada, UI belum
- **Notifikasi** — Firebase Messaging sudah terintegrasi, perlu UI badge
- **Build AOT + signing** — tahap akhir

---

## 4. Cara Menjalankan

```bash
# 1. Install Flutter (jika belum)
brew install flutter
# Atau download manual: https://flutter.dev/docs/get-started/install/macos

# 2. Buka project
cd ~/Desktop/Niumination/presensi_rekon

# 3. Ambil dependencies
flutter pub get

# 4. Jalankan di HP yang terhubung USB
flutter run
```

**Catatan:** HP harus dalam mode USB Debugging. Setelah build pertama (~2 menit), app akan berjalan di device.

---

## 5. next step setelah Flutter ready

1. `flutter run` → login pakai NIP+password asli dari user
2. Amati response JSON dari setiap endpoint di console Flutter debugger
3. Sesuaikan field names jika ada perbedaan dengan inferensi
4. Lanjut ke T6 (face enrollment) dan T7 penuh (izin/cuti UI)
