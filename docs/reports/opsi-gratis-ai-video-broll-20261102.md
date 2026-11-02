# Opsi Gratis AI Video Generation untuk B-roll Kreator
**Tanggal:** 2026-11-02  
**Konteks:** LTX 2.5 API butuh kredit ($5 min), ComfyCloud free tier blokir API. Cari alternatif gratis.

---

## 1. HuggingFace Spaces (LTX-2.5) — GRATIS, Tapi Tidak Reliabel

**Space:** https://huggingface.co/spaces/Lightricks/LTX-2.5  
**Alternatif:** https://huggingface.co/spaces/firstlight/ltx-2-5-demo

- **Biaya:** Gratis (ZeroGPU shared)
- **Syarat:** Tidak perlu akun/kartu kredit
- **Kendala:**
  - Antrian ZeroGPU panjang (bisa menit sampai jam)
  - Daily quota terbatas per IP/account
  - Space sering error/offline (diverifikasi: firstlight space 503, official space 404 di queue API)
  - Tidak ada API — harus pakai browser manual
- **Cocok untuk:** Eksperimen sekali-sekali, bukan produksi

**Verdict:** ❌ Tidak reliable untuk pipeline otomatis. Hanya untuk trial manual.

---

## 2. NovAI — CogVideoX Flash (FREE Forever)

**Platform:** https://aiapi-pro.com  
**Model:** CogVideoX Flash (Zhipu AI)  
**Biaya:** $0 — gratis selamanya untuk prototyping

**Yang didapat gratis:**
- **5 video + 20 gambar per hari** via AI Studio web
- **API key gratis** — no credit card, no subscription
- Async task API: submit → poll → download (sama pola dengan LTX)
- Preview watermarked, download unlock setelah top-up $5

**API shape:**
```bash
curl -X POST https://aiapi-pro.com/v1/video/generations \
  -H "Authorization: Bearer YOUR_NOVAI_KEY" \
  -d '{"model":"cogvideox-flash","prompt":"a cat walking on neon streets"}'
# → {"id":"task_...","status":"queued"}
```

**Limitasi:**
- Kualitas lebih rendah dari LTX 2.5 (model lama, 2-5s clip)
- Watermark di preview gratis
- Max 5 video/hari — terbatas untuk produksi
- Upgrade ke model premium: Seedance 2.0 ($0.13/s), Seedance 2.5 ($0.14/s)

**Verdict:** ⚠️ Bagus untuk prototyping, tapi quality kurang untuk B-roll profesional. Cocok kalau cuma butuh konsep/preview.

---

## 3. Magic Hour — Free Signup Credits

**Platform:** https://magichour.ai  
**Biaya:** Free 400 credits saat signup (no card required)

**Yang didapat gratis:**
- **400 signup credits** — cukup untuk beberapa video test
- **Daily credits:** Basic account dapat 100 credits/hari (max 7x claim = 700 credits lifetime)
- Multiple models: video generation, image, audio
- API access tersedia
- Credits never expire (roll over forever)

**Pricing:** $1 = 400 credits. Video generation harga bervariasi per model.

**Verdict:** ⚠️ Bisa untuk pilot awal (beberapa clip test), tapi tidak long-term free.

---

## 4. LTX API Direct — Pay Per Second (Bukan Gratis Tapi Murah)

**Platform:** https://console.ltx.io  
**Biaya:** $0.09/detik (720p fast)

**Kelebihan:**
- Quality terbaik di class-nya (LTX 2.5)
- Multi-shot, native audio, 4K
- Tidak perlu subscription — bayar per detik
- Min top-up hanya $5
- New account dapat free trial credit

**Simulasi biaya pilot 10 clip (4s @ 720p fast):**
- 10 × 4s × $0.09 = **$3.60**
- Di bawah minimum top-up $5

**Verdict:** ✅ **Opsi terbaik** kalau mau quality LTX 2.5. Biaya minim untuk pilot.

---

## 5. ComfyCloud — Perlu Upgrade Paid Plan

**Status saat ini:** Free tier = 5 runs manual, **nol API access**  
**Upgrade ke Standard:** $16/bulan (billed yearly) = API access + ~4.4 jam generation

**Verdict:** ❌ Terlalu mahal untuk pilot. Hanya perlu jika butuh workflow kompleks (mix LTX + ControlNet + upscale).

---

## 6. Opsi Lain yang Belum Diuji

| Platform | Model | Gratis? | Catatan |
|---|---|---|---|
| fal.ai | LTX 2.3/2.5 | Trial credits | Perlu daftar, free credits case-by-case |
| Replicate | LTX 2.5 | Pay-per-run | Ada free trial, tapi bukan free forever |
| Runway | Gen-4 | Paid only | Tidak ada free tier untuk API |
| Kling AI | K2.5 | Limited free | Web-only, tidak ada API publik |
| Veo 3.1 (Google) | Via Gemini API | Paid only | $0.40/s — terlalu mahal |

---

## Rekomendasi

**Untuk pilot B-roll LTX 2.5:**
1. **Top-up $5 LTX API** → dapat ~55 detik video 720p fast (~13 clip 4 detik)
2. **Test 3-5 clip** via API, eval quality
3. Kalau quality cocok → lanjut LTX API untuk produksi
4. Kalau quality kurang → coba Magic Hour free credits untuk bandingkan

**Untuk prototyping gratis (bukan LTX):**
1. Daftar NovAI → dapat API key gratis
2. Generate 5 clip/hari via CogVideoX Flash
3. Gunakan untuk validasi prompt/wireframe, bukan output final

**Yang TIDAK recommend:**
- HuggingFace Spaces — unreliable, tidak bisa di automate
- ComfyCloud free tier — API blocked
- LTX API tanpa top-up — insufficient funds

---

## Bukti
- LTX API V1 retired 26 Okt 2026 → perlu V2
- LTX API key valid tapi balance $0 → `insufficient_funds_error: Required 36 cents`
- ComfyCloud API → `FREE_TIER_NOT_ALLOWED` (403)
- HuggingFace LTX spaces → 503/error (firstlight), queue API 404 (official)
- NovAI → 200 OK, free tier documented (5 video/day)
- Magic Hour → 400 signup credits, no card required
