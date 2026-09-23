# Pembelajaran Produksi — reels-003 (23 Sep 2026)

Tulisan ini mencatat kenapa konten pertama di studio jatuh kualitasnya setelah
penerapan skill content-studio, dan apa yang sebenarnya menjadi pembatas.
Ditulis untuk mencegah pengulangan, bukan untuk menyalahkan satu sesi.

## Perbandingan hasil

| | reels-02 (niu-oss-dashboard, 19 Sep) | reels-003 v1 | reels-003 v2 | reels-003 v3 |
|---|---|---|---|---|
| Mesin render | HyperFrames + GSAP | FFmpeg concat | FFmpeg Ken Burns | HyperFrames + GSAP |
| Komposisi | HTML/CSS kaya | PNG ImageMagick statis | PNG + zoom/pan | HTML/CSS kaya |
| Suara | Gemini TTS | edge-tts ArdiNeural | Piper id_ID | Piper id_ID |
| Durasi | 56,6 s | 40,3 s | 39,7 s | 39,7 s |
| Ukuran | 5,2 MB | 1,3 MB | 1,3 MB | 3,92 MB |
| Hasil | dipublikasi | ditolak | ditolak | disetujui |

Perbedaan kualitasnya tidak terletak pada durasi atau durasi total, melainkan
pada **jenis artefak visual**. PNG datar 1,3 MB tidak mungkin terlihat seperti
komposisi GSAP 5,2 MB — keduanya bukan satu kategori barang.

## Tiga akar masalah v1 dan v2

**1. edge-tts dipakai untuk konten berbayar.** Skill content-produce melarang
edge-tts eksplisit untuk konten yang dijual (priority chain: suara sendiri →
Piper → Kokoro). Saya langsung loncat ke edge-tts karena tercepat. Ini bukan
kesalahan estetika; ini pelanggaran aturan studio yang seharusnya sudah terbaca
sebelum naskah ditulis.

**2. Komposisi HTML/CSS tidak dipakai.** Skill content-produce Mode A menyebut
Revideo atau Motion Canvas. Keduanya tidak pernah dicoba secara benar. Yang
dibuat adalah card PNG + concat, yang secara teknis memenuhi "video 40 detik"
tapi tidak memenuhi "motion graphic". Skill menyebut Revideo sebagai jalur
utama, padahal Revideo 0.11 tidak jalan di mesin ini sama sekali.

**3. BRAND.md diabaikan.** Font wajib Inter + JetBrains Mono, warna wajib
`#0B0F17` / `#7DD3FC` / `#FACC15`. v1 memakai Arial + Menlo dengan palet
navy-ungu-merah. BRAND.md menyatakan eksplisit "dokumen ini yang menang jika
bentrok dengan template", dan tetap dilewati karena card dibangun dengan
ImageMagick yang sudah punya palet default sendiri.

## Pembatas yang sebenarnya: mesin render

Revideo 0.11 gagal dua kali:

- `Failed to resolve import "src/project.ts"` — renderer Vite tidak resolve
  path relatif dari cwd saat headless render.
- Proses render pertama tidak pernah benar-benar mati. `pkill -f
  "chrome-mac-153"` membunuh Chrome, tapi proses `node render.mjs` lama tetap
  hidup di port 9000. Render kedua bertabrakan, dan yang terlihat hanya log
  kosong selama 7,4 jam.

Jalur chrome CLI per-frame (`--screenshot` + query string `?__t=`) terbukti
mampu seek GSAP, tapi laju rendernya 2,9 detik per frame — 1 jam untuk 1212
frame di mesin ini dengan 4 pekerja. Tidak praktis.

Jalur yang benar sudah ada di mesin sejak awal: **HyperFrames 0.8.6 global**
(`hyperframes@0.8.6` di `/usr/local/bin/hyperframes`, package.json reels-02
memakai `npx hyperframes@0.8.30`). Reels-02 dirender dengan 2 worker dalam
4 menit 31 detik untuk 1698 frame; reels-003 v3 dalam 4 menit 7 detik untuk
1212 frame.

Kesimpulan: **ketika seorang agent tidak menemukan path yang sudah dipakai
sebelumnya, waktu render berubah dari 4 menit menjadi 7 jam.** Ini pola yang
harus dicek pertama kali di proyek konten baru.

## Hal yang perlu diperbaiki di skill / proses

1. **Mode A seharusnya menunjuk HyperFrames**, bukan Revideo, untuk studio ini.
   Revideo 0.11 terverifikasi tidak berfungsi di mesin ini (23 Sep 2026).
   HyperFrames terverifikasi berfungsi dua kali.
2. **Langkah "cari pipeline riwayat" wajib sebelum produksi konten baru.**
   Mencari `hyperframes` di `~/Downloads/niu-konten/*/package.json` memakan
   waktu 2 menit dan menghemat 7 jam.
3. **QA teknik harus mengecek `BRAND.md` secara otomatis** (font family +
   kode warna), bukan hanya resolusi dan loudness.
4. **Proses kill render harus membunuh node + chrome + port**, bukan hanya
   Chrome. `lsof -iTCP:9000 -sTCP:LISTEN` sebelum mulai render ulang.

## Yang sudah benar dari awal dan harus dipertahankan

- VO Piper `id_ID-news_tts-medium` (v2 ke atas) — legal untuk konten berbayar.
- Timing scene dipatok dari durasi segmen VO nyata, bukan perkiraan.
- QA visual per-frame sebelum klaim selesai.
- `output/` sebagai source of truth, LFS untuk artefak biner.
