# ZB-Vela — Status Ekosistem

> Tanggal: **19 November 2026** (OAuth YouTube mandiri + sinkronisasi ekosistem) • VPS: VM-11-184-ubuntu (Tailscale: zb-vela, 100.77.18.39)
> Semua status diverifikasi langsung (systemctl / curl / DB query / API) pada tanggal di atas.
> Dokumen ini menggantikan versi 15 November 2026.

---

## 1. Ringkasan Kondisi (19 Nov 2026)

- **VPS sehat**: uptime 4 minggu 5 hari (sejak 17 Okt 2026, tanpa reboot), disk 71% (14 GB bebas dari 50 GB), RAM 4,1/7,4 GiB terpakai (3,3 GiB available).
- **9 layanan user + 5 layanan system + 1 layanan OAuth** berjalan normal (daftar di §2).
- **YouTube OAuth mandiri LIVE (19 Nov)**: Kitab Surgawi lepas dari Composio (token lama ter-revoke 18 Nov, 403). 8 routine OMB dialihkan ke helper OAuth lokal; project `kitabsurgawi-yt` sudah **In Production**.
- **Niudrive sinkron**: UI graphite/lime + Sonner/Vaul/cmdk/motion di-push (11 file blob-hash verified), PR #3 merged `9d2630db32` (pohon fisik per-akun `FolderDriveMapping`).
- ⚠️ **Keputusan user 15 Nov**: apt upgrade & reboot **ditunda tanpa batas** (server belum pernah reboot) — 197 paket security backlog sengaja tidak dieksekusi.
- **Niudrive upgrade besar** (11–12 Nov): UI baru penuh Bahasa Indonesia, ikon custom duotone, batch upload cepat, routing akun Drive diperbaiki, cloudflared pindah ke `--protocol http2` (fix upload >1 MB gagal/502).
- **Kebersihan data**: akun Drive `archk4li@gmail.com` dikosongkan (dokumen pribadi pindah ke `zhallbay28`); routing prioritas → `zhallbay28@gmail.com`.
- ⚠️ **Insiden data (dikonfes)**: 16 file root folder `9drive` akun archk4li hilang permanen karena purge tanpa audit (11 Nov). Kredensial inti masih ada di VPS `~/zb/`; dokumen pribadi diasumsikan masih di Mac.

## 2. Layanan Berjalan (terverifikasi 12 Nov)

### User services (semua enabled, survive reboot)
| Service | Port | Fungsi | Status |
|---|---|---|---|
| `ombnew.service` | 8799 UI/API, 8800 webhook | OpenMausBot v0.1.130 — engine openaiCompat → 9Router | ✅ |
| `omb-relay-bridge.service` | 8801 | Bridge chat zbmaus-humanoid ↔ OMB (kode `~/zb/omb-new/relay-bridge.mjs`) | ✅ |
| `novnc-gate.service` | 6081 | Token-gate proxy noVNC (6080) | ✅ |
| `9router.service` | 20128 | 9Router AI gateway (22 model; Hermes & OMB) | ✅ |
| `niudrive-backend.service` | 4000 | 9Drive API (Express+Prisma, MariaDB `9drive`) | ✅ health OK |
| `niudrive-frontend.service` | 5173 | 9Drive UI (Vite preview, PWA) | ✅ 200 |
| `hermes-gateway.service` | — | Hermes Agent Gateway (Telegram, dst.) | ✅ |
| `hermes-agent-os-dashboard.service` | 8765 | Mission Control (read-only) | ✅ |
| `zb-humanoid.service` | 3001 | zb-humanoid API + static site | ✅ |

### System services
| Service | Fungsi | Catatan |
|---|---|---|
| `cloudflared.service` | Cloudflare Tunnel connector | **kini `--protocol http2`** (systemd drop-in `/etc/systemd/system/cloudflared.service.d/override.conf`) — fix upload besar gagal via tunnel |
| `deepseek-harness.service` | DSH WebUI :3080 | dengan `--trusted-host dsh.abstract.biz.id`; token login via journalctl |
| `vela-x11vnc.service` / `vela-novnc.service` | VNC :5900 / :6080 | sandi di `~/.vnc/passwd` |
| `tailscaled.service` | Tailscale | funnel Mission Control aktif |
| `ytoauth.service` | 8099 (loopback) | Callback OAuth YouTube mandiri via `yt.abstract.biz.id` | ✅ health ok |

## 3. Peta Domain (Cloudflare Tunnel `zb-vela`)

Satu connector `cloudflared` (remote-managed, token `/etc/cloudflared/token`, **protocol http2**).

| Hostname | Origin | Status (12 Nov) |
|---|---|---|
| pipatung.abstract.biz.id | 127.0.0.1:3100 | ⚠️ 502 — app belum jalan (kode `~/zb/pi-patung` v0.1.0, start manual saat dipakai) |
| zbmaus.abstract.biz.id | 127.0.0.1:8799 | ✅ 200 (pairing device) |
| zb-humanoid.abstract.biz.id | 0.0.0.0:3001 | ✅ 200 (publik) |
| ombrelay.abstract.biz.id | 127.0.0.1:8801 | ✅ (root 404 = normal; `/health` ok) |
| dsh.abstract.biz.id | 127.0.0.1:3080 | ✅ 401 tanpa token = benar |
| opencraft.abstract.biz.id | 127.0.0.1:6081 | ✅ 401 tanpa key = benar |
| **niudrive.abstract.biz.id** | 127.0.0.1:5173 | ✅ 200 — UI baru live |
| **api.abstract.biz.id** | 127.0.0.1:4000 | ✅ `/health` ok |
| **yt.abstract.biz.id** | 127.0.0.1:8099 | ✅ `/health` ok, `/auth` 302 ke Google (root 404 = normal) |

⚠️ **`yt.maus.abstract.biz.id` tidak bisa dipakai**: sertifikat wildcard Cloudflare hanya menjangkau satu level (`*.abstract.biz.id`), sehingga subdomain dua level gagal TLS handshake. Redirect URI yang terdaftar di Google: `https://yt.abstract.biz.id/oauth2callback` (persis, tanpa trailing slash).
| Mission Control | Tailscale funnel | ✅ https://zb-vela.tailec8707.ts.net |

Ingress dikelola via Composio (`CLOUDFLARE_UPDATE_TUNNEL_CONFIGURATION`, replace-style — selalu kirim daftar lengkap). DNS record via `composio proxy` toolkit cloudflare (zone `762ed25a87cead530391792341d414ad`).

### YouTube OAuth Mandiri (baru 19 Nov 2026)

- **Tujuan**: lepas dari infra Composio (token YouTube lama ter-revoke 18 Nov → 403 Forbidden) dan menghitung pemakaian ke kuota project Google Cloud sendiri (`kitabsurgawi-yt`, 10.000 unit/hari, reset 15.00 WIB). Redirect URI **tidak** menentukan kuota — kuota melekat pada Client ID.
- **Endpoint**: `https://yt.abstract.biz.id` → tunnel → `127.0.0.1:8099`. Service `ytoauth.service` (systemd system, user `ytoauth`, `/opt/yt-oauth` mode 700, `token.json` mode 600). `/health` → `ok`; `/auth` → 302 ke Google; `/oauth2callback` menukar kode → token.
- **Scope WAJIB**: `https://www.googleapis.com/auth/youtube` **+** `https://www.googleapis.com/auth/youtube.force-ssl`. Tanpa `force-ssl`, endpoint komentar (`commentThreads`/`comments`) ditolak **403 insufficientPermissions** (sudah diuji & diperbaiki 19 Nov).
- Consent screen sudah **In Production** → refresh token tidak lagi kedaluwarsa 7 hari (tidak perlu re-auth mingguan).
- Channel terverifikasi: **Kitab Surgawi**, `UCs-1tjk6U6vMqqChpaR4j8w`.
- Helper di `/opt/yt-oauth/` — semua dipanggil `sudo -n` (sudoers `/etc/sudoers.d/yt-oauth-token`); token tidak pernah muncul di argv/log/chat:
  - `yt-api.py ENDPOINT param=val ...` — panggilan API v3 bebas (GET)
  - `yt-manage.py [--videos|--comments|--playlists]` — satu JSON berisi channel/video/playlist/komentar
  - `yt-reply.py COMMENT_ID "teks"` — balas komentar (50 unit)
  - `yt-moderate.py COMMENT_ID heldForReview|rejected|published` (50 unit)
  - `yt-playlist-add.py PLAYLIST_ID VIDEO_ID` (skip duplikat), `yt-playlist-create.py "Judul"`
  - `yt-upload.py FILE.mp4 "Judul" "Deskripsi" [tag,...] [--private]` — resumable upload langsung dari file lokal (~1600 unit; diuji sampai 308 `Resume Incomplete` tanpa publish)
  - `yt-thumbnail.py VIDEO_ID thumb.jpg`, `get_access_token.py` (auto-refresh)
- **8 routine Kitab Surgawi sudah dialihkan** dari tool `YOUTUBE_*` Composio → helper lokal: Balasan Komentar, Laporan Performa Mingguan, Short ke playlist, Upload EP-003, Produksi Dokumenter, Monitoring Harian, Evaluasi Kualitas, Cross-post FB/IG. Panduan bot: `~/.openmausbot-ombnew/workspaces/3bbb857a-0cdc-4849-898b-a135cf3bf78c/memory/yt-oauth-helpers.md`.
- ⚠️ **OMB write-back**: `PATCH /api/routines/:id` atau restart saat OMB hidup dapat menimpa `routines.json` dengan state lama. Urutan aman: **stop ombnew → tulis file → start ombnew**. Backup: `~/.openmausbot-ombnew/routines.json.bak-yt-oauth-20261119-1530`.
- Job Hermes `0b257dad1a83` = **on-demand** (one-shot 2030-01-01, dipicu manual via `cronjob_manage action=run`), bukan jadwal rutin. Pemeriksaan read-only: service, health, token, scope, channel, commentThreads.

## 4. Niudrive (9Drive) — Kondisi Terkini

### Arsitektur
- Backend: Express + TypeScript + Prisma, MariaDB `9drive` — 17 migrasi up-to-date.
- Frontend: Vite 8 + React 19 + Tailwind 4, PWA (autoUpdate), Vite preview :5173.
- Repo: `github.com/Niumination/niudrive` (main). Merge PR #1 (redesign UI arena.ai) = `3da9d2b`; UI graphite/lime + Sonner/Vaul/cmdk/motion di-push 16 Nov (11 file, blob-hash verified); **PR #3 merged `9d2630db32`** (18–19 Nov) — model pohon fisik per-akun `FolderDriveMapping`, tanpa share lintas-akun; menggantikan PR #2 yang direvert.

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
- **Password akun backup-agent dirotasi 12 Nov** (172 session lama invalid). `.env` Mac & VPS (`~/niudrive/backup/.env`) sudah keduanya memakai password baru (terverifikasi login 200 + backup sukses 15 Nov). File `~/zb/niudrive-backup-agent-NEWPASS.txt` tinggal menunggu konfirmasi akhir untuk dihapus.

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
- v0.1.130, engine openaiCompat → 9Router :20128, browser=false, bot `MausBot` (agnes/agnes-2.5-flash).
- Antigravity engine masih `authenticated=false` (OAuth :53727 pending).

### AgenticTrade (PAUSE bersih)
- Repo publik `github.com/Niumination/AgenticTrade` (EA MT5 XAUUSD, transparansi penuh, angka backtest = NOT VERIFIED).
- Sprint 1–6 selesai; kriteria STOP terpicu pada WFO v0.3 → iterasi rule-based dihentikan → **Fase 2 forward test (demo IC Markets 53134764) menunggu keputusan runtime**. Tick data 2020–2025 dihapus dari disk (re-downloadable via `fetch_years.sh`).

### OneDrive (composio) — BARU 12 Nov
- Toolkit `one_drive` tersambung (akun `afriearrafi@gmail.com`, personal, 5 GB total / 4,1 GB sisa).
- **Diperuntukkan khusus pekerjaan ASN** — tanpa backup pribadi/ekosistem; jangan akses tanpa perintah user.

## 6. Backup

| Timer | Jadwal | Terakhir | Isi |
|---|---|---|---|
| `niudrive-backup.timer` | harian 01:30 | **19 Nov 01:30: 24 upload, 0 gagal, 1112 dilewati, 1 file 0-byte** | `~/zb` → niudrive API → Drive |
| `zb-backup.timer` | Senin 00:10 | 9 Nov | backup kecil harian → Google Drive via Composio |
| `zb-backup-full.timer` | Minggu 02:30 | 15 Nov GAGAL → **fix akar 16 Nov** (`shutil.copytree` race, `arch=None`); bukti nyata run Minggu 22 Nov 02:30 | full split `--secret`, keep-3, auto-cleanup Drive |

**Insiden & perbaikan backup (15 Nov):**
1. `niudrive-backup.service` gagal 401 — `.env` VPS masih password lama pasca-rotasi 12 Nov. FIXED: password baru dipasang `~/niudrive/backup/.env`, login 200, run manual success. **Pelajaran: rotasi password wajib update SEMUA .env konsumen (Mac *dan* VPS) di sesi yang sama.**
2. `zb-backup-full.service` crash `UnboundLocalError: arch` (cleanup line 174 berjalan sebelum arsip dibuat saat error awal). FIXED: `arch=None` + `tmpdir` di-init sebelum `try` (backup-full-zb.py). Verifikasi runtime: timer Minggu 22 Nov 02:30.

Disk: **60% terpakai (20 GB bebas)** — dibersihkan 11 Nov (tick data AgenticTrade 9,8 GB + cache ±1,6 GB).

## 7. Akses & Kredensial (lokasi file, JANGAN isi di chat)

| Item | Lokasi |
|---|---|
| Bearer webhook OMB | `~/zb/zbmaus-humanoid-webhook-secret.txt` |
| Gate key noVNC | `~/zb/omb-new/novnc-gate.key` (juga di `novnc-gate.env`) |
| URL akses opencraft | `~/zb/opencraft-access-url.txt` |
| Token login DSH | `sudo journalctl -u deepseek-harness \| grep 'dsh web:'` (berubah tiap restart) |
| Sandi VNC | terenkripsi di `~/.vnc/passwd` |
| Password baru backup-agent niudrive | `~/zb/niudrive-backup-agent-NEWPASS.txt` (chmod 600 — hapus setelah Mac update) |
| Kredensial VPS (kaggle.json, strata, dll.) | `~/zb/` (re-upload ke niudrive bila diminta) |

**Login flow:** DSH `?token=<token>` sekali → cookie 30 hari; OpenCraft `/vnc.html?key=<key>` → cookie 7 hari + sandi VNC.

## 8. Keamanan

- **Cloudflare Bot Fight Mode: OFF** (wajib — BFM men-challenge fetch server-to-server dari Vercel, mematikan chat live site).
- Proteksi per hostname: zbmaus (pairing), dsh (token), opencraft (gate key + sandi), ombrelay (bearer), niudrive (JWT + argon2, PWA), zb-humanoid (publik by design).
- Rotasi password backup-agent niudrive 12 Nov + 172 session lama invalid; `.env` VPS & Mac disinkronkan 15 Nov.
- **Tailworm (Okt 2026) ditangani 13 Nov**: Tailscale SSH server OFF (vektor utama worm), client di-upgrade 1.104.5 → **1.104.7**, Tailscale Funnel publik ditutup (Mission Control dashboard sempat terekspos internet tanpa auth — kini hanya via tailnet). Peers (aperture, lightvela, Mac, HP) tidak ada yang menjalankan Tailscale SSH. Tailnet Lock belum aktif (opsional).
- **9Router di-upgrade 0.5.111 → 0.5.119** (14 Nov), katalog model di-refresh; konsumen: Hermes (`custom:ninerouter`) & OMB (`openaiCompat`) — 22 model terverifikasi via `/v1/models`, inferensi uji OK.
- **197 paket security-update OS backlog** — **DITUNDA tanpa batas sesuai keputusan user 15 Nov** (server belum pernah reboot, risiko crash). 36 paket krusial sudah diidentifikasi (kernel/openssh/sudo/openssl/systemd/curl/rsync/tar/libc6/git/bind9/python3-*), tapi TIDAK dieksekusi.
- Repos baru 13 Nov: `Niumination/zbmaus-vela` (publik, paket setup OMB+9Router, 18 file + docs INSTALL-PROMPT.md) & `zbmaus-vela-secrets` (PRIVATE, 31 file: env asli, bots.json + souls 7 bot, config.json, unit systemd produksi, credentials, state routines).
- File rahasia yang sempat bocor ke Drive sudah di-purge permanen (`niudrive-backup-agent.env`, duplikat GPG key). Audit menyeluruh 8 akun Drive: bersih dari kebocoran tak sengaja.
- `git push` CLI exit 128 → GitHub HANYA via composio contents API. Repo `ecosystem-config` tidak boleh disentuh tanpa izin eksplisit user.
- Dilarang push otomatis/aksi ke repo milik user tanpa approval (pelajaran insiden opencode `776b3a3`).

## 9. Known Issues / Pending

1. **PiPatung belum jalan** (:3100 kosong → 502). Kode `~/zb/pi-patung` v0.1.0 — start manual saat dibutuhkan.
2. Antigravity OMB `authenticated=false` (OAuth :53727 pending sign-in).
3. **File password backup-agent masih di VPS** (`~/zb/niudrive-backup-agent-NEWPASS.txt`) — .env Mac & VPS sudah keduanya update; hapus file setelah konfirmasi akhir user. (Mac copy: hapus di sisi Mac juga.)
4. ~~Routine YouTubeGrowth OMB gagal berulang (14–15 Nov)~~ — **SELESAI 19 Nov**: akar = token Composio YouTube ter-revoke (403). Semua 8 routine YouTube sudah pakai OAuth mandiri; uji nyata bot memanggil `yt-manage.py --comments` via sudo sukses.
5. **apt security backlog 197 paket** — upgrade selektif krusial belum dijalankan (kernel/openssh/sudo/openssl/systemd/curl dll.).
6. Hermes Agent OS: wiki + offsite backup deployment menunggu keputusan user.
7. Composio koneksi `cloudflare` tanpa scope DNS/zone untuk beberapa tool (`LIST_ZONES` 403) — tapi `composio proxy` ke REST CF langsung berfungsi (DNS, bot_management, rulesets).
8. noVNC `/websockify` via HTTP/2 bisa 404 — browser nyata selalu HTTP/1.1 untuk WS, aman.

## 10. Perintah Operasi Cepat

```bash
# Status layanan inti
systemctl --user is-active ombnew omb-relay-bridge novnc-gate 9router niudrive-backend niudrive-frontend hermes-gateway zb-humanoid

# Restart niudrive
systemctl --user restart niudrive-backend niudrive-frontend

# Lihat token DSH terbaru
sudo journalctl -u deepseek-harness | grep 'dsh web:'

# Tes upload besar via tunnel (harus 201; kalau 502/hang cek cloudflared protocol http2)
curl -s -o /dev/null -w "%{http_code}" -X POST https://api.abstract.biz.id/uploads \
  -H "Authorization: Bearer <jwt>" -F sizeBytes=5000000 -F fileName=test.bin -F file=@/path/5mb.bin

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
# cron on-demand (tidak rutin): cronjob_manage action=run job_id=0b257dad1a83

# Push file ke repo via composio (redirect + verifikasi hash WAJIB)
composio proxy "https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=main" -t github --skip-connection-check > /tmp/f.json
composio proxy "https://api.github.com/repos/OWNER/REPO/contents/PATH" -t github --skip-connection-check -X PUT --data @/tmp/put.json
```
