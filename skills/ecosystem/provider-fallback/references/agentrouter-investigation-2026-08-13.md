# Provider Troubleshooting — AgentRouter Investigation (2026-08-13)

## Context
During provider mapping review, AgentRouter was found to be non-functional despite being configured in `config.yaml`. Investigation revealed it's not a native Hermes provider.

## Investigation Steps (Reproducible)

### Step 1: Test API connectivity
```bash
# Test /v1/models endpoint
curl -s --max-time 10 \
  -H "Authorization: Bearer $AGENTROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  https://agentrouter.org/v1/models

# Test /v1/chat/completions
curl -s --max-time 10 \
  -H "Authorization: Bearer $AGENTROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST https://agentrouter.org/v1/chat/completions \
  -d '{"model":"test","messages":[{"role":"user","content":"test"}]}'
```

### Step 2: Check Hermes config for known issues
```bash
# Check for unknown keys being ignored
grep -i "agentrouter" /Volumes/HermesAgent/HermesAgentUSB/data/logs/gateway.error.log
# Output: WARNING hermes_cli.config: providers.agentrouter: unknown config keys ignored: type

# Count how many times this appeared
grep -c "providers.agentrouter: unknown config keys ignored: type" /Volumes/HermesAgent/HermesAgentUSB/data/logs/gateway.error.log
```

### Step 3: Check if provider was ever used for completions
```bash
# Search session dumps for agentrouter usage
grep -rn "agentrouter" /Volumes/HermesAgent/HermesAgentUSB/data/sessions/*.json \
  | grep -v "agentrouter.org" \
  | grep -v "agentrouter_api_key"
```

## Root Cause Analysis

### Why AgentRouter Failed

1. **Not a native Hermes provider** — Hermes Agent requires custom TypeScript extensions for AgentRouter
2. **401 Unauthorized on all endpoints** — key appears unverified/unregistered
3. **Config keys ignored** — `type: openai` in config.yaml is silently ignored by Hermes
4. **Never actually used** — no chat completions logged despite being in config since 2026-07-23

### AgentRouter Architecture

AgentRouter.org is a Chinese AI proxy/gateway service. According to their docs:
- Requires Discord-based account verification (`https://discord.gg/aYq5B4RW3`)
- Hermes Agent integration needs custom extension using `pi.registerProvider()`
- Two API flavors: Anthropic Messages (Claude) and OpenAI Compatible (GPT-5.5/GLM-5.2)

## Fix Applied

### Config Cleanup
```bash
# Remove from providers section
hermes config set providers.agentrouter.base_url ""
hermes config set providers.agentrouter.key_env ""
hermes config set providers.agentrouter.type ""

# Remove other references
hermes config set providers.openrouter.base_url ""
hermes config set providers.openrouter.key_env ""
hermes config set openrouter.response_cache false
hermes config set openrouter.response_cache_ttl 0
hermes config set openrouter.min_coding_score 0
hermes config set delegation.provider gemini

# Verify cleanup
grep -c "openrouter\|agentrouter" /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml
# Expected: 0
```

### Cache Cleanup
```bash
rm -f /Volumes/HermesAgent/HermesAgentUSB/data/provider_models_cache.json
rm -f /Volumes/HermesAgent/HermesAgentUSB/data/cache/model_catalog.json
```

## Provider Inventory After Cleanup

### Working Providers
| Provider | Status | Models | Notes |
|----------|--------|--------|-------|
| 9router (Local) | ✅ | 48 | `gratis`, `capek`, `gila`, Gemini, Claude, DeepSeek, etc. |
| Huancheng | ⚠️ | 20 | Token active but invalid for API calls |

### Removed Providers
| Provider | Issue | Action |
|----------|-------|--------|
| OpenRouter | Empty key, 401 errors | Removed, delegation to gemini |
| AgentRouter | 401 unauthorized, needs custom ext | Removed from config |

## Reference: Hermes Agent AgentRouter Docs
- URL: `https://agentrouter.org/docs/hermes.html`
- Pattern: Custom TypeScript extension with `pi.registerProvider()`
- Two API variants: `anthropic-messages` and `OpenAI Compatible`
