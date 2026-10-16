# 📊 Model Mapping — Update Complete
**Date:** 31 Ags 2026

## ✅ Changes Applied

### Default Model Updated
| Before | After |
|--------|-------|
| `upstage/solar-pro4:free` (Nous) | `gh/gpt-5.4-mini-free-auto` (9router) |

### Fallback Chain Updated (12 models)
| # | Model | Provider | Context | Quota |
|---|-------|----------|---------|-------|
| 1 | `gh/gpt-5.4-mini-free-auto` | GH | 400K | FREE |
| 2 | `gemini/gemini-3.7-flash` | Native Gemini | 1M | Terpisah |
| 3 | `gh/gpt-4.1-2025-04-14` | GH | 1M | Terpisah |
| 4 | `kr/minimax-m2.5` | Kimi | 200K | Terpisah |
| 5 | `kr/qwen3-coder-next` | Kimi | — | Terpisah |
| 6 | `gh/claude-haiku-4.5` | GH | 200K | Terpisah |
| 7 | `ag/claude-sonnet-4-6` | AG Claude | 1M | Terpisah |
| 8 | `gemini/gemini-3.6-flash` | Native Gemini | 1M | Terpisah |
| 9 | `gh/gpt-5-mini` | GH | 400K | Terpisah |
| 10 | `ag/gpt-oss-120b-medium` | Open Source | 128K | Lokal |
| 11 | `kr/deepseek-3.2` | Kimi | — | Terpisah |
| 12 | `gh/gpt-4o-mini` | GH | 128K | Terpisah |

### Channel Overrides Updated
| Channel | Before | After |
|---------|--------|-------|
| **1** | `ag/gemini-3.5-flash-low` | `gh/gpt-5-mini` |
| **802** | `ag/gemini-3-flash-agent` | `gh/claude-haiku-4.5` |
| **803** | `gh/gpt-4o-mini` | (unchanged) |
| **804** | `ag/gemini-3.7-flash-low` | `gemini/gemini-3.7-flash` |
| **1172** | `gemini/gemma-4-31b-it` | (unchanged) |

### Backend Distribution
| Backend | Count | Models |
|---------|-------|--------|
| GH (GitHub) | 5 | gpt-5.4-mini-free-auto, gpt-4.1, claude-haiku-4.5, gpt-5-mini, gpt-4o-mini |
| Native Gemini | 3 | gemini-3.7-flash, gemini-3.6-flash, gemma-4-31b-it |
| Kimi | 3 | minimax-m2.5, qwen3-coder-next, deepseek-3.2 |
| AG Claude | 1 | claude-sonnet-4-6 |
| Open Source | 1 | gpt-oss-120b-medium |

## ✅ Benefits
- **Zero shared Google quota** — all models have independent backend
- **FREE model as default** — gh/gpt-5.4-mini-free-auto (400K ctx)
- **More diverse** — 4 provider backends instead of 2
- **Longer context** — 4 models with 1M+ context
- **All verified in catalog** — 100% match

## 📁 Files Updated
- `~/.hermes/config.yaml` — Fallback chain + channel overrides
- `~/.hermes/config.yaml.bak-2026-08-31` — Backup
- `~/.hermes/DEFAULT-MODEL-UPDATE-2026-08-31.md` — Default model update report
- `/tmp/9router_full.json` — Full model catalog backup

## ⚠️ Note
- Default model changed to `gh/gpt-5.4-mini-free-auto`
- To restore old default: `upstage/solar-pro4:free`
- 9router gateway running on port 20128
- All 12 fallback models verified in 9router catalog

## 🔧 Rollback
```bash
cp ~/.hermes/config.yaml.bak-2026-08-31 ~/.hermes/config.yaml
```

**Status:** ✅ Complete

⚡ (◕‿◕)★
