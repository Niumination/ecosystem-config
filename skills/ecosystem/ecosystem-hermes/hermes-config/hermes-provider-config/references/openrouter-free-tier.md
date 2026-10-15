# OpenRouter Free Tier — Key Check, Model, Limits

> Verified 2026-08-16 dengan key free tier nyata (is_free_tier: true, usage 0). Key aktif tersimpan di `/Users/zaryu/.config/openrouter/env` (chmod 600, format `OPENROUTER_API_KEY=sk-or-v1-...`).

## 1. Cek key (sebelum dipasang)

```bash
curl -s https://openrouter.ai/api/v1/key -H "Authorization: Bearer $OPENROUTER_API_KEY"
```
Field penting: `is_free_tier` (belum pernah beli credit), `usage*` (0 = baru), `limit_remaining` (null = tanpa cap credit), `expires_at` (null = tidak expire), `rate_limit` (deprecated, abaikan).

## 2. Rate limit model `:free` (docs resmi — 2 jenis limit)

| Credit dibeli (all time) | req/menit | req/hari |
|---|---|---|
| < $10 | 20 | **50** |
| ≥ $10 | 20 | 1000 |

- **50 req/hari cukup untuk dev/tes/cron ringan — TIDAK untuk produksi** (thread MC aktif bisa 240+ pesan/hari).
- `402` = saldo akun ≤ 0 → **model free ikut mati** (cek `limit_remaining` via `/api/v1/key`).
- `429` = rate limit → retry exponential backoff, honor header `Retry-After`; header `X-RateLimit-*` HANYA ada di error response (sukses tidak membawanya).
- Rate limit mid-stream → SSE event `finish_reason: "error"` (bukan HTTP 429, status 200 sudah terkirim).
- DDoS protection Cloudflare = lapis kedua.

## 3. Model gratis (19 per 2026-08-16, dari `/api/v1/models` filter `pricing.prompt == "0"`)

Highlight (context_length):
- `nvidia/nemotron-3-ultra-550b-a55b:free` — 1M, frontier reasoning
- `nvidia/nemotron-3.5-lightning:free` — 1M
- `cohere/north-mini-code:free` — 256k, agentic coding
- `poolside/laguna-s-2.1:free` / `laguna-xs-2.1:free` — 262k, coding
- `google/gemma-4-26b-a4b-it:free` / `gemma-4-31b-it:free` — 262k (**sudah dites 200 OK**)
- `openai/gpt-oss-20b:free` — 131k
- `openrouter/free` — 200k, auto-pilih model gratis terbaik
- Lainnya: dots-3-note-preview, liquid/lfm-2.5-2.6b, poolside, nvidia nano series, lyria (audio, berbayar per klip)

Catatan: model `:free` = gratis selamanya. Ada model "gratis" TANPA `:free` (harga $0) yang tetap butuh saldo > $0 di akun — cek dengan chat-probe, jangan andalkan harga saja.

## 4. Uji pakai (non-streaming, model gratis)

```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"google/gemma-4-26b-a4b-it:free","messages":[{"role":"user","content":"halo"}],"max_tokens":10}'
```
Hasil nyata: 200, response "Halo", 8 token in / 1 out. (Pola probe sama seperti skill ini: stream:false, jangan andalkan /v1/models saja.)

## 5. Integrasi Hermes (config.yaml — aktif: /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml)

```yaml
providers:
  openrouter:
    base_url: https://openrouter.ai/api/v1
    api_mode: chat_completions
    key_env: OPENROUTER_API_KEY
```
- Key harus ada di .env aktif (`hermes config env-path`) + `terminal.env_passthrough` agar subprocess baca (lihat Pitfall 3 SKILL.md).
- Posisi yang masuk akal: fallback tier-2 setelah 9router (failover otomatis), atau untuk cron jobs murah (morning brief, up-eco) yang tak butuh kualitas tinggi.
- `fallback_providers` contoh: `- provider: openrouter / model: google/gemma-4-26b-a4b-it:free`.

## 6. Catatan ekosistem

- 9router lokal (localhost:20128) mungkin sudah meneruskan ke OpenRouter — cek `providerConnections` sebelum menambah provider baru.
- Key free tier ini 0 usage — cadangan bersih untuk failover.
