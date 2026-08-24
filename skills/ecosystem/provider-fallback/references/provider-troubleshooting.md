# Provider Troubleshooting Guide

## Common Provider Failures

### 1. Invalid Token
**Error:** `Invalid token (request id: ...)`
**Cause:** API key expired or revoked
**Fix:** Regenerate key from provider dashboard, update .env

### 2. Unauthorized Client
**Error:** `unauthorized client detected`
**Cause:** IP restriction or account suspension
**Fix:** Check provider dashboard, verify key format

### 3. Empty API Key
**Check:** `echo ${#KEY_VAR}` should return length > 0
**Fix:** Set key in .env or export

### 4. Endpoint 404
**Error:** Returns HTML 404 instead of JSON
**Fix:** Check provider docs for current endpoint URL

## Fallback Strategy

1. **Local 9router** (localhost:20128) — most reliable, 48+ models
2. **OpenRouter** (if key set)
3. **Direct provider** (if key valid)

## Quick Diagnostic

```bash
# Test 9router local
curl -s http://localhost:20128/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"data\",[]))} models')"

# Check key lengths
echo "Huancheng: ${#HUANCHENG_API_KEY}"
echo "AgentRouter: ${#AGENTROUTER_API_KEY}"
echo "OpenRouter: ${#OPENROUTER_API_KEY}"
```

## Configuration Fix

When primary provider fails, update config.yaml:
```yaml
model:
  default: gratis
  provider: 9router
  base_url: http://localhost:20128/v1
```

Then `/reset` or restart session.
