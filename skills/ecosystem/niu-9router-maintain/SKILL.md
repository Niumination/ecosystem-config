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

Daemon dikelola launchctl: `com.9router.autostart` (server) + `com.niumination.9router-sync` (watcher
katalog, non-kritis — plist `com.niumination.9router-watch` sudah **dihapus**, dua poller balapan di file
hash yang sama). Sudah di-set **auto-restart** — kalau server mati akan hidup sendiri.

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

## Full Model Accessibility Audit (pakai script — DRY-RUN default)
```bash
python3 ~/.hermes/skills/niu-9router-maintain/scripts/audit_models.py            # probe + laporan, DB TIDAK disentuh
python3 ~/.hermes/skills/niu-9router-maintain/scripts/audit_models.py --apply    # baru boleh ubah DB
```
Script ini: fetch `/v1/models` → probe chat tiap model (3 percobaan, 4 worker) → klasifikasi
**ok / transient / permanent** → tulis JSON → (hanya dengan `--apply`) disable provider yang
`ok=0` **dan** `transient=0`.

**Aturan yang tidak boleh dilanggar: satu probe jaringan TIDAK PERNAH cukup untuk mematikan provider.**
Provider yang sedang 429/timeout akan terbaca "0 model OK" dan tampak mati, padahal ia baru saja
melayani trafik produksi. Sebelum men-disable, buktikan dengan `usageHistory`:
```sql
SELECT timestamp, provider, model, status FROM usageHistory
WHERE provider='<nama>' ORDER BY id DESC LIMIT 5;
```
Baris `status='ok'` yang lebih baru dari probe = provider HIDUP; kegagalan probe itu transient.
Nonaktifkan provider hanya kalau `usageHistory` juga menunjukkan kegagalan.

**Kode di balik wrapper 503.** 9router menyarungkan kode upstream asli ke dalam body, jadi 503 luar
sering membawa `[401]` / `[404]` / `[403]` dari provider sebenarnya. Klasifikasikan dari kode
**dalam** — kalau tidak, model yang benar-benar mati dilaporkan sebagai "sedang sibuk" (dan
sebaliknya). Contoh nyata: 50 model `pixz/*` tampak "transient" padahal semuanya `[401]` = kredensial mati.

## Provider Gratis vs Berbayar
9router **tidak punya flag paid/free**. Kriteria: tes akses langsung. Tapi **"0 model OK" ≠ "disable"** —
lihat aturan `usageHistory` di bagian audit di atas.

**Jangan simpan daftar provider hidup/mati di skill ini.** Daftar seperti itu basi dalam hitungan hari
(katalog bergerak 48→77→135 model dalam beberapa pekan) dan langsung menyesatkan sesi berikutnya.
Yang durable adalah **kriterianya**: probe chat 3×, cek `usageHistory`, baru putuskan. Kalau butuh
angka terkini, jalankan audit dan baca JSON-nya — jangan percaya tabel di dokumen mana pun, termasuk ini.
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

**Pitfall:** notifikasi hanya muncul kalau ada DELTA model. Hash sama = silent. Jangan kira script mati kalau tidak ada notif — cek `tail ~/.cache/niumination/9router-sync.log` & `.9router-state.json`.

### Otomasi bisa mati DIAM-DIAM — cara mendeteksinya
Script watcher ini pernah berhenti bekerja 5 hari tanpa satu pun error terlihat. Gejalanya: log cuma
`fetch failed` / `change pending` selamanya, `~/.cache/niumination/9router-models.hash` kosong atau
berisi hash kosong, dan `.9router-state.json` membeku di tanggal lama.

**Deteksi cepat — umur state file vs sekarang:**
```bash
stat -f "%Sm %N" ~/Desktop/Niumination/.9router-state.json   # >1 jam saat katalog berubah = curiga
wc -c ~/.cache/niumination/9router-models.hash               # 0 atau 1 byte = hash tak pernah terisi
grep "change:" ~/.cache/niumination/9router-sync.log | tail  # "hash " kosong = commit cacat
```

**Klasik penyebabnya: `sha256sum` tidak ada di PATH launchd.** Di macOS `sha256sum` hidup di `/sbin`,
sedangkan PATH plist tidak memuat `/sbin`. Dan fallback `cmd_a || cmd_b` **tidak menyelamatkan** kalau
keduanya dirantai dalam pipeline: exit code pipeline diambil dari perintah TERAKHIR (`cut` = 0), jadi
`||` tak pernah jalan. Hasilnya `HASH` kosong → sama dengan `PREV_HASH` kosong → script selalu memilih
cabang "tidak ada perubahan" dan keluar diam, tanpa pernah menulis hash (self-perpetuating).

**Pola benar — cek keberadaan binary, jangan andalkan `||` di dalam pipeline:**
```bash
_hash_ids() {
  if command -v sha256sum >/dev/null 2>&1; then printf '%s' "$IDS" | sha256sum | cut -d' ' -f1
  elif command -v shasum >/dev/null 2>&1; then printf '%s' "$IDS" | shasum -a 256 | cut -d' ' -f1
  else printf '%s' "$IDS" | openssl dgst -sha256 | awk '{print $NF}'; fi
}
HASH=$(_hash_ids)
[ -z "$HASH" ] && { echo "$(date -Iseconds) FATAL: no sha256 tool" >> "$LOG_FILE"; exit 1; }
```
Guard `exit 1` itu penting: gagal **keras** jauh lebih baik daripada sukses palsu yang menyembunyikan
kerusakan berhari-hari.

**Uji di bawah PATH launchd yang sebenarnya, bukan PATH shell Anda.** Script yang lolos dari shell
interaktif bisa tetap rusak di bawah launchd — dan sebaliknya (script ini dulu "kelihatan jalan"
justru karena `up-eco.sh` memanggilnya dari shell yang PATH-nya memuat `/sbin`):
```bash
env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=$HOME /bin/bash ~/Desktop/Niumination/scripts/9router-sync.sh; echo "exit=$?"
```
Lihat `references/launchd-script-hardening.md` untuk pola lengkap + cara membaca `launchctl print`.

**Verify notifikasi jalan:** `osascript -e 'display notification "test" with title "9router sync"'` → harus muncul di Notification Center.

## Pitfalls
- **Jangan matikan provider dari satu probe.** Probe paralel/ber-timeout menghasilkan false-negative;
  provider produksi yang baru saja melayani trafik bisa terbaca "0 OK". Wajib cross-check `usageHistory`
  sebelum `isActive=0`, dan pulihkan (`isActive=1` + restart) begitu ketahuan salah disable.
- **Jangan naikkan worker paralel untuk "mempercepat" audit.** Beban paralel justru menciptakan timeout
  yang terbaca sebagai kematian provider. 4 worker cukup.
- **Channel produksi bergantung pada provider tertentu — cek `channel_overrides` sebelum men-disable apa pun.**
  `hermes config get platforms.telegram.channel_overrides` menunjukkan model+provider tiap thread; mematikan
  provider yang dipakai channel = thread mati. Mematikan `gemini` pernah melumpuhkan channel 1.
- **`/v1/models` yang lebih panjang dari `/v1/models` yang baru dihapus.** Provider `isActive=0` bisa masih
  mengembalikan modelnya di katalog (mis. `muse`), jadi picker tetap menampilkan model yang tidak bisa dipakai.
  Katalog ≠ status provider.
- Jangan matikan `com.9router.autostart` — itu server utama. `com.niumination.9router-watch` boleh mati (cuma cache).
- Model 400 di GitHub Copilot = model tidak ada di free tier, biarkan (provider masih berguna, ada yang OK).
- `big-pickle`/`hy3-free` **tidak ada di 9router** — lewat opencode-zen langsung (cron model).
- 9router pakai `NINE_ROUTER_API_KEY` (env passthrough di config Hermes).
- DB sqlite: `~/.9router/db/data.sqlite` (providerConnections, usageHistory).
- **Katalog 9router FLAPPING.** Diukur 11 Okt 2026: total bergerak `168 ↔ 126` dalam hitungan detik —
  satu provider (pixz, 83 model) keluar-masuk agregat saat upstream-nya error lalu pulih, padahal
  endpoint provider itu sendiri stabil (diuji langsung: 83 konsisten). **Jangan ambil keputusan dari satu
  sampel katalog.** Untuk skrip otomatis, baca 2-3x dengan jeda dan hanya bertindak kalau dua bacaan
  berturut-turut sama; kalau masih bergerak, lewati run itu. Tanpa ini, job periodik akan menulis ulang
  config dan mengirim notifikasi tiap kali katalog bergoyang.
- **Jangan verifikasi dengan fetch ulang katalog setelah menulis.** Pada endpoint yang flapping, bacaan
  kedua bisa berbeda dari yang dipakai menulis dan menggagalkan job yang sebenarnya sehat
  (`config holds 126, expected 168`). Verifikasi byte di disk terhadap snapshot yang **sama**.
- **`--no-agent` memakai interpreter Hermes, tanpa PyYAML.** Skrip cron di `~/.hermes/scripts/` yang
  `import yaml` gagal dengan `ModuleNotFoundError` — bukan terlihat saat diuji manual dengan python3
  sistem. Pakai stdlib saja (`re`, `json`, `urllib`).
- **`models:` di config punya kerabat yang mirip:** ada dua `9router:` di `~/.hermes/config.yaml`
  (`providers.9router` dan `model_catalog.9router`). Parser yang mencari kemunculan pertama bisa menulis
  ke ruang yang salah — verifikasi parent key sebelum replace.
- Probe SSE: model yang balas `data: {...}` bukan "parse error". Parser yang tidak menangani SSE akan
  melaporkan model hidup sebagai gagal — baca respons mentah sebelum memvonis model mati.
- **`max_tokens` < 16 → 400 palsu.** Sebagian model menolak dengan
  `` `max_output_tokens` The number must be `>= 16` ``. Itu payload probe yang salah, bukan model mati —
  `oc-combo-2` pernah divonis "rusak" karena ini, ternyata sehat. Pakai `max_tokens >= 64`.
- **Plist `com.niumination.9router-sync` PATH-nya TIDAK memuat `/sbin`.** Di macOS `sha256sum` ada di
  `/sbin/sha256sum`, di luar PATH launchd. Dan jangan andalkan `|| shasum` di dalam pipeline: exit code
  pipeline diambil dari perintah **terakhir** (`cut` = 0), jadi fallback tidak pernah jalan dan `HASH`
  keluar kosong — yang lalu dibandingkan dengan `PREV_HASH` kosong → skrip selalu memilih cabang "tidak
  ada perubahan" dan diam selamanya. Pakai `command -v` + guard hash kosong (`exit 1`).
- **Cache katalog Hermes menunda efek disable provider.** `~/.hermes/provider_models_cache.json` (TTL 1 jam)
  didahulukan daripada `models:` di config, jadi picker masih menyajikan model provider yang baru dimatikan.
  Hapus entry `custom:http://localhost:20128/v1*` agar picker langsung bersih.
- **`models:` di `providers.<nama>` adalah FALLBACK, bukan pin.** Diverifikasi: saat cache hangat, picker
  tetap memakai hasil cache (141 model, termasuk 50 `pixz/*` yang sudah dimatikan) meski `models:` hanya
  berisi 85. `models:` dipakai saat cache dingin/kosong. Karena itu, setelah mengubah katalog, **invalidate
  cache** — jangan hanya mengedit `models:`.
- **Sinkronisasi models: → config bisa diotomatisasi** dengan `scripts/sync-models-to-config.py` (cron `--no-agent`). Script ini rewrite `models:` dengan parser string murni (tanpa PyYAML), invalidate cache katalog, dan verifikasi ulang dari disk. Uji dulu pada salinan /tmp sebelum deploy — config asli jangan pernah menjadi target uji.
