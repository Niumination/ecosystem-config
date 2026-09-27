---
name: 9router-model-mapping
description: "Configure and maintain 9router model mapping for Hermes — fallback chain, channel overrides, quota-aware model selection"
version: "3.0.1"
author: Afrizal Munthe
tags: [9router, model-mapping, fallback, quota, niumination, hermes-config]
updated: 2026-09-27
---

# 9Router Model Mapping

## Overview
9router (localhost:20128) is a **secondary/cadangan** provider. Primary provider is `nous` (OAuth, `~/.hermes/auth.json`). 9router catalog **berflapping** — terukur 67 → 51 → 67 dalam 27 Sep 2026. Namespace `explabs` **tidak ada lagi**.

## Live Catalog — 27 Sep 2026 (probe 22:2x, `curl localhost:20128/v1/models`)

**Total: 67 model** | **Namespace:** `gh` 34 · `kr` 24 · `ag` 4 · `cf` 2 · `gemini` 1 · `openrouter` 1 · tanpa-prefix 1 (`opencode-combo`)
**Tidak ada lagi:** `explabs` · `claude-combo` · `experimentallabs`

> ⚠️ **Katalog ini berflapping.** Dalam satu hari terukur 67 → 51 → 67. Angka di sini adalah snapshot, bukan jaminan. Selalu probe ulang sebelum menyimpulkan; jangan menulis angka katalog ke dokumen tanpa mencatat waktu probe-nya.

| Namespace | Count | Isi nyata (27 Sep 2026) |
|-----------|-------|--------------------------|
| `gh` | 34 | GitHub Models — `gpt-4o`, `gpt-4o-mini`, `gpt-4.1`, `gpt-5-mini`, `gpt-5.4-mini-free-auto`, `gpt-5.6-luna`, `gpt-5.6-luna-free-auto`, `gpt-6-luna`, `claude-haiku-4.5`, `kimi-k3`, `kimi-k3-base`, `kimi-k3-copilot`, `mai-code-1*`, `copilot-search-a/b/c`, `exec-agent-a/b/c`, `trajectory-compaction`, `gpt-3.5-turbo*`, `gpt-4*` |
| `kr` | 24 | Kimi/Kiro — `deepseek-3.2` (+`thinking`/`agentic`), `minimax-m2.1`/`m2.5` (+ varian), `claude-sonnet-4` (+ varian), `glm-5-thinking` (+ varian), `qwen3-coder-next` (+ varian), `auto`/`auto-thinking` |
| `ag` | 4 | Antigravity — `claude-opus-4-6-thinking`, `claude-sonnet-4-6`, `gemini-3.8-flash`, `gpt-oss-120b-medium` |
| `cf` | 2 | Cloudflare Workers — `@cf/moonshotai/kimi-k2.6`, `@cf/zai-org/glm-4.7-flash` |
| `gemini` | 1 | Google AI Studio native — `gemini-3.8-flash` |
| `openrouter` | 1 | `typesafe/jev-1.13` |
| (tanpa prefix) | 1 | `opencode-combo` |

## Current Config — 27 Sep 2026 (`~/.hermes/config.yaml`)

```yaml
model:
  provider: nous
  default: stealth/space-bunny-alpha
  base_url: https://inference-api.nousresearch.com/v1

providers:
  9router:
    base_url: http://localhost:20128/v1
    api_mode: chat_completions
    key_env: NINE_ROUTER_API_KEY
  huancheng:
    base_url: https://api.hcnsec.cn/v1
    api_mode: chat_completions
    key_env: HUANCHENG_API_KEY
    default_model: auto
  atria:
    base_url: https://api.atria-asi.ai/v1
    api_mode: chat_completions
    key_env: ATRIA_API_KEY
    default_model: Atria-Dawn-Preview

cron:
  model: meituan/longcat-2.0:free
  model_provider: nous

x_search:
  model: upstage/solar-pro4:free
  provider: nous
```

## Channel Overrides — 27 Sep 2026 (verified in config.yaml)

| Channel | Model | Provider | Notes |
|---------|-------|----------|-------|
| 1 (Home) | `inclusionai/ling-3.0-flash-fin:free` | nous | Primary thread |
| 802 (Research) | `inclusionai/ling-3.0-flash-sante:free` | nous | |
| 803 (Builder) | `meituan/longcat-2.0:free` | nous | |
| 804 (QA/Pengawas) | `deepseek/deepseek-v4-flash-0731:free` | openrouter | |
| 1172 (Kreator) | `poolside/laguna-s-2.1:free` | nous | |
| 7402 (Serbaguna) | `meituan/longcat-2.0:free` | nous | Flex-thread |
| 8853 (ASN Admin) | `sensenova-6.8-flash-lite` | huancheng | Dinas ASN |

## Other Active Mappings

| Function | Model | Provider |
|----------|-------|----------|
| Cron | `meituan/longcat-2.0:free` | nous |
| x_search | `upstage/solar-pro4:free` | nous |
| Delegation | `nvidia/nemotron-3-ultra-550b-a55b:free` | openrouter |
| Image Gen | `gpt-image-2-medium` | openai-codex |
| Auxiliary Vision | (env: `AUXILIARY_VISION_API_KEY`) | auto |
| Atria (custom) | `Atria-Dawn-Preview` | atria — `https://api.atria-asi.ai/v1` |
| Stt | whisper-1 | openai |

## Nous `:free` Models — 19 Sep 2026 snapshot (7 terverifikasi)

`inclusionai/ling-3.0-flash-fin:free` · `inclusionai/ling-3.0-flash-sante:free` · `meituan/longcat-2.0:free` · `poolside/laguna-s-2.1:free` · `poolside/laguna-xs-2.1:free` · `stepfun/step-3.7-flash:free` · `upstage/solar-pro4:free`

## 9router sebagai Fallback (cadangan)

9router **bukan** mapping utama. Fungsinya: (1) fallback saat nous tidak terjawab, (2) sumber model alternatif.

**Model yang benar-benar ada di katalog 27 Sep 2026** (semua diverifikasi lewat `/v1/models`):

| Model | Namespace | Catatan |
|---|---|---|
| `gh/gpt-4o-mini` | gh | GitHub Models |
| `gh/claude-haiku-4.5` | gh | GitHub Models — claude di prefix `gh`, **bukan** `kr` |
| `ag/claude-sonnet-4-6` | ag | Antigravity |
| `ag/claude-opus-4-6-thinking` | ag | Antigravity |
| `kr/claude-sonnet-4` | kr | Kimi/Kiro |
| `kr/deepseek-3.2` | kr | Kimi/Kiro |
| `gemini/gemini-3.8-flash` | gemini | AI Studio native |
| `cf/@cf/moonshotai/kimi-k2.6` | cf | Cloudflare Workers |
| `openrouter/typesafe/jev-1.13` | openrouter | — |

**Model yang TIDAK ada (jangan dipakai):** `kr/claude-haiku-4.5` · `kr/claude-sonnet-4.5` · `kr/claude-opus-5-thinking` · `kr/claude-sonnet-5-thinking` · `kr/gpt-5.6-sol-*` · `gemini/gemini-3.5-flash-lite` · `cf/@cf/meta/llama-3.3-70b-instruct-fp8-fast`

**Pitfall namespace:** prefix tidak bisa ditebak dari nama model. `claude-haiku-4.5` ada di `gh/`, `claude-sonnet-4.6` ada di `ag/`, `claude-sonnet-4` ada di `kr/`. **Selalu cek `/v1/models` sebelum menulis nama model ke config.**

## CRITICAL Rules

### 0. Jangan edit `config.yaml` pakai `hermes config set` untuk perubahan multi-key
`hermes config set` ** menulis ulang seluruh file dan membuang blok komentar di EOF secara senyap.**
Terbukti 27 Sep 2026: dua panggilan `hermes config set` menghapus blok komentar
`# ── Fallback Model ──` 22 baris di akhir file (877 → 855 baris). Key-nya sendiri ditulis
benar; yang hilang adalah dokumentasi yang dibaca sesi berikutnya.

Prosedur aman:
1. `cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak-$(date +%Y%m%d)`
2. Edit in-place dengan `str.replace` yang meng-`assert s.count(old) == 1` — gagal keras
   kalau match 0 atau >1, daripada diam-diam merusak routing.
3. `diff` backup vs baru — harus hanya baris yang dimaksud.
4. `python3 -c "import yaml;yaml.safe_load(...)"` untuk konfirmasi struktur.
5. `grep -c ""` kedua file — jumlah baris harus sama kecuali memang menambah baris.

`hermes config set` aman untuk satu key sekali pakai yang tidak cared. Apapun yang menyentuh
`platforms.telegram.channel_overrides` bukan sekali pakai.
Detail lengkap + perbandingan ketiga jalur tulis: skill `hermes-config-mutation-safety`.

### 0b. 9router butuh `NINE_ROUTER_API_KEY` di environment proses
`curl` dengan token hardcoded → `401 invalid_api_key`. Kunci hanya ada di `~/.hermes/.env`:
```bash
set -a; source ~/.hermes/.env; set +a
```
Kalau gateway/sesi tidak memuat `.env`, routing `provider: 9router` gagal 401 walau 9router
sendiri sehat. Cek env dulu sebelum menyalahkan model saat menambah channel override 9router.

### 1. Verify in Live Catalog
```bash
curl -s http://localhost:20128/v1/models     # 200 + JSON tanpa auth
```
**Verified 27 Sep 2026:** `/v1/models` **tidak** butuh header auth. Yang butuh header `Authorization` adalah `/v1/chat/completions`. Klaim lama ("tanpa header → HTML 404") sudah dibantah oleh probe.

### 2. Provider adalah `nous`, bukan 9router
Config aktual: `model.provider: nous`. 9router hanya cadangan.

### 3. No `explabs` namespace
Provider `explabs` sudah dihapus dari 9router. Gunakan `nous` atau `openrouter`.

### 4. Nous OAuth, bukan API key
`nous` menggunakan OAuth device-code di `~/.hermes/auth.json`. `key_env: NINE_ROUTER_API_KEY` menyesatkan untuk provider `nous`.

### 5. Mission Control — MATI (verified 27 Sep 2026, 22:0x)
`localhost:5200` dan `localhost:3000` keduanya **HTTP 000** (connection refused). Tidak ada proses `next-server` untuk MC, dan tidak ada listener di kedua port. Dua plist MC (`com.niu.missioncontrol`, `com.niumination.missioncontrol`) **tidak ter-load** di launchd. Klaim lama "MC sehat, butuh auth" **tidak berlaku** — tidak ada endpoint yang bisa dijawab.

### 6. Python Env Expansion Pitfall
`$VAR` does **not** expand inside Python string literals. Use `os.environ.get("NINE_ROUTER_API_KEY", "")`.

### 7. Config Sync Requirement
When updating Hermes model config, mirror to:
- `~/.hermes/config.yaml`
- `~/Desktop/Niumination/apps/JHermUSB-portable/config/config.yaml`

## Quota Backend Map (9router namespaces)

| Prefix | Backend | Notes |
|--------|---------|-------|
| `gh/*` | GitHub Models | Independent per repo |
| `kr/*` | Kimi (Kiro) | Independent |
| `ag/*` | Antigravity (Google AI) | ⚠️ ALL share same quota |
| `cf/*` | Cloudflare Workers | Independent |
| `gemini/*` | Google AI Studio | Separate from Antigravity |
| `openrouter/*` | OpenRouter | Independent |

## Verification Checklist
- [ ] All models in channel_overrides exist and are verified
- [ ] No `explabs` namespace in any mapping
- [ ] Primary provider is `nous` (not 9router)
- [ ] 9router catalog di-probe (tanpa auth; header hanya untuk /chat/completions)
- [ ] Mission Control dicek terpisah (27 Sep 2026: 5200 & 3000 mati)
- [ ] Backup created before edit

## Related Skills
- `model-status-checker` — 3-tier health probe
- `provider-fallback` — general fallback strategy
- `config-history-review` — audit config changes
- `ecosystem-dox-maintenance` — DOX hygiene
- `model-mapping` — model-mapping.md source of truth

## Rollback
```bash
cp ~/.hermes/config.yaml.bak-YYYYMMDD ~/.hermes/config.yaml
```

## Change Log
- 2026-09-27 v3.0.1 — Koreksi 7 klaim salah hasil audit: katalog 67 (bukan 51), `/v1/models` tanpa auth, MC MATI (bukan butuh-auth), 4 model fallback tidak ada (prefix salah), 2 model `kr` tidak ada. Semua klaim kini hasil probe langsung.
- 2026-09-27 v3.0.0 — Rewrite: nous sebagai primary, 9router cadangan, `explabs` dihapus
- 2026-09-07 v2.0.0 — Previous: 9router primary, `explabs/` namespace active
