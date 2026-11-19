# VPS Health — Laporan Eksternal

> **Sumber:** laporan Hermes di VPS (diteruskan pemilik 20 Nov 2026)
> **Jenis:** catatan status — *tidak* diverifikasi ulang dari Mac (Tailscale stopped, tailnet tak terjangkau)

## 1. Lightvela — 🟢 sehat, 2 isu operasional

**Server:** up 27 hari · load 0.09 · RAM 1.8G/7.4G · disk 38G/50G (9.5G bebas, 80%)

**Docker:** `omb` Up 13 hari (healthy) · build cache 1.16G (0 reclaimable) · image reclaimable 2.1G

**User services:** 3 failed — `xdg-desktop-portal-gtk`, `xdg-desktop-portal`, `xfce4-notifyd`
(kosmetik desktop GUI, tak dipakai operasi)

**Gateway:** active since 16 Nov 15:57 · NRestarts=0 · mem 1.6G (peak 6.8G) · Telegram `getMe` 200 ·
WhatsApp/vela-im tersambung

**Cron:** 10 job, 9 enabled · semua streak=0 terakhir · 3 hari: CRON 19 sesi / 153 call / 3.03M token
(`agnes-2.5-flash` ×15) · Job QA Studio 19 Nov 13:01 ok

**Endpoint:** abstract 200 · cuaca 200 · niu 200 · mira 200 · dao 200 · OMB 8799 200 ·
A2A 9900 (tailnet) 200 · aperture 302 (hidup) · `token.lightvela.ai/v1/models` 401 (wajar, butuh key) ·
9router 20128 `/v1/models` 200

**Tailscale:** serve `/`→7444, `/agroclimate`→7444, `/api`→7455; 9443→20128 · Funnel OFF ·
v1.104.7 (≥ fix Tailworm)

**Git:** 5z-repo / 5z-mira / niu-rem — dirty 0, HEAD = remote

## 2. zb-vela — 🟢 sehat, tanpa anomali

**Server:** uptime 4m5h14h · disk 71% (14 GB bebas) · RAM 3.3/7.4 GiB (4.1 GiB available)

**Layanan (9 user, semua active):** ombnew · omb-relay-bridge · novnc-gate · 9router ·
niudrive-backend/frontend · hermes-gateway · zb-humanoid · hermes-agent-os-dashboard
**System (6):** ytoauth · cloudflared · tailscaled · deepseek-harness · vela-x11vnc · vela-novnc

**Domain `/health` 200:** yt · api · zbmaus · niudrive · zb-humanoid
**Root 200:** zbmaus · niudrive · zb-humanoid · **404 normal:** yt · api · ombrelay ·
**401 (token-gated, benar):** opencraft · dsh · **502 (known):** pipatung

**YouTube OAuth:** token OK (auto-refresh) · channel Kitab Surgawi terverifikasi · 8/8 routine pakai helper OAuth lokal

**Backup:** niudrive-backup 19 Nov 01:30 (24 upload / 0 gagal), berikutnya 20 Nov 01:30 ·
zb-backup-full 22 Nov · zb-backup 23 Nov

**Tailnet:** zb-vela `100.77.18.39` online

## 3. Keputusan tertunda — Lightvela (butuh "gas")

### 3.1 Composio MCP mati
- Gejala: 4.517 baris warning di `agent.log`, 2.908 di `errors.log`
- Penyebab: `Bearer token rejected: not a valid AuthKit JWT`
- Kunci **tidak ada** di `.env` (hanya 23 key, COMPOSIO absen); drop-in systemd tak menyetel
- Kunci di `~/niumination/Composio-api.md` juga **ditolak server (401)** → kredensial usang,
  bukan salah konfigurasi
- **Pilihan:** (a) matikan server composio di `config.yaml`, (b) ambil JWT AuthKit baru

### 3.2 backup-repo divergen (selamanya non-ff)
- Gejala: lokal 88 commit vs remote 88, **beda rantai total**
- Sebab struktural: `daily-hermes-backup.sh` baris **172–173** sudah fetch+rebase
  (fallback `reset --hard`), tapi **prune `filter-branch` baris 181–184** berjalan **setelah push**
  dan mengubah hash commit lokal
- Akibat: push 19 Nov 21:00 mendarat (`PUSH OK`), lalu prune membuat lokal ≠ remote permanen.
  Push berikutnya akan selalu non-ff → backup harian berisiko gagal
- Isi aman: blob gpg lokal = remote `3513ff11…` (101.235.575 B) · MANIFEST sama `4de51a5b…` · fsck bersih
- **Perbaikan:** pindahkan prune ke **sebelum** push (atau rebase ulang pasca-prune)

## 4. Sisa ringan — Lightvela (semua regenerable)

- `backup-repo/.git` 8.2G
- `state-snapshots` 1.7G (8 snapshot — rekomendasi: sisakan 2 → bebas ±1.3G)
- `/tmp` 1.9G
- apt cache 114M
- docker image reclaimable 2.1G

## 5. Upgrade tertunda (ditahan sesuai arahan pemilik)

- Hermes `v0.21.5` → `v0.23.2`
- 9router `0.5.112` → `0.5.119`

## 6. Catatan verifikasi & akses

- **Tailscale semula STOPPED** di Mac → `100.65.20.34` / `100.77.18.39` tak terjangkau
  (rute keluar lewat gateway normal, HTTP 000). `nc -z` sempat melaporkan OPEN — **positif palsu**.
- **Tailscale dinaikkan 20 Nov 2026** (`tailscale up`) → 6 peer terlihat, agent card A2A
  Lightvela `200`. Pemulihan akses ini **reversibel** (`tailscale down`).
- **SSH ke Lightvela DIBLOKIR** tailnet policy: `tailnet policy does not permit you to SSH as user "root"`.
- **A2A Mac → Lightvela MATI (401).** `POST /` dengan `Authorization: Bearer <token>` →
  `{"code":-32050,"message":"unauthorized"}`. Ketiga sumber token di Mac (`a2a_agents.cloud.token`
  di config, `vault/a2a-token.txt`, `~/.hermes/.env`) **identik** (48 char) — jadi bukan token
  usang di Mac; server Lightvela menolak token ini.
  → mendispatch tugas ke Lightvela dari Mac **tidak mungkin** sampai token diselaraskan.
- Laporan di dokumen ini **belum diverifikasi ulang** dari sisi Mac — dicatat apa adanya.
