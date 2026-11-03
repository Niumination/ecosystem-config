# Test NovAI CogVideoX Flash — Hasil Lengkap
**Tanggal:** 2026-11-02  
**Key:** `nvai-e2a8...2742` (dari Downloads/NovAI-api.md)  
**Model:** cogvideox-flash (Zhipu AI)  
**Status:** BERFUNGSI ✅ — dengan limitasi free tier

---

## 1. Verifikasi API Key

- Key valid ✅
- Model catalog tersedia: 5 free models + 20+ paid models
- Balance: trial credit $2 (tidak bisa dipakai untuk video models)

## 2. Test Generate — SUKSES

**Request:**
```bash
curl -X POST https://aiapi-pro.com/v1/video/generations \
  -H "Authorization: Bearer $NOVAI_KEY" \
  -d '{"model":"cogvideox-flash","prompt":"A cinematic drone shot over turquoise ocean waves at golden hour","duration":5}'
```

**Response:** `{"id":"202611021437443894f997e40f484f","status":"queued",...}`

**Video properties:**
- Resolusi: **1792×1024** (≈16:9, HD)
- Durasi: **5.1 detik**
- FPS: 37
- Codec: H.264
- Ukuran: **2.5 MB**
- URL: ada watermark di filename (`_watermark.mp4`)

## 3. Limitasi Free Tier

| Limit | Nilai |
|---|---|
| Free video calls/hari | **5 clip** |
| Free model calls/hari (total) | 10 calls |
| Rate limit | 5 requests/menit |
| Reset | 00:00 UTC+8 |
| Watermark | ✅ Ada di preview gratis |
| Concurrency | Shared ZeroGPU — sering "busy" (429) |

**Status setelah 1 generate:** Sisa 4 clip/hari. Error 429 "upstream concurrency cap" = GPU free tier sedang penuh.

## 4. Model Lain Tersedia (Berbayar)

| Model | Vendor | Catatan |
|---|---|---|
| doubao-seedance-2.0-fast | ByteDance | $0.131/s, perlu top-up |
| minimax-video-h3 | MiniMax | High quality |
| kling-video-v3 | NovAI | Chinese model |
| pixverse-video-v6.0 | PixVerse | |

Trial credit ($2) **tidak bisa** dipakai untuk video models — hanya untuk chat/vision models gratis.

## 5. Penggunaan di Pipeline Kreator

**Workflow yang bisa dibangun:**
1. Agent tulis prompt → call NovAI API → poll result → download MP4
2. Simpan ke `project/<slug>/output/`
3. Gabung dengan VO (Gemini TTS Charon) + caption via FFmpeg

**Contoh script Python:**
```python
import os, time, requests

KEY = os.getenv("NOVAI_API_KEY")
URL = "https://aiapi-pro.com/v1/video/generations"

def generate_video(prompt, duration=5, model="cogvideox-flash"):
    r = requests.post(URL, headers={"Authorization": f"Bearer {KEY}"},
                      json={"model": model, "prompt": prompt, "duration": duration})
    job = r.json()
    # Poll until succeeded
    while job.get("task_status") != "SUCCESS":
        time.sleep(10)
        r2 = requests.get(f"{URL}/{job['id']}?model={model}",
                          headers={"Authorization": f"Bearer {KEY)"})
        job = r2.json()
    return job["video_result"][0]["url"]
```

**Catatan penting:**
- Output free tier ada **watermark** — tidak cocok untuk konten publik final
- Untuk output tanpa watermark, perlu top-up minimal (harga belum terungkap di free tier)
- Quality CogVideoX Flash **di bawah LTX 2.5** — lebih cocok untuk storyboard/preview

---

## Kesimpulan

| Kriteria | NovAI (CogVideoX Flash) | LTX API |
|---|---|---|
| Biaya | Gratis (5 clip/hari) | $0.09/detik (min $5 top-up) |
| Quality | Standar (Flash tier) | Tinggi (22B model) |
| Watermark | Ada | Tidak |
| Reliabilitas | Sering 429 (concurrency) | Stabil |
| Cocok untuk | Prototyping, storyboard | Production B-roll |

**Rekomendasi:** Gunakan NovAI untuk **validasi prompt & storyboard** (gratis). Untuk **output final**, top-up LTX API $5 atau tunggu ComfyCloud upgrade.

---

## Bukti
- `POST /v1/video/generations` → 200, job ID `202611021437443894f997e40f484f`
- `GET /v1/video/generations/{id}` → `task_status: SUCCESS`, video_url ada
- Video downloaded: 2.5MB, 1792×1024, 5.1s, H.264
- Retry → 429 `upstream concurrency cap` (free tier shared GPU busy)
- Paid model (seedance) → 403 `Trial credit cannot be used for video models`
- Daily limit: 5 video/day, 10 total calls/day, reset 00:00 UTC+8
