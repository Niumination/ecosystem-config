# Audit Model & Provider — Niumination Hermes

| Field | Nilai |
|---|---|
| **Tanggal** | 18 Agustus 2026 (WIB) |
| **Metode** | Probe langsung: GET /v1/models + chat completion + tool-calling test per provider |
| **Status** | Referensi — BELUM diterapkan ke config |

---

## Ringkasan

5 provider hidup (HTTP 200), 2 mati (401), 1 tidak aktif. Temuan kritis: **primary `big-pickle` & `deepseek-v4-flash-free` sedang 429 (kuota free habis)** — ini akar "kinerja model buruk".

## Hasil Probe Provider

| Provider | /v1/models | Chat | Tool-call | Verdict |
|---|---|---|---|---|
| opencode-zen | ✅ 200 (62 model) | ⚠️ sebagian 429 | ✅ | Primary — kuota free habis |
| 9router (lokal) | ✅ 200 (39 model) | ✅ | ✅ cepat | Layak fallback |
| nvidia_nim | ✅ 200 (102 model) | ✅ | ✅ 0.7s | Layak cadangan |
| openrouter | ✅ 200 (412 model) | ⚠️ 15 free, sebagian 429 | ✅ | Layak, terbatas |
| huancheng | ✅ 200 (20 model) | ❌ timeout semua | ❌ | TIDAK layak sekarang |
| juan-router | ❌ 401 | — | — | Key ditolak |
| agentrouter | ❌ 401 | — | — | Key ditolak |
| aerolink | key ada, URL tidak di config | — | — | Tidak aktif |

## Temuan KRITIS

`big-pickle` & `deepseek-v4-flash-free` = HTTP 429 (FreeUsageLimitError) — kuota free habis. Hermes primary sedang mati, fallback `juan-router` 401 menambah masalah.

## Rekomendasi Model

### Tier 1 — Utama (keluarga Zen)

| Model | Latency | Tool-call | Status |
|---|---|---|---|
| big-pickle | — | ✅ | ❌ 429 — tunggu reset |
| deepseek-v4-flash-free | — | ✅ | ❌ 429 |
| **hy3-free** | 3.6s | ✅ args valid | ✅ HIDUP |
| **laguna-s-2.1-free** | 3.6s | ✅ args valid | ✅ HIDUP |
| nemotron-3-ultra-free | 17s | ✅ | ✅ Hidup, lambat |

### Tier 2 — Fallback (infrastruktur)

| Model | Latency | Tool-call | Catatan |
|---|---|---|---|
| gemini/gemini-3.7-flash (9router) | 1.1s | ✅ args valid | Tercepat |
| gratislonggar (9router) | 9.2s | ✅ args valid | Resolve ke gemini-3.6 |
| meta/llama-3.1-8b-instruct (NVIDIA) | 0.7s | ✅ args valid | Sangat cepat, 8B |
| openai/gpt-oss-20b:free (OpenRouter) | 12.2s | ✅ | JSON mode ❌ |

### Tidak layak

- juan-router, agentrouter — key 401
- huancheng/* — inference timeout semua
- openrouter non-free — key tanpa kredit (402)
- deepseek-v4-flash (Zen) — butuh payment (401 CreditsError)

## Saran Konfigurasi (belum diterapkan)

```yaml
model: opencode-zen / big-pickle   # primary tetap

fallback_providers:
  - opencode-zen / hy3-free            # keluarga SAMA, hidup sekarang
  - opencode-zen / laguna-s-2.1-free   # cadangan kedua keluarga sama
  - 9router / gemini/gemini-3.7-flash  # setelah probe 200
```

---

*Audit dilakukan 2026-08-18 dengan test langsung (bukan estimasi).*