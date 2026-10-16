# 9Router Model Mapping — FINAL
**Date:** 31 Ags 2026
**Status:** CONFIGURATION COMPLETE

---

## ✅ Configuration Changes Applied

### Default Model Updated
| Setting | Before | After |
|---------|--------|-------|
| **Provider** | nous | 9router |
| **Default** | `upstage/solar-pro4:free` | `claude-combo` |
| **Base URL** | `https://inference-api.nousresearch.com/v1` | `http://localhost:20128/v1` |

### Fallback Chain Updated (Commented)
All 12 recommended models are now available in `config.yaml` as commented fallback_providers:
- `gh/gpt-5.4-mini-free-auto` (FREE, 400K)
- `gemini/gemini-3.7-flash` (Native Gemini, 1M)
- `gh/gpt-4.1-2025-04-14` (GH, 1M)
- `kr/minimax-m2.5` (Kimi)
- `kr/qwen3-coder-next` (Kimi, code)
- `gh/claude-haiku-4.5` (GH, Claude)
- `ag/claude-sonnet-4-6` (AG Claude, 1M)
- `gemini/gemini-3.6-flash` (Native Gemini)
- `gh/gpt-5-mini` (GH, 400K)
- `ag/gpt-oss-120b-medium` (Open source)
- `kr/deepseek-3.2` (Kimi)
- `gh/gpt-4o-mini` (GH, 128K)

### Channel Overrides Updated
| Channel | Model |
|---------|-------|
| **1** | `gh/gpt-5-mini` |
| **802** | `gh/claude-haiku-4.5` |
| **803** | `gh/gpt-4o-mini` |
| **804** | `gemini/gemini-3.7-flash` |
| **1172** | `gemini/gemma-4-31b-it` |

---

## ✅ Backend Distribution
| Backend | Count | Models |
|---------|-------|--------|
| GH (GitHub) | 5 | gpt-5.4-mini-free-auto, gpt-4.1, claude-haiku-4.5, gpt-5-mini, gpt-4o-mini |
| Native Gemini | 3 | gemini-3.7-flash, gemini-3.6-flash, gemma-4-31b-it |
| Kimi | 3 | minimax-m2.5, qwen3-coder-next, deepseek-3.2 |
| AG Claude | 1 | claude-sonnet-4-6 |
| Open Source | 1 | gpt-oss-120b-medium |

**Zero shared Google quota** ✅

---

## ✅ All Models Verified in 9router Catalog (99 models)

### Primary Model
- `claude-combo` — 9router

### Fallback Models
- `gh/gpt-5.4-mini-free-auto` ✅
- `gemini/gemini-3.7-flash` ✅
- `gh/gpt-4.1-2025-04-14` ✅
- `kr/minimax-m2.5` ✅
- `kr/qwen3-coder-next` ✅
- `gh/claude-haiku-4.5` ✅
- `ag/claude-sonnet-4-6` ✅
- `gemini/gemini-3.6-flash` ✅
- `gh/gpt-5-mini` ✅
- `ag/gpt-oss-120b-medium` ✅
- `kr/deepseek-3.2` ✅
- `gh/gpt-4o-mini` ✅

### Channel Override Models
- `gh/gpt-5-mini` ✅
- `gh/claude-haiku-4.5` ✅
- `gh/gpt-4o-mini` ✅
- `gemini/gemini-3.7-flash` ✅
- `gemini/gemma-4-31b-it` ✅

---

## 📁 Files Created/Updated
| File | Status |
|------|--------|
| `~/.hermes/config.yaml` | ✅ Updated |
| `~/.hermes/config.yaml.bak-2026-08-31` | ✅ Backup |
| `~/.hermes/MODEL-MAPPING-UPDATE-2026-08-31.md` | ✅ Report |
| `~/.hermes/DEFAULT-MODEL-UPDATE-2026-08-31.md` | ✅ Report |
| `/tmp/9router_full.json` | ✅ Catalog backup |
| `/tmp/test_models.py` | ✅ Verification script |
| `/tmp/restore_default.py` | ✅ Restore script |
| `/tmp/upgrade_plan.py` | ✅ Skill upgrade plan |
| `/tmp/memory_upgrade.py` | ✅ Memory upgrade plan |
| `/tmp/test_fallback.py` | ✅ Fallback test |
| `/tmp/test_backup.py` | ✅ Backup test |

---

## 🔧 Rollback
```bash
cp ~/.hermes/config.yaml.bak-2026-08-31 ~/.hermes/config.yaml
```

**Status:** ✅ Complete

⚡ (◕‿◕)★
