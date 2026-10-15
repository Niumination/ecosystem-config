---
name: ffmpeg-ken-burns-motion
category: creative
description: "Use when making still cards move: FFmpeg zoompan + mux VO."
version: 1.0.0
---

# FFmpeg Ken Burns — motion dari still card, tanpa GPU/browser

Jalur PALING SEDERHANA untuk short vertikal bergerak: card PNG (brand) + efek zoom/pan via FFmpeg `zoompan` + mux VO. Stdlib-native, tanpa Chrome headless, tanpa npm stack. Terbukti di reels-003: sukses di percobaan pertama setelah Revideo+Chrome macet berjam-jam.

## Kapan pakai

- Card PNG 1080×1920 sudah jadi (ImageMagick, brand: Inter/JetBrains Mono, bg #0B0F17)
- Mesin tanpa GPU; mau hasil motion (bukan slide statis) tanpa menambah dependency JS
- Render Revideo/headless macet atau tidak menulis output

## Alur

1. Segmen: tuple `(nama_card, start_detik, durasi_detik, efek)` — durasi = durasi VO segmen; total = durasi VO keseluruhan. Jumlah segmen = jumlah scene; total = durasi VO.
2. Render tiap segmen:
   - zoom_in (AMAN utk card padat teks): `ffmpeg -y -loop 1 -i card.png -vf "zoompan=z='zoom+0.0005':d=<dur*30>:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30" -t <dur> -c:v libx264 -pix_fmt yuv420p seg.mp4`
   - pan_left/pan_right: zoom tetap 1.1–1.2, geser x/y linear satu tepi ke tepi lain — HANYA utk card jarang teks di tepi.
3. Concat: daftar segmen + `ffmpeg -f concat -safe 0 -i list.txt -c copy silent.mp4` (tambah fade via filter bila perlu).
4. Mux VO: `ffmpeg -i silent.mp4 -i vo_clean.wav -c:v copy -c:a aac -b:a 128k -af loudnorm=I=-14:TP=-1.5 -movflags +faststart final.mp4` → target -14 LUFS.

## Pitfalls

- **Pan menggeser crop & memotong teks di tepi card** — judul/checklist kena clip. Card padat teks → zoom_in (crop tengah, aman). Rule: pan hanya untuk visual yang isinya aman di-clip tepi.
- **QA teks terpotong: periksa CARD SUMBER dulu** — font card melebihi lebar 1080px = bug PNG asli, bukan efek render. Fix font/size card, jangan ubah efek dulu.
- **Verifikasi tiap percobaan**: `ffprobe` durasi ≈ total VO, ukuran ≤ ~2MB utk 40s, loudness ±1 -14 LUFS; ekstrak frame per scene → vision QA.

## Referensi

- VO Piper + mux + brand: lihat skill `revideo-motion-graphic` (jalur Revideo) — VO/mux/brand sama.
