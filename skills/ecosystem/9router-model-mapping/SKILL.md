---
name: 9router-model-mapping
description: "Configure and maintain 9router model mapping for Hermes — fallback chain, channel overrides, quota-aware model selection"
version: "2.0.0"
author: Afrizal Munthe
tags: [9router, model-mapping, fallback, quota, niumination, hermes-config]
---

# 9Router Model Mapping

## Overview
Configure Hermes to use 9router as primary provider with a diversified fallback chain. All models must be verified in the live 9router catalog (localhost:20128) before being added to config.

## Current Config (07 Sep 2026)

```yaml
model:
  provider: 9router
  default: explabs/gpt-5.4-mini
  base_url: http://localhost:20128/v1
  api_mode: chat_completions
  key_env: NINE_ROUTER_API_KEY

fallback_model:
  - provider: 9router
    model: ag/gemini-3.8-flash-medium
  - provider: 9router
    model: ag/gemini-3.7-flash-medium
```

## Verified Working Models (from live catalog + HTTP-200 probe)

| Role | Model | Provider | Notes |
|------|-------|----------|-------|
| Default | `explabs/gpt-5.4-mini` | 9router | primary, may 503 intermittently |
| Fallback 1 | `ag/gemini-3.8-flash-medium` | 9router | more stable during backend degradation |
| Fallback 2 | `ag/gemini-3.7-flash-medium` | 9router | secondary fallback |
| Vision | `explabs/claude-fable-5` | 9router | |
| Compression | `ag/gemini-3.7-flash-low` | 9router | active; previously retired `ag/gemini-3.5-flash-*` variants are deprecated |
| Delegation | `explabs/gpt-5.4-mini` | 9router | |
| X-search | `explabs/grok-4.20` | 9router | |
| Cron | `explabs/gpt-5.4-mini` | 9router | |
| Channel 1 | `explabs/gpt-5.4-mini` | 9router | |
| Channel 802 | `explabs/claude-haiku-4.5` | 9router | may 503 intermittently |
| Channel 803 | `explabs/gpt-4o-mini` | 9router | may 503 intermittently |
| Channel 804 | `explabs/claude-sonnet-4.6` | 9router | may 503 intermittently |
| Channel 1172 | `explabs/gemma-4-31b` | 9router | may 503 intermittently |

## Backend Stability Notes
- `explabs/` routes may return **503** from backend `openai-compatible-chat-...` while the 9router service and catalog remain healthy.
- `ag/gemini-*` routes have been more stable during backend degradation.
- Do not declare a fallback chain “good” from stale probe results. Re-probe immediately before finalizing config.

## Config Sync Requirement
When updating Hermes model config, mirror the change to:
- `~/.hermes/config.yaml`
- `~/Desktop/Niumination/apps/JHermUSB-portable/config/config.yaml`

Both must stay aligned because the portable repo is the DR restore source.

## Catalog State
- Total models: 334
- Active namespace: `explabs/`, `ag/`, `claude-combo`
- Deprecated namespaces: `gh/`, `kr/`, `gemini/`, `experimentallabs/`

## CRITICAL Rules

### 1. Verify in Live Catalog
ALWAYS check `curl -s http://localhost:20128/v1/models` before adding a model. Never assume availability.

### 2. Use Verified Working Models Only
Only add models that returned HTTP-200 in live probe. Retired models must be removed from config immediately.

### 3. Use Active Namespaces Only
Configure models from active namespaces: `explabs/`, `ag/`, `claude-combo`. Do not use deprecated namespaces `gh/`, `kr/`, `gemini/`, `experimentallabs/`.

### 4. Re-verify Before Finalizing
Models can retire between probes. Always re-probe selected models immediately before writing config, not from earlier session results.

### 5. Python Env Expansion Pitfall
When writing inline Python probe scripts, `$VAR` does **not** expand inside Python string literals. Use `os.environ.get("NINE_ROUTER_API_KEY", "")` instead of embedding shell variables directly.

### 6. Batch Probe Pattern
Use a threaded probe script with queue-based workers (8 workers, 12s timeout) against `http://localhost:20128/v1/chat/completions`. Save results to `/tmp/explabs_probe_results.json` for offline analysis.

### 7. Config Edit Rules
- Backup first: `cp config.yaml config.yaml.bak-YYYYMMDD`
- Use `hermes config set` or direct YAML edit via patch tool
- Never use heredoc-style replacement — causes escape-drift
- Verify with `hermes config show` after edit
- Restart gateway from separate shell after config change

## Quota Backend Map
| Prefix | Backend | Notes |
|--------|---------|-------|
| `ag/gemini-*` | Google AI (Antigravity) | ⚠️ ALL share same quota |
| `gemini/*` | Google AI (native) | Separate quota from Antigravity |
| `gh/*` | GitHub Models | Independent |
| `kr/*` | Kimi | Independent |
| `ag/claude-*` | AG (Claude) | Different family |
| `ag/gpt-oss-*` | Local open source | No API |

## Verification Checklist
- [ ] All models in `fallback_providers` exist in `curl http://localhost:20128/v1/models`
- [ ] No two models share the same quota backend
- [ ] Default model verified working
- [ ] Channel override models verified
- [ ] Backup created before edit
- [ ] Documentation updated

## Rollback
```bash
cp ~/.hermes/config.yaml.bak-YYYYMMDD ~/.hermes/config.yaml
```

## Related Skills
- `provider-fallback` — general fallback strategy
- `model-checker` — model availability checking
- `config-history-review` — audit config changes
- `ecosystem-dox-maintenance` — DOX hygiene
