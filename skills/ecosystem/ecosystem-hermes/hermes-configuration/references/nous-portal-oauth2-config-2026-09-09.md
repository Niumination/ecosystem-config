# Nous Portal OAuth2 Config — 9 Sep 2026

## Problem: Config Drift Between hermes status and config.yaml

On 9 Sep 2026, `hermes status` showed `inclusionai/ling-3.0-flash-fin:free` / `Nous Portal` as the active model/provider, but `config.yaml` still had `provider: opencode-free` / `default: muse-spark-1.2-contributor-free` / `base_url: https://opencode.ai/zen/v1`.

**Root cause:** Model was changed via Nous Portal (OAuth2 flow), but `config.yaml`'s `model.*` fields were not synced.

## Fix Applied (verified working)

```bash
hermes config set model.provider nous
hermes config set model.default inclusionai/ling-3.0-flash-fin:free
hermes config set model.base_url https://inference-api.nousresearch.com/v1
hermes config set model.key_env NINE_ROUTER_API_KEY
hermes config set model.api_mode chat_completions
```

## Verification

- `hermes config show` → Model: `nous` / `inclusionai/ling-3.0-flash-fin:free`
- `hermes status` → Model: `inclusionai/ling-3.0-flash-fin:free`, Provider: `Nous Portal`
- API reachable: `curl https://inference-api.nousresearch.com/v1/models` with `NINE_ROUTER_API_KEY` → 391 models, `inclusionai/ling-3.0-flash-fin:free` confirmed present

## Key Facts

- `inference-api.nousresearch.com/v1` uses the same API key as Nous Portal (`NINE_ROUTER_API_KEY`)
- Nous Portal is OAuth2 — token stored in `hermes auth` state, NOT in config.yaml providers section
- But `model.provider: nous` in config.yaml works with `key_env: NINE_ROUTER_API_KEY` for inference API calls
- NEVER edit config.yaml directly — use `hermes config set` only

## Related Skills

- `hermes-configuration` — Config drift detection procedure
- `provider-fallback` — Fallback chain strategy
