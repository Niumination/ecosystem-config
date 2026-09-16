# Audit DR & Backup — rev 1 (temuan mentah)

**Tanggal:** 17 Sep 2026
**Konteks:** Persiapan mekanisme restore penuh (Hermes + dotfiles/mac + ekosistem) untuk pindah device.
**Status:** REV 1 — temuan terverifikasi, **belum** rencana final. Lihat "Celah yang belum diaudit" di bawah.

## Tujuan yang diminta owner

1. Hermes agent + instalasi + seluruh isinya — full/portable, siap pakai, kecuali yang bisa di-generate ulang
2. Mac dotfiles — kecuali yang bisa rebuild/regenerate
3. Semua pengaturan/konfigurasi ekosistem — termasuk berkas yang di-gitignore dan tidak bisa direbuild (masalah utama saat reclone)
4. (Di luar scope) Downloads/Documents/dll — sudah dibackup manual ke cloud oleh owner

Keputusan owner: **satu repo privat**, mekanisme restore harus "tanpa kesalahan" (pola dotfiles/stow).

## Kondisi nyata yang terukur

### Tidak ada Time Machine
- `tmutil destinationinfo` → `No destinations configured`
- Hanya 1 APFS local snapshot (media sama → bukan perlindungan kehilangan device)
- Tidak ada disk eksternal (konfirmasi owner)
- Disk internal: 128 GB, 17 GB free → jalur backup = GitHub

### Ukuran yang harus dilindungi
| Item | Ukuran |
|---|---|
| `~/Desktop/Niumination` | 12 GB |
| `~/.hermes` | 719 MB |
| `~/.ssh` (kunci) | 419 B (privat) |
| `~/src/hermes-agent` | 3,1 GB |

### `~/.hermes` 719 MB — rincian
| Kategori | Item | Ukuran |
|---|---|---|
| REGEN | `lsp/` | 111 MB |
| REGEN | `bin/` | 81 MB |
| REGEN | `firefox-profile-backup/` | 86 MB |
| REGEN | `checkpoints/` | 61 MB |
| REGEN | `logs/` | 51 MB |
| REGEN | `cache/` | 12 MB |
| REGEN | `models_dev_cache.json` | 4,7 MB |
| DATA | `state.db` | **241 MB** |
| DATA | `sessions/` | 56 MB |
| DATA | `kanban/` + `kanban.db` | 1,4 MB + 123 KB |
| DATA | `projects.db`, `verification_evidence.db` | 45 KB + 115 KB |
| WAJIB | `skills/` | 13 MB (1.075 berkas) |
| WAJIB | `cron/` | 380 KB (67 berkas) |
| WAJIB | `.env`, `config.yaml`, `auth.json`, `SOUL.md`, `custom_persona.json`, `self-schema.json`, `memory_tiering.json`, `memories/`, `plugins/`, `platforms/`, `scripts/`, `install_id` | ~60 KB |

## Berkas ekosistem: gitignored tapi tidak tergantikan

Total 167.491 berkas gitignored → **162.634 regenerable** (deps/cache/build) → **4.857 kandidat** di 28 repo.

Prioritas kritis:
1. **Kunci signing Android** — `apps/ai-file-manager-android/play-store/signing/ai-organizer-release.jks` + `upload_certificate.pem` → hilang = app di Play Store tidak bisa di-update permanen
2. **`vault/`** — 2,1 MB, tidak ada di repo mana pun
3. **`.env`/`.env.local` ×13** — kune-ya.com, niu-lkh, arch-web-dashboard, mac-web-dashboard, cc-acehtengah, sapa-ai, niu-dash-fullstack, niu-kanban-dash, tedeo-kanban, audit-ti-at, niu-vermilion, pi-app-studio-mata, niutui
4. **`.vercel/project.json` ×8** + `.vercel/env` (cc-acehtengah)
5. **DB & data** — `services/niu-mission-control/data/swarm_state.db`, `apps/kune-ya.com/prisma/dev.db`, `sites/niu-dash-fullstack/data/projects.json`, `labs/mata-aihackfest-2026/mata/config.json`, `services/cc-acehtengah/data/dtsen-raw/*` (zip+csv+metadata, memuat data kependudukan)
6. **`apps/PemdiAcehTengah/.claude/skills/`** — 1.837 berkas

## Delapan rantai ketergantungan yang akan memutus saat restore

1. **`~/.hermes/SOUL.md` adalah symlink** → `~/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/hermes/SOUL.md`. Restore Hermes tanpa dotfiles = SOUL menggantung = identitas default.
2. **Bank skill 3 salinan tidak sinkron:** `~/.hermes/skills` **202** · ecosisstem `skills/` **121** · `JHermUSB-portable/config/skills` **178**. **81 skill hanya ada di `~/.hermes`** (apple/*, creative/*, autonomous-ai-agents/*, camofox-browser, hermes-agent, dll). **3 skill drift** (versi Hermes lebih baru): `ecosystem-dox-maintenance` (09-16 16:22 vs 13:11), `hermes-configuration` (09-17 vs 09-10), `git-security-sanitization` (09-16 vs 09-01).
3. **Instalasi Hermes di `~/src/hermes-agent` (3,1 GB)** — di luar 3 scope. Fork `Niumination/hermes-agent`, upstream `NousResearch/hermes-agent`. **2 patch lokal** (`0da89439d3` notif gateway BI + status block + bounded-wait; `05ef3d7518` notif startup) — ada di remote **hanya** di branch `origin/backup-local-20260910`, **bukan di `main`**. Clone + checkout `main` = patch hilang diam-diam.
4. **75 berkas konfigurasi memuat path absolut `/Users/zaryu`** (launchd plist, script, SKILL.md) → restore hanya aman jika username device baru sama.
5. **`.hermes/.env` dirujuk 7 script ekosistem** (`model-health-probe-wrapper.sh`, `model-checker.py`, `model-status-probe-cron.sh`, `secret-scan-staged.py`, dll) → kredensial Hermes = prasyarat script ekosistem; absen = gagal senyap.
6. **4 submodule `file://` lokal** (`inactive-2026-09/{Ultra,niu-studio,zen,niumination-workspace}`) → pasti pecah. Plus submodule remote termasuk `aihackfest-mata-media` (privat).
7. **11 launchd agent** — `ai.hermes.gateway`, `ai.hermes.gateway-marker`, `com.niu.missioncontrol`, `com.niumination.missioncontrol`, `com.niumination.9router-sync`, `ai.hermes.camofox`, `com.9router.autostart`, `com.niumination.nosleep`, 3 Google. Semua path absolut.
8. **`~/.hermes-portable/venv` sudah rusak** — hanya berisi `lib/`, tanpa `bin/`; `bin/python`, `bin/hermes`, `bin/pip` HILANG. Dirujuk `scripts/setup-uacc.sh` + `test-uacc.py` → UACC mati senyap **sekarang**, bukan hanya saat pindah device. Interpreter hidup: `~/src/hermes-agent/.venv/bin/python` (17 MB).

## Barang yang "tidak tergantikan" (peringkat)

1. Kunci signing Android (`.jks` + cert)
2. `vault/` 2,1 MB
3. Kunci SSH `~/.ssh/id_ed25519_niumination` (fingerprint `SHA256:4rYXsvVPC7SNPqPYJLY9fKH5GeaHC5ZBRhnIBCNhczc`) — device baru butuh ini untuk clone repo privat
4. 13 `.env` + 8 `.vercel/` + `~/.npmrc` + `~/.ssh/config`
5. DB & data kerja (swarm_state, prisma dev.db, projects.json, mata/config.json, dtsen-raw)
6. Hermes: config, persona, 202 skill, 67 cron, memories, sessions, state.db

Catatan: **tidak ada kunci GPG** di device ini (`~/.gnupg` kosong, `commit.gpgsign=false`).

## Chicken-and-egg: backup tidak bisa menyelamatkan dirinya sendiri

Repo privat butuh kunci SSH untuk di-clone; kunci SSH harus ada di repo privat. Sama untuk passphrase enkripsi. → Wajib ada jalur pemulihan di luar repo (cloud pribadi owner / kertas).

**Tidak ada GPG** — jadi enkripsi harus memakai tool lain (age/SOUL/git-crypt/openssl) → **belum diverifikasi tool mana yang terpasang**.

## Celah yang belum diaudit (rev 1 jujur menyatakan ini)

1. **Fitur backup/export/migrasi bawaan Hermes** — belum diperiksa sama sekali (`hermes --help`, subcommand `backup`/`export`/`profile`). Bisa jadi platform sudah menyediakan solusi first-party yang lebih andal.
2. **Komponen di luar 3 scope yang belum dipetakan:** `~/.9router/` (db `data.sqlite` + `machine-id`, dirujuk skill), `~/.camofox/` (launchd), `~/.config` (113 MB / 6.832 berkas — belum disaring), `~/.local/bin`, `~/.hermes/profiles/`, `/Applications` (NIU CAST.app, Hermes.app), `~/.ssh/agent/`, `crontab -l`, `~/Library/Preferences`, browser profile.
3. **Tool enkripsi & backup yang tersedia** (`age`, `git-crypt`, `gpg`, `openssl`, `zstd`, `restic`, `sqlite3`) — belum dicek.
4. **Kapabilitas `gh`** (scope token: bisakah membuat repo privat baru?) — belum dicek.
5. **Job cron Hermes** — hanya jumlah berkas (72) yang diketahui; definisi job (nama, jadwal, delivery) belum diinventaris.
6. **Berkas >50 MB** yang akan ditolak/diperingatkan GitHub — belum dipindai.
7. **Snapshot SQLite yang konsisten** — `state.db` 241 MB sedang aktif dipakai (WAL); menyalin mentah berisiko korup. Metode benar (`sqlite3 .backup` / `VACUUM INTO`) belum diterapkan.
8. **Total ukuran paket backup** vs batas GitHub (file 100 MB, repo 1–5 GB) — belum dihitung.
9. **Klasifikasi 202 skill**: mana bawaan Hermes (dari `~/src/hermes-agent/skills/`) vs buatan owner — belum dipisahkan.
10. **Asumsi OS device baru** — diasumsikan macOS dengan username `zaryu`; belum dikonfirmasi (JHermUSB punya `launch.bat`/`restore-gui.ps1` → ada skenario Windows).
11. **Validitas kredensial** (13 `.env` + `vault/`) — mana yang masih hidup/expired, belum diperiksa.
12. **Uji restore nyata** — belum ada satu pun.

## Bukti (perintah kunci)

- `tmutil destinationinfo` → `No destinations configured`
- `df -h` → `/System/Volumes/Data` 95 Gi used, 17 Gi avail
- `du -sh ~/Desktop/Niumination ~/.hermes` → 12 G / 719 M
- Audit ignored: 167.491 berkas → 162.634 regenerable → 4.857 kandidat / 28 repo
- `readlink ~/.hermes/SOUL.md` → `/Users/zaryu/Desktop/Niumination/dotfiles/zaryu-terminal-dotfiles/hermes/SOUL.md`
- Bank skill: 202 / 178 / 121; drift 3; hanya-di-Hermes 81
- `git -C ~/src/hermes-agent branch -r --contains HEAD` → `origin/backup-local-20260910`
- `git -C ~/src/hermes-agent rev-list --count origin/main..HEAD` → 7944
- `ls ~/.hermes-portable/venv/` → hanya `lib/`; `bin/python` → `No such file or directory`
- `git -C ~/src/hermes-agent status --porcelain` → 0 perubahan (bersih)
