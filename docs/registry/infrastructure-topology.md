# Infrastructure Topology — Niumination

> **Diverifikasi:** 2026-11-18 10:45–11:05 WIB · **Metode:** probe DNS/HTTP langsung, SSH read-only ke Cloudbaik, inspeksi `state.db` & config Mac
> **Aturan:** dokumen ini tidak memuat kredensial — hanya nama host, IP, dan port.

## 1. Empat Lokasi

| # | Lokasi | Akses | Isi (per 18 Nov 2026) |
|---|---|---|---|
| 1 | **Mac** (lokal) | — | Hermes Agent (gateway), OpenCode, MIRAI :8800, 9router :20128, A2A :9900, Camofox :9377 |
| 2 | **VPS Lightvela** | tailnet `100.65.20.34` · publik `103.30.146.232` | Hermes Agent, OMB (`maus.abstract.web.id`) — **TIDAK TERJANGKAU** |
| 3 | **VPS zb-vela** | tailnet `100.77.18.39` · CF Tunnel | Hermes Agent, OMB (`zbmaus.abstract.biz.id`), DSH (`dsh.abstract.biz.id`) |
| 4 | **VPS Cloudbaik** | SSH `vps-baik` → `103.30.146.23` | OpenCode (`oc.niumination.id`), DSH (`dsh.niumination.id`), cloudflared |

Tailnet: `tailec8707` · peer: Mac `100.120.57.37`, lightvela `100.65.20.34`, aperture `100.78.217.67`, zb-vela `100.77.18.39`.

## 2. Node 1 — Mac

| Layanan | Port | Status |
|---|---|---|
| Hermes gateway (`ai.hermes.gateway`) | — | running (LaunchAgent) |
| OpenCode | — | running (`opencode serve --service`) |
| MIRAI Mission Control | 8800 | `200` |
| 9router | 20128 | `200` |
| A2A | 9900 | **tidak listening** — lihat Temuan |
| Camofox | 9377 | running |

## 3. Node 4 — Cloudbaik (terverifikasi via SSH read-only)

- **Host:** `arch-kali-baik2641-client-cloudbaik-id` · uptime 8 hari · load 0.13
- **SSH:** `vps-baik` → `103.30.146.23` (port 22) · ping OK (49 ms)
- **Docker:** tidak terpasang
- **Systemd running:** `cloudflared` (active), `dsh-web`, `dsh-auth-proxy`, `cron`, `ssh`
- **Cloudflared tunnel** `4f016243-4f23-4ee3-bb00-e15f3dea3257`:
  - `oc.niumination.id` → `localhost:49374`
  - `dsh.niumination.id` → `localhost:8000`
- **DSH:** `/root/dsh-web` → `@deepseek-ai/dsh web --host 127.0.0.1 --port 8000`
- **Hermes:** **tidak ada** (`which hermes` kosong, `~/.hermes` tidak ada) — konsisten dengan deskripsi pemilik
- **Port publik:** 22, 8001, 19988 · sisanya localhost

## 4. Node 3 — zb-vela (via Cloudflare Tunnel)

| Domain | Endpoint | Status |
|---|---|---|
| `zbmaus.abstract.biz.id` | :8799 (OMB) | `200` |
| `dsh.abstract.biz.id` | :3080 | `401` (token — benar) |
| `zb-humanoid.abstract.biz.id` | :3001 | `200` |
| `ombrelay.abstract.biz.id` | :8801 | root `404`, `/health` `200` |
| `opencraft.abstract.biz.id` | :6081 | `401` (key — benar) |
| `niudrive.abstract.biz.id` | :5173 | `200` |
| `api.abstract.biz.id` | :4000 | root `404`, `/health` `200` |
| `pipatung.abstract.biz.id` | :3100 | ⚠️ `502` — app belum jalan (terdocumentasi) |

Detail lengkap: `docs/ECOSYSTEM-STATUS.md`.

## 5. Node 2 — Lightvela — TIDAK TERJANGKAU

- `103.30.146.232` → **ping 100% packet loss**; port 9900/8799/8800/3000 semua **closed**
- `maus.abstract.web.id` → **NXDOMAIN** (tidak ada record)
- Catatan: `maus.abstract.biz.id` **ada** dan `200` (A record Cloudflare) — kemungkinan OMB Lightvela pindah ke zona `.biz.id`, atau alias zbmaus

## 6. Temuan

1. **Lightvela offline.** IP publik mati, domain `maus.abstract.web.id` tidak terdaftar. A2A Mac↔Lightvela ikut mati. Perlu keputusan: nyalakan lagi, ganti IP, atau arsip.
2. **Tailscale STOPPED** di Mac → IP `100.120.57.37` tidak ada → A2A bind gagal, semua peer tailnet (lightvela, zb-vela, aperture) tak terjangkau. Konfigurasi masih benar (`bind: 100.120.57.37`, `localhost_only: False`), yang berubah hanya status tailscale.
3. **`maus.abstract.web.id` salah zona.** NXDOMAIN; `.biz.id` yang ada.
4. **`pipatung.abstract.biz.id` 502** — app belum dijalanakan (sudah terdocumentasi di `ECOSYSTEM-STATUS.md`).
5. **`docs/registry/deployment-status.md` stale** — masih menulis `abstract.biz.id` = "DNS REFUSED" (8 Okt 2026); hari ini zona itu resolve normal.
6. **Aset publik lain yang muncul:** `maus.abstract.biz.id` (200) belum terdaftar di registry mana pun.

## 7. Cara Mengakses

| Target | Cara |
|---|---|
| Cloudbaik | `ssh vps-baik` (key `~/.ssh/vps_baik.pem`) |
| zb-vela | tailnet `100.77.18.39` (butuh tailscale up) · layanan via CF Tunnel |
| Lightvela | tailnet `100.65.20.34` (butuh tailscale up) · **publik mati** |
| Mac A2A | `localhost:9900` setelah tailscale up |
