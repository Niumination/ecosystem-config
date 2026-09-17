---
name: camofox-browser
description: Manage Camofox stealth browser at localhost:9377.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [camofox, browser, stealth, headless]
    related_skills: [agent-reach, niu-9router-maintain]
---

# Camofox Browser

**Camofox Browser** — stealth headless browser automation server. Berjalan di `localhost:9377` sebagai REST API. Mesinnya **Camoufox** — fork Firefox yang spoofing fingerprint (WebGL, AudioContext, hardwareConcurrency, WebRTC, screen geometry) di level C++.

## Quick Reference

### Start Server
```bash
cd ~/Desktop/Niumination/tools/camofox-browser
CAMOFOX_API_KEY="hermes-camofox-2026" CAMOFOX_ACCESS_KEY="hermes-camofox-2026" CAMOFOX_ADMIN_KEY="hermes-camofox-admin-2026" CAMOFOX_PORT=9377 node --max-old-space-size=512 server.js &
```

### Health Check
```bash
curl -s http://localhost:9377/health
# Expected: {"ok":true, "browserRunning":true, "activeTabs":0, "memory":{"rssMb":...}}
```

### API Workflow
1. **Create tab**: `POST /tabs` → `{tabId}`
2. **Navigate**: `POST /tabs/:id/navigate` → `{url, title}`
3. **Snapshot**: `GET /tabs/:id/snapshot?userId=...` → accessibility tree with refs (`e1`, `e2`)
4. **Click/Type**: `POST /tabs/:id/click` or `/type` with ref or CSS selector
5. **Cleanup**: `DELETE /tabs/:id`

### Auth
- Header: `Authorization: Bearer hermes-camofox-2026`
- API key from env `CAMOFOX_API_KEY`

### Auto-start
Server auto-start via launchd: `~/Library/LaunchAgents/ai.hermes.camofox.plist` (`RunAtLoad` + `KeepAlive`). `launchctl load/unload` DIBLOKIR dari dalam Hermes — jalankan dari Terminal terpisah:
```bash
launchctl load ~/Library/LaunchAgents/ai.hermes.camofox.plist
```
Fallback manual (env lengkap):
```bash
cd ~/Desktop/Niumination/tools/camofox-browser
CAMOFOX_PORT=9377 CAMOFOX_API_KEY=hermes-camofox-2026 CAMOFOX_ACCESS_KEY=hermes-camofox-2026 CAMOFOX_ADMIN_KEY=hermes-camofox-admin-2026 CAMOFOX_HERMES_ACTIVE=1 node server.js &
```
Plist env change (mis. tambah variabel) hanya berlaku setelah `unload` + `load` ulang dari Terminal terpisah — `kill` PID saja me-restart dengan env LAMA (kode baru tetap termuat karena dibaca dari disk).

### Config
File: `camofox.config.json`
- `plugins.youtube`: enabled (yt-dlp transcript extraction)
- `plugins.persistence`: enabled (session persistence to `~/.camofox/profiles`)
- `plugins.vnc`: disabled

### Integration Pattern
Jangan install package di proyek lain — cukup HTTP call ke `localhost:9377`:
```js
const tab = await fetch('http://localhost:9377/tabs', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer hermes-camofox-2026' },
  body: JSON.stringify({ userId: 'agent1', sessionKey: 'task1', url: 'https://example.com' })
}).then(r => r.json());
const snap = await fetch(`http://localhost:9377/tabs/${tab.tabId}/snapshot?userId=agent1`, {
  headers: { 'Authorization': 'Bearer hermes-camofox-2026' }
}).then(r => r.json());
```

### Troubleshooting
| Issue | Fix |
|-------|-----|
| `node_modules` missing | `cd ~/Desktop/Niumination/tools/camofox-browser && npm install` |
| Port 9377 not listening | After `kill`, confirm KeepAlive actually resurrected via `pgrep` + `/health` (restart is not instant) — if still down, start manually with full env, then keep the launchd job as owner |
| Browser not launching | Check `~/.cache/camoufox/` dan `~/Library/Caches/camoufox/` |
| 401 Unauthorized | Global access-gate membandingkan Bearer dengan `CAMOFOX_ACCESS_KEY` (bukan API key) — header: `Authorization: Bearer hermes-camofox-2026` |
| `userId and sessionKey required` | `POST /tabs` wajib `userId` DAN `sessionKey` — contoh: `{"userId":"agent1","sessionKey":"task1","url":"https://example.com"}` |
| `lib/launcher.js` error | Pastikan `camoufox-js` binary terinstall: `npx camoufox-js --version` |
| npm install timeout | `timeout 300 npm install` atau `npm install --prefer-offline` |
| `Blocked URL scheme: file:` | Camofox hanya melayani http/https. Untuk file lokal, jalankan `python3 -m http.server` (background) di direktori file, lalu buka `http://127.0.0.1:<port>/<file>` |
| Tab create `timed out after 30000ms` pada URL lokal | Jangan stack beberapa percobaan membuat tab paralel ke server yang sama pada URL yang sama saat browser sedang hang — satu request timeout akan hang semua request berikutnya (session per userId terisolasi, tapi browser process-nya satu). Restart server bila stuck |
| Perlu analisis visual (aplikasi vision) | Pilih provider/model yang mendukung input gambar. Error `No endpoints found that support image input` berarti model aktif tidak punya kemampuan vision — ganti model, atau pakai jalur OCR (`tesseract`) untuk inventaris teks |

### Notes
- **npm install terkadang timeout** — proses install 163M+ package. Gunakan `timeout 300` atau jalankan dari Terminal terpisah. Jika terminal call ter-block approval-timeout TAPI `node_modules` sudah terbentuk penuh (cek `du -sh node_modules`, ±163M), install sebenarnya sudah selesai — lanjut langsung ke start server, jangan ulang `npm install`.
- **Hermes-aware keepalive** — saat gateway Hermes aktif, browser TIDAK boleh idle-shutdown: guard di `scheduleBrowserIdleShutdown()` (single funnel untuk semua call site: tutup session, expiry sweep, pre-warm), watchdog 60 detik relaunch bila browser mati (crash/memory-pressure restart), `/health` memicu warm-retry + field `hermes.{active,gatewayProcess,gatewayPlist}`. Flag via `CAMOFOX_HERMES_ACTIVE=1`; fallback deteksi live `pgrep -f "hermes_cli.main gateway"` di `lib/hermes.js` (`child_process` tetap terisolasi di `lib/`, jangan panggil dari `server.js` langsung — aturan separation repo ini).
- **Diagnosis dua lapis sebelum restart** — port 9377 tidak LISTEN = server mati (start ulang); `/health` `ok:true` tapi `browserRunning:false` = browser idle-shutdown/crash (pukul `/health` untuk trigger warm-retry atau tunggu watchdog 60s; launch butuh ~30-60 dtk cold start). Jangan restart server untuk kasus kedua — warm-retry cukup.
- **Browser lazy-launch** — request `/tabs` pertama setelah idle men-trigger launch (~3-5 dtk). Selama itu jangan mengirim request tab paralel; tunggu launch selesai.
- **Repo mandiri** — `tools/camofox-browser/` adalah git repo sendiri (di-ignore root Niumination). Commit perbaikan di repo itu, bukan di root ekosistem.
- **Memory** — ~110-120MB saat idle, naik saat aktif.
- **VNC plugin** — tersedia tapi disabled. Aktifkan di `camofox.config.json` jika butuh interactive browser.
- **Bukan tool untuk file:// atau inventaris visual** — untuk memeriksa isi screenshot/frame video lokal, jalur yang jauh lebih murah: `ffmpeg` ekstrak frame + `tesseract` OCR teksnya. Camofox hanya untuk interaksi web http/https.

## Files
- `~/Desktop/Niumination/tools/camofox-browser/` — repo upstream `jo-inc/camofox-browser`
- `camofox.config.json` — plugin configuration
- `server.js` — REST API server
- `~/Library/LaunchAgents/ai.hermes.camofox.plist` — launchd config (manual load only)
