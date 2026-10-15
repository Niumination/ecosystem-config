# OpenCode Provider Configuration — Session Notes

**Date:** 2026-09-08
**Issue:** OpenCode provider base_url misconfiguration caused 404 errors

## Problem

Hermes auto-appends `/v1` to every provider `base_url`. Configuring `base_url: https://opencode.ai/zen/v2` results in requests to `https://opencode.ai/zen/v2/v1` — a 404.

## Investigation

1. Tested `https://opencode.ai/zen/v2/models` → 404 (docs site, not API)
2. Tested `https://opencode.ai/zen/v1/models` → 200 (70 models loaded)
3. Tested `https://opencode.ai/zen/go/v1/models` → 200
4. Tested `https://opencode.ai/zen/v1/chat/completions` → needs billing

## Correct Configuration

| Provider | base_url | Hermes calls | Status |
|---|---|---|---|
| `opencode-zen` | `https://opencode.ai/zen` | `https://opencode.ai/zen/v1` | ✅ Working |
| `opencode-go` | `https://opencode.ai/zen/go` | `https://opencode.ai/zen/go/v1` | ✅ Working |

## Additional Findings

- **key_env:** `OPENCODE_ZEN_API_KEY` blocked by `_HERMES_PROVIDER_ENV_BLOCKLIST`. Use `OPENCODE_API_KEY`.
- **Free tier:** Models like `muse-spark-*` cannot be used via API — only in OpenCode app.
- **API billing:** `chat/completions` endpoint responds "No payment method" — API key loads correctly, just needs billing setup.

## Fix Commands

```bash
hermes config set providers.opencode-zen.base_url "https://opencode.ai/zen"
hermes config set providers.opencode-zen.key_env "OPENCODE_API_KEY"
hermes config set providers.opencode-go.base_url "https://opencode.ai/zen/go"
hermes config set providers.opencode-go.key_env "OPENCODE_API_KEY"
```
