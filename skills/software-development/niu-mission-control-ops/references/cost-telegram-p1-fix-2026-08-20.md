# Cost & Telegram Feed P1 fix — 20 Ags 2026 (verification transcript)

## Symptom chain (as seen live)

1. `/api/mc/cost/agents?days=30` → `{"agents":{},"total_cost":0.0,"total_tokens":0,"total_requests":0,"period_days":30}`
2. page-cost DOM: `costTotalCost="$0.00"`, `costTotalTokens="0"`, `costAgentGrid.children.length = 0`
3. Console: `loadCostData is not defined` — **the function referenced by `onclick` in index.html was never created in app.js** (not a "slow fetch" — it literally did not exist).

## Root cause 1 — backend empty

`data/swarm_state.db` table `cost_tracking` had **0 rows**. Cost is only recorded when `record_usage` is invoked; MC itself rarely calls it. But Hermes gateway DOES write usage per LLM call into its own `state.db`:

- DB: `/Volumes/HermesAgent/HermesAgentUSB/data/state.db`
- Table: `session_model_usage` (761 rows as of 20 Ags 2026)
- Columns: `session_id, model, billing_provider, billing_base_url, billing_mode, task, api_call_count, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, reasoning_tokens, estimated_cost_usd, actual_cost_usd, cost_status, cost_source, first_seen, last_seen`

### Fallback query added to `swarm/bus.py` `get_agent_costs()`

```python
if not rows:  # cost_tracking empty
    import sqlite3 as _sqlite3
    state_db = os.environ.get(
        "HERMES_STATE_DB",
        os.path.join(os.environ.get("HERMES_HOME", "/Volumes/HermesAgent/HermesAgentUSB/data"),
                     "state.db"),
    )
    if os.path.exists(state_db):
        conn = _sqlite3.connect(f"file:{state_db}?mode=ro", uri=True)
        try:
            cutoff = (datetime.now() - timedelta(days=days)).timestamp()
            cur = conn.execute("""
                SELECT
                    COALESCE(billing_provider, 'unknown') AS agent_id,
                    model,
                    SUM(input_tokens), SUM(output_tokens),
                    SUM(input_tokens) + SUM(output_tokens) AS total_tokens,
                    SUM(COALESCE(estimated_cost_usd, 0.0)),
                    COUNT(*)
                FROM session_model_usage
                WHERE last_seen > ?
                GROUP BY agent_id, model
                ORDER BY total_tokens DESC
            """, (cutoff,))
            rows = cur.fetchall()
        finally:
            conn.close()
```

- Needed imports in `bus.py`: `from datetime import datetime, timedelta` (was missing → Pyright error).
- `billing_provider` mapped to agent_id so dashboard semantics (`agent → models[]`) hold; `cost_usd` is often 0.0 on free-tier gateway entries, but token counts and request counts are real.
- Result after restart: `agents: 12 | total tokens: 113,859,097 | requests: 138`.

## Root cause 2 — frontend function missing

`index.html` had the full cost page markup (KPI spans + `costAgentGrid` / `costModelGrid` / `costRecentList` + `onclick="loadCostData()"`) but `app.js` had zero `loadCostData`/`renderCostData` functions. Added:

- `loadCostData()` — fetch `/api/mc/cost/agents?days=<period>`, then `renderCostData(data)`.
- `renderCostData(data)` — sets 4 KPIs, renders cost-by-agent cards, flattens per-model cards, and recent entries list.
- Init: added `loadCostData();` to the "Initialize App" block (near `loadEcosystem()`).

## Cache-busting requirement

After editing `dashboard/app.js`, `/dashboard` still served the OLD js to the browser:
- `fetch('/static/app.js')` from console → `hasCost:false` while disk file already had the function.
- Fix: `index.html` line `~1114` `<script src="/static/app.js">` → `<script src="/static/app.js?v=20260820-1">`; then `launchctl kickstart -k gui/501/niu.missioncontrol`; then verify `typeof loadCostData === 'function'` in a FRESH browser session (old session may keep cached html).

## Telegram feed fix detail

`modules/gateway_log_parser.py` line ~38 had:
```python
TG_GROUP_CHAT_ID = "-REDACTED_CHAT_ID"  # placeholder → 0 messages
```
Fixed:
```python
TG_GROUP_CHAT_ID = os.environ.get("HERMES_TELEGRAM_CHAT_ID", "-1004204696417")
```
Same env var already used by `modules/hermes_bridge.py` — the real group chat ID must exist in the MC launchd plist EnvironmentVariables **and** the parser must read it, not hardcode a placeholder. Verified via API: 9 messages topic=1 render in `#tgFeed`.

## Lesson summary

- Empty cost/telegram pages: check backend endpoint AND DB rows first, then **verify the JS function actually exists** (`typeof loadCostData` in browser console) — "function referenced in HTML but never defined" is a recurring dashboard bug.
- Two different modules hardcoded `-REDACTED_CHAT_ID`; after finding one, grep the whole `modules/` dir.
- FastAPI StaticFiles serves live from disk — stale JS is a BROWSER CACHE problem, fixed with version query + MC restart, not by re-uploading files.