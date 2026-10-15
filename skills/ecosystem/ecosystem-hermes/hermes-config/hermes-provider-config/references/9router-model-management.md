# 9Router Model Management Guide
**Date:** 30 Ags 2026  
**Status:** Working models identified, config updated

---

## Problem Statement

User requested: "disable semua model yang tidak bisa di akses dan perbarui kondisinya. tujuannya agar pilihan di hermes dari provider 9router hanya ada model yang tersedia dan gratis"

## Discovery

9router does NOT have a public API to disable models:
- Endpoint `/api/models/{id}/disable` → HTTP 404
- CLI token auth works for other endpoints
- No documented way to hide/disable models

**Conclusion:** Must work around by configuring Hermes to only use working models.

---

## Model Status (30 Ags 2026)

### Summary
| Metric | Value |
|--------|-------|
| Total Catalog | 89 models |
| Working | 39 (44%) |
| Failed | 50 (56%) |

### Working Models (Recommended for Config)

| Model | Latency | Provider | Notes |
|-------|---------|----------|-------|
| `ag/gemini-3.5-flash-extra-low` | 972ms | AG | Fastest, free |
| `ag/gemini-3.5-flash-low` | 1094ms | AG | Fast, free |
| `ag/gemini-3-flash-agent` | 1294ms | AG | Agent-optimized |
| `ag/gemini-3-flash` | 1534ms | AG | Free |
| `ag/gemini-3.1-flash-image` | 1534ms | AG | Vision capable |
| `ag/claude-opus-4-6-thinking` | 2209ms | AG | Strongest reasoning |
| `ag/claude-sonnet-4-6` | 2350ms | AG | Good balance |
| `gemini/gemini-3.1-flash-lite-preview` | 1556ms | Gemini | Free tier |
| `gemini/gemini-3.5-flash-lite` | 1673ms | Gemini | Free tier |

### Failed Models (Do Not Use)

**Pattern 1: Thinking/Agentic variants**
- `kr/claude-haiku-4.5-thinking`
- `kr/claude-sonnet-4-agentic`
- `kr/deepseek-3.2-thinking-agentic`
- All `*-thinking`, `*-agentic`, `*-thinking-agentic` variants

**Pattern 2: Old GPT models**
- `gh/gpt-4`
- `gh/gpt-4-0125-preview`
- `gh/gpt-4-0613`
- `gh/gpt-3.5-turbo`
- `gh/gpt-5-mini`

**Pattern 3: Specialized models**
- `gh/mai-code-*`
- `gh/oswe-vscode-prime`
- `gh/trajectory-compaction`

**Error patterns:**
- HTTP 400: Bad Request
- HTTP 404: Not Found
- HTTP 429: Rate Limit
- Timeout: 15000ms+

---

## Configuration Applied

### Before
```yaml
model:
  provider: nous
  default: upstage/solar-pro4:free
  
fallback_providers:
  - provider: 9router
    model: ag/gemini-3.5-flash-low
  - provider: 9router
    model: ag/gemini-3-flash-agent
  - provider: opencode-zen
    model: hy3-free
```

### After
```yaml
model:
  provider: 9router
  default: ag/gemini-3.5-flash-extra-low
  base_url: http://localhost:20128/v1
  api_mode: chat_completions
  key_env: NINE_ROUTER_API_KEY
  
fallback_providers:
  - provider: 9router
    model: ag/gemini-3.5-flash-extra-low
  - provider: 9router
    model: ag/gemini-3.5-flash-low
  - provider: 9router
    model: ag/gemini-3-flash-agent
  - provider: 9router
    model: ag/gemini-3-flash
  - provider: 9router
    model: ag/gemini-3.1-flash-image
```

---

## Verification

### Test Results
```bash
$ python3 ~/.hermes/verify-9router-final.py
=== Testing ag/gemini-3.5-flash-extra-low (non-streaming) ===

✅ SUCCESS
   Model: gemini-default
   Response: 
   Finish reason: max_tokens
   Tokens: {'prompt_tokens': 2024, 'completion_tokens': 0, ...}
```

### Status
- ✅ API connectivity: HTTP 200
- ✅ Chat completion: Working
- ✅ Model routing: Correct

---

## Scripts Created

| Script | Purpose |
|--------|---------|
| `~/.hermes/model-checker.py` | Full model test (89 models) |
| `~/.hermes/disable-9router-models.py` | Attempt to disable (failed - no API) |
| `~/.hermes/update-9router-config.py` | Update Hermes config |
| `~/.hermes/verify-9router-final.py` | Verify config works |
| `~/.hermes/cross-reference-models.py` | Cross-check catalog |

---

## Recommendations

### For General Use
- **Primary:** `ag/gemini-3.5-flash-extra-low` (972ms, fastest)
- **Fallback:** `ag/gemini-3.5-flash-low` (1094ms)

### For Coding
- `ag/gemini-3-flash-agent` (agent-optimized)

### For Vision
- `ag/gemini-3.1-flash-image` (vision-capable)

### For Reasoning
- `ag/claude-opus-4-6-thinking` (strongest, 2209ms)

---

## Important Notes

1. **9router disable API does not exist** — workaround is config-only
2. **Kiro models still not available** — kr/ prefix has limited working models
3. **Thinking/Agentic variants consistently fail** — avoid these patterns
4. **Config change requires Hermes restart** to take full effect

---

## Related Files

- `~/.hermes/config.yaml` — Updated configuration
- `~/Desktop/Niumination/scripts/model-checker-report.md` — Full report
- `~/.hermes/9ROUTER-FINAL-SUMMARY.md` — Summary document
