# Ringkasan — 11 Nov 2026 (Update Kedua)

## Yang Ditemukan dari HP (adb logcat + strings APK)

**Device:** Infinix X6873, Android 16  
**Versi APK terinstall:** sama persis dengan yang di Downloads (SHA-256 cocok)

### Field-names asli dari server (diambil dari strings APK)
Berikut adalah field names yang dipakai response server, berdasarkan reverse engineering strings di `libapp.so`:

**POST /me (profil):**
`nip`, `nama`, `jabatan`, `unor`, `golongan_ruang`, `kelas_jabatan`, `foto_url`, `hp`, `username`

**POST /absen/masuk dan /absen/pulang:**
Response mengandung: `status_masuk`, `status_pulang`, `jam_masuk`, `jam_pulang`, `jarak`/`jarak_meter`, `radius`, `in_radius`, `warning`

**Error codes yang dikenal app:**
- `ERR_LOCATION_OUT_OF_RADIUS` — lokasi di luar radius
- "Lokasi simulasi terdeteksi" — Fake GPS terdeteksi
- "Batas waktu absen masuk sudah lewat" — jam masuk sudah dilalui
- "Absen masuk belum dibuka. Dibuka pukul HH:mm" — jendela absen belum aktif

**UI strings utama (Indonesia):**
- "Absen Masuk", "Absen Pulang", "Dalam radius ✓", "Di luar radius ✗"
- "Jarak ke titik absen: X m", "Radius absen: X m"
- "Anda sudah absen masuk hari ini." / "Belum absen masuk"
- "Wajah berhasil terdaftar (3 template tersimpan)"
- Firebase Storage: `presensi-asn-9f5ab.firebasestorage.app`

### Struktur source asli (dari package paths di APK)
```
package:presensi_asn/pages/absen_page.dart
package:presensi_asn/pages/profil_page.dart
package:presensi_asn/pages/riwayat_absensi_page.dart
package:presensi_asn/pages/lokasi_absen_page.dart
package:presensi_asn/pages/izin_page.dart
package:presensi_asn/models/izin_revision.dart
package:presensi_asn/models/izin_status.dart
package:presensi_asn/widgets/cuti_besar_info.dart
package:presensi_asn/widgets/saldo_cuti_info.dart
```

---

## Update Kode (commit 68ca58f)

| File | Perubahan |
|---|---|
| `auth_models.dart` | Tambah field `hp`, `username`; perbaiki parser LoginResponse |
| `absensi_models.dart` | **Baru** — model AbsenHarian + RekamAbsen + SaldoCuti |
| `izin_models.dart` | **Baru** — model IzinItem, OpsiIzin, PenilaianKin |
| `client.dart` | Fix `/me` dan `/logout` jadi POST; tambah semua endpoint cuti/izin |
| `absen_controller.dart` | State ditambah: `accuracy`, `ageSeconds`, `jarakMeter`, `radiusMeter`, `inRadius`, `warning` |
| `home_screen.dart` | UI baru: card radius+jarak, status dalam/luar radius, tombol disabled sesuai status |
| `profile_screen.dart` | Tampilkan foto profil + field lengkap (hp, username) |

**Total file Dart:** 15 files | **Commit:** `68ca58f`

---

## Yang Masih Perlu Flutter SDK

Flutter belum terinstall di mesin ini. Untuk melanjutkan:

```bash
# Install Flutter (pilih salah satu)
brew install flutter        # jika brew tersedia
# atau download manual: https://flutter.dev/docs/get-started/install/macos
```

Setelah Flutter terinstall:
```bash
cd ~/Desktop/Niumination/presensi_rekon
flutter pub get
flutter run                    # jalankan di HP yang terhubung USB
```

---

## Tahap Selanjutnya (T6–T9)
- **T6** Face enrollment — perlu implementasi camera + upload foto ke `/face/enroll`
- **T7** Riwayat absensi + cuti + izin — halaman baru pakai model yang sudah dibuat
- **T8** Notifikasi + pengaturan
- **T9** Build AOT + signing
