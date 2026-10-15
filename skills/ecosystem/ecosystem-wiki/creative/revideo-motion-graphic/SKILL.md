---
name: revideo-motion-graphic
category: creative
description: "ARSIF — jalur motion-graphic Revideo ini DITOLAK (macet 7,4 jam, 0 output, 23 Sep 2026). BACA DULU banner penolakan di atas. Pakai HyperFrames atau Remotion."
version: 1.0.0
---

# Revideo Motion Graphic (Short Vertikal, tanpa GPU)

> ## ⛔ JALUR INI DITOLAK — jangan pakai (putusan 23 Sep 2026)
>
> Revideo **tidak dipakai** di studio ini setelah gagal nyata:
> `npx revideo render` macet **7 jam 4 menit** dan **tidak menulis file apa pun**.
> Catatan skill yang dulu menyertai kegagalan itu — "render langsung jalan, ~1
> menit, tanpa install berat" — tidak benar; kegagalan justru berasal dari
> install-nya. Tercatat di `apps/abstract-studio/data/TOOL_DECISIONS.csv`
> (entri `REVIDEO-2D`, status `TIDAK DIPAKAI`).
>
> **Pakai HyperFrames** untuk komposisi HTML (skill `hyperframes`, pin
> `0.8.30`) atau **Remotion** untuk React (skill `remotion-video`).
> Jalur paling sederhana bila hanya gerakan zoom/pan: skill
> `ffmpeg-ken-burns-motion`.
>
> **Koreksi:** kalimat asli dokumen ini menulis "VO bahasa Indonesia **Piper**
> — pola yang terbukti di reels-003". Keduanya salah. Reels-003 membuktikan
> **HyperFrames + Gemini TTS Charon**, bukan Revideo + Piper. Piper sudah
> ditolak sebelum reels-003 v1 dibuat (ukur LRA 2,30 flat vs target 4,50).
> Dokumen ini ditulis **sebelum** kedua penolakan itu terjadi dan tidak pernah
> dikembalikan ke belakang.
>
> Isi di bawah ini dipertahankan sebagai arsip dokumentasi, karena
> `revideo render` memang tidak ada di CLI 0.11 — itu fakta yang masih relevan
> bila ada yang tetap mencoba. BUKAN rekomendasi.

Jalur produksi short vertikal berkualitas MENENGAH-ATAS tanpa GPU: komposisi motion graphic **Revideo 2D** (bukan card statis), VO bahasa Indonesia **Piper** (legal komersial), mux via **FFmpeg** — pola yang terbukti di reels-003.

## Kapan pakai

- User minta video reels/short vertikal dengan animasi & gerakan, bukan slide statis
- Butuh VO bahasa Indonesia gratis untuk konten berbayar (Piper = legal; JANGAN edge-tts untuk berbayar)
- Render komposisi animasi headless tanpa GPU

## Alur (urutan WAJIB)

### 1. Baca BRAND.md + skill content-produce TERLEBIH DAHULU
Kegagalan paling mahal: produksi BUKAN pakai brand (font/warna/motion salah) karena skip baca. `content-produce` A.1 mewajibkan baca `BRAND.md` + `NASKAH.md` + `SHOTLIST.csv`. Font = Inter + JetBrains Mono; warna brand; motion graphic wajib.

### 2. Install stack
```bash
npm init -y
npm install @revideo/2d @revideo/core
npm install -D @revideo/cli
npm install @revideo/renderer @revideo/ui
npx puppeteer browsers install chrome   # sekali, ~380M; wajib untuk headless render
```

### 3. VO Piper (bahasa Indonesia, legal komersial)
- Download voice id_ID: `https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium/id_ID-news_tts-medium.onnx` (+ `.onnx.json`)
- Generate: `piper -m <model> -f vo_raw.wav < naskah.txt`
- Bersihkan: `ffmpeg -i vo_raw.wav -af "highpass=f=80,lowpass=f=11000,loudnorm=I=-16:TP=-1.5" vo_clean.wav`
- Fonetiskan istilah teknis ID sesuai `brand/voice/pronunciation-id.csv` (API → "ei pi ai", .env → "dot en vi")
- Transkrip verifikasi otomatis TIDAK wajib; catat UNCHECKED + alasan bila tool tidak ada

### 4. Komposisi Revideo
- **File scene = `.tsx`, BUKAN `.ts`** — JSX tidak diparse di .ts (error rolldown/vite)
- API 0.11: `makeProject({scenes, settings:{shared:{size:{x,y}, background}, rendering:{fps, resolutionScale}}})` dari `@revideo/core`; scene = `makeScene2D('nama', function* (view){...})` dari `@revideo/2d`
- Komponen: `Txt`, `Rect`, `Circle`; refs via `createRef<T>()`; animasi: `yield* ref().opacity(1, dur)`, `yield* waitFor(sec)` untuk mengatur durasi scene
- Layout brand: bg gelap `#0B0F17`, aksen `#7DD3FC`, warning `#FACC15`; font Inter + JetBrains Mono
- Jenis animasi yang dipakai: text_slam (hook), terminal line-by-line, punch zoom (masalah), checklist bertahap, pre-commit block, CTA
- **Audio: JANGAN mount `<Audio>` per-scene** — render SILENT lalu mux VO via FFmpeg (pola `-silent.mp4` + mux); lebih sederhana & tidak perlu sinkron per-scene

### 5. Render headless
```bash
cat > render.mjs << 'EOF'
import {renderVideo} from '@revideo/renderer';
async function main() {
  await renderVideo({projectFile: 'src/project.ts', settings: {outFile: '../output/motion-silent.mp4', log: 'error'}});
}
main().catch(e => {console.error(e); process.exit(1);});
EOF
node render.mjs   # lambat (~3-5 menit untuk 40s@30fps); JALANKAN BACKGROUND + notify
```
- Butuh Chrome headless (puppeteer); error "Could not find Chrome" → `npx puppeteer browsers install chrome`

### 6. Mux VO → final
```bash
ffmpeg -y -i silent.mp4 -i vo_clean.wav -c:v copy -c:a aac -b:a 128k \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -movflags +faststart final.mp4
```
- Loudness target video sosial: **-14 LUFS** (VO bersih I=-16 → mux ke -14)

## Pitfalls

- **edge-tts DILARANG untuk konten berbayar** (lisensi CPML/CC-BY-NC/proprieter per content-produce). Prioritas: suara sendiri > Piper id_ID > Kokoro (EN only).
- **Card statis ≠ motion graphic** — konten short butuh gerakan; tanpa Revideo minimal FFmpeg Ken Burns.
- **Baca skill + BRAND.md SEBELUM produksi** — jangan skip; inilah akar kualitas turun.
- **Render headless lambat** — selalu background=true + notify=true; jangan blocking di terminal.
- **File `.ts` dengan JSX** → parse error (rolldown/vite); pakai `.tsx`.
- **`revideo render` subcommand tidak ada di 0.11** — CLI hanya `serve`/`editor`; render lewat API renderer (`renderVideo()`).
- **Audio per-scene rumit** — render silent + mux jauh lebih sederhana.

## Verification

- Output: `ffprobe` durasi ≈ 40s, 1080×1920, 30fps; loudness -14 LUFS (±1); audio ada
- QA visual: ekstrak frame tiap scene → vision check (teks tidak terpotong, tidak overlap)
- Cover/thumbnail: `ffmpeg -ss 1 -i final.mp4 -frames:v 1 cover.jpg`
