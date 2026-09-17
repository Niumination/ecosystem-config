---
name: model-status-checker
description: Model status checker. 3-tier probe for daily health cron.
tags: [model, status, cron, 9router, openrouter, hermes, probe]
---

# Model Status Checker

Daily model availability and latency report via hybrid 3-tier approach.

## Trigger
- User asks for "model status", "model health", "daily model report"
- Setting up or debugging the model status cron job
- Investigating why a model is failing in production

## Architecture

### Tier 1 — Static Data (0 token, ~5s)
- **OpenRouter API**: `GET https://openrouter.ai/api/v1/models` — returns 444+ models with pricing (free/paid), context length, capabilities
- **9router local**: `GET http://localhost:20128/v1/models` — returns 88 models across 4 namespaces (gh, gemini, kr, cf)
- **Hermes config.yaml**: default model, providers, channel_overrides, cron model

### Tier 2 — Minimal Probe (1 token per model, ~30s for 6 critical)
- Only probe models identified as **critical** from Hermes config:
  - Default model (currently `inclusionai/ling-3.0-flash-fin:free`)
  - Channel overrides (802, 803, 804, 1172, 1)
  - Cron model
- Skip `explabs/` namespace — these are Hermes internal routing, not real provider models
- Route `nous` provider through 9router base URL (localhost:20128), NOT direct Nous Portal
- Probe payload: `{"model": "...", "messages": [{"role":"user","content":"OK"}], "max_tokens": 1, "stream": false}`
- Timeout: 15 seconds per model

### Tier 3 — Analysis & Report
- Cross-reference OpenRouter free list with 9router catalog
- Identify failed critical models
- Generate recommendations (switch default if failing, etc.)
- Output: JSON report file + stdout summary for Telegram delivery

## Cron Job Configuration

| Field | Value |
|-------|-------|
| Schedule | `0 9 * * *` (09:00 WIB daily) |
| Provider | 9router (localhost, no API key needed) |
| Model | explabs/gpt-5.4-mini |
| Deliver | telegram:-1004204696417:1,local |
| Script | `python3 ~/Desktop/Niumination/scripts/model_status_checker.py` |

## Output Format

```
📊 Model Status Report — 2026-09-17 09:00 WIB

OpenRouter: 24 free / 444 total
9router: 88 total (gh:33, gemini:8, kr:34, cf:13)

✅ Critical OK: 5
❌ Critical Failed: 1
   • inclusionai/ling-3.0-flash-fin:free: http_404 (5ms) [false negative — see pitfall]
⏭️  Skipped: 5 (explabs/* namespace)

💡 Default model is healthy — no change needed
💡 24 free OpenRouter models available as fallback

📁 Saved: ~/.hermes/cron/output/model-status-20260917-090000.json
```

## Pitfalls

1. **Direct probe = false negative for routed models.** `inclusionai/ling-3.0-flash-fin:free` returns HTTP 404 when probed directly at 9router because it is internally routed to Nous Portal. But it WORKS in production (confirmed by active session using it). Never mark a model as failed based solely on direct probe if it is the active default or confirmed working in chat.

2. **`explabs/` namespace is not a real provider.** It is Hermes internal routing. Skip these during probe — they cannot be tested directly. If a channel uses `explabs/gpt-5.4-mini`, it works as long as 9router is healthy.

3. **Nous provider goes through 9router.** `provider: nous` in config.yaml does NOT mean direct connection to `inference-api.nousresearch.com`. All Nous traffic routes through 9router at localhost:20128. Always probe Nous models via 9router base URL.

4. **HTTP 401 via direct Nous URL is expected.** If you bypass 9router and hit `https://inference-api.nousresearch.com/v1` with `NINE_ROUTER_API_KEY`, you get 401 because that key is for 9router, not Nous Portal directly. This is not a model failure.

5. **OpenRouter free models ≠ 9router free models.** OpenRouter publishes pricing metadata (free/paid). 9router does not — all 88 models appear identical in the catalog. The only way to know if a 9router model is free is to check if its underlying provider has a free tier (e.g., `gemini` via AI Studio, `github` via Copilot free).

6. **Cron delivery failures from provider auth.** The cron job itself needs a working LLM provider to format and send the report. If the default Hermes provider (nous) is unreachable from cron sessions, set the cron job to use `9router` as provider with base_url `http://localhost:20128/v1` and model `explabs/gpt-5.4-mini`. Direct provider config (provider: 9router) sometimes fails to persist via cronjob_manage — verify with `hermes cron list` after update.

7. **Probe budget.** 6 critical models × ~2 tokens × 1x/day = ~12 tokens/day. Even with 10x overhead for retries, this is negligible (<1K tokens/month). Do NOT probe all 88 9router models daily — that would cost ~180K tokens/month for no additional value.

8. **Cron model vs main model.** The cron job uses a separate model (`explabs/gpt-5.4-mini`) from the default (`inclusionai/ling-3.0-flash-fin:free`). If the default fails, cron may still work and vice versa. Report both statuses independently.