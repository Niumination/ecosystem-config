# Mission Control Bridge Migration — Session Reference (2026-09-07)

## Context
Mission Control (`services/niu-mission-control/`) was refactored from a Python FastAPI + Next.js hybrid to a pure Next.js app (`apex-ui/`) at commit `7044e8f`. This refactor deleted critical bridge modules:
- `modules/hermes_bridge.py` — Telegram send, terminal, agent turn
- `swarm/agents.py` — Agent config
- `swarm/bus.py` — Message bus
- `swarm/worker.py` — Worker management
- `modules/skill_monitor.py` — Skill usage tracking

## Root Cause
`server.py` (FastAPI) imported `swarm.agents`, `swarm.bus`, `swarm.worker`, and `modules.skill_monitor`. After refactor, only `apex-ui/` (Next.js) remained. No equivalent bridge existed.

## Recovery Steps Taken

### 1. Diagnose
```bash
cd services/niu-mission-control
python3 server.py
# ModuleNotFoundError: No module named 'swarm'
```

### 2. Recover from git history
```bash
git log --all --oneline -- modules/hermes_bridge.py | head -5
# 7044e8f feat: migrate to apex-ui (Next.js)

git show 7044e8f^:modules/hermes_bridge.py > /tmp/original_bridge.py
```

### 3. Reimplement in TypeScript
Created `apex-ui/lib/bridge.ts`:
- `sendChat(text, topicId)` — uses `hermes send -t telegram:<chat>:<topic>`
- `runTerminal(cmd, timeout)` — allowlist-only: `ls`, `pwd`, `echo`, `grep`, `find`, `head`, `tail`, `ps`, `wc`, `date`, `uptime`, `df`, `du`, `whoami`, `env`
- `runAgentTurn(prompt, sessionId, model, provider, timeout)` — uses `hermes -z --resume`

### 4. Add supporting DB schema
```sql
-- data/init.sql
CREATE TABLE IF NOT EXISTS dispatches (
    id TEXT PRIMARY KEY,
    target_topic TEXT NOT NULL,
    message TEXT NOT NULL,
    source_agent TEXT DEFAULT 'general',
    status TEXT DEFAULT 'pending',
    error TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Add DB queries to `db_manager.py`
- `add_dispatch(target_topic, message, source_agent)` → returns record dict
- `update_dispatch_status(dispatch_id, status, error)` → returns bool
- `get_dispatches(limit)` → returns list of dicts

### 6. Add API routes (Next.js App Router)
- `POST /api/mc/dispatch` — create dispatch, validate target ∈ {1, 802, 803, 804, 1172}
- `GET /api/mc/dispatches` — list recent dispatches
- `POST /api/mc/telegram/send` — send message via `hermes send` CLI
- `POST /api/mc/tasks/update` — update task status

### 7. Verify
```bash
npx next build
# ✓ Compiled successfully, 11 routes

curl -s http://localhost:5200/api/mc/health
# {"status":"ok","database":"connected","version":"2.0.0"}

curl -s -X POST http://localhost:5200/api/mc/dispatch \
  -H "Content-Type: application/json" \
  -d '{"to":"803","message":"test","source":"general"}'
# {"id":"d...","status":"pending","target":"803",...}

curl -s http://localhost:5200/api/mc/dispatches
# {"dispatches":[{"id":"d...","status":"pending",...}]}
```

## Key Environment Values
| Value | Location |
|-------|----------|
| `HERMES_CLI` | `/Users/zaryu/src/hermes-agent/.venv/bin/hermes` |
| `TELEGRAM_CHAT_ID` | `-1004204696417` (Niu-MissionControl group) |
| `DB_PATH` | `/Users/zaryu/Desktop/Niumination/services/niu-mission-control/data/swarm_state.db` |
| `DB_MANAGER` | `/Users/zaryu/Desktop/Niumination/services/niu-mission-control/db_manager.py` |

## Topic Mapping
| Topic ID | Agent | Purpose |
|----------|-------|---------|
| `1` | chief/general | General orchestration |
| `802` | research | Research agent |
| `803` | programmer | Coding agent |
| `804` | qa | QA/audit agent |
| `1172` | creator | Content creation |
