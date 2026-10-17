# KEPUTUSAN-TETAP.md — registry keputusan sadar

> **Kenapa berkas ini ada.** Audit berulang menemukan **akar masalah D: alarm palsu** — 2 alarm palsu pada ekosistem ini,
> dan satu di antaranya justru FileVault (16 Okt). Penyebabnya selalu sama: **keadaan yang *disengaja* tidak pernah tercatat**,
> sehingga setiap pemeriksaan (dan setiap agen: Hermes, OpenCode, Desktop, siapa pun) membacanya sebagai **kerusakan** dan
> mengusulkan "perbaikan" yang justru membalikkan keputusan Anda.
>
> **Aturan berkas ini:**
> 1. Setiap keadaan yang tampak seperti masalah **tetapi sengaja dipilih** dicatat di sini dengan ID (K-01, K-02, …).
> 2. Pemeriksa **wajib membaca berkas ini** sebelum menilai; bila ID-nya ada → **bukan temuan**.
> 3. Sebuah keputusan di sini punya **pemicu tinjauan ulang** (kapan boleh dibuka lagi) — jadi bukan "dibiarkan tanpa arah".
> 4. **Agen tidak boleh** membalikkan keputusan di sini tanpa persetujuan manusia. Bila agen merasa keputusan ini salah → tulis argumen, jangan langsung eksekusi.

---

## Lokasi & riwayat berkas ini

| Item | Nilai |
|---|---|
| Lokasi kanonik | `docs/registry/KEPUTUSAN-TETAP.md` |
| Asal | `roadmap/KEPUTUSAN-TETAP.md` dalam paket `eco-map-last.zip` (16 Okt 2026) |
| Dipulihkan | 18 Okt 2026 — diekstrak dari sesi OpenCode (`ses_ebb37d5f9ffe7W4f9otoiKJJZB`) setelah salinan aslinya hilang dari disk |
| Rujukan silang | `docs/DECISIONS.md` (ledger hidup) · `LOG-PERBAIKAN.md` 16 Okt |

> **Pelajaran pencadangan:** berkas ini **pernah hilang sepenuhnya** dari disk — hanya tersisa di dalam sesi
> OpenCode. DB sesi bukan arsip: ia bisa dipangkas/dikosongkan. Keputusan penting wajib hidup di repo,
> bukan di log percakapan.

---

## K-01 · FileVault DIMATIKAN dengan sengaja

| | |
|---|---|
| **Tanggal** | 16 Oktober 2026 (klarifikasi pengguna; jejak proses terlihat 16 Okt 14:33–15:10) |
| **Keputusan** | FileVault **OFF**, dan tidak dinyalakan selama mesin ini masih berjalan sebagai Hackintosh. |
| **Status** | ⛔ Aktif — **bukan temuan**, jangan diangkat lagi sebagai alarm. |

**Alasan (dari pengguna):** setelah FileVault aktif, **sandi akun selalu ditolak di layar boot** — berulang kali harus masuk memakai **recovery key**, lalu **reset sandi**. Dugaan pengguna: konfigurasi plist/kext/driver Hackintosh tidak mendukung jalur boot FileVault. **Dugaan itu tepat.**

**Diagnosa teknis (riset 16 Okt):** FileVault 2 bergantung pada jalur *preboot* (EFI → APFS *Preboot* → AppleKeyStore), dengan materi kunci di NVRAM/EFI variable. Pada Hackintosh jalur itu melewati OpenCore. Ada laporan bug resmi acidanthera dengan gejala **identik** — pada **macOS Tahoe** volume FV2 menjadi tidak bisa di-boot: *"the prebooter loads, but doesn't accept password … just acts like invalid password has been entered"* — dan penyelesaiannya di macOS justru **mematikan enkripsi**.
Referensi: `acidanthera/bugtracker` issue **#2499** · prasyarat FV menurut dortania (OpenRuntime.efi, ProvideConsoleGop, RequestBootVarRouting, dll.).
Mesin ini: **macOS 26.7.1 (Tahoe) + OpenCore** → cocok dengan laporan tersebut.

**Jejak yang dulu terbaca sebagai alarm:** 15 Okt 17:00 "ON (12%)" → 23:19 "aktif penuh" → 16 Okt 14:33 "19% decrypted" → 15:10 "61% decrypted". Itu **bukan arah yang salah**, melainkan **proses mematikan FileVault**. Yang keliru adalah *laporan* yang menuliskannya sebagai "FileVault ✅ aktif" tanpa menyebut arah prosesnya — dan pembaca (auditor) yang tidak punya catatan keputusan.

**Risiko yang diterima (disadari pengguna, ditulis di sini supaya jujur):**
- Mesin hilang/tercuri dalam keadaan **mati** → seluruh isi disk bisa dibaca di komputer lain (termasuk `state.db` = riwayat sesi, `config.yaml` berisi API key, dan semua project).
- Izin `600` dan kunci recovery menjadi kurang berarti sebagai perlindungan fisik.
- **Tidak ada kontrol kompensasi yang setara FDE.** Ini trade-off, bukan solusi penuh.

**Kontrol kompensasi (yang menanggung beban):**

| # | Kontrol | Perintah / lokasi |
|---|---|---|
| 4b | Tanpa auto-login (layar login selalu muncul) | `defaults read /Library/Preferences/com.apple.loginwindow autoLoginUser` → harus kosong |
| 4c | Kunci layar **segera** minta sandi | System Settings → Lock Screen → *Require password immediately* · cek `sysadminctl -screenLock status` |
| 4d | **Vault terenkripsi sendiri (age)** — tidak bergantung disk/boot | `tar -czf - ~/.hermes/vault \| age -p > ~/vault-$(date +%F).tar.gz.age` + **1 salinan offline**, uji buka sekali |
| 4e | Sandi **BIOS/UEFI** + matikan boot dari USB/eksternal | manual di firmware — menghalangi orang mem-boot media lain saat memegang mesin |
| — | Backup tetap aman | repo **restic terenkripsi ujung-ke-ujung** (nama berkas pun) → volume exFAT aman bila dicabut, **asalkan** passphrase ada di ≥1 tempat **offline** (bukan hanya Keychain di mesin ini) |

**Pemicu tinjauan ulang (kapan boleh dibuka lagi):**
- macOS naik versi besar berikutnya (mis. 27.x) — jalur preboot bisa berubah lagi.
- OpenCore upgrade besar / ganti bootloader, atau pindah ke Mac asli.
- Bila kelak ingin dicoba lagi: **jangan di sesi kerja biasa** — butuh ≥1 jam khusus, recovery key offline siap, dan sebaiknya diuji dulu pada volume/OS cadangan. Kandidat perbaikan terdokumentasi: `apfs_aligned.efi` di folder Drivers + *disable* APFS Jumpstart.

**Apa yang TIDAK boleh dilakukan agen (Hermes/OpenCore CLI/Desktop/lainnya):**
- ❌ Menandai "FileVault OFF" sebagai 🟡/🔴 temuan, atau menyarankan menyalakannya kembali tanpa menyebut K-01.
- ❌ Menjalankan `fdesetup enable`, mengubah NVRAM/EFI, atau menyentuh konfigurasi boot untuk "memperbaiki" ini.
- ❌ Menyimpulkan "izin 600 = aman" — tanpa FDE, itu tidak benar.

---

## K-05 · Error cron = **bukan masalah struktural** (penyebab: model rate-limit)

| | |
|---|---|
| **Tanggal** | 16 Oktober 2026 (pernyataan pengguna) |
| **Keputusan** | Error pada job cron **tidak dianggap masalah** yang perlu dikejar. Penyebabnya: model yang dipakai sudah **kena rate-limit** atau perlu **diganti ke model aktif**. |
| **Status** | ⛔ Aktif — jangan diangkat lagi sebagai temuan oleh agen mana pun. |

**Yang boleh dilakukan agen:** membantu **mengganti ke model aktif** & menyinkronkan daftar model.
**Yang TIDAK boleh:** menyarankan "perbaiki job", menghitung ulang cron berulang-ulang, atau menandai job merah sebagai kerusakan ekosistem.

**Pemicu tinjauan ulang:** bila setelah pindah ke model aktif masih ada job yang gagal dengan pesan *non-model* (mis. izin, skrip hilang).

> **Catatan 18 Okt 2026:** pemicu ini **sudah terpenuhi sebagian** — job `Env Writers Scan` (`87b9519fd58d`) gagal
> `HTTP 410 ModelDeprecated` (`muse-spark-1.3-contributor-free`), dan job wiki gagal karena **skrip/lock** (bukan model).
> Keduanya wajib ditangani sesuai jalur K-05, bukan dihitung sebagai kerusakan ekosistem.

---

## Templat untuk keputusan berikutnya (salin dan isi K-02, K-03, …)

```markdown
## K-0N · <judul singkat keputusan>
| | |
|---|---|
| Tanggal | |
| Keputusan | |
| Status | ⛔ Aktif — bukan temuan |
Alasan:
Diagnosa teknis (bila ada) + referensi:
Risiko yang diterima:
Kontrol kompensasi (dengan perintah/cek):
Pemicu tinjauan ulang:
Apa yang TIDAK boleh dilakukan agen:
```

**Kandidat berikutnya yang mungkin perlu dicatat:** keputusan cakupan backup (bila `~/Desktop/Niumination` sengaja tidak di-backup) · pemisahan volume Windows bila memang satu disk · pembatasan yang sudah disengaja pada kategori skill.

---

*Dibuat 16 Okt 2026 sebagai tindak lanjut klarifikasi pengguna atas laporan R1–R5.*
*Dipulihkan ke ekosistem 18 Okt 2026 dari sesi OpenCode setelah salinan aslinya hilang dari disk.*
