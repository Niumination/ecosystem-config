# Provider & Model Audit — 18 Agustus 2026 (sweep penuh dengan auth)

Metode: probe `/v1/models` DENGAN Authorization header dari `data/.env` + User-Agent `hermes-agent/0.19.0`, lalu chat-completion test per model kandidat (tool-calling payload + JSON mode).

## Hasil probe per provider

| Provider | /v1/models | Total model | Chat/tool-call | Verdict |
|---|---|---|---|---|
| opencode-zen (opencode.ai/zen/v1) | 200 | 62 | big-pickle & deepseek-v4-flash-free → **429 FreeUsageLimitError** | Primary, kuota free HABIS |
| 9router (localhost:20128) | 200 | 39 | gratislonggar ✅ (SSE!), gemini/gemini-3.7-flash ✅ 1.1s | Layak fallback |
| huancheng (api.hcnsec.cn) | 200 | 20 | **SEMUA model timeout di inference** (DeepSeek-V4-Flash, glm-5.2, Kimi-K2.6, MiniMax-M3, DeepSeek-V4-Pro) | TIDAK layak — list OK, chat mati |
| openrouter (openrouter.ai) | 200 | 412 (15 `:free`) | openai/gpt-oss-20b:free ✅ 12.2s tool-call, JSON mode ❌; google/gemma-4-31b-it:free → 429 | Layak cadangan |
| nvidia_nim (integrate.api.nvidia.com) | 200 | 102 | meta/llama-3.1-8b-instruct ✅ 0.7s tool-call | Layak cadangan |
| juan-router (router.juan.web.id) | **401** | — | key ditolak server (bukan false positive — sudah dengan auth) | ❌ |
| agentrouter (agentrouter.org) | **401** | — | key ditolak server | ❌ |
| aerolink | key ada | — | URL tidak ada di config aktif | tidak aktif |

## Model opencode-zen family free (62 total)

`big-pickle` (429), `deepseek-v4-flash-free` (429), `mimo-v2.5-free` (429), `hy3-free` ✅ 3.6s tool-call, `nemotron-3-ultra-free` ✅ 17s, `nemotron-3.5-lightning-free` ✅ 33s (lambat), `laguna-s-2.1-free` ✅ 3.6s tool-call.
Berbayar: `deepseek-v4-flash` → 401 CreditsError (belum ada payment method).

## Hasil tool-calling test (payload: tools=[hitung], "Pakai tool hitung untuk 15+27")

| Model | Latency | Hasil |
|---|---|---|
| 9router `gemini/gemini-3.7-flash` | 1.1s | ✅ TOOL_CALL hitung args={a:15,b:27} |
| 9router `gratislonggar` | 9.2s | ✅ TOOL_CALL (SSE-only — parse `data:` lines) |
| nvidia `meta/llama-3.1-8b-instruct` | 0.7s | ✅ TOOL_CALL |
| openrouter `openai/gpt-oss-20b:free` | 12.2s | ✅ TOOL_CALL, JSON mode ❌ NoneType |
| zen `hy3-free` / `laguna-s-2.1-free` | 3.6s | ✅ TOOL_CALL |
| zen `nemotron-3-ultra-free` | 17s | ✅ TOOL_CALL |
| huancheng semua model | timeout | ❌ |

## Rekomendasi config saat Zen 429 (disarankan, BELUM diterapkan)

```yaml
fallback_providers:
  - provider: opencode-zen
    model: hy3-free          # keluarga SAMA, hidup saat big-pickle 429
  - provider: opencode-zen
    model: laguna-s-2.1-free
  - provider: 9router
    model: gemini/gemini-3.7-flash   # setelah probe 200
```

## Pitfall yang terkonfirmasi ulang

1. **401 palsu:** probe tanpa Authorization → semua provider remote tampak 401. Selalu bawa key.
2. **SSE walau `stream:false`:** gratislonggar balas `data: {...}` chunks — parser harus handle dua bentuk response.
3. **429 bukan config:** `FreeUsageLimitError` = kuota harian free habis; jangan ubah config, tunggu reset atau pindah keluarga model.
4. **Listed ≠ usable:** huancheng list 20 model tapi inference timeout semua — `/v1/models` 200 TIDAK membuktikan chat jalan.
