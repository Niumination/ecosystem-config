# AgentRouter — probe & operasional

Provider Hermes `agentrouter` (`https://agentrouter.org/v1`, `chat_completions`, key `AGENTROUTER_API_KEY`).

## Titik-titik penting
- Docs khusus Hermes: `https://ps.air-outer.com/docs/hermes.html` — domain konsol BEDA dari domain API.
- Konsol: `ps.air-outer.com/console/token` (API key), `/console/personal` (daftar model aktif untuk akun — source of truth), `/pricing` (ejaan nama model resmi).
- Daftar model dinamis (naik-turun ikut resource) — selalu re-probe; jangan percaya cache lama.

## Semantik status (urutan diagnosa)
1. **401** → cek `User-Agent: hermes-agent/<versi>` dulu (penyebab terbanyak, 401 palsu walau key valid); baru curiga key invalid/dirotasi.
2. **402 Payment Required** → key valid, model butuh top-up kuota. Jangan utak-atik config; model lain bisa tetap 200.
3. **503** → nama model salah atau offline; cocokkan persis dengan `/console/personal` atau `/pricing`.
4. **400 content-blocked** → WAF relay memblokir konten payload (historis: frasa data pemerintahan Indonesia ≥2 kata) — bukan config error; uji dengan payload lain.

## Resep probe (hemat kuota)
```bash
KEY=$(grep '^AGENTROUTER_API_KEY=' ~/.hermes/.env | cut -d= -f2-)
UA='User-Agent: hermes-agent/0.19.0'
# daftar model
curl -s -m 20 -H "Authorization: Bearer $KEY" -H "$UA" https://agentrouter.org/v1/models
# uji per model (max_tokens 1 ≈ 0 biaya)
curl -s -m 30 -H "Authorization: Bearer $KEY" -H "$UA" -H 'Content-Type: application/json' \
  -d '{"model":"glm-5.3","messages":[{"role":"user","content":"hi"}],"max_tokens":1}' \
  https://agentrouter.org/v1/chat/completions
```
Model terverifikasi 200 pada probe terakhir: `glm-5.3`, `deepseek-v4-flash`. Model 402 (butuh top-up): `gpt-6-astra`, `gpt-5.6-sol`, `claude-opus-5`, `claude-opus-4-8`.

## Kredensial
- `vault/agentrouter-key.md` — API key + system access token + catatan status uji terkini.
- Rotasi menyentuh: `vault/secrets.zsh`, `vault/hermes.env.bak`, `~/.hermes/.env` (semua harus cocok); backup pra-rotasi `vault/_backup-credentials/`.
