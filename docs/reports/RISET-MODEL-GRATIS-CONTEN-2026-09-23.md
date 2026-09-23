# RISET MODEL GRATIS UNTUK PIPELINE KONTEN

**Tanggal:** 2026-09-23
**Sumber awal:** https://free.theresanaiforthat.com/
**Ruang lingkup:** model yang bisa dipakai membuat konten, gratis, tanpa kartu kredit
**Status:** riset selesai — 1 jalur layak dites, 4 jalur dibatalkan dengan alasan

---

## Kesimpulan utama

Situs itu adalah **katalog informasi**, bukan penyedia akses. Halaman detail setiap model
menautkan tombol "Visit model" ke link afiliasi vendor (`?ref=taaft&utm_source=taaft`),
tanpa kontrol Generate, tanpa API key, tanpa trial. "Free mode" di sana berarti gratis
membuka *halaman infonya*.

Dari 21 entri model terbaru yang berhasil di-parse dari `/models/` (2,989 perusahaan,
143.2k+ AI, terakhir diperbarui 22 Sep 2026), hanya **satu keluarga** yang relevan dengan
pipeline konten kita: Alibaba Qwen. Dua model keluarganya ditandai "Open source" oleh
katalog — dan dua-duanya saya telusuri ke sumber aslinya. Hasilnya: **satu lolos lisensi
tapi gagal bahasa, satu gagal lisensi.**

**Tidak ada satu pun model dari situs ini yang dapat mengisi slot TTS Bahasa Indonesia.**

---

## Analisis per kandidat

### 1. Qwen3-TTS — LULUS lisensi, GAGAL bahasa

Ditelusuri ke: https://github.com/QwenLM/Qwen3-TTS · 13.5k stars · rilis 22 Jan 2026

| Aspek | Hasil verifikasi |
|---|---|
| Lisensi | **Apache-2.0** — terkonfirmasi dari teks LICENSE penuh; "Commercial use" eksplisit di-permit. Cocok untuk konten berbayar. |
| Bahasa | 10 bahasa: Zh, En, Ja, Ko, De, Fr, Ru, Pt, Es, It. **Indonesia TIDAK ada.** |
| Bukti kegagalan bahasa | Laporan pengguna lokal: *"cloning is ok, only if you use english or supported languages. however in your non-supported language, the cloned voice will not pronounce words"* — bukan sekadar kualitas buruk, tapi gagal mengucapkan kata. |
| Kebutuhan hardware | Semua contoh resmi memakai `device_map="cuda:0"` + `attn_implementation="flash_attention_2"`. **Mesin kita CPU-only, VRAM 2 GB (UHD 620).** |
| Ukuran | 0.6B = 0.9B params / 993 MB Q8_0; 1.7B = 2B params / 2.08 GB Q8_0. Ada varian GGUF pihak ketiga (Serveurperso/Qwen3-TTS-GGUF) dengan runtime `qwentts.cpp` — muat di RAM 16 GB. |

Variasi GGUF memang menjadikannya *mungkin* dijalankan di CPU. Tapi masalah bahasanya
tetap berdiri: untuk TTS Indonesia, model ini secara eksplisit gagal. Menjadikannya
pengganti Gemini Charon untuk konten Pemkab Aceh Tengah tidak realistis.

**Tersisa satu cara:** voice clone dengan audio referensi Indonesia, dan berharap model
mengeneralisasi melampaui bahasa latihannya. Itu spekulasi, bukan verifikasi.

### 2. Qwen-Image-2.1 — GAGAL lisensi

Ditelusuri ke: https://huggingface.co/Qwen/Qwen-Image-2.1 · 28,407 unduhan/bln

Lisensinya **bukan** Apache. Teks LICENSE berbunyi *"Qwen RESEARCH LICENSE AGREEMENT"*:

> *"FOR NON-COMMERCIAL PURPOSES ONLY... You shall not use the Materials for any commercial
> purpose without obtaining a separate commercial license."*

Dan definisi eksplisit: *"Non-Commercial shall mean for research or evaluation purposes only."*

**Dibatalkan.** Tidak bisa dipakai untuk konten berbayar abstract.biz.id atau layanan publik
Pkem Aceh Tengah. Ini contoh konkret kenapa label "Open source" di katalog itu menyesatkan —
model open weight **bukan** otomatis izin komersial.

### 3. Qwen Audio 3.1 TTS Flash / Next — closed source

Rilis 22 Sep 2026 (kemarin). Fitur menarik sekali untuk konten: TTS Next mendukung dialogue
multi-speaker, podcast, sound design sinematik, output hingga 240 detik — persis kebutuhan
kita. Tapi kedua model ditutup; aksesnya hanya lewat Alibaba Cloud Model Studio (DashScope),
yang membutuhkan akun cloud.

### 4. Freya Adam V1 / Eve V1 — closed source, API berbayar

Rilis 21 Sep 2026. Adam V1 tercatat peringkat 2 di Design Arena Audio Realism Bench.
Akses hanya lewat situs Freya. Tidak ada jalur gratis.

### 5. MeloTTS — MIT, CPU real-time, tapi gagal bahasa

Alternatif lokal yang saya cek paralel: https://github.com/myshell-ai/MeloTTS · MIT license
(komersial OK) · mengklaim *"Fast enough for CPU real-time inference"* — cocok dengan mesin
kita. Tapi daftar bahasanya: Inggris (4 aksen), Spanyol, Prancis, Tionghoa, Jepang, Korea.
**Indonesia juga tidak ada.** Dan terakhir di-commit Desember 2024 — sudah 21 bulan tak aktif.

---

## Jalur yang tersisa: free tier API Alibaba Cloud

Satu-satunya jalur yang belum saya batalkan. Model Studio (DashScope) menawarkan kuota gratis
untuk pengguna baru — banner resminya menyebut *"1M tokens per model"* dan platform sister
(QianwenAI) mengklaim *"over 100 million free tokens"* untuk pengguna baru. Kuota ini berlaku
otomatis saat aktivasi pertama, tanpa pembelian.

Yang relevan untuk kita: **Qwen3-TTS-Flash** dan **Cosyvoice-V3-Flash** — keduanya tampil di
daftar model TTS platform tersebut.

Tapi saya tidak bisa mengklaim ini jalan, karena tiga hal:

1. **Kartu kredit / KYC — belum terverifikasi.** Halaman `/new-free-quota` tidak memberikan
   jawaban bersih tentang persyaratan pembayaran saat registrasi. Dokumentasi Alibaba Cloud
   internasional umumnya mensyaratkan verifikasi identitas akun; apakah kartu kredit wajib
   atau cukup identitas, **UNCHECKED**. Ini pertanyaan eksplisit Anda, dan saya belum menjawabnya.
2. **Regionalitas.** Dokumentasi mencatat *"The following models offer a free quota only in
   Singapore. No free quota is available in other regions."* Tidak jelas model TTS masuk daftar
   itu atau bukan.
3. **Akun sendiri.** Mengaktifkan ini membutuhkan Anda mendaftar akun Alibaba Cloud, yang
   melibatkan identitas pribadi Anda. Saya tidak akan melakukannya atas nama Anda.

---

## Mengapa hasilnya negatif — dan kenapa itu berguna

Selama produksi reels-003, kendala nyata kita bukan penulisan naskah melainkan **VO**:
Gemini TTS Charon dibatasi 10 permintaan/hari. Saya memasuki riset ini dengan hipotesis
bahwa katalog itu akan membuka celah TTS gratis. Tidak.

Tiga pembatal bekerja simultan, dan ketiganya struktural bukan sementara:

1. **Bahasa.** Model TTS open source berkualitas tinggi (Qwen3-TTS, MeloTTS, Freya) semuanya
   dioptimalkan untuk bahasa besar. Indonesia tidak dilatih — dan komunitas mengonfirmasi
   kegagalannya bersifat keras (kata tidak terucap), bukan sekadar kurang natural.
2. **Hardware.** Contoh resmi semuanya asumsikan GPU CUDA. Mesin kita 2 GB VRAM.
3. **Lisensi.** Label "Open source" di katalog tidak menjamin izin komersial — terbukti pada
   Qwen-Image-2.1 yang ternyata Research-only.

Artinya **kuota Gemini 10/hari kemungkinan besar tetap menjadi batas nyata** untuk slot VO
kita dalam jangka pendek. Pilihan yang realistis: menaikkan kuota Gemini, atau menerima
volume konten yang sesuai kuota.

Yang tidak berubah — jalur yang sudah tertutup dan tetap tertutup:
- **Penulisan naskah** — 7 model `:free` di nous + 22 di openrouter, terverifikasi di
  `docs/registry/model-mapping.md`. Tidak ada celah.
- **Render video** — HyperFrames open source, gratis, sudah produksi. Tidak ada celah.
- **QA visual** — vision_analyze berjalan.

---

## Yang belum saya verifikasi

Untuk jujur, ini daftar kegapaian, bukan daftar pencapaian:

| Item | Status |
|---|---|
| Persyaratan kartu kredit untuk free quota Alibaba Cloud | **UNCHECKED** — halaman dokumentasi tidak menjawab; perlu registrasi akun untuk melihatnya |
| Apakah Qwen3-TTS menghasilkan Indonesia yang dapat diterima | **UNCHECKED** — laporan komunitas negatif; tidak diuji sendiri |
| Apakah `qwentts.cpp` berjalan di macOS x86_64 ini | **UNCHECKED** — membutuhkan build + unduhan ~1 GB |
| Key 9router (`No active credentials for provider`) | **UNCHECKED** — router hidup (`/v1/models` → 200) tapi 3 model gratis ditolak; konsisten dengan riwayat `GITHUB_TOKEN` kedaluwarsa |
| Halaman `/tasks/text-to-speech/` dll. | Mengembalikan redirect ke index generik; tidak ada daftar task-filtered |

Saya tidak menjalankan instalasi, unduhan model, atau registrasi akun apa pun. Ketiganya
butuh persetujuan eksplisit Anda.

---

## Rekomendasi

Tidak ada tindakan pengadaan yang saya sarankan dari hasil ini. Secara berurutan:

1. **Tetap pakai Gemini TTS Charon.** Sudah memenuhi standar kualitas yang Anda setujui
   di reels-003 (LRA 3.70 vs 2.30 Piper yang gagal). Kuota 10/hari menjadi pembatas, bukan
   kualitas.
2. **Jika kuota jadi masalah**, pilih yang satu ini — naikkan kuota Gemini, atau kurangi
   frekuensi produksi. Masing-masing keputusan bisnis Anda.
3. **Satu-satunya jalur yang layak dites** adalah free tier Model Studio, tapi itu butuh Anda
   mendaftar akun Alibaba Cloud, dan persyaratan kartunya belum saya ketahui.

Saya tidak akan menyentuh skill bank, instalasi, atau konfigurasi apa pun tanpa perintah Anda.

---

## Bukti

- `free.theresanaiforthat.com/models/` → 2,989 perusahaan, "Last updated: September 23, 2026"
- `free.theresanaiforthat.com/model/qwen-audio-3-1-tts-flash/` → tombol Visit model =
  `docs.modelstudio.console.alibabacloud.com/...?ref=taaft&utm_medium=referral`; tanpa kontrol generate
- `free.theresanaiforthat.com/search/?q=text+to+speech` → halaman kosong tanpa hasil
- `/tasks/text-to-speech/`, `/tasks/youtube-thumbnails/`, `/tasks/social-media-management/`
  → ketiganya redirect ke index generik
- 21 entri model ter-parse dari cache `/models/`: 9 open source, 12 closed source
- `github.com/QwenLM/Qwen3-TTS` → "QwenLM/Qwen3-TTS is licensed under the Apache License 2.0",
  Permission "Commercial use" di-✓; daftar bahasa 10, tanpa Indonesia
- `huggingface.co/Qwen/Qwen-Image-2.1/blob/main/LICENSE` → "Qwen RESEARCH LICENSE AGREEMENT",
  "FOR NON-COMMERCIAL PURPOSES ONLY", "Non-Commercial shall mean for research or evaluation purposes only"
- `github.com/myshell-ai/MeloTTS` → MIT license, CPU real-time, bahasa: En/Es/Fr/Zh/Ja/Ko — tanpa Indonesia
- `reddit.com/r/LocalLLM/...1rgybig...` → "in your non-supported language, the cloned voice will not pronounce words"
- `huggingface.co/Serveurperso/Qwen3-TTS-GGUF` → runtime `qwentts.cpp`, Q4_K_M 605–993 MB
- `alibabacloud.com/help/en/model-studio/new-free-quota` → kuota baru otomatis saat aktivasi;
  persyaratan pembayaran tidak tercantum; catatan regional "free quota only in Singapore"
- `docs/registry/model-mapping.md` → 42 terverifikasi (22 gratis), snapshot 2026-08-30
- Router `127.0.0.1:20128` → `/v1/models` HTTP 200; 3 model gratis ditolak `No active credentials for provider`
- `sysctl -n hw.memsize` → 16.0 GB RAM; UHD 620 = 2 GB VRAM
