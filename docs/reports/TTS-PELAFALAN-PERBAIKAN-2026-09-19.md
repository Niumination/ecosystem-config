# Perbaikan Pelafalan TTS — 19 Sep 2026

**Status:** selesai, terverifikasi
**Mesin:** `hermes-tts` (`tts_hermes.py` + modul baru `pelafalan_tambahan.py`)
**Lokasi kerja:** `~/Downloads/niu-konten/hermes-tts/` (di luar repo ekosistem, sesuai aturan)
**Uji:** `uji_emas_pelafalan.py` — **28/28 lulus** (sebelum: 22/27)

---

## 1 · Yang diminta

Memperbaiki pelafalan TTS agar tepat untuk **singkatan, akronim, campuran bahasa, dan yang lainnya**.

## 2 · Diagnosis — apa yang sebenarnya salah

Rekon memakai fungsi asli dari `tts_hermes.py` menemukan **13 dari 28 kasus bermasalah**, dan
beberapa di antaranya **kerusakan serius**, bukan sekadar belum diatur:

| Masukan | Yang diucapkan (SEBELUM) | Sifat |
|---|---|---|
| `laporan skpd ke bpkp` | `laporan skpd ke bpkp` | **tidak diganti** — kamus peka huruf besar |
| `0812-3456-7890` | `delapan ratus dua belas-tiga ribu empat ratus lima puluh enam-...` | **salah total** |
| `19/09/2026` | `sembilan belas/sembilan/dua ribu dua puluh enam` | garis miring tersisa |
| `v4.1.0` | `v4.satu.nol` | angka 4 tersisa, titik liar |
| `09:30` | `sembilan:tiga puluh` | titik dua tersisa |
| `5-10` | `lima-sepuluh` | tanda hubung tersisa |
| `A & B (urgent)` | `A & B (urgent)` | simbol tidak diucapkan |
| `dll., dgn, sbb.` | tidak diganti | singkatan tak dikenal |
| `admin@niumination.web.id` | `@` tersisa | email tidak ditangani |
| `10 GB` | `GB` tetap huruf | satuan tak ada di kamus |

**Akar masalah:** `pakai_kamus()` memakai regex **peka huruf besar**, dan tidak ada lapis
normalisasi untuk format khusus (tanggal/jam/versi/telepon/URL/email/rentang/simbol).

## 3 · Yang diperbaiki

### 3.1 Modul baru `pelafalan_tambahan.py`

Menyediakan `normalisasi()` + `rapikan()` + `tag_asing()`, dipanggil dari `tts_hermes.siapkan()`
dan `baca_naskah()`. Prinsipnya: **keluaran bukan kalimat jadi**, melainkan teks yang
diserahkan ke `eja_angka_*` yang sudah ada — jadi tidak ada logika pengeja angka yang diduplikasi.

Cakupan: tanggal · jam · versi · nomor telepon/NIK (digit demi digit) · rentang · ordinal
(`ke-3` → `ketiga`) · email · URL · ekstensi berkas · singkatan umum · simbol (`& ( ) = + / @ "`)
· tag bahasa otomatis untuk nama merek/istilah Inggris.

### 3.2 Kamus diperluas 52 → 128 entri

Ditambah: satuan (KB/MB/GB/TB/GHz/kWh/kg/km/°C) · singkatan dinas (ASN, NIK, NPWP, KTP, SAKIP,
WTP, PAD, DAU, BLUD, PDAM, DPRD, BPS, BKN) · istilah teknis (HTML, CSS, URL, DNS, VPN, FTP, IoT)
· wilayah (Gampong, Mukim, Pemkab, Sekda) · zona waktu (WIB/WITA/WIT).

### 3.3 Perkecualian yang saya tambahkan (penting)

Pencocokan jadi **tanpa peka huruf**, supaya `skpd` ikut diganti seperti `SKPD`. Tapi itu
menimbulkan risiko: `API` → "a pe i" padahal **`api` = fire**. Saya ukur dulu dengan korpus
nyata (120 berkas ekosistem), lalu buat daftar `_peka_huruf_besar`:

```
API  AI  PA  RAM  RT  RW  DAK  LAN  TIK  PAD
```

Entri di daftar itu dicocokkan **persis huruf besar**. Sebaliknya `PDF/CSV/JSON/SQL/SSH/GPU/CPU`
sengaja **tidak** masuk daftar, supaya `laporan.pdf` dan `data.csv` ikut dieja benar.

### 3.4 Tiga bug pada paket yang ikut diperbaiki

1. `baca_naskah()` mengabaikan label (`S1`/`R3`) dan selalu menamai keluaran `S1.mp3`.
2. Pola angka menelan **titik akhir kalimat** → jeda penutup hilang pada TTS.
3. `tag_asing()` membuat tag bersarang bila naskah sudah memakai `<en>…</en>`.

## 4 · Verifikasi

### 4.1 Uji emas (harapan tulisan tangan, bukan pemeriksa otomatis)

`uji_emas_pelafalan.py` memuat 28 kasus dengan **harapan eksplisit** lalu membandingkan
teks yang benar-benar dikirim ke mesin TTS. **28 lulus · 0 gagal** (sebelum: 22 lulus · 5 gagal).

> Catatan kejujuran: harness pertama saya menyatakan "26/33 bersih" padahal rekon memperlihatkan
> kerusakan nyata — karena pemeriksanya memakai logika yang sama dengan yang diperiksa.
> Harness itu saya buang dan ganti uji emas.

### 4.2 Regresi ke naskah nyata produksi

33 naskah MATA (8 menit + reels, versi humanized **dan** pra-humanizer) dijalankan lewat
jalur lama vs baru. **29 tidak berubah**, 4 berubah dan **semuanya perbaikan**:

| Naskah | Sebelum | Sesudah |
|---|---|---|
| MATA-S1-lama | `dua puluh empat/tujuh` | `dua puluh empat per tujuh` |
| MATA-S6-lama | `'monitor offline, coba lagi'` | `monitor offline, coba lagi` |
| MATA-S8-lama | `'indikasi', bukan 'bersalah'` | `indikasi, bukan bersalah` |
| MATA-S9 | `cukup... diawasi` | `cukup … diawasi` |

Satu **regresi yang saya perkenalkan sendiri** sempat lolos: elipsis `...` runtuh jadi `.`
sehingga jeda dramatis hilang. Sudah diperbaiki (elipsis dipertahankan).

### 4.3 Verifikasi audio — perbaikan benar-benar terdengar

Korelasi gelombang antara rekaman "sebelum" dan "sesudah" per kasus:

| Kasus | Korelasi | Δ durasi |
|---|---|---|
| kontrol (berkas sama, render 2×) | **0,9974** | — |
| akronim huruf kecil | −0,0455 | +0,048 s |
| tanggal & jam | 0,0175 | −0,384 s |
| nomor telepon | 0,1069 | **−0,960 s** |
| simbol & satuan | 0,0413 | −0,936 s |
| singkatan umum | −0,0066 | **−2,376 s** |
| versi & ukuran | −0,0735 | +0,264 s |
| email & URL | 0,0626 | +0,528 s |

Kontrol 0,9974 membuktikan metodenya sah; semua kasus ≈0 = audio benar-benar berubah.

**Audisi untuk telinga:** `audisi_pelafalan/audisi_pelafalan_sebelum_vs_sesudah.mp3`
(107,9 s — tiap kasus: penanda "Sebelum." → versi lama → penanda "Sesudah." → versi baru).

> **Batasan yang saya nyatakan jujur:** saya **tidak bisa mendengar** audio, dan dua proksi
> otomatis untuk pelafalan **tidak layak** — (1) `whisper-cli` model *base* berhalusinasi
> ("es ka pe de" ditranskripsi "Eskapi diri"); (2) durasi ucapan tidak bisa dipakai karena
> edge-tts memangkas output pendek ke 1,872 s. Karena itu bukti yang saya ajukan adalah
> **level teks (deterministik) + korelasi audio**, dan penilaian akhir tetap di telinga pemilik.

## 5 · Hasil

| Masukan | Yang diucapkan (SESUDAH) |
|---|---|
| `laporan skpd ke bpkp` | `laporan es ka pe de ke be pe ka pe` |
| `0812-3456-7890` | `nol delapan satu dua tiga empat lima enam tujuh delapan sembilan nol` |
| `19/09/2026` | `sembilan belas September dua ribu dua puluh enam` |
| `v4.1.0` | `versi empat titik satu titik nol` |
| `09:30` | `jam sembilan tiga puluh` |
| `14.00` | `jam empat belas tepat` |
| `5-10` | `lima sampai sepuluh` |
| `Rp 3.117.360.000` | `tiga miliar seratus tujuh belas juta tiga ratus enam puluh ribu rupiah` |
| `A & B (urgent)` | `A dan B urgent` |
| `dll., dgn, sbb.` | `dan lain-lain, dengan, sebagai berikut` |
| `admin@niumination.web.id` | `admin at niumination titik web titik id` |
| `10 GB` | `sepuluh gigabita` |
| `ke-3` | `ketiga` |
| `data.csv` | `data se es ve` |

Render penuh end-to-end: 5 potongan → semua `44100 Hz · stereo · 192 kbps`, `panggilan TTS: 5/200`.

## 6 · Berkas

| Berkas | Isi |
|---|---|
| `hermes-tts/pelafalan_tambahan.py` | modul normalisasi pelafalan (baru) |
| `hermes-tts/tts_hermes.py` | dipatch: impor modul, kamus tanpa-peka-huruf, panggilan normalisasi |
| `hermes-tts/kamus_pelafalan.json` | 128 entri + `_peka_huruf_besar` (52 → 128) |
| `uji_emas_pelafalan.py` | 28 kasus dengan harapan eksplisit |
| `uji_regresi_naskah.py` | bandingkan lama vs baru pada 33 naskah MATA |
| `buat_audisi_pelafalan.py` | render audisi A/B |
| `verifikasi_audio_pelafalan.py` | korelasi gelombang sebelum vs sesudah |
| `audisi_pelafalan/audisi_pelafalan_sebelum_vs_sesudah.mp3` | audisi untuk telinga (107,9 s) |
| `recon_pelafalan.py` · `analisis_varian_kamus.py` | analisis awal (diagnosis) |

## 7 · Menambah istilah baru (tanpa sentuh skrip)

Edit `hermes-tts/kamus_pelafalan.json`, lalu jalankan `python3 uji_emas_pelafalan.py`
untuk memastikan tidak ada regresi.
