# Rencana Mapping Model Per-Thread — REVISI 2 (Maksimal + Fungsi Reels)

**Tanggal:** 21 Agustus 2026 · **Otoritas:** D-0004 — hanya OpenCode Zen `*-free` + Nous Portal `:free` (portal.nousresearch.com).
**Koreksi dari revisi 1:**
- Thread 1172 = **Kreator Konten Reels/Video** (bukan tulisan). Butuh model multimodal/long-context untuk script hook + analisis reference video.
- Mapping dipilih **maksimal per fungsi** dari kedua provider, tanpa bentrok (tiap thread dapat specialist terkuat yang available).

---

## Model Free-Tier Tersedia (sah)
**Zen `*-free`:** `nemotron-3-ultra-free` (ultra/flagship, multimodal), `hy3-free` (ringan/cepat), `big-pickle` (creative).
**Nous Portal `:free` (6):** `meituan/longcat-2.0:free` (long-context ~1M+, reasoning), `poolside/laguna-s-2.1:free` (coding specialist), `poolside/laguna-xs-2.1:free` (coding kecil), `stepfun/step-3.7-flash:free` (flash/cepat), `tencent/hy3:free` (general), `upstage/solar-pro4:free` (reasoning flagship).

> Catatan: TIDAK ada model `:free` yang khusus video-generation. "Maksimal untuk reels" = model multimodal/long-context terkuat untuk menulis script + menganalisis reference = `nemotron-3-ultra-free` (Zen ultra).

---

## Mapping Final (Maksimal per Fungsi)

| Thread | Fungsi | Model | Provider | Alasan Kapasitas Maksimal |
|--------|--------|-------|----------|----------------------------|
| **1** (General) | Router / orchestrator | `hy3-free` | opencode-zen | Ringan & cepat → ideal untuk routing (bukan heavy compute). Sisakan ultra untuk beban berat. |
| **802** (MC-Research) | Riset web, deep-dive | `meituan/longcat-2.0:free` | nous | LongCat = long-context terbesar (1M+ token) untuk ingest artikel/paper panjang + reasoning. |
| **803** (MC-Programmer) | Coding, review | `poolside/laguna-s-2.1:free` | nous | Poolside = lab coding; laguna-s adalah coding `:free` terbesar. |
| **804** (MC-QA) | Audit, testing | `upstage/solar-pro4:free` | nous | Solar Pro = reasoning flagship Upstage → audit/koreksi paling kuat di free-tier. |
| **1172** (Kreator Reels) | Video content | `nemotron-3-ultra-free` | opencode-zen | Ultra = model terbesar Zen, multimodal → script hook + analisis reference video (maksimal untuk reels di free-tier). |

**Distribusi:** Nous menyumbang 3 specialist (longcat/laguna/solar), Zen menyumbang ultra (video) + hy3 (router). Tiap thread dapat model terkuat untuk fungsinya, tidak ada yang seragam.

**Skill bindings tetap:** 803→ponytail+requesting-code-review, 804→codebase-audit, 1172→ghost+humanizer.

---

## Cara Terapkan (setelah zaryu setuju)
```bash
export HOME=/Users/zaryu
hermes config set platforms.telegram.channel_overrides '{
  "1":    {"model":"hy3-free","provider":"opencode-zen"},
  "802":  {"model":"meituan/longcat-2.0:free","provider":"nous"},
  "803":  {"model":"poolside/laguna-s-2.1:free","provider":"nous"},
  "804":  {"model":"upstage/solar-pro4:free","provider":"nous"},
  "1172": {"model":"nemotron-3-ultra-free","provider":"opencode-zen"}
}'
```
Verifikasi: `HERMES_HOME=/Users/zaryu/.hermes python3 scripts/telegram_threads.py`

---

## Catatan
- Semua `*-free` / `:free` → 100% patuh D-0004. Tidak ada OpenRouter/model asing.
- Nous `:free` bisa rotasi: jika model hilang, fallback auto ke `nemotron-3-ultra-free`.
- General (1) sengaja pakai `hy3-free` (ringan) agar `nemotron-3-ultra-free` (berat/multimodal) tersedia penuh untuk thread 1172 (reels). Jika Anda mau General juga pakai ultra, bisa disamakan — tidak masalah di Telegram (thread beda bisa model sama).

*Tidak dieksekusi sampai zaryu konfirmasi.*
