# Fallback Chain Selection & 9router Diagnostics (2026-08-13)

## Konteks
Thread #general error total: `gemini-3.5-flash-lite` kena 429 (kuota) → fallback `9router/auto` → `404 No active credentials for provider: openai` → `Non-retryable client error` ke user. Fix: ganti fallback `auto` dengan chain 3 level hasil stress-test.

## Error chain di gateway (panduan diagnosa cepat)
`logs/errors.log` urutan 3 sinyal:
1. `429 You exceeded your current quota` — provider utama kena rate limit (Gemini: ~20 req/jam)
2. `404 No active credentials for provider: openai` — fallback `auto` resolve ke provider tanpa kredensial
3. `Non-retryable client error` — error total ke user (retry habis)

Sinyal 2+3 = fallback HARUS diganti dari `auto` ke model eksplisit.

## Chain yang terpasang
```yaml
fallback_providers:
  - provider: 9router
    model: JuanRouter/glm-5.2
  - provider: 9router
    model: cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b
  - provider: 9router
    model: gratislonggar
```
Verifikasi runtime: `get_fallback_chain()` dari `hermes_cli/fallback_config.py` → 3 level. Gateway auto-refresh per turn (`gateway/run.py` `_refresh_fallback_model`, baca disk tiap agent create/reuse).

## Hasil stress test (8 request beruntun cepat, max_tokens=5, stream:false)
| Model | Sukses |
|---|---|
| gratislonggar (combo) | 8/8 |
| gemini/gemini-3.5-flash-lite | 8/8 |
| gemini/gemma-4-31b-it | 8/8 |
| cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b | 8/8 |
| JuanRouter/glm-5.2 | 8/8 |
| JuanRouter/gemini-3.5-flash-lite | 8/8 |
| JuanRouter/gemini-3.6-flash | 8/8 |
| JuanRouter/qwen3.7-plus | 8/8 |
| gemini/gemini-3.6-flash | 7/8 |
| gc/gemini-2.5-flash-lite | 4/8 |
| gc/gemini-2.5-flash | 2/8 |
| nvidia/z-ai/glm-5.2 | 2/8 |

**Pelajaran kunci:** `nvidia/z-ai/glm-5.2` (jalur Nvidia, model utama thread 804) LEMAH 2/8 sedangkan `JuanRouter/glm-5.2` (jalur router.juan.web.id) 8/8 — model sama, kuota beda per jalur. Setelah 9router update provider, selalu re-stress-test jalur yang dipakai thread.

## Recipe: probe + stress test (Python)
- Key: `NINE_ROUTER_API_KEY` dari `/Volumes/HermesAgent/HermesAgentUSB/data/.env`
- Endpoint: `http://localhost:20128/v1/chat/completions`
- WAJIB `stream:false` + parser SSE — 9router kadang balas SSE (`data: {...}` lines) walau minta JSON; plain `json.loads` gagal (`Expecting value` / `Extra data`)
- Parser SSE: loop tiap line; `line.startswith('data:')` → `json.loads(line[5:].strip())`; kumpulkan `choices[].delta.content`; abaikan `[DONE]`
- Interpretasi: HTTP 429 = rate limit (ganti jalur); 404 `No active credentials` = provider tanpa kredensial (bukan model mati); 530 = error upstream provider

## Diagnostik 9router (lokal, port 20128)
- Versi & startup: `~/.9router/logs/stdout.log` (`🚀 9router v0.5.50`); proses `ps aux | grep 9router`
- Daftar model: `curl http://localhost:20128/v1/models` (format OpenAI: `data[].id`)
- DB konfigurasi: `~/.9router/db/data.sqlite` (SQLite):
  - `providerNodes` — `SELECT id, type, name, substr(data,1,120) FROM providerNodes;` → prefix/baseUrl tiap node (contoh: openai-compatible "JuanRouter" → router.juan.web.id/v1)
  - `providerConnections` — apiKey + `testStatus` (active/error) tiap kredensial
- Update provider (via opencode/9router app) mengubah DB — Hermes TIDAK tahu otomatis; selalu re-probe `/v1/models` setelah update untuk cek model baru/berubah
- v0.5.50 (2026-08-13): 33 model; baru `JuanRouter/*` (15 model: gemini-3.1-pro, glm-5.2, gpt-5.6-luna, grok-4.5/4.6, kimi-k2.7/k3, qwen3.7-plus, qwen3.8-max, dll) + combo `gratislonggar`

## Batasan fallback Hermes (dari source)
- `ChannelOverride` (`gateway/config.py:514`) hanya punya `model`, `provider`, `system_prompt` — TIDAK ada field fallback per-channel
- `fallback_model` (legacy) vs `fallback_providers` (baru): keduanya digabung oleh `get_fallback_chain()` (`hermes_cli/fallback_config.py:71`), urutan = prioritas, dedup by provider/model/base_url
- Fallback = GLOBAL: semua thread + DM + cron pakai chain yang sama
