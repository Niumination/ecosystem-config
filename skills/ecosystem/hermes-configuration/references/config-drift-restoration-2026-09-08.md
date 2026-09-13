# Config Drift Detection & Restoration — 2026-09-08

## Incident Summary

On 2026-09-08 at 00:27, Hermes config drifted from `9router/explabs/gpt-5.4-mini` to `opencode-zen/muse-spark-1.3-contributor-free` without user intent. The drift affected 4 fields in `model:` section.

## Detection Method

```bash
# Compare current config against latest backup
diff ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.<latest-timestamp>

# Output showed:
# 2,5c2,5
# <   provider: 9router
# <   default: explabs/gpt-5.4-mini
# <   base_url: http://localhost:20128/v1
# <   api_mode: chat_completions
# ---
# >   provider: opencode-zen
# >   default: muse-spark-1.3-contributor-free
# >   base_url: https://opencode.ai/zen/v2
# >   api_mode: codex_responses
```

## Restoration Procedure

**CRITICAL:** `patch` and `write_file` are BLOCKED for `~/.hermes/config.yaml`. Only `hermes config set` works.

```bash
# Restore each drifted field individually
hermes config set model.provider 9router
hermes config set model.default explabs/gpt-5.4-mini
hermes config set model.base_url http://localhost:20128/v1
hermes config set model.api_mode chat_completions
```

## Post-Restoration Validation

```bash
# 1. YAML validity
python3 -c "import yaml; yaml.safe_load(open('/Users/zaryu/.hermes/config.yaml'))"

# 2. Model exists in catalog
curl -s http://localhost:20128/v1/models | python3 -c "
import json,sys
d=json.load(sys.stdin)
target='explabs/gpt-5.4-mini'
found=any(m.get('id')==target for m in d['data'])
print(f'{target}: {\"FOUND\" if found else \"NOT FOUND\"}')
"

# 3. Fallback chain intact
grep -A 5 "^fallback_model:" ~/.hermes/config.yaml
```

## Adding Providers (opencode-zen & opencode-go)

When user requested adding opencode providers back to config:

```bash
# opencode-zen (codex_responses protocol)
hermes config set providers.opencode-zen.base_url "https://opencode.ai/zen/v2"
hermes config set providers.opencode-zen.api_mode "codex_responses"
hermes config set providers.opencode-zen.key_env "OPENCODE_ZEN_API_KEY"

# opencode-go (chat_completions protocol)
hermes config set providers.opencode-go.base_url "https://opencode.ai/zen/go/v1"
hermes config set providers.opencode-go.api_mode "chat_completions"
hermes config set providers.opencode-go.key_env "OPENCODE_ZEN_API_KEY"
```

## Key Differences Between opencode-zen and opencode-go

| Field | opencode-zen | opencode-go |
|---|---|---|
| Base URL | `https://opencode.ai/zen/v2` | `https://opencode.ai/zen/go/v1` |
| api_mode | `codex_responses` | `chat_completions` |
| Key Env | `OPENCODE_ZEN_API_KEY` | `OPENCODE_ZEN_API_KEY` |

## Root Cause Analysis

The drift likely occurred because:
1. User switched model via `/model opencode/muse-spark-1.3` in Telegram
2. Hermes (or a foreground agent) wrote the full provider config to `model:` section
3. This overwrote the default 9router provider settings

**Prevention:** When user requests model switch via `/model`, verify if the change is provider-level or model-level. Provider-level changes should be confirmed explicitly.

## Network Status (2026-09-08)

| Endpoint | Status | Notes |
|---|---|---|
| `api.telegram.org` | ✅ 302 (0.6s) | Reachable from Mac |
| `api.hcnsec.cn` | ✅ 401 (1.9s) | Reachable (401 = needs auth, not network failure) |
| `localhost:20128` (9router) | ✅ 200 (1.7s) | Reachable |

Previous log errors showing "Connection error" for huancheng and Telegram were transient or DNS-related, not persistent network failures.
