# AI Video Generation Providers

Panduan memilih provider text-to-video untuk B-roll generatif di Kreator pipeline.

## Ringkasan Provider

| Provider | Gratis? | Rate | Kualitas | Status di mesin ini |
|---|---|---|---|---|
| **NovAI** (cogvideox-flash) | 5 clip/hari | $0 | 720p, ada watermark gratisan | ✅ Kunci ada, upstream sering busy |
| **fal.ai** (MiniMax H3 Max) | 5x/hari via sandbox | $0.08/s API | 768p, audio native | ⚠️ Key ter-lock TOP_UP, perlu top-up $1 |
| **HuggingFace Inference** | Gratis (token) | $0 | Bervariasi | ❌ DNS tidak resolve dari mesin ini |
| **LTX API** (ltx.io) | Tidak | $0.09/s | 720p/1080p | ⚠️ Perlu top-up minimal $5 |
| **ComfyCloud** | 5 runs manual | API blocked free tier | — | ❌ FREE_TIER_NOT_ALLOWED |

## NovAI (Primary Recommendation)

**Endpoint:** `https://aiapi-pro.com/v1/video/generations`
**Model gratis:** `cogvideox-flash` (Zhipu AI)
**Limit:** 5 video/hari, 10 model calls/hari, 5 requests/menit
**Key env:** `NOVAI_API_KEY`

**Cara pakai:**
```bash
# Submit job
python3 apps/abstract-studio/scripts/ai_video.py "a drone shot over rice terraces" \
  --provider novai --model cogvideox-flash --duration 5

# Atau via script langsung
export AI_VIDEO_PROVIDER=novai
python3 apps/abstract-studio/scripts/ai_video.py "prompt here"
```

**Catatan:** Watermark di output gratisan. Tanpa top-up akun, hanya dapat preview watermark.

## fal.ai

**Endpoint:** `https://fal.run/fal/minimax/h3-max/text-to-video`
**Model:** `minimax/h3-max/text-to-video`
**Limit:** 5 free/day via sandbox UI, API perlu key + top-up
**Key env:** `FAL_KEY` (format `uid:key`)

**Catatan:** Key saat ini ter-lock `TOP_UP`. Butuh minimal $1 di https://fal.ai/dashboard/billing.

## HuggingFace Inference

**Status:** DNS `api-inference.huggingface.co` tidak resolve dari mesin ini.
**Alternatif:** Gunakan HF token + SDK `huggingface_hub` bila DNS memperbaiki.

## Workflow Integrasi

Script `ai_video.py` sudah terpasang di `apps/abstract-studio/scripts/`.
Untuk gunakan di Kreator thread 1172:

```bash
# Set provider via env atau argumen
AI_VIDEO_PROVIDER=novai python3 scripts/ai_video.py "prompt" --output project/output/video.mp4
```

Output akan tersimpan di path yang ditentukan, siap untuk mux dengan VO dan caption.
