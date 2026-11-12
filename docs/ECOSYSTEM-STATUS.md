# ZB-Vela — Status Ekosistem

> Tanggal: **12 November 2026** • VPS: VM-11-184-ubuntu (Tailscale: zb-vela, 100.77.18.39)
> Semua status diverifikasi langsung (systemctl / curl / DB query) pada tanggal di atas.
> Dokumen ini menggantikan versi 6 November 2026.

---

## 1. Ringkasan Kondisi (12 Nov 2026)

- **VPS sehat**: uptime sejak 17 Okt 2026, disk 60% (20 GB bebas dari 50 GB), RAM 4,9/7,4 GiB terpakai.
- **9 layanan user + 5 layanan system** berjalan normal (daftar di §2).
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
| Mission Control | Tailscale funnel | ✅ https://zb-vela.tailec8707.ts.net |

Ingress dikelola via Composio (`CLOUDFLARE_UPDATE_TUNNEL_CONFIGURATION`, replace-style — selalu kirim daftar lengkap). DNS record via `composio proxy` toolkit cloudflare (zone `762ed25a87cead530391792341d414ad`).

## 4. Niudrive (9Drive) — Kondisi Terkini

### Arsitektur
- Backend: Express + TypeScript + Prisma, MariaDB `9drive` — 17 migrasi up-to-date.
- Frontend: Vite 8 + React 19 + Tailwind 4, PWA (autoUpdate), Vite preview :5173.
- Repo: `github.com/Niumination/niudrive` (main). Merge PR #1 (redesign UI arena.ai) = `3da9d2b`.

### UI/UX (12 Nov)
- **Bahasa Indonesia penuh** di seluruh UI (27 file; istilah teknis tetap: Google Drive, OAuth, API, MIME, MB/GB).
- **Ikon brand baru**: glyph "9" seimbang + gradient lime di graphite (`favicon`, `pwa-192/512`, `maskable`, `BrandLogo.tsx`).
- **Ikon folder duotone inline** (`FolderGlyph` di `FolderVisual.tsx`) — menggantikan fetch remote `api.iconify.design` (yang 403 dari VPS). 42 pilihan ikon; URL iconify lama di DB otomatis dimapping (`normalizeFolderIconKey`).
- Tema graphite + lime, dark/light, PWA installable.

### Upload & performa
- **Batch upload**: file kecil (<5 MB) dikumpulkan ≤25 file/request, total ≤8 MB/request; file ≥5 MB single request. UI upload juga batch (`UploadContext.tsx`, ≤20 MB/≤25 file).
- Backend cache per-request (auth, folder ID, routing) — ±8 panggilan/batch (dulu ±150).
- **cloudflared `--protocol http2`** — TANPA ini, upload >1–2 MB via tunnel hang/502 (isu QUIC). Terbukti: 19 MB → 201 dalam 6 detik.
- Benchmark 40 file kecil: 7,2 s (0,18 s/file, 16× lebih cepat dari sequential).
- Audit log `UPLOAD_FILE` tercatat untuk semua jalur upload.

### Data (12 Nov, dari DB)
- **1.523 file aktif, 481 folder, 8 akun Drive connected** (pool ±128 GB).
- Routing policy: mode priority → **zhallbay28@gmail.com #1**. Folder baru otomatis di-pin ke akun hasil routing (fisik + pencatatan kuota konsisten — patch folder.routes.ts, revert commit opencode `776b3a3`).
- `archk4li@gmail.com` dikosongkan (folder `9drive` dihapus permanen).
- Backup Mac: `~/Downloads` (37 file vault + 16 loose + APK 115 MB) dan `~/Documents` (405 file) — di `9drive/mac/...` zhallbay28, terverifikasi fisik di Drive. Script Mac: `~/backup-niudrive/backup-device.mjs` (sinkron repo ≥`3974265`: cek `failed[]` di respons 201, FormData baru per retry, `NINEDRIVE_EXCLUDE` tersedia).
- **Kebijakan user**: tidak ada exclude — kredensial/rahasia memang sengaja dibackup ke niudrive. Pencegahan (rotate/purge) hanya jika ada potensi bocor publik.
- **Password akun backup-agent dirotasi 12 Nov** (file `~/zb/niudrive-backup-agent-NEWPASS.txt`, chmod 600; hapus setelah Mac update `.env`; 172 session lama di-invalidasi).

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
| `niudrive-backup.timer` | harian 01:30 | 13 Nov 01:30 | DB+config niudrive → Drive |
| `zb-backup.timer` | Senin 00:10 | 9 Nov | backup kecil harian → Google Drive via Composio |
| `zb-backup-full.timer` | Minggu 02:30 | 8 Nov | full split `--secret`, keep-3, auto-cleanup Drive |

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
- Rotasi password backup-agent niudrive 12 Nov + 172 session lama invalid.
- File rahasia yang sempat bocor ke Drive sudah di-purge permanen (`niudrive-backup-agent.env`, duplikat GPG key). Audit menyeluruh 8 akun Drive: bersih dari kebocoran tak sengaja.
- `git push` CLI exit 128 → GitHub HANYA via composio contents API. Repo `ecosystem-config` tidak boleh disentuh tanpa izin eksplisit user.
- Dilarang push otomatis/aksi ke repo milik user tanpa approval (pelajaran insiden opencode `776b3a3`).

## 9. Known Issues / Pending

1. **PiPatung belum jalan** (:3100 kosong → 502). Kode `~/zb/pi-patung` v0.1.0 — start manual saat dibutuhkan.
2. Antigravity OMB `authenticated=false` (OAuth :53727 pending sign-in).
3. **File password backup-agent masih di VPS & Mac** — hapus keduanya setelah `.env` Mac diperbarui.
4. Hermes Agent OS: wiki + offsite backup deployment menunggu keputusan user.
5. Composio koneksi `cloudflare` tanpa scope DNS/zone untuk beberapa tool (`LIST_ZONES` 403) — tapi `composio proxy` ke REST CF langsung berfungsi (DNS, bot_management, rulesets).
6. noVNC `/websockify` via HTTP/2 bisa 404 — browser nyata selalu HTTP/1.1 untuk WS, aman.

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

# Push file ke repo via composio (redirect + verifikasi hash WAJIB)
composio proxy "https://api.github.com/repos/OWNER/REPO/contents/PATH?ref=main" -t github --skip-connection-check > /tmp/f.json
composio proxy "https://api.github.com/repos/OWNER/REPO/contents/PATH" -t github --skip-connection-check -X PUT --data @/tmp/put.json
```
