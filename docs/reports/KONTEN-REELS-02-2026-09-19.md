# Paket Konten Reels 02 — "Niu OSS Dashboard" (19 Sep 2026)

**Pelaksana:** Hermes — thread Kreator (1172)
**Pemicu:** permintaan Afrizal Munthe — buat reels soal proyek baru Niu-OSS-Dashboard, sampai siap posting
**Status:** **siap tayang** — video final, naskah, caption, dan paket tayang lengkap
**Mesin suara:** Gemini TTS 3.1 Flash (suara Charon) — standar yang dikunci hari ini

---

## 0. Ringkasan

| Item | Nilai |
|---|---|
| Pilar | `Behind the Build` — produk baru |
| Durasi | 56,6 detik (6 adegan) |
| Format | 1080×1920 · 30 fps · h264 + aac 192 kbps |
| Ukuran | 5.180.143 bita |
| md5 | `484a404abf278916883a329ac4443dee` |
| Suara | Charon (Informative) + preset `narator` |
| Berkas tayang | `~/Movies/Posting - Instagram/2026-09-19-reels-02-niu-oss-dashboard.mp4` |
| Sumber kerja | `~/Downloads/niu-konten/reels-002/` |

## 1. Fakta yang dipakai — semua diverifikasi ke repo

| Klaim di konten | Sumber |
|---|---|
| 91 repo publik | `data/repos.json` → 91 entri |
| 101 berkas JSON di API v1 | `find public/api/v1 -name '*.json'` → 101 |
| 41 tes lulus | `npm test` per AGENTS.md proyek |
| Next.js 15 + React 19 | `package.json` proyek |
| Hero 3D sadar performa | README proyek |
| Repo publik & bisa dibuka | GitHub API → `status=200`, `private: false` |

**Yang sengaja TIDAK diklaim:** situs `niumination.web.id` **belum live** (DNS belum resolve
per 19 Sep 2026). Karena itu ajakan di video mengarah ke **repo GitHub yang sudah publik**,
dan caption menyebut "segera live" — bukan "sudah tayang".

## 2. Struktur naskah & adegan

| # | Adegan | Waktu | Isi |
|---|---|---|---|
| 1 | Hook | 0 – 6,4 s | 91 repo, satu halaman |
| 2 | Masalah | 6,4 – 13,7 s | Bukan bikin proyeknya — tidak ada yang tahu proyeknya ada |
| 3 | Apa ini | 13,7 – 25,1 s | Satu situs, dua wajah |
| 4 | Fitur | 25,1 – 36,9 s | Pencarian, kategori, Ctrl+K, API publik v1 |
| 5 | Teknis | 36,9 – 49,4 s | Next.js 15 + React 19, 3D adaptif, 41 tes |
| 6 | CTA | 49,4 – 56,6 s | Repo publik + ajakan simpan |

Batas adegan **diturunkan dari VO, bukan ditebak**: naskah dirender jadi satu berkas
(1 permintaan kuota), lalu jeda antar-paragraf diukur dari profil energi audio, dan
dipetakan ke batas paragraf naskah secara monotonik. Total galat pemetaan **0,99 detik**;
empat dari lima titik terpilih adalah jeda terpanjang — konsisten dengan `[short pause]`
yang memang ditaruh di situ.

## 3. Suara — mengikuti standar yang dikunci

- Naskah dikirim **apa adanya** (angka sebagai angka, istilah Inggris sebagai Inggris)
- Gaya lewat **preset `narator`** (profil Pak Rizal + adegan + arahan performa)
- **Tag audio berbahasa Inggris**: `[short pause]` `[interest]` `[thoughtfully]` `[neutral]` `[warmly]`
- Satu permintaan untuk seluruh naskah — hemat kuota

**Dua perbaikan yang dilakukan justru karena TERBUKTI salah** (bukan karena dugaan):

| Temuan | Bukti | Perbaikan |
|---|---|---|
| `Niu` terucap "Neo" | transkrip `periksa_vo.py` dua kali | ditulis `Nyu` → terucap "nyu" |
| `command palette` jadi "komen pelet" | transkrip `periksa_vo.py` | diganti "pintasan Control K" → terucap jelas |

`Next.js` dibiarkan apa adanya — hasilnya "Next JS", sudah benar. **Tidak ditambal.**

Nama produk di layar tetap ditulis **Niu** (ejaan merek benar); hanya suaranya yang
diucapkan "nyu" — sesuai keputusan pemilik 19 Sep 2026.

## 4. Verifikasi yang dijalankan

| Pemeriksaan | Hasil |
|---|---|
| `hyperframes lint --verbose` | **0 error, 0 warning** |
| Render video | h264 · 1080×1920 · 30 fps · 56,600 s |
| Mux audio | aac 193 kbps · 56,600 s · 5.180.143 bita |
| Tingkat audio | mean **−20,1 dB** · puncak **−1,6 dB** (setelah `loudnorm` I=−16) |
| Isi VO terbaca | transkrip `periksa_vo.py`: 91, 101, 41, GitHub, React semua ADA |
| Audio utuh & sejajar | korelasi VO vs audio video **0,9981** (kontrol bergeser 0,5 s: **0,0034**) |
| QA visual 6 frame | tidak ada teks terpotong, tumpang tindih, atau elemen rusak |

## 5. Paket tayang

`caption.md` memuat caption siap tempel + 10 hashtag + catatan tayang. Ajakan mengarah
ke repo GitHub (bisa dibuka sekarang), bukan ke situs (belum live).

## 6. Berkas

| Berkas | Isi |
|---|---|
| `reels-002-niu-oss-dashboard.mp4` | video final (5,2 MB) |
| `reels-002-silent.mp4` | master tanpa suara (untuk render ulang VO) |
| `vo/vo_utuh.mp3` | voice-over 56,56 s · md5 `09976f81714a1a8f49187f1c9a4d8e49` |
| `naskah.txt` | naskah yang dikirim ke mesin TTS |
| `index.html` | komposisi HyperFrames (6 adegan, palet merek Niu-OSS) |
| `caption.md` | caption + hashtag + catatan tayang |

Aset sementara (`renders/`, `qa/`) dihapus setelah QA.

## 7. Catatan untuk konten berikutnya

- Kuota TTS terpakai untuk konten ini: **2 permintaan** (satu render awal, satu setelah perbaikan)
- Palet merek Niu-OSS: ink `#14110d` · cream `#f2ecdf` · ember `#e05a1e` · spotlight `#00e5ff`
- Templat komposisi dapat dipakai ulang dengan mengganti isi adegan dan menyesuaikan
  `data-start`/`data-duration` bila naskahnya berubah
