# Architecture Migration: FastAPI → Next.js — 29 Ags 2026

## Context
Session audit Mission Control (port 5200) mengungkap pergeseran arsitektur besar: backend Python FastAPI (v2/v3) digantikan Next.js 15.3.8 app di `apex-ui/`. Skill `niu-mission-control-ops` yang ada masih mendokumentasikan stack lama — perlu patch untuk refleksi realita baru.

## Evidence
```bash
$ lsof -i :5200 -P
COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
node    831 zaryu  12u IPv6 ... TCP *:5200 (LISTEN)

$ ps -p 831 -o pid,ppid,command
  831     1 next-server (v15.3.8)

$ launchctl print gui/501/niu.missioncontrol
Bad request. Could not find service "niu.missioncontrol" in domain for user gui: 501

$ ls ~/Library/LaunchAgents/niu.*
ls: /Users/zaryu/Library/LaunchAgents/niu.*: No such file or directory
```

## New structure
```
services/niu-mission-control/
├── apex-ui/                    # ← NEW: Next.js 15.3.8 app
│   ├── app/
│   │   ├── api/mc/            # API routes (Next.js Route Handlers)
│   │   │   ├── agents/route.ts
│   │   │   ├── tasks/route.ts
│   │   │   ├── cost/
│   │   │   ├── hermes/
│   │   │   ├── logs/
│   │   │   ├── system/
│   │   │   ├── telegram/
│   │   │   └── ws/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   ├── next.config.mjs
│   ├── package.json            # next@15.3.8, react@19, three, @react-three/fiber
│   └── node_modules/
├── server.py                   # ← OLD: FastAPI v2 (tidak digunakan)
├── dashboard/                  # ← OLD: vanilla frontend (tidak digunakan)
└── docs/
```

## API endpoints (real)
| Route | Status | Source |
|---|---|---|
| `GET /` | ✅ 200 | Next.js page (ORB + dashboard) |
| `GET /api/mc/agents` | ✅ 200 | Hardcoded array di `route.ts` |
| `GET /api/mc/tasks` | ✅ 200 | Sample data statis |
| `GET /api/mc/healthz` | ❌ 404 | Tidak ada di Next.js |
| `GET /api/mc/telegram-feed` | ❌ 404 | Tidak ada route handler |
| `GET /api/mc/ecosystem` | ❌ 404 | Tidak ada route handler |

## Health probe status
Probe (`niu.healthprobe` atau script manual) masih catat MC sebagai UP:
```
[MC] HTTP 200 in 0.00s
```
Ini karena probe hanya cek HTTP status code, tidak validasi endpoint spesifik. MC "up" tapi health endpoints hilang.

## Gaps & TODO
1. **No LaunchAgent** — MC tidak auto-restart setelah kill/reboot. Perlu buat plist baru.
2. **Static data** — API routes return hardcoded arrays, belum connect ke SQLite/Hermes state.db.
3. **Missing endpoints** — `/healthz`, `/readyz`, `/version`, `/api/mc/telegram-feed`, `/api/mc/ecosystem` tidak ada.
4. **Skill docs outdated** — `niu-mission-control-ops` SKILL.md penuh referensi FastAPI/v2/v3 yang sudah tidak relevan.

## Files examined
- `/Users/zaryu/Desktop/Niumination/services/niu-mission-control/apex-ui/package.json`
- `/Users/zaryu/Desktop/Niumination/services/niu-mission-control/apex-ui/app/api/mc/agents/route.ts`
- `/Users/zaryu/Desktop/Niumination/services/niu-mission-control/apex-ui/next.config.mjs`
- `/Users/zaryu/Desktop/Niumination/brain/ops/probe.stdout.log` (tail)
