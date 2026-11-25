# ZB-Vela — Status Ekosistem

> Tanggal: **25 November 2026** (pembaruan: voice-gateway↔OMB, storage, Kaggle uncensored; audit dasar 21 Nov tetap berlaku) • VPS: VM-11-184-ubuntu (Tailscale: zb-vela, 100.77.18.39)
> Semua status diverifikasi langsung via systemctl / curl / journalctl / DB pada tanggal di atas.
> Dokumen ini menggantikan versi 19 November 2026. Riwayat keputusan lama tetap dipertahankan di seksi 8b–8e.

---

## 1. Ringkasan Kondisi (21 Nov 2026 — audit langsung)

- **VPS sehat**: uptime **5 minggu 4 jam** (sejak 17 Okt 2026, **tanpa reboot**), disk **72% (14 GB bebas / 50 GB)**, RAM **3,3/7,4 GiB used (4,2 GiB available)**, kernel `6.8.0-101-generic`.
- **9 layanan user + 4 layanan system + OMB + DSH** semuanya **active** (daftar §2). Tailscale `100.77.18.39` online.
- **YouTube OAuth mandiri LIVE & sehat**: `ytoauth` active, `/health` = `ok`, 8 routine Kitab Surgawi pakai helper OAuth lokal (project `kitabsurgawi-yt`, In Production).
- **OMB v0.1.130 sehat**: 14 routine di `routines.json`, zbmaus `/` = 200. Update ke v0.1.173 **ditunda** (keputusan 20 Nov).
- **Niudrive**: UI graphite/lime + Sonner/Vaul/cmdk/motion live, PR #3 merged `9d2630db32`; backup harian 21 Nov 01:30 → **1 upload, 0 gagal, 1135 dilewati, 1 file 0-byte**.
- **DSH pindah server**: `dsh.niumination.id` aktif (401 tanpa token = token-gate benar) di **VPS baru yang terpisah**; VPS ini tetap jalankan DSH lama `dsh.abstract.biz.id` (401, tidak diubah). Repo privat `dsh-abstract-biz-id` = sumber restore (127/127 chunk MATCH).
- **Vault kredensial** terenkripsi GPG di repo privat `zbmaus-vela-secrets/vault/`; index metadata di `ecosystem-config`.
- **Voice gateway `watch-fit-ai` ↔ OMB LIVE (24–25 Nov)**: `https://voice.abstract.biz.id` health 200, selftest 5/5, 3 device, TTS piper Indonesia, jawaban AI sungguhan dari bot ZB via webhook (§8f).
- **Kaggle uncensored v9 — LIVE 64K (25 Nov)**: notebook diaudit & diperbaiki (8 fix + keep-alive background thread), di-`push --no-run` dengan `CONTEXT = "64k"`, **Run All manual sukses**. `/health` = **200 `max_context: 65536`, `loaded:true, api_key:true`**; `/v1/models` = 401 (auth gate). Model Gyro-S abliterated 58 GB jalan di 2× T4. Dipakai dari Hermes Mac via 9Router `ninerouter`, model `strata/qwen3.8-flash-next-gyro-gyro-s`. Sinkronisasi selesai: VPS config (2 entri) **65536**, 9Router connection `providerSpecificData.contextLength` **65536**, dan **key Strata dirotasi ke sesi baru** (test 9Router `valid:true`, chat completion nyata HTTP 200 jawaban "Merah"). ⚠️ Sesi tidak kekal; key berubah tiap Run All → HARUS update key di 9Router + `/home/agentuser/zb/strata-api-key.txt` (mode 600) tiap sesi baru. Akar error input panjang sebelumnya = wildcard 9router `*qwen*` → 262144, Hermes baca via `custom_providers` (localhost vs 127.0.0.1). Mac masih perlu sinkron pin 65536 + `/new`.
- ✅ **Storage (Tier 1 selesai 25 Nov)**: disk 96% (2,2 GB) → **81% (9,4 GB bebas)** setelah hapus part backup gagal, journal vacuum, docker/apt/npm cache; layanan sehat (§8f).
- ⚠️ **Keputusan user 15 Nov**: apt upgrade & reboot **ditunda tanpa batas** (server belum pernah reboot) — 197 paket security backlog sengaja tidak dieksekusi.
- ⚠️ Insiden lama (dikonfes, 11 Nov): 16 file root folder `9drive` akun archk4li hilang permanen karena purge tanpa audit. Kredensial inti masih di `~/zb/`.

## 2. Layanan Berjalan (terverifikasi 21 Nov 2026 — semua active)

### User services (semua enabled, survive reboot)
| Service | Port | Fungsi | Status |
|---|---|---|---|
| `ombnew.service` | 8799 UI/API, 8800 webhook | OpenMausBot **v0.1.130** — engine openaiCompat → 9Router | ✅ active |
| `omb-relay-bridge.service` | 8801 | Bridge chat zbmaus-humanoid ↔ OMB | ✅ active |
| `novnc-gate.service` | 6081 | Token-gate proxy noVNC (6080) | ✅ active |
| `9router.service` | 20128 | 9Router AI gateway (22 model; Hermes & OMB) | ✅ active |
| `niudrive-backend.service` | 4000 | 9Drive API (Express+Prisma, MariaDB `9drive`) | ✅ active, health 200 |
| `niudrive-frontend.service` | 5173 | 9Drive UI (Vite preview, PWA) | ✅ active, 200 |
| `hermes-gateway.service` | — | Hermes Agent Gateway (Telegram, dst.) — Hermes v0.21.5 | ✅ active |
| `hermes-agent-os-dashboard.service` | 8765 | Mission Control (read-only) | ✅ active |
| `zb-humanoid.service` | 3001 | zb-humanoid API + static site | ✅ active |

### System services
| Service | Fungsi | Status / Catatan |
|---|---|---|
| `cloudflared.service` | Cloudflare Tunnel connector | ✅ active, **`--protocol http2`** (fix upload besar via tunnel) |
| `deepseek-harness.service` | DSH WebUI :3080 (VPS lama) | ✅ active, `--trusted-host dsh.abstract.biz.id`; token via journalctl |
| `tailscaled.service` | Tailscale | ✅ active, funnel Mission Control ditutup (tailnet only) |
| `ytoauth.service` | 8099 (loopback) | ✅ active, callback OAuth YouTube via `yt.abstract.biz.id` |

> DSH di `dsh.niumination.id` berjalan di **VPS baru terpisah**, bukan di host ini — tidak tercakup dalam tabel service lokal.

## 3. Peta Domain (Cloudflare Tunnel `zb-vela`)

Satu connector `cloudflared` (remote-managed, token `/etc/cloudflared/token`, **protocol http2**).

| Hostname | Origin | Status (21 Nov) |
|---|---|---|
| pipatung.abstract.biz.id | 127.0.0.1:3100 | ⚠️ 502 — app belum jalan (kode `~/zb/pi-patung` v0.1.0, start manual saat dipakai) |
| zbmaus.abstract.biz.id | 127.0.0.1:8799 | ✅ 200 (pairing device) |
| zb-humanoid.abstract.biz.id | 0.0.0.0:3001 | ✅ 200 (publik) |
| ombrelay.abstract.biz.id | 127.0.0.1:8801 | ✅ root 404 = normal; `/health` ok |
| dsh.abstract.biz.id | 127.0.0.1:3080 | ✅ 401 tanpa token = benar (VPS lama, tidak diubah) |
| dsh.niumination.id | **VPS baru terpisah** | ✅ 401 tanpa token = token-gate aktif (diverifikasi 21 Nov) |
| opencraft.abstract.biz.id | 127.0.0.1:6081 | ✅ 401 tanpa key = benar |
| **niudrive.abstract.biz.id** | 127.0.0.1:5173 | ✅ 200 — UI baru live |
| **api.abstract.biz.id** | 127.0.0.1:4000 | ✅ root 404 = normal; `/health` 200 |
| **yt.abstract.biz.id** | 127.0.0.1:8099 | ✅ root 404 = normal; `/health` 200, `/auth` 302 ke Google |

⚠️ **`yt.maus.abstract.biz.id` tidak bisa dipakai**: sertifikat wildcard Cloudflare hanya menjangkau satu level (`*.abstract.biz.id`), sehingga subdomain dua level gagal TLS handshake. Redirect URI terdaftar di Google: `https://yt.abstract.biz.id/oauth2callback` (persis, tanpa trailing slash).
| Mission Control | Tailscale funnel | ✅ https://zb-vela.tailec8707.ts.net (tailnet only) |

Ingress dikelola via Composio (`CLOUDFLARE_UPDATE_TUNNEL_CONFIGURATION`, replace-style — selalu kirim daftar lengkap). DNS record via `composio proxy` toolkit cloudflare (zone `762ed25a87cead530391792341d414ad`).

### YouTube OAuth Mandiri (19 Nov 2026, sehat 21 Nov)
- **Tujuan**: lepas dari infra Composio (token YouTube lama ter-revoke 18 Nov → 403) dan menghitung pemakaian ke kuota project Google Cloud sendiri (`kitabsurgawi-yt`, 10.000 unit/hari, reset 15.00 WIB). Redirect URI **tidak** menentukan kuota — kuota melekat pada Client ID.
- **Endpoint**: `https://yt.abstract.biz.id` → tunnel → `127.0.0.1:8099`. Service `ytoauth.service` (systemd system, user `ytoauth`, `/opt/yt-oauth` mode 700, `token.json` mode 600). `/health` → `ok` (diverifikasi 21 Nov); `/auth` → 302 ke Google; `/oauth2callback` menukar kode → token.
- **Scope WAJIB**: `https://www.googleapis.com/auth/youtube` **+** `https://www.googleapis.com/auth/youtube.force-ssl`. Tanpa `force-ssl`, endpoint komentar (`commentThreads`/`comments`) ditolak **403 insufficientPermissions** (diperbaiki 19 Nov).
- Consent screen sudah **In Production** → refresh token tidak kedaluwarsa 7 hari (tidak perlu re-auth mingguan).
- Channel terverifikasi: **Kitab Surgawi**, `UCs-1tjk6U6vMqqChpaR4j8w`.
- Helper di `/opt/yt-oauth/` — semua dipanggil `sudo -n` (sudoers `/etc/sudoers.d/yt-oauth-token`); token tidak pernah muncul di argv/log/chat:
  - `yt-api.py ENDPOINT param=val ...` — panggilan API v3 bebas (GET)
  - `yt-manage.py [--videos|--comments|--playlists]` — satu JSON berisi channel/video/playlist/komentar
  - `yt-reply.py COMMENT_ID "teks"` — balas komentar (50 unit)
  - `yt-moderate.py COMMENT_ID heldForReview|rejected|published` (50 unit)
  - `yt-playlist-add.py PLAYLIST_ID VIDEO_ID` (skip duplikat), `yt-playlist-create.py "Judul"`
  - `yt-upload.py FILE.mp4 "Judul" "Deskripsi" [tag,...] [--private]` — resumable upload langsung dari file lokal (~1600 unit)
  - `yt-thumbnail.py VIDEO_ID thumb.jpg`, `get_access_token.py` (auto-refresh)
- **8 routine Kitab Surgawi dialihkan** dari tool `YOUTUBE_*` Composio → helper lokal: Balasan Komentar, Laporan Performa Mingguan, Short ke playlist, Upload EP-003, Produksi Dokumenter, Monitoring Harian, Evaluasi Kualitas, Cross-post FB/IG. Panduan bot: `~/.openmausbot-ombnew/workspaces/3bbb857a-0cdc-4849-898b-a135cf3bf78c/memory/yt-oauth-helpers.md`.
- ⚠️ **OMB write-back**: `PATCH /api/routines/:id` atau restart saat OMB hidup dapat menimpa `routines.json` dengan state lama. Urutan aman: **stop ombnew → tulis file → start ombnew**. Backup: `~/.openmausbot-ombnew/routines.json.bak-yt-oauth-20261119-1530`.
- Job Hermes `d4165674ae2a` = **on-demand** (script-only `~/.hermes/scripts/yt-oauth-healthcheck.sh`, jadwal formal 1 Januari tiap tahun agar tidak jalan rutin; dipicu manual via `cronjob_manage action=run job_id=d4165674ae2a`). `no_agent=true` — kebal terhadap ketersediaan model LLM. Pemeriksaan read-only: service, health, token, scope, channel, commentThreads.

## 4. Niudrive (9Drive) — Kondisi Terkini

### Arsitektur
- Backend: Express + TypeScript + Prisma, MariaDB `9drive` — 17 migrasi up-to-date.
- Frontend: Vite 8 + React 19 + Tailwind 4, PWA (autoUpdate), Vite preview :5173.
- Repo: `github.com/Niumination/niudrive` (main). Merge PR #1 (redesign UI arena.ai) = `3da9d2b`; UI graphite/lime + Sonner/Vaul/cmdk/motion di-push 16 Nov (11 file blob-hash verified); **PR #3 merged `9d2630db32`** (18–19 Nov) — model pohon fisik per-akun `FolderDriveMapping`, tanpa share lintas-akun; menggantikan PR #2 yang direvert.

### UI/UX (12 Nov)
- **Bahasa Indonesia penuh** di seluruh UI (27 file; istilah teknis tetap: Google Drive, OAuth, API, MIME, MB/GB).
- **Ikon brand baru**: glyph "9" seimbang + gradient lime di graphite (`favicon`, `pwa-192/512`, `maskable`, `BrandLogo.tsx`).
- **Ikon folder duotone inline** (`FolderGlyph` di `FolderVisual.tsx`) — menggantikan fetch remote `api.iconify.design` (yang 403 dari VPS). 42 pilihan ikon; URL iconify lama di DB otomatis dimapping (`normalizeFolderIconKey`).
- Tema graphite + lime, dark/light, PWA installable. Warna folder di DB lama `#3b82f6` (2.253 folder) sudah diubah ke `#84cc16` (19 Nov); `FolderVisual.tsx` juga memetakan hex legacy biru/slate → lime.

### Upload & performa
- **Batch upload**: file kecil (<5 MB) dikumpulkan ≤25 file/request, total ≤8 MB/request; file ≥5 MB single request. UI upload juga batch (`UploadContext.tsx`, ≤20 MB/≤25 file).
- Backend cache per-request (auth, folder ID, routing) — ±8 panggilan/batch (dulu ±150).
- **cloudflared `--protocol http2`** — TANPA ini, upload >1–2 MB via tunnel hang/502 (isu QUIC). Terbukti: 19 MB → 201 dalam 6 detik.
- Benchmark 40 file kecil: 7,2 s (0,18 s/file, 16× lebih cepat dari sequential).
- Audit log `UPLOAD_FILE` tercatat untuk semua jalur upload.

### Data (18 Nov, dari DB)
- **2.307 folder, 10.345 file, 8 akun Drive connected** (18 Nov; 15 Nov: 1.975 file/760 folder). Tabel `folder_drive_mappings` (0 rows normal — lazy, dibuat saat upload). Migrasi `20261118120000_folder_drive_mappings` applied; backup pre-deploy `/tmp/9drive-full-predeploy-2223.sql.gz`.
- Routing policy: mode priority → **zhallbay28@gmail.com #1**. Folder baru otomatis di-pin ke akun hasil routing (fisik + pencatatan kuota konsisten — patch folder.routes.ts, revert commit opencode `776b3a3`).
- `archk4li@gmail.com` dikosongkan (folder `9drive` dihapus permanen).
- Backup Mac (15 Nov): **mac/** ter-mirror lengkap — 336+ file di 200 folder: `Downloads` (511 file, 860 MB), `Documents`, `projects`, `.config`, `backup-niudrive`, `nvim`, `zsh`, `tmux`, `git`, `bin` — plus `vault` (37 file) & `Pemdi-Vault` (85 file, 40 MB) via folder sumber. Upload terverifikasi 452 file/0 gagal (15 Nov). Script: `~/backup-niudrive/backup-device.mjs` (sinkron repo ≥`3974265`; cek `failed[]`, FormData per retry, `NINEDRIVE_EXCLUDE` tersedia).
- **Kebijakan user**: tidak ada exclude — kredensial/rahasia memang sengaja dibackup ke niudrive. Pencegahan (rotate/purge) hanya jika ada potensi bocor publik.
- **Password akun backup-agent dirotasi 12 Nov** (172 session lama invalid). `.env` Mac & VPS (`~/niudrive/backup/.env`) sudah keduanya memakai password baru (terverifikasi login 200 + backup sukses). File `~/zb/niudrive-backup-agent-NEWPASS.txt` tinggal menunggu konfirmasi akhir untuk dihapus.

### Pelajaran penting (agar tidak terulang)
1. **composio proxy GitHub memotong respons >20 KB senyap** — sinkron file repo↔lokal WAJIB: shell redirect ke file lalu verifikasi git-blob-hash per file. (PR #1 dulu gagal sync 33/68 file tanpa terdeteksi.)
2. DELETE niudrive = soft-delete (file fisik tetap di Drive). Purge permanen via helper `backend/scripts/delete-drive-files.mjs`.
3. Retry upload tanpa verifikasi membuat duplikat fisik di Drive (pernah 9 salinan/file saat 502).
4. Audit isi folder SEBELUM purge — insiden 16 file hilang permanen (11 Nov).

## 5. Aplikasi Web Lain

### zbmaus-humanoid (Vercel)
- https://zbmaus-humanoid.vercel.app ✅ — chat live site ↔ OMB sinkron (±8 dtk).
- Repo `github.com/Niumination/zbmaus-humanoid`. Rantai: browser → `/api/chat` (Vercel) → `ombrelay.abstract.biz.id/hooks/wh_knBDiZz4DGRydSZi` → bridge :8801 → OMB :8800 (bot `ZbmausHumanoid-Vercel`).
- Bearer webhook: `~/zb/zbmaus-humanoid-webhook-secret.txt`.

### OMB (OpenMausBot)
- v0.1.130 (diverifikasi 21 Nov di `~/.local/node-v24.11.1-linux-x64/lib/node_modules/openmausbot`), engine openaiCompat → 9Router :20128, browser=false, bot `MausBot` (agnes/agnes-2.5-flash), `--no-pair`.
- `routines.json`: **14 routine** (21 Nov); 8 di antaranya routine Kitab Surgawi pakai helper OAuth lokal. Update ke v0.1.173 ditunda (§8c).
- Antigravity engine masih `authenticated=false` (OAuth :53727 pending).

### AgenticTrade (PAUSE bersih)
- Repo publik `github.com/Niumination/AgenticTrade` (EA MT5 XAUUSD, transparansi penuh, angka backtest = NOT VERIFIED).
- Sprint 1–6 selesai; kriteria STOP terpicu pada WFO v0.3 → iterasi rule-based dihentikan → **Fase 2 forward test (demo IC Markets 53134764) menunggu keputusan runtime**. Tick data 2020–2025 dihapus dari disk (re-downloadable via `fetch_years.sh`).

### OneDrive (composio) — 12 Nov
- Toolkit `one_drive` tersambung (akun `afriearrafi@gmail.com`, personal, 5 GB total / 4,1 GB sisa).
- **Diperuntukkan khusus pekerjaan ASN** — tanpa backup pribadi/ekosistem; jangan akses tanpa perintah user.

## 6. Backup

| Timer | Jadwal | Terakhir (diverifikasi 21 Nov) | Isi |
|---|---|---|---|
| `niudrive-backup.timer` | harian 01:30 | **21 Nov 01:30: 1 upload, 0 gagal, 1135 dilewati, 1 file 0-byte** | `~/zb` → niudrive API → Drive |
| `zb-backup.timer` | Senin 00:10 (next 23 Nov) | 16 Nov | backup kecil mingguan → Google Drive via Composio |
| `zb-backup-full.timer` | Minggu 02:30 (next 22 Nov) | 15 Nov GAGAL → **fix akar 16 Nov** (`shutil.copytree` race, `arch=None`) | full split `--secret`, keep-3, auto-cleanup Drive |

**Insiden & perbaikan backup (15–16 Nov):**
1. `niudrive-backup.service` gagal 401 — `.env` VPS masih password lama pasca-rotasi 12 Nov. FIXED: password baru dipasang `~/niudrive/backup/.env`, login 200, run manual sukses. **Pelajaran: rotasi password wajib update SEMUA .env konsumen (Mac *dan* VPS) di sesi yang sama.**
2. `zb-backup-full.service` crash `UnboundLocalError: arch` (cleanup berjalan sebelum arsip dibuat saat error awal). FIXED: `arch=None` + `tmpdir` di-init sebelum `try` (backup-full-zb.py). Verifikasi runtime: timer Minggu 22 Nov 02:30.

Disk: **72% terpakai (14 GB bebas dari 50 GB)** — dibersihkan 11 Nov (tick data AgenticTrade 9,8 GB + cache ±1,6 GB).

## 7. Akses & Kredensial (lokasi file, JANGAN isi di chat)

| Item | Lokasi |
|---|---|
| Bearer webhook OMB | `~/zb/zbmaus-humanoid-webhook-secret.txt` |
| Gate key noVNC | `~/zb/omb-new/novnc-gate.key` (juga di `novnc-gate.env`) |
| URL akses opencraft | `~/zb/opencraft-access-url.txt` |
| Token login DSH (VPS lama) | `sudo journalctl -u deepseek-harness \| grep 'dsh web:'` (berubah tiap restart) |
| Sandi VNC | terenkripsi di `~/.vnc/passwd` |
| Password baru backup-agent niudrive | `~/zb/niudrive-backup-agent-NEWPASS.txt` (chmod 600 — hapus setelah konfirmasi akhir) |
| Kredensial VPS (kaggle.json, strata, dll.) | `~/zb/` (re-upload ke niudrive bila diminta) |
| Vault terenkripsi GPG | repo privat `zbmaus-vela-secrets/vault/`; kunci privat + passphrase di `~/.gnupg/` (mode 700/600) |

**Login flow:** DSH `?token=<token>` sekali → cookie 30 hari; OpenCraft `/vnc.html?key=<key>` → cookie 7 hari + sandi VNC.

## 8. Keamanan

- **Cloudflare Bot Fight Mode: OFF** (wajib — BFM men-challenge fetch server-to-server dari Vercel, mematikan chat live site).
- Proteksi per hostname: zbmaus (pairing), dsh (token), opencraft (gate key + sandi), ombrelay (bearer), niudrive (JWT + argon2, PWA), zb-humanoid (publik by design).
- Rotasi password backup-agent niudrive 12 Nov + 172 session lama invalid; `.env` VPS & Mac disinkronkan 15 Nov.
- **Tailworm (Okt 2026) ditangani 13 Nov**: Tailscale SSH server OFF, client 1.104.5 → **1.104.7**, Tailscale Funnel publik ditutup (Mission Control hanya via tailnet). Peers tidak ada yang menjalankan Tailscale SSH. Tailnet Lock belum aktif (opsional).
- **9Router di-upgrade 0.5.111 → 0.5.119** (14 Nov), katalog 22 model terverifikasi via `/v1/models`; konsumen: Hermes (`custom:ninerouter`) & OMB (`openaiCompat`).
- **197 paket security-update OS backlog** — **DITUNDA tanpa batas sesuai keputusan user 15 Nov** (server belum pernah reboot, risiko crash). 36 paket krusial sudah diidentifikasi, tapi TIDAK dieksekusi.
- Repos 13 Nov: `Niumination/zbmaus-vela` (publik, paket setup OMB+9Router) & `zbmaus-vela-secrets` (PRIVATE, env asli, bots.json + souls 7 bot, config.json, unit systemd produksi, credentials, state routines).
- File rahasia yang sempat bocor ke Drive sudah di-purge permanen (`niudrive-backup-agent.env`, duplikat GPG key). Audit 8 akun Drive: bersih dari kebocoran tak sengaja.
- Aturan git: `git push`/`fetch` CLI exit 128 → GitHub HANYA via composio contents API. Repo `ecosystem-config` tidak boleh disentuh tanpa izin eksplisit user. Dilarang push otomatis/aksi ke repo user tanpa approval.

## 8b. Vault & Backup Kredensial (20 Nov)
- **Vault terpusat PRIVAT**: `Niumination/zbmaus-vela-secrets/vault/` — `vault.tar.gpg` (GPG RSA-3072/AES256, 6 kredensial), `vault-public.key`, `manifest.json`, `README.md`. Blob GPG verified MATCH.
- **Keputusan**: `ecosystem-config` PUBLIK → tidak menyimpan kredensial. Index metadata saja: `docs/VAULT-BACKUP-INDEX.md` (sha `1e0a521f25e5`).
- Kunci privat + passphrase HANYA di VPS `~/.gnupg/` (mode 700/600), tidak pernah di-commit. Fingerprint penerima `614498AD5AF5776D61216910549F94537A2F3782`.
- Cakupan: yt-oauth.env, yt-token.json, cf-kaggle-token, kaggle-arb/tunnel, tunnel-kaggle. Staging plaintext di-shred setelah enkripsi.
- Aturan: jangan plaintext (walau repo privat); dekripsi → pakai → hapus; rotasi kunci → re-enkripsi → update manifest.

## 8c. Keputusan Update zbmaus — TUNDA (20 Nov, masih berlaku 21 Nov)
- **Versi terpasang**: `openmausbot@0.1.130` (diverifikasi 21 Nov; jalankan via `~/zb/omb-new/start.sh`, `--no-pair`).
- **Versi terbaru npm**: `0.1.173` (43 versi lebih baru, rilis terakhir 19 Nov).
- **Keputusan user**: TUNDA update. zbmaus sehat (health 200, 14 routine, 8 routine OAuth lokal jalan).
- **Alasan**: rilis v0.1.131–173 mayoritas fitur desktop/UI — TIDAK menyentuh API `:8799`, routines, OAuth, atau write-back `routines.json`. Lompatan 43 versi berisiko mengganggu konfigurasi stabil.
- **Catatan versi menengah**: v0.1.161 (automation gagal tidak auto-mati) agak relevan tapi tidak mendesak.
- **Prosedur bila nanti update**: backup `routines.json` + data dulu → update → verifikasi stop→write→start. Jangan update otomatis.

## 8d. Repo DSH mandiri (20 Nov, migrasi 21 Nov)
- **Repo PRIVAT mandiri**: `Niumination/dsh-abstract-biz-id` — setup + konfigurasi + backup lengkap `~/.dsh` (termasuk data sensitif, sesuai permintaan user untuk pindah server).
- Arsip `~/.dsh` (124 MB, 51 MB terkompresi) dienkripsi GPG RSA-3072 (fingerprint `614498AD...`), dipecah 27 chunk @2 MB → `backup/parts/part-00..26`.
- `workspace/parts/wschunk-00..wschunk-9009` (100 chunk) = arsip `~/Documents/deepseek-harness` (610 MB, workspace aktif DSH).
- Verifikasi: **27/27 + 100/100 chunk MATCH** via Git blob SHA-1; kedua arsip lolos dekripsi GPG + gzip test. Concat == arsip asli (SHA-256 workspace `90498bc9…`).
- chunk 90-99 bernama `wschunk-9000..9009` (`split -d` habis digit) — urutan gabung lexicographic tetap benar.
- Isi repo: `README.md`, `docs/SETUP.md`, `docs/PLUGINS.md`, `manifest.json`, `vault-public.key`, `systemd/deepseek-harness.service`, `profiles/web/cordis.patch.yml.example`, `backup/parts/`, `workspace/parts/`.
- Alasan chunk: composio proxy membatasi body PUT 4.718.592 byte.
- Cara restore: `cat backup/parts/part-* > dsh-full.tar.gz.gpg` (urut 00→26) → dekripsi GPG dengan private key + passphrase di `~/.gnupg/` → ekstrak ke `~/.dsh`.
- **Migrasi selesai (21 Nov)**: user konfirmasi "Dsh baru sudah aman di dsh.niumination.id" di **VPS baru yang terpisah**. Domain baru aktif (401 tanpa token = token-gate benar). Domain lama `dsh.abstract.biz.id` tetap dicatat & service di host ini tidak diubah. Repo tetap jadi sumber restore.

## 8e. Plugin DSH (Plaza/SkillHub) — catatan restore (20 Nov)
- Plugin TERSIMPAN di backup: `~/.dsh/profiles/web/node_modules` (~122 MB, masuk arsip 51 MB — dibuktikan perbandingan tar: dengan node_modules 53.680.450 vs backup 53.663.344; tanpa hanya 1.227.508).
- **Cara aktifasi**: BUKAN `cordis.yml` (sengaja `[]`), tapi `package.json` → `dsh.profile.bundles` + `cordis.patch.yml`. Plaza = `@cocofhu/skillhub` 0.2.16, sudah di bundles.
- **Kenapa plaza hilang di VPS baru**: `pnpm install` belum dijalankan setelah restore (8 symlink relatif di `.bin/` perlu re-resolve). Pnpm store `~/.local/share/pnpm` (~857 MB) TIDAK ikut → butuh network/GitHub.
- Dokumentasi: `dsh-abstract-biz-id/docs/PLUGINS.md` & `profiles/web/cordis.patch.yml.example` (blob MATCH). 12 plugin: skillhub, opencode-zen-free-provider, dingtalk/lark/qqbot/wecom/weixin, file-download, media-web-preview, our-free-model, vision-router, visual-option.

## 8f. Voice gateway ↔ OMB & Kaggle uncensored (24–25 Nov)

**Voice gateway `watch-fit-ai` terhubung ke OMB (24 Nov).** Repo `Niumination/watch-fit-ai` di `~/zb/voice-gateway`, HEAD `43cf487` (adapter OMB). Container `gateway-gateway-1`, `127.0.0.1:8091 → 8080`, domain `https://voice.abstract.biz.id`, health 200, selftest 5/5. Tiga device: `and-zbvela-4277`, `and-5ddb4c9f`, `and-78ed6a33`. Kredensial & `DEVICE_TOKENS` di `.env` mode 600 (GROQ_API_KEY, GATEWAY_SECRET, OMB webhook token — [REDACTED]). TTS piper lokal `id_ID-news.onnx` (62.950.044 byte).
- Adapter `default_agent` = `omb` (override `.env`, karena `agents.json` sempat ditimpa). Uji audio asli → **HTTP 200 + jawaban AI sungguhan dari bot ZB** (bukan fallback "Maaf, agent tidak menjawab"), WAV 95.896 byte.
- **Bridge OMB dua listener**: `~/zb/omb-new/relay-bridge.mjs` dipatch `BRIDGE_HOST` (default `127.0.0.1`) + `BRIDGE_EXTRA_HOST=172.18.0.1` (`relay-bridge.env`). Tidak pakai `0.0.0.0` (UFW inactive); situs humanoid tetap 200. Webhook sementara `wh_knBDiZz4DGRydSZi` (bot `ZbmausHumanoid-Vercel`) — jawaban bisa muncul juga di situs humanoid.
- Patch lokal voice gateway: `docker-compose.yml` port `127.0.0.1:8091` (upstream masih `expose: 8080`) — needs re-apply tiap pull sampai di-upstreamkan.

**Kaggle uncensored — AUDIT SELESAI & LIVE (25 Nov).** Kernel `ryuarch/strata-kaggle-launcher-uncensored` (Gyro-S abliterated 58 GB, tunnel `kaggle-arb` → `arbitrage-model.abstract.biz.id/v1`). **Hasil akhir: RUN ALL MANUAL SUKSES, kernel `COMPLETE`, model LIVE.** `/health` = `200 {"status":"ok","loaded":true,"api_key":true,"model":"qwen3.8-flash-next-gyro-gyro-s","max_context":32768,"service":"strata"}`; `/v1/models` tanpa key = 401 (auth gate benar); domain `kaggle-model` = 530 (tak dipakai). Dipakai dari **Hermes Mac via 9Router**: provider `ninerouter`, model `strata/qwen3.8-flash-next-gyro-gyro-s` (terdaftar di `~/.hermes/config.yaml` baris 343). ⚠️ Katalog 9Router belum punya entri `strata` → model mungkin perlu didaftarkan lewat dashboard 9Router (`/dashboard`) agar muncul di daftar; base_url dan model id sudah benar. Sesi TIDAK kekal — mati kapan saja bila kuota/idle, endpoint kembali 530.
- **8 bug yang ditemukan & diperbaiki** saat audit: (1) `KAGGLE_USERNAME` placeholder → `ryuarch` (penyebab ERROR lama, gagal detik ke-14); (2) `kaggle_env()` hanya baca Secrets → fallback `arb-creds`; (3) pra-validasi `PRA-UJI cache OK` sebelum unduh 58 GB; (4) `MONITOR_HOURS` 6 → 0 (lalu **dikembalikan ke 6 di v7** — lihat bawah); (5) `UPLOAD_CACHES=False`; (6) `NameError` `_g`/`_o` (di-import dalam `_fetch`, dipakai di luar) → import di scope sel; (7) **nama GGUF kanonik** — Strata cari `...-Gyro-S-TQ1_0.gguf` tanpa `-abliterated` → dibuat hardlink (nama baru, inode sama, tanpa duplikat 58 GB); (8) engine Strata 0.1.67 (593 MB) ter-install sekali, di-skipped run berikutnya. Notebook final: `~/zb/kaggle-audit/strata-kaggle-launcher-uncensored.FIXED.ipynb` + `CARA-PAKAI.md` + `fix_notebook.py` (mode 600). Push v6 via `kernels push --no-run` (quick save, aman tanpa GPU). Aturan: push = run = bakar kuota; watchdog dilarang tanpa approval; 1 tunnel = 1 konektor. Cache GGUF 58.487.015.904 byte persis. Blob repo: import fix `884b7473`, kanonik fix `4cc03302`.
- **Versi 7 — keep-alive 6 jam (25 Nov, diminta user).** Setelah sesi mati otomatis & restart, disk session turun dari ~80 GB ke 2 GB karena `MODEL_RESTORE_MODE = "copy"` (copy lokal 58 GB hilang saat Kaggle reset sesi). Cell 19 diubah: `MONITOR_HOURS = 6`, health check `requests.get(.../health)` tiap 60 dtk + heartbeat print + cek auth publik (401/403), fallback `TUNNEL_URL`, jangan tutup tab/cancel. Push v7 via `kernels push --no-run` (aman); terverifikasi 21 sel, 0 syntax error, semua fix lama utuh. **Efek:** menjaga sesi tetap hidup 6 jam supaya copy tidak perlu diulang; setelah itu Kaggle yang menghentikan. Sesi masih tidak kekal — bila endpoint 530, Start manual + Run All (engine/cache hangat).
- **Versi 8 — keep-alive jadi BACKGROUND THREAD (25 Nov).** Versi 7 pakai `while ... sleep(60)` yang mem-blok kernel → console tidak bisa jalan (`strata launch --show-key` gagal). v8: cell 19 pakai `threading.Thread(daemon=True)`, kernel tetap bebas; cell 17 ditambah catatan ambil key via **Terminal Kaggle terpisah** (File → New → Terminal), bukan console notebook. Push v8 `--no-run`, verifikasi thread + fix lama utuh. Untuk sesi yang sudah jalan pakai v7: jangan pakai console, buka Terminal terpisah untuk `strata launch --show-key`.

**Versi 9 — CONTEXT 64K (25 Nov, diminta user).** Alasan: system prompt + tool schema Hermes ≈ 29.379 token dari 32.768 → headroom ~3,4k → sering compaction. Akar 262144 = wildcard statis 9router `*qwen*` (`8402.js`), bukan Strata/API key; Hermes baca via `custom_providers` (base_url `localhost` Mac vs `127.0.0.1` VPS TIDAK dinormalisasi → keduanya perlu entri). Cell 1: `CONTEXT = "32k"` → `"64k"` (hanya parameter context; path/nama model tidak berubah). Push v9 via `kernels push --no-run` (GPU tidak menyala), terverifikasi Kaggle live `CONTEXT = "64k"`, 21 sel, 0 syntax error, leak audit 0; blob repo `2eb4a5d4…` MATCH; README + `CARA-PAKAI.md` ter-update. **RUN ALL MANUAL SUKSES** — `/health` 200 `max_context: 65536`, `loaded:true`, auth 401. Sinkronisasi klien: VPS config dua entri (baris 345 `providers.ninerouter` + 480 `custom_providers`) **32768 → 65536** via backup `config.yaml.bak-64k-20261125-150544` + exact-string replace + diff (2 baris saja berubah); resolver terverifikasi `127.0.0.1 → 65536`, `localhost → 65536`, model lain `None`. 9Router connection `e32b7d7d…` `providerSpecificData.contextLength → 65536` (backup `9router-connection-strata-backup-65536.json`). **Key Strata berubah tiap Run All** — key lama menghasilkan 401 `missing or wrong API key` (test server `valid:false`); user kirim key baru, dipasang via PUT `apiKey`, test `valid:true`, chat completion nyata lewat 9Router HTTP 200 jawaban "Merah". Key disimpan mode 600 di `~/zb/strata-api-key.txt`. Mac masih perlu sinkron pin 65536 + `/new`. 64k menambah KV cache di 2× T4 (16 GB) — lebih berat dari 32k tapi masih masuk; 128k tidak disarankan. Metode sunting config: backup + exact-string replace + diff, BUKAN `hermes config set` (lossy); sesi jalan perlu `/new` agar config dibaca ulang.

**Storage (Tier 1 dieksekusi 25 Nov).** Sebelum: 45/50 GB (96%, sisa 2,2 GB). Sesudah: **38/50 GB (81%, sisa 9,4 GB)** — dihapus 11 part backup gagal (`zb-backup-full-20261122-*`, 3,7 GB), journal vacuum 466 MB, `docker builder prune` 2,6 GB, apt cache 12 `.deb`, npm cache 532 MB; `/tmp` 4,0 GB → 310 MB. Tier 2 (~1 GB: ms-playwright, browser-vnc-offline, pip cache) belum dijalankan. Layanan (gateway, OMB, 9Router) tetap sehat.

## 9. Known Issues / Pending

1. **PiPatung belum jalan** (:3100 → 502). Kode `~/zb/pi-patung` v0.1.0 — start manual saat dibutuhkan.
2. Antigravity OMB `authenticated=false` (OAuth :53727 pending sign-in).
3. **File password backup-agent masih di VPS** (`~/zb/niudrive-backup-agent-NEWPASS.txt`) — .env Mac & VPS sudah update; hapus setelah konfirmasi akhir user.
4. ~~Routine YouTubeGrowth gagal berulang (14–15 Nov)~~ — **SELESAI 19 Nov**: token Composio ter-revoke; 8 routine pakai OAuth mandiri, uji nyata sukses.
5. **apt security backlog 197 paket** — ditunda tanpa batas (keputusan user 15 Nov).
6. Hermes Agent OS: wiki + offsite backup deployment menunggu keputusan user.
7. Composio koneksi `cloudflare` tanpa scope DNS/zone untuk beberapa tool (`LIST_ZONES` 403) — `composio proxy` ke REST CF langsung berfungsi.
8. noVNC `/websockify` via HTTP/2 bisa 404 — browser nyata selalu HTTP/1.1 untuk WS, aman.
9. **Plugin Plaza di VPS DSH baru** — perlu `pnpm install` di `~/.dsh/profiles/web` bila belum muncul (§8e).

## 10. Perintah Operasi Cepat

```bash
# Status layanan inti (semua active per 21 Nov)
systemctl --user is-active ombnew omb-relay-bridge novnc-gate 9router niudrive-backend niudrive-frontend hermes-gateway zb-humanoid

# Restart niudrive
systemctl --user restart niudrive-backend niudrive-frontend

# Lihat token DSH terbaru (VPS lama)
sudo journalctl -u deepseek-harness | grep 'dsh web:'

# Tes upload besar via tunnel (harus 201; kalau 502/hang cek cloudflared protocol http2)
curl -s -o /dev/null -w "%{http_code}" -X POST https://api.abstract.biz.id/uploads \
  -H "Authorization: Bearer ***" -F sizeBytes=5000000 -F fileName=test.bin -F file=@/path/5mb.bin

# Tes chat live site
curl -X POST https://zbmaus-humanoid.vercel.app/api/chat -H 'content-type: application/json' -d '{"message":"tes"}'

# Edit route tunnel (replace-style: kirim daftar lengkap!)
composio execute CLOUDFLARE_UPDATE_TUNNEL_CONFIGURATION --data '{...full ingress list...}'

# YouTube OAuth mandiri (JANGAN pernah cetak token/secret)
sudo -n systemctl is-active ytoauth
curl -s https://yt.abstract.biz.id/health                  # ok
sudo -n /opt/yt-oauth/yt-api.py channels part=snippet mine=true
sudo -n /opt/yt-oauth/yt-manage.py --comments > /tmp/yt.json
# re-otorisasi HANYA bila token/scope bermasalah: buka https://yt.abstract.biz.id/auth
# cron on-demand (tidak rutin): cronjob_manage action=run job_id=d4165674ae2a

# Push file ke repo via composio (redirect + verifikasi hash WAJIB)
composio proxy "https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=main" -t github --skip-connection-check > /tmp/f.json
composio proxy "https://api.github.com/repos/OWNER/REPO/contents/PATH" -t github --skip-connection-check -X PUT --data @/tmp/put.json
```
