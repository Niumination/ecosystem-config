# OpenCode Provider Troubleshooting — 8 Sep 2026

## Session Summary

This session exposed multiple configuration issues with OpenCode providers (`opencode-zen` and `opencode-go`) that caused 404 errors and credential registration failures.

## Issues Found

### 1. Base URL Misconfiguration
- **Wrong:** `https://opencode.ai/zen/v2` (docs site, not API)
- **Correct:** `https://opencode.ai/zen` (Hermes auto-appends `/v1`)
- **Wrong:** `https://opencode.ai/zen/go/v1`
- **Correct:** `https://opencode.ai/zen/go` (Hermes auto-appends `/v1`)

### 2. Security Filter Blocking `OPENCODE_ZEN_API_KEY`
- Hermes security filter (GHSA-rhgp-j443-p4rf) blocks `OPENCODE_ZEN_API_KEY`
- **Solution:** Use `OPENCODE_API_KEY` instead for both providers

### 3. Free Tier Policy Instability
- Model `muse-spark-1.2-contributor-free` worked in morning, failed by evening
- Error: `HTTP 400: OpenCode's free tier can only be used in OpenCode`
- **Conclusion:** Free tier API access is unreliable; use paid models or alternative providers

## Verified Working Configuration

```yaml
providers:
  opencode-zen:
    base_url: https://opencode.ai/zen
    api_mode: chat_completions
    key_env: OPENCODE_API_KEY
  opencode-go:
    base_url: https://opencode.ai/zen/go
    api_mode: chat_completions
    key_env: OPENCODE_API_KEY
```

## Verification Commands

```bash
# Test Zen endpoint
curl -s -o /dev/null -w "zen/v1/models: %{http_code}\n" \
  --connect-timeout 5 https://opencode.ai/zen/v1/models

# Test Go endpoint
curl -s -o /dev/null -w "zen/go/v1/models: %{http_code}\n" \
  --connect-timeout 5 https://opencode.ai/zen/go/v1/models

# Check if env var is blocked
grep "OPENCODE_ZEN_API_KEY" ~/.hermes/logs/errors.log
```

## Related Mobile-Harness Integration

Added 4 new provider presets to `Niumination/Mobile-Harness`:
- `AGENTROUTER` — OpenAI Chat protocol
- `HUANCHENG` — Anthropic Gateway protocol
- `NINE_ROUTER` — OpenAI Chat protocol
- `OPENCODE_ZEN` — OpenAI Chat protocol

Files modified:
- `Models.kt` — enum entries
- `RuntimeBridge.kt` — env var mapping
- `PocketDevApp.kt` — UI colors/marks

Commit: `77d6afb` (Niumination/Mobile-Harness)

## Lessons Learned

1. Always check if base_url has version suffix — Hermes auto-appends `/v1`
2. Security filter may block specific env var names; test with alternative names
3. Free tier APIs are not stable for production use; have fallback providers ready
4. OpenCode docs site (`/v2/docs`) is NOT the API endpoint
