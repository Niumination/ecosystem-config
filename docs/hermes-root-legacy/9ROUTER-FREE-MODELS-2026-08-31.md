# 🆓 Free & Low-Limit Models on 9router (current state)
**Date:** 06 Sep 2026
**Source:** live 9router catalog + verified HTTP-200 probe against `http://localhost:20128/v1`

---

## ✅ CURRENT ACTIVE CONFIG (verified working)

| Role | Model | Provider | Status |
|------|-------|----------|--------|
| Default | `explabs/gpt-5.4-mini` | 9router | ✅ Verified |
| Vision | `explabs/claude-fable-5` | 9router | ✅ Verified |
| Compression | `ag/gemini-3.7-flash-low` | 9router | ✅ Verified |
| Delegation | `explabs/gpt-5.4-mini` | 9router | ✅ Verified |
| X-search | `explabs/grok-4.20` | 9router | ✅ Verified |
| Cron | `explabs/gpt-5.4-mini` | 9router | ✅ Verified |
| Channel 1 | `explabs/gpt-5.4-mini` | 9router | ✅ Verified |
| Channel 802 | `explabs/claude-haiku-4.5` | 9router | ✅ Verified |
| Channel 803 | `explabs/gpt-4o-mini` | 9router | ✅ Verified |
| Channel 804 | `explabs/claude-sonnet-4.6` | 9router | ✅ Verified |
| Channel 1172 | `explabs/gemma-4-31b` | 9router | ✅ Verified |

---

## 🔎 CATALOG STATE

| Namespace | Count | Notes |
|-----------|-------|-------|
| `explabs/` | 313 | Primary working namespace |
| `ag/` | 20 | Antigravity / Google Gemini family |
| `claude-combo` | 1 | Combo model |

Deprecated namespaces no longer present in 9router:
- `gh/` → gone
- `kr/` → gone
- `gemini/` → gone
- `experimentallabs/` → replaced by `explabs/`

---

## ⚠️ RETIRED / UNSTABLE MODELS

These models returned errors during live probe and should not be used as primary mapping:

- `ag/gemini-3.5-flash-extra-low` → retired
- `ag/gemini-3.5-flash-low` → retired
- `ag/gemini-3.5-flash-high` → retired
- `ag/gemini-3.5-flash` → retired

---

## 📋 SELECTED WORKING MODELS

### `explabs/` selection
- `explabs/gpt-5.4-mini`
- `explabs/gpt-4o-mini`
- `explabs/claude-fable-5`
- `explabs/claude-haiku-4.5`
- `explabs/claude-sonnet-4.6`
- `explabs/gemma-4-31b`
- `explabs/grok-4.20`

### `ag/` selection
- `ag/gemini-3.7-flash-low`
- `ag/gemini-3.7-flash-medium`
- `ag/gemini-3.7-flash-high`
- `ag/gemini-3.8-flash-medium`
- `ag/gemini-3.8-flash-low`
- `ag/gemini-3.8-flash-high`
- `ag/claude-sonnet-4-6`
- `ag/claude-opus-4-6-thinking`

---

## 🧭 RULES

- Only use models verified by live HTTP-200 probe.
- Do not use retired `ag/gemini-3.5-*` models.
- Do not use old namespaces `gh/`, `kr/`, `gemini/`, `experimentallabs/`.
- Prefer `explabs/` for general tasks; prefer `ag/` only for Gemini-family tasks that are verified working.
