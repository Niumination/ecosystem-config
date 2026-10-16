# 📊 Model Mapping Activation Test Results
**Date:** 06 Sep 2026
**Test Type:** Live verification against current 9router catalog + HTTP-200 probe

---

## ✅ PRIMARY MODEL — CONFIRMED ACTIVE
| Item | Status |
|------|--------|
| **Provider** | 9router (`http://localhost:20128/v1`) |
| **Model** | `explabs/gpt-5.4-mini` |
| **API Mode** | chat_completions |
| **Key** | `NINE_ROUTER_API_KEY` |
| **Status** | ✅ ACTIVE |

---

## 🔌 9ROUTER CATALOG — CURRENT STATE
| Item | Status |
|------|--------|
| **Base URL** | `http://localhost:20128/v1` |
| **Catalog Size** | 334 models |
| **Active Namespace** | `explabs/`, `ag/`, `claude-combo` |
| **Status** | ✅ RUNNING |

Deprecated namespaces: `gh/`, `kr/`, `gemini/`, `experimentallabs/`

---

## ✅ CONFIGURED MODELS — ALL VERIFIED
| Role | Model | Verified |
|------|-------|----------|
| Default | `explabs/gpt-5.4-mini` | ✅ |
| Vision | `explabs/claude-fable-5` | ✅ |
| Compression | `ag/gemini-3.7-flash-low` | ✅ |
| Delegation | `explabs/gpt-5.4-mini` | ✅ |
| X-search | `explabs/grok-4.20` | ✅ |
| Cron | `explabs/gpt-5.4-mini` | ✅ |
| Channel 1 | `explabs/gpt-5.4-mini` | ✅ |
| Channel 802 | `explabs/claude-haiku-4.5` | ✅ |
| Channel 803 | `explabs/gpt-4o-mini` | ✅ |
| Channel 804 | `explabs/claude-sonnet-4.6` | ✅ |
| Channel 1172 | `explabs/gemma-4-31b` | ✅ |

---

## ⚠️ RETIRED / DO NOT USE
- `ag/gemini-3.5-flash-extra-low` → retired
- `ag/gemini-3.5-flash-low` → retired
- `ag/gemini-3.5-flash-high` → retired
- `ag/gemini-3.5-flash` → retired
- Old namespaces: `gh/*`, `kr/*`, `gemini/*`, `experimentallabs/*`

---

## ✅ OTHER CONFIGURED PROVIDERS
| Provider | Base URL | Status |
|----------|----------|--------|
| agentrouter | `https://agentrouter.org/v1` | ✅ Configured |
| huancheng | `https://api.hcnsec.cn/v1` | ✅ Configured |

---

## 📋 NOTES
- All configured models passed live HTTP-200 probe on 06 Sep 2026.
- Mapping source: verified live catalog, not assumed availability.
- If a model starts returning 404/429/503, re-run probe before changing fallback order.
