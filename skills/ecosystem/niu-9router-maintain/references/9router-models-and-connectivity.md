# 9Router — Model Catalog & Connectivity Verification

Companion to `niu-9router-maintain` SKILL.md. Captured 29-Agu-2026.

## Verified Live Setup (localhost:20128)

9router v0.5.55, bound `127.0.0.1:20128`, tray mode (`--tray --skip-update`).
Auth: `Authorization: Bearer $NINE_ROUTER_API_KEY` (env `NINE_ROUTER_API_KEY`, value `sk-...`).
Use `127.0.0.1`, NOT `localhost` (avoids IPv6 surprises — though both worked once warmed up).

## Model Catalog (subset seen 29-Agu, via /v1/models)

- `gemini/` (Google AI Studio key from user): `gemini-3.7-flash`, `gemini-3.6-flash`,
  `gemini-3.5-flash-lite`, `gemini-3.1-pro-preview`, `gemini-3.1-flash-lite-preview`, `gemini-3-flash-preview`
- `ag/` (Antigravity, OAuth Google/GitHub di dashboard 9router): `ag/gemini-3.7-flash-{high,medium,low}`,
  `ag/gemini-3.6-flash-{high,medium,low}`
- Also present: `gh/` (GitHub Copilot free), `oc/` (OpenCode free), `kr/` (Kiro), `glm/`, `minimax/`.

**Model-ID gotcha:** 9router returns models from its catalog even if the upstream model is
unavailable. Picking a model the upstream doesn't serve → `404` from upstream (e.g.
`gemini-3.5-flash-low` → "models/gemini-3.5-flash-low is not found"). Always pick a model that
actually exists in the live catalog above.

## Connectivity Verification Recipe (test each provider with a real chat)

```bash
K="$NINE_ROUTER_API_KEY"
# Antigravity — WORKS (OAuth in dashboard, not key)
curl -s -N -m 30 -X POST "http://127.0.0.1:20128/v1/chat/completions" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $K" \
  -d '{"model":"ag/gemini-3.5-flash-low","messages":[{"role":"user","content":"reply OK"}],"max_tokens":15,"stream":true}'
# → SSE stream, HTTP 200, delta content "OK"

# Gemini — WORKS (needs AI Studio key set in 9router dashboard)
curl -s -N -m 35 -X POST "http://127.0.0.1:20128/v1/chat/completions" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $K" \
  -d '{"model":"gemini/gemini-3.5-flash-lite","messages":[{"role":"user","content":"reply OK only"}],"max_tokens":12}'
# → SSE stream, HTTP 200
```
Note: responses are **SSE** (`data: {...}` lines, ends `data: [DONE]`), not a single JSON body.
Parse with: split lines, skip `data: [DONE]`, `json.loads(line[6:])['choices'][0]['delta']['content']`.

## GOOGLE_API_KEY vs 9router

- `GOOGLE_API_KEY` lives in `~/.hermes/.env` (value `AQ.Ab8...`, len 53 — custom AI Studio format,
  NOT the `AIza...` standard, but still valid). It is Hermes's own Gemini auth, separate from 9router.
- LangChain `langchain-google-genai` `_BaseGoogleGenerativeAI.google_api_key` reads `GOOGLE_API_KEY`
  then `GEMINI_API_KEY` (precedence GOOGLE first). Confirms `GOOGLE_API_KEY` is the standard env var.
- To verify the key directly (bypassing 9router): must read it FROM THE FILE (shell session does not
  export it). Direct call returned `503 high demand` for `gemini-3.7-flash` = key accepted, model
  overloaded. `gemini-3.5-flash-lite` is the stable choice.
- 9router Gemini uses the key configured in ITS dashboard, independent of Hermes `.env`.

## Failure Modes Seen (and what they meant)

| Observation | Meaning | Action |
|---|---|---|
| `000` for ~10s after launch, then `200` | startup race — server not yet bound | wait / retry, don't "fix" |
| process in `launchctl list` but no `LISTEN` on 20128 | `KeepAlive:false` → died, no restart | set `KeepAlive:true`, reload plist |
| chat → `404` upstream "model not found" | wrong model ID | use a catalog-real model |
| direct Gemini `403` "no established identity" | key not actually passed (empty env) | read key from `.env` file, not `$var` |
| `503 high demand` | key OK, model overloaded | use lighter model (3.5-flash-lite) |
