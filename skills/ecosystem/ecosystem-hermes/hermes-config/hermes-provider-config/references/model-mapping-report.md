# Laporan Mapping Model Aktif — Template & Nilai Terkini (15 Ags 2026)

Format laporan "mapping model aktif" yang diminta user (audit berkala). Semua nilai harus
dari probe live + `hermes config get`, bukan klaim. Sumber: config.yaml aktif, channel_overrides
(dashboard server MC `modules/dispatch_store.py` THREAD_MODELS harus sinkron), probe chat.

## Struktur laporan

1. **Model utama** — `hermes config get model` (default + provider + base_url).
2. **Fallback chain** — `hermes config get fallback_providers` (urutan = prioritas).
3. **Thread Telegram** — `hermes config get platforms.telegram` → channel_overrides:
   thread 1 = general, 802 = research, 803 = programmer, 804 = qa, 1172 = kreator.
4. **Provider terdaftar** — semua key di `providers:` config.
5. **Probe live** — tiap model kritis di-chat-probe (script `scripts/probe-provider-models.py`),
   tandai ✅ 200 / ⚠️ 429 / ❌ error.

## Nilai terkini (15 Ags 2026 — snapshot, selalu re-probe)

| Bagian | Nilai |
|---|---|
| Model utama | `opencode-zen / big-pickle` (UA `opencode/1.18.18` wajib) |
| Fallback L1 | `juan-router / agnes-2.0-flash` ✅ (berbayar — saldo) |
| Fallback L2 | `9router / cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` ⚠️ sering 429 |
| Fallback L3 | `9router / gratislonggar` ✅ (alias → `gemini-3.1-flash-lite`) |
| Thread 1 | `9router / gemini/gemini-3.5-flash-lite` ✅ |
| Thread 802 | `9router / gc/gemini-2.5-pro` ✅ |
| Thread 803 | `9router / cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` ⚠️ 429 |
| Thread 804 | `9router / cf/@cf/zai-org/glm-4.7-flash` ⚠️ 429 |
| Thread 1172 | `9router / gemini/gemma-4-31b-it` ✅ |

## Catatan metodologi

- **429 ≠ model mati** — itu upstream rate limit (Cloudflare `cf/@cf/*`). Lapor sebagai ⚠️
  rate limit, jangan langsung ganti config. Retry dengan delay ≥6s untuk konfirmasi.
- **juan-router model list (6):** agnes-2.0-flash ✅, gemma-4-31b-it, laguna-s-2.1,
  laguna-xs-2.1, ling-3.0-flash-free ⚠️ (terdaftar tapi 401 not supported), mistral-large.
- **9router 38 model** — daftar lengkap via `curl localhost:20128/v1/models`.
- Kandidat upgrade thread 803/804 bila 429 terus: `JuanRouter/deepseek-v4-flash`,
  `JuanRouter/glm-5.2` (non-Cloudflare).
- Thread mapping di MC: `modules/dispatch_store.py` THREAD_MODELS — sinkronkan dengan
  config.yaml channel_overrides (dua-duanya sumber; drift = thread pakai model beda).
