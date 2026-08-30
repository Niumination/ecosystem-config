---
name: niu-mission-control-ops
description: "Operate the Niu-MissionControl dashboard server (port 5200): Next.js 15 runtime, SQLite backend, health checks, and deployment workflows."
domain: devops
tags: [mission-control, niumination, server, nextjs, dashboard, ops]
version: "2.0"
author: Hermes Agent (Niumination)
last_updated: "2026-08-29"
---

# Niu-MissionControl Ops v2

Operasi server dashboard Mission Control (`services/niu-mission-control/`, Next.js 15 + Python SQLite backend, port **5200**).

## Arsitektur Baru (2026-08-29)

**NEXT.JS + PYTHON BACKEND:**
- **Frontend:** Next.js 15 app di `apex-ui/` (sudah tidak ada, sekarang standalone)
- **Backend API:** Next.js API routes di `app/api/mc/`
- **Database:** Python SQLite manager (`db_manager.py`) dengan database di `data/swarm_state.db`
- **Entry Point:** `npx next start --port 5200`

## Server Lifecycle

**LaunchAgent (Primary):**
- Plist: `~/Library/LaunchAgents/com.niumination.missioncontrol.plist`
- PID: 831 (next-server v15.3.8)
- Status: running
- Log: `brain/ops/mc.stdout.log` / `mc.stderr.log`

**Manual Start:**
```bash
cd /Users/zaryu/Desktop/Niumination/services/niu-mission-control/apex-ui
NODE_ENV=production npx next start --port 5200 --hostname 0.0.0.0
```

**Build:**
```bash
cd /Users/zaryu/Desktop/Niumination/services/niu-mission-control/apex-ui
NODE_ENV=production npx next build
```

## Health Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/mc/health` | GET | Liveness check - returns DB status |
| `/api/mc/agents` | GET | List all agents with stats |
| `/api/mc/tasks` | GET | List tasks grouped by status |
| `/api/mc/tasks` | POST | Create new task |
| `/api/mc/cost` | GET | Cost summary (30 days default) |
| `/api/mc/hermes/status` | GET | Hermes gateway status |
| `/api/mc/hermes/sessions` | GET | Recent Hermes sessions |
| `/api/mc/hermes/skills` | GET | Available skills count |

**Verify:**
```bash
curl -s http://localhost:5200/api/mc/health
# Expected: {"status":"ok","database":"connected","version":"2.0.0",...}
```

## Database

**Location:** `data/swarm_state.db`

**Schema:**
- `agents` - 5 agents (chief, research, programmer, qa, creator)
- `tasks` - Task queue dengan status tracking
- `cost_tracking` - Cost monitoring per model/provider
- `system_logs` - Audit trail

**Manage with Python:**
```bash
cd /Users/zaryu/Desktop/Niumination/services/niu-mission-control
python3 db_manager.py
# Or query directly:
python3 db_manager.py get_agents
python3 db_manager.py get_task_groups
python3 db_manager.py create_task "Title" "agent_id" "priority" "description"
```

## Apex-UI Reference

Folder `apex-ui/` sekarang berisi referensi desain saja (bukan submodule aktif).

**Untuk update referensi:**
```bash
git clone https://github.com/RubenM1990/APEX-UI.git apex-ui-ref
```

## Pitfalls

1. **Database path:** `db_manager.py` menggunakan env var `MC_DB_PATH` atau default ke `data/swarm_state.db`
2. **API routes:** Harus rebuild Next.js setelah edit route.ts
3. **LaunchAgent:** Sudah ter-config dengan KeepAlive, auto-restart on crash
4. **No FastAPI:** Skill lama menyebutkan FastAPI/v3 routers - SUDAH TIDAK BERLAKU
5. **Next.js cache:** Clear `.next` folder jika ada masalah caching

## DoD Verification

1. ✅ Control loop: `launchctl print gui/501/com.niumination.missioncontrol` → state = running
2. ✅ Health check: `curl -s http://localhost:5200/api/mc/health` → `{"status":"ok","database":"connected"}`
3. ✅ Agents real: `curl -s http://localhost:5200/api/mc/agents` → 5 agents dari SQLite
4. ✅ Tasks real: `curl -s http://localhost:5200/api/mc/tasks` → groups dari SQLite
5. ✅ Create task: `POST /api/mc/tasks` → returns task ID
