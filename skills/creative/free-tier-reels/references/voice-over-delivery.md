# Voice-over gratis yang terdengar wajar (edge-tts) + cara mengaudit provenance voice

Dipakai saat narasi perlu terdengar seperti orang berbicara, bukan TTS membaca teks. Ada dua lapis: **naskah** (skill `ghost`) dan **delivery** (parameter yang bisa dikontrol).

## Lapis 1 — naskah (pass `ghost`)

- Kalimat pendek berdiri sendiri. "Bikin konten itu mahal. Editing. Stok video. Penjadwal." lebih enak didengar daripada satu kalimat mengalir.
- Buang pembukaan basa-basi dan kiasan; ganti dengan kata kerja biasa.
- Variasikan ritme: selipkan kalimat 2–3 kata di antara kalimat panjang.
- **Angka dieja kata**: "seratus empat puluh tiga", "dua ratus dua puluh sembilan juta rupiah". Digit (`229.391.668`) membuat TTS salah jeda atau membacanya per digit.
- Pass ini hanya menyentuh cara mengucapkan — jangan ubah fakta/klaim saat merapikan gaya.

## Lapis 2 — delivery

- **Jeda hanya lewat tanda baca.** `edge-tts` gratis tidak menerima SSML (tidak ada `<break>`): titik = jeda penuh, koma = jeda pendek, em-dash `—` = jeda dramatis.
- **rate & pitch per adegan, bukan satu setelan.** Tabel acuan (rate / pitch):

| Jenis adegan | rate | pitch | Alasan |
|---|---|---|---|
| hook pembuka | +8% … +10% | −2 Hz | pembuka cepat dan agak berat |
| naratif biasa | +2% | 0 | alami |
| proses/aksi | +6% | 0 | energi |
| **adegan angka** | −4% | −3 Hz | angka harus melambat supaya dicerna |
| penutup/CTA | −4% | −2 Hz | menutup dengan tenang |

- **Audisi voice sebelum produksi.** Render satu kalimat hook dengan ≥3 voice, gabung berurutan jadi satu berkas (beri jeda 0,4 s antar kandidat), kirim ke pemilik untuk dipilih; simpan berkas audisi di folder kerja supaya pilihan bisa diulang.
- Kalau nanti ditambah musik trending dari aplikasi Instagram: turunkan volume audio tambahan (±10–20%) supaya VO tetap jelas.

## Alur produksi VO

```bash
ET=$HOME/.venv-mata/bin/edge-tts          # edge-tts gratis, tanpa API key
# satu render per adegan; rate/pitch mengikuti tabel di atas
$ET --voice en-US-EmmaMultilingualNeural --rate=+10% --pitch=-2Hz \
    --text "Seratus empat puluh tiga skill AI — satu orang, satu laptop." \
    --write-media vo2/S1.mp3
# ukur tiap segmen DAN pastikan muat di jendela scene-nya
ffprobe -v error -show_entries format=duration -of csv=p=0 vo2/S1.mp3

# gabung dengan delay = awal tiap scene (ms), lalu normalisasi loudness + apad
ffmpeg -v error -y -i vo2/S1.mp3 -i vo2/S2.mp3 -i vo2/S3.mp3 \
  -filter_complex "[0:a]adelay=500|500[a0];[1:a]adelay=5500|5500[a1];[2:a]adelay=11600|11600[a2];\
[a0][a1][a2]amix=inputs=3:normalize=0:dropout_transition=0[mix];[mix]loudnorm=I=-16:TP=-1.5:LRA=11,apad[out]" \
  -map "[out]" -t 38 -ar 48000 -ac 2 vo_mix.wav

# mux ke video SENYAP (video dirender lebih dulu)
ffmpeg -v error -y -i final-silent.mp4 -i vo_mix.wav -c:v copy -c:a aac -b:a 192k \
  -t 38 final.mp4            # JANGAN -shortest: itu memotong video sepanjang audio
```

Verifikasi hasil: `ffprobe` (h264 1080×1920 + aac stereo, durasi = durasi komposisi) dan `volumedetect` (mean ≈ −19 s.d. −20 dB, max di bawah −3 dB → tidak clipping).

## Kalau pemilik menunjuk voice referensi yang "lebih bagus"

1. **Tanya dulu tool/engine yang membuat berkas referensi itu.** Satu pertanyaan selalu lebih murah daripada forensik audio; forensik hanya kalau pemilik tidak tahu.
2. Kalau perlu bukti, urutannya: **properti container** lebih dulu (`ffprobe` → sample rate, bitrate, `TAG:encoder`) — tag `Lavf*` berarti berkas sudah diproses ulang ffmpeg, bukan keluaran mentah engine; lalu **jarak DTW log-mel dengan kontrol terkalibrasi** lewat `scripts/audio-similarity.py` di skill `short-form-video-production` (kontrol: referensi vs dirinya ≈0 · voice sama di-render ulang ≈0,1 · berkas sama di-encode ulang ≈1 = batas atas "voice sama"; ≥5× batas itu = engine berbeda). Korelasi gelombang mentah hanya sah untuk berkas yang benar-benar sama: re-encode tidak merusaknya (≈0,97), tetapi perubahan rate atau teks menghancurkannya — jadi "korelasi ≈0" BUKAN bukti engine berbeda.
2b. **Jangan simpulkan "set ini berisi beberapa voice" dari f0 per berkas.** f0 median bergeser 40–55 Hz hanya karena berkas dipotong di titik berbeda — di dalam SATU berkas sekali pun — jadi perbandingan antar-berkas menghasilkan "beberapa voice" dari set yang sebenarnya satu voice. Kalau ingin menguji jumlah voice, pakai metrik timbre (rata-rata spektrum mel pada frame bersuara) beserta **kontrol teks-beda**: berkas identik `0,0000` · satu voice beda rate 22% `0,0002` · satu voice teks beda `~0,001` · antar-adegan satu voice `0,007–0,015` · voice lain `0,027+`. Tanpa kontrol teks-beda, jarak `0,02` terlihat "dekat" padahal itu voice lain. Skripnya: `scripts/audio-similarity.py` mode `--timbre` di skill `short-form-video-production`.
2c. **Jangan menyimpulkan "rekaman manusia" dari ketidakcocokan.** Tidak cocok = engine belum diketahui, bukan berarti bukan TTS (folder bernama `vo-manual/` pun bisa berisi TTS). Lapor "engine tidak teridentifikasi" dan tanyakan lagi dengan berkas spesifik di tangan, lalu tawarkan opsi di poin 4.
3. **Estimasi f0 kasar bukan bukti.** Median f0 dari autokorelasi sederhana rentan kesalahan oktav, dan bergeser 40–55 Hz di dalam satu berkas hanya karena titik potongnya. Pakai hanya sebagai petunjuk pemilihan voice, bukan kesimpulan; kalau butuh f0 yang sah, validasi estimatornya dulu pada nada sintetis (110/220/150 Hz harus terbaca tepat) dan pakai estimator tahan oktav (YIN).
4. Kalau engine referensi tidak bisa direproduksi dengan tool gratis, katakan terbuka ke pemilik dan tawarkan: (a) voice gratis terdekat, atau (b) pilih dari berkas audisi. Jangan teruskan forensik setelah pemilik bisa menjawabnya.
