# Provider Sweep & Model Selection Report — 29 Agustus 2026

## Executive Summary
Sweep lengkap 6 provider + stress-test 20+ kandidat model. **9router adalah primary provider** (tercepat + paling stabil). **Huancheng untuk DM utama** (preferensi user). **Opencode-zen hanya hy3-free yang stabil**.

## Provider Status
| Provider | Status | Models | Chat Test | Verdict |
|----------|--------|--------|-----------|---------|
| **9router** (localhost:20128) | ✅ LIVE | 78 | 7/17 OK | **PRIMARY** — all flash variants long limit |
| **huancheng** (api.hcnsec.cn) | ⚠️ PARTIAL | 20 | DM auto OK | DM default, tapi case-sensitive model ID |
| **opencode-zen** (opencode.ai/zen) | ⚠️ LIMITED | 64 | 3/7 OK | Hanya hy3-free stabil; big-pickle & laguna 429 |
| **openrouter** | ❌ HEAVY 429 | 388 | 1/12 OK | Free tier rate-limited berat |
| **agentrouter** | ❌ REJECTED | — | 401 | Key ditolak + blokir frasa ID |
| **juan-router** | ❌ REJECTED | — | 401 | Key ditolak server |

## Recommended Models (10/10 Burst Test)
| Model | Provider | Latency | Use Case |
|-------|----------|---------|----------|
| `ag/gemini-3.5-flash-low` | 9router | 729ms | DM/Thread 1 — tercepat |
| `ag/gemini-3-flash-agent` | 9router | 966ms | Thread 802 — agent-optimized |
| `gh/gpt-4o-mini` | 9router | 930ms | Thread 803 — coding proven |
| `ag/gemini-3.7-flash-low` | 9router | 2483ms | Thread 804 — strong reasoning |
| `gemini/gemma-4-31b-it` | 9router | 1039ms | Thread 1172 — creative quality |
| `hy3-free` | opencode-zen | 2510ms | Fallback L3 — satu-satunya Zen stabil |

## Fallback Chain (3 Level)
```yaml
fallback_providers:
  - provider: 9router
    model: ag/gemini-3.5-flash-low   # L1: tercepat
  - provider: 9router
    model: ag/gemini-3-flash-agent   # L2: agent-optimized
  - provider: opencode-zen
    model: hy3-free                  # L3: cadangan
```

## DM Main Model
```yaml
model:
  provider: huancheng
  default: auto
  base_url: https://api.hcnsec.cn/v1
  api_mode: codex_responses
```

## Excluded Models ( dengan alasan )
| Model | Provider | Reason |
|-------|----------|--------|
| `big-pickle` | opencode-zen | 0/8 burst — kuota free habis |
| `laguna-s-2.1-free` | opencode-zen | 5/8 burst — sering 429 |
| `nemotron-3-ultra-free` | opencode-zen | 0/8 burst — mati |
| All :free models | openrouter | 429 rate limit berat |
| All models | huancheng | Timeout semua chat (kecuali DM auto) |
| All models | agentrouter | Key 401 + content filter blokir frasa ID |
| All models | juan-router | Key 401 ditolak server |

## Test Methodology
1. **Model List**: `GET /v1/models` dengan Authorization header
2. **Single Probe**: 1 request, max_tokens=5, stream=false, timeout=8s
3. **Burst Test**: 10 request beruntun (0.05s delay), hitung success rate
4. **Long Limit Threshold**: ≥9/10 burst success = ACCEPTED

## Files Generated
- `~/.hermes/provider-sweep-results.json` — Full sweep results
- `~/.hermes/live-test-results.json` — Live test (8 bursts)
- `~/.hermes/extended-stress-test.json` — Extended test (20 bursts, timed out)
- `~/.hermes/provider-sweep-2026-08-29.json` — Original sweep

## Config Backup
- `~/.hermes/config.yaml.bak-before-model-mapping-*.yaml`

## Next Actions
✅ Config.yaml sudah di-update (29 Ags 2026)
✅ Skill documentation updated
⏳ Monitor thread performance 24-48 jam ke depan
⏳ Re-test monthly atau jika ada perubahan quota
