---
name: model-status-checker
description: Model status checker. 3-tier probe for daily health cron.
tags: [model, status, cron, 9router, openrouter, hermes, probe]
updated: 2026-09-27
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
- **9router local**: `GET http://localhost:20128/v1/models` — **tanpa header auth** (verified 27 Sep 2026). **67 model** saat probe 22:2x: `gh` 34 · `kr` 24 · `ag` 4 · `cf` 2 · `gemini` 1 · `openrouter` 1 · `opencode-combo` 1. **Katalog berflapping** (67→51→67 dalam sehari) — selalu probe ulang, jangan hardcode angka.
- **Hermes config.yaml**: default model, providers, channel_overrides, cron model

### Tier 2 — Minimal Probe (1 token per model, ~30s for 6 critical)
Only probe models identified as **critical** from Hermes config:
- Default model (currently `stealth/space-bunny-alpha` via nous)
- Channel overrides (1, 802, 803, 804, 1172, 7402, 8853)
- Cron model (`meituan/longcat-2.0:free` via nous)
- x_search model (`upstage/solar-pro4:free` via nous)
- Delegation model (`nvidia/nemotron-3-ultra-550b-a55b:free` via openrouter)
- Skip `explabs/` namespace — **does not exist** anymore
- Route `nous` provider through direct URL `https://inference-api.nousresearch.com/v1` (NOT 9router), with the **OAuth access_token from `~/.hermes/auth.json`** → `providers.nous.access_token`. NOT from `.env` — there is no `NOUS_TOKEN` key there.
- Route `openrouter` models through OpenRouter endpoint directly
- Route `huancheng` models through `https://api.hcnsec.cn/v1`
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
| Provider | nous |
| Model | meituan/longcat-2.0:free |
| Deliver | telegram:-1004204696417:**7402**,local |
| Script | `python3 ~/Desktop/Niumination/scripts/model_status_checker.py` |

## Output Format

```
Model Status Report — 2026-09-27 09:00 WIB

9router: 67 models (gh:34, kr:24, ag:4, cf:2, gemini:1, openrouter:1, opencode-combo:1)
Nous: active (oauth), default: stealth/space-bunny-alpha

✅ Critical OK: N
❌ Critical Failed: M
⏭️  Skipped: X

💡 Default model is healthy — no change needed
💡 7 nous :free models available

📁 Saved: ~/.hermes/cron/output/model-status-YYYYMMDD-090000.json
```

## Pitfalls

1. **Nous is NOT through 9router.** `provider: nous` in config.yaml means direct connection to `https://inference-api.nousresearch.com/v1` via OAuth device-code (`~/.hermes/auth.json`). Do NOT route nous models through 9router base URL.

2. **9router: `/v1/models` tanpa auth, `/v1/chat/completions` butuh auth.** Verified 27 Sep 2026: `/v1/models` → HTTP 200 `application/json` tanpa header. Hanya `/v1/chat/completions` yang perlu `Authorization: Bearer $NINE_ROUTER_API_KEY`.

3. **`explabs/` namespace does not exist.** Removed from 9router catalog. All mappings migrated to `nous` or `openrouter`.

4. **9router is cadangan, bukan primary.** Primary is `nous`. 9router used as fallback only.

5. **Mission Control MATI (verified 27 Sep 2026, 22:0x).** `localhost:5200` dan `localhost:3000` keduanya HTTP 000. Tidak ada proses `next-server` MC; kedua plist MC tidak ter-load di launchd. Klaim lama "MC sehat tapi butuh auth" tidak berlaku.

6. **Nous `:free` model limitations.** 7 models: `inclusionai/ling-3.0-flash-fin:free` · `inclusionai/ling-3.0-flash-sante:free` · `meituan/longcat-2.0:free` · `poolside/laguna-s-2.1:free` · `poolside/laguna-xs-2.1:free` · `stepfun/step-3.7-flash:free` · `upstage/solar-pro4:free`. Account is free tier — no paid credits.

7. **OpenRouter free models have daily limits.** 429 errors on heavy usage without paid balance.

8. **Cron model vs main model.** Cron uses `meituan/longcat-2.0:free` (nous), different from default `stealth/space-bunny-alpha` (nous). Report both independently.

## Channel Mapping for Probe

| Channel | Model | Provider | Probe Endpoint |
|---------|-------|----------|----------------|
| 1 | `inclusionai/ling-3.0-flash-fin:free` | nous | https://inference-api.nousresearch.com/v1 |
| 802 | `inclusionai/ling-3.0-flash-sante:free` | nous | https://inference-api.nousresearch.com/v1 |
| 803 | `meituan/longcat-2.0:free` | nous | https://inference-api.nousresearch.com/v1 |
| 804 | `deepseek/deepseek-v4-flash-0731:free` | openrouter | https://openrouter.ai/api/v1 |
| 1172 | `poolside/laguna-s-2.1:free` | nous | https://inference-api.nousresearch.com/v1 |
| 7402 | `meituan/longcat-2.0:free` | nous | https://inference-api.nousresearch.com/v1 |
| 8853 | `sensenova-6.8-flash-lite` | huancheng | https://api.hcnsec.cn/v1 |

## Probe Budget
6 critical models × ~2 tokens × 1x/day = ~12 tokens/day. Negligible.
Do NOT probe all 67 9router models daily. Use 9router as fallback probe only.

## Related Skills
- `9router-model-mapping` — model mapping reference and rules
- `provider-fallback` — general fallback strategy
- `config-history-review` — audit config changes
- `ecosystem-dox-maintenance` — DOX hygiene
