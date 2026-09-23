---
name: reels-motion-render
description: Use when rendering a Reels/TikTok video with HyperFrames.
---

# Reels motion render (HyperFrames + GSAP + Piper)

Produksi short vertikal motion graphic untuk ZARYU ABSTRACT STUDIO. Pipeline
ini satu-satunya yang terverifikasi menghasilkan kualitas setara konten yang
sudah dipublikasi — PNG statis + FFmpeg concat menghasilkan artefak 3× yang
dikirim ke mana-mana (ke mana saja) (lihat bawah).

## Langkah 0 — WAJIB sebelum produksi konten baru

Cari pipeline riwayat dulu. Satu langkah ini menghemat satu malam.

```bash
grep -rl "hyperframes" ~/Downloads/niu-konten/*/package.json 2>/dev/null
which hyperframes && hyperframes --version
```

Kalau binary ada, pakai yang ini — bukan framework motion lain yang belum
pernah dirender di mesin ini. Komposisi lama di `~/Downloads/niu-konten/<reels-NN>/index.html`
adalah sumber pola yang paling boleh disalin; `assets/gsap.min.js` di sana bisa
lalu di-copy.

## Langkah 1 — Struktur proyek

Satu proyek = satu home di `project/<slug>/`. Komposisi di `web/`:

```
web/
  hyperframes.json    {"$schema":"https://hyperframes.heygen.com/schema/hyperframes.json",
                       "registry":"https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
                       "paths":{"blocks":"compositions","components":"compositions/components","assets":"assets"},
                       "media":{"autoProxy":true}}
  package.json        {"name":"reels-NNN","private":true,"type":"module",
                       "scripts":{"render":"hyperframes render"}}
  index.html          komposisi
  assets/gsap.min.js  dari proyek riwayat (jangan download ulang)
```

Node 26 + hyperframes 0.8.x global di `/usr/local/bin/hyperframes`.

## Langkah 2 — VO dulu, baru timing scene

Urutan terbalik membuat scene dan suara seret. Buat VO penuh, split per
segmen, ukur durasi tiap segmen, baru tentukan `data-start`/`data-duration`
setiap scene = durasi segmen + gap 0,2 s.

```bash
for i in 1 2 3 4 5 6; do ffprobe -v error -show_entries format=duration \
  -of csv=p=0 src/vo/seg-0$i.mp3; done
```

Prioritas suara: suara sendiri → Piper → Kokoro. `edge-tts` dilarang untuk
konten yang dijual (konten berbayar). Suara legal adalah aturan studio, bukan
preferensi estetika.

## Langkah 3 — Komposisi

Root wajib membawa metadata, dan setiap scene di-track terpisah:

```html
<div id="root" data-composition-id="reels003" data-start="0" data-duration="40.4"
     data-width="1080" data-height="1920" data-fps="30">
  <section id="s1" class="clip" data-start="0" data-duration="4.2" data-track-index="1">
```

Tanpa `data-duration` di root, HyperFrames tidak tahu kapan berhenti dan
render menjadi kosong. Tanpapa `data-track-index`, scene bertumpuk.

Satu timeline GSAP paused, didaftarkan ke `window.__timelines` — format ini
yang dibaca HyperFrames saat capture per-frame. Pola kaya yang terverifikasi:
`fromTo` + `power3.out` untuk entry (opacity + y + scale), `back.out` untuk
elemen punch terakhir, fade-out antar scene dengan `tl.to(..., 0.35)` diikuti
`tl.set(opacity, 0)` tepat di batas. Detail markup + timing:
`references/composition.md`.

Font dan palet dari BRAND.md proyek (Inter + JetBrains Mono; `#0B0F17` /
`#7DD3FC` / `#FACC15`). BRAND.md menang kalau bentrok dengan template —
periksa `font-family` dan kode warna sebelum render, bukan sesudah.

## Langkah 4 — Render silent

```bash
cd web && hyperframes render . -o ../output/<slug>-silent.mp4 \
  --format mp4 -f 30 --workers 2 --no-browser-gpu
```

Benchmark mesin ini (i5-10310U, 16 GB, UHD 620 2 GB): 4 menit 31 detik untuk
1698 frame, 4 menit 07 detik untuk 1212 frame, keduanya 2 worker.

`--no-browser-gpu` sengaja: VRAM 2 GB tidak menambah kecepatan, software
raster sudah cukup cepat untuk komposisi CSS murni.

## Langkah 5 — Mux audio

```bash
ffmpeg -y -v error -i output/<slug>-silent.mp4 -i src/vo_piper_clean.wav \
  -c:v copy -c:a aac -b:a 128k -ac 2 -ar 48000 -movflags +faststart \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -shortest output/<slug>.mp4
```

`-ar 48000` wajib: Piper output 192 kHz, dan platform sosial menolak atau
menurunkan sample rate non-standar saat upload. `-c:v copy` menghindari
re-encode video.

## Langkah 6 — QA sebelum klaim selesai

Ekstrak satu frame per scene **setelah animasi elemen terakhir selesai masuk**
(baca offset di timeline, bukan titik tengah durasi scene — frame awal scene
hanya menampilkan headline). Verifikasi dengan `vision_analyze`:

1. Semua teks utuh, tidak terpotong tepi. Ini bug berulang — judul lebar di
   tengah atas paling sering kena, termasuk oleh efek pan.
2. Font + warna sesuai BRAND.md.
3. `ffprobe`: `h264,1080,1920,30/1` dan `aac,48000,2`.
4. Loudness `input_i` antara -14,5 dan -13,5.
5. Cover 1080×1920 diambil dari frame paling padat secara visual.

## Pitfall

**Proses render lama tidak mati saat Chrome dibunuh.** `pkill` terhadap binary
Chrome tidak membunuh `node render` yang memilikinya, sehingga port tetap
listen dan render berikutnya bertabrakan — gejalanya log kosong selama
jam-jam berturut-turut. Sebelum render ulang: `lsof -iTCP:9000,9001
-sTCP:LISTEN`, lalu kill node + chrome + bebaskan port. Render yang berjalan
>2× estimasi benchmark harus dihentikan, bukan dibiarkan.

**Jalur frame-persendirian tidak praktis di mesin ini.** Screenshot CLI per
frame mengukur 2,9 detik/frame — 1 jam untuk 1212 frame. Loop CDP dalam satu
sesi browser tidak stabil untuk jumlah frame tersebut (frame detach di ~frame
20). HyperFrames satu-satunya jalur masuk akal; jangan diinvestasi ulang.

**Jangan `git add -f` artefak.** `node_modules/` ter-ignore dan harus tetap
ter-ignore — 363 MB dependency tidak perlu masuk repo. Gate
`scripts/secret-scan-staged.py` hanya menangkap pola rahasia, bukan volume.

**Satu proyek, satu rumah.** Semua artefak di `project/<slug>/`; video final
hanya diakui dari `output/`. Folder di `~/Downloads/niu-konten/` adalah
riwayat referensi, bukan tempat kerja proyek baru.
