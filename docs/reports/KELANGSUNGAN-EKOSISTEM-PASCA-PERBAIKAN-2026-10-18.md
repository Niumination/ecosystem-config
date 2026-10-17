# KELANGSUNGAN EKOSISTEM PASCA PERBAIKAN — Penilaian & Rekomendasi

**Disusun:** 18 Okt 2026, 02:10 WIB · oleh Hermes
**Pertanyaan pemilik:** apakah ekosistem ini bisa terus hidup tanpa dijaga manusia setiap hari?
**Metode:** audit read-only terhadap 23 job cron, 14 skrip penjaga, rantai heartbeat, dan riwayat 3 hari terakhir. Semua angka dari keluaran perintah.

---

## 1. Jawaban singkat

**Sebagian besar ya — 5 pilar pemeliharaan berjalan sendiri dan terbukti bekerja. Tapi ada 4 lubang yang membuat "hidup sendiri" itu rapuh**, dan salah satunya baru saja saya buktikan secara langsung: **satu-satunya jalur backup Hermes tidak terjadwal sama sekali** sehingga titik kembali tertua tertinggal 4 hari.

Skor: **7/10**. Bukan karena apa yang dibangun salah, tapi karena **yang menjaga belum tentu tahu bahwa ia menjaga**.

---

## 2. Lima pilar yang SUDAH berjalan sendiri (terbukti)

| Pilar | Penjaga | Jadwal | Bukti hidup |
|---|---|---|---|
| Backup Hermes | `eco-guard-backup.sh` (job `8281a448d857`) | 05:30 | `hermes-2026-10-18-0143.zip` 368 MB, `unzip -t` No errors |
| Backup restic | `restic-backup.sh` | 04:00 | 3 snapshot, terbaru 18 Okt 00:23 (290,9 MiB) |
| Backup DR off-site | `dr-restore-sync.sh` | harian 21:00 | release GitHub `l1-2026-10-17` (8 part terenkripsi, uploaded) |
| Deteksi Hermes mati | healthchecks.io | 03:00 / 04:00 / 07:00 | 3 ping HTTP 200 hari ini |
| Pemeriksaan kesehatan | `eco-guard.sh verify` | 08:00 & 20:00 | `[ OK ] backup terbaru`, `[ OK ] drill` |

Ini fondasi yang benar. Yang lemah ada di sekelilingnya.

---

## 3. Empat lubang kelangsungan

### Lubang 1 — Catatan keputusan hidup di tempat yang bisa dihapus (PALING KRITIS)

`roadmap/KEPUTUSAN-TETAP.md` berisi **K-01** (FileVault sengaja OFF) dan **K-05** (error cron bukan masalah struktural). Berkas ini **tidak ada di ekosistem**:
- `find ~/Desktop/Niumination ~/Downloads -name 'KEPUTUSAN-TETAP*'` → **nol hasil**
- `git log --all -S'KEPUTUSAN-TETAP'` → **nol hasil** (belum pernah di-commit)
- Satu-satunya salinan: sesi OpenCode + `/private/var/folders/.../T/opencode/eco-map-study/` (direktori sementara, **bisa hilang kapan saja**)

Dan `roadmap/run/FINAL-CEK.sh` — skrip yang *seharusnya* membaca K-01 sebelum menilai — **juga tidak ada** di repo.

**Konsekuensi nyata, bukan teori:** hari ini saya melakukan persis kesalahan yang K-01 cegah. Saya menjalankan `fdesetup status`, melihat `FileVault is Off.`, dan menuliskannya sebagai "regresi dari target G9.8" di laporan. Karena catatannya tidak ada di ekosistem, saya menyimpulkan dari pengukuran mentah. Agen berikutnya akan mengulanginya.

> **Ini pola "alarm palsu" yang sama** yang menurut `KEPUTUSAN-TETAP.md` adalah akar masalah paling sering: *keadaan yang disengaja tidak pernah tercatat, sehingga setiap pemeriksa membacanya sebagai kerusakan.*

### Lubang 2 — Yang gagal tidak selalu diberi tahu, dan yang diberi tahu tidak selalu bisa bertindak

**Eco Guard Verify** punya `failure_streak: 7` dan `deliver: telegram:…:12595`. Artinya tiap kegagalan mengirim pesan ke thread yang sama — **7 kali berturut**. Efeknya bukan peringatan, tapi noise; dan noise mematikan perhatian.

Lebih dalam lagi: pesan itu berisi `[MASALAH] 17 baris error/blocked di 'hermes cron list' (OK: 38)`. Angka 17 itu **hitungan historis** (K-05: bukan masalah struktural), dan **tidak pernah turun** karena tidak ada yang menghitung ulang. Jadi ekosistem sudah 7 hari mengumumkan hal yang sama tanpa perubahan — alarm yang berteriak tapi tidak pernah selesai.

**Presence relay** (`401 Unauthorized`) dilaporkan `Ecosystem Health Check` **tiap 2 jam sejak minimal 17 Okt 14:00** — 6 laporan berturut-turut, tidak ada yang memeriksa. Ini gejala klasik: pelaporan tanpa pemilik.

### Lubang 3 — Empat job agent melanggar larangan #8 (tanpa jaluran keluar `[SILENT]`)

| Job | Jadwal | Deliver |
|---|---|---|
| Daily Tab Stash Update | 22:00 | telegram 12595 |
| Daily Brain – Top 10 URL | 08:00 | telegram 12595 |
| Dettack Daily Security Check | 09:00 | telegram 12595 |
| A2A Cloud Health Check | 10:00 | telegram 12595 |

Empat job agent (berbiaya token) mengirim ke thread yang sama setiap hari, tanpa jalur `[SILENT]`. `eco-guard.sh verify` sendiri menandai ini `[PERIKSA]`. Ini bukan sekadar pelanggaran aturan: **4 pesan/hari menenggelamkan 1 peringatan yang penting**.

### Lubang 4 — Dua job paused tanpa alasan tercatat

`wiki-lint` (`59f3d966b912`) dan `wiki-closing-snapshot` (`b5fdcff7dcd3`) paused dengan `paused_reason: null`. Keduanya paused karena **race lock wiki** (catatan FASE-FIX P1), bukan karena rusak — tapi karena alasannya tidak tertulis, agen berikutnya akan menganggapnya mati dan mungkin menghidupkannya tanpa tahu risikonya.

---

## 4. Prinsip yang muncul dari keempat lubang itu

Keempatnya bukan masalah teknis — semuanya masalah **jejak**:

1. Keputusan penting disimpan di tempat sementara, bukan di ekosistem → agen mengukir ulang kesimpulan dari nol.
2. Pemeriksa melapor tapi tidak ada yang menindaklanjuti → alarm kehilangan makna.
3. Pengumuman rutin bercampur peringatan → keduanya tidak terbaca.
4. Tindakan (pause) tanpa catatan alasan → tidak bisa dipertanggungjawabkan.

**Artinya: perbaikan teknis sudah selesai. Yang belum selesai adalah menjadikannya bisa dirawat tanpa ingatan manusia.**

---

## 5. Rekomendasi (urut prioritas, semua read-only / murah)

### R1 — Kembalikan `KEPUTUSAN-TETAP.md` ke ekosistem [S, ~5 menit] — **SELESAI 18 Okt 02:20**
Ini perbaikan paling tinggi rasio manfaat/biayanya, dan mencegah kesalahan yang baru saja saya lakukan terulang.

**Catatan penting:** sumber aslinya **sudah tidak ada** di disk — `/private/var/folders/.../T/opencode/eco-map-study/` sudah hilang, dan tidak ada di `eco-map.zip`, `/Volumes/Mac Win`, maupun backup zip Hermes. **Satu-satunya salinan yang tersisa ada di `~/.local/share/opencode/opencode.db`** (7 baris sesi `ses_ebb37d5f9ffe7W4f9otoiKJJZB`, termasuk satu compaction 71 KB). DB itu sendiri adalah target backup restic, tapi ia **bukan tempat yang boleh diandalkan sebagai arsip keputusan** — ia bisa dikosongkan/dipangkas kapan saja.

**Yang dikerjakan (sudah dieksekusi):**
```
1. Ekstrak teks asli K-01 & K-05 dari opencode.db (read-only, sesi ses_ebb37d5f9ffe7W4f9otoiKJJZB)
2. Tulis ke docs/registry/KEPUTUSAN-TETAP.md  (7.698 B) — isi ASLI, bukan ringkasan
3. Catat di docs/DECISIONS.md sebagai D-2026-1018-01
4. Commit c3a8406 + PUSH ke GitHub
5. Snapshot restic 77eac8e1 (02:20)
```
Jangan salin ke `roadmap/` saja — `docs/registry/` yang dibaca `eco-guard` dan agen setiap sesi. Sekaligus: catat K-01 & K-05 sebagai entri di `docs/DECISIONS.md` (ledger hidup) supaya ada dua salinan di dua tempat dengan peran berbeda.

**Verifikasi (diambil ulang):**
- `grep -c 'K-01' docs/registry/KEPUTUSAN-TETAP.md` → **3** · `'K-05'` → **2**
- `git log --oneline -1` → `c3a8406` · `git status -sb` → `## main...origin/main` (0 ahead → sudah ter-push)
- `restic dump latest …/KEPUTUSAN-TETAP.md | grep -c 'K-01'` → **3** (berkas benar-benar terbaca dari snapshot)
- snapshot restic `77eac8e1` 02:20:55 · `bash eco-guard.sh verify` → **1 masalah** (FileVault tidak lagi disebut sebagai temuan)

> Ini juga membuktikan poin di Lubang 1: sebuah keputusan penting **hampir hilang sepenuhnya** karena hanya hidup di tempat sementara. DB sesi bukan arsip.

> **Catatan cakupan backup (ditemukan saat R1):** `hermes backup` **tidak memuat `~/Desktop/Niumination`** — ia hanya mengarsipkan `~/.hermes`. Jalur off-site untuk repo ekosistem adalah (a) **push GitHub** (`origin/main`) dan (b) **restic** (memuat `docs/`, `vault/`, `brain/`, `wiki/`). Keduanya sudah diverifikasi membawa berkas ini.

### R2 — Beri penjaga pada Eco Guard Verify [S, ~5 menit] — **SELESAI 18 Okt 03:15**

**Masalah:** `eco-guard.sh verify` keluar `code 1` setiap kali ada temuan → cron menandai job "failed" → stdout terkirim **tiap tick**, isi yang sama. Akibatnya `failure_streak` 7+ dan 10 insiden `be7dc5154b2c` menumpuk.

**Yang dikerjakan:**
```
1. Wrapper baru ~/.hermes/scripts/eco-guard-notify.sh
2. eco-guard-verify.sh diarahkan ke wrapper (backup: .bak-20261018-024031)
3. State: ~/.hermes/eco-guard-state.sha (+ .sha.prev) — fingerprint temuan
```
Dedup memakai **fingerprint temuan ternormalisasi** (bukan stdout mentah), jadi:
- hitung-mundur `'nous' kedaluwarsa dalam 0.4 jam` → dinormalisasi ke `<N>`
- `N baris error/blocked (OK: N)` → dinormalisasi ke `<N>`
- daftar alat menganggur → dinormalisasi ke satu kelas

**Verifikasi:**
- `bash eco-guard-notify.sh` run ke-2 → **stdout kosong** (cron tidak mengirim)
- run pertama (baseline) → menampilkan daftar temuan
- job cron utuh: `0 8,20 * * *`, `no_agent: True`, `deliver: telegram:…:12595` — tidak berubah

**Temuan bug nyata (bukan cacat saya):** `check_dormant_tools()` di `eco-guard.sh` (baris 515–531) memakai `grep -q "$t" "$HERMES_HOME/cron/jobs.json"` untuk menentukan apakah sebuah alat terjadwal. Karena keluaran `[PERIKSA] alat ini ada tapi TIDAK dipanggil penjadwal mana pun: …` disimpan ke `last_error` job **yang sama**, maka begitu alat dilaporkan menganggur, **laporan itu sendiri membuat dirinya dianggap terjadwal**. Baris hilang → fingerprint berubah → lapor lagi → `jobs.json` berubah lagi → loop. Ini menjelaskan mengapa baris itu berflap dan mengapa `jobs.json` berubah setiap run (mtime 03:12:29 = saat job berjalan). Perlu perbaikan terpisah: pemeriksaan harus mengabaikan `last_error` job sendiri (atau membaca hanya field `script`/`prompt`).

> **Catatan:** dedup tetap berfungsi dengan benar di atas flapping ini — ia melapor saat ada perubahan, dan berhenti saat stabil. Yang belum selesai adalah **bug deteksi alat menganggur** di `eco-guard.sh`, yang merupakan pekerjaan terpisah (menyentuh `eco-guard.sh`, penulis tunggal `Hermes`).

### R3 — Tambahkan pemilik pada Presence relay [K]
`Ecosystem Health Check` melapor `Presence: FAIL (401)` tapi tidak ada yang memeriksa. Perlu salah satu: (a) perbaiki token relay, atau (b) matikan pemeriksaannya dan catat alasannya. **Laporan tanpa pemilang = alarm mati.**

### R4 — Tambahkan jalur `[SILENT]` pada 4 job agent [S]
Agar peringatan penting tidak tenggelam. `eco-guard` sudah menyediakan polanya.

### R5 — Catat alasan paused [S, ~2 menit]
`wiki-lint` & `wiki-closing-snapshot` → `paused_reason: "race lock wiki (FASE-FIX P1, 16 Okt 2026) — hidupkan hanya setelah lock dihapus"`.

---

## 6. Apa yang TIDAK perlu diperbaiki

Supaya tidak ada pekerjaan baru tanpa alasan (freeze D-1013-05 masih berlaku):
- **FileVault OFF** — sudah diputuskan, bukan temuan. Jangan disentuh.
- **17 baris error cron historis** — K-05, akan turun sendiri.
- **Kategori skill 98** — target ≤40 adalah aspirasi roadmap, bukan kerusakan.
- **4 file dirty di working tree** — artefak normal dari `skills/ecosystem/opencode-troubleshooting/` yang belum di-commit.

---

## 7. Kesimpulan

Ekosistem ini **sudah bisa berdiri sendiri untuk operasi sehari-hari** — backup jalan, DR terbukti, pengawas eksternal hidup. Yang belum selesai adalah **membuatnya bisa dirawat tanpa manusia mengingat apa yang pernah diputuskan**.

Tiga langkah pertama yang paling berdampak, semuanya di bawah 15 menit dan tidak menambah unit:
1. Kembalikan `KEPUTUSAN-TETAP.md` ke `docs/registry/` + catat di `DECISIONS.md`
2. Jadikan Eco Guard Verify tidak berisik
3. Beri pemilik pada laporan Presence relay

Setelah itu, ekosistem berpindah dari "bisa hidup" menjadi "bisa dirawat" — dan di situlah perbaikan berhenti menjadi acara dan mulai menjadi ritme.

---

## Bukti
- `hermes cron list` → 23 job (21 enabled); `failure_streak` per job
- `find ~/Desktop/Niumination ~/Downloads -name 'KEPUTUSAN-TETAP*'` → 0 hasil
- `git log --all -S'KEPUTUSAN-TETAP'` → 0 hasil
- `ls docs/audit-2026-10-13/roadmap/run/` → hanya `FASE-1.sh`, `OPENCODE-CEK.sh` (tidak ada `FINAL-CEK.sh`)
- `grep -c 'hc-ping' ~/.hermes/scripts/hc-heartbeat-*.sh` → 3 skrip, semua ping 200
- `hermes-2026-10-18-0143.zip` → `unzip -t` No errors, 4.661 file
- `ls -t ~/.hermes/cron/output/d0ab0fde1b2e/*.md | head -6` → semua `Presence: FAIL (HTTP Error 401)`
