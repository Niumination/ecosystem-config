# Provider Scan & Model Selection — 29 Agustus 2026

## Konteks
User meminta scan semua provider + seleksi model untuk seluruh thread+DM+fallback, fokus free tier, hindari berbayar, pilih yang paling cepat+kuat+long limit.

## Hasil Sweep Provider

| Provider | /v1/models | Chat Test | Verdict |
|---|---|---|---|
| **9router** (localhost:20128) | 78 models | ✅ 7/17 kandidat OK | **PRIMARY** - paling stabil |
| **opencode-zen** | 64 models | ⚠️ 3/7 OK (big-pickle MATI!) | SECONDARY - limited |
| OpenRouter | 388 models (18 free) | ❌ 1/12 OK (429 massal) | Cadangan only |
| Huancheng | 20 models | ❌ SEMUA timeout | EXCLUDED |
| AgentRouter | 401 key ditolak | — | EXCLUDED |
| JuanRouter | 401 key ditolak | — | EXCLUDED |

## Stress Test Results (10 bursts per model)

### 9router — SEMUA LONG LIMIT ✅
| Model | Burst | Latency | Status |
|---|---|---|---|
| `ag/gemini-3.5-flash-low` | 10/10 | 729ms | 🟢 TERCEPAT |
| `ag/gemini-3.5-flash-extra-low` | 10/10 | 906ms | 🟢 |
| `gh/gpt-4o-mini` | 10/10 | 930ms | 🟢 |
| `ag/gemini-3-flash-agent` | 10/10 | 966ms | 🟢 Agent-optimized |
| `gemini/gemma-4-31b-it` | 10/10 | 1039ms | 🟢 Creative |
| `ag/gemini-3.6-flash-low` | 10/10 | 1101ms | 🟢 |
| `ag/gemini-3.7-flash-low` | 10/10 | 2483ms | 🟢 Terkuat |

### opencode-zen — SEBAGIAN MATI ❌
| Model | Burst (8x) | Status |
|---|---|---|
| `big-pickle` | 0/8 | ❌ HABIS quota |
| `laguna-s-2.1-free` | 5/8 | ⚠️ Sering 429 |
| `hy3-free` | 8/8 | 🟢 Satu-satunya stabil |

### OpenRouter free tier — 429 MASSAL ❌
Hanya `nvidia/nemotron-3-super-120b-a12b:free` 3/4 OK, sisanya 429.

## Rekomendasi Mapping (SUDAH DIPERLUKAN)

```yaml
model:
  provider: huancheng
  default: auto
  base_url: https://api.hcnsec.cn/v1
  api_mode: codex_responses

platforms:
  telegram:
    channel_overrides:
      '1':
        model: ag/gemini-3.5-flash-low
        provider: 9router
      '802':
        model: ag/gemini-3-flash-agent
        provider: 9router
      '803':
        model: gh/gpt-4o-mini
        provider: 9router
      '804':
        model: ag/gemini-3.7-flash-low
        provider: 9router
      '1172':
        model: gemini/gemma-4-31b-it
        provider: 9router

fallback_providers:
  - provider: 9router
    model: ag/gemini-3.5-flash-low
  - provider: 9router
    model: ag/gemini-3-flash-agent
  - provider: opencode-zen
    model: hy3-free
```

## ScriptReusable
- `~/.hermes/provider-sweep-rapid2.py` — Single probe per candidate
- `~/.hermes/burst-ultra.py` — 4-burst stress test (quick)
- `~/.hermes/limit-check-quick.py` — 10-burst limit check
- `~/.hermes/apply-mapping.py` — Apply config changes

## Lessons Learned
1. **Probe tunggal TIDAK cukup** — big-pickle 1/1 OK tapi 0/8 burst (quota habis)
2. **9router > opencode-zen** untuk free tier stabil saat ini
3. **Huancheng `/v1/models` 200 ≠ chat jalan** — semua inference timeout
4. **User preferensi DM = huancheng/auto** karena lebih sering dipakai di DM
5. **Gemini flash variants (prefix `ag/`) = longest limit** di 9router
