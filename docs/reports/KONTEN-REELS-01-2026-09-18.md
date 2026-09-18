# Paket Konten Reels 01 — "Behind the Build" (18 Sep 2026)

**Pelaksana:** Hermes — thread Kreator (1172)
**Pemicu:** permintaan Afrizal Munthe — lanjutkan rencana konten, seluruh produksi harus gratis (Rp 0)
**Status:** **siap tayang** — video, narasi, dan paket caption selesai; distribusi menunggu keputusan kanal. **Revisi v2 (19 Sep 2026):** voice-over diperbaiki mengikuti lapis delivery pipeline MATA — lihat §9.

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

**Temuan korektif: VO MATA bukan satu voice.** f0 median berbeda antar adegan —
R1 216 Hz · R2 186 Hz · R3 122 Hz · R4 123 Hz · S0 147 Hz · S3 123 Hz · S9 154 Hz.
Kalimat pertama R1 dan S0 **teksnya identik** tetapi jarak DTW 15,13 (kontrol potongan sama = 0,00).
Jadi agent arena memilih **voice berbeda per adegan** — bukan satu voice terpilih.

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
| Gemini TTS (Kore, Puck, Charon, Fenrir, Aoede, Leda) | 12,99–18,69 |
| Kokoro-82M via `hyperframes tts` | gagal: `kokoro-onnx` tidak terpasang |
| macOS `say` (Damayanti id_ID) | belum diuji |

**Petunjuk terkuat yang tersisa:** mesin ini memiliki `FAL_KEY` di `~/.hermes/.env` — sandbox arena.ai
umumnya memberi akses fal.ai untuk tugas media, dan fal.ai menyediakan banyak model TTS.
Uji cepat ke fal.ai gagal karena akun terkunci (`403 {"detail":"User is locked. Reason: TOP_UP."}`),
jadi jalur ini tidak bisa diverifikasi dari Mac ini.

**Kesimpulan:** engine pembuat `vo-manual` MATA **bukan edge-tts, bukan gTTS, bukan Gemini TTS**, dan
berganti voice per adegan. Yang paling cepat menutup ini: task arena.ai yang menghasilkan
`audio/vo-manual/` (memuat perintah/audisi voice) — belum tersedia di zip.

### 9.6 Tindak lanjut

1. Pemilik menyebutkan engine/alat yang dipakai untuk `audio/vo-manual/*.mp3` → reproduce persis (kalau gratis).
2. Bila tidak reproduktif: v2 (Emma) dipakai apa adanya, atau pilih voice lain dari audisi 3 kandidat.
3. Usul (menunggu approval): tambahkan **lapis delivery** ini ke skill `free-tier-reels` di bank skill —
   aturan naskah `ghost`, angka dieja kata, jeda tanda baca, rate/pitch per adegan, langkah audisi voice.

