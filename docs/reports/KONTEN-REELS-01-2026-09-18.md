# Paket Konten Reels 01 — "Behind the Build" (18 Sep 2026)

**Pelaksana:** Hermes — thread Kreator (1172)
**Pemicu:** permintaan Afrizal Munthe — lanjutkan rencana konten, seluruh produksi harus gratis (Rp 0)
**Status:** **siap tayang** — video, narasi, dan paket caption selesai; distribusi menunggu keputusan kanal. **Revisi v2 (19 Sep 2026):** voice-over diperbaiki mengikuti lapis delivery pipeline MATA — lihat §9.

> ⚠️ **USANG — jangan diikuti (19 Sep 2026).** Seluruh §9 (investigasi voice & produksi VO v1–v4) memakai mesin **edge-tts + normalisasi teks berlapis**, yang sudah **dibatalkan**. Standar yang berlaku sekarang: **Gemini TTS** — lihat [`TTS-STANDAR-VO-2026-09-19.md`](TTS-STANDAR-VO-2026-09-19.md) dan skill `skills/creative/gemini-vo-narration/`. Visual reels (naskah, storyboard, animasi) tetap berlaku; hanya lapis suaranya diganti.

---

## 0. Ringkasan

| Item | Nilai |
|---|---|
| Pilar konten | `Behind the Build` |
| Durasi | 38,0 detik |
| Spesifikasi | 1080×1920 (9:16), 30 fps, H.264 + AAC stereo, 4,9 MB |
| Narasi | Voice-over Indonesia (suara `id-ID-ArdiNeural`), tanpa musik berlisensi |
| Berkas jadi | `~/Movies/Posting - Instagram/2026-09-18-reels-01-behind-the-build.mp4` |
| Proyek kerja | `~/Downloads/niu-konten/reels-001/` |
| **Biaya produksi** | **Rp 0** — tanpa langganan, tanpa stok berbayar, tanpa API berbayar |

---

## 1. Naskah & struktur (6 scene)

| Waktu | Scene | Teks di layar | Narasi (VO) |
|---|---|---|---|
| 0–5 s | Hook | "143 skill AI dibangun sendiri." · chip: Naskah / Video / Tayang / **Rp 0** | "Seratus empat puluh tiga skill AI, dibangun sendiri." |
| 5–11 s | Masalah | "Bikin konten itu mahal." · baris: Editing Rp 150rb · Stok video Rp 300rb · Penjadwal Rp 200rb | "Bikin konten biasanya mahal. Saya pilih jalur gratis." |
| 11–19 s | Bukti 1 | Stat: **49** repo git · **4** aplikasi live di Vercel · **11** situs GitHub Pages | "Empat puluh sembilan repo. Empat aplikasi live. Sebelas situs jalan." |
| 19–26 s | Untuk publik | Kartu: Portal Pemdi Aceh Tengah — **52 OPD · 70 halaman** (live) | "Portal Pemdi Aceh Tengah: lima puluh dua OPD, tujuh puluh halaman." |
| 26–33 s | Cara kerja | 3 langkah: Tulis naskah → Render video di laptop → Tayang lewat penjadwal gratis | "Tulis naskah, render video di laptop, lalu tayang lewat penjadwal gratis." |
| 33–38 s | CTA | "Semua alatnya gratis." · Naskah → Render → Tayang · tombol Niumination | "Semua alatnya gratis. Ikuti prosesnya." |

Catatan desain: teks ditempatkan di **zona aman atas–tengah** (nomor scene watermark di kanan bawah, progress bar di dasar) sehingga tidak tertutup UI Instagram saat tayang.

## 2. Setiap angka di video sudah diverifikasi (18 Sep 2026)

| Klaim di video | Sumber verifikasi |
|---|---|
| 143 skill AI | Bank skill pusat: 143 `SKILL.md`, manifest 144 skill / 711 berkas sinkron (`up-eco`, 18 Sep 2026) |
| 49 repo git lokal | `find . -maxdepth 3 -name .git -type d` di `~/Desktop/Niumination` |
| 4 aplikasi live | `docs/registry/deployment-status.md`: pemdi-aceh-tengah, kms-spbe, kune-ya-com, virtual-assistance → ✅ HTTP 200 |
| 11 situs GitHub Pages | `deployment-status.md`: niu-dash, Niu-LKH, niu-private, Niu-Startpage, DiskominfoAT, Diskominfo-Web, SPBE-DevOps-Academy, Maze-3D, AuditTI-AT, zaryu.startpage, NiuHomePage |
| Portal Pemdi 52 OPD / 70 halaman | `deployment-status.md` + portal live HTTP 200 |
| 98 model AI (disebut di scene 5) | 9router lokal `localhost:20128` — 98 model terdaftar |

Harga pada scene "Masalah" (Rp 150rb / 300rb / 200rb) adalah **ilustrasi kisaran harga pasar alat**, bukan penawaran; kalau dipakai untuk klaim komersial, sebut sebagai contoh.

## 3. Toolchain gratis yang dipakai (semua tanpa biaya)

| Tahap | Alat | Lisensi/biaya |
|---|---|---|
| Penulisan naskah | `ghost` + penyuntingan manusia | skill ekosistem |
| Render video | **HyperFrames 0.8.30** (HTML→MP4, render lokal) | Apache-2.0, gratis |
| Animasi | **GSAP 3.14.2** — di-vendor ke `assets/gsap.min.js` (tidak mengambil CDN saat render) | gratis untuk pemakaian ini |
| Encode & mux audio | **ffmpeg** (lokal) | gratis |
| Narasi | `text_to_speech` Hermes dengan provider **edge** (suara `id-ID-ArdiNeural`) | gratis, tanpa API key berbayar |
| Komposisi audio | `ffmpeg` `adelay` + `amix` + `loudnorm` (target −16 LUFS) | gratis |

**Tidak dipakai:** stok video berbayar, musik berlisensi, Canva Pro, penjadwal berbayar, layanan render cloud.

## 4. Cara posting gratis (pilih satu)

1. **Penjadwal native Instagram** (gratis) — 25 post/hari, maksimum 30 hari ke depan, mendukung reels. Sumber: `help.instagram.com/439971288310029`.
2. **Buffer Free** — 3 kanal × 10 post terjadwal per kanal (isi ulang kapan saja). Sumber: `buffer.com/pricing`.
3. **Postiz self-hosted** — gratis penuh (AGPL-3.0) bila ingin tanpa batas kuota; butuh server/VM.

Catatan: video ini **sudah punya voice-over**, jadi saat menambahkan audio trending di aplikasi Instagram, turunkan volume audio tambahan (≈10–20%) agar narasi tetap terdengar.

## 5. Caption siap tempel

```
143 skill AI, 49 repo, 4 aplikasi live — semuanya dibangun dari satu laptop, tanpa langganan.

Yang bikin berat itu bukan idenya, tapi alatnya: editing, stok video, penjadwal. Semuanya ditagih bulanan.

Jadi saya susun ulang: naskah, render video, tayang — pakai alat gratis semua.

Hasilnya bukan cuma konten: ada layanan publik digital untuk 52 OPD di Aceh Tengah, 70 halaman, jalan sampai sekarang.

Simpan video ini kalau kamu mau jalur gratisnya juga.

#AcehTengah #Diskominfo #LayananPublik #SPBE #AI #GovTech #OpenSource #ContentCreator
```

## 6. Cara reproduksi / render ulang

```bash
cd ~/Downloads/niu-konten/reels-001
npx --no-install hyperframes lint
npx --no-install hyperframes render --resolution=portrait --fps=30 --quality=high \
  -o ~/Downloads/niu-konten/reels-001-final-silent.mp4
# mux narasi (delay mengikuti awal tiap scene)
cd ~/Downloads/niu-konten && ffmpeg -y -i vo/vo1.ogg -i vo/vo2.ogg -i vo/vo3.ogg -i vo/vo4.ogg \
  -i vo/vo5.ogg -i vo/vo6.ogg -filter_complex \
  "[0:a]adelay=600|600[a0];[1:a]adelay=5600|5600[a1];[2:a]adelay=11600|11600[a2];[3:a]adelay=19700|19700[a3];[4:a]adelay=26600|26600[a4];[5:a]adelay=33500|33500[a5];[a0][a1][a2][a3][a4][a5]amix=inputs=6:normalize=0:dropout_transition=0[mix];[mix]loudnorm=I=-16:TP=-1.5:LRA=11[out]" \
  -map "[out]" -t 38 -ar 48000 -ac 2 vo_mix.wav
ffmpeg -y -i reels-001-final-silent.mp4 -i vo_mix.wav -c:v copy -c:a aac -b:a 192k -shortest reels-001-final.mp4
```

Untuk hasil identik di mesin lain (font & Chrome terpatok), gunakan mode Docker: `--docker`.

## 7. Verifikasi hasil

| Pemeriksaan | Hasil |
|---|---|
| `hyperframes lint --verbose` | 0 error, 0 warning |
| Kodek & dimensi (`ffprobe`) | h264 1080×1920, 30/1 fps, + aac stereo |
| Durasi | 37,916 s (video 38,000 s) |
| Ukuran | 4.877.436 bita (4,9 MB) |
| Level audio (`volumedetect`) | mean −20,6 dB, max −4,5 dB, 3.639.936 sampel — tidak clipping |
| Frame QA visual | 6 frame kunci diperiksa manual (detik 2,5 / 7,5 / 13 / 21 / 28,5 / 35,5) — teks terbaca, tidak ada elemen terpotong |
| Integritas salinan | md5 video kerja = md5 berkas di `~/Movies/Posting - Instagram` (`bbc187c10d7df5bbf8b9e98c95583dc1`) |

## 8. Catatan & batasan

- **Lokasi kerja di luar ekosistem** mengikuti pitfall skill `creative/hyperframes`: proyek video tidak dibuat di dalam `~/Desktop/Niumination/`. Ekosistem tetap 15 folder standar.
- **MP4 tidak di-commit** ke repo (bukan artefak repo + ukuran). Berkas jadi ada di folder output pemilik; template HTML bisa dipindah ke lokasi resmi setelah pemilik memutuskan (skill bank/aset proyek memerlukan approval).
- **Belum ada musik latar**: audio berlisensi berbayar dihindari agar klaim "Rp 0" tetap jujur; audio trending ditambahkan dari aplikasi Instagram (gratis).
- **Rencana lanjutan:** Reels 02 (AI Tools Gratis) dan Reels 03 (GovTech/Pemdi) memakai template yang sama, hanya ganti scene 3–5.

---

*Produksi 18 Sep 2026; revisi VO v2 19 Sep 2026. Semua angka di video diverifikasi dari sumber ekosistem pada hari yang sama; perbarui bila angka ekosistem berubah.*
---

## 9. Revisi v2 (19 Sep 2026) — lapis delivery voice-over

Pemicu: penilaian pemilik bahwa VO reels v1 kalah dari VO video MATA. Investigasi atas paket pipeline MATA
(`labs/mata-aihackfest-2026/assets/media/pipeline/hermes-video-pipeline.zip`) menghasilkan tiga aturan yang
hilang di v1 dan dipakai ulang di v2.

### 9.1 Yang diperbaiki

| Lapis | Aturan (dari `VOICE.md` MATA) | v1 | v2 |
|---|---|---|---|
| Naskah | pass skill `ghost`: kalimat pendek berdiri sendiri, register lisan, buang basa-basi | kalimat sedang seragam | "Bikin konten itu mahal. Editing. Stok video. Penjadwal." |
| Angka | dieja kata, bukan digit | sudah (143 → "seratus empat puluh tiga") | dipertahankan |
| Jeda | hanya lewat tanda baca (edge-tts gratis tanpa SSML): titik = jeda penuh, em-dash = jeda dramatis | tanpa em-dash | em-dash dipakai di scene 1 & 4 |
| Delivery | **rate & pitch per adegan**, bukan satu setelan | satu setelan (default) | hook +10%/−2 Hz · masalah +6% · angka −4%/−3 Hz · publik +2% · cara +6% · penutup −4%/−2 Hz |

Setiap segmen VO diverifikasi **muat di jendela scene**-nya sebelum digabung (table di §9.3).

### 9.2 Berkas hasil v2

| Berkas | Isi |
|---|---|
| `~/Movies/Posting - Instagram/2026-09-18-reels-01-v2-vo-emma.mp4` | 38,000 s · 1080×1920 · 30 fps · H.264+AAC · 4.816.165 bita · VO `en-US-EmmaMultilingualNeural` |
| `~/Downloads/niu-konten/audisi/audisi_hook_3voice.mp3` | audisi: Emma → Andrew → Ardi (hook, rate +10%, pitch −2 Hz) |
| `~/Downloads/niu-konten/gen_vo2.sh` · `mix_vo2.sh` | skrip produksi v2 (ganti voice: `VOICE=<nama> bash gen_vo2.sh && bash mix_vo2.sh`) |

Pemilihan `Emma` berbasis kedekatan f0 dengan VO MATA terpilih (`R1.mp3` ≈ 176–210 Hz pada dua estimator
berbeda; Emma 188 Hz; Gadis 227 Hz; Andrew 110 Hz). Keputusan akhir tetap di telinga pemilik lewat audisi.

### 9.3 Jadwal VO v2 (semua muat di jendelanya)

| Scene | rate/pitch | mulai | durasi | akhir | jendela |
|---|---|---|---|---|---|
| S1 hook | +10% / −2 Hz | 0,50 s | 4,584 s | 5,08 s | 0–5 s |
| S2 masalah | +6% / 0 | 5,50 s | 5,352 s | 10,85 s | 5–11 s |
| S3 angka | −4% / −3 Hz | 11,60 s | 6,744 s | 18,34 s | 11–19 s |
| S4 publik | +2% / 0 | 19,70 s | 5,520 s | 25,22 s | 19–26 s |
| S5 cara | +6% / 0 | 26,60 s | 5,304 s | 31,90 s | 26–33 s |
| S6 penutup | −4% / −2 Hz | 33,60 s | 3,576 s | 37,18 s | 33–38 s |

### 9.4 Temuan forensik: VO MATA bukan edge-tts

Pemilik memastikan VO MATA adalah murni TTS (bukan rekaman manusia) dan bisa dipilih/disesuaikan otomatis.
Pemeriksaan berkas `audio/vo-manual/R1.mp3`:

- Properti: MP3 24 kHz mono **32 kbps**, encoder `Lavf59.27.100` (diproses ffmpeg)
- Durasi bicara (setelah trim sunyi) 11,267–11,546 s; f0 median 176–210 Hz (indikasi voice perempuan/tinggi)
- Korelasi gelombang terhadap kandidat edge-tts dengan **teks & rate identik**: Seraphina +10% **0,038** ·
  Ardi 0% 0,047 · Emma +10% 0,039 · Ava 0% 0,027 · Gadis +10% 0,035 · Thalita −5% 0,028 → semuanya ≈0
  (dua render TTS deterministik dari voice yang sama seharusnya berkorelasi >0,8)
- Uji gTTS (Google Translate, 24 kHz mono 32 kbps — kemiripan properti): korelasi 0,018 → juga bukan

Kesimpulan: **engine pembuat VO MATA bukan edge-tts dan bukan gTTS.** Kandidat yang belum bisa diuji dari Mac
ini karena sesi/VPS-nya tidak ada di `state.db` lokal: TTS yang tersedia lewat Hermes di VPS (mis. Gemini/OpenAI/
Kokoro) atau tool lain yang dipakai pemilik saat audisi. Pertanyaan pelacak sudah diajukan ke pemilik (§9.5).

### 9.5 Investigasi lanjutan (19 Sep 2026, dini hari) — hasil lengkap

Workspace arena.ai yang diunduh pemilik (`~/Downloads/hermes-video-pipeline.zip`, 66,8 MB, 94 berkas) diperiksa.
Isinya pipeline + `audio/vo-manual/` (17 berkas) + `video/mata_demo.mp4` + `mata_reels.mp4` + subtitle + QC.
**Tidak ada** `audio/voice-samples/`, tidak ada history/log/cache → jejak perintah pembuat VO tidak ikut terbawa.
`audio/vo-manual/R1.mp3` di zip md5-nya identik dengan salinan di media repo (`94d0e8662dfc9f173646ec8d07c05a59`).

**KOREKSI atas temuan sebelumnya — kesimpulan "voice berbeda per adegan" DITARIK.**
Temuan itu berasal dari estimator f0 saya sendiri, bukan dari berkasnya. Kontrol D: f0 di **dalam satu
berkas** berayun 45–56 Hz (S0 153,8 | 112,7 | 98,2 Hz; R1 160,0 | 200,0 | 205,1 Hz) — jadi variasi
antar-adegan tidak bisa disimpulkan dari f0 median. DTW 15,13 antara R1 dan S0 juga bukan bukti:
metrik DTW tidak punya skala kalibrasi jarak antar-teks.

**Yang bertahan, diukur dengan timbre (tempo-invariant) dan kontrol yang ketat:**

| Uji | Jarak | Arti |
|---|---|---|
| kontrol identik (berkas sama 2×) | 0,0000 | metode sah |
| kontrol **teks beda**, voice+rate sama (Ardi S0-teks vs Ardi S1-teks) | **0,0013** | efek teks sangat kecil |
| kontrol voice sama, rate beda 22% | 0,0002 | tahan tempo |
| antar-adegan MATA (R1↔R2/R3/R6, S0↔S1/S3/S9, S0↔R1, S3↔R3) | **0,0075–0,0151** | semua adegan konsisten satu voice |
| kandidat edge-tts terdekat (25 & 45 voice) | 0,0275 / 0,0428 | 2–3× lebih jauh dari variasi antar-adegan |
| Ardi (kandidat asli) vs S0 | 0,0465 | jauh |

Kesimpulan yang sah: **vo-manual MATA konsisten dengan satu voice**, dan voice itu **bukan** salah satu
dari 5 kandidat edge-tts yang dirender untuk audisi (hook_ardi/andrew/brian/florian/gadis).

**Metode & kontrol (dua metrik independen):**

| Kontrol | Hasil | Arti |
|---|---|---|
| DTW log-mel: voice+teks+rate sama, render ulang | 0,117 | metode sah |
| DTW log-mel: potongan berkas sama | 0,000 | metode sah |
| DTW log-mel: re-encode mp3 32 kbps | 1,046 | toleran kompresi |
| Korelasi gelombang: re-encode mp3 32 kbps | 0,968 | klaim lama (korelasi ≈0 = engine beda) tetap sah |
| Timbre (spektrum mel rata-rata): identik | 0,0000 | metrik tempo-invariant |
| Timbre: voice sama, rate beda 22% | 0,0002 | tahan perbedaan tempo |

**Semua kandidat yang sudah dieliminasi** (jarak jauh di atas ambang, dengan kontrol di atas):

| Kandidat | Jarak ke R1 |
|---|---|
| 45 voice edge-tts × 2 rate (98 render, sapuan penuh) | timbre terdekat `en-NZ-MollyNeural` 0,0428 vs kontrol 0,0000 |
| 25 voice edge-tts (metrik timbre, daftar lain) | terdekat `en-US-JennyNeural` 0,0275 |
| 14 voice edge-tts multilingual (DTW, teks humanized) | 9,95–14,42 |
| Teks `vo_lama` (pra-humanizer) × 4 voice | 14,26–18,57 |
| Pitch shift 0,70–2,00× pada 5 voice terbaik | minimum 10,25 |
| gTTS (3 domain: com, co.id, com.au) | 14,22–14,25 |
| Gemini TTS (probe lama) | **DITARIK** — probe lama tidak valid (PCM mentah didekode sbg wav). Lihat baris "Gemini" di bawah |
| Kokoro-82M via `hyperframes tts` | gagal: `kokoro-onnx` tidak terpasang |
| macOS `say` (Damayanti id_ID) | timbre 0,1009 · f0 238,8 Hz → bukan |

**Petunjuk terkuat yang tersisa:** mesin ini memiliki `FAL_KEY` di `~/.hermes/.env` — sandbox arena.ai
umumnya memberi akses fal.ai untuk tugas media, dan fal.ai menyediakan banyak model TTS.
Uji cepat ke fal.ai gagal karena akun terkunci (`403 {"detail":"User is locked. Reason: TOP_UP."}`),
jadi jalur ini tidak bisa diverifikasi dari Mac ini.

**Dua metrik, hasil sepakat (dua-duanya sudah dikontrol):**

| Metrik | Terdekat dari semua kandidat | Kontrol "identik" |
|---|---|---|
| DTW log-mel, 45 voice edge-tts × 2 rate (98 render) | `en-US-BrianMultilingualNeural` **9,99** | 0,117 |
| Timbre (spektrum mel rata-rata), 45 voice × 2 rate | `en-NZ-MollyNeural` **0,0428** | 0,0000 |
| Timbre, 25 voice tambahan | `en-US-JennyNeural` **0,0275** | 0,0000 |
| macOS `say` voice `Damayanti` (id_ID) | **0,1009** (paling jauh dari semua) | 0,0000 |

**Gemini TTS diuji ULANG dengan decode PCM yang benar** (petunjuk kunci: Gemini mengembalikan
`audio/L16;codec=pcm;rate=24000` — 24 kHz mono, persis properti berkas vo-manual MATA yang di-encode
ffmpeg `Lavf59.27.100`). Hasil pada teks S0: **Charon 0,0234** · Puck 0,0332 · Kore 0,0897 · Zephyr 0,0928
(pembanding: Ardi 0,0465 · kontrol teks-beda 0,0013). Kuota Gemini habis setelah 4 voice, 26 voice sisanya
tidak teruji. Charon/Puck **lebih dekat** daripada Ardi, tetapi durasinya 17,2–17,6 s vs `S0.mp3` 19,48 s —
belum cukup untuk menyimpulkan identik. A/B untuk telinga:
`~/Downloads/niu-konten/audisi2/ab_voice00_vs_kandidat.mp3` (MATA → Charon → Puck → Ardi).

**Kesimpulan final:** engine pembuat `vo-manual` MATA **bukan edge-tts (45 dari 324 voice diuji), bukan
gTTS, bukan macOS `say`**. Gemini TTS **belum bisa dinyatakan tereliminasi** — dua voice-nya (Charon, Puck)
justru kandidat terdekat yang pernah ditemukan, dengan format audio yang cocok. Tidak dapat diuji dari Mac
ini: fal.ai (akun terkunci `403 … TOP_UP`), Kokoro-82M (paket tidak terpasang), 26 voice Gemini (kuota),
dan mesin yang mungkin hanya ada di sandbox arena.ai.

**Klarifikasi dari `VOICE.md` lengkap (218 baris, `~/Downloads/VOICE.md`, sha256 `ebe793b8…c70ee5`)** —
berbeda dari `VOICE.md` di paket (8.282 bita): dokumen ini menyebut voice terpilih sebagai **"voice-00"**,
yaitu **narator pria tenang** hasil audisi yang disetujui pemilik, **bukan** salah satu dari 5 kandidat
edge-tts. Jadi tebakan "Ardi" tidak berlaku untuk VO MATA (Ardi = suara cadangan pipeline saja). Dokumen
juga menyebut `audio/uji-voice-00.mp3` dan `vo_bebas.py` — **keduanya tidak ada di mesin ini** (sudah
dicari di `~` dan `/tmp`), jadi bukti reproduksibilitas itu belum bisa diverifikasi.

### 9.7 JAWABAN DEFINITIF (19 Sep 2026) — paket `tts-hermes.zip`

Pemilik menyerahkan `~/Downloads/tts-hermes.zip` (21.769 bita, sha256 `783cb396…c196fa9`) berisi
`hermes-tts/` (6 berkas): `tts_hermes.py` · `suara.json` · `kamus_pelafalan.json` · `contoh_naskah.txt` ·
`pasang-hermes-tts.sh` · `INSTRUKSI-TTS-HERMES.md` (320 baris).

**Identitas voice-00 terjawab eksplisit** (`INSTRUKSI-TTS-HERMES.md` §0): voice-00 adalah **"mesin TTS Arena,
narator pria"** dan **tidak bisa dipanggil dari laptop**. Pengganti terdekat yang bisa dipakai sendiri =
**`id-ID-ArdiNeural`** via `edge-tts` (gratis, tanpa kunci) — di `suara.json` ia disebut
*"velvet paling dekat dengan voice-00"*. Jadi tebakan "Ardi" dari pemilik **benar sebagai pengganti**,
tetapi bukan voice-00 itu sendiri.

**Paket dijalankan & diverifikasi (bukan hanya dibaca):**

| Uji | Hasil |
|---|---|
| `--cek` pada `contoh_naskah.txt` | 7 potongan · 10 span · 2 bahasa · **bersih** (tanpa jaringan) |
| render teks S0 (`--keluar`) | 1 panggilan TTS (batas 200) · `S1.mp3` **44,1 kHz stereo 192 kbps** · 22,23 s · `durations.json` |
| routing bahasa `<id>` vs `<en>` | f0 **107,0 Hz vs 126,0 Hz** → dua suara berbeda, klaim terbukti |
| timbre Ardi(−12%/−2 Hz) vs `S0.mp3` (voice-00) | **0,0494** vs kontrol teks-beda 0,0013 → **bukan voice-00**, sesuai klaim dokumen |
| `~/piper-voices/` | belum ada (model offline belum diunduh) |

**Fitur yang membuat paket ini bernilai (dan tidak ada di skrip reels saya):**
- **Eja angka otomatis** (`Rp 3.117.360.000` → "tiga miliar seratus tujuh belas juta tiga ratus enam puluh ribu rupiah")
- **Kamus akronim** 55 entri (SKPD→"es ka pe de", KPK, BPKP, D4→"de empat", IDwebhost) — bisa ditambah tanpa ubah skrip
- **Tag bahasa** `<en>…</en>` sebaris + blok `@en` → istilah Inggris pakai suara Inggris (Andrew), Indonesia pakai Ardi
- **Pengaman biaya**: `--maks-panggilan 200`, berkas yang ada dilewati, kunci `.tts.lock`, timeout 60 s, retry maks 2×
- **Standar keluaran identik** `tts.py` (44,1 kHz stereo 192 kbps, lead 0,60 s, tail 0,80 s, `durations.json`) → langsung bisa masuk `audio/vo-manual/`
- Tiga mesin: `edge` (gratis) · `piper` (offline penuh) · `azure` (SSML penuh, butuh kunci)

**Catatan berkas acuan:** dokumen §11 menyebut `../audio/uji-voice-00.mp3` — berkas itu **tidak ada di zip ini**
maupun di mesin (sudah dicari). Jadi A/B terhadap voice-00 asli tetap memakai `S0.mp3`/`R1.mp3` dari paket MATA.

**Jalur yang tersisa (urut biaya):**
1. Task arena.ai yang menghasilkan `audio/vo-manual/` (atau `audio/uji-voice-00.mp3`) — satu-satunya cara mereproduksi persis.
2. Pilih dari audisi: `audisi2/ab_voice00_vs_kandidat.mp3` (MATA → Charon → Puck → Ardi) atau `audisi2/audisi_timbre_4voice.mp3` (Jenny/Seraphina/Brian/Emma) → render ulang.
3. Pakai reels v2/v3/v4 yang sudah jadi (`…-v2-vo-emma.mp4`, `…-v3-vo-ardi.mp4`,
   `…-v4-vo-ardi-ttshermes.mp4`) — lapis delivery MATA sudah diterapkan; v4 memakai mesin paket.

**Usul adopsi ke bank skill (MENUNGGU APPROVAL — belum disentuh):** jadikan `hermes-tts` mesin VO
standar di skill `skills/creative/free-tier-reels`, dengan `gen_vo3.sh` sebagai jembatan delivery
per-adegan. Alasan: paket ini memberi eja-angka otomatis, kamus akronim 55 entri, routing bahasa
`<en>…</en>`, dan pengaman biaya — semuanya tidak ada di skrip reels v1/v2.

### 9.8 Produksi v4 — mesin `tts_hermes.py` + delivery per adegan (dijalankan)

Keputusan pemilik ("ya lanjutkan"): pakai paket `tts-hermes` sebagai mesin VO produksi.

**Celah yang harus dijembatani (temuan saya):** `tts_hermes.py` mengatur rate/pitch **per bahasa**
(`suara.json` → `edge.id`), sedangkan lapis delivery MATA butuh **per adegan** (`VOICE.md` §2c).
Paket tidak punya opsi CLI untuk rate/pitch per adegan.

**Jembatan tanpa mengubah kode paket:** `gen_vo3.sh` (baru, `~/Downloads/niu-konten/`) menulis
`suara.json` sementara berisi rate/pitch adegan itu, memanggil `tts_hermes.py`, lalu memulihkan
`suara.json.orig` lewat `trap EXIT`. Jadi mesin paket dipakai apa adanya (dapat eja-angka otomatis +
kamus akronim), sementara delivery tetap per adegan.

**Temuan implementasi:**
- `baca_naskah()` **mengabaikan label potongan** (`S1`/`R3`) dan selalu menamai keluaran satu-blok
  `S1.mp3` → skrip harus me-rename hasilnya sendiri.
- `--cek` (gratis, tanpa jaringan) adalah satu-satunya cara melihat akronim kamus mana yang terpakai;
  mode render tidak mencetaknya.
- `--tanpa-jeda` dipakai supaya lead/tail tidak dobel dengan `adelay` di tahap mux.
- Kamus ditambah 3 entri: `OPD` → "o pe de" · `SPBE` → "es pe be e" · `APBD` → "a pe be de"
  (sebelumnya 52 entri; `OPD` belum ada padahal dipakai di naskah reels).

**Hasil v4 — enam adegan semua muat jendelanya:**

| Scene | rate/pitch | durasi | akhir | jendela | kamus aktif |
|---|---|---|---|---|---|
| S1 hook | +10% / −2 Hz | 4,320 s | 4,82 s | 5 s | `AI` → "ei" |
| S2 masalah | +8% / 0 | 4,776 s | 10,28 s | 6 s | — |
| S3 angka | −4% / −3 Hz | 7,152 s | 18,75 s | 8 s | — |
| S4 publik | +2% / 0 | 5,088 s | 24,79 s | 7 s | `OPD` → "o pe de" |
| S5 cara | +6% / 0 | 6,216 s | 32,82 s | 7 s | — |
| S6 penutup | −4% / −2 Hz | 4,344 s | 37,94 s | 5 s | — |

Semua keluaran **44,1 kHz · stereo · 192 kbps** (standar paket, identik `tts.py`). Video:
`~/Movies/Posting - Instagram/2026-09-18-reels-01-v4-vo-ardi-ttshermes.mp4` — 38,000 s · 1080×1920 ·
30 fps · H.264+AAC · 4.733.534 bita · md5 `097069330dff7eeee385e8d82e994a67` · audio mean −20,3 dB /
max −3,2 dB.

**Verifikasi audio benar dari mesin baru (bukan sisa run lama).** Run pertama memakai `vo2_mix.wav`
(Emma) yang tertinggal, jadi hasilnya salah; setelah `vo2_mix.wav` → `vo3_mix.wav` dan render ulang,
dibuktikan dengan korelasi gelombang:

| Uji | Korelasi |
|---|---|
| video v4 segmen hook vs `vo3/S1.mp3` (Ardi via tts_hermes) | **0,9991** |
| video v4 segmen hook vs `vo2/S1.mp3` (Emma) | 0,1569 |
| kontrol beda-voice `vo3/S1` vs `vo2/S1` | 0,1671 |
| kontrol segmen S2 vs `vo3/S2` | 0,9998 |

Catatan metode: timbre **tidak** cukup memisahkan di sini (0,0047 vs 0,0022) dan f0 median **ambigu**
(113,6 Hz di antara 105,3 dan 120,3) — korelasi gelombang yang memutuskan. Estimator f0 divalidasi
ulang pada nada sintetis (106→106,0 · 188→188,2 Hz).

### 9.6 Tindak lanjut

1. Pemilik menyebutkan engine/alat yang dipakai untuk `audio/vo-manual/*.mp3` → reproduce persis (kalau gratis).
2. Bila tidak reproduktif: v2 (Emma) dipakai apa adanya, atau pilih voice lain dari audisi 3 kandidat.
3. Usul (menunggu approval): tambahkan **lapis delivery** ini ke skill `free-tier-reels` di bank skill —
   aturan naskah `ghost`, angka dieja kata, jeda tanda baca, rate/pitch per adegan, langkah audisi voice.

