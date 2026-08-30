---
name: hermes-provider-config
description: >
  Understand and manage Hermes Agent model provider configuration.
  Covers: API-key providers (config.yaml), OAuth2 providers (hermes auth), model_catalog.json,
  provider status investigation, and cleanup of disabled/broken providers.
  Use when: configuring new providers, debugging "provider not found" or auth errors,
  investigating why a provider works in one context but not another, or cleaning up provider config.
---

# Hermes Provider Configuration

## Overview

Hermes Agent supports multiple provider configuration mechanisms. Understanding which mechanism applies to which provider type is essential for debugging and config management.

---

## Provider Types

### 1. API-Key Providers (config.yaml)

Providers that authenticate via API key stored in environment variables. These live in `config.yaml` under `providers:` section.

**Location:** `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml` → `providers:`

**Structure:**
```yaml
providers:
  provider-name:
    base_url: https://api.example.com/v1
    api_mode: chat_completions   # usually
    key_env: PROVIDER_API_KEY    # env var name
```

**Examples:** 9router, OpenRouter, AgentRouter (when configured), Aerolink, Huancheng

**How Hermes uses them:**
- Reads `base_url`, `api_mode`, `key_env` from config.yaml
- Looks up the actual key from environment variable named by `key_env`
- Makes API calls to `base_url` with the key

### 2. OAuth2 Providers (hermes auth)

Providers that authenticate via OAuth2 access tokens. These do NOT appear in `config.yaml` providers section.

**Location:** Managed via `hermes auth` commands; token state persisted separately.

**Examples:** Nous Portal

**How Hermes uses them:**
- Access token stored outside config.yaml (in auth state)
- Refreshed automatically via refresh token
- Referenced in `model_catalog.json` under `providers.nous`
- Session-level `/model` overrides can persist provider=nous in state.db

**Key insight:** OAuth2 providers are invisible in `config.yaml` providers section — this is NOT a bug, it's the correct architecture.

### 3. Model Catalog (model_catalog.json)

A cached manifest of available models per provider, fetched from Hermes cloud.

**Location:** `/Volumes/HermesAgent/HermesAgentUSB/data/cache/model_catalog.json`

**Structure:**
```json
{
  "providers": ["openrouter", "nous"],
  "provider": {
    "nous": {
      "display_name": "Nous Portal",
      "models": [...]
    },
    "openrouter": {...}
  }
}
```

**Notes:**
- Model catalog defines which models are available per provider
- The `providers` array lists all known providers (including OAuth2 ones)
- `model_catalog.enabled: true` in config.yaml enables auto-fetch
- TTL is 1 hour by default

---

## opencode-free Provider (27 Ags 2026 — post-constitution rollback)

### Overview
`opencode-free` is the **anonymous free tier** of the OpenCode Zen API — no API key required. Migrated from `opencode-zen` (required `OPENCODE_ZEN_API_KEY`) as part of the Constitution era rollback (24 Agu 2026).

### Configuration
```yaml
providers:
  opencode-free:
    base_url: https://opencode.ai/zen/v1
    api_mode: chat_completions
    # NO key_env needed — anonymous bearer accepted
```

### Available Free Models (Verified HTTP 200)
| Model | Use Case | Verified |
|:---|:---|:---|
| `hy3-free` | General purpose, fast | ✅ HTTP 200 |
| `nemotron-3-ultra-free` | Reasoning heavy, cron | ✅ HTTP 200 |
| `laguna-s-2.1-free` | Coding specialist | ✅ HTTP 200 |
| `muse-spark-1.2-contributor-free` | Creative/writing | ✅ HTTP 200 |
| `x-preview-f-free` (Ox Alpha) | **EXCLUDED** | ❌ HTTP 401 |

### Current Usage in Config (Active)
| Function | Model | Provider |
|:---|:---|:---|
| **DM Default** | `hy3-free` | `opencode-free` |
| **Thread 1** | `hy3-free` | `opencode-free` |
| **Thread 1172** | `nemotron-3-ultra-free` | `opencode-free` |
| **Cron** | `nemotron-3-ultra-free` | `opencode-free` |
| **Delegation** | `hy3-free` | `opencode-free` |
| **Compression** | `hy3-free` | `opencode-free` |
| **X-Search** | `hy3-free` | `opencode-free` |

### Fallback Chain (3-Level, Single Provider Family)
```yaml
fallback_providers:
  - provider: opencode-free
    model: hy3-free              # L1: fast, lightweight
  - provider: opencode-free
    model: nemotron-3-ultra-free # L2: reasoning heavy
  - provider: opencode-free
    model: laguna-s-2.1-free     # L3: coding specialist
```

**Core v2 Principle**: Single provider family (`opencode-free`), diversify models — NOT silent hop to different providers (provider swap = HALT + HANDOFF).

### Migration Notes (27 Ags 2026)
1. **Provider**: `opencode-zen` → `opencode-free` (12 locations in config.yaml)
2. **API Key**: Removed `OPENCODE_API_KEY` from `env_passthrough` (not needed)
3. **Default Model**: `big-pickle` → `hy3-free` (more stable free tier)
4. **Fallback**: 1-level → 3-level (all opencode-free)
5. **Removed**: `x-preview-f-free` from fallback (401 on free tier)

### Verification Commands
```bash
# Test all models
for m in hy3-free nemotron-3-ultra-free laguna-s-2.1-free; do
  curl -s -o /dev/null -w "HTTP %{http_code} %{time_total}s" \
    --max-time 15 https://opencode.ai/zen/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"$m\",\"messages\":[{\"role\":\"user\",\"content\":\"OK\"}],\"stream\":false}"
  echo
done
```

### Related Files
- `~/.hermes/config.yaml` — Main configuration
- `.hermes/skills/provider-fallback/SKILL.md` — Fallback strategy doc
- `docs/references/model-mapping-post-rollback.md` — Complete mapping reference

---

## Investigation Workflow

When a provider isn't working or you need to understand its status:

### Step 1: Check config.yaml
```bash
grep -A 5 "^providers:" /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml
```

### Step 2: Check model_catalog.json
```bash
cat /Volumes/HermesAgent/HermesAgentUSB/data/cache/model_catalog.json | python3 -c "import sys,json; d=json.load(sys.stdin); print('Providers:', d.get('providers',[]))"
```

### Step 3: Check hermes auth status
```bash
hermes auth status
```

### Step 4: Test provider connectivity
```bash
# For API-key providers:
curl -s -X POST <base_url>/v1/chat/completions -H "Authorization: Bearer ***" ...

# For OAuth2 providers:
hermes auth status   # check if access token is valid
```

### Teknik probe yang benar (verified 15 Ags 2026 — audit mapping model)

Probe chat-completion langsung ≠ sekadar `/v1/models` (yang cuma daftar). Tiga aturan:

1. **Header User-Agent wajib.** Plain urllib/curl UA → `403` di banyak router. Baca UA dari config: `opencode-zen` butuh `User-Agent: opencode/1.18.18` (ambil dari `model.default_headers` config); `juan-router`/`agentrouter` terima `hermes-agent/<versi>`. Include UA di SEMUA probe.
2. **Selalu `stream: false`.** Streaming bisa return chunk kosong padahal model hidup (`agnes-2.0-flash`: stream → chunk kosong + `[DONE]`; non-stream → isi "OK" + `finish_reason: stop`). Verifikasi = non-streaming.
3. **Listed ≠ usable.** `/v1/models` menampilkan `ling-3.0-flash-free`, tapi chat → `401 not supported`. Selalu chat-probe model sebelum dipasang di thread/fallback.

429 = upstream rate limit (sering `cf/@cf/*` Cloudflare) → retry dengan delay ≥6s, atau pilih model non-429. Script reusable: `scripts/probe-provider-models.py` (probe per model, baca key dari .env, UA configurable).

### Step 5: Check gateway logs for provider errors
```bash
grep -i "provider\|auth\|token" /Volumes/HermesAgent/HermesAgentUSB/data/logs/gateway.log | tail -20
```

---

## Common Pitfalls

### Pitfall 1: Looking for Nous Portal in config.yaml providers section
**Symptom:** User asks "why isn't nous in providers?" or "why can't I configure nous?"
**Reality:** Nous Portal is an OAuth2 provider — it lives in `hermes auth` state, not config.yaml. Its model list is in model_catalog.json under `providers.nous`.
**Fix:** Use `hermes auth add nous` to set up auth; don't look for it in config.yaml.

### Pitfall 2: Provider section has empty entries after cleanup
**Symptom:** After removing a provider, config.yaml still shows `provider-name:` with empty fields.
**Reality:** Hermes config tools (hermes config set) often leave empty section headers. These are harmless but clutter the file.
**Fix:** Manually edit config.yaml to remove empty provider sections, or use direct file editing:
```bash
python3 -c "
from pathlib import Path
p = Path('/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml')
t = p.read_text()
lines = t.split('\n')
out = []
skip = False
for line in lines:
    stripped = line.strip()
    if stripped.endswith(':') and stripped != 'providers:' and stripped != 'auxiliary:' and stripped != 'model:':
        # Check if next non-empty line is also empty/meaningless
        pass
    # ... handle removal
"
```

### Pitfall 3: Integrasi ditulis ke config yang SALAH — cache-home vs config aktif
**Symptom:** Integrasi provider "sudah selesai" (config + .env ditulis), tapi Hermes tetap pakai config lama / provider tidak muncul di `hermes config get`.
**Reality (15 Ags 2026, juan-router):** Integrasi 10 Ags ditulis ke `~/.hermes/config.yaml` — di Hermes portable `~/` resolve ke **USB cache-home** (`/Volumes/HermesAgent/.cache/unix-home/.hermes/`), BUKAN config aktif `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml`. Hasilnya: provider tidak pernah aktif, dan config aktif punya sisa fallback invalid `JuanRouter/glm-5.2` (model ber-prefix provider lain di bawah provider 9router).
**Fix:**
1. **Konfirmasi config aktif dulu:** `export HOME=/Users/zaryu; hermes config path` → harus `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml`. JANGAN pernah menulis ke `~/.hermes/` (cache-home).
2. **Edit via `hermes config set` (jalur sah — `patch`/`write_file` di-refuse untuk config.yaml):**
   ```bash
   hermes config set providers.<name>.base_url "https://..."
   hermes config set providers.<name>.api_mode "chat_completions"
   hermes config set providers.<name>.key_env "<ENV_VAR>"
   hermes config set fallback_providers.0.provider "<name>"   # index array 0-based
   hermes config set fallback_providers.0.model "<model>"
   ```
3. **Tambahkan key ke .env aktif** (`hermes config env-path`) DAN ke `terminal.env_passthrough` (agar subprocess hermes bisa baca): `hermes config set terminal.env_passthrough '["HOME", ..., "<ENV_VAR>"]'`.
4. **Verifikasi end-to-end:** `hermes -m <provider>/<model> -z "Balas hanya satu kata: OK"` → harus output teks. (`-z` = one-shot prompt; `-p` TIDAK ada di CLI ini.)
5. File salah lama di cache-home: rename `.bak-<tanggal>` (jangan hapus tanpa izin).

### Pitfall 4: AgentRouter 401 = WAF User-Agent whitelist (BUKAN butuh extension)
**Symptom:** AgentRouter returns `401 {"message":"unauthorized client detected","type":"unauthorized_client_error"}`.
**Reality (dikoreksi 13 Ags 2026):** AgentRouter mem-whitelist User-Agent — hanya `hermes-agent/<version>` yang diterima; `curl/7.x`, `OpenAI/Python ...`, `hermes-cli/...` ditolak. Provider config native `providers.agentrouter` di config.yaml BERFUNGSI penuh; TIDAK butuh TypeScript extension (docs agentrouter.org/docs/hermes.html menampilkan TS extension API untuk versi Hermes lain).
**Fix:** Tambahkan `extra_headers: {User-Agent: hermes-agent/<versi-hermes>}` di section `providers.agentrouter` — Hermes merge ini ke OpenAI client `default_headers` via `apply_custom_provider_extra_headers_to_client_kwargs()`.
**Verifikasi sebelum menyalahkan extension:** `curl /v1/models` dengan `-H "User-Agent: hermes-agent/0.19.0"` — kalau 200, key & provider OK.
Detail + hasil uji model: `references/agentrouter-integration.md` di skill `telegram-router-orchestration`.

### Pitfall 4: Session overrides persisting after provider removal
**Symptom:** After removing a provider from config, sessions still try to use it.
**Reality:** Session-level `/model` overrides stored in state.db can persist provider references. These are rehydrated on session start.
**Fix:** Check state.db for stale overrides:
```bash
sqlite3 /Volumes/HermesAgent/HermesAgentUSB/data/state.db \
  "SELECT session_key, model FROM gateway_routing WHERE session_key LIKE '%telegram%' ORDER BY session_key;"
```

### Pitfall 5: Empty provider entries after `hermes config set`
**Symptom:** Running `hermes config set providers.X.base_url ""` leaves `X:` section with empty fields.
**Reality:** The `hermes config set` command doesn't remove sections — it just clears values.
**Fix:** Direct file editing to remove empty sections.

### Pitfall 6: Relay provider content filter memblokir bahasa non-Inggris — uji dengan konten representatif
**Symptom:** Provider LULUS uji minimal (`curl` "ping", `hermes chat -q "reply OK"`) tapi thread live error `HTTP 500 sensitive words detected` / `content-blocked` saat percakapan nyata.
**Reality (13 Ags 2026, AgentRouter):** relay China memblokir **frasa Bahasa Indonesia ≥2 kata** sementara Inggris, Cina, dan kata tunggal ID lolos. Uji ASCII minimal tidak memicu filter → false positive "siap pakai". Deteksi bahasa = filter anti-spam relay, bukan bug config.
**Fix (probe yang benar):** uji provider sebelum dipasang di thread live dengan **konten representatif** — kalimat asli multi-kata dalam bahasa pengguna: `{"messages":[{"role":"user","content":"saya makan"}]}`. Kalau `content-blocked`, provider hanya cocok untuk chat EN — jangan pasang di thread berbahasa Indonesia, dan jangan andalkan fallback (`auto` bisa resolve ke provider tanpa kredensial → 404 → error total).
**Catatan error chain di gateway:** retry gagal → fallback → 404 → error ke user. Cek `logs/errors.log` untuk `content-blocked` + `No active credentials for provider` — dua sinyal ini = filter konten + fallback patah.

### Pitfall 7: `fallback_model: model: auto` bisa resolve ke provider tanpa kredensial → 404 patahkan rantai
**Symptom:** Model utama kena rate-limit (429) → fallback `9router/auto` dipanggil → `HTTP 404 No active credentials for provider: openai` → error total ke thread (bukan pindah model).
**Reality (13 Ags 2026):** `auto` di 9router meresolve ke provider yang TIDAK punya kredensial aktif (openai). "Auto" ≠ "coba apa pun yang jalan".
**Fix:** Jangan pakai `auto` di fallback — pin model konkret yang sudah teruji hidup. Fallback = jaring pengaman, harus deterministik.

### Pitfall 8: Model ID CASE-SENSITIVE di relay new-api (Huancheng/hcnsec.cn) — `model_not_found` padahal key valid
**Symptom (18 Ags 2026):** curl chat ke Huancheng pakai `deepseek-v4-flash` → `{"error":{"code":"model_not_found","message":"No available channel for model deepseek-v4-flash under group default"}}`. Key VALID (list models jalan), tapi tiap chat gagal.
**Reality:** Server relay (hcnsec.cn) menyimpan model ID dengan case EKSAK — `DeepSeek-V4-Flash` ≠ `deepseek-v4-flash`. `/v1/models` menampilkan ID persis seperti yang harus dipakai (campuran case: `DeepSeek-V4-Pro`, `glm-5.2`, `Kimi-K2.6`, `MiniMax-M3`, `step-3.7-flash`...).
**Fix:**
1. List ID eksak: `curl <base_url>/v1/models | jq -r '.data[].id'`
2. Set default model di section provider (config.yaml tidak bisa di-patch langsung — wajib `hermes config set`):
   ```bash
   hermes config set providers.huancheng.default_model "DeepSeek-V4-Flash"
   ```
3. Verifikasi ulang dengan ID eksak (non-stream, UA benar).
**Aturan umum:** kalau relay memberi `model_not_found` padahal model terlihat di `/v1/models`, SELALU cek case ID dulu sebelum menyalahkan key.

### Pitfall 9: Permintaan "periksa/pastikan X" = verifikasi LANGSUNG + laporan ringkas, BUKAN rekap sejarah / BUKAN eksekusi fix
**Symptom (18 Ags 2026, user marah keras "FUCKYOU", "kamu gak perlu kerjain apapun kalau aku gak minta"):** User minta "periksa apakah rtk benar diterapkan dan pastikan huancheng dapat digunakan". Agent malah: (1) bikin rekap sejarah panjang dari session_search, (2) menawarkan/eksekusi fix yang tidak diminta. Padahal yang diminta CUKUP: probe langsung (rtk --version / rtk rewrite / curl /v1/models) + lapor hasil singkat.
**Aturan (user preference, berlaku SEMUA task):**
1. **"periksa/cek/pastikan" = langsung probe dengan tool, lapor singkat.** Jangan perluas scope, jangan tulis rekap/wall-of-text, jangan bikin dokumen.
2. **Jangan kerjakan apa pun yang tidak diminta** — termasuk fix config, restart gateway, edit file, atau ekspansi task lain. Tunggu instruksi eksplisit ("gas", "fix", "kerjakan").
3. Kalau probe menemukan masalah, LAPORKAN + tawarkan fix SATU BARIS ("mau saya fix?"), jangan langsung eksekusi.
4. Data harus dari tool output real, bukan rekonstruksi memory/session.

### Pitfall 10: `429 FreeUsageLimitError` di opencode-zen = kuota FREE HABIS — akar "kinerja model buruk"
**Symptom (18 Ags 2026):** `big-pickle` DAN `deepseek-v4-flash-free` (primary + fallback yang sama-sama keluarga Zen) balas `HTTP 429 {"type":"FreeUsageLimitError","message":"Rate limit exceeded"}`. User mengeluh "kinerja model tidak bagus / ekosistem kacau" — padahal bukan config rusak, bukan fallback salah: **kuota harian free tier Zen habis**.
**Reality:** Semua model `*-free` di opencode-zen berbagi kuota harian. Begitu habis, SEMUA model free kena 429 serentak (big-pickle, deepseek-v4-flash-free, mimo-v2.5-free). Model berbayar (`deepseek-v4-flash`) balas 401 `CreditsError` (belum ada payment). Diagnosa: cek HTTP code 429 + body `FreeUsageLimitError` — bukan debug config.
**⚠️ KOREKSI 19 Ags 2026 (user): probe 429 TIDAK membuktikan model mati di runtime.** User mengkonfirmasi `big-pickle` AKTIF dan dipakai di sesi gateway saat probe eksternal saya menunjukkan 429. Sebab: probe curl pakai API key/metode berbeda dari yang dipakai gateway aktif (ekosistem punya banyak key sisa/duplikat di .env — mis. `OPENCODE_API_KEY` vs `OPENCODE_ZEN_API_KEY`; endpoint/host beda). **Aturan:**
1. JANGAN klaim "model X mati/kuota habis" hanya dari probe eksternal — verifikasi dulu bagaimana gateway runtime memanggil model itu (key mana, base_url mana, header apa, `/model` aktif di sesi).
2. Kalau user bilang model jalan (mereka melihatnya di sesi), TERIMA — jangan membantah dengan hasil probe yang beda metode.
3. Selidiki dulu BEDA metode (key aktif vs .env lama, base_url, UA) sebelum menyimpulkan.
**Fix (untuk kasus 429 yang benar-benar valid):**
1. Jangan ubah config dulu — tunggu reset kuota (harian) ATAU pindah ke keluarga model lain yang punya kuota terpisah.
2. Alternatif yang tetap hidup saat Zen free 429 (tested 18 Ags): **9router `gemini/gemini-3.7-flash` (1.1s tool-call)** · 9router `gratislonggar` (9.2s, resolve ke gemini-3.6) · nvidia `meta/llama-3.1-8b-instruct` (0.7s) · openrouter `openai/gpt-oss-20b:free` (12.2s, JSON mode gagal).
3. Kalau harus tetap di keluarga Zen: `hy3-free`, `laguna-s-2.1-free`, `nemotron-3-ultra-free` kadang masih hidup saat big-pickle 429 (kuota per-model tidak identik) — test per model, jangan asumsi semua free mati.
4. `stream:false` TIDAK menjamin response JSON — **9router/gratislonggar balas SSE (`data: {...}` chunks) walau diminta `stream:false`**. Parser probe harus handle dua bentuk: `data:` prefix (SSE) atau JSON penuh. (`gratislonggar` non-stream kadang kosong — test ulang, jangan vonis model mati dari 1 response kosong.)

### Pitfall 11: `hermes config set fallback_providers '<JSON string>'` menyimpan STRING, bukan list — chain jadi kosong
**Symptom (18 Ags 2026):** Runs `hermes config set fallback_providers '[{"provider": "opencode-zen", "model": "deepseek-v4-flash-free"}]'` → tool bilang "✓ Set", tapi `hermes fallback ls` tampil **"No fallback providers configured"**. Config.yaml berisi:
```yaml
fallback_providers: '[{"provider": "opencode-zen", "model": "deepseek-v4-flash-free"}]'   # STRING literal!
```
**Reality:** `hermes config set` menulis VALUE sebagai scalar YAML (string), TIDAK parse JSON/struct. `hermes fallback ls` tidak membaca rantai → tampil kosong. `hermes fallback add/remove` adalah **picker interaktif** (tidak menerima argumen posisional non-interaktif) dan `hermes fallback clear` minta konfirmasi `[y/N]` di stdin — tidak bisa di-script tanpa expect/pty.
**Fix (non-interaktif, direct YAML edit):**
1. Backup: `cp config.yaml config.yaml.bak-before-fallback-fix`
2. Ganti string → list YAML via python (yaml.safe_load untuk verifikasi):
```python
old = "fallback_providers: '[{\"provider\": \"opencode-zen\", \"model\": \"deepseek-v4-flash-free\"}]'"
new = """fallback_providers:
  - provider: opencode-zen
    model: deepseek-v4-flash-free"""
content = content.replace(old, new)
```
3. Verifikasi: `python3 -c "import yaml; d=yaml.safe_load(open('config.yaml')); print(type(d['fallback_providers']).__name__)"` → `list`; lalu `hermes fallback ls` → harus tampil 1 entry.
**Catatan fallback pasca-rekonstruksi (D-0004, 21 Ags 2026):** kebijakan Niumination sekarang = **free tier `opencode-zen`** (`big-pickle` / `nemotron-3-ultra-free` primary; fallback se-provider `hy3-free` / `*-free` lain) **+ free tier Nous Portal** (`:free`, OAuth2), bukan zoo debug (juan 401 di depan, 9router ×2). Lihat skill `niu-core-governance` (umbrella tata kelola core: hukum tersegel, kebijakan model, fence/handoff/ledger, pitfall path hook niu-*).

**CLI note (20 Ags 2026):** `hermes fallback remove <name>` dan `hermes mcp remove <name>` TIDAK menerima argumen non-interaktif; `remove` adalah picker/konfirmasi — `--force` unrecognized. Cara script-safe: `echo "y" | hermes mcp remove uacc` untuk MCP; untuk fallback gunakan direct YAML edit (Pitfall 11) atau `echo y | hermes fallback clear` lalu add via YAML.

### Pitfall 12: `auxiliary.vision` MAKESPAN config rusak → `503 model_not_found` di browser_vision (dashboard tetap sehat)
**Symptom (20 Ags 2026):** `browser_vision` gagal 2× dengan `503 {code: model_not_found, message: "No available channel for model Qwen3.5-397B-A17B under group default"}` — screenshot ter-capture tapi analisis tidak jalan. Dashboard MC sendiri SEHAT (DOM audit berhasil).
**Reality:** Config `auxiliary:` (vision, compression) adalah service PENDAMPING — kalau salah set, mematikan fitur yang bergantung padanya TAPI tidak menyentuh model utama/gateway. Di install ini:
```yaml
auxiliary:
  vision:
    provider: 9router                     # label provider
    model: Qwen3.5-397B-A17B              # model TIDAK ada di provider itu
    base_url: https://api.hcnsec.cn/v1    # URL milik PROVIDER LAIN (huancheng)!
```
Tiga elemen tidak sinkron (provider-label = 9router, base_url = huancheng, model tidak terdaftar di keduanya) → relay balas `model_not_found`. Bukan "browser tools rusak" — config vision yang salah.
**Fix:**
1. Verifikasi apa yang tersedia di base_url itu: `curl <base_url>/v1/models` dengan key yang sesuai.
2. Selaraskan TRIPEL (provider-label, base_url, model) — harus milik SATU provider; model exact-match di `/v1/models` (lihat Pitfall 8 case-sensitive).
3. Cek key UX/auxiliary di .env (`AUXILIARY_VISION_API_KEY` dst) — bisa beda dari key model.
4. Sampai fix: audit visual via DOM count (chars + elemen data) — lihat skill `niu-mission-control-ui` → `references/dom-visual-audit-2026-08-20.md`.
**Aturan:** kalau `browser_vision`/vision gagal `model_not_found`, selidiki config `auxiliary:` DULU sebelum menyalahkan tooling; jangan pernah tulis "vision tool rusak" sebagai fakta permanen — ini state config yang bisa diperbaiki.

**Fix selesai (20 Ags 2026):** ganti ke triple selaras = provider `9router`, model `gemini/gemini-3.7-flash`, base_url `http://localhost:20128/v1`, key `NINE_ROUTER_API_KEY` (via `hermes config set auxiliary.vision.*`). **TAPI config tidak hot-reload:** sesudah `hermes config set` + verifikasi `grep`, gateway MASIH memakai nilai lama (`using custom (Qwen3.5-397B-A17B)` di log) sampai restart gateway. Dan **restart gateway diblokir dari dalam proses gateway** (`launchctl kickstart -k gui/501/ai.hermes.gateway` → "Blocked: cannot restart or stop the gateway from inside the gateway process ... SIGTERM propagates"). Alur benar: (1) fix config via `hermes config set`, (2) uji endpoint langsung dengan script vision-probe agar ada bukti model hidup SEBELUM restart, (3) minta user restart gateway dari luar (`launchctl kickstart -k gui/501/ai.hermes.gateway` di terminal terpisah), (4) verifikasi log `grep "Auxiliary vision: using"` → harus tampil `gemini/gemini-3.7-flash`, (5) baru test `browser_vision`.

Script reusable: `scripts/test-vision-endpoint.py` — kirim chat-completion dengan gambar (base64 data URL) ke endpoint OpenAI-compatible + model apa pun, print status + respons (mendeteksi SSE `data:` chunks juga). Pakai untuk memverifikasi model vision hidup di endpoint tertentu sebelum menulis config.

---

## Fallback Chains & Model Selection

### Arsitektur fallback (source-verified, gateway/run.py + hermes_cli/fallback_config.py)

- **Fallback GLOBAL — satu rantai untuk SEMUA thread + DM.** `fallback_providers` / `fallback_model` dibaca dari root config.yaml setiap turn (`_refresh_fallback_model` re-read disk → **tanpa restart gateway**). Tidak bisa beda fallback per channel.
- **`ChannelOverride` (channel_overrides) hanya 3 field:** `model`, `provider`, `system_prompt` — TIDAK ada field fallback. Per-thread hanya bisa beda model utama.
- **Multi-level chain didukung:** list urutan = prioritas; dedupe otomatis per (provider, model, base_url). ⚠️ **Format lama `JuanRouter/glm-5.2` di bawah provider 9router = INVALID** (prefix model ≠ provider) — diperbaiki 15 Ags 2026 menjadi provider `juan-router` tersendiri + model polos (`agnes-2.0-flash`):
```yaml
fallback_providers:
  - provider: juan-router
    model: agnes-2.0-flash                              # L1 (berbayar, verified)
  - provider: 9router
    model: cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b  # L2
  - provider: 9router
    model: gratislonggar                             # L3 — jaring terakhir
```
- Legacy `fallback_model:` tetap didukung, digabung setelah `fallback_providers`.

### Metodologi pilih model/fallback: stress-test burst (bukan probe tunggal)

Probe 1× ("ping") TIDAK cukup — rate limit hanya kelihatan saat burst. Uji: 8 request beruntun cepat per model, hitung sukses/8. Hasil 13 Ags 2026 (9router v0.5.50):

| Model | Burst 1 | Burst 2 (1 jam kemudian) |
|-------|---------|--------------------------|
| `gemini/gemini-3.5-flash-lite` | 8/8 | 8/8 |
| `gratislonggar` (combo) | 8/8 | 8/8 |
| `gemini/gemini-3.6-flash` | **7/8** | **2/8** ⚠️ |
| `gc/gemini-2.5-flash` | 2/8 | — |
| `nvidia/z-ai/glm-5.2` | 2/8 | — |
| `nvidia/minimaxai/minimax-m3` | **1/8** | — |

**Aturan:**
1. **Stress-test SEBELUM pasang** di thread/fallback; re-test model yang dipakai thread — hasil bisa berubah antar jam (quota harian upstream).
2. **Diversifikasi rantai fallback lintas upstream** (mis. JuanRouter + Cloudflare + Gemini) — kalau satu provider down, yang lain tetap hidup.
3. **Utamakan provider non-berbayar** kecuali diminta: JuanRouter = saldo (berbayar), Cloudflare (`cf/`) & Gemini (`gemini/`, `gc/`) = gratis tapi bisa kena quota.
4. **Periksa mapping lama:** model thread yang dulu OK bisa jadi lemah (2/8) — audit berkala dengan burst test; ganti ke model 8/8 sekelas (mis. `nvidia/z-ai/glm-5.2` → `cf/@cf/zai-org/glm-4.7-flash` 8/8).

Script reusable: `scripts/stress-test-models.py` (probe + burst, ranking otomatis).

---

## 9Router Gateway Administration (Multi-Key Failover)

9Router (localhost:20128) is the local gateway used by ALL Mission Control threads. To add a new key/connection (e.g., a second key for failover when the first key's balance is exhausted):

1. **API Auth** (dashboard password ≠ CLI secret; 3 failed attempts → lockout):
   ```python
   import hashlib
   machine_id = open('/Users/zaryu/.9router/machine-id').read().strip()
   cli_secret = open('/Users/zaryu/.9router/auth/cli-secret').read().strip()
   token = hashlib.sha256((machine_id + "9r-cli-auth" + cli_secret).encode()).hexdigest()[:16]
   # → '95222746561be6dc'
   ```
   **Header:** `x-9r-cli-token: 95222746561be6dc`

2. **Two-step process:**
   - `POST /api/provider-nodes` → create an `openai-compatible` node → returns ID `openai-compatible-chat-<uuid>`
   - `POST /api/providers` → register a connection with `apiKey` and the node ID
   - Models appear as `<prefix>/<model>` (e.g., `JuanRouterClaude/claude-opus-4-8`)

3. **Multi-key = second connection** with `priority` → automatic failover on 401/429/error; `usageHistory.connectionId` proves the switch.

4. **Balance exhaustion signal:** `lastError: "预扣费额度失败, 用户剩余额度: $0.237140, 需要预扣费额度: $3.010126"` → time to add a new key.

Full details (DB schema, token derivation, request JSON, pitfalls): `references/9router-gateway-admin.md`.

9router (localhost:20128) = gateway lokal yang dipakai SEMUA thread MC. Untuk
menambah key/connection baru (mis. key kedua agar failover saat saldo/key-1 habis):

1. **Auth API** (dashboard password ≠ cli-secret; 3× salah → lockout):
   `x-9r-cli-token: sha256(machine_id + "9r-cli-auth" + cli_secret).hexdigest()[:16]`
   (`machine_id` & `cli_secret` dari `~/.9router/`).
2. **Dua langkah:** `POST /api/provider-nodes` (buat node openai-compatible → id
   `openai-compatible-chat-<uuid>`) lalu `POST /api/providers` (daftarkan connection
   dengan apiKey). Model muncul sebagai `<prefix>/<model>` (mis. `JuanRouterClaude/claude-opus-4-8`).
3. **Multi-key = connection kedua** dengan `priority` → failover otomatis 401/429/error;
   `usageHistory.connectionId` membuktikan perpindahan.

Detail lengkap (schema DB, token derivation, request JSON, sinyal saldo habis,
pitfalls): `references/9router-gateway-admin.md`.

---

## Cleanup: Removing a Disabled Provider

When a provider is broken/disabled and you want to remove it cleanly:

1. **Clear its config values:**
   ```bash
   hermes config set providers.<name>.base_url ""
   hermes config set providers.<name>.key_env ""
   ```

2. **Remove empty section from config.yaml directly:**
   Edit `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml` and delete the empty `<name>:` block.

3. **Check for related references:**
   ```bash
   grep -rn "<name>" /Volumes/HermesAgent/HermesAgentUSB/data/ \
     --include="*.yaml" --include="*.json" --include="*.log" 2>/dev/null \
     | grep -v "config.yaml" | grep -v ".git"
   ```

4. **Clear auth cache if applicable:**
   ```bash
   hermes auth reset <name>   # for OAuth2 providers
   ```

5. **Clear model catalog cache (optional):**
   ```bash
   rm -f /Volumes/HermesAgent/HermesAgentUSB/data/cache/model_catalog.json
   ```

6. **Verify:**
   ```bash
   grep -c "<name>" /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml
   # Should be 0 (or only in comments)
   ```

---

## Provider Status Quick Reference

| Provider | Config Location | Auth Method | Check Command |
|----------|---------------|-------------|---------------|
| 9router | config.yaml → providers.9router | API Key (env) + gateway multi-key via `providerConnections.priority` (admin: `references/9router-gateway-admin.md`) | `curl localhost:20128/v1/models`; add key/connection: `POST /api/provider-nodes` + `/api/providers` dgn `x-9r-cli-token` |
| OpenRouter | config.yaml → providers.openrouter | API Key (env) `OPENROUTER_API_KEY` | `GET https://openrouter.ai/api/v1/key` → cek `is_free_tier`/`usage`; 19 model `:free` (per 16 Ags 2026), rate limit 20/min·50/hari tanpa credit — detail & pola config: `references/openrouter-free-tier.md` |
| Nous Portal | model_catalog.json + hermes auth | OAuth2 | `hermes auth status` |
| AgentRouter | config.yaml → providers.agentrouter | API Key (env) + `extra_headers` UA `hermes-agent/<ver>` | `curl /v1/models` dgn UA benar; hanya gpt-5.6-sol aktif (Claude: budget pool exhausted); ⚠️ **blokir frasa Bahasa Indonesia ≥2 kata** (content-blocked) |
| JuanRouter | config.yaml → providers.juan-router | API Key (env) `JUAN_ROUTER_API_KEY` | `curl https://router.juan.web.id/v1/models`; **BERBAYAR (saldo)** — hanya untuk fallback, bukan model utama. Verified: `agnes-2.0-flash` ✅; `ling-3.0-flash-free` terdaftar tapi 401 not supported |
| Huancheng | config.yaml → providers.huancheng | API Key (env) `HUANCHENG_API_KEY` | `curl https://api.hcnsec.cn/v1/models` → 20 model; ⚠️ **model ID case-sensitive** (`DeepSeek-V4-Flash` ≠ `deepseek-v4-flash` → `model_not_found`); `default_model` sudah di-set via `hermes config set providers.huancheng.default_model` |
| Aerolink | config.yaml → providers.aerolink | API Key (env) | Test via API |

## Provider Health Verification Pattern

A configured provider is not necessarily usable. Always probe providers before relying on them in fallback chains.

### Quick Probe Pattern

⚠️ **WAJIB sertakan Authorization header dari .env** — probing `/v1/models` TANPA key memberi 401 PALSU pada provider yang key-nya valid (juan-router, huancheng, agentrouter semua tampak "401" di audit 18 Ags karena curl tanpa header). Probe tanpa auth hanya valid untuk 9router localhost. Juga set `User-Agent` (Pitfall 4: WAF whitelist).

```bash
set -a; source /Volumes/HermesAgent/HermesAgentUSB/data/.env; set +a
for p in opencode-zen juan-router 9router agentrouter huancheng openrouter nvidia_nim; do
  case "$p" in
    opencode-zen) url="https://opencode.ai/zen/v1/models"; key="$OPENCODE_ZEN_API_KEY" ;;
    juan-router) url="https://router.juan.web.id/v1/models"; key="$JUAN_ROUTER_API_KEY" ;;
    9router) url="http://localhost:20128/v1/models"; key="$NINE_ROUTER_API_KEY" ;;
    agentrouter) url="https://agentrouter.org/v1/models"; key="$AGENTROUTER_API_KEY" ;;
    huancheng) url="https://api.hcnsec.cn/v1/models"; key="$HUANCHENG_API_KEY" ;;
    openrouter) url="https://openrouter.ai/api/v1/models"; key="$OPENROUTER_API_KEY" ;;
    nvidia_nim) url="https://integrate.api.nvidia.com/v1/models"; key="$NVIDIA_NIM_API_KEY" ;;
  esac
  status=$(curl -sS -m 8 -H "Authorization: Bearer ***" -H "User-Agent: hermes-agent/0.19.0" "$url" -o /dev/null -w "%{http_code}" 2>/dev/null || echo "timeout")
  echo "$p: $status"
done
```

Hasil probe DENGAN auth (18 Ags 2026): opencode-zen 200 (62 model) · 9router 200 (39) · huancheng 200 (20) · openrouter 200 (412) · nvidia_nim 200 (102) · **juan-router 401 & agentrouter 401 = key benar-benar ditolak server** (beda dengan 401 palsu tanpa header).

### Interpreting Results
- `200` — provider reachable, models listed
- `401/403` — cek DULU apakah probe menyertakan key: tanpa key = false positive; dengan key masih 401 = key mati/ditolak server
- `429 FreeUsageLimitError` — **kuota free habis** (Zen free tier) — bukan error config; lihat Pitfall 10
- `timeout` — network blocked, service down, ATAU (huancheng) server responsif di `/models` tapi lambat/timeout di inference
- `000` — connection refused

### Known Failure Modes
- **Huancheng** — `model_not_found` padahal key valid = model ID case-sensitive (lihat Pitfall 8); jangan salahkan key dulu, cek `/v1/models` untuk ID eksak
- **AgentRouter** — may return `unauthorized client detected` due to User-Agent whitelist; fix with `extra_headers: {User-Agent: hermes-agent/<version>}`
- **9router** — localhost gateway; if unreachable, check launchd service status

---

---

## References

- `references/model-catalog-structure.md` — Details on model_catalog.json schema and provider entries
- `references/oauth2-vs-apikey.md` — Deep dive on the two auth mechanisms
- `references/model-mapping-report.md` — Template laporan "mapping model aktif" (model utama, fallback chain, thread overrides, provider list, probe live) + snapshot nilai 15 Ags 2026
- `scripts/stress-test-models.py` — burst-test (8×) model rate limits terhadap endpoint OpenAI-compatible (default 9router) → ranking sukses/8 untuk pilih model thread & rantai fallback
- `scripts/probe-provider-models.py` — probe chat-completion non-streaming per model (UA configurable, key dari .env via KEY_ENV); verifikasi cepat model hidup/sebelum pasang di thread
- `references/9router-gateway-admin.md` — administrasi gateway 9router: schema DB (`data.sqlite`), derivasi CLI token (`x-9r-cli-token`), alur 2-langkah tambah connection (node → provider), multi-key failover via `priority`, sinyal saldo habis
- `references/openrouter-free-tier.md` — OpenRouter free tier (verified 16 Ags 2026): cek key via `GET /api/v1/key`, 19 model `:free` + highlights, rate limit 20/min·50/hari (1000/hari setelah beli ≥$10), error 402/429 + retry, pola provider config.yaml, lokasi key `~/.config/openrouter/env`
- `references/rtk-verification.md` — Recipe verifikasi RTK (Rust Token Killer): `rtk --version`, `rtk rewrite` exit codes (3=rewritten, 1=pass-through), `rtk gain` stats, cek plugin enabled di config, pitfalls (config write protection, plugins folder ≠ enabled)
- `references/provider-audit-2026-08-18.md` — Hasil sweep penuh 8 provider + tool-call test 18 Ags 2026: opencode-zen 429 kuota free habis, huancheng list-OK-chat-timeout, 9router/nvidia/openrouter yang hidup, rekomendasi fallback saat Zen 429
- `references/provider-scan-2026-08-29.md` — Hasil scan 29 Ags 2026: sweep 6 provider, stress-test 37 kandidat, burst 4x top candidates. Rekomendasi mapping thread+DM+fallback (belum diterapkan). Huancheng/agentrouter/ju-router EXCLUDED. OpenRouter free tier 429 massal.

---

### Pitfall 13: Huancheng `/v1/models` 200 ≠ chat jalan (verified 29 Ags 2026)
**Symptom:** `curl https://api.hcnsec.cn/v1/models` → HTTP 200, 20 model tercantum. Tapi semua chat-completion timeout (30s+).
**Reality:** Server Huancheng responsif di endpoint listing tapi inference engine mati/timeout untuk SEMUA model (DeepSeek-V4-Flash, glm-5.2, Kimi-K2.6, MiniMax-M3, DeepSeek-V4-Pro). **List ≠ usable** bahkan lebih parah dari kasus lain karena tidak ada satupun model yang bisa diselamatkan.
**Fix:** Selalu lakukan chat-probe minimal 1 model SEBELUM menyimpulkan provider "hidup". Script `scripts/probe-provider-models.py` dengan timeout 30s akan timeout juga, tapi itu bukti bahwa inference mati. Jangan pasang provider ini di fallback chain.

### Pitfall 14: 9router `ollama/qwen3.5` = 402 Payment Required (bukan gratis!)
**Symptom:** Model terdaftar di `curl localhost:20128/v1/models` tapi chat → HTTP 402.
**Reality:** 9router punya campuran model gratis DAN berbayar (saldo-based). `ollama/qwen3.5` termasuk yang berbayar. Juga `ollama/glm-5` → 410 Gone. Selalu cek error code: 402 = perlu saldo, 404 = model tidak ada, 400 = model salah/hapus, 500 = upstream error.
**Fix:** Prioritaskan model dengan prefix `ag/` (Gemini agent-optimized), `gh/` (GitHub pathway), dan `gemini/` (langsung dari Google) yang semuanya gratis di 9router. Hindari `ollama/*` kecuali sudah diverifikasi.

### Pitfall 15: OpenRouter free tier 429 massal (verified 29 Ags 2026)
**Symptom:** 17 dari 18 model `:free` di OpenRouter kena 429 rate limit saat di-probe beruntun.
**Reality:** Free tier OpenRouter (20 req/min, 50 req/hari tanpa credit) sangat terbatas. Model `google/gemma-4-31b-it:free` dan `poolside/laguna*.free` langsung 429. Hanya `nvidia/nemotron-3-super-120b-a12b:free` yang 3/4 OK (1 miss karena 429).
**Fix:** OpenRouter free tier TIDAK layak sebagai primary atau fallback utama. Gunakan hanya sebagai cadangan ketiga/keempat setelah 9router dan opencode-zen. Atau top-up ≥$10 untuk naik ke 1000 req/hari.

### Pitfall 16: Kimi models di 9router = 500 Internal Server Error
**Symptom:** `kimi/kimi-k3`, `kimi/kimi-k2.5`, `kimi/kimi-for-coding` semua return HTTP 500.
**Reality:** Upstream Moonshot AI quota exhausted atau endpoint bermasalah di 9router. Model kimi lain (`kimi/k3`, `kimi/kimi-k2.7-code`) perlu dicek terpisah.
**Fix:** Jangan pakai kimi models di 9router untuk saat ini. Alternatif coding: `laguna-s-2.1-free` (opencode-zen) atau `cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` (jika tidak 429).

### Pitfall 17: 9router (localhost:20128) adalah SPOF untuk SEMUA channel Telegram — JANGAN dimatikan saat "kill all localhost" (verified 29 Ags 2026)
**Symptom:** User minta "matikan semua localhost di mac". Agent menjalankan `kill` pada semua process Next.js (port 3000/5200/20128) — TERMASUK 9router (`/usr/local/lib/node_modules/9router/app`). Hasil: semua 5 channel Telegram (1/802/803/804/1172) diam/drop karena `channel_overrides` semuanya mengarah ke `9router@localhost:20128`. Hermes gateway TETAP jalan, tapi tiap chat Telegram gagal resolve model.
**Reality:** `9router` = gateway lokal yang dipakai SEMUA thread MC + channel Telegram override. Hanya CLI tray (`com.9router.autostart` → `9router/cli.js`, port 7000/5000) yang auto-start; **server Next.js (port 20128) tidak auto-restart** setelah di-kill. `com.niumination.9router-watch` (cache-watcher) non-kritis — boleh mati.
**Fix (verifikasi live 29 Ags — semua hijau setelahnya):**
1. **Saat "kill all localhost", SPARE:** 9router (PID next-server port 20128) + hermes gateway (python `hermes serve`, port ~54671). Yang AMAN dimatikan: dev server proyek (cc-acehtengah :3000, Mission Control :5200, 9router CLI tray :7000 — tapi SERVER :20128 jangan).
2. **Cek 9router mati:** `curl -s -o /dev/null -w '%{http_code}' -m 5 http://localhost:20128/v1/models` → `000` = mati.
3. **Restart server (bukan kill):** `launchctl kickstart -k gui/$(id -u)/com.9router.autostart` → port 20128 balik `200` dalam ~3 detik.
4. **Verifikasi channel:** `hermes config get platforms.telegram.channel_overrides` → semua 5 channel ke `9router`; lalu chat-probe tiap model via 9router (lihat Pitfall 18).
**Aturan umum:** "localhost cleanup" ≠ "matikan semua next-server". Selalu kecualikan gateway yang dipakai routing produktif (9router untuk Telegram, hermes gateway untuk sesi).

### Pitfall 18: Model reasoning (gemma-4-31b-it) butuh max_tokens besar — small max_tokens → "no content" false negative (verified 29 Ags 2026)
**Symptom:** Channel `1172` (`gemini/gemma-4-31b-it` via 9router) balas kosong saat probe `max_tokens:15`. Parser SSE membaca `content` = '' → disimpulkan "model mati".
**Reality:** gemma-4-31b-it adalah **reasoning model** — outputnya masuk ke `delta.reasoning_content`, BUKAN `delta.content`, sampai token reasoning habis. Dengan `max_tokens:15`, budget habis di reasoning → tidak ada `content` final.
**Fix:** Saat probe reasoning model, pakai `max_tokens:200` (atau lebih). Parser SSE harus akumulasi `delta.content` DAN `delta.reasoning_content`. Bukti: gemma-4-31b-it dengan `max_tokens:200` → `content: "OK"`. Berlaku untuk semua model ber-prefix reasoning (DeepSeek-R1 distil, nemotron-3-ultra, dll) — jangan vonis "no content" dari 1 probe token-kecil.

### Pitfall 19: opencode-zen butuh env `OPENCODE_ZEN_API_KEY` (bukan `OPENCODE_API_KEY`) — terminal.env_passthrough salah (verified 29 Ags 2026)
**Symptom:** Fallback `opencode-zen/hy3-free` gagal saat dijalankan dari subprocess terminal/toolshell, padahal chat-probe langsung (`https://opencode.ai/zen/v1`, key dari `.hermes/.env`) sukses 200.
**Reality:** Preset `opencode-zen` di `hermes_cli/auth.py` membaca `api_key_env_vars=("OPENCODE_ZEN_API_KEY",)`, base_url `https://opencode.ai/zen/v1`. Config `terminal.env_passthrough` lama cuma menyertakan `OPENCODE_API_KEY` (milik provider/endpoint LAIN — `api.opencode.ai/v1` yang balas "Not Found"). Gateway sendiri baca `OPENCODE_ZEN_API_KEY` dari `.hermes/.env` saat startup → jadi fallback di level gateway jalan, tapi terminal subprocess tidak.
**Fix:** `hermes config set terminal.env_passthrough '["HOME","PATH","HERMES_HOME","OPENROUTER_API_KEY","OPENCODE_API_KEY","OPENCODE_ZEN_API_KEY","OPENAI_API_KEY","AGENTROUTER_API_KEY","AEROLINK_API_KEY","HUANCHENG_API_KEY","NINE_ROUTER_API_KEY"]'`. Catatan: `config.yaml` sendiri REFUSE untuk di-patch/write_file (security) — WAJIB via `hermes config set`.

## Provider Scan Workflow (Class Procedure — 29 Ags 2026)

Ketika user meminta "scan & seleksi model untuk semua thread + DM + fallback":

1. **Load env keys:** `load_env(Path.home() / '.hermes' / '.env')` — jangan asumsi `/Volumes/.../.env` (sudah tidak ada di setup saat ini).
2. **Probe `/v1/models` per provider** dengan Authorization header + UA `hermes-agent/0.19.0`.
3. **Candidate selection:** hand-pick dari hasil list:
   - 9router: prefix `ag/` (Gemini flash variants), `gh/gpt-4o-mini`, `gemini/gemma-4-31b-it`
   - OpenRouter: hanya model `:free` yang survive 429
   - opencode-zen: `big-pickle`, `hy3-free`, `laguna-s-2.1-free`
4. **Single-chat probe** per candidate (timeout 8s, SSE parser).
5. **Burst stress-test 4x** per top candidate (interval 0.2s).
6. **Ranking:** burst success → latency → fungsi agent match.
7. **Sajikan rekomendasi BELUM diterapkan** — tunggu konfirmasi user sebelum edit config.yaml.

Script reusable: `~/.hermes/provider-sweep-rapid2.py` (single probe) dan `~/.hermes/burst-ultra.py` (4-burst stress test). Simpan di workspace agent, bukan di skill scripts (environment-specific).

## Related Skills

- `telegram-router-orchestration` — Model mapping per-thread Telegram, provider health snapshot
- `provider-fallback` — Fallback chain strategy, stress-test methodology

## References (29 Ags 2026 — Sweep Results)
- `references/provider-sweep-2026-08-29.md` — Full sweep report: all providers, excluded models, recommendations
- `references/model-mapping-report-2026-08-29.md` — Final mapping table with test results
- `references/provider-status-2026-08-29.md` — Quick reference: DM, thread overrides, fallback chain YAML
- `~/.hermes/provider-sweep-results.json` — Raw sweep data
- `~/.hermes/live-test-results.json` — Live burst test results (8x)
- `~/.hermes/MAPPING-UPDATE-SUMMARY.md` — Change log
- `telegram-router-orchestration` — Per-thread model mapping di Telegram gateway
- `provider-fallback` — Fallback chain strategy & troubleshooting
