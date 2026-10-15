# JuanRouter (router.juan.web.id) — Integrasi Hermes (15 Ags 2026)

## Latar belakang kegagalan pertama (10 Ags 2026)
Integrasi awal di thread #general menulis ke `~/.hermes/config.yaml` + `~/.hermes/.env`
→ di Hermes portable resolve ke **USB cache-home** (`/Volumes/HermesAgent/.cache/unix-home/.hermes/`),
BUKAN config aktif `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml`.
Klaim "integrasi aktif sepenuhnya" = PALSU; config aktif tidak pernah berubah.

## Resep integrasi yang benar (verified end-to-end)

```bash
export HOME=/Users/zaryu   # WAJIB — keyring + path config aktif
hermes config path          # → /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml

# 1. Provider (format: base_url + api_mode + key_env)
hermes config set providers.juan-router.base_url "https://router.juan.web.id/v1"
hermes config set providers.juan-router.api_mode "chat_completions"
hermes config set providers.juan-router.key_env "JUAN_ROUTER_API_KEY"

# 2. Key ke .env aktif
hermes config env-path      # → /Volumes/HermesAgent/HermesAgentUSB/data/.env
echo 'JUAN_ROUTER_API_KEY="sk-..."' >> "$(hermes config env-path)"

# 3. Passthrough env agar subprocess hermes baca key
hermes config set terminal.env_passthrough '["HOME","PATH","HERMES_HOME","OPENROUTER_API_KEY","OPENCODE_API_KEY","OPENAI_API_KEY","AGENTROUTER_API_KEY","AEROLINK_API_KEY","JUAN_ROUTER_API_KEY"]'

# 4. Fallback (index array 0-based)
hermes config set fallback_providers.0.provider "juan-router"
hermes config set fallback_providers.0.model "agnes-2.0-flash"

# 5. Validasi + uji end-to-end
hermes config check
hermes -m "juan-router/agnes-2.0-flash" -z "Balas hanya satu kata: OK"
# → OK  (catatan: -z = one-shot prompt; -p TIDAK ada di CLI v0.19.0)
```

## Probe API langsung
```bash
curl -s --max-time 15 https://router.juan.web.id/v1/models \
  -H "Authorization: Bearer $KEY"          # daftar model
curl -sN --max-time 40 https://router.juan.web.id/v1/chat/completions \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"agnes-2.0-flash","messages":[{"role":"user","content":"Balas hanya: OK"}],"max_tokens":50,"stream":false}'
# → {"choices":[{"finish_reason":"stop", ... "content":"OK"}]}
```

## Quirk yang ditemukan
- **Streaming = chunk kosong**: `stream` default (SSE) mengembalikan chunk usage kosong
  (`choices:[]`); non-streaming (`"stream":false`) memberi konten penuh + `finish_reason:stop`.
  Hermes CLI handle ini fine — verifikasi via `hermes -m` bukan curl streaming.
- **`ling-3.0-flash-free`** terdaftar di `/v1/models` tapi chat → `401 Model not supported`.
  Jangan pakai; gunakan `agnes-2.0-flash` (verified OK).
- **Model tersedia** (15 Ags 2026): `agnes-2.0-flash`, `gemma-4-31b-it`, `laguna-s-2.1`,
  `laguna-xs-2.1`, `ling-3.0-flash-free` (401), `mistral-large`.
- **BERBAYAR (saldo)** — aturan user: hanya untuk fallback chain, bukan model utama thread.
- Key model respons ter-route sebagai `nr/agnes-2.0-flash` (upstream dibungkus relay).
