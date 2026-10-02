---
name: remotion-video
description: "Buat video vertikal 9:16 pakai Remotion — prompt ke MP4, Mode A CPU-only, gratis (Free tier ≤3 org). SCOPE: thread Konten Kreator (1172) saja."
version: 1.0.0
author: Niumination / Adaptasi remotion-dev/skills
license: MIT
metadata:
  hermes:
    tags: [Content, Video, Remotion, Vertical, Kreator]
    related_skills: [content-produce, content-script, content-studio]
    scope: "Thread Konten Kreator saja — bukan ekosistem luas"
    runtime: "sandbox/remotion-studio (di luar ekosistem utama)"
---

# Remotion Video — Konten Kreator

Buat video vertikal pendek (9:16, ≤30 detik) dari prompt teks, render via Remotion di CPU-only MacBook i5-10310U.

## When to Use

- `/video-vertical <prompt>` — prompt ke video 9:16 pendek
- "buat video teaser", "video intro 10 detik", "cover konten"
- Bila user minta motion graphic sederhana tanpa GPU

## Batasan Mode A (CPU-only, wajib ditaati)

| Parameter | Nilai | Alasan |
|-----------|-------|--------|
| Durasi | ≤ 30 detik (900 frame @30fps) | Render <5 menit di CPU ini |
| Resolusi | 1080×1920 (9:16 vertikal) | Format TikTok/Reels/Shorts |
| Efek | Tidak boleh: 3D, Partikel, Glow kompleks, Multi-layer | CPU UHD 620 tidak mampu |
| Concurrent | 1 render saja | RAM 16 GB marginal |

## Procedure

### A. Terima prompt

1. Baca `workspace/BRAND.md` + `project/<slug>/BRIEF.md` (jika ada).
2. Ekstrak: pesan inti, durasi target, platform tujuan, tone.
3. Tulis brief 3 baris di `project/<slug>/STATUS.md` sebelum nulis kode.

### B. Tulis komponen Remotion

1. Buat folder `project/<slug>/remotion/` dengan 3 file:
   - `Root.tsx` — registerRoot + Composition (1080×1920, fps=30, durasi sesuai brief)
   - `Video.tsx` — komponen utama (teks + CSS animation + GSAP jika perlu)
   - `package.json` — sudah ada di sandbox, cukup edit
2. Ikuti pola template (lihat `templates/formats/remotion-shorts.json`).
3. Gunakan `remotion-best-practices` skill (sudah terinstall) sebagai panduan.

### C. Render

```bash
cd ~/Desktop/Niumination/sandbox/remotion-studio
npx remotion render src/index.ts MyComp out/<slug>.mp4 -q 480
```

Bila durasi >30 detik atau kompleksitas tinggi → **hentikan**, tawarkan HyperFrames sebagai fallback.

### D. Verifikasi output

- `ffprobe out/<slug>.mp4` → durasi, rasio, fps, bitrate
- Loudness: `ffmpeg -i out/<slug>.mp4 -af loudnorm=print_format=json -f null -`
- Kapasitas file wajar (<50 MB untuk 30 detik 480p)

### E. Handoff

- MP4 → `project/<slug>/output/`
- Update `STATUS.md` → stage `4.QA`
- Lanjut ke `content-produce` caption/vertical_clip/sharing

## Pitfalls

- **Jangan render >30 detik di CPU ini** — waktu eksponensial naik
- **Jangan pakai efek GPU** (blur besar, shadow, gradient animasi berlebihan)
- **Jangan lupa `registerRoot`** — error umum entry point salah
- **Lisensi:** Free tier ≤3 org → jangan deploy >3 orang tanpa beli license
- **Chrome Headless:** first-run download 98 MB — one-time only
- **Komposisi salah:** ID composition harus cocok persis dengan argumen `render`

## References

- `references/agent-skills-catalog.md` — 12 Remotion Agent Skills catalog, which are relevant for Konten Kreator workflow

## Verification

- `out/<slug>.mp4` ada + ffprobe valid
- Durasi ≤30 detik, rasio 9:16 (1080×1920)
- Render time tercatat di `STATUS.md`
- Lisensi Free tier masih sesuai (≤3 org)
