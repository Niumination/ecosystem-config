# OpenCode Provider Quirks (Zen & Go)

## Base URL

OpenCode has two API gateways — **Zen** and **Go**. Hermes auto-appends `/v1` to `base_url`, so the config must NOT include the `/v1` suffix.

| Provider | Correct base_url | Hermes resolves to | Status |
|----------|------------------|-------------------|--------|
| `opencode-zen` | `https://opencode.ai/zen` | `https://opencode.ai/zen/v1` | ✅ Working |
| `opencode-go` | `https://opencode.ai/zen/go` | `https://opencode.ai/zen/go/v1` | ✅ Working |

### ❌ WRONG — `/v2` is docs site, NOT API

`https://opencode.ai/zen/v2` is the **OpenCode documentation site** (Next.js app), not an API gateway. Hermes appends `/v1` → `/zen/v2/v1` → returns HTML 404 page.

```bash
# Verify:
curl -s -o /dev/null -w "%{http_code}" https://opencode.ai/zen/v1/models  # → 200
curl -s -o /dev/null -w "%{http_code}" https://opencode.ai/zen/v2/models  # → 404 (HTML page)
```

## API Key

Use `OPENCODE_API_KEY` (not `OPENCODE_ZEN_API_KEY`). The latter is blocked by Hermes security filter `_HERMES_PROVIDER_ENV_BLOCKLIST` (GHSA-rhgp-j443-p4rf).

## Free Tier Limitation

OpenCode free tier models (`muse-spark-1.2-contributor-free`, `muse-spark-1.3-contributor-free`) may work intermittently via API but are **officially restricted to the OpenCode app**. Error: `"OpenCode's free tier can only be used in OpenCode"`.

For reliable API usage, a paid plan or billing setup is required: `https://opencode.ai/workspace/<id>/billing`

## Model Discovery

Zen gateway exposes 70+ models including Claude, GPT, Gemini families. Go gateway requires $10/month subscription for open source models.

## Protocol

- Zen: `codex_responses` (OpenAI Responses API format)
- Go: `chat_completions` (OpenAI Chat Completions format)

## Verification

```bash
# Load models
curl -s https://opencode.ai/zen/v1/models | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d[\"data\"])} models')"

# Test chat (requires billing)
curl -s -X POST https://opencode.ai/zen/v1/chat/completions \
  -H "Authorization: Bearer $OPENCODE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-fable-5","messages":[{"role":"user","content":"Say OK"}],"max_tokens":10}'
```
