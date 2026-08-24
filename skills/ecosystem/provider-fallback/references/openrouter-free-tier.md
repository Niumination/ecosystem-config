# OpenRouter Free Tier — Verified 2026-08-16

## Status
Key `sk-or-v1-...02b` VALID & free tier (`is_free_tier: true`, usage 0, no credit cap).
Simpan di `~/.config/openrouter/env` (`OPENROUTER_API_KEY=...`, chmod 600).

## Key Check
```bash
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $OPENROUTER_API_KEY"
# → data.is_free_tier, usage, limit_remaining (null = unlimited)
```

## Free-tier Rate Limits (model id berakhiran `:free`)
| Credits purchased (all time) | Req/min | Req/day |
|---|---|---|
| < $10 | 20 | 50 |
| ≥ $10 | 20 | 1000 |

- **402** = saldo negatif → free model ikut mati; top-up credit.
- **429** = rate limit → retry exponential backoff, honor `Retry-After`.
- Mid-stream 429 → SSE `finish_reason:"error"`.
- 50 req/hari cukup untuk dev/tes/cron — BUKAN produksi berat.

## Model :free yang TERBUKTI jalan (19 total, 413 model terdaftar)
- `google/gemma-4-26b-a4b-it:free` (262k ctx) — **diuji balas OK**
- `google/gemma-4-31b-it:free` (262k)
- `nvidia/nemotron-3-ultra-550b-a55b:free` (1M ctx, frontier reasoning)
- `nvidia/nemotron-3.5-lightning:free` (1M)
- `nvidia/nemotron-3-super-120b-a12b:free` (262k)
- `cohere/north-mini-code:free` (256k, agentic coding)
- `poolside/laguna-s-2.1:free` / `laguna-xs-2.1:free` (262k, coding agents)
- `openai/gpt-oss-20b:free` (131k)
- `openrouter/free` (200k, auto-pick model gratis terbaik)
- `dots-studio/dots-3-note-preview:free` (512k), `liquid/lfm-2.5-2.6b:free`, dll.

## Hermes Config Pattern
```yaml
providers:
  openrouter:
    base_url: https://openrouter.ai/api/v1
    api_mode: chat_completions
    key_env: OPENROUTER_API_KEY
```
Cocok sebagai fallback tier-2 (setelah 9router) untuk cron/tes murah.

## Catatan
- `:free` suffix = gratis 100%. Model "gratis" TANPA suffix tetap butuh credit minimum — jangan tertukar.
- 9router lokal (localhost:20128) adalah jalur utama; OpenRouter = cadangan bila 9router mati.
