# Paket Dokumen Serah Terima

Register dokumen dan isi wajib masing-masingnya. Nomor berkas sengaja tetap
(`00`-`10`) supaya urutannya stabil dan bisa dirujuk dari dokumen lain. Dokumen
administrasi (`11`, `12`) hanya ditambahkan bila penerima memerlukannya, dan selalu
di **belakang** — jangan menyisipkan di tengah.

## Mengapa nomor tetap

Penerima merujuk "butir 4 di dokumen 00" saat rapat serah terima. Kalau nomor
bergeser tiap rilis, rujukan itu mati. Tambahkan dokumen baru di akhir, jangan
menyisipkan di tengah.

## Register dan isi wajib

**`README.md` (indeks paket)** — apa ini, untuk siapa, **cara membaca sesuai peran**
(pimpinan / pengelola teknis / persandian / pengguna / pemeriksa mutu), daftar
berkas satu baris masing-masing, konvensi (bahasa, tanpa rahasia), dan kewajiban
memperbarui dokumen saat perilaku berubah.

**`00-BERITA-ACARA-SERAH-TERIMA.md`** — identitas aplikasi + versi + tanggal;
para pihak (nama, jabatan, unit, NIP placeholder); tabel ruang lingkup yang
diserahkan (kode, hak cipta, dokumentasi, proyek hosting, domain, penyimpanan
keadaan, sumber data, kredensial "diserahkan terpisah"); deskripsi singkat;
**butir keadaan saat serah terima** (semua yang belum selesai, apa adanya);
tabel kriteria penerimaan dengan kolom status; batas tanggung jawab; blok tanda
tangan.

**`01-RINGKASAN-APLIKASI.md`** — untuk semua pembaca: kegunaan, siapa penggunanya,
sumber data dan konsekuensi bila sumber mati, daftar halaman & endpoint, cara
jawaban disusun, matriks saklar/kontrol, batasan yang perlu diketahui sejak awal,
keadaan saat ini, dan daftar dokumen lain.

**`02-ARSITEKTUR.md`** — alur data dari sumber sampai jawaban (diagram teks),
komponen + tanggung jawab, pilihan teknologi beserta alasan singkat, struktur
folder penting, **batasan desain yang disengaja** (apa yang sengaja tidak ada),
dan perilaku saat layanan hulu mati.

**`03-PANDUAN-INSTALASI-DAN-DEPLOYMENT.md`** — prasyarat (versi runtime dari
`.nvmrc`/`engines`), langkah lokal, **seluruh** variabel env dari `.env.example`
beserta wajib/opsional dan nilai bawaannya, build & jalankan, langkah deploy
ke hosting (termasuk region), pengaturan domain, verifikasi pasca-deploy.
Setiap langkah disertai hasil yang diharapkan.

**`04-PANDUAN-OPERASIONAL-RUNBOOK.md`** — daftar periksa harian/mingguan/bulanan,
memeriksa kesehatan, menyalakan/mematikan layanan, menyegarkan cache, tabel gejala →
langkah penanganan, prosedur rollback, batas anggaran waktu berlapis, dan jalur
eskalasi dengan placeholder yang jelas.

**`05-PANDUAN-PENGGUNA.md`** — untuk pegawai non-teknis: apa yang bisa/tidak bisa
ditanyakan, contoh pertanyaan nyata (minimal 8), arti tiap bagian jawaban (narasi,
bukti/tabel, satuan, tahun, OPD, rekomendasi), arti pesan galat + tindakannya, dan
pernyataan tegas bahwa jawaban AI bersifat informatif — angka resmi dari OPD.

**`06-DOKUMENTASI-API.md`** — per endpoint: metode, path, parameter, contoh `curl`
siap tempel, contoh respons, kode status yang mungkin (termasuk 401/503) dan artinya.
Untuk SSE: urutan event secara eksplisit (status → token → result/error).

**`07-KEAMANAN-DAN-DATA.md`** — klasifikasi data yang diproses; **alur data ke pihak
ketiga** (apa yang dikirim keluar, apa yang tidak) — ini butir yang paling dicari
peninjau keamanan; daftar rahasia beserta tempat penyimpanan dan siapa boleh
memegang; kontrol akses panel admin; perlindungan endpoint yang mengubah keadaan;
palang penyaring data pribadi; prosedur rotasi kredensial dan prosedur bila diduga
bocor; daftar risiko terbuka yang jujur (tanpa jejak audit per aksi, kunci tunggal,
tanpa peran pengguna, ketergantungan pihak ketiga).

**`08-TATA-KELOLA-AI.md`** — model & penyedia, seluruh kontrol on/off beserta
matriks akibat tiap kombinasi, jaminan agar model tidak mengarang angka
(grounding/eject — telusuri di kode, jangan diklaim), pagar prompt, metrik pemakaian,
kendali biaya, prosedur mengganti model/penyedia lewat env, dan batas tanggung jawab.

**`09-PENGUJIAN-DAN-MUTU.md`** — kelompok pengujian yang ada, perintah menjalankan
tiap jenis, gerbang otomatis di CI (sebutkan job mana yang `continue-on-error`),
hasil terkini, dan **batas yang belum tercakup** (jujur, mis. perilaku UI di browser).

**`10-PEMELIHARAAN-DAN-ROADMAP.md`** — tiga hal yang dirawat, kegiatan rutin,
definisi operasional "layanan sehat", **tindakan yang harus diselesaikan penerima**
(kuota, batas pemakaian, baseline evaluasi, tinjauan lisensi, kebersihan branch),
rencana lanjutan, tabel risiko → penanganan, dan ketergantungan yang perlu dipantau
masa berlakunya.

**Di akar repo (bukan di folder paket):** `LICENSE` (hak cipta + daftar lisensi
komponen pihak ketiga, termasuk peringatan lisensi non-OSI), `CHANGELOG.md`
(versi, tanggal, dan ALASAN tiap perubahan besar), `README.md` (pintu masuk repo,
menunjuk ke paket serah terima), serta `AGENTS.md` (aturan agen — jangan disalin ke
dokumen penerima).

## Dokumen administrasi (`11`, `12`)

Diminta terpisah dari paket teknis, biasanya oleh pengelola administrasi kegiatan.
Keduanya **tidak boleh memuat satu pun angka karangan** — setiap nilai rupiah,
nomor dokumen, tahun anggaran, dan pagu ditulis sebagai `[DIISI: …]` supaya jelas
bahwa itu kewenangan penyusun anggaran, bukan pengembang. Hitung jumlah isian dan
sebutkan ke pemilik saat melapor, supaya ia tahu berapa yang harus dilengkapi.

**`11-KERANGKA-ACUAN-KERJA.md` (KAK)** — nama kegiatan, unit kerja, tahun anggaran,
sumber dana (placeholder); latar belakang (masalah nyata yang dipecahkan); maksud &
tujuan; sasaran dengan ukuran keberhasilan; ruang lingkup yang dibagi **termasuk**
dan **tidak termasuk** (paling penting: sumber data pihak ketiga, pengadaan
perangkat, biaya langganan, data pribadi); keluaran beserta bentuk dan bukti
penerimaan; kriteria penerimaan yang bisa diuji; metode pelaksanaan bertahap; jadwal;
personel; penunjuk ke RAB; pelaporan dan serah terima; blok tanda tangan.

**`12-RENCANA-ANGGARAN-BIAYA.md` (RAB)** — ringkasan komponen; biaya pengembangan
(satuan OB/OH dengan placeholder); biaya operasional tahunan; pengembangan lanjutan
opsional; rekapitulasi; dan catatan penyusunan. Yang **boleh** diisi karena bisa
dibuktikan: pos yang memang tanpa biaya pada tier yang sedang dipakai (tulis "biaya
Rp0" beserta tier-nya, jangan diamkan kosong) dan mana yang berbasis pemakaian.
Untuk pos berbasis pemakaian, tulis **rumus** dari metrik aplikasi yang tersedia
(mis. `jumlah pertanyaan/bulan × rata-rata token keluaran × harga per token penyedia`)
dan sebutkan endpoint metriknya — lebih berguna daripada taksiran.

Aturan yang sama berlaku untuk seluruh dokumen paket: nilai yang bisa diperiksa
diisi, nilai yang butuh keputusan pejabat dikosongkan dengan penanda. Sebutkan juga
penghematan yang sudah melekat pada arsitektur (mis. tanpa basis data berarti tanpa
biaya server basis data), karena itu bahan pertimbangan anggaran yang sah dan bukan
karangan.

## Templat brief untuk penulis paralel

Delegasi menulis dokumen berhasil hanya bila brief-nya mengikat. Isi brief:

```text
Target pembaca: <unit penerima> — teknisi/pengguna, bukan pengembang aplikasi ini.
Bahasa Indonesia formal; perintah, path, dan nama variabel tetap Inggris.

APLIKASI: <nama> — <fungsi singkat>. Sumber data: <sumber>. Arsitektur sengaja
<batasan>: tanpa <daftar>. Repo: <url> (privat). Produksi: <url>.

Alur jawaban/perilaku yang WAJIB dibaca dari kode, bukan dikarang:
<berkas-berkas kunci>

Fakta yang harus diverifikasi sendiri dari repo: <endpoint, env, test, skrip>.

ATURAN KETAT:
- HANYA fakta yang bisa dibuktikan dari repositori. Dilarang mengarang angka,
  nama variabel, endpoint, atau perilaku.
- Bila ragu, tulis "(perlu dikonfirmasi)".
- JANGAN menulis nilai rahasia apa pun (API key, token, kredensial).
- JANGAN menjalankan git yang mengubah keadaan; hanya baca dan tulis berkas target.
- Bahasa Indonesia, tanpa emoji, heading + bullet, langkah siap diikuti.
- Setelah selesai: laporkan daftar berkas yang kamu tulis + jumlah baris + fakta
  kunci apa saja yang kamu verifikasi SENDIRI dari repo.
```

Ukuran batch: **maksimal 2 dokumen panjang per penulis.** Tiga dokumen panjang
menghabiskan batas waktu anak sehingga ia kembali tanpa hasil sama sekali — dan
yang hilang bukan hasil yang bisa diperbaiki, melainkan seluruh kerjanya.

Setelah kembali: hitung baris tiap berkas, lalu grep klaim usang (langkah 5 di
SKILL.md). Penulis paralel tidak tahu repo sudah dibersihkan sesudah ia membaca.

Tetapi laporan anak (daftar berkas + fakta yang ia verifikasi) adalah petunjuk
untuk memeriksa lebih tajam, bukan bukti. Yang paling sering salah bukan panjang
atau judul, melainkan **spesifik yang akan disalin pembaca**: bentuk parameter
endpoint, kode status, nama variabel env, jumlah test. Cocokkan tiap sebutan itu ke
route/handler/`env.example`, jalankan sendiri setiap angka, dan probe sendiri setiap
klaim keamanan — klaim anak yang salah menjadi temuan palsu bagi penerima.
