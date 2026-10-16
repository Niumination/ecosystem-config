# 📋 Rencana Solusi: Model dengan Limit Longgar untuk 9router
**Date:** 31 Ags 2026
**Status:** Plan — Menunggu approval sebelum eksekusi

---

## 🎯 Tujuan

Membuat fallback chain yang optimal menggunakan model dengan limit truly longgar, menghindari masalah quota habis (HTTP 429) dan shared Google quota.

---

## 📊 Analisis Kuota Backend

| Backend | Model Prefix | Konteks | Status | Catatan |
|---------|-------------|---------|--------|---------|
| **Google AI** | `ag/gemini-*` | 1M tokens | ❌ Problem | Semua share quota Google yang sama → 429 semua |
| **Google AI (native)** | `gemini/*` | 1M tokens | ⚠️ Berbeda | Native Gemini, quota terpisah dari Antigravity |
| **GitHub Models** | `gh/*` | 128K–1M tokens | ✅ Terpisah | Quota GitHub, tidak terkait Google |
| **Kimi** | `kr/*` | Varies | ✅ Terpisah | Quota Kimi, benar-benar terpisah |
| **Open Source** | `ag/gpt-oss-*` | 128K tokens | ✅ Terpisah | Lokal, tanpa API |

---

## 🏆 Top Model Longgar per Kategori

### 1️⃣ GH (GitHub Models) — Quota Terpisah dari Google

| Model | Konteks | Max Output | Vision | Tools | Search | Reasoning | Status |
|-------|---------|------------|--------|-------|--------|-----------|--------|
| **gh/gpt-4.1-2025-04-14** | **1M** | 32K | ✅ | ✅ | ❌ | ❌ | 🏆 **POWERFUL** |
| **gh/gpt-4.1** | **1M** | 32K | ✅ | ✅ | ❌ | ❌ | 🏆 **POWERFUL** |
| gh/gpt-5.4-mini-free-auto | 400K | 128K | ✅ | ✅ | ✅ | ✅ | ✅ **FREE** |
| gh/gpt-5.6-luna | 400K | 128K | ✅ | ✅ | ✅ | ✅ | 💰 |
| gh/gpt-5-mini | 400K | 128K | ✅ | ✅ | ✅ | ✅ | 💰 |
| gh/gpt-4o-mini | 128K | 16K | ✅ | ✅ | ✅ | ❌ | 💰 Murah |
| gh/claude-haiku-4.5 | 200K | 64K | ✅ | ✅ | ✅ | ✅ | 💰 |

### 2️⃣ Native Gemini — Quota Terpisah dari Antigravity

| Model | Konteks | Max Output | Vision | Tools | Search | Reasoning | Status |
|-------|---------|------------|--------|-------|--------|-----------|--------|
| **gemini/gemini-3.7-flash** | **1M** | 65K | ✅ | ✅ | ✅ | ✅ | 🏆 **TERCEPAT** |
| gemini/gemini-3.6-flash | 1M | 65K | ✅ | ✅ | ✅ | ✅ | ✅ |
| gemini/gemini-3.5-flash-lite | 1M | 65K | ✅ | ✅ | ✅ | ✅ | ✅ |
| gemini/gemini-3.1-pro-preview | 1M | 65K | ✅ | ✅ | ✅ | ✅ | 💰 |
| gemini/gemini-3.1-flash-lite-preview | 1M | 65K | ✅ | ✅ | ✅ | ✅ | ✅ |

### 3️⃣ KR (Kimi) — Quota Terpisah Penuh

| Model | Konteks | Catatan | Status |
|-------|---------|---------|--------|
| **kr/minimax-m2.5** | 200K | MiniMax model | ✅ |
| **kr/qwen3-coder-next** | — | Code-focused | ✅ |
| **kr/glm-5** | — | GLM-5 | ✅ |
| **kr/deepseek-3.2** | — | DeepSeek | ✅ |
| kr/claude-haiku-4.5 | — | Claude via Kimi | ✅ |
| kr/claude-sonnet-4.5 | — | Claude via Kimi | ✅ |
| kr/claude-opus-4.5/4.7/4.8/5 | — | Claude via Kimi | 💰 |
| kr/gpt-5.6-luna/sol/terra | — | GPT via Kimi | 💰 |

### 4️⃣ AG Non-Gemini (Open Source / Claude)

| Model | Konteks | Catatan | Status |
|-------|---------|---------|--------|
| **ag/claude-sonnet-4-6** | **1M** | Claude via AG | 💰 |
| ag/claude-opus-4-6-thinking | 200K | Claude via AG | 💰 |
| ag/gpt-oss-120b-medium | 128K | Open source lokal | ✅ |

---

## 🎯 Fallback Chain Rekomendasi

### Prinsip
1. **1 powerful model** sebagai primary fallback
2. **Sisanya dari provider berbeda** (GH, Gemini native, KR, Open Source)
3. **Tidak ada dua model dari backend yang sama**
4. **Semua model punya konteks besar** (≥128K)

### Rantai Fallback (11 model)

| Priority | Model | Provider | Konteks | Kuota | Alasan |
|----------|-------|----------|---------|-------|--------|
| **1** | `gh/gpt-5.4-mini-free-auto` | GH | 400K | ✅ FREE | FREE, 400K ctx, tools+search+reasoning |
| **2** | `gemini/gemini-3.7-flash` | Native Gemini | 1M | Terpisah | 🏆 Fastest + 1M context |
| **3** | `gh/gpt-4.1-2025-04-14` | GH | 1M | Terpisah | 🏆 Most powerful (1M ctx) |
| **4** | `kr/minimax-m2.5` | Kimi | 200K | Terpisah | Kimi, benar-benar terisolasi |
| **5** | `kr/qwen3-coder-next` | Kimi | — | Terpisah | Code-focused |
| **6** | `gh/claude-haiku-4.5` | GH | 200K | Terpisah | Claude via GH |
| **7** | `ag/claude-sonnet-4-6` | AG (Claude) | 1M | Terpisah | AG Claude, 1M ctx |
| **8** | `gemini/gemini-3.6-flash` | Native Gemini | 1M | Terpisah | Backup Gemini |
| **9** | `gh/gpt-5-mini` | GH | 400K | Terpisah | GH backup |
| **10** | `ag/gpt-oss-120b-medium` | Open Source | 128K | Lokal | Open source, no API |
| **11** | `kr/deepseek-3.2` | Kimi | — | Terpisah | DeepSeek via Kimi |

### Backend Distribution
| Backend | Count | Models |
|---------|-------|--------|
| GitHub Models | 5 | gh/gpt-5.4-mini-free-auto, gh/gpt-4.1, gh/claude-haiku-4.5, gh/gpt-5-mini, gh/gpt-4o-mini |
| Native Gemini | 2 | gemini/gemini-3.7-flash, gemini/gemini-3.6-flash |
| Kimi | 3 | kr/minimax-m2.5, kr/qwen3-coder-next, kr/deepseek-3.2 |
| AG (Claude) | 1 | ag/claude-sonnet-4-6 |
| Open Source | 1 | ag/gpt-oss-120b-medium |

**Zero models share the same quota backend!** ✅

---

## 📝 Plan Eksekusi

### Phase 1: Survey + Analisis (✅ Selesai)
- [x] Survey semua 89 model 9router
- [x] Filter model dengan konteks ≥128K
- [x] Kategorikan berdasarkan quota backend
- [x] Identifikasi model longgar dari masing-masing provider

### Phase 2: Buat Config Baru (Menunggu Approval)
- [ ] Update `fallback_providers` di `~/.hermes/config.yaml`
- [ ] Update channel overrides jika perlu
- [ ] Backup config lama

### Phase 3: Test (Menunggu Approval)
- [ ] Test setiap model di fallback chain
- [ ] Verify HTTP 200 untuk semua model
- [ ] Check latency dan kualitas response
- [ ] Test rate limit handling

### Phase 4: Update Dokumentasi (Menunggu Approval)
- [ ] Update `~/.hermes/9router-models-status.md`
- [ ] Update `~/.hermes/9ROUTER-FREE-MODELS-2026-08-31.md`
- [ ] Update `docs/reference/model-mapping.md`
- [ ] Update AGENTS.md jika perlu

### Phase 5: Monitor (Ongoing)
- [ ] Monitor error logs selama 1 minggu
- [ ] Cek quota usage per model
- [ ] Adjust jika diperlukan

---

## ⚠️ Catatan Penting

1. **Native Gemini (`gemini/*`)** vs **Antigravity (`ag/gemini-*`)** — berbeda quota backend
2. **GH models** menggunakan quota GitHub Models (terpisah dari Google)
3. **KR models** menggunakan quota Kimi (terpisah dari kedua-duanya)
4. **gh/gpt-5.4-mini-free-auto** dan **gh/gpt-5.6-luna-free-auto** = FREE tier
5. **ag/claude-sonnet-4-6** = 1M konteks via Antigravity (Claude, bukan Gemini)
6. **ag/gpt-oss-120b-medium** = open source lokal (tanpa API call)

---

## 🔄 Rollback Plan

Jika config baru bermasalah:
```bash
# Restore config lama
cp ~/.hermes/config.yaml.bak ~/.hermes/config.yaml

# Restart services
launchctl stop com.niumination.missioncontrol
launchctl start com.niumination.missioncontrol
```

---

## 📄 Referensi

- Full model catalog: `/tmp/9router_models.json`
- Error analysis: `~/.hermes/OPENCODE-ZEN-ERROR-ANALYSIS-2026-08-31.md`
- Free models report: `~/.hermes/9ROUTER-FREE-MODELS-2026-08-31.md`
- Current config: `~/.hermes/config.yaml`

---

**Plan siap dijalankan setelah approval. Siapapun yang menyetujui, eksekusi dimulai dari Phase 2.**

⚡ (◕‿◕)★
