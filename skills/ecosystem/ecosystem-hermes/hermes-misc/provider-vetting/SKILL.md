---
name: provider-vetting
version: 1.0.0
last_updated: "2026-09-23"
description: "Use when vetting a third-party AI model before adopting it."
tags:
  - provider
  - model
  - vetting
  - license
  - tts
---

# Provider & Model Vetting — Niumination

Prosedur sebelum berjanji memakai model pihak ketiga untuk pipeline konten.
Katalog AI (TAAFT, ModelScope, sejenis) adalah **sumber penemuan**, bukan sumber
kebenaran: tiap klaim di katalog wajib diverifikasi ke sumber utama sebelum masuk
rekomendasi.

Dua lapis wajib lulus untuk konten berbayar atau layanan publik Pemkab Aceh Tengah:
**lisensi** (teks `LICENSE` asli di repositori, bukan label katalog) dan
**bahasa/hardware** (daftar bahasa di model card + contoh kode resminya).

## Prosedur

1. **Baca teks `LICENSE` asli.** Buka repositori (HF/GitHub), baca isi file
   `LICENSE`, bukan catatan pendek di bawahnya. Catat: komersial di-permit
   eksplisit? Ada batasan region atau atribusi wajib?
2. **Tentukan slot yang jadi celah dulu.** Jangan menilai model sebelum tahu slot
   mana yang dibuka (lihat tabel slot di bawah).
3. **Verifikasi bahasa target eksplisit.** Cari daftar bahasa tertulis di model
   card; jangan percaya klaim "multilingual". Lengkapi dengan laporan komunitas
   untuk membedakan kegagalan fatal dari yang hanya kurang natural.
4. **Verifikasi hardware dari contoh resmi.** Kalau semua contoh memakai
   `device_map="cuda:0"` + FlashAttention, mesin CPU-only tak memenuhi syarat
   default. Cari jalur CPU riil (GGUF, runtime CPU) dan catat ukurannya.
5. **Tandai hal yang butuh registrasi/instalasi.** Jangan daftar akun, jangan
   instal, jangan unduh tanpa persetujuan eksplisit. Syarat tak terbaca di docs
   publik ditandai `UNCHECKED + alasan`, bukan ditebak.
6. **Laporkan tabel verdict.** Satu baris per kandidat (verdict + alasan satu
   kalimat), baris `UNCHECKED` terpisah. Simpan ke `docs/reports/`.

## Slot pipeline

| Slot | Mesin saat ini | Batas nyata |
|---|---|---|
| Penulisan naskah | model `:free` (nous 7, openrouter 22) | sudah tertutup |
| VO / TTS | Gemini TTS Charon | kuota permintaan/hari |
| Gambar / keyframe | — | tanpa kuota |
| Render video | HyperFrames (open source, lokal) | sudah tertutup |
| QA visual | vision_analyze | berjalan |

## Pitfalls

**Verifikasi lisensi selalu dua lapis — tag katalog bisa menyesatkan.** Baca isi
file `LICENSE` di repositori, bukan label "Open source" di katalog. Mekanisme:
model open *weight* masih bisa berlisensi riset yang melarang komersial; tag
katalog hanya mengindikasikan weight dibagikan, syarat penggunaan di lapisan lain
yang wajib dicek terpisah — satu lulus tak menyertai yang lain.

**Identifikasi slot celah sebelum menilai model.** Selama produksi reels-003 celah
nyata untuk VO bukan kualitas penulisan melainkan kuota API. Masuk riset "model
gratis" tanpa tahu slot yang dibuka cenderung menghasilkan rekomendasi yang tak
mengisi celah apa pun.

**Verifikasi bahasa target eksplisit, bukan "multilingual".** Cek daftar bahasa
terulis di model card, bukan jumlahnya. Model yang mengklaim 10 bahasa tetap bisa
tak memasukkan bahasa target, dan kegagalan bahasa tak didukung biasanya fatal
(kata tak diucapkan), bukan kosmetik.

**Pemeriksaan GPU dari contoh resmi, bukan asumsi.** `cuda:0` + FlashAttention
adalah preferensi penulis, bukan ukuran kebutuhan model. Untuk CPU-only, cari
GGUF atau runtime CPU pihak ketiga dulu, lalu catat ukuran sebenarnya terhadap RAM.

**Jangan mendaftarkan akun atau menginstal apa pun atas nama user.** Registrasi
vendor, verifikasi identitas, instalasi, dan unduhan model menunggu persetujuan
eksplisit. Kalau syarat akses tak terbaca di docs publik, tandai `UNCHECKED` dan
jelaskan mengapa — jangan menebak akses tersedia.

**Jangan klaim lolos dari uji yang output-nya tak terlihat.** Verifikasi seperti
secret-scan harus menampilkan countnya (`MARKER_MATCHES=0`), bukan berkaca dari
ketiadaan pesan gagal. Kalau `|| echo LOLOS` tak muncul di output, uji belum jalan
benar dan wajib diulang dengan counter eksplisit.

## Hasil vetting — kandidat yang pernah diverifikasi

Lapisan: **lisensi** (file LICENSE) · **bahasa** (model card) · **hardware**
(contoh kode) · **akses** (halaman vendor).

| Model | Lisensi | Bahasa target | Hardware | Akses | Verdict |
|---|---|---|---|---|---|
| Qwen-Image-2.1 (7B) | *Qwen RESEARCH LICENSE* — "FOR NON-COMMERCIAL PURPOSES ONLY"; "Non-Commercial shall mean for research or evaluation purposes only" | — | — | HF | **Dibatalkan** — label katalog "Open source" menyesatkan; weight terbuka ≠ izin komersial |
| Qwen3-TTS 0.6B/1.7B | Apache-2.0 — "Commercial use" ✓ | 10 bahasa, Indonesia **tidak ada** | contoh `cuda:0`; GGUF pihak ketiga Q4_K_M 605–993 MB, muat RAM 16 GB | HF, tanpa kredit | **Dibatalkan** — lisensi bersih, bahasa fatal |
| MeloTTS | MIT — komersial ✓ | En/Es/Fr/Zh/Ja/Ko — tanpa Indonesia | CPU real-time ✓ | GitHub/HF | **Dibatalkan** — lisensi + hardware cocok, bahasa gagal |
| Qwen Audio 3.1 TTS Flash/Next | closed | closed | closed | Alibaba Cloud Model Studio (DashScope), akun cloud | dibatalkan — butuh akun cloud |
| Freya Adam V1 / Eve V1 | closed | closed | closed | API Freya, berbayar | dibatalkan — closed |

Kegagalan bahasa Qwen3-TTS bersifat fatal bukan kosmetik; komunitas melaporkan
*"the cloned voice will not pronounce words"* di bahasa yang tak didukung. Jalur
teoritis untuk Indonesia hanyalah voice cloning dengan audio referensi Indonesia
— itu spekulasi, bukan verifikasi.

Qwen3-TTS satu-satunya kandidat berlisensi komersial bersih. Penghalangnya bukan
lisensi melainkan bahasa.

### Lapisan yang tak terverifikasi tanpa akun

Kuota gratis Alibaba Cloud Model Studio berlaku otomatis saat aktivasi pertama,
tapi dua hal tak terbaca di docs publik dan tetap `UNCHECKED`: (1) wajib atau tidak
kartu kredit saat registrasi; (2) regionalitas — docs menyebut sebagian model hanya
punya free quota di region Singapore, tak jelas model TTS termasuk daftar itu. Mengetahuinya
membutuhkan pendaftaran akun (identitas user), jadi menunggu persetujuan eksplisit.

### Sifat sumber katalog

Subdomain katalog "free" berperilaku konsisten: tombol "Visit model" menautkan ke
vendor dengan parameter afiliasi (`?ref=...`), tanpa kontrol Generate tanpa login,
halaman task di-redirect ke index generik, pencarian sering kosong. Nilainya
terbatas sebagai sumber penemuan nama vendor yang layak dicek.

### Temuan negatif bernilai

Ketiga lapisan berinteraksi; pembatalan di satu lapisan mengakhiri jalur tanpa perlu
memeriksa lapisan lain. Membangun verdict per lapis membuat alasan pembatalan tetap
tajam, bukan sekadar "tidak cocok".
