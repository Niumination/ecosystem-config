---
name: system-one-decisions
description: "Use when calling decision models (jev/systemone) via 9router."
version: 1.0.0
author: Hermes Agent
description: "Use when calling decision models (jev) via 9router."
platforms: [macos, linux]
metadata:
  hermes:
    tags: [9router, systemone, decisions, jev, openrouter, model-routing]
    related_skills: [niu-9router-maintain, 9router-model-mapping, provider-model-verification]
---

# System One & Decision Models (9router)

9router exposes a stateful proxy endpoint `POST /systemone` (Next.js rewrite → `/api/v1/systemone`) for **decision models** — models that answer structured questions, not free chat. Classic example: `openrouter/typesafe/jev-1.13` (TypeSafe System One, 200k context).

## Hard rule: decisions models reject chat/completions

`openrouter/typesafe/jev-1.13` returns HTTP 400 on `/v1/chat/completions`: `"is a decisions model and cannot be used with the chat/completions endpoint. Use the /api/alpha/decisions endpoint instead."`
- Do NOT try to use a decisions model through a normal Hermes/OpenAI-compatible chat path — it will 400.
- The correct route is `/systemone` (or OpenRouter `/api/alpha/decisions` via SDK).

## POST /systemone body shape

```json
{
  "model": "openrouter/typesafe/jev-1.13",
  "state": {"messages": [{"role": "user", "content": "..."}]},
  "questions": {
    "jawaban": {
      "type": "choice",
      "instructions": "Apa isi pesan?",
      "criteria": {"sapaan": "Berisi sapaan", "lain": "Lainnya"}
    }
  }
}
```

- `state` = arbitrary context object (messages, fields, docs). Required.
- `questions` = **object** (NOT array — 9router rejects arrays with `Missing required field: questions`); each value is an object with schema:
  - `type: "choice"` → `criteria` = object of option-label → description
  - `type: "noul"` → yes/no boolean (noul = "noulli")
- Auth: `Authorization: Bearer $NINE_ROUTER_API_KEY`.

Response:
```json
{"model": "typesafe/jev-1.13-20260917", "answers": {"jawaban": {"type": "choice", "choice": "sapaan", "probabilities": {"lain": 0, "sapaan": 1}, "confidence": 1}}, "usage": {"input_tokens": 334, "output_tokens": 34, "cost": 0.000014028}}
```

## How 9router routes /systemone

- Rewrite: `/systemone` → `/api/v1/systemone` (verified in `server.js` `_originalRewrites`).
- Route resolves model → provider via provider-alias/prefix, picks an active connection, and proxies `{...body, model}` + API key (+ `x-opencode-session` header) to the provider's `systemoneConfig.baseUrl`.
- Providers WITH `systemoneConfig` (verified via grep in `/usr/local/lib/node_modules/9router/app/.next-cli-build/server/chunks/*.js`): `opencode` → `https://opencode.ai/zen/v1/systemone`, `openrouter` → `https://openrouter.ai/api/v1/systemone`.
- Providers WITHOUT `systemoneConfig` → 400 `Provider 'X' does not support System One.`

## Hermes integration: NOT automatic

- Hermes providers all use `api_mode: chat_completions` — there is no config path to `/systemone`, and no python code references systemone (grep source = 0 hits).
- A decision model cannot be set as a normal Hermes model. It only works via: (a) curl/script hitting `/systemone` directly, or (b) a 9router **combo** model (`combos` table) that embeds the decision call.
- Default answer when user asks "is systemone active in Hermes?": **no** — endpoint exists and works, but Hermes never calls it automatically.

## Combo CANNOT embed a decisions model — PROVEN 2026-09-26

Do not propose a 9router combo for jev. Verified empirically: a test combo
`['openrouter/typesafe/jev-1.13','oc/big-pickle']` called via
`/v1/chat/completions` returns HTTP 400
`"typesafe/jev-1.13 is a decisions model and cannot be used with the
chat/completions endpoint."`

Why, from the 9router bundle (`server/chunks/8910.js`): combo resolution is
`p(a,b){ if(a.includes("/")) return null; combos.find(b=>b.name===a) }` then a
loop over `handleSingleModel(body, model)`. Every combo runs on the
chat/completions path; jev is rejected upstream by OpenRouter before the
fallback model is tried. The `combos.kind` column is written but never read in
the resolution path — `kind:"systemone"` is a **model** attribute in the provider
catalog (`8325.js`: `{id:"jev-1.13", name:"Jev 1.13", kind:"systemone"}`), not a
combo type.

## Wrapper script: scripts/systemone.py

`scripts/systemone.py` (repo Niumination, chmod 755) is the only supported
caller. It POSTs to `/systemone` and prints choice/noul results. No execution
path: no subprocess, no eval/exec, no os.system, no file writes except a
chmod 600 audit log at `~/.hermes/logs/systemone-audit.log`.

Safety gates (all fail-closed — a failed gate means DO NOT call):
1. `--allow` is required; without it the script is a dry-run printer.
2. `SYSTEMONE_DISABLED=1` env or `~/.hermes/systemone.disabled` file = hard stop.
3. Per-call cost cap (`--budget`, default 0.01 USD); estimate over cap = refuse
   before any request.
4. Caps: max 10 questions/request, max 20 criteria, max 8000 chars of context.
5. API key read from `~/.hermes/.env`, never printed, never in argv.

## Free tier exists — default is `opencode/jev-1.13-free`

Tested 2026-09-26 against `/systemone`:

| Model | Result |
|---|---|
| `opencode/jev-1.13-free` | 200, `usage.cost` = **None (free)**, 5/5 stable |
| `openrouter/typesafe/jev-1.13` | 200, cost ~1.2e-05/call |
| `opencode/jev-1.13` (no `-free`) | 401 "Rate-limited Zen models require a workspace" |
| `oc/big-pickle`, `opencode/gpt-5` | 500 / 401 — not decisions models |

`scripts/systemone.py` defaults to the free one. Override with
`SYSTEMONE_MODEL=openrouter/typesafe/jev-1.13`. Do not use opencode `jev-1.13`
without `-free` — it always 401s.

`/systemone` filters models itself: only entries tagged `kind:"systemone"`
resolve. That tag is internal 9router metadata (`8325.js`) and is **not**
exposed by `/v1/models` — the catalog lists 0 `opencode/*` models yet
`opencode/jev-1.13-free` still works. So `/v1/models` is not a valid
availability check for a decisions model; `--health` warns when the configured
model is absent from the catalog. `capabilities.tools: true` in the catalog
does NOT mean the model supports systemone (that flag is generic tool-calling).

## Response shape differs by type — do not assume `choice`
- `choice` → `{"type":"choice","choice":...,"confidence":...,"probabilities":{...}}`
- `noul` → `{"type":"noul","noul":0.82}` — a **float score** 0..1, no `choice` key.

Self-check (free, no network, no cost): `python3 scripts/systemone.test.py`.
Health (costs ~1.2e-5 USD, does call the API): `python3 scripts/systemone.py --health`.

## Verification recipe

```bash
# 1. confirm model exists in catalog
curl -s -m 10 http://localhost:20128/v1/models | python3 -c 'import json,sys; d=json.load(sys.stdin); ms=d.get("data",d); print([m.get("id") for m in ms if isinstance(ms,list) and "jev" in str(m.get("id"))])'

# 2. confirm provider connection active
sqlite3 ~/.9router/db/data.sqlite "SELECT id, provider, name, isActive, substr(data,1,80) FROM providerConnections WHERE provider='openrouter';"

# 3. POST /systemone (see body above) — expect 200 with answers

# 4. detect which providers support systemone
ls /usr/local/lib/node_modules/9router/app/.next-cli-build/server/chunks/ | while read f; do grep -l systemoneConfig /usr/local/lib/node_modules/9router/app/.next-cli-build/server/chunks/$f; done | sort -u
```

## Pitfalls
- `questions` must be an object whose VALUES are objects — `questions: {q1: "string"}` fails zod validation (`expected object, received string`).
- Missing either field gives misleading error: omit `state` → `Missing required field: state`; send array questions → `Missing required field: questions`. Always send both.
- 9router `data` column in `providerConnections` holds JSON: apiKey + `testStatus`, NOT a flat `apiKey` column.
- Model alias trick: catalog lists `openrouter/typesafe/jev-1.13`; response model may come back as `typesafe/jev-1.13-20260917` (snapshot). Don't match on exact response id.
