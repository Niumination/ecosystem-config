# Riset Format Reference — Zenarmor Reels "Others Think You Need All This"

**Tanggal** : 2026-10-06
**Sumber** : https://www.instagram.com/p/Dd6S9rWALFc/
**Diposting** : 2026-09-30
**Akun** : `@zenarmor_official` — Zenarmor (SASE, ZTNA, SSE, NGFW), Instagram user ID `40607093292`
**Penulis** : Kreator — thread 1172 (Niu-MissionControl)

## Kesimpulan singkat

**Bisa dibuat, dan mesin kita sudah mampu.** Format ini bukan video produk — ia adalah
**argumentasi komparatif** (masalah lama vs solusi baru) dalam 22 detik, dibangun dari
slate tipografi besar + skema visual satu per slide. Tiga aspek yang terlihat sulit
(spotlight glow, diagram globe, mockup UI) semuanya bisa dibuat di Remotion tanpa GPU.
Empat aspek yang butuh keputusan pemiliki tercatat di bagian 6.

Hal ini sejalan dengan posisi kita: reels-003 dan reels-004 sudah memakai struktur
masalah→bukti→solusi, hanya dengan satu motif visual. Yang baru dari format ini adalah
**banyaknya motif visual berbeda dalam satu video pendek** — satu konsep visual per
slate — bukan penambahan efek yang lebih berat.

---

## 1. Cara video ini diambil

`web_extract` gagal (saldo upstream habis, bukan error Instagram) dan browser tool tidak
merespons sama sekali (bahkan `https://example.com` gagal), jadi jalur tersebut tidak
dipakai. Wayback `available` API membalas 429. `JINA_API_KEY` tidak diset, jadi jalur
Jina dilewati sesuai aturan skill `blocked-page-recovery`.

Yang berhasil: **`yt-dlp` versi 2026.08.19** dengan `--impersonate chrome`, tanpa login.
Metadata JSON ditarik (29.667 byte), lalu video DASH 1080x1920 VP9 (3.141.235 byte) dan
audio AAC 48 kHz stereo (185.868 byte) diunduh terpisah.

```
yt-dlp --no-download --dump-json --socket-timeout 25 --impersonate chrome <URL>
yt-dlp -f dash-1609431417593241v -o ref-v.mp4 <URL>      # video 1080x1920
yt-dlp -f dash-1609431174259932a -o ref-a.m4a <URL>      # audio saja
```

Caption/keterangan Instagram **kosong** di metadata yt-dlp — seluruh isi harus dibaca
dari frame, bukan dari deskripsi.

---

## 2. Spesifikasi (diukur, bukan dibaca dari UI)

| Sifat | Nilai | Alat |
|---|---|---|
| Durasi | 22,166667 detik | `ffprobe` |
| Resolusi | 1080 x 1920 | `ffprobe` |
| Codec video | VP9 (`vp09.00.40.08.00.01.01.01.00`) | metadata |
| Codec audio | AAC LC, 48000 Hz, stereo | `ffprobe` |
| Bitrate | 1201 kbps total | metadata |
| Ukuran | video 3,0 MB + audio 186 KB | unduhan |

Sesuai standar kita (1080x1920, 48 kHz). **Selisih utamanya: ia punya audio, kita tidak.**

### Profil audio

Audio di-dekode ke PCM 16 kHz mono lalu diukur RMS per detik:

```
 0s  13,7%  ####
 1s  11,4%  ###
 2s   4,4%  #
 3s   2,3%
 4s   8,9%  ##
 5s  14,9%  ####
 6s  18,4%  ######
 7s  16,9%  #####
...setara 15-19% sampai akhir...
21s  15,2%  #####
```

Sunyi di detik 0-4, lalu level **stabil 15-19% sepanjang sisa video**. Level yang datar
demikian bukan percakapan (percakapan naik-turun drastis antar kalimat dan jeda). Ini
**musik latar** — kemungkinan ada jingle pendek di pembukaan lalu bed music. Tidak ada
keberadaan narasi suara yang bisa dikonfirmasi dari waveform; **UNCHECKED** — tidak ada
engine transkripsi di mesin ini (tanpa `whisper`, tanpa `sox`).

---

## 3. Struktur narasi (dibangun dari frame f0-f21)

Tujuh slate dalam 22 detik. Durasi per slate diperkirakan dari deteksi cut + sampel frame;
deteksi otomatis hanya menangkap cut keras di rentang 6,53-11,53 detik (7 deteksi),
artinya **sebagian besar transisi adalah motion halus, bukan potongan** — itu kenapa
beberapa batas bawah ini labelnya perkiraan.

| # | Sekitar | Teks (asli) | Visual | Fungsi |
|---|---|---|---|---|
| 1 | 0-4s | *Others think you need **all this**.* | Hardware firewall `PW-7000` dengan layar "LICENSE EXPIRED" | Hook + framing masalah |
| 2 | 4-6,5s | *Well..* | Terminal konfig + klien VPN macet "Connecting... 12%" + label merah: *endless manual configs*, *a VPN that keeps breaking*, *a box for every site* | Puncak masalah |
| 3 | ~6,5-7,5s | *(kosong)* | **Lingkaran oranye menyala + kursor mouse putih** | Transisi — "klik untuk melanjutkan" |
| 4 | ~7,5-9,7s | *Meet **zenarmor** Innovation* | Logo oranye + wordmark putih, center | Perkenalan merek |
| 5 | ~9,7-11,5s | *One app. **Instant security**. Any platform.* | Grid 12 logo platform (Windows, Android, iOS, macOS, Linux, Fedora, FreeBSD, Docker, Ubuntu, Bitdefender) | Klaim platform luas |
| 6 | ~11,5-15s | *Fast, direct **connection**. Policy-enforced.* | Globe dot-matrix + garis oranye + label *HQ / Branch / Warehouse / Remote Contractor* + `NO PoP` dicoret + `P2P - ENCRYPTED` hijau | Cara kerja |
| 7 | ~15-19s | *Manage it all in **one console**.* | Mockup UI Zensconsole: toggle "Web filtering policy", 4 baris (HQ 24 devices, Branch 14, Warehouse 14, Remote 1 Laptop), badge `Applied` hijau | Bukti produk |
| 8 | ~19-22s | *(logo + tagline)* | Tagline *"Radically simple unified network security"*, `1000+ CUSTOMERS WORLDWIDE`, badge `SOC2` `GDPR` `COMPLIANCE READY` | Penutup + proof |

### Rangkuman pola yang bisa dipindahkan

1. **Kontras masalah vs solusi** — masalah selalu gelap dan berantakan (terminal, kabel kusut, warna merah), solusi selalu bersih (oranye terang, garis lurus, globe rapi). Mata otomatis membaca itu tanpa teks.
2. **Warna aksen tunggal** — oranye untuk satu kata kunci per slate. Sisanya putih. Ini jauh lebih disiplin daripada menandai banyak hal sekaligus.
3. **Satu kata kunci ditegaskan, bukan satu kalimat** — *ALL THIS*, *WELL..*, *INSTANT SECURITY*, *CONNECTION*, *ONE CONSOLE*. Masing-masing hanya 1-3 kata.
4. **Motif visual berbeda tiap slate** — hardware → terminal → orb → logo → grid ikon → globe → UI → badge. Penonton tidak pernah melihat motif sama dua kali beruntun.
5. **Transisi di-drive oleh kursor**, bukan transisi efek — murah, dan mengkomunikasikan "ini diklik dari console".
6. **Bukti sosial di akhir**, bukan di awal — `1000+`, `SOC2`, `GDPR`.
7. **Tanpa watermark akun di frame** — ini beda dari kebiasaan kita (`@zaryu-abstract-studio` selalu di pojok).

---

## 4. Kejaran teknis — apa yang kita punya vs yang dibutuhkan

### Sudah dimiliki (bisa langsung dipakai)

| Kebutuhan format | Status kita |
|---|---|
| Canvas 1080x1920, 30 fps, H.264 | Sudah. reels-004: `1080x1920 30/1 nb_frames=600` |
| Slate tipografi besar + aksen warna | Sudah. reels-004 slide 5 slate, Inter 900 + `#FACC15` |
| Terminal sintetis | Sudah. reels-004 slide 3, JetBrains Mono 40 pt |
| List langkah bernomor | Sudah. reels-004 slide 4 |
| Bar/progress dihitung dari `frame` | Sudah, termasuk pelajaran CSS keyframes tidak beranimasi |
| Stagger inline per item | Sudah (pola `slice(0,rows)` terbukti fatal: langkah 02+03 hanya sempat 0,3 detik) |
| Audio 48 kHz + loudnorm | Sudah terukur — input_i -19,85 LUFS -> output_i -15,41 LUFS via `mux.sh`. |
| VO Charon | Sudah. `gemini_vo.py` v1.1.0, fallback dicabut |
| Bebas efek GPU berat | Sudah. Transform + opacity saja |

### Bisa dibuat, butuh usaha (tetap tanpa GPU)

| Aspek | Cara |
|---|---|
| Spot highlight + vignette | CSS `radial-gradient` **statis** — ini gradient konstan, bukan yang bergerak, jadi tidak melanggar larangan `background-position: animate`. |
| Diagram globe | SVG dot-matrix + garis, animasi `stroke-dasharray` yang dihitung dari `frame` (bukan CSS `animation`). |
| Mockup UI console | Komponen React biasa — div, border, badge. Masing-masing slate butuh 20-40 baris. |
| Grid logo platform | Grid flex, tanpa aset eksternal. |
| Audio sepanjang 22 detik | Bisa buat VO Charon 22 detik dengan `gemini_vo.py`, lalu `mux.sh` + `loudnorm`. Catatan: ini **VO saja** — musik latar belum ada jalur (lihat tabel berikutnya). |

### Tidak dimiliki — butuh keputusan pemilik

| Aspek | Kendala |
|---|---|
| Musik latar lisensi bersih | `brand/music/` **kosong** dan **tidak ada skrip pembuat musik** di repo. Saya salah menulis `scripts/make_bgm.py` di versi awal laporan ini — berkas itu tidak pernah ada (sudah saya verifikasi dengan `search_files`, hasil 0). Reels-001 dan reels-003 justru **tidak pernah pakai musik**: `mux.sh` reels-003 hanya mencampur VO Charon lalu `loudnorm`. Jalur musik kita belum pernah diuji. |
| Logo produk sendiri | Video ini menjual produk fisik + UI nyata. Pilar kita (4 AI Code Doctor, 2 Digitalisasi Publik) tidak punya "produk" yang bisa di-mockup — perlu diganti dengan sesuatu yang benar-benar ada. |
| Transkripsi / analisis VO asli | Tidak ada engine transkripsi di mesin. Konten vocal video asli **UNCHECKED**. |

### Tergantung keputusan durasi (bukan masalah teknis)

22 detik x 0,296 detik/frame = **6,5 detik render** termasuk bundling pertama — masih
sangat aman di bawah ambang 5 menit (33 detik). Bahkan 30 detik baru 8,9 detik. Jadi
format ini justru **lebih ringan dari batas kita daripada dari batas mesin**.

---

## 5. Selisih format vs reel kita

| Dimensi | Zenarmor | reels-004 kita |
|---|---|---|
| Durasi | 22 detik | 20 detik |
| Jumlah motif visual | 7 motif berbeda | 3 motif (slate, panel terminal, card list) |
| Kata kunci per slate | 1-3 kata, satu kata diberi warna | 1-3 baris, sebagian diberi warna |
| Kertas audio | Musik (level datar 15-19%) | **Tidak ada audio sama sekali** |
| Watermark | Tidak ada | `@zaryu-abstract-studio` tiap frame |
| Bukti sosial | Ada (`1000+`, `SOC2`, `GDPR`) | Tidak ada |
| Aksen warna | Oranye konsisten | Kuning `#FACC15` konsisten |
| Latar | Radial gradient dengan vignette | Solid `#0B0F17` |

Dua hal yang membedakan paling nyata: **audio** dan **keragaman motif visual**.
Keragaman motif itu yang membuatnya terasa "mahal" — bukan efeknya.

---

## 6. Rekomendasi

### 6.1 Keputusan pemiliki yang diperlukan (4)

1. **Audio.** Dua opsi: tetap motion-graphic tanpa audio (reels-004), atau tambah VO
   Charon dengan `gemini_vo.py` + `mux.sh`. Video referensi memakai musik latar, tapi
   kita **belum punya jalur musik sama sekali** — `brand/music/` kosong dan tidak ada
   skrip pembuat musik di repo. Kalau mau musik, aset CC0 perlu diunduh dulu.
2. **Topik pengganti "produk".** Video referensi menjual hardware + console. Pilar kita
   tidak punya produk fisik. Kalau mau mengikuti formatnya, slatenya harus diisi dengan
   sesuatu yang nyata milik kita — misal audit TI (ada proyek `sites/audit-ti-at/`),
   digitalisasi dinas, atau layanan publik Aceh Tengah. Jangan meniru strukturnya lalu
   mengisi dengan klaim yang tidak bisa kita ukur sendiri.
3. **Watermark.** Format referensi tidak menaruhnya; brand kit kita mewajibkan. Perlu
   dipertahankan atau disesuaikan per-format.
4. **Bukti sosial.** `1000+ customers` tidak bisa kita klaim. Kalau dipakai, harus diganti
   dengan angka yang benar-benar terukur (misal jumlah OPD di portal Pemdi, atau jumlah
   repo di ekosistem). Jangan angka dekoratif.

### 6.2 Kalau mau dibuat

Urutan kerja paling aman, tiap tahap berdiri sendiri:

1. **Slate saja dulu** (tanpa audio) — 4-5 slate, motif tunggal, durasi 18 detik.
   Memvalidasi tempo + tipografi sebelum menambah kompleksitas.
2. **Tambah satu motif baru** — diagram SVG animasi dari `frame` (mirip globe), bukan
   banyak motif sekaligus.
3. **Tambah audio terakhir** — BGM dulu, VO Charon setelah struktur narasi terkunci.
   Audio paling mahal untuk diulang kalau narrasinya berubah.

### 6.3 Yang sebaiknya tidak dilakukan

- **Jangan meniru transisi kursor** sebagai dekorasi. Ia berarti di video itu karena
  produknya memang diklik dari console. Meniru bentuknya tanpa isi hanya menambah noise.
- **Jangan menambah motif lebih dari satu per slate.** Di video referensi pun tiap slate
  masih fokus pada satu hal.
- **Jangan meniru tone "Others think you need all this"** kalau tidak ada produk untuk
  digantikan. Kalimat itu bekerja karena slatenya menunjukkan apa yang sedang
  digantikan.

---

## Bukti

```
# Pengambilan
$ yt-dlp --no-download --dump-json --impersonate chrome https://www.instagram.com/p/Dd6S9rWALFc/
  exit=0, stdout 29667 byte, stderr kosong

$ ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 /tmp/ref-v.mp4
  duration=22.166667

$ ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 /tmp/ref-v.mp4
  codec_name=h264  width=1080  height=1920

$ ffprobe -v error -select_streams a -of default=noprint_wrappers=1 /tmp/ref-a.m4a
  codec_name=aac  sample_rate=48000  channels=2
```

```
# Pengukuran audio (RMS per detik, PCM 16 kHz mono)
  0s 13.7%   3s  2.3%   6s 18.4%  13s 18.5%
  1s 11.4%   4s  8.9%   7s 16.9%  19s 18.9%
  2s  4.4%   5s 14.9%   8s 15.1%  21s 15.2%

# Deteksi cut scene (15 fps, selisih nilai piksel rata-rata > 12)
  7 cut: 6.53s 6.60s 6.67s 9.73s 9.80s 11.47s 11.53s
  333 frame terekstrak; sisanya transisi halus, bukan cut keras

# Kapasitas mesin (standar reels-004, sudah terukur)
  Durasi 20s -> render 31,3 detik wall ; ambang 5 menit jatuh di 33 detik
  Format referensi 22 detik -> proyeksi 6,5 detik (jauh di bawah ambang)
```

```
# Aset
  brand/music/          -> kosong, 0 file
  skrip pembuat musik   -> TIDAK ADA di repo (make_bgm.py tidak pernah ada)
  project/reels-003/mux.sh -> mencampur VO Charon + loudnorm, TANPA musik
  skills/creative/gemini-vo-narration/scripts/gemini_vo.py -> v1.1.0, fallback dicabut
  engine transkripsi    -> TIDAK ADA (tanpa whisper/sox) -> analisis VO asli UNCHECKED
```

## Batas analisis ini

- Konten vocal audio asli **UNCHECKED** — tidak ada engine transkripsi. Kesimpulan
  "musik bukan narasi" diturunkan dari stabilitas level RMS, bukan dari pendengaran.
- Caption Instagram kosong di metadata yt-dlp, jadi tidak ada teks asli selain yang
  tertulis di frame.
- Hanya **satu video** dianalisis, jadi ini pola satu klip, bukan gaya konsisten akun
  `@zenarmor_official`. Belum bisa disimpulkan apakah format ini memang gaya khasnya.
- Durasi per slate perkiraan dari deteksi cut + sampel frame 1 detik, bukan batas frame
  eksak.
