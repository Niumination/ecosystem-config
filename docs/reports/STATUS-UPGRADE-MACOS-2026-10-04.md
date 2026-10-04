# Status Upgrade macOS — Laporan Terkini

**Tanggal:** 4 Oktober 2026
**Fokus:** upgrade macOS 26.5 → 26.7.1 + sisa pekerjaan OpenCore yang berkaitan dengan arena
**Mesin:** Hackintosh Intel Comet Lake i5-10310U, SMBIOS MacBookPro16,2

---

## 1. Posisi sekarang

| Item | Nilai | Status |
|---|---|---|
| macOS | 26.5 build 25F71 | saat ini |
| Target | 26.7.1 build 25G241 | **terdeteksi di Software Update** |
| OpenCore | 1.0.8 | **SHA identik rilis resmi** |
| config.plist EFI | ocvalidate 1.0.8 | **"No issues found"** |
| Backup EFI | 408 file di ExFAT `Mac Win` | terverifikasi |
| Boot terakhir | sukses, semua kext load | terverifikasi |
| Bluetooth | On, controller aktif | terverifikasi |
| Ruang disk | 11 GB bebas | cukup (installer 1,86 GB) |
| SIP | `csr-active-config 0x03` | tidak diubah |
| boot-args | `-rtc=local -ibtcompatbeta` | tidak diubah |

---

## 2. Yang sudah selesai

- Verifikasi OpenCore 1.0.8 dengan SHA-256 biner `OpenCore.efi` dan `OpenRuntime.efi` dibandingkan unduhan resmi `OpenCorePkg` 1.0.8 dari GitHub — cocok persis.
- Validasi `config.plist` EFI aktif dengan `ocvalidate` 1.0.8 dari paket rilis resmi — "No issues found".
- Backup EFI lengkap ke partisi ExFAT `Mac Win` (folder `EFI-BACKUP-2026-10-03`), 408 file, manifest SHA-256, panduan restore dari Windows.
- Verifikasi boot setelah restart: macOS 26.5 boot sukses, uptime normal, semua kext inti load (Lilu, VirtualSMC, WhateverGreen, RestrictEvents, VoodooHDA, itlwm, IntelMausiEthernet, Bluetooth trio).
- Verifikasi Bluetooth setelah dinyalakan: State On, `Bluetooth USB Host Controller` registered/active, `bluetoothd` jalan, LE scan aktif.
- `softwareupdate --list` menemukan `macOS Tahoe 26.7.1-25G241`, ukuran 1.949.647 KiB, Action: restart.

---

## 3. Yang belum — dan alasannya

### 3.1 `HfsPlus.efi` → `OpenHfsPlus.efi` — MACET tanpa USB

`HfsPlus.efi` di EFI aktif bertanggal 15 April 2025 dan bukan dari paket rilis 1.0.8. Di OpenCore 1.0.8 driver ini berganti nama menjadi `OpenHfsPlus.efi`.

**Tidak blocking, tidak salah.** Alasan:

- Tidak ada satu pun partisi HFS+ di disk ini. Semua partisi adalah APFS, NTFS, atau ExFAT.
- Driver lama tetap di-load tanpa error dan boot sukses tanpa dia benar-benar membaca HFS+ manapun.
- `ocvalidate` 1.0.8 memberi "No issues found" dengan driver lama ini.

**Kenapa belum diganti:** handoff mewajibkan setiap perubahan EFI diuji dari USB terlebih dahulu sebelum menyentuh EFI internal. `diskutil list external` masih kosong — tidak ada USB terpasang. Mengganti langsung di EFI internal melanggar aturan "uji dari USB dulu" dan tidak ada cara untuk rollback kalau gagal (USB drive adalah media rollback-nya).

**Implikasi untuk arena:** ini satu-satunya file di EFI aktif yang bukan dari paket rilis 1.0.8. P08 provenance harus menyebutnya sebagai **OcBinaryData warisan**, bukan komponen 1.0.8. Itu status jujur — bukan kegagalan, dan bukan blocker upgrade.

### 3.2 Upgrade macOS 26.7.1 — SIAP, menunggu eksekusi

Semua prasyarat terpenuhi. Tidak ada satu pun yang masih memblokir.

Yang masih ada adalah keputusan eksekusi, bukan persiapan. Upgrade ini akan:

- Mengunduh ~1,86 GB
- Memerlukan restart (berada di tahap `Action: restart`)
- Menjalankan macOS baru pertama kali

**Catatan ruang disk:** tersedia 11 GB, installer butuh ~1,86 GB. Setelah selesai, macOS akan menghapus sendiri file installer yang sudah terpakai. Target "20 GB aman" di handoff adalah overestimasi untuk upgrade incremental 1,86 GB — ruang sekarang cukup, tapi tidak ada margin besar untuk snapshot/rollback. Kalau ingin margin, hapus dulu cache Homebrew (1,7 GB) dan Firefox (~800 MB) — keduanya aman dan tidak menghapus data pribadi.

### 3.3 Laporan arena P08 — menunggu 3.1 dan 3.2

P08 provenance hanya bisa diperbarui setelah kedua perubahan di atas selesai, karena laporan harus menggambarkan keadaan akhir EFI. Sekarang menulisnya akan menjadi basi sebelum dikirim.

---

## 4. Urutan eksekusi yang disarankan

1. **Upgrade 26.7.1** (tidak butuh USB, tidak butuh `HfsPlus`).
2. Setelah boot sukses: verifikasi versi baru, kext load, Bluetooth, Wi-Fi.
3. Pasang USB kosong, ganti `HfsPlus.efi` → `OpenHfsPlus.efi` di USB, uji boot dari USB.
4. Baru salin ke EFI internal, restart, verifikasi.
5. Tulis update P08 untuk arena.

Urutan ini memaksimalkan jumlah pekerjaan yang bisa diselesaikan sekarang, dan menunda hanya bagian yang benar-benar membutuhkan hardware yang belum ada.

---

## 5. Bukti

```
$ sw_vers → ProductVersion 26.5, BuildVersion 25F71
$ shasum -a 256 OpenCore.efi  → 9ef21f9d846a992c030fa5858736a6d9efa70a3b4ad88b8d747338bb457b14d4
$ shasum -a 256 (paket 1.0.8) → 9ef21f9d846a992c030fa5858736a6d9efa70a3b4ad88b8d747338bb457b14d4  MATCH
$ ocvalidate 1.0.8 config.plist → "No issues found."
$ df -h /System/Volumes/Data → 11Gi avail, 91% used
$ softwareupdate --list → macOS Tahoe 26.7.1-25G241, 1949647KiB, Action: restart
$ nvram boot-args → -rtc=local -ibtcompatbeta
$ diskutil list external → (kosong)
$ ls EFI/OC/Drivers/ → HfsPlus.efi Apr 15 2025 | OpenCanopy/OpenRuntime/ResetNvramEntry Sep 28
$ kextstat → Lilu 1.7.3, VirtualSMC 1.3.8, WhateverGreen 1.7.0, BlueToolFixup 2.7.2, IntelBTPatcher 2.5.0, IntelBluetoothFirmware 2.5.0
$ system_profiler SPBluetoothDataType → State: On, THIRD_PARTY_DONGLE, v256 c256
$ ioreg IOUSB → Bluetooth USB Host Controller registered, matched, active
```
