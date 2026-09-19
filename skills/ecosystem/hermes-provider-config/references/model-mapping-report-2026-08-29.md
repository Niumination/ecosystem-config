# Model Mapping Report — Updated 29 Agustus 2026

## DM Utama (Default)
| Parameter | Value |
|-----------|-------|
| Provider | huancheng |
| Model | auto |
| Base URL | https://api.hcnsec.cn/v1 |
| API Mode | codex_responses |
| Status | ✅ Primary (user aktif pakai DM ini) |

## Thread Telegram Overrides
| Thread | Persona | Model | Provider | Test Result |
|--------|---------|-------|----------|-------------|
| 1 | General/Command Center | ag/gemini-3.5-flash-low | 9router | ✅ 10/10 burst, 729ms |
| 802 | Research/Riset | ag/gemini-3-flash-agent | 9router | ✅ 10/10 burst, 966ms |
| 803 | Programmer/Builder | gh/gpt-4o-mini | 9router | ✅ 10/10 burst, 930ms |
| 804 | QA/Pengawas | ag/gemini-3.7-flash-low | 9router | ✅ 10/10 burst, 2483ms |
| 1172 | Konten Kreator | gemini/gemma-4-31b-it | 9router | ✅ 10/10 burst, 1039ms |

## Fallback Chain (Global, 3 Level)
| Level | Provider | Model | Notes |
|-------|----------|-------|-------|
| L1 | 9router | ag/gemini-3.5-flash-low | Tercepat, long limit |
| L2 | 9router | ag/gemini-3-flash-agent | Agent-optimized |
| L3 | opencode-zen | hy3-free | Satu-satunya Zen stabil |

## Provider Status (29 Ags 2026)
| Provider | Status | Models | Notes |
|----------|--------|--------|-------|
| 9router | ✅ LIVE | 78 | Primary — semua flash variant long limit |
| huancheng | ⚠️ PARTIAL | 20 | DM default, chat OK tapi model ID case-sensitive |
| opencode-zen | ⚠️ LIMITED | 64 | Hanya hy3-free stabil; big-pickle & laguna 429 |
| openrouter | ❌ HEAVY 429 | 388 | Free tier rate-limited berat |
| agentrouter | ❌ REJECTED | — | Key 401 + blokir frasa ID |
| juan-router | ❌ REJECTED | — | Key 401 ditolak server |

## Perubahan dari Versi Sebelumnya (27 Ags)
1. DM switch dari opencode-zen/big-pickle → huancheng/auto (preferensi user)
2. Semua thread pindah ke 9router (lebih stabil daripada opencode-zen free tier)
3. Fallback chain diversifikasi: 9router × 2 + opencode-zen × 1
4. Thread 803 (Programmer) ganti dari cf/deepseek-r1-distill-qwen-32b → gh/gpt-4o-mini
5. Thread 1 (General) ganti dari gemini-3.5-flash-lite → ag/gemini-3.5-flash-low (lebih cepat)
6. Thread 804 (QA) ganti dari cf/glm-4.7-flash → ag/gemini-3.7-flash-low (versi lebih baru)

## Test Methodology
- Single probe: HTTP 200 + response content validation
- Burst test: 10 request beruntun (0.05s delay), hitung success rate
- Long limit threshold: ≥9/10 burst success = ACCEPTED
- All recommended models passed 10/10 burst test on 29 Ags 2026

## Config Location
- Main config: `~/.hermes/config.yaml`
- Backup: `~/.hermes/config.yaml.bak-before-model-mapping-20260829_*.yaml`
- Test results: `~/.hermes/provider-sweep-results.json`, `~/.hermes/live-test-results.json`
