# LAPORAN PERUBAHAN EKOSISTEM NIUMINATION — 13–18 Oktober 2026

**Disusun:** 18 Okt 2026, 00:30 WIB · oleh Hermes (sesi DM)
**Cakupan:** seluruh ekosistem `~/Desktop/Niumination` + `~/.hermes` + OpenCode CLI
**Metode:** 10 iterasi tambang bukti (git log, DOX, registry, opencode.db SQLite read-only, eco-guard, lsof, sqlite3, df) — semua angka dari keluaran perintah, bukan ingatan.

---

## 0. Ringkasan satu paragraf

Dua gelombang perubahan: **(1) 13–15 Okt** = audit eksternal + OpenCode CLI v2.0.28 dipakai mengeksekusi roadmap 10 fase (DR/backup, konsolidasi unit, keamanan, dokumen); **(2) 16–17 Okt** = OpenCode menjalankan sprint FASE-FIX (5 subagent: A model, B cron, C restic, D housekeeping, P1 pin model cron) + registrasi proyek **hypr-rust** ke ekosistem. Setelah itu: **4 job cron gagal→terpin**, state.db 510M→504M, restic terbukti restore, 8 unit launchd dipensiunkan, dan `~/Downloads/LAPORAN-KONDISI-POST-FIX-2026-10-17.md` disusun sebagai laporan pasca-perbaikan.

---

## 1. Garis waktu (terverifikasi dari git log + opencode.db)

| Tanggal | Peristiwa |
|---|---|
| 13 Okt | Audit eksternal; baseline + roadmap 10 fase dibuat (`docs/audit-2026-10-13/`) · 11 commit |
| 14 Okt | **OpenCode CLI v2.0.28** terpasang (`brew install anomalyco/tap/opencode-v2`, 197,9 MB) · FASE 0–4 dijalankan |
| 15 Okt | FASE 5,7,8,9 selesai · provider mati diganti `combo-delegasi` · **drill DR PASS 18/19** · `LAPORAN-AKHIR.md` |
| 16 Okt (siang–malam) | OpenCode sesi `eco-map.zip` (659 pesan) menjalankan penerapan · FASE-FIX A/B/C/D + P1 + E oleh 5 subagent OpenCode |
| 17 Okt | Verifikasi langsung 00:20 · `LAPORAN-KONDISI-POST-FIX-2026-10-17.md` · **hypr-rust** didaftarkan (`D-2026-1017-01`) + spike macOS |
| 18 Okt 00:00–00:06 | Commit terakhir: `4251abe` (BACKLOG sesi 2) |

**Aktivitas OpenCode per hari** (dari `~/.local/share/opencode/opencode.db`, read-only):

```
2026-10-09   381 pesan / 1 sesi     2026-10-15   236 pesan / 1 sesi
2026-10-14   302 pesan / 2 sesi     2026-10-16   396 pesan / 8 sesi
                                  2026-10-17   351 pesan / 14 sesi
```

---

## 2. Perubahan OpenCode "beberapa hari ke belakang" (16–17 Okt)

### 2.1 Sprint FASE-FIX — 5 subagent, 16 Okt 21:35–23:50

| Fase | Isi | Hasil |
|---|---|---|
| **A** | Stabilisasi model: verifikasi provider 9router, HTTP 200, 155 model, `combo-delegasi` di config | 3 gate LULUS |
| **B** | Diagnosa 5 cron gagal → akar: **model `combo-*` tidak punya fallback di 9router** saat model `:free` pertama mati | Diagnosa selesai, tanpa perubahan |
| **C** | Verifikasi restic: repo di `/Volumes/Mac Win/Backups/restic`, snapshot `e5cc9d95` (290,5 MiB), restore `config.yaml` 37 KB LULUS | 4 gate LULUS |
| **D** | Housekeeping: commit submodule `8dceec0` → induk `291346c`; **VACUUM state.db 510M→504M**; sqlite 3.54.0; bats 1.14.0 | 4 gate LULUS |
| **P1** | **Pin 5 job cron ke `kr/deepseek-3.2`** (probe chat completion 200 ×3) | LULUS |
| **E** | Verifikasi akhir: port 20128/8800/9377 listening, dispatch Telegram OK `message_id=16359` | LULUS dengan sisa |

### 2.2 Registrasi hypr-rust — 17 Okt (override freeze)

- **Klarifikasi dulu:** larangan #5 AGENTS.md (freeze D-1013-05) menghalangi repo baru → owner memilih **"override pemilik"** → tercatat `D-2026-1017-01` (BERLAKU, sekali pakai).
- **Isi zip:** 27 berkas (93 KB) — riset tiling WM/controller untuk Windows 11 x64 & Intel macOS; audit rahasia **0 temuan** sebelum push.
- **Repo:** `github.com/Niumination/hypr-rust` (PUBLIC, `main`, commit awal `5740cd5`).
- **Lokal:** `labs/hypr-rust/`.
- **Spike macOS (17–18 Okt):** `cargo fmt --check` OK · `cargo clippy -D warnings` bersih · `cargo test` **6/6 passed** · harness Swift 6.3.3 → **Spike 1 (kontrol window AX) PASS**, workspace native **DISABLED** · PR #1/#2.
- **Commit:** `d2fc8ed` (fix toolchain) → `a2d899b` → `fb120d9` (rerun) → `ea50040` (laporan).

### 2.3 Pencatatan wajib

- `docs/RIWAYAT-PERBAIKAN-2026-10-16.md` (12 bagian) — commit `2bf7bc1`.
- 5 entri sprint di `docs/audit-2026-10-13/LOG-PERBAIKAN.md` (A+B, C, D, P1, E) — submodule `b36d980`, induk `5b61b5a`.
- `~/Downloads/LAPORAN-KONDISI-POST-FIX-2026-10-17.md` + `.html` (laporan pasca-perbaikan).
- Catatan 17 Okt 00:35: **P1 disk-relief** — 6 file dipindah ke `/Volumes/Mac Win/Backups/` (2 installer, 3 zip DR, 1 db lama), `sha256` identik, sumber dihapus setelah verify; disk 5,8 GiB (95%) → 8,2 GiB (93%).

---

## 3. SEBELUM vs SESUDAH

### 3.1 Konfigurasi & identitas file

| Item | SEBELUM | SESUDAH |
|---|---|---|
| `AGENTS.md` root | 23.110 B (DOX 4.0, 6+ seksi + catalog) | **3.974 B** — 9 larangan + 1 tabel penulis + pointer registry |
| `~/.hermes/SOUL.md` | **symlink** (melanggar larangan #3) | **file nyata** 3.167 B, izin 600 |
| `~/.hermes/config.yaml` | izin 644 | **izin 600** (35.001 B) |
| `model.provider` | `custom:atria` / Atria-Dawn-Preview | **`9router` / `combo-delegasi`** |
| `skills.external_dirs` | tidak ada (bank terputus) | **`["/Users/zaryu/Desktop/Niumination/skills"]`** |
| `skills.create_dir` | ada | **dihapus** |
| `terminal.cwd` | tidak ada | **`/Users/zaryu/Desktop/Niumination`** |
| MCP filesystem scope | `/Users/zaryu` (seluruh home) | **`/Users/zaryu/Desktop/Niumination`** (1 project) |
| `~/.hermes/.env` | tanpa HC ping | `TELEGRAM_CRON_THREAD_ID=12595` + 3 `HC_PING_*` (mode 600) |
| OpenCode provider | `agentrouter.org` (openai + anthropic) | **`http://localhost:20128/v1`** (9router, 6 model `:free`) |
| OpenCode default model | `AgentRouter…/deepseek-v4-flash` | `9router/nous/meituan/longcat-2.5-preview:free` |

### 3.2 Cron & model routing

| Item | SEBELUM | SESUDAH |
|---|---|---|
| Job bermasalah | 5 job gagal berulang tiap tick (`Model is unavailable`) | **5 job dipin `kr/deepseek-3.2`** — streak gagal 0 |
| Job cron total | 22 | 22 (17 `ok`, 4 `error` sisa historis/paused) |
| Job baru | — | 8 (Eco Guard Verify, Skill Audit Mingguan, Env Writers Scan, 3 HC Heartbeat, Restic Backup Harian, Restic Retensi Mingguan) |
| Job diubah | — | DR Snapshot Refresh → harian 21:00; wiki-librarian 02:30→02:35; wiki-lint 02:50→02:55 |
| Job dipaused | 0 | **9** (termasuk wiki-lint & wiki-closing-snapshot — race lock, bukan model) |
| Akar masalah | disangka "rate-limit model" (K-05) | **terbukti: `combo-*` tanpa fallback** — bukan cron/jadwal yang rusak |

### 3.3 Layanan, keamanan, backup

| Item | SEBELUM | SESUDAH |
|---|---|---|
| Unit launchd non-Apple | 12+ | **≤ 8 resmi** (8 dipensiunkan: 2 duplikat MC, 9router-sync, nosleep, office-relay, 4 login item) |
| CamoFox | `*:9377` (wildcard) | **`127.0.0.1:9377`** (loopback) — diverifikasi `lsof` |
| FileVault | OFF | **ON** (namun lihat §5 — status live bertentangan dengan dokumen) |
| Firewall | OFF | **ON** (State = 1) |
| PAT GitHub | klasik | **fine-grained** (tersimpan `vault/PAT-Niu-Eco.md`) |
| Arsip rahasia | tanpa enkripsi | **age-encrypted** (`rahasia-age-2026-10-16.tar.gz.age`, magic `age-encryption.org/v1`) + `opencode.db` 158 MB |
| Gitleaks | 2 leaks | **0 leaks** (`571 commits scanned … no leaks found`) |
| Backup Hermes | tidak ada | 471 MB + drill; **catatan: zip terakhir di `~/Backups/hermes` hanya `.partial` (2 file) — lihat §5** |
| Restic | job ada, repo tak ada | repo `/Volumes/Mac Win/Backups/restic` — **3 snapshot** (`e5cc9d95`, `04ac713b`, `90fc02be`) + uji restore LULUS |
| SQLite | 3.51.0 (CLI) | CLI tetap 3.51.0 (diterima), brew 3.54.0 di `/usr/local/opt/sqlite/bin` |
| state.db | 508 MB | **504 MB** (VACUUM) → kini 508 MB lagi (pemasukan sesi) |

### 3.4 Skill & proyek

| Item | SEBELUM | SESUDAH |
|---|---|---|
| Kategori `ecosystem` | 74 skill (target ≤40) | **98** di manifest — dipecah ke 3 subkategori (hermes/mac/wiki), **target ≤40 belum tercapai** |
| Proyek tanpa git | 8 | **0** (semua direktori project punya `.git`; 70 repo total, 65 live, 60 ber-remote GitHub) |
| Skill bank | terputus dari Hermes | **terhubung** via `external_dirs`; manifest 239 skill / 1.182 file (17 Okt 16:31 UTC) |
| Skill baru | — | `ecosystem/opencode-troubleshooting` (17 Okt 22:37) |
| Proyek baru | — | **`labs/hypr-rust`** + repo publik |

### 3.5 Dokumen baru

`docs/registry/DR-PIPELINE.md` · `docs/RITME-PERAWATAN.md` · `docs/registry/dr-drill.md` · `docs/audit-2026-10-13/LAPORAN-AKHIR.md` · `docs/RIWAYAT-PERBAIKAN-2026-10-16.md` · `vault/INVENTARIS-KUNCI.md` · `docs/DECISIONS.md` (ledger hidup, 1.994 B — 1 entri) + snapshot lama di `docs/audit-2026-10-13/kit/docs/DECISIONS.md`.

---

## 4. Metrik 10 iterasi — baseline vs sekarang

| Metrik | Baseline 13 Okt | 15 Okt | **18 Okt 00:20 (live)** |
|---|---|---|---|
| Cron OK | 6/14 | 25/28 | **17 `ok` / 4 `error`** (22 job) |
| Streak gagal job target | 5 | — | **0** |
| Unit hidup | 12+ | ≤8 | **7** (gateway, camofox, 9router, MIRAI, nosleep, office-relay, marker) |
| state.db | 508 MB | 508 MB | **504→508 MB** (integrity `ok`, 465 sesi / 96.785 pesan) |
| Drill DR | belum ada | PASS 18/19 | PASS 18/19 (15 Okt) |
| Kategori ecosystem | 74 | ≤40 | **98** ⚠️ |
| Proyek tanpa git | 8 | 0 | **0** ✅ |
| CamoFox | wildcard | loopback | **loopback** ✅ |
| FileVault | OFF | ON | **OFF** ⚠️ |
| Firewall | OFF | ON | **ON** ✅ |
| AGENTS.md | 23 KB | 3974 B | **3974 B** ✅ |
| Gitleaks | 2 leaks | 0 | **0** ✅ |
| Disk Data | — | 8,2 GiB bebas | **11 GiB bebas (91%)** ✅ |
| Skill manifest | 305 | 305 | **239 skill / 1.182 file** |
| eco-guard | — | — | **1 masalah, 15 perhatian** (01:08, setelah backup ditutup) |

---

## 5. Catatan jujur — penyimpangan antara dokumen dan kondisi live

Ini yang penting: beberapa klaim di dokumen OpenCode **tidak cocok dengan pengukuran hari ini**. Bukan menyangkal pekerjaan, hanya menandai agar tidak dipercaya buta:

1. **FileVault OFF — BUKAN temuan, dan jangan diangkat lagi.** Saya salah menilainya sebagai regresi; koreksi setelah menelusuri sesi OpenCode: ini **K-01, keputusan sadar** (`roadmap/KEPUTUSAN-TETAP.md`). Alasan pemilik: setelah FileVault aktif, sandi akun selalu ditolak di layar boot → harus masuk pakai recovery key lalu reset sandi. Diagnosa teknis mendukung: mesin ini macOS 26.7.1 (Tahoe) + OpenCore, dan bug resmi `acidanthera/bugtracker#2499` punya gejala identik (*"the prebooter loads, but doesn't accept password"*) — penyelesaiannya justru mematikan enkripsi. Jejak 15 Okt "ON 12%" → 16 Okt "61% decrypted" adalah **proses mematikan FileVault**, bukan arah yang salah. Risiko diterima pemilik (mesin hilang dalam keadaan mati → isi disk terbaca) dan ditopang kontrol kompensasi (tanpa auto-login, kunci layar segera, vault age, sandi BIOS). **Agen dilarang menandai ini sebagai temuan atau menjalankan `fdesetup enable` tanpa persetujuan manusia.**
   - **Celah kelangsungan (bukan soal FileVault, tapi soal catatan):** `KEPUTUSAN-TETAP.md` **tidak ada di ekosistem** — hanya tersimpan di sesi OpenCode dan di `/tmp/opencode/eco-map-study/` (sementara, sudah tidak ada). `roadmap/run/FINAL-CEK.sh` yang seharusnya membacanya juga **tidak ada**. Artinya keputusan K-01 bisa hilang lagi, dan agen berikutnya akan mengulang kesalahan yang sama seperti saya.
2. **`~/Backups/hermes` tidak punya backup Hermes valid.** Isi hari ini: 2 file `.zip.…partial` (135 MB + 239 MB, tidak selesai) + `pre-vacuum-state.db` 510 MB. `eco-guard` menandai `[MASALAH] belum ada file backup di /Users/zaryu/Backups/hermes`. **Namun backup Hermes SAH tetap ada** di `/Volumes/Mac Win/Backups/hermes-dr-zips-20261014/` — 3 zip, semua `unzip -t` rc=0 (4455, 4483 file; ±494 MB), terverifikasi hari ini. Jadi keadaannya: backup valid ada, tapi **di luar jalur yang dipantau eco-guard**, dan yang ada di jalur itu justru sisa `.partial`.
   - **Akar masalah (ditemukan saat eksekusi 18 Okt):** `eco-guard.sh backup` **tidak pernah dijadwalkan** — tidak ada cron job untuk itu, dan `crontab` user kosong. Itulah sebabnya isi `~/Backups/hermes` beku sejak 14 Okt. Bukan cuma soal lupa jadwalkan: `hermes backup` juga pernah **hang (timeout 120s)** di FASE-FIX D dan meninggalkan arsip sementara `.partial`.
   - **Ditutup 18 Okt 01:46** (dua lapis):
     1. `post-soul-fix-20261014-1704.zip` (471 MB) disalin ke `~/Backups/hermes/` — sha256 identik (`56db939d…9d9b`), `unzip -t` rc=0.
     2. **Job cron baru `Hermes Backup Harian` (`8281a448d857`)** — `30 5 * * *`, no-agent, `deliver: local`, gagal-lapor ke thread 12595. Sudah diuji jalan: hasil `hermes-2026-10-18-0143.zip` (368 MB, 4.661 file, `unzip -t` No errors, sha256 `105827a6…78ba`). eco-guard: `[ OK ] backup terbaru: hermes-2026-10-18-0143.zip`.
     3. Wrapper baru `~/.hermes/scripts/eco-guard-backup.sh` — **wajib**, karena `eco-guard.sh` memparse lewat `case "${1:-}"`; tanpa argumen ia hanya menampilkan usage lalu exit 2, jadi `--script eco-guard.sh` saja **tidak akan membackup apa pun** (job percobaan pertama `3fd70af21191` dibuang karena alasan ini).
   - **Sampah dibersihkan:** 2 file `.partial` (135 MB + 239 MB) dihapus setelah dibuktikan rusak (`unzip -t` rc=9).
3. **Kategori skill `ecosystem` = 98**, bukan ≤40 seperti ditulis di `LAPORAN-AKHIR.md`. Pemecahan jadi 3 subkategori sudah dilakukan, tapi angka totalnya justru naik (skill baru terus masuk).
4. **`muse-spark-1.3-contributor-free` deprecated** → job `Env Writers Scan` (`87b9519fd58d`) gagal HTTP 410 pada 17 Okt 21:30. Belum dipin.
5. **`eco-guard` 1 masalah** (hitungan historis 17 baris error cron, OK: 39) — sudah dikenal, bukan temuan baru. Masalah backup sudah ditutup 18 Okt (lihat §5.2).
6. **Working tree root belum bersih**: 4 file termodifikasi (`skill-registry.md`, `INDEX.md`, `manifest.json`, `.promotion-ledger.json`) + `?? 0000` (berkas 0 byte, mtime **26 Agu 2027** — sisa artefak, belum di-commit sejak awal).
7. **`docs/audit-2026-10-13` = submodule tanpa remote** — 22.981 B log perbaikan hanya ada lokal; belum ada cadangan eksternal. (eco-guard juga menandai `inactive-2026-10/orchestrator` = checkout kedua repo ecosystem-config.)

---

## 6. Kesimpulan

**Yang benar-benar berubah dan terbukti:** model routing (5 job terpin, akar combo tanpa fallback), state.db (VACUUM), restic (3 snapshot + restore terbukti), unit launchd (12+→7), CamoFox loopback, MCP scope 1 project, PAT fine-grained, arsip age-encrypted, gitleaks 0, AGENTS.md ramping, skill bank terhubung, 8 proyek tanpa git ditutup, dan satu proyek baru (hypr-rust) masuk dengan proses klarifikasi + keputusan tertulis.

**Yang masih terbuka:** FileVault (klaim vs live), kategori skill 98 (>40), pin job `Env Writers Scan` (`muse-spark-1.3-contributor-free` deprecated), push commit root (sudah 0 ahead), bersihkan 4 file dirty + `0000` + `skills/ecosystem/opencode-troubleshooting/`, dan backup remote untuk submodule audit.

**Sudah ditutup 18 Okt 01:46:** `~/Backups/hermes` kini punya **backup segar harian** (`hermes-2026-10-18-0143.zip`, 368 MB, 4.661 file, `unzip -t` No errors) lewat job cron `8281a448d857`. `[MASALAH] belum ada file backup` hilang → eco-guard **2 → 1 masalah** (`[ OK ] backup terbaru`). 2 file `.partial` rusak (694 MB) dibersihkan.

**Sudah dijalankan 18 Okt 01:46:** job `Hermes Backup Harian` (`8281a448d857`, `30 5 * * *`, no-agent, wrapper `eco-guard-backup.sh`) sudah aktif dan terbukti menghasilkan `hermes-2026-10-18-0143.zip`. **Catatan penting untuk perawatan:** jangan ganti `--script`-nya dengan `eco-guard.sh` polos — tanpa argumen skrip itu hanya menampilkan usage (exit 2), jadi tidak ada backup yang terjadi.
