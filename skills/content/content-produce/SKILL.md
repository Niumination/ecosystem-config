---
name: content-produce
description: "Produksi video, audio, gambar dengan stack open source"
version: 1.0.0
author: Hermes Content Studio Pack
license: MIT
metadata:
  hermes:
    tags: [Content, Production, FFmpeg, WhisperX, TTS, ComfyUI]
    related_skills: [content-studio, content-script, content-legal]
---

# Content Produce

Mengubah naskah menjadi berkas jadi yang memenuhi spesifikasi platform — memakai **hanya** tool gratis/open source, dengan jalur kerja untuk mesin tanpa GPU maupun dengan GPU.

## When to Use

- `/produksi <slug>`, "render", "bikin videonya", "export untuk TikTok/YouTube"
- "buat voice over", "caption otomatis", "thumbnail", "carousel jadi gambar", "musik/SFX"
- "perbaiki audio/video ini", "buang bagian hening", "jadikan vertikal"

## Quick Reference

| Kebutuhan | Tool (lisensi) | Perintah inti |
|---|---|---|
| Transkrip + caption word-level | WhisperX (BSD-2), faster-whisper (MIT) | `whisperx audio.wav --model large-v3 --align_model wav2vec2 --output_format json` |
| Voice over CPU | Kokoro-82M (Apache-2.0) | `python -m kokoro --voice af_heart --text "naskah" out.wav` / kokoro-fastapi (Docker) |
| Voice clone (butuh GPU) | Chatterbox (MIT), Orpheus 3B (Apache-2.0) | server lokal → POST audio referensi + teks |
| Buang hening | Auto-Editor (LGPL) | `auto-editor in.mp4 --edit audio --threshold -35dB --margin 0.1s` |
| Vertikal + loudnorm + caption | FFmpeg (LGPL) | `bash scripts/vertical_clip.sh in.mp4 out.mp4` |
| Motion graphics / batch render | Motion Canvas (MIT), Revideo (MIT) | `npx revideo render project.ts --props data.json` |
| Gambar/poster dengan teks | Qwen-Image (Apache-2.0) via ComfyUI | API `:8188` prompt → PNG |
| B-roll generatif | Wan 2.2 (Apache-2.0), FramePack (Apache-2.0, 6GB) | ComfyUI workflow I2V/T2V |
| Avatar/lip-sync | LatentSync (Apache-2.0), MuseTalk (MIT), InfiniteTalk (Apache-2.0) | foto + audio → video berbicara |
| Denoise/enhance audio | DeepFilterNet (Apache/MIT), resemble-enhance (MIT) | `deepFilter in.wav` |
| Musik/SFX | ACE-Step, MMAudio (cek checkpoint), Freesound CC0 | generate → mix −20 dB |
| Upscale/interp | Real-ESRGAN (Apache/BSD), RIFE (MIT) | 720p → 4K, 30 → 60 fps |
| Vektor/desain | Inkscape (GPL), Penpot (MPL-2.0), ImageMagick | `magick` untuk batch resize/watermark |
| Rekam layar (inti Mode A) | OBS Studio (GPL) | scene FULL/EDITOR/BROWSER/TERMINAL, zoom 150%, MKV→MP4 |
| NLE manual | OpenCut (MIT), Kdenlive (GPL), Shotcut (GPL) | untuk finishing manusia |

## Procedure

### A. Persiapan (selalu)
1. Baca `project/<slug>/NASKAH.md` + `SHOTLIST.csv` + `BRAND.md` (font, warna, watermark).
2. Buat `project/<slug>/assets/` dan `output/`.
3. Cek alat: `ffmpeg -version`, `magick -version`, `python3 -c "import faster_whisper"`, `npx revideo --version`, ComfyUI `curl localhost:8188/system_stats`.
4. Tentukan **mode**: `A` (tanpa GPU) atau `B` (GPU). Tulis mode di `STATUS.md` supaya jujur soal kemampuan.

### B. Voice over — **jalur bahasa Indonesia (Mode A)**

Kokoro-82M **tidak mendukung bahasa Indonesia** (hanya en/ja/zh/fr/it/pt/es/hi). Untuk konten Indonesia, urutan keputusan:

| Prioritas | Mesin | Lisensi | Kebutuhan | Kapan dipakai |
|---|---|---|---|---|
| **1** | **Suara sendiri** (rekam HP/mic) | — | CPU + Audacity/DeepFilterNet | **Default.** Gratis, autentik, campuran ID+istilah EN natural — dan untuk niche teknis, suara manusia = kepercayaan = nilai jual |
| **2** | **Piper** voice `id_ID-news_tts-medium` | MIT (voice) · GPL (tool) | CPU, ONNX 63 MB | Batch/faceless. Satu-satunya TTS **bahasa Indonesia open source** yang jalan di CPU. Gaya berita: rapi tapi datar |
| **3** | **Kokoro-82M** | Apache-2.0 | CPU | Hanya untuk segmen/istilah **berbahasa Inggris** yang Piper salah ucapkan |
| **4** | **Chatterbox Multilingual** (voice `ms` sebagai proksi ID) | MIT | **GPU 6–12 GB** | Jalur upgrade ke Mode B; belum ada `id` resmi (issue #506 open), Melayu mirip fonetis + bisa clone suara Anda |
| ❌ | XTTS v2 (dukung ID), F5-TTS, edge-tts | CPML / CC-BY-NC / proprieter | — | **Jangan** untuk konten berbayar |

```bash
# ── Prioritas 2: Piper bahasa Indonesia (CPU, MIT) ─────────────────────────
# install
pip install piper-tts
python3 -m piper.download_voices id_ID-news_tts-medium     # atau unduh manual dari
#   https://huggingface.co/rhasspy/piper-voices/tree/main/id/id_ID/news_tts/medium
# sintesis
python3 -m piper -m id_ID-news_tts-medium -f vo_raw.wav -- < naskah_vo.txt
# bersihkan + normalisasi
ffmpeg -i vo_raw.wav -af "highpass=f=80,lowpass=f=11000,loudnorm=I=-16:TP=-1.5" vo_clean.wav
# uji dulu sebelum render penuh (wajib):
python3 -m piper -m id_ID-news_tts-medium -f uji.wav <<< "Saya deploy aplikasi Supabase ke Vercel."

# ── Prioritas 3: Kokoro untuk segmen EN (Apache-2.0, CPU) ─────────────────
python3 -m kokoro --voice af_heart --speed 1.0 --text "Row level security keeps user data safe." vo_en.wav

# ── Prioritas 1: suara sendiri → bersihkan ────────────────────────────────
deepFilter rekaman.wav                      # DeepFilterNet (Apache/MIT) — pengganti Adobe Podcast
ffmpeg -i rekaman_denoised.wav -af "loudnorm=I=-16:TP=-1.5" vo_clean.wav
```

**Masalah nyata Piper + konten coding:** istilah teknis Inggris diucapkan aneh oleh phonemizer espeak `id`.
Penanganan wajib:
1. Pakai kamus pelafalan `workspace/brand/voice/pronunciation-id.csv` — tulis ulang istilah ke ejaan fonetis Indonesia di naskah VO (`Supabase`→"supa beis", `middleware`→"midel wer", `deploy`→"di ploi", `query`→"kwe ri", `dashboard`→"des bord").
2. **Teks on-screen/caption tetap memakai istilah asli** walau VO memfonetiskannya.
3. Kalimat yang sangat padat istilah → rekam suara sendiri, atau pakai Kokoro (EN) untuk kalimat itu lalu gabung dengan `ffmpeg concat`.
4. Simpan istilah baru yang bermasalah ke kamus pelafalan — aset ini makin berharga tiap minggu.
5. Selalu dengarkan `uji.wav` sebelum render penuh; jangan pernah render 10 menit lalu menemukan pelafalan rusak.

Pilih **satu** suara sebagai brand voice, catat di `BRAND.md`. Butuh suara orang lain? Rekam 10–60 detik → Chatterbox (Mode B) → simpan `brand/voice/ref.wav` + surat izin `templates/model-release.md`. Podcast 2 suara: rekam sendiri, atau dua preset berbeda lalu mix.

### C. Caption & transkrip
```bash
whisperx vo_clean.wav --model small --language id --output_format srt --output_dir cap/
# atau faster-whisper bila WhisperX berat:
python3 -c "from faster_whisper import WhisperModel; ..."
```
Lalu burn-in (gaya TikTok, aman dari UI):
```bash
ffmpeg -i draft.mp4 -vf "subtitles=cap/vo_clean.srt:force_style='FontName=Inter,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=320'" -c:v libx264 -crf 19 -c:a copy out_cap.mp4
```
Simpan `.srt` juga sebagai file terpisah (untuk LinkedIn/YouTube yang butuh unggah caption).

### D. Rakit video
**Mode A — motion graphic / slideshow (paling cepat & konsisten):**
1. Siapkan aset: screenshot (OBS), gambar CC0 (Pexels/Pixabay), diagram SVG (Inkscape), logo.
2. Buat proyek Revideo/Motion Canvas dari `templates/formats/shorts.json` → render headless:
   `npx revideo render src/short.ts --props project/<slug>/data.json --out output/short.mp4`
3. Atau rakit langsung dengan FFmpeg concat + zoom (Ken Burns) + overlay teks.

**Mode B — dengan footage generatif:**
1. ComfyUI: Qwen-Image untuk thumbnail/poster; Wan 2.2/FramePack untuk B-roll; LatentSync untuk lip-sync.
2. Gabungkan B-roll + VO + caption di OpenCut/Kdenlive atau langsung FFmpeg.

**Finishing (semua mode):**
```bash
auto-editor rough.mp4 --edit audio --threshold -35dB      # buang hening
bash scripts/vertical_clip.sh rough_tight.mp4 output/tiktok_1080x1920.mp4
ffmpeg -i output/tiktok_1080x1920.mp4 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" output/ig_square.mp4
ffmpeg -i output/tiktok_1080x1920.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black" output/yt_landscape.mp4
```

### E. Thumbnail & carousel
```bash
ffmpeg -ss 00:00:14 -i output/yt_landscape.mp4 -frames:v 1 frame.jpg
magick frame.jpg -resize 1280x720^ -gravity center -extent 1280x720 \
  -pointsize 88 -font Inter-Bold -stroke black -strokewidth 6 -annotate +60+540 "GRATIS" \
  -stroke none -fill "#FFD166" -annotate +60+540 "GRATIS" output/thumb_v1.jpg
```
Buat **3 varian thumbnail** (kata berbeda/warna berbeda) untuk A/B. Carousel: render tiap slide Markdown → SVG (Inkscape) → PNG 1080×1350, atau ekspor dari Penpot.

### F. Audio mix & loudness
| Target | Setting |
|---|---|
| Video sosial | `loudnorm=I=-14:TP=-1.5:LRA=11` |
| Podcast | `loudnorm=I=-16:TP=-1.5:LRA=11`, 48 kHz stereo |
| Musik latar | −20 dB relatif VO |
| SFX | −18 dB, durasi < 0,5 s |

### G. Handoff ke publish
Tulis `project/<slug>/output/MANIFEST.md`: daftar file, platform tujuan, rasio, durasi, checksum, caption/deskripsi, hashtag, CTA, kredit aset, status AI disclosure. Lalu panggil `content-publish`.

## Pitfalls

- **Jangan pakai model non-komersial** (FLUX.1/2 [dev], XTTS v2, F5-TTS weights, SVD, Wav2Lip) untuk konten yang menghasilkan uang.
- **Jangan unggah aset tanpa mencatat lisensi** → tiap unduhan masuk `workspace/data/ASSETS_LICENSE.csv`.
- **Loudness salah = terasa murahan.** Selalu jalankan `loudnorm`; verifikasi dengan `ffmpeg -i out.mp4 -af loudnorm=print_format=json -f null -`.
- **Caption menutupi UI platform.** Jaga margin bawah ± 320 px (9:16) dan atas ± 220 px.
- **VRAM kurang → jangan paksa.** Turunkan resolusi/model (GGUF quantized, FramePack 6GB) atau pindah Mode A.
- **Render headless di container:** pastikan FFmpeg + font terpasang di *backend* yang dipakai Hermes (Docker/VPS), bukan hanya di laptop Anda.
- **Font tidak ditemukan** → pasang font OFL (Inter, Archivo, Bebas Neue) ke `~/.fonts` lalu `fc-cache -f`.
- **Jangan kompres dua kali.** Simpan master tanpa kompresi; export turunan dari master.

## Verification

- `output/MANIFEST.md` ada dan lengkap; setiap file tujuan platform ada.
- `ffprobe` tiap output: rasio & fps benar, durasi sesuai brief, ada stream audio.
- Loudness terukur −14 LUFS (±1) untuk video; −16 LUFS untuk podcast.
- Caption `.srt` tersedia dan sinkron (cek 3 titik acak).
- 3 varian thumbnail tersimpan; nama file mengandung versi (`_v1`, `_v2`).
- `ASSETS_LICENSE.csv` memiliki baris untuk setiap aset pihak ketiga yang dipakai.
- `STATUS.md` berpindah ke `4.QA` dan siap diperiksa `content-studio qa`.
