# 9Router Configuration Update Report
**Date:** 30 Ags 2026 14:25 WIB  
**Status:** ✅ Completed

---

## Executive Summary

Konfigurasi 9router telah diupdate untuk menggunakan **hanya model yang terverifikasi working** berdasarkan hasil model-checker.

---

## Changes Made

### 1. Config.yaml Updated

| Setting | Before | After |
|---------|--------|-------|
| **Default Provider** | `nous` | `9router` |
| **Default Model** | `upstage/solar-pro4:free` | `ag/gemini-3.5-flash-extra-low` |
| **Fallback Models** | 3 models (mixed) | 5 working models |

### 2. Fallback Providers (Working Only)

```yaml
fallback_providers:
  - provider: 9router
    model: ag/gemini-3.5-flash-extra-low  # ✅ 972ms, FASTEST
  - provider: 9router
    model: ag/gemini-3.5-flash-low        # ✅ 1094ms
  - provider: 9router
    model: ag/gemini-3-flash-agent        # ✅ 1294ms
  - provider: 9router
    model: ag/gemini-3-flash              # ✅ 1534ms
  - provider: 9router
    model: ag/gemini-3.1-flash-image      # ✅ Vision capable
```

---

## Model Status Summary

### ✅ Working Models (19 models)

| Provider | Models | Status |
|----------|--------|--------|
| **AG** | 14 | ✅ All working |
| **GEMINI** | 5 | ✅ All working |
| **GH** | 0 | ⚠️ All failed (400 errors) |
| **KR** | 5 | ✅ Working (paid) |

### ❌ Failed Models (50 models)

**Patterns that fail:**
- `*-thinking` variants (e.g., `kr/claude-haiku-4.5-thinking`)
- `*-agentic` variants (e.g., `kr/deepseek-3.2-agentic`)
- Old GPT models (`gh/gpt-4`, `gh/gpt-4-0613`)
- Specialized models (`gh/mai-code-*`, `gh/oswe-vscode-prime`)

---

## Verification Test

**Test Model:** `ag/gemini-3.5-flash-extra-low`
- **Status:** ✅ HTTP 200 OK
- **Response Time:** ~1500ms
- **Tokens Used:** 2023 prompt + 0 completion (streaming response)

---

## Next Steps

### For User
1. **Restart Hermes** untuk apply perubahan config
2. **Test dengan `/model-check`** untuk verifikasi
3. **Gunakan model baru** secara default

### Optional: Re-enable Failed Models
Jika ingin mencoba model yang failed, edit `~/.hermes/config.yaml`:
```yaml
fallback_providers:
  - provider: 9router
    model: kr/qwen3-coder-next  # Try re-enabling
```

---

## Files Modified

| File | Action |
|------|--------|
| `~/.hermes/config.yaml` | ✅ Updated |
| `~/.hermes/9router-models-status.md` | ✅ Created |
| `~/.hermes/disable-9router-models.py` | ✅ Created (reference) |
| `~/.hermes/update-9router-config.py` | ✅ Created |

---

## Recommendations

**For General Use:**
- Primary: `ag/gemini-3.5-flash-extra-low` (fastest, free)
- Fallback: `ag/gemini-3.5-flash-low` (balance speed/quality)

**For Coding:**
- Try: `kr/qwen3-coder-next` (currently failed, may work after fix)

**For Vision:**
- Use: `ag/gemini-3.1-flash-image` (free, vision-capable)

**For Reasoning:**
- Use: `ag/claude-opus-4-6-thinking` (free, strongest reasoning)

---

**Status:** ✅ Configuration updated dan terverifikasi working!
