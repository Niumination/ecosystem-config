# DB_PATH Debug: Empty Kanban Dashboard

## Symptoms
- Browser shows empty kanban board (0 tasks)
- `hermes kanban stats` shows 55 tasks (ready)
- API `/api/tasks` returns empty array

## Root Cause
The Niu-Kanban-Dash `server.js` line 9 was hardcoded to read from the **default profile's** kanban database:

```js
// OLD (wrong — reads default profile, stale since Jun 6)
const DB_PATH = process.env.KANBAN_DB || '/Users/zaryu/.hermes/kanban.db';
```

But all kanban tasks created via `hermes kanban create` (running under the `opencode` profile) go to the **opencode profile's** kanban database:

```
/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db
```

## Fix

```js
// NEW (correct — reads opencode profile's active kanban)
const DB_PATH = process.env.KANBAN_DB || '/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db';
```

Then restart the server:
```bash
kill $(lsof -ti :5199)
cd ~/Desktop/Niumination/projects/niu-kanban-dash && node server.js &
```

## Verification
```bash
curl -s http://127.0.0.1:5199/api/tasks | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d)} tasks'); [print(f'  {t[\"status\"]}: {t[\"title\"]}') for t in d[:3]]"
```

Expected output:
```
55 tasks
  ready: TEDEO 🔴 (P1)
  ready: kune-ya.com 🔴 (P1)
  ready: niu-vermilion (P2)
```

## File structure
- `server.js` — Express server with hardcoded `DB_PATH`
- Kanban DBs are per-profile; each Hermes profile has its own data directory

## Prevention
When setting up a new kanban dashboard or troubleshooting an empty one, ALWAYS check:
1. Which profile is the dashboard serving? (default vs opencode)
2. Where does that profile's Hermes store its kanban data? (check `$HERMES_HOME/../kanban.db`)
3. Does `server.js` hardcode `DB_PATH` to the correct location?
