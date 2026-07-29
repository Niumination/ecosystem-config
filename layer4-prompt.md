# Layer 4 — Mission-Control Dashboard: Skill Monitoring

> ✅ **COMPLETED — 29 Jul 2026** oleh Jcode. Lihat `services/niu-mission-control/modules/skill_monitor.py` dan dashboard tab "Skill Monitor".

## Goal
Bangun dashboard monitoring skill ecosystem di Mission-Control yang sudah ada (`services/niu-mission-control/`).

## Context
Ini adalah layer terakhir dari arsitektur 4 layer bank skill terpusat Niumination. Layers 1-3 sudah selesai:
- Layer 1: Bank skill pusat di `~/Desktop/Niumination/skills/` (8 SKILL.md terisi)
- Layer 2: Sync script `skills/sync-to-agents.sh` (auto-copy ke Jcode/Hermes, cron every 6h)
- Layer 3: DOX Injection Engine di AGENTS.md (auto-loaded skills via trigger keyword)
- **Layer 4 (sekarang):** Dashboard live monitoring

## What Already Exists
1. **`services/niu-mission-control/`** — FastAPI + WebSocket server (already built, running)
2. **`scripts/hooks/`** — 12 Orca hook scripts that send telemetry on agent session start/stop
3. **Ref guide:** `docs/skill-ecosystem-guide.md` (1000 baris, complete ecosystem documentation)
4. **AGENTS.md** — v4.3 with DOX injection section (baris 155-228)
5. **`skills/INDEX.md`** — catalog of all 8 active skills
6. **`scripts/eco-collect.py`** — existing data collection script (bisa diperluas)

## What Layer 4 Needs

### Core Dashboard (halaman baru di niu-mission-control)
1. **Skill Activity Feed** — skill apa yang di-load hari ini, dari agent mana (Hermes/Jcode)
2. **Usage Stats** — frekuensi penggunaan per skill (daily, weekly, monthly)
3. **Stale Detection** — skill yang 30+ hari tidak dipakai → marked stale
4. **Trigger Match Log** — trigger keyword apa yang paling sering cocok dengan task
5. **Live status** — WebSocket real-time update ketika skill di-load

### Integration Points
1. **Orca hooks** — `scripts/hooks/` sudah kirim telemetry session start/stop. Perlu ditambah payload skill usage.
2. **sync-to-agents.sh** — sudah sync tiap 6 jam. Bisa tambah logging skill yang di-copy.
3. **AGENTS.md DOX injection** — trigger keyword section (sudah ada, tinggal di-track match-nya)

### Tech Stack (ikuti existing mission-control)
- FastAPI backend (existing — tinggal tambah routes)
- WebSocket (existing — tinggal tambah event types)
- SQLite / JSON log file (keep it simple)
- Frontend: ikuti gaya existing dashboard (Vite + React atau HTML vanilla)

## Constraints
- ✅ **Non-destructive** — jangan ubah AGENTS.md (sudah fix di v4.3)
- ✅ **Evolusioner** — extend yang existing, bukan rewrite
- ✅ **Keep it simple** — monitoring dashboard, bukan data warehouse
- ⚠️ **Orca hooks adalah sumber data utama** — hindari bikin mekanisme baru kalau Orca sudah cukup

## File References
- `docs/skill-ecosystem-guide.md` — complete guide (baca dulu untuk konteks penuh)
- `scripts/hooks/` — 12 hook files (coba extend salah satu untuk test)
- `services/niu-mission-control/` — existing FastAPI + WebSocket server
- `skills/INDEX.md` — skill catalog yang harus di-track
- `AGENTS.md` — DOX injection section (trigger keywords per skill)

## Output Target
- Extended niu-mission-control dengan endpoint skill monitoring
- Frontend dashboard page accessible via browser
- Integrasi dengan minimal 1 Orca hook
- Log format yang bisa diparse untuk data analytics
- Update INDEX.md + referensi di guide setelah selesai
