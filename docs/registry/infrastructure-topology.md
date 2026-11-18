# Infrastructure Topology — Niumination

> **Diverifikasi:** 2026-11-18 10:45–11:05 WIB · **Metode:** probe DNS/HTTP langsung, SSH read-only ke Cloudbaik, inspeksi `state.db` & config Mac
> **Aturan:** dokumen ini tidak memuat kredensial — hanya nama host, IP, dan port.

## 1. Empat Lokasi

| # | Lokasi | Akses | Isi (per 18 Nov 2026) |
|---|---|---|---|
| 1 | **Mac** (lokal) | — | Hermes Agent (gateway), OpenCode, MIRAI :8800, 9router :20128, A2A :9900, Camofox :9377 |
| 2 | **VPS Lightvela** | tailnet `100.65.20.34` · CF Tunnel | Hermes Agent, OMB (`maus.abstract.biz.id` — **LIVE 200**) |
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

## 5. Node 2 — Lightvela

- **OMB: `maus.abstract.biz.id` → LIVE `200`**, judul `MausBot` (933 B) — instance berbeda dari zb-vela (`zbmaus.abstract.biz.id` → `OpenMausBot`, 859 B).
- **IP publik `103.30.146.232` tidak merespons** — ping 100% loss; port 80/443/8080/8799/8800/9900 semua closed. Kemungkinan: IP berubah, atau server di-firewall hanya untuk Cloudflare Tunnel.
- **A2A (tailnet `100.65.20.34:9900`) tidak terjangkau** — tailscale Mac stopped.
- Domain `maus.abstract.web.id` **tidak ada** (NXDOMAIN) — catatan lama salah zona.

## 6. Temuan

1. **IP publik Lightvela mati.** `103.30.146.232` tak merespons (ICMP + 6 port). OMB tetap LIVE via CF Tunnel → server kemungkinan UP; IP publik perlu diverifikasi ulang (berubah, atau firewall CF-only).
2. **Tailscale STOPPED** di Mac → IP `100.120.57.37` tidak ada → A2A bind gagal, semua peer tailnet (lightvela, zb-vela, aperture) tak terjangkau. Konfigurasi masih benar (`bind: 100.120.57.37`, `localhost_only: False`) — yang berubah hanya status tailscale.
3. **`maus.abstract.web.id` salah zona.** NXDOMAIN. Yang benar `maus.abstract.biz.id` (LIVE). Catatan lama di `ROADMAP-MIRAI-2026-11-04.md` memakai zona `.web.id`.
4. **A2A health check gagal terus — tapi BUKAN bukti downtime.** 43 run: OK terakhir 29 Okt 2026; penyebab kegagalan adalah model/provider (`HTTP 403 OpenCode free tier`, `HTTP 404 No active credentials for provider: openai`), bukan konektivitas. Jangan dijadikan indikator status peer.
5. **`pipatung.abstract.biz.id` 502** — app belum dijalanakan (sudah terdocumentasi di `ECOSYSTEM-STATUS.md`).
6. **`docs/registry/deployment-status.md` stale** — masih menulis `abstract.biz.id` = "DNS REFUSED" (8 Okt 2026); hari ini zona itu resolve normal.
7. **`maus.abstract.biz.id` sebelumnya tak terdaftar** di registry mana pun — sekarang tercatat di dokumen ini.

## 7. Cara Mengakses

| Target | Cara |
|---|---|
| Cloudbaik | `ssh vps-baik` (key `~/.ssh/vps_baik.pem`) |
| zb-vela | tailnet `100.77.18.39` (butuh tailscale up) · layanan via CF Tunnel |
| Lightvela | tailnet `100.65.20.34` (butuh tailscale up) · **publik mati** |
| Mac A2A | `localhost:9900` setelah tailscale up |

## 8. Repo GitHub per Node

Perkembangan Lightvela & zb-vela **tidak** masuk `ecosystem-config` — masing-masing punya repo sendiri di org `Niumination` (169 repo total).

### Lightvela
| Repo | Visibilitas | Isi |
|---|---|---|
| `omb-lightvela` | PUBLIC | deployment OMB LightVela — Docker stack aktif di `maus.abstract.biz.id` |
| `omb-lightvela-secrets` | PRIVATE | secrets & state live stack (pasangan repo publik) |
| `lightvela-hermes-backup` | PRIVATE | backup harian terenkripsi instance Hermes LightVela + runbook restore |
| `lightvela-dash` | PRIVATE | LightVela Dashboard — Telegram Mini App |

### zb-vela
| Repo | Visibilitas | Isi |
|---|---|---|
| `zbmaus-vela` | PUBLIC | paket setup & konfigurasi OMB untuk satu VPS (OMB UI, noVNC token gate, …) |
| `zbmaus-vela-secrets` | PRIVATE | secrets & state live stack zbmaus |
| `zbmaus-vela-eco` | PUBLIC | snapshot ekosistem OMB (bot, routine, memory, skills, koneksi) |
| `zbmaus-humanoid` · `zb-humanoid` | PUBLIC | interface humanoid yang terhubung OMB |
| `niudrive` | PRIVATE | Niudrive (9Drive) |

### Terkait OMB (lintas node)
| Repo | Visibilitas | Isi |
|---|---|---|
| `ecosystem-omb` | PUBLIC | registry ekosistem OpenMausBot — struktur tim/bot, routine, kebijakan |
| `contentvela` | PUBLIC | content creator workspace |

> Push terakhir repo-repo ini: **18 Nov 2026** (zbmaus-vela trio) — sesuai catatan pemilik bahwa perkembangan kedua VPS selalu di-update.
