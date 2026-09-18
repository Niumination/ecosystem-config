# Paket Konten Reels 01 — "Behind the Build" (18 Sep 2026)

**Pelaksana:** Hermes — thread Kreator (1172)
**Pemicu:** permintaan Afrizal Munthe — lanjutkan rencana konten, seluruh produksi harus gratis (Rp 0)
**Status:** **siap tayang** — video, narasi, dan paket caption selesai; distribusi menunggu keputusan kanal

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

*Produksi 18 Sep 2026. Semua angka di video diverifikasi dari sumber ekosistem pada hari yang sama; perbarui bila angka ekosistem berubah.*
