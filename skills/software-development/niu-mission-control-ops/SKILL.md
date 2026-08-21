---
name: niu-mission-control-ops
description: "Operate the Niu-MissionControl dashboard server (port 5200): start/restart with the correct venv, verify health before reporting, known silent-death causes, runtime data shapes, and test/rebuild workflows. Use whenever MC is down, needs restart, tests fail, or /up-eco reports MC unreachable."
domain: devops
tags: [mission-control, niumination, server, fastapi, dashboard, ops]
version: "1.0"
author: Hermes Agent (Niumination)
---

# Niu-MissionControl Ops

Operasi server dashboard Mission Control (`services/niu-mission-control/`, FastAPI + WebSocket, port **5200**).

## Server lifecycle

**LaunchAgent (2026-08-19, cara resmi sekarang):** MC hidup via `niu.missioncontrol` LaunchAgent dengan `KeepAlive=true` — **auto-restart setelah kill/crash/Mac reboot**. Tidak perlu restart manual per session lagi.
- Plist: `~/Library/LaunchAgents/niu.missioncontrol.plist`. **PENTING:** launchd gui domain user zaryu memindai `/Users/zaryu/Library/LaunchAgents/`, BUKAN sandbox HOME (`/Volumes/HermesAgent/.cache/unix-home/...`) — salin plist ke `/Users/zaryu/Library/LaunchAgents/` dan load via `launchctl bootstrap gui/501 <plist>`.
- **Kritikal: ProgramArguments HARUS pakai venv python, bukan `/usr/bin/python3`** → `venv/bin/python3 server.py`. `/usr/bin/python3` gagal `ModuleNotFoundError: pythonjsonlogger` (dep hanya di venv). Ini bug nyata yang sudah diperbaiki 19 Ags.
- Restart setelah edit server.py: `launchctl kickstart -k gui/501/niu.missioncontrol` (bukan kill manual).
- Status: `launchctl print gui/501/niu.missioncontrol` (state = running, pid).
- Log: `brain/ops/mc.stdout.log` / `mc.stderr.log`.
- **DoD test (control loop):** `kill -9 $(pgrep -f "mission-control/server.py")` → tunggu ~6s → PID baru otomatis + `/healthz` 200. Terbukti lulus.
- Companion: `niu.healthprobe` LaunchAgent (`scripts/niu-health-probe.py --loop --interval 120 --heal`) — merekam MC/9router/zen/gateway/skills/canary tiap 120s ke `brain/ops/probe.stdout.log`, tanpa LLM.

**Health endpoints (sejak 19 Ags):** `/healthz` (liveness), `/readyz` (readiness + DB, 503 jika DB down), `/version`. Tambah di `server.py` (root path, tanpa auth).

**Start v3 (manual fallback):** `cd /Users/zaryu/Desktop/Niumination/services/niu-mission-control/backend && /Users/zaryu/Desktop/Niumination/services/niu-mission-control/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 5200` (background). v3 serve dashboard + 17 API endpoints + WebSocket.
- **Start v2 (fallback):** `cd /Users/zaryu/Desktop/Niumination/services/niu-mission-control && venv/bin/python server.py` (background). BUKAN `python3` polos — bisa salah interpreter.
- **Verify setelah start:** tunggu ~4s, lalu `curl -s -o /dev/null -w "%{http_code}" http://localhost:5200/health` → harus 200. Jangan lapor "hidup" sebelum curl sukses.
- **Silent death (penyebab #1):** server mati TANPA error saat proses induknya terbunuh — session compaction/restart Hermes, proses background di-kill, dsb. `ps aux | grep server.py` bisa kosong tanpa jejak crash. Gejala: dashboard blank di browser, /up-eco lapor "MC tidak merespon".
- **_get_home pitfall:** `modules/skill_monitor.py` `_get_home()` HARUS cek `Desktop/Niumination/skills/` (bukan cuma `Desktop/Niumination/`) — Hermes HOME cache punya folder kosong yang membingungkan resolusi, mengakibatkan 43 conflicts palsu.
- **Restart sequence:** kill PID lama kalau ada → start ulang (venv) → sleep 4 → curl health 200 → cek `/api/mc/skills/stats` 200 → baru klaim.

## Orchestrator MVP — `/api/mc/delegate` (F5, 20 Ags 2026)

**Endpoint:** `POST /api/mc/delegate` body `{"agent": "research|programmer|qa|creator|chief", "instruction": "...", "parent_id": null}` → buat task di swarm_state.db lalu kirim instruksi ke Telegram topic per-agent (802=research, 803=programmer, 804=qa, 1172=creator, 1=chief).

**REQUIRED env di plist launchd (tanpa ini delegate GAGAL):**
```
HERMES_TELEGRAM_CHAT_ID=-1004204696417   # chat id NYATA — jangan biarkan placeholder "-REDACTED_CHAT_ID"
HERMES_HOME=/Volumes/HermesAgent/HermesAgentUSB/data
```
- **Gejala env salah:** `{"task_id":"...","status":"failed","bridge":{"status":"error","message":"hermes send: Could not resolve '-REDACTED_CHAT_ID:802' on telegram..."}}` — chat ID default di `modules/hermes_bridge.py` adalah placeholder, env wajib override di plist.
- **Sukses:** `{"task_id":"...","status":"dispatched","bridge":{"status":"sent","persona":"research","topic_id":"802","simulated":false}}`. `simulated:true` berarti CLI tidak ditemukan — pesan tidak benar-benar terkirim.
- **Fix env:** `plutil -replace EnvironmentVariables -json '...' /Users/zaryu/Library/LaunchAgents/niu.missioncontrol.plist` lalu `launchctl bootout gui/501/niu.missioncontrol` + `launchctl bootstrap gui/501 ...`.
- **Task list:** `/api/mc/tasks` → DICT kolom `{pending, running, completed, failed}` (bukan array!). `bus.get_tasks()` memuat riwayat task lama — 47 task `running` stale bisa menumpuk di DB, bukan error.
- **Membersihkan task stale (dieksekusi 20 Ags 2026):** task `running` yang tidak pernah update (updated_at berhari-hari) = stale dari pra-rekonstruksi, bukan task hidup. Arkib → `failed` dengan alasan (JANGAN dihapus — jaga history):
  ```sql
  -- via venv/bin/python3, sqlite3 data/swarm_state.db
  UPDATE tasks SET status='failed', updated_at=?, result=?
  WHERE status='running' AND updated_at < '2026-08-18 00:00:00';
  -- result = json {"stale": true, "reason": "arked <tanggal>: stale task, tidak ada agent yang memperbarui"}
  ```
  Setelah itu `SELECT status, COUNT(*) FROM tasks GROUP BY status` → harus 0 `running`. Tabel `tasks` kolom: task_id, parent_id, assigned_agent, status, payload, result, created_at, updated_at (bukan `agent`).
- **Fail-closed bagus:** kalau bridge gagal, task ditandai `failed` — MC TIDAK mengarang status sukses. Jangan "rapikan" jadi sukses; itu sudah perilaku yang benar.

## Frontend page fixes — Cost & Telegram feed (20 Ags 2026)

**Pelajaran kelas:** halaman dashboard kosong ≠ selalu frontend; audisi DULU backend (endpoint + DB) sebelum menyalahkan JS. Kasus ini punya AKAR GANDA (backend kosong DAN fungsi frontend hilang) — dua-duanya harus dicek.

### Telegram feed kosong → chat-id placeholder HARDCODED di file KEDUA

**Gejala:** `/api/mc/telegram-feed` balas `{"messages":[],"count":0,"source":"hermes_state_db","gateway":{"group_chat_id":"-REDACTED_CHAT_ID",...}}` — frontend render "No Telegram messages yet" meski `state.db` punya pesan.

**Reality:** chat-id placeholder `"-REDACTED_CHAT_ID"` hardcoded di **DUA file berbeda**:
1. `modules/hermes_bridge.py` (sudah terdokumentasi di Orchestrator MVP section)
2. `modules/gateway_log_parser.py` — `TG_GROUP_CHAT_ID = "-REDACTED_CHAT_ID"` (~line 38) dipakai query `WHERE s.chat_id = ?` → 0 hasil karena id palsu.

**Fix (parser):** baca dari env dengan default chat asli:
```python
TG_GROUP_CHAT_ID = os.environ.get("HERMES_TELEGRAM_CHAT_ID", "-1004204696417")
```
Restart MC (`launchctl kickstart -k gui/501/niu.missioncontrol`) → `curl "http://127.0.0.1:5200/api/mc/telegram-feed?limit=5"` → harus `count > 0`. Terverifikasi: 9 pesan topic=1 (GENERAL) ter-render setelah fix. Test parser tanpa restart: `HERMES_TELEGRAM_CHAT_ID=-1004204696417 venv/bin/python3 -c "from modules.gateway_log_parser import parse_telegram_feed; print(len(parse_telegram_feed(limit=5)))"`.

**Aturan:** kalau `-REDACTED_CHAT_ID` muncul, GREP SEMUA file modules/ (`grep -rn "REDACTED" modules/`) — bukan hanya hermes_bridge.py. Placeholder bisa hardcoded di beberapa tempat.

### Cost page kosong → AKAR GANDA: cost_tracking 0 rows + loadCostData tidak pernah ada

**Gejala:** page-cost tampil KPI `$0.00` / `0` terus; `/api/mc/cost/agents` balas `{"agents":{},"total_cost":0.0,...}`.

**Akar 1 (backend):** tabel `cost_tracking` di `data/swarm_state.db` = **0 rows** (belum pernah ada pencatatan cost di MC). State machine mencatat hanya kalau `record_usage` dipanggil — jarang di MC sendiri.

**Akar 2 (frontend):** `index.html` punya `onclick="loadCostData()"` + elemen KPI (`costTotalCost`, `costAgentGrid`, dll) TAPI **`loadCostData` TIDAK PERNAH DIDEFINISIKAN di app.js** → `loadCostData is not defined` di console, halaman selamanya kosong. (Separuh halaman dashboard diindex.html yang memang belum pernah diimplementasi JS-nya.)

**Fix backend — fallback sumber data dari Hermes state.db (reusable pattern):**
Di `swarm/bus.py` `get_agent_costs()`: jika query `cost_tracking` kosong, aggregate dari `state.db` → tabel **`session_model_usage`** (761 rows, sumber usage gateway 20 Ags 2026):
- Kolom: `session_id, model, billing_provider, billing_base_url, billing_mode, task, api_call_count, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, cost_status, cost_source, first_seen, last_seen`
- Query fallback (cutoff `last_seen > now - days`, GROUP BY `billing_provider, model`): total input/output/cost + COUNT → 47 rows, 12 provider-agent (opencode-zen, huancheng, opencode, nous, custom, 9router...), ~113M tokens total.
- Cek ketersediaan: `venv/bin/python3 -c "import sqlite3; print(sqlite3.connect('file:/Volumes/HermesAgent/HermesAgentUSB/data/state.db?mode=ro', uri=True).execute('SELECT COUNT(*) FROM session_model_usage').fetchone())"`.

**Fix frontend:** tambahkan `loadCostData()` + `renderCostData()` di `dashboard/app.js` (fetch `/api/mc/cost/agents?days=<period>`, render KPI + agent grid + model grid + recent list), dan panggil di init: `loadCostData();` di blok Initialize App.

### Deploy page kosong/stale → `loadDeployStatus` hanya update KPI, grid JADI STATIC (P2, 20 Ags 2026)

**Gejala:** Deploy page tampil 2 kartu hardcoded terus (`Niu-Vermilion`, `Pemdi Aceh Tengah`); `/api/mc/deploy/status` balas `{"projects":[...],"total":2,"success":2}` (backend SEHAT). Console TIDAK ada error — fungsi ada tapi separuh jalan.

**Akar:** `loadDeployStatus()` di app.js hanya set 2 KPI (`deployLiveCount`, `deployLastTime`) — **tidak pernah render ke `#deployProjectGrid`** yang di index.html masih placeholder static. Pola yang sama persis dengan Cost page: HTML punya elemen + onclick, JS ada tapi tidak menyentuh kontainer utama.

**Fix (app.js):** di `loadDeployStatus()` render grid dinamis dari `data.projects`:
- map → card `agent-card-premium`: name + badge, branch, env, URL (strip `https://`), status badge (`success`/`live` → `state-executing` label LIVE, else `state-error`), tombol `triggerDeploy('...')` (escape `'`).
- Panggil `loadDeployStatus();` di init (blok Initialize App).
- **Wajib cache-bust berikutnya:** naikkan `?v=` di index.html + `launchctl kickstart -k gui/501/niu.missioncontrol` + verifikasi `typeof loadDeployStatus === "function"` di browser.

**Aturan kelas:** kalau halaman dashboard tampil placeholder static padahal backend API balas bagus, cek apakah JS render ke kontainer utama ATAU cuma update KPI/elemen samping. `grep` handler function dan lihat `getElementById(<grid-id>)` tersentuh atau tidak.

### ⚠️ Vision TIDAK melihat halaman yang baru di-switch — ORB iframe selalu di layer atas (P2)

**Symptom:** setelah `browser_vision` FIXED (bukan lagi 503), verifikasi halaman COST/SWARM via `browser_vision` tetap menampilkan **dashboard utama (ORB 3D)**, bukan halaman yang baru saja tampil lewat `document.querySelectorAll('.page').forEach(p=>p.style.display='none')`. Vision menyimpulkan "halaman tidak ter-render / pilih navigasi COST" — itu SALAH.

**Reality:** dashboard unified = ORB iframe (`orb.html`, fullscreen) yang HIDUP TERUS di layer atas + `#pageVault` sections tersembunyi. Menampilkan `.page` via JS TIDAK memindahkan layer ORB; `browser_vision` menangkap viewport penuh → yang terlihat ya ORB. **Satu frame vision ≠ bukti halaman kosong.**

**Aturan:** untuk halaman flat (COST, DEPLOY, SWARM, TELEGRAM), **DOM count adalah bukti otoritatif** — cek `costAgentGrid.children.length`, `deployProjectGrid.children.length`, `tgFeed.children.length` setelah fetch, BUKAN `browser_vision`. Vision dipakai untuk verifikasi layout global/ORB saja. Kalau vision lapor "bukan halaman X", bandingkan DOM dulu — jangan percaya vision bahwa halaman kosong (P2: SWARM sempat dinilai "data tipis" padahal DOM menunjukkan 6 topo nodes + prompt editor + fetch agents OK).

### Skill Market page kosong → `loadMarket` hanya panggil `filterMarket` (P3, 20 Ags 2026)

**Gejala:** page-skills-market tampil 4 kartu hardcoded terus (ponytail-core, ultrathink, systematic-debugging, project-orientation) walau `/api/mc/skills` balas 47 skill real. Tombol Refresh (`onclick="loadMarket()"`) tidak mengubah apa pun.

**Akar:** `loadMarket()` di app.js hanya `filterMarket()` — dan `filterMarket()` hanya filter elemen DOM statis (`#marketGrid .agent-card-premium`). Sama persis pola Cost/Deploy: HTML punya onclick + kontainer, JS ada tapi tidak pernah render dari API.

**Fix (app.js):**
1. `loadMarket()`: `Promise.all([fetch('/api/mc/skills'), fetch('/api/mc/skills/stats')])` → render `marketGrid` dinamis (name, domain badge, ACTIVE badge, load count, stats total/this_week → dari `session_model_usage`/skill_monitor), simpan `window.__marketSkills` + `window.__marketStats`.
2. `filterMarket()`: jika `__marketSkills` terisi → filter array & re-render (bukan filter DOM statis); fallback ke perilaku lama kalau data API belum ada.
3. Panggil `loadMarket();` di init (blok Initialize App).
4. Cache-bust: naikkan `?v=` di index.html + `launchctl kickstart -k gui/501/niu.missioncontrol` + verifikasi `typeof loadMarket === "function"`.

**Verifikasi:** `filterMarket` dengan input "hermes" → 3 kartu, reset → 47 kartu. `marketGrid.children.length` = 47 (DOM otoritatif, vision lihat ORB — lihat section Vision).

**Pelajaran kelas (P1-P3):** pola berulang di dashboard ini — halaman "kosong/stale" = HTML punya `onclick` + kontainer TAPI fungsi JS hanya update elemen samping (KPI), bukan kontainer utama. Audit langkah: (1) backend API balas? (2) `typeof <fn>` di browser? (3) `grep getElementById(<grid>)` di app.js — kontainer utama tersentuh atau tidak?

### ⚠️ Cache-busting WAJIB setelah edit file dashboard

**Gejala:** sudah edit `dashboard/app.js` + verifikasi `grep` file benar di disk, tapi browser masih `typeof loadCostData === "undefined"`. Server serve file LAMA.

**Reality:** `dashboard/index.html` memuat `<script src="/static/app.js">` TANPA query version → browser meng-cache app.js. FastAPI `StaticFiles` serve disk file (cek `fetch('/static/app.js?v='+Date.now())` → `hasCost: true` = file baru sampai server), tapi HTML yang dirender browser tetap referensi app.js lama.

**Fix:**
1. `index.html`: `<script src="/static/app.js?v=20260820-1">` (version query — naikkan tiap edit).
2. Restart MC: `launchctl kickstart -k gui/501/niu.missioncontrol` (cache HTML juga).
3. Verifikasi function benar-benar ter-load di browser: `typeof loadCostData` → `"function"` (bukan cuma cek file di disk).

### Verifikasi page terisi via DOM (tanpa vision)

Kalau vision/auxiliary down atau mau bukti cepat: switch page via console lalu baca elemen data:
```js
const cost = document.getElementById('page-cost');
document.querySelectorAll('.page').forEach(p=>p.style.display='none'); cost.style.display='block';
loadCostData();
// lalu: costTotalTokens.textContent, costAgentGrid.children.length, costModelGrid.children.length
```
DOM terisi (KPI 113,965,875 tokens + 12 agent cards + 12 model + 20 recent) = terbukti, sebelum screenshot/vision.

## DoD verifikasi + storage cleanup quick-wins (20 Ags 2026)

**DoD 4 kondisi hijau — perintah verifikasi cepat:**
1. Control loop: `launchctl print gui/501/niu.missioncontrol` (state=running + pid) + `launchctl print gui/501/niu.healthprobe` + `curl -s http://127.0.0.1:5200/healthz`
2. Fail-closed: `hermes fallback ls` (Primary nemotron-3-ultra-free, chain se-provider free tier Zen) + cron `c6ec80ed633f` `Last run: ... ok`
3. Skill plane: `find skills -name SKILL.md | wc -l` = 68 bank; AGENTS.md ≤ 2KB
4. Token tax: grep compression config (threshold 0.5) + `hermes plugins list | grep rtk` (enabled)

**Storage hygiene (aman, tanpa LLM):**
- **mcp-stderr.log noise:** backup lalu **truncate** (`: > <file>`), bukan hapus — log roller butuh filenya: `cp log /tmp/...pre-clean.log && : > log`
- **LSP node_modules prune (pola reusable):** config LSP hanya mengaktifkan typescript, tapi node_modules berisi semua server language (pyright 201MB, yaml 38MB, bash 6MB, dockerfile). Cek `package.json` deps → hapus yang TIDAK direferensikan config (`lsp:` section), **TAR backup dulu**, lalu test binary inti tetap jalan: `./node_modules/.bin/typescript-language-server --version` → harus output versi. Hasil: 409MB → 162MB.
- **state.db di ExFAT = risiko korupsi:** backup rutin ke APFS internal: `cp <usb>/data/state.db /Users/zaryu/Backups/hermes-state/state.db.<tanggal>.bak` lalu **verifikasi SHA**: `shasum -a 256 <asli> == shasum -a 256 <backup>` (diff) — baru klaim valid.
- **Catatan WAL:** jika `state.db-wal` ada, `cp` snapshot bisa nonsinkron — backup berikutnya ideal pakai `sqlite3 .backup` (checkpointed). Untuk snapshot cepat, cp + verify tetap OK.

Detail transcript: `references/quick-wins-cleanup-2026-08-20.md`.

## Integrasi /up-eco

- `/up-eco` lapor "⚠️ Mission Control server tidak merespon di port 5200" → JANGAN langsung percaya; verifikasi `curl -s -o /dev/null -w "%{http_code}" http://localhost:5200/health` (000/refused = benar mati, 200 = false positive / timeout scan).
- Setelah restart: **re-run `up-eco.sh`** — lapor selesai hanya jika run kedua menunjukkan rekomendasi kosong ("tidak ada rekomendasi"). Run pertama = deteksi, run kedua = bukti fix.
- Catatan: skill `up-eco` (Bank Pusat-synced, created_by=None) tak bisa di-patch oleh agent — pelajaran MC ops hidup di skill ini.

## Runtime data shapes (dashboard)

- `/ws/swarm` kirim `agents` sebagai **DICT** `{agent_id: status_string}`; REST `/api/mc/agents` kirim **array**. `renderAgents()` di app.js sudah normalisasi (Object.entries + AGENT_META mirror `swarm/agents.py`). Kalau JS crash `Cannot read properties of undefined (reading 'toUpperCase')` → shape mismatch lagi, cek payload WS.
- Gateway status: `/api/mc/hermes` → `{gateway: {online, simulated, pid}}`. Poll dashboard tampak OFFLINE 2-3 detik pertama (belum settle) — tunggu ~2s lalu re-baca, atau verifikasi langsung via curl.
- Thread/session state: `data/dispatches.json` + `modules/dispatch_store.py` (THREAD_NAMES/THREAD_SESSIONS) + kanban.db — TIDAK tersinkron satu sama lain; cek semuanya sebelum menyimpulkan (lihat delegated-output-verification).

## v3.0 Architecture (2026-08-17)

Entry point v3: `uvicorn app.main:app` dari `backend/`. Entry point v2 (fallback): `server.py`. Backend v3 di `backend/`:
- `backend/app/main.py` — app factory (`create_app()`)
- `backend/app/core/` — config (pydantic-settings), middleware (auth+ratelimit), logging (JSON + correlation ID)
- `backend/app/routers/` — 12 domain routers (system, tasks, agents, ecosystem, terminal, telegram, artifacts, config, skills, cost, deploy, ws)
- `backend/app/services/` — state_machine (TaskStatus enum + transitions), dispatcher (SQLite queue: submit/claim/ack/nack), agent_adapter (HermesAdapter + MockAdapter), approval (dangerous action gate), cost_tracker, ws_hub (rooms + replay), metrics (counters/gauges/histograms)
- `backend/app/db/` — aiosqlite + WAL + schema (tasks, events, dispatches, audit, cost tables)
- `backend/run.py` — entry point v3

**Keamanan v3:**
- Auth: exact match paths (bukan startswith bebas) — `/api/*` selalu minta auth
- Terminal: `shell=False` + `shlex.split`, allowlist read-only (python/cat dihapus dari allowlist)
- `.env` via pydantic-settings (config wajib dari env vars, bukan hardcoded)

**State machine:**
- TaskStatus: queued → delegated → running → review → done/failed/cancelled
- Transisi divalidasi + persist di DB + emit event + audit trail
- Dispatcher: SQLite-backed queue, claim/execute/ack/nack pattern

**Test baseline:** `venv/bin/pytest backend/tests/ tests/ -q` → 55 passed (44 lama + 11 v3). Dashboard rebuild tetap pakai `build_unified.py` — f-string escaping `{{ }}`依然penting.

## Test & rebuild

- **Tes:** `venv/bin/pytest backend/tests/ tests/ -q` → baseline **55 passed** (44 lama + 11 v3). Jangan claim hijau tanpa menjalankan.
- **Cost & Telegram page fixes (20 Ags 2026):** full transcript, SQL fallback, cache-busting detail → `references/cost-telegram-p1-fix-2026-08-20.md`.
- **Deploy page fix (P2, 20 Ags 2026):** template kartu proyek + verifikasi DOM → `references/deploy-p2-fix-2026-08-20.md`.
- **Dashboard rebuild** (refactor gutted / layout ulang): ikuti playbook `delegated-output-verification` → `references/rebuild-gutted-dashboard.md` — builder `dashboard/build_unified.py`, f-string escaping `{{ }}`, elemen JS-referenced wajib di DOM, verifikasi browser objektif (console zero errors, `new Function()` parse, route curl 200).

## Migration from v2 → v3

**Script:** `backend/scripts/migrate_data.py`
- Dry-run: `python3 backend/scripts/migrate_data.py --dry-run`
- Migrasi: `python3 backend/scripts/migrate_data.py` (backup otomatis ke `*.v2_backup_*.db`)
- Migrates: `data/dispatches.json` → dispatches table, `data/swarm_config.json` → config table
- Cutover checklist: `docs/CUTOVER_CHECKLIST.md`
- Rollback: stop v3 → `git checkout HEAD~6` → start v2 (`server.py`)

**git filter-repo — purge sensitive data:**
- Gunakan untuk hapus chat ID, secrets dari git history
- **WAJIB backup dulu:** `cp -r .git .git.backup.$(date +%Y%m%d)`
- Install: `pip3 install --break-system-packages git-filter-repo`
- Replace text: `git filter-repo --replace-text <(echo "PATTERN==>REDACTED") --force`
- Hapus file dari history: `git filter-repo --invert-paths --path data/file.json --force`
- Setelah filter-repo: remote hilang → `git remote add origin <url>` → `git push --force origin main`
- Semua collaborator harus `git pull --rebase` atau clone ulang

## Pitfalls

- **Startup crash: missing venv deps (e.g. `ModuleNotFoundError: No module named 'pydantic_settings'`).** The system Python may not have project deps installed. Always start via the project venv, not bare `python3`/`uvicorn`. Verified command: `cd services/niu-mission-control/backend && /Users/zaryu/Desktop/Niumination/services/niu-mission-control/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 5200`.
- **Health check after restart:** `curl -s -o /dev/null -w "%{http_code}" http://localhost:5200/health` must return `200` before reporting MC alive. Do not rely on browser alone; server can appear started while still crashing on first request.
- `lsof -i :5200 -P | grep LISTEN` → kalau kosong = benar mati (curl 000 konfirmasi).
- Browser console buffer lama menumpuk → `clear` dulu sebelum menilai error baru.
- `git add -A` di repo MC ikut men-stage folder backup vendored (ribuan file fontawesome) — `.gitignore` + stage file spesifik (lihat delegated-output-verification).
- Background server via Hermes `terminal(background=true)` mati saat session berakhir — **sudah digantikan LaunchAgent `niu.missioncontrol` (KeepAlive) sejak 19 Ags 2026**; pakai `launchctl kickstart -k gui/501/niu.missioncontrol` untuk restart, bukan background terminal.
- **Mac restart = otomatis hidup** sejak LaunchAgent terpasang (RunAtLoad + KeepAlive). Tetap verifikasi dengan `curl http://localhost:5200/healthz` sebelum klaim aktif — jangan asumsi.
