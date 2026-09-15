---
name: niu-9router-maintain
description: Maintenance router model lokal 9router (localhost:20128) untuk ekosistem Niumination — health check, tes akses semua model, disable provider/model yang gagal, restart daemon otomatis. Gunakan saat user tambah provider/model manual ke 9router atau minta "cek/rawat 9router".
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [9router, model-router, localhost, niumination, maintenance, telegram-routing]
    related_skills: [ecosystem-snapshot, hermes-agent]
---

# Niu 9Router Maintenance

Router model lokal **9router** jalan di `localhost:20128` (Next.js app di `/usr/local/lib/node_modules/9router/app`). Semua channel Telegram Hermes (1/802/803/804/1172) mengarah ke sini via `channel_overrides` di `~/.hermes/config.yaml`. Kalau 9router mati → Telegram lumpuh.

Daemon dikelola launchctl: `com.9router.autostart` (server) + `com.niumination.9router-watch` (cache watcher, non-kritis). Sudah di-set **auto-restart** — kalau server mati akan hidup sendiri.

## When to Use
- User: "cek 9router", "rawat 9router", "tambah model ke 9router", "model di Telegram error"
- Setelah user tambah provider/api-key manual di UI 9router
- Verifikasi routing Telegram pasca perubahan

## Quick Health Check (read-only)
```bash
curl -s -o /dev/null -w "%{http_code}" -m 8 http://localhost:20128/v1/models
# 200 = hidup. Selain itu → restart:
launchctl kickstart -k gui/$(id -u)/com.9router.autostart
```

## Full Model Accessibility Audit (pakai script)
Script `scripts/audit_models.py` akan:
1. Fetch `/v1/models` dari 9router
2. Tes chat completion tiap model (parallel, timeout 20s)
3. Pisahkan FAIL permanen (400/402/404/410/500/503) vs sementara (429/timeout)
4. Disable provider yang **0 model OK** via sqlite `providerConnections.isActive=0`
5. Restart server agar reload

```bash
python3 ~/.hermes/skills/niu-9router-maintain/scripts/audit_models.py
```

## Provider Gratis vs Berbayar
9router **tidak punya flag paid/free**. Kriteria: tes akses langsung. Yang 0/OK = disable.
**Penting:** 9router listing 511 model dari 13 provider, tapi 94% tidak accessible (400/403/410/429/503). Provider yang 0 model OK → disable via sqlite.
Provider yang diketahui punya akses (per 14-Sep-2026): `gemini` (AI Studio key), `github` (Copilot free tier, banyak model 400), `kr` (Kiro free tier), `cf` (Cloudflare Workers). Provider yang DISABLE (0 model OK): `explabs` (342 model, payment required), `antigravity` (timeout), `kimi` (quota exhausted), `nvidia` (410 retired), `ollama` (410 retired), `bazaarlink` (402 credits), `byteplus` (400 subscription), `poolside` (404), `bpm` (503), `ps` (503), `api-airforce` (503).
→ Disable provider yang 0 model OK via sqlite `providerConnections.isActive=0`, lalu restart server.
→ Nonaktifkan provider TIDAK menghapus data — model tetap ada di catalog tapi tidak di-return ke Telegram.

## Manual Provider Disable (sqlite)
```python
import sqlite3
con=sqlite3.connect('/Users/zaryu/.9router/db/data.sqlite')
con.execute("UPDATE providerConnections SET isActive=0 WHERE provider=?", ('kimi',))
con.commit()
# lalu restart server
```

## Restart Setelah Perubahan
```bash
launchctl kickstart -k gui/$(id -u)/com.9router.autostart
sleep 4
curl -s -o /dev/null -w "%{http_code}" -m 8 http://localhost:20128/v1/models
```

## Verify Telegram Routing (Hermes)
```bash
hermes fallback list          # primary + chain
hermes config get platforms.telegram.channel_overrides   # 5 channel → 9router
```

## Crash-Loop Fix (dari insiden 27-Agu-2026 — diperbarui 29-Agu)
Jika 9router mati / `curl 127.0.0.1:20128` terus `000`:
- **Symptom A (TUI loop):** launchd restart 130+ kali, tiap instance print `Exiting...` lalu mati. Root cause: 9router CLI tampilkan **TUI menu interaktif** (web/terminal/tray/exit) saat jalan tanpa TTY → menu baca EOF → pilih "exit" → cleanup kill server child → loop.
- **Symptom B (KeepAlive false):** process ada di `launchctl list` tapi **tidak listen** (lsof kosong). Penyebab nyata 29-Agu: plist punya `KeepAlive: false` → kalau server child exit, launchd **tidak restart**. Tray jalan tapi HTTP server mati diam-diam.
- **Symptom C (race condition startup):** setelah launch, `curl` balikin `000` selama ~10 detik pertama meskipun nanti `200`. Ini BUKAN crash — server belum bind. Tunggu / retry.

**Fix wajib (plist `com.9router.autostart`):**
```xml
<key>ProgramArguments</key>
<array>
  <string>/usr/local/Cellar/node/26.7.0/bin/node</string>
  <string>/usr/local/lib/node_modules/9router/cli.js</string>
  <string>--tray</string>
  <string>--skip-update</string>
  <string>--no-browser</string>
  <string>--host</string><string>127.0.0.1</string>
  <string>--port</string><string>20128</string>
</array>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>   <!-- PENTING: false = 9router mati & tidak auto-restart -->
```
```bash
launchctl unload ~/Library/LaunchAgents/com.9router.autostart.plist
pkill -f "9router/cli.js"
launchctl load ~/Library/LaunchAgents/com.9router.autostart.plist
```

**Verify (dengan retry — jangan panik kalau 000 di 3 detik pertama):**
```bash
for i in $(seq 1 8); do
  curl -s -o /dev/null -w "try$i: %{http_code}\n" -m 8 http://127.0.0.1:20128/v1/models
  sleep 2
done   # expect 200 setelah ~try3
lsof -iTCP:20128 -sTCP:LISTEN -P -n   # harus ada baris LISTEN
```
Model catalog + resep verifikasi Gemini/Antigravity: lihat `references/9router-models-and-connectivity.md`.

## Model Change Notifications (Realtime) — `com.niumination.9router-sync`
User suka dapat notifikasi macOS tiap ada perubahan model di 9router. Mechanism + cara (re)pasang:

**Cara kerja (realtime, dua lapis):**
1. **9router fetch LIVE** — `/v1/models` **tidak di-cache** (tidak ada tabel `modelCache` di sqlite, tidak ada TTL). Tiap request → 9router tanya langsung ke provider (Gemini/AG/Antigravity API). Model baru dari provider otomatis kelihatan besok tanpa restart.
2. **Notifikasi** — `scripts/9router-sync.sh` (hybrid watcher): fetch `/v1/models` → hash sorted IDs → bandingkan dgn `~/.cache/niumination/9router-models.hash`. Kalau hash beda → `osascript display notification` + tulis `~/.9router-state.json`. Kalau sama → silent (exit 0).

**Plist launchd (`com.niumination.9router-sync.plist`):** ada di `scripts/com.niumination.9router-sync.plist` (backup version-controlled). Trigger ganda:
- `StartInterval: 300` (poll 5 menit)
- `WatchPaths: ~/.9router/db/data.sqlite` (trigger instan kalau provider di-enable/disable di dashboard)

```bash
# (re)pasang:
cp ~/Desktop/Niumination/scripts/com.niumination.9router-sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.niumination.9router-sync.plist
# test manual (harusnya notify kalau ada delta):
bash ~/Desktop/Niumination/scripts/9router-sync.sh
```

**Pitfall:** notifikasi hanya muncul kalau ada DELTA model. Hash sama = silent. Jangan kira script mati kalau tidak ada notif — cek `tail /tmp/9router-sync.log` & `.9router-state.json`.

**Verify notifikasi jalan:** `osascript -e 'display notification "test" with title "9router sync"'` → harus muncul di Notification Center.

## Pitfalls
- Jangan matikan `com.9router.autostart` — itu server utama. `com.niumination.9router-watch` boleh mati (cuma cache).
- Model 400 di GitHub Copilot = model tidak ada di free tier, biarkan (provider masih berguna, ada yang OK).
- `big-pickle`/`hy3-free` **tidak ada di 9router** — lewat opencode-zen langsung (cron model).
- 9router pakai `NINE_ROUTER_API_KEY` (env passthrough di config Hermes).
- DB sqlite: `~/.9router/db/data.sqlite` (providerConnections, usageHistory).
