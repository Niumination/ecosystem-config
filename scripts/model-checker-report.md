# 📊 Laporan Model 9router — 14 September 2026

**Sumber:** `http://127.0.0.1:20128/v1/models`
**Total model terdaftar:** 511
**Waktu cek:** 08:30–08:45 WIB

---

## 😂 Ringkasan Eksekutif

| Status | Jumlah Model | Persentase |
|--------|-------------|------------|
| ✅ **Bisa dipakai** (sample OK) | ~31 | ~6% |
| ❌ **Tidak bisa** (503/403/410/timeout) | ~480 | ~94% |

**Catatan kritis:** Provider `explabs` menyumbang **342 model (67%)** dan **semuanya HTTP 503**. Ini adalah penyumbang terbesar dari "tidak bisa".

---

## 🔵 PROVIDER YANG BISA DIPAKAI

### 1. `gemini` (Google AI Studio) — 8 model, 5 OK
| Model | Latency | Status |
|-------|---------|--------|
| `gemini/gemini-3.5-flash-lite` | 694ms | ✅ OK |
| `gemini/gemini-3-flash-preview` | 982ms | ✅ OK |
| `gemini/gemini-3.1-flash-lite-preview` | 1280ms | ✅ OK |
| `gemini/gemini-3.6-flash` | 1552ms | ✅ OK |
| `gemini/gemini-3.8-flash` | 6025ms | ✅ OK (lambat) |
| `gemini/gemini-3.7-flash` | — | ❌ timeout |
| `gemini/gemma-4-31b-it` | — | ❌ timeout |
| `gemini/gemini-3.1-pro-preview` | — | ❌ 503 |

**Rekomendasi:** `gemini/gemini-3.5-flash-lite` (gratis, stabil, <1 detik).

---

### 2. `cf` (Cloudflare AI) — 13 model, 10 OK
| Model | Latency | Status |
|-------|---------|--------|
| `cf/@cf/meta/llama-3.2-3b-instruct` | 383ms | ✅ OK (tercepat) |
| `cf/@cf/mistralai/mistral-small-3.1-24b-instruct` | 473ms | ✅ OK |
| `cf/@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | 590ms | ✅ OK |
| `cf/@cf/qwen/qwq-32b` | 595ms | ✅ OK |
| `cf/@cf/qwen/qwen2.5-coder-32b-instruct` | 791ms | ✅ OK |
| `cf/@cf/meta/llama-3.2-1b-instruct` | 857ms | ✅ OK |
| `cf/@cf/meta/llama-3.1-8b-instruct-fp8-fast` | 579ms | ✅ OK |
| `cf/@cf/meta/llama-3.1-70b-instruct-fp8-fast` | 830ms | ✅ OK |
| `cf/@cf/meta/llama-3.3-70b-instruct-fp8-fast` | 1651ms | ✅ OK |
| `cf/@cf/zai-org/glm-4.7-flash` | 9201ms | ✅ OK (lambat) |
| `cf/@cf/meta/llama-3.1-8b-instruct-awq` | — | ❌ 503 |
| `cf/@cf/moonshotai/kimi-k2.5` | — | ❌ 503 |
| `cf/@cf/moonshotai/kimi-k2.6` | — | ❌ 503 |

**Rekomendasi:** `cf/@cf/meta/llama-3.2-3b-instruct` (383ms, gratis, ringan) atau `cf/@cf/qwen/qwq-32b` (reasoning).

---

### 3. `kr` (Kiro) — 34 model, 9 OK dari sample 10
| Model | Latency | Status |
|-------|---------|--------|
| `kr/glm-5` | 1272ms | ✅ OK |
| `kr/glm-5-agentic` | 1088ms | ✅ OK |
| `kr/glm-5-thinking` | 1327ms | ✅ OK |
| `kr/auto` | 1456ms | ✅ OK |
| `kr/auto-thinking` | 2537ms | ✅ OK |
| `kr/deepseek-3.2` | 2639ms | ✅ OK |
| `kr/minimax-m2.1` | 3031ms | ✅ OK |
| `kr/glm-5-thinking-agentic` | 4044ms | ✅ OK |
| `kr/claude-sonnet-4` | 1667ms | ✅ OK |
| `kr/minimax-m2.5` | — | ❌ timeout |

**Rekomendasi:** `kr/glm-5` (gratis terbatas, <1.5 detik) atau `kr/claude-sonnet-4` (berbayar, 1.6 detik).

---

### 4. `gh` (GitHub Copilot) — 33 model, 5 OK dari sample 5
| Model | Latency | Status |
|-------|---------|--------|
| `gh/copilot-search-b` | 475ms | ✅ OK |
| `gh/copilot-search-c` | 527ms | ✅ OK |
| `gh/exec-agent-b` | 730ms | ✅ OK |
| `gh/copilot-search-a` | 1207ms | ✅ OK |
| `gh/exec-agent-a` | 868ms | ✅ OK |

**Catatan:** Semua model "search" dan "exec" OK. Model `mai-code-*` (400 not supported) TIDAK bisa. Gunakan search/exec agent.

---

### 5. `ollama` — 7 model, 1 OK
| Model | Latency | Status |
|-------|---------|--------|
| `ollama/gpt-oss:120b` | 1544ms | ✅ OK |
| `ollama/glm-5` | — | ❌ 410 retired |
| `ollama/kimi-k2.5` | — | ❌ 503 |

**Catatan:** `ollama/glm-5` sudah **retired** sejak 15 Juli 2026. Hanya `gpt-oss:120b` yang bisa.

---

### 6. `af` — 3 model, 1 OK
| Model | Latency | Status |
|-------|---------|--------|
| `af/gpt-oss-20b` | 1343ms | ✅ OK |
| `af/gpt-oss-120b` | — | ❌ 503 |

---

## 🔴 PROVIDER YANG TIDAK BISA DIPAKAI

| Provider | Total | Alasan |
|----------|-------|--------|
| **explabs** | 342 | `model_requires_purchase` / 429 — perlu beli kredit explabs. Termasuk gpt-5.4-mini, gemini-3.1-flash-lite, glm-5.3-flash. |
| **kimi** | 10 | `403 monthly usage limit` / quota exhausted. Bulan ini habis. |
| **nvidia** | 8 | `410 Gone / retired` — model sudah ditarik dari NIM. |
| **ag** | 20 | `timeout >25s` — OAuth gateway overload, tidak usable. |
| **bzl** | 24 | `402 insufficient credits` — Bazaarlink butuh top-up. |
| **bpm** | 7 | `503 generic` — upstream error. |
| **ps** | 2 | `503 generic` — upstream error. |

---

## 💡 REKOMENDASI

### Untuk Chat/Task Ringan (Gratis)
1. `gemini/gemini-3.5-flash-lite` — 694ms, gratis AI Studio
2. `cf/@cf/meta/llama-3.2-3b-instruct` — 383ms, gratis Cloudflare
3. `gh/copilot-search-b` — 475ms, gratis Copilot

### Untuk Reasoning/Coding (Gratis Terbatas)
1. `kr/glm-5` — 1272ms, free tier Kiro
2. `cf/@cf/qwen/qwq-32b` — 595ms, gratis Cloudflare

### Untuk Kualitas Tinggi (Berbayar)
1. `kr/claude-sonnet-4` — 1667ms, Kiro subscription
2. `gemini/gemini-3.8-flash` — 6025ms, AI Studio (lambat tapi gratis)

### Tidak Usai Dicoba
- Semua `explabs/*` — 342 model, semua 503 (perlu kredit explabs)
- Semua `ag/*` — timeout >25s (OAuth gateway overload)
- Semua `nvidia/*` — 410 retired
- Semua `kimi/*` — quota habis bulan ini

---

## ⚠️ CATATAN

1. **`explabs` adalah jumlah terbesar (342) tapi tidak ada yang bisa dipakai.** Model-model ini dulu gratis via free tier explabs, tapi sekarang di-lock dengan `model_requires_purchase`.
2. **`gh/mai-code-*` tidak tersedia** (400 model_not_supported), tapi search/exec agent OK.
3. **Total model "bisa" hanya ~31 dari 511.** Sisanya (480) tidak accessible.
4. **9router sendiri hidup** — bukan masalah router, tapi masalah kredit/quota di masing-masing provider upstream.
5. **Aksi:** Tidak perlu 9router-sync (ini bukan masalah URL, tapi kredit upstream).
