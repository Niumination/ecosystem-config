# Komposisi HyperFrames untuk video 9:16 — aturan yang lolos lint & QA

Catatan praktis yang dipakai saat menulis komposisi HTML→MP4 untuk reels. Aturan framework ada di dokumentasi resmi (`npx --no-install hyperframes docs data-attributes|gsap|rendering`); berkas ini memuat yang membuat render lolos lint dan tembus QA mata.

## Struktur komposisi

- Root: `data-composition-id`, `data-start="0"`, `data-duration="<total detik>"`, `data-width="1080"`, `data-height="1920"`, `data-fps="30"`.
- Tiap scene = satu elemen `class="clip"` dengan `data-start`/`data-duration`. `data-track-index` hanya lane tampilan di Studio — render tidak membacanya dan tidak menentukan urutan tumpuk (pakai `z-index`).
- Semua animasi didaftarkan di `window.__timelines["<composition-id>"] = gsap.timeline({ paused: true })`, diposisikan absolut (`tl.to(el, vars, 1.5)`). Properti yang didukung: `opacity, x, y, scale, scaleX, scaleY, rotation, width, height, visibility` — warna/`filter`/`clip-path` tidak.
- Hanya logika deterministik: tanpa `Date.now()`, tanpa `Math.random()`, tanpa fetch jaringan.

## Dua hal yang paling sering menggagalkan render

**1. GSAP wajib di-vendor.** Scaffold bawaan menaruh `<script src="https://cdn.jsdelivr.net/npm/gsap@3/...">`. Unduh sekali ke `assets/gsap.min.js` (±73 KB) dan rujuk lokal: JS deterministik tidak boleh bergantung pada unduhan saat render, dan render yang gagal memuat GSAP menghasilkan frame statis tanpa pesan jelas.

**2. Tween keluar tidak boleh menyasar elemen `.clip`.** Lint akan menolak dengan `gsap_exit_missing_hard_kill`: runtime mengatur visibilitas clip, dan seeking non-linear bisa berhenti setelah fade sehingga status visibilitas tertinggal. Pola yang diterima:

```html
<section id="s1" class="clip" data-start="0" data-duration="5">
  <div class="inner" id="s1in"> <!-- layout: flex/padding tinggal di wrapper ini -->
    …isi scene…
  </div>
</section>
```
```js
// animasi masuk menyasar elemen di dalam (#s1k, #s1h, …)
tl.to("#s1in", { opacity: 0, duration: 0.4 }, 4.6);   // fade keluar
 tl.set("#s1in", { opacity: 0 }, 5.0);                  // hard kill di batas clip berikutnya
```

## Alur render yang hemat waktu

```bash
npx --no-install hyperframes lint --verbose        # WAJIB 0 error sebelum render
npx --no-install hyperframes render --resolution=portrait --fps=30 --quality=draft -o draft.mp4   # ±1 menit (38 s)
# — periksa frame (lihat bawah), perbaiki komposisi, ulangi lint + draft —
npx --no-install hyperframes render --resolution=portrait --fps=30 --quality=high  -o final-silent.mp4  # ±2 menit
```

- `--resolution=<preset>` mengubah `deviceScaleFactor` Chrome: rasio harus sama dengan komposisi dan pengalinya bilangan bulat. Jangan mengarang flag `--width/--height`.
- `npx --no-install hyperframes check` (lint + runtime + layout + motion + contrast) lebih lengkap daripada `lint` sendiri.
- `init` bisa tampak menggantung di akhir karena jaringan npm padahal berkasnya sudah ditulis: periksa isi folder sebelum menunggu atau mengulang.
- Proyek hasil `init` mem-pin versi CLI; naikkan dengan `npx hyperframes@latest upgrade --project . --check`.

## Gerbang QA frame (sebelum render final, bukan sesudah)

```bash
ffmpeg -v error -ss 2.5 -i draft.mp4 -frames:v 1 -y f1.png
ffmpeg -v error -i f1.png -i f2.png -i f3.png \
  -filter_complex "[0:v]scale=600:1067[a];[1:v]scale=600:1067[b];[2:v]scale=600:1067[c];[a][b][c]hstack=3" -y sheet.png
```

Periksa dengan tool vision: teks terbaca, tidak ada elemen terpotong/beririsan, kanvas tidak separuh kosong, hierarki jelas. Alternatif dari CLI: `npx --no-install hyperframes snapshot` (frame kunci jadi PNG). Satu render draft jauh lebih murah daripada satu video yang ditolak pemilik.

## Verifikasi hasil

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate \
  -show_entries format=duration,size -of default=noprint_wrappers=1 out.mp4
```

Pastikan kodek, dimensi sesuai preset, dan durasi = durasi komposisi (durasi bisa terpotong kalau mux audio memakai `-shortest`; lihat `voice-over-delivery.md`).

## Dokumentasi keyword yang berguna

`npx --no-install hyperframes docs <topik>`: `data-attributes`, `gsap`, `rendering`, `compositions`, `examples`, `troubleshooting`. Untuk daftar perintah lengkap: `npx --no-install hyperframes --help` (termasuk `check`, `snapshot`, `inspect`, `benchmark`, `doctor`).
