# Laporan Konfigurasi Hermes Aktif
**Tanggal:** 6 Juli 2026  
**Profile:** Default (root)  
**Config:** `/Volumes/HermesAgent/HermesAgentUSB/data/config.yaml`  
**Config Version:** 27

---

## Ringkasan

| Aspek | Status | Catatan |
|-------|--------|---------|
| **Provider Utama** | opencode-zen | Model: `big-pickle` |
| **Provider Cadangan** | openrouter | Terdaftar, tidak aktif sebagai fallback |
| **Fallback** | ❌ Tidak ada | `fallback_providers: ''` — kosong |
| **Curator** | 🟡 Aktif | Setiap 168 jam, makan 3-5 API call |
| **Compression** | 🟡 `auto` | Pakai provider utama (opencode-zen) — parallel request! |
| **Vision** | ✅ Gemini | `gemini-2.5-flash` — sudah jalan |
| **Web Extract** | 🟡 `auto` | Juga pakai provider utama |
| **Approval** | 🟡 `auto` | |
| **Delegasi** | ✅ openrouter | Model `nex-agi/nex-n2-pro:free` |
| **Checkpoints** | ✅ Aktif | 20 snapshot, retensi 14 hari |
| **Streaming** | ❌ Mati | |
| **Session Auto-Prune** | ❌ Mati | Retensi 90 hari, DB tumbuh tanpa batas |
| **Kanban** | ✅ Aktif | Dispatch in-gateway tiap 60 detik |
| **Plugins** | spotify, rtk-rewrite | |

---

## 1. Model & Provider

```yaml
model:
  default: big-pickle
  provider: opencode-zen
  base_url: https://opencode.ai/zen/v1
  api_mode: chat_completions
```

| Key | Value |
|-----|-------|
| **Model** | `big-pickle` (OpenCode Zen) |
| **Provider Type** | OpenAI-compatible |
| **Endpoint** | `https://opencode.ai/zen/v1` |
| **Retry** | 3 attempts, 120s backoff |

### Provider Terdaftar

| Provider | Type | Status |
|----------|------|--------|
| **openrouter** | openai | Ada API key di `.env`, base_url `https://openrouter.ai/api/v1` |
| **opencode-zen** | — | Provider utama, tidak ada blok definisi explicit di `providers:` — Hermes recognize otomatis |

### Fallback Chain

```yaml
fallback_providers: ''         # ❌ Kosong — tidak ada fallback
credential_pool_strategies: {} # ❌ Kosong — tidak ada rotasi credential

# fallback_model:              # ❌ Di-comment — tidak aktif
#   provider: openrouter
#   model: anthropic/claude-sonnet-4
```

**Tidak ada fallback sama sekali.** Ketika OpenCode Zen 429, sistem mati total.

---

## 2. Auxiliary Systems

### Vision ✅ — SUDAH BAGUS

```yaml
auxiliary:
  vision:
    provider: gemini          # ✅ Terpisah dari provider utama
    model: gemini-2.5-flash   # Gratis, 60 RPM
    api_key: ''               # Pakai GOOGLE_API_KEY dari .env
```

### Compression 🟡 — BERMASALAH

```yaml
  compression:
    provider: auto            # 🟡 auto = opencode-zen = parallel request!
    model: ''
    timeout: 120
```

**`auto` berarti pakai provider utama (`opencode-zen`).** Setiap kali session di-compress, dia bikin API call PARALEL ke provider yang sama dengan main agent. Ini yang bikin rate limit makin parah.

### Lain-lain (semua `auto`)

| Subsystem | Provider | Efek |
|-----------|----------|------|
| **web_extract** | `auto` | Pakai opencode-zen |
| **skills_hub** | `auto` | Pakai opencode-zen |
| **approval** | `auto` | Pakai opencode-zen |
| **mcp** | `auto` | Pakai opencode-zen |
| **title_generation** | `auto` | Pakai opencode-zen |
| **triage_specifier** | `auto` | Pakai opencode-zen |
| **kanban_decomposer** | `auto` | Pakai opencode-zen |
| **profile_describer** | `auto` | Pakai opencode-zen |
| **curator** | `auto` | Pakai opencode-zen |

Semua subsystem `auto` fallback ke provider utama — **potensi parallel request bertumpuk**.

---

## 3. Curator

```yaml
curator:
  enabled: true           # 🟡 HIDUP
  interval_hours: 168     # Setiap 7 hari
  min_idle_hours: 2       # Tunggu 2 jam idle sebelum jalan
  stale_after_days: 30
  archive_after_days: 90
  prune_builtins: true
  backup:
    enabled: true
    keep: 5
```

### Apakah Curator Perlu?

**Fungsinya:**
- Evaluasi skill usage secara otomatis tiap minggu
- Arsipkan skill yang sudah 30 hari tidak dipakai
- Prune skill yang sudah 90 hari tidak dipakai
- Backup sebelum prunning

**Analisis untuk workflow kamu:**

| ✅ Keuntungan | ❌ Kerugian |
|--------------|-------------|
| Skills tetap rapi | **Makan 3-5 API call per minggu** dari provider utama |
| Skill usang otomatis dibersihkan | Skillset kamu relatif stabil — jarang ganti skill |
| Backup otomatis | Curator jalan di background, tidak terlihat — boros quota tanpa sadar |
| | Interval 7 hari terlalu sering untuk skill yang jarang berubah |

**Verdict:** ❌ **Tidak perlu untuk workflow kamu.** Skillset relatif tetap, dan 3-5 API call/minggu ke opencode-zen adalah pemborosan quota yang berharga. Lebih baik disable dan lakukan pruning manual kalau diperlukan.

---

## 4. Environment Variables (`.env`)

| Variable | Status | Untuk |
|----------|--------|-------|
| `OPENCODE_ZEN_API_KEY` | ✅ Aktif | Provider utama |
| `OPENCODE_API_KEY` | ✅ Aktif | Cadangan / fallback |
| `OPENROUTER_API_KEY` | ✅ Aktif | Delegasi, fallback |
| `GOOGLE_API_KEY` | ✅ Aktif | Gemini (vision & compression) |
| `TELEGRAM_BOT_TOKEN` | ✅ Aktif | Telegram gateway |
| `GITHUB_TOKEN` | ✅ Aktif | GitHub MCP |
| `GH_PAT` | ✅ Aktif | GitHub Personal Access Token |
| `SUPABASE_PG_URL` | ✅ Aktif | Database ekosistem |
| `VERCEL_TOKEN` | ✅ Aktif | Vercel deployment |
| `TAVILY_API_KEY` | ✅ Aktif | Web search |
| `FAL_KEY` | ✅ Aktif | Image generation (FAL) |
| `DISCORD_BOT_TOKEN` | ❌ Comment | Tidak aktif (#) |

---

## 5. MCP Servers

| Server | Status | Command |
|--------|--------|---------|
| **time** | ✅ Aktif | `mcp-server-time` (Python) |
| **github** | ✅ Aktif | `npx @modelcontextprotocol/server-github` |
| **filesystem** | ✅ Aktif | `mcp-server-filesystem` (terbatas ke `/Users/zaryu`) |
| **hermes-sqlite** | ✅ Aktif | SQLite kanban DB |
| **hermes-postgres** | ✅ Aktif | PostgreSQL supabase |
| **ponytail** | ✅ Aktif | Node.js (tools/ponytail/) |

---

## 6. Delegasi (Sub-agents)

```yaml
delegation:
  model: nex-agi/nex-n2-pro:free
  provider: openrouter
  base_url: https://openrouter.ai/api/v1
  inherit_mcp_toolsets: true
  max_iterations: 50
  child_timeout_seconds: 600
  max_concurrent_children: 3
  max_spawn_depth: 1
  orchestrator_enabled: true
```

Sub-agent pakai **OpenRouter** (model free tier) — terpisah dari provider utama. Sudah bagus.

---

## 7. Sistem Pendukung

| Fitur | Status | Detail |
|-------|--------|--------|
| **Compression** | ✅ Aktif | Threshold 50%, target 20%, max 400 msg |
| **Checkpoints** | ✅ Aktif | 20 snapshot, retensi 14 hari |
| **Tool Loop Guardrails** | ✅ Aktif | Hard stop setelah 5 error |
| **Security (Tirith)** | ✅ Aktif | Approval system untuk command berbahaya |
| **Prompt Caching** | ✅ Aktif | Cache TTL 5 menit |
| **Streaming** | ❌ Mati | Output dikirim sekaligus setelah selesai |
| **Session Auto-Prune** | ❌ Mati | DB tumbuh tanpa limit |
| **Memory** | ✅ Aktif | 2200 char memory, 1375 char user profile |

---

## 8. Masalah Teridentifikasi

| # | Masalah | Severity | Solusi |
|---|---------|----------|--------|
| 1 | **Compression `auto` pakai opencode-zen** | 🔴 Tinggi | Ganti ke `gemini` (GOOGLE_API_KEY sudah ada) |
| 2 | **Curator enabled** | 🟡 Sedang | Disable (tidak diperlukan) |
| 3 | **Semua subsystem `auto`** | 🟡 Sedang | Alihkan ke Gemini masing-masing |
| 4 | **Tidak ada fallback provider** | 🟡 Sedang | Sesuai instruksi kamu — aman |
| 5 | **Session auto-prune mati** | 🟢 Rendah | DB akan tumbuh besar dalam 6+ bulan |
| 6 | **Streaming mati** | 🟢 Rendah | Hanya soal preferensi UX |

---

## 9. Rekomendasi Langsung

### 🔴 Prioritaskan: Compression → Gemini

**Required:**
- `GOOGLE_API_KEY` ✅ **SUDAH ADA** di `.env` (dipakai vision)
- Tinggal ganti config:

```bash
hermes config set auxiliary.compression.provider gemini
hermes config set auxiliary.compression.model gemini-2.5-flash
```

**Tidak perlu API key tambahan.** Gemini sudah jalan untuk vision — tinggal dipakai juga untuk compression.

### 🟡 Bisa Juga: Matikan Curator

```bash
hermes config set curator.enabled false
```

Hemat 3-5 API call/minggu ke opencode-zen.

---

*Laporan dibuat otomatis berdasarkan `config.yaml` (v27, 649 baris) dan `.env` saat ini.*
