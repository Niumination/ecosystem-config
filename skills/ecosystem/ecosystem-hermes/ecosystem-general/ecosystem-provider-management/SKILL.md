---
name: ecosystem-provider-management
description: Provider AI lintas 3 agent + pilih model produksi.
---

# Ecosystem Provider Management (3-Agent + Produksi)

## Trigger

- User minta integrasi/removal/cek provider di "3 agent" (Hermes + JCode + OpenCode) — pola tetap user.
- User minta pilih model yang paling tepat untuk AI produksi (cc-acehtengah SAPA Smart AI, dll).
- Sync kredensial provider ke vault, atau audit provider lintas agent.

## Prinsip Kunci

1. **Satu provider = 5 titik konfigurasi** yang harus konsisten:
   | Titik | Lokasi | Cara ubah |
   |-------|--------|-----------|
   | Hermes provider | `~/.hermes/config.yaml` → `providers.<name>` | `hermes config set` (patch/write_file DITOLAK untuk config.yaml) |
   | Hermes env passthrough | `terminal.env_passthrough` | `hermes config set terminal.env_passthrough '[...]'` |
   | Hermes .env | `~/.hermes/.env` | edit file (hapus baris saat removal) |
   | JCode | `~/.jcode/config.toml` + `~/.config/jcode/<name>.env` | `jcode provider add`; **TIDAK ada subcommand remove** → edit TOML manual |
   | OpenCode | `~/.config/opencode/opencode.jsonc` → `provider.<name>` | edit JSON (patch) |
   | Vault | `~/Desktop/Niumination/vault/secrets.zsh` | export var |
2. **Verifikasi = probe chat nyata**, bukan `/v1/models` saja (listed ≠ usable) dan bukan probe tanpa auth (401 palsu).
3. **Hapus bersih = grep 0 sisa** di semua titik + vault, bukan hanya unset config.

## Workflow: Integrasi Provider Baru (3 Agent)

Contoh nyata: huancheng (https://api.hcnsec.cn/v1, key `HUANCHENG_API_KEY`).

1. **Probe dulu** — key valid? model apa saja? chat works?
   ```bash
   KEY=$(grep HUANCHENG_API_KEY ~/.hermes/.env | cut -d= -f2- | tr -d ' \r\n"')
   curl -s -m 10 -H "Authorization: Bearer $KEY" https://api.hcnsec.cn/v1/models | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin)['data']]"
   curl -s -m 15 -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
     -d '{"model":"auto","messages":[{"role":"user","content":"Say OK"}]}' \
     https://api.hcnsec.cn/v1/chat/completions
   ```
2. **Hermes:**
   ```bash
   hermes config set providers.huancheng.base_url "https://api.hcnsec.cn/v1"
   hermes config set providers.huancheng.api_mode "chat_completions"
   hermes config set providers.huancheng.key_env "HUANCHENG_API_KEY"
   hermes config set providers.huancheng.default_model "auto"
   hermes config set terminal.env_passthrough '["HOME","PATH","HERMES_HOME","HUANCHENG_API_KEY", ...]'
   ```
   Key juga harus ada di `~/.hermes/.env`.
3. **JCode:**
   ```bash
   echo "HUANCHENG_API_KEY=$KEY" > ~/.config/jcode/huancheng.env
   jcode provider add huancheng --base-url https://api.hcnsec.cn/v1 --model auto \
     -p openai-compatible --api-key-env HUANCHENG_API_KEY
   ```
4. **OpenCode:** tambah blok `provider.huancheng` di `opencode.jsonc`:
   ```json
   "huancheng": {
     "options": { "baseURL": "https://api.hcnsec.cn/v1", "apiKey": "<key>" },
     "models": { "auto": {"name": "Auto (huancheng)"} }
   }
   ```
5. **Vault:** `export HUANCHENG_API_KEY="..."` di `vault/secrets.zsh` (jika belum ada).
6. **Verifikasi end-to-end per agent:** `jcode --provider-profile huancheng run 'Say OK'` dan curl chat; Hermes via `hermes -m huancheng/<model> -z "ok"`.

## Workflow: Removal Provider (3 Agent) — bersih sampai 0 sisa

Contoh nyata: juan-router dihapus (28 Agu 2026) karena tidak bisa dipakai.

1. **Hermes:**
   ```bash
   hermes config unset providers.juan-router          # unset = hapus section (set "" = kosongkan saja)
   hermes config set terminal.env_passthrough '[...tanpa JUAN...]'   # tulis ulang array
   grep -v "JUAN_ROUTER_API_KEY" ~/.hermes/.env > /tmp/env && mv /tmp/env ~/.hermes/.env
   ```
2. **JCode:** tidak ada `jcode provider remove` — edit `~/.jcode/config.toml` manual (hapus blok `[providers.juan-router]` + `[[providers.juan-router.models]]`) + `rm ~/.config/jcode/juan-router.env`.
3. **OpenCode:** `del data['provider']['juan-router']` di opencode.jsonc (python json).
4. **Vault:** hapus `export JUAN_ROUTER_API_KEY="..."` dari secrets.zsh.
5. **Verifikasi:** `grep -c "juan" config.yaml .env config.toml opencode.jsonc secrets.zsh` → semua 0.

## Metodologi Pilih Model Produksi (workload-representative test)

Pelajaran inti (28 Agu 2026, cc-acehtengah): probe "ping" tidak cukup untuk memilih model AI produksi. Model harus diuji dengan **workload persis seperti app**:

1. **Payload JSON schema asli app** — cc-acehtengah butuh `{"narasi","visualisasi","rekomendasi"}`. Test dengan system-prompt schema itu, nilai kecepatan + JSON valid (bukan cuma "OK").
2. **Stress data besar** — 30 evidence item → model harus tetap output JSON utuh (banyak model truncate).
3. **Streaming test** — TTFB + chunk count (cc pakai SSE stream).
4. **Stabilitas 3× repeat** — 1 sukses ≠ stabil; ulangi 3x.

Hasil nyata 28 Agu 2026 (bandingkan antar provider sebelum deploy):
- `huancheng auto` (→ agnes-2.5-flash): JSON 3/3, tabel 30 rows 2/3, 3.6–4.5s, streaming OK — **pemenang**.
- `opencode laguna-s-2.1-free`: kadang OK (11.5s, JSON valid) tapi 503 intermiten + truncate data besar.
- `opencode nemotron-3-ultra-free`: 502 Nvidia overload sering + truncate.
- `agentrouter` (glm-5.3/deepseek-v4-flash): **HTTP 400 content-blocked** untuk payload data pemerintahan Indonesia — WAF relay memblokir konten, bukan config salah.
- `huancheng kimi-k3`/`MiniMax-M3`: 429 rate limit; `glm-4.5-air`/`DeepSeek-V4-Pro`: timeout 60s+; `step-3.7-flash`: EOL.

### `auto` alias = TIDAK bisa dipin (unpinnable)

- `model: auto` di huancheng resolve ke model internal (mis. `agnes-2.5-flash`) — TAPI model itu **tidak terdaftar di `/v1/models`** → request dengan `model: agnes-2.5-flash` eksplisit gagal `model_not_found`.
- Konsekuensi: `auto` bisa berpindah ke model lain kapan saja di sisi provider → **output bisa berubah tanpa perubahan config**.
- **Konsistensi produksi harus dijamin di layer app, bukan model:** parser JSON robust (extractJsonObject), sanitize placeholder, grounding angka ke evidence (jangan biarkan model mengarang), visualisasi deterministik dari data. Kalau app punya 4 lapis ini, ganti model di balik `auto` hanya mengubah gaya bahasa, bukan format/kejujuran.
- Alternatif pin model eksplisit sering gagal (429/timeout) — kalau `auto` adalah satu-satunya yang jalan, terima + perkuat grounding.

## Pitfalls

1. **`jcode provider add` pakai `-p openai-compatible`** — tanpa itu profile tidak valid. Setelah add, test dengan `jcode --provider-profile <name> run 'Say OK'` (bukan auth-test saja; auth-test probe pakai key global OPENAI_COMPAT, bisa false-401 padahal profile OK).
2. **jcode env file** `~/.config/jcode/<name>.env` — kalau `openai-compat.env` lama masih ada dengan key lain, bisa menimpa/confuse probe. Bersihkan file env yang tidak terpakai.
3. **Vercel env swap:** `vercel env add` untuk var yang SUDAH ada → error `branch_not_found`; harus `vercel env rm <name> production --yes` dulu, baru add. Verifikasi dengan `vercel env ls | grep`.
4. **`hermes config unset providers.<name>` menghapus section utuh** (lebih bersih dari `set ""` yang menyisakan section kosong).
5. **SSH git diblokir** (permission denied publickey) di mesin ini — push pakai `git push https://oauth2:${GH_TOKEN}@github.com/<org>/<repo>.git <branch>` (GH_TOKEN dari vault atau .env). Fetch refs juga lewat URL token agar `git branch -r` akurat.
6. **Model EOL/berubah:** `step-3.7-flash` EOL 28 Agu 2026, `DeepSeek-V4-Flash` no-channel — selalu re-check `/v1/models` saat model gagal, jangan percaya daftar lama.
7. **Header User-Agent wajib untuk agentrouter** (`hermes-agent/<versi>`) — tanpa UA benar → 401 whitelist WAF (lihat skill `hermes-provider-config`).

## References

- `references/cc-acehtengah-ai-output-2026-08-28.md` — Studi kasus penuh: pemilihan model huancheng, debug crash streaming (missing await), label demo DTSEN, fix tabel fusion multi-source.

## Related Skills

- `hermes-provider-config` (user-owned) — detail Hermes-only provider config + pitfalls (case-sensitive model ID, UA WAF, fallback chain)
- `provider-fallback` (user-owned) — strategi fallback + stress-test burst
- `up-eco` / `ecosystem-snapshot` — status ekosistem umum
