# Kimi Models on 9router — Investigation Report (29 Ags 2026)

## Summary
**Kimi models TIDAK TERSEDIA di 9router.** Semua model Moonshot AI telah dihapus/dipindahkan dari katalog 9router.

## Test Results

### Phase 1: Test Kimi Model IDs (10 models)
| Model | Status | Error |
|-------|--------|-------|
| kimi/kimi-k3 | ❌ | HTTP 404 |
| kimi/k3 | ❌ | HTTP 404 |
| kimi/kimi-for-coding | ❌ | HTTP 404 |
| kimi/kimi-for-coding-highspeed | ❌ | HTTP 404 |
| kimi/kimi-k2.7-code | ❌ | HTTP 404 |
| kimi/kimi-k2.7-code-highspeed | ❌ | HTTP 404 |
| kimi/kimi-k2.6 | ❌ | HTTP 404 |
| kimi/kimi-k2.5 | ❌ | HTTP 404 |
| kimi/kimi-k2.5-thinking | ❌ | HTTP 404 |
| kimi/kimi-latest | ❌ | HTTP 404 |

**Result:** 0/10 working (0%)

### Phase 2: Check Full Model Catalog
- Total models on 9router: **89 models**
- Kimi-related models: **0 models**
- Kimi/Moonshot prefix: **Not found**

### Phase 3: Alternative Testing (kr/ prefix)
Tested models with `kr/` prefix (possible rebranding):
| Model | Status | Latency |
|-------|--------|---------|
| kr/deepseek-3.2 | ✅ OK | 3402ms |
| kr/glm-5 | ❌ Timeout | — |
| kr/minimax-m2.5 | ✅ OK | 4245ms |
| kr/qwen3-coder-next | ✅ OK | 1018ms |
| kr/claude-haiku-4.5 | ✅ OK | 1302ms |
| kr/claude-sonnet-4 | ✅ OK | 2558ms |

**Result:** 5/6 working (83%), but these are NOT kimi models.

## Available Model Prefixes on 9router
| Prefix | Count | Description |
|--------|-------|-------------|
| `ag` | 16 | Gemini flash variants, Claude, GPT-oss |
| `gemini` | 7 | Google Gemini models |
| `gh` | 32 | GPT variants, Claude Haiku, coding models |
| `kr` | 34 | DeepSeek, GLM, MiniMax, Qwen, Claude |

## Conclusion
1. **Kimi models tidak tersedia di 9router** — telah dihapus atau dipindahkan
2. **Tidak ada model Moonshot AI** di katalog saat ini
3. **Alternatif tersedia:**
   - `kr/qwen3-coder-next` (1018ms) — untuk coding
   - `kr/deepseek-3.2` (3402ms) — untuk general use
   - `kr/claude-haiku-4.5` (1302ms) — untuk fast responses
   - `kr/claude-sonnet-4` (2558ms) — untuk reasoning

## Recommendation
Jika user membutuhkan model mirip Kimi (coding/agentic), gunakan:
- `kr/qwen3-coder-next` — coding-focused, fastest (1018ms)
- `kr/deepseek-3.2` — general purpose, proven stable

Atau pertimbangkan provider lain seperti OpenRouter yang masih memiliki `moonshotai/kimi-k3`.
