---
name: provider-fallback
description: "Handle AI provider failures and fallback to working providers"
version: 1.0.0
author: agnes
tags: [provider, fallback, troubleshooting, configuration]
---

# Provider Fallback Strategy

## Purpose
When primary LLM provider fails (invalid token, unauthorized, empty key), automatically fallback to working providers.

## Priority Order

1. **Local 9router** (localhost:20128)
   - Most reliable, no external dependencies
   - 48+ models: `gratis`, `capek`, `gila`, `gemini-*`, `claude-*`
   - Requires: 9router application running

2. **OpenRouter** (key free-tier VALID sejak 16-Ags-26)
   - Wide model selection — 19 model `:free` (gemma-4, nemotron, gpt-oss-20b, dll)
   - Rate limit free: 20 rpm / 50 rpd tanpa credit; 1000 rpd setelah top-up ≥ $10
   - Requires: `OPENROUTER_API_KEY` env var (simpan di `~/.config/openrouter/env`)
   - Detail & model teruji: `references/openrouter-free-tier.md`

3. **Direct providers** (Anthropic, OpenAI, etc.)
   - Best quality but requires valid keys

## Diagnosis Steps

```bash
# 1. Check all provider keys
env | grep -E "API_KEY|AUTH" | cut -d= -f1

# 2. Test each endpoint
curl -s --max-time 5 https://api.hcnsec.cn/v1/chat/completions \
  -H "Authorization: Bearer $HUANCHENG_API_KEY" \
  -d '{"model":"auto","messages":[{"role":"user","content":"test"}]}'

# 3. Check local 9router
curl -s http://localhost:20128/v1/models | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f'9router: {len(d.get(\"data\",[]))} models')
"

# 4. Check memory status
# If near 99%, consider consolidation
```

## Fix Procedure

### Quick Fix (Session)
```yaml
# Update config.yaml
model:
  default: gratis
  provider: 9router
  base_url: http://localhost:20128/v1
```
Then: `/reset` or restart session

### Permanent Fix
1. Fix primary provider (regenerate key, update .env)
2. Keep 9router as fallback in config
3. Monitor provider health with `hermes doctor`

## AgentRouter Specifics (dikoreksi 13 Ags 2026)

**AgentRouter.org IS native Hermes config.yaml provider** — klaim lama "butuh custom TS extension" SALAH. Yang sebenarnya: WAF mem-whitelist User-Agent.

| Aspect | Detail |
|--------|--------|
| Auth | `AGENTROUTER_API_KEY` (env) + `extra_headers: {User-Agent: hermes-agent/<versi>}` di `providers.agentrouter` — UA lain (curl, OpenAI/Python) → 401 `unauthorized client detected` |
| Model | Hanya `gpt-5.6-sol` yang respond; Claude (`claude-opus-4-8`, `claude-opus-5`) → `Budget pool quota has been exhausted` |
| ⚠️ KONTEN | Blokir **frasa Bahasa Indonesia ≥2 kata** (`content-blocked` / `sensitive words detected`); EN/Cina/kata-tunggal-ID lolos → TIDAK layak untuk thread berbahasa Indonesia |
| Verifikasi | `curl /v1/models -H "User-Agent: hermes-agent/0.19.0"` → 200 = key & provider OK |
| Detail | `hermes-provider-config` Pitfall 3 & 6; `references/agentrouter-integration.md` di `telegram-router-orchestration` |

---

## Fallback Chain Configuration (fallback_providers)

Semantik kunci (diverifikasi dari source `gateway/run.py` + `hermes_cli/fallback_config.py`):

- **GLOBAL** — `fallback_providers`/`fallback_model` berlaku untuk SEMUA thread + DM + cron. Tidak bisa per-channel.
- **Tidak ada fallback per-channel** — `ChannelOverride` (`platforms.<name>.channel_overrides`) hanya punya `model`, `provider`, `system_prompt`. Per-thread hanya bisa beda model UTAMA.
- **Multi-level chain** — `fallback_providers` menerima LIST; urutan = prioritas (L1 gagal → L2 → L3...). `fallback_providers` diutamakan atas legacy `fallback_model`; `get_fallback_chain()` menggabungkan keduanya.
- **Auto-refresh tanpa restart** — gateway `_refresh_fallback_model()` baca ulang config.yaml dari disk tiap agent create/reuse (cache mtime-keyed). Ubah file → langsung efektif di pesan berikutnya.
- **⚠️ JANGAN pakai `model: auto` sebagai fallback** — `auto` di-resolve 9router ke provider tanpa kredensial (openai) → `404 No active credentials for provider` → error TOTAL ke user (non-retryable, bukan pindah model).

Contoh chain 3 level (diversifikasi jalur provider — satu provider down tidak mematikan semua level):
```yaml
fallback_providers:
  - provider: 9router
    model: JuanRouter/glm-5.2
  - provider: 9router
    model: cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b
  - provider: 9router
    model: gratislonggar
```

### ⚠️ Edit chain NON-interaktif (verified 19 Ags 2026)

- `hermes fallback remove <nama>` dan `hermes fallback clear` adalah **picker interaktif** — di shell non-interaktif mereka berhenti nunggu `[y/N]` lalu cancel ("Cancelled") tanpa mengubah apa pun.
- `hermes config set fallback_providers '[{"provider":...}]'` **menulis JSON sebagai STRING** (`fallback_providers: '[{...}]'`), bukan list YAML → `hermes fallback ls` tampil "No fallback providers configured" padahal key ada.
- **Fix yang benar (edit YAML langsung):** backup dulu (`cp config.yaml config.yaml.bak-before-fallback-fix`), lalu javascript-style replace di file (patch tool) atau python yaml — ganti `fallback_providers: '[...]'` (string) jadi block list:
  ```yaml
  fallback_providers:
    - provider: opencode-zen
      model: hy3-free
  ```
  Verifikasi `hermes fallback ls` → "Fallback chain (1 entry)".

## Memilih Model Fallback: Stress-Test Rate Limit

Jangan pilih fallback dari asumsi — ukur dengan burst request (8 request beruntun cepat per kandidat, hitung sukses vs HTTP 429; `stream:false` + parser SSE karena 9router kadang balas SSE walau diminta JSON). **Gunakan script runnable:** `scripts/stress_test_models.py` (probe + burst + ranking; `--key-env`/`--env-file` untuk key, `--bursts` untuk pass cepat). Recipe & hasil lengkap: `references/fallback-chain-selection-2026-08-13.md`.

Hasil nyata (2026-08-13):
- **8/8 (longgar):** `gratislonggar`, `gemini/gemini-3.5-flash-lite`, `gemini/gemma-4-31b-it`, `cf/deepseek-r1`, `cf/zai-org/glm-4.7-flash`, `JuanRouter/glm-5.2`, `JuanRouter/gemini-3.5/3.6-flash`, `JuanRouter/qwen3.7-plus`
- **Lemah (429 sering):** `gc/gemini-2.5-flash` (2/8), `gc/gemini-2.5-flash-lite` (4/8), **`nvidia/z-ai/glm-5.2` (2/8)**, **`nvidia/minimaxai/minimax-m3` (1/8)**

⚠️ **Model sama ≠ kuota sama per jalur:** `nvidia/z-ai/glm-5.2` (2/8) vs `JuanRouter/glm-5.2` (8/8) — selalu cek jalur provider yang DIPAKAI thread, bukan nama model.
⚠️ **Kuota berubah antar-run:** `gemini/gemini-3.6-flash` 7/8 (sore) → 2/8 (malam). Test ULANG saat mau dipakai — jangan pakai data stress lama.
⚠️ **JuanRouter = BERBAYAR (saldo-based, rule user):** untuk model UTAMA thread pakai jalur gratis (`cf/`, `gemini/`); JuanRouter hanya untuk fallback chain. Mengganti model thread yang lemah? Pilih model **sama keluarga di jalur beda** (glm-5.2 lemah di nvidia → glm-4.7-flash di cf) — kualitas kontinu.
**Test juga model UTAMA thread, bukan cuma fallback:** stress test menemukan 2 model thread lemah yang lolos probe tunggal (glm-5.2 2/8 → diganti cf/glm-4.7-flash; minimax-m3 1/8 → diganti gemini/gemma-4-31b-it).

---

## Multi-Key Failover (via 9Router)

For high-availability LLM routing (e.g., JuanRouter, OpenCode, AgentRouter), use **9Router's multi-key failover** — the router automatically retries failed requests (429, 403, 503) with the next available key for the same provider.

### How It Works

1. **Create a provider node** (POST `/api/provider-nodes`) — defines the base URL and API type (e.g., `openai-compatible`)
2. **Add multiple connections** (POST `/api/providers`) — each with a different API key, same provider node ID
3. **Router handles failover** — when a request fails, 9Router retries with the next connection in priority order

### API Reference

See `references/9router-multi-key.md` in `hermes-external-integration` skill for:
- POST `/api/provider-nodes` + `/api/providers` examples
- CLI auth token calculation
- Pitfalls (403 `/models`, priority order, User-Agent)
- Full JuanRouter multi-key setup example

### Usage in Hermes

Model reference:
```
model: JuanRouterMulti/claude-opus-4-8
```

9Router handles failover automatically — no Hermes config changes needed.

### When to Use

- **JuanRouter**: key lama saldo habis → key baru khusus Claude
- **OpenCode**: multi-key untuk failover
- **AgentRouter**: multi-key untuk bypass rate limits

### Pitfalls

1. **`/models` endpoint 403 for special keys** — some keys (e.g., Claude-only keys) block `/models`. Use User-Agent `opencode/1.18.18` and probe via chat completion instead.
2. **Provider node ID required** — you cannot add a connection without first creating a node.
3. **Priority order** — lower numbers = higher priority. Set key1=1, key2=2, etc.
4. **No `/models` listing for Claude-only keys** — verified 15 Aug 2026: `claude-opus-4-8` only, `/models` 403.

When removing a provider from `config.yaml`, don't just empty fields — fully remove:

### Step 1: Remove provider from `providers:` section
```bash
# Using hermes config set (preferred):
hermes config set providers.<provider>.base_url ""
hermes config set providers.<provider>.key_env ""
hermes config set providers.<provider>.type ""
```

### Step 2: Remove other references
```bash
# Check for delegation reference:
hermes config show | grep "delegation:"

# Remove if found:
hermes config set delegation.provider gemini  # or your preferred fallback
```

### Step 3: Remove section-level config (e.g. `openrouter:` block)
```bash
# For openrouter response_cache section:
hermes config set openrouter.response_cache false
hermes config set openrouter.response_cache_ttl 0
hermes config set openrouter.min_coding_score 0
```

### Step 4: Verify cleanup
```bash
grep -c "openrouter\|agentrouter" /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml
# Should return 0 after cleanup
```

### Step 5: Clean caches (optional but recommended)
```bash
rm -f /Volumes/HermesAgent/HermesAgentUSB/data/provider_models_cache.json
rm -f /Volumes/HermesAgent/HermesAgentUSB/data/cache/model_catalog.json
```

## Status of All Providers (2026-08-13)

### Tested & Working
| Provider | Status | Models | Endpoint |
|----------|--------|--------|----------|
| **9router (Local)** | ✅ Working | 33 model (v0.5.50, +JuanRouter berbayar) | `http://localhost:20128/v1` |
| **Huancheng (API)** | ⚠️ Token active but invalid | 20 models | `https://api.hcnsec.cn/v1` |

### Broken / Removed
| Provider | Issue | Action Taken |
|----------|-------|--------------|
| **OpenRouter** | ✅ Free-tier key valid (16-Ags-26) — 19 model `:free`, 20rpm/50rpd | Key baru disimpan `~/.config/openrouter/env`; lihat `references/openrouter-free-tier.md` |
| **AgentRouter** | ✅ Working (native + extra_headers UA) | Hanya `gpt-5.6-sol`; Claude budget pool exhausted; blokir frasa ID ≥2 kata — idle, tidak dipasang di thread |

### Not Configured
| Provider | Reason |
|----------|--------|
| **Aerolink** | 404 endpoint, key exists but endpoint not responsive |
| **Anthropic** | No API key configured |
| **OpenAI** | No API key configured |

## Status of All Providers (2026-08-18 — audit ulang, lihat `references/provider-audit-2026-08-18.md`)

| Provider | /v1/models | Chat | Tool-call | Verdict |
|---|---|---|---|---|
| opencode-zen | ✅ 200 (62 model) | ⚠️ sebagian 429 | ✅ | Primary — keluargakeputusan (lihat false-429 di bawah) |
| 9router (lokal) | ✅ 200 (39 model) | ✅ | ✅ 1.1s (gemini-3.7-flash) | Layak fallback |
| nvidia_nim | ✅ 200 (102 model) | ✅ | ✅ 0.7s (llama-3.1-8b) | Layak cadangan |
| openrouter | ✅ 200 (412 model) | ⚠️ 15 free, sebagian 429 | ✅ | Layak, terbatas |
| huancheng | ✅ 200 (20 model) | ❌ **timeout SEMUA chat** | ❌ | TIDAK layak fallback |
| juan-router | ❌ 401 | — | — | Key ditolak |
| agentrouter | ❌ 401 (tanpa UA hermes) | — | — | Key ditolak |
| aerolink | key ada, URL tidak aktif | — | — | Tidak aktif |

### ⚠️ False-429 lesson (dikoreksi user 19 Ags 2026)

Probe curl ad-hoc ke `opencode.ai/zen/v1` dengan `OPENCODE_ZEN_API_KEY` dari `.env` memberi **HTTP 429** untuk `big-pickle` & `deepseek-v4-flash-free` — **TAPI `big-pickle` AKTIF di sesi gateway**. Runtime Hermes memakai metode/key berbeda dari probe manual, jadi 429 hanya membuktikan "endpoint menolak key itu", BUKAN "model mati".

**Aturan:** sebelum melaporkan provider/model mati, verifikasi dengan jalur yang sama dengan runtime gateway (config default + env yang di-export ke gateway). Audit ad-hoc = rekomendasi, bukan status final tanpa konfirmasi user. Jangan pernah menurunkan model primary dari 429 probe manual.

### Model Zen free yang HIDUP saat big-pickle 429 di probe (tool-call ✅)

- `hy3-free` (3.6s), `laguna-s-2.1-free` (3.6s), `nemotron-3-ultra-free` (17s)
- 9router `gemini/gemini-3.7-flash` = tercepat 1.1s; `gratislonggar` resolve ke gemini-3.6 (⚠️ responsnya **SSE stream** — test non-streaming salah-parse)
- Fallback resmi (D-0004): free tier `opencode-zen` (`big-pickle` / `nemotron-3-ultra-free` primary, fallback se-provider `hy3-free` / `*-free` lain) + free tier Nous Portal (`:free`); buang zoo (juan/9router/huancheng) dari chain. Prinsip core: ganti lintas PROVIDER (zen↔nous) atau model asing = HALT + HANDOFF, bukan silent hop. Sesama provider = bebas lanjut.

## Notes

- `channel_overrides` & `fallback_providers` di config.yaml: gateway re-read per turn (auto-refresh, TANPA restart). Restart hanya perlu untuk perubahan `.env`/key baru atau perubahan config lain yang dibaca sekali saat startup
- Local providers (9router) are most reliable for development
- Always test provider connectivity before starting complex tasks
- Memory capacity affects context retention — keep below 90%
- See `references/agentrouter-investigation-2026-08-13.md` for detailed AgentRouter diagnosis and cleanup procedure
