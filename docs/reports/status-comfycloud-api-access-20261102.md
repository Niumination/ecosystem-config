# Status: ComfyCloud & LTX API Access
**Tanggal:** 2026-11-02  
**Subjek:** Kendala akses ComfyCloud API + alternatif viable untuk LTX 2.5

---

## 1. ComfyCloud — API Tidak Bisa Dipakai (Free Tier)

**Status key:** Valid, akun aktif (`oJaJlSfSCmM8CbZ6MhwxhuPVduv1`)  
**Hambatan:** API endpoint menolak dengan `FREE_TIER_NOT_ALLOWED`

**Penyebab:** ComfyCloud memisahkan fitur berdasarkan tier:
- **Free tier:** 5 free runs manual di web UI, **TIDAK ada API access**
- **Standard ($16/bulan tahunan / $20/bln):** API access + ~4.4 jam generation/bln
- **Creator ($28/bulan tahunan):** API + import model sendiri + 3 concurrent
- **Pro ($80/bulan tahunan):** API + 1 jam max runtime + 5 concurrent

**Kesimpulan:** Key sudah benar, tapi perlu upgrade ke Standard minimum untuk pakai API workflow.

**Keputusan:** Jangan upgrade ComfyCloud dulu. Terlalu mahal untuk pilot awal.

---

## 2. Alternatif Viable — Urutan Rekomendasi

### Opsi A: LTX API Langsung (Paling Direkomendasikan)
- **Get key:** https://console.ltx.io → sign up → API Keys → Create
- **Biaya:** Pay-per-second, tanpa subscription
  - Fast: $0.09/s (720p) → 2s video = **$0.18**
  - Pro: $0.12/s (720p) → 2s video = **$0.24**
- **New account:** Dapat free trial credit (cukup untuk ~15-20 video pilot)
- **Endpoint:** `POST https://api.ltx.io/v1/text-to-video`
- **Auth:** `Authorization: Bearer YOUR_API_KEY`
- **Req body:**
  ```json
  {"prompt": "...", "model": "ltx-2-5-fast", "duration": 2, "resolution": "1280x720"}
  ```
- **Response:** MP4 langsung di body
- **Kelebihan:** Simple, murah untuk volume kecil, langsung usable
- **Kekurangan:** Tidak bisa mix dengan node ComfyUI lain

### Opsi B: HuggingFace Spaces (Gratis, Tapi Lambat)
- **Official:** https://huggingface.co/spaces/Lightricks/LTX-2.5
- **Alternatif:** https://huggingface.co/spaces/firstlight/ltx-2-5-demo
- **Biaya:** Gratis, tapi antrian ZeroGPU bisa panjang (menit hingga jam)
- **Cocok untuk:** Eksperimen sekali-sekali, bukan produksi

### Opsi C: ComfyCloud Upgrade (Jika Butuh Workflow Kompleks)
- Hanya jika perlu mix LTX dengan node lain (ControlNet, upscale, dll)
- Minimum Standard $16/bulan (billed yearly)
- Belum disarankan untuk fase pilot

---

## 3. Rekomendasi Next Step

1. **Ambil LTX API key** di https://console.ltx.io (Gratis trial credit)
2. **Test 3-5 clip** via curl/API untuk verify quality
3. **Jika cocok** → integrasikan ke pipeline Kreator via script Python sederhana
4. **Simpan key** di `~/.hermes/.env` → `LTX_API_KEY=...`

---

## 4. File yang Sudah Siap

- `skills/creative/comfyui/workflows/ltx25_t2v.json` — workflow manual (untuk nanti kalau upgrade ComfyCloud)
- `skills/creative/comfyui/workflows/README.md` — sudah terupdate
- `.hermes/skills/content/content-produce/SKILL.md` — B-roll row sudah pakai LTX 2.5
- `apps/abstract-studio/data/TOOL_DECISIONS.csv` — LTX 2.5 DITERIMA
- `~/.hermes/.env` — COMFY_CLOUD_API_KEY sudah terpasang (tapi belum bisa dipakai karena free tier)

---

## Bukti
- `curl /api/user` → 200, akun active
- `curl /api/prompt` → 403 `FREE_TIER_NOT_ALLOWED`
- `curl /api/queue` → 200 (free tier bisa queue, tapi tidak bisa submit prompt)
- `curl /api/experiment/models/diffusion_models` → 200, LTX 2.5 models tersedia (17 model)
- `curl /api/object_info/LtxApi25TextToVideo` → node tersedia tapi tidak bisa diakses free tier
- `curl lightricks-ltx-2-5.hf.space` → 200, tapi antrian panjang
