# Kasus Gagal — Pelajaran yang Mengunci Skill Ini

Enam kegagalan nyata dalam mengerjakan pelafalan TTS, beserta aturannya. Baca sebelum
mengubah apa pun di skill ini.

---

## 1. Jangan mengoptimasi proksi — ukur hasilnya

**Aturan:** bukti akhir adalah suara yang terdengar, bukan angka yang nyaman diukur.

Sebuah rangkaian perbaikan pernah dinyatakan "28/28 lulus" dan "korelasi audio terbukti
berubah", tetapi pemilik mendengarnya dan menyebutnya **lebih buruk daripada sebelumnya**.
Semua uji saya benar; yang salah adalah **apa yang saya ukur**. Teks yang dikirim ke mesin
hanyalah perantara — yang dinilai orang adalah hasil akhirnya.

---

## 2. Jangan memperbaiki kualitas mesin dengan teks

**Aturan:** kalau suaranya kurang bagus, ganti mesinnya — jangan tambal teksnya.

Mesin kelas menengah ditambal dengan teks yang "dimasak" menghasilkan ucapan yang terpotong
dan robotik. Kualitas prosodi adalah properti **model**, bukan properti string. Praktisi TTS
menyebut pola kegagalannya secara harfiah: *"period-separated fragments sound chopped"* —
memecah teks menjadi potongan pendek adalah cara tercepat membuat suara terdengar terputus.

---

## 3. Jangan menambal masalah yang belum dibuktikan

**Aturan:** buktikan dulu mesinnya salah pada kasus itu, baru tambal.

Puluhan aturan normalisasi pernah dibangun atas asumsi bahwa mesin gagal membaca singkatan,
angka, dan URL — **tanpa satu pun diuji lebih dulu**. Sebagian besar asumsi itu tidak benar,
dan setiap aturan yang tidak perlu menambah satu titik gagal. Normalisasi berlapis membuat
kesalahan makin sulit dilacak, bukan makin mudah.

---

## 4. "Benar" tidak sama dengan "natural"

**Aturan:** uji pelafalan dan uji kealamian adalah dua hal berbeda. Lulus yang satu tidak
berarti lulus yang lain.

Transkripsi ulang membuktikan mesin mengucapkan kata yang diminta dengan tepat — termasuk
`Rp 3.117.360.000` terbaca utuh. Pada saat yang sama, telinga menolak hasilnya karena kaku
dan terpenggal. **Jangan pernah memakai hasil uji pelafalan sebagai bukti kualitas suara.**

---

## 5. Semua ASR menerapkan inverse text normalization — dan model kecil berhalusinasi

**Aturan:** baca transkripnya, jangan hanya mencocokkan pola; dan jangan pakai model STT
lokal kecil untuk Bahasa Indonesia.

Whisper mengubah bilangan yang *diucapkan* kembali menjadi *angka*. Frasa yang diucapkan
sebagai "tiga miliar seratus tujuh belas juta …" muncul di transkrip sebagai
`Rp 3.117.360.000.` — perhatikan titik pemisah ribuan. Pemeriksaan yang mencari kata
`miliar` melaporkan **gagal palsu**: sembilan dari tiga belas kasus pernah salah dinyatakan
gagal karena hal ini.

Lebih buruk lagi, whisper `base` berhalusinasi: "es ka pe de" pernah menjadi "Eskapi diri".
Model yang akurat berukuran 1,5 GB dan butuh ~2,5 menit per potongan di CPU tanpa GPU —
mahal untuk alat yang hanya dipakai sesekali.

**Gantinya:** pakai `scripts/periksa_vo.py` (Gemini sebagai pentranskrip). Tanpa unduhan,
kuota terpisah dari kuota TTS, dan lebih akurat untuk Bahasa Indonesia. Bukti bahwa model
kecil menyesatkan: dua unsur pernah dinyatakan "tidak terbaca" oleh whisper, lalu
dinyatakan **benar** saat diperiksa dengan cara ini.

**Tetap hati-hati:** pentranskrip juga menormalkan bentuk dan nama tak lazim. Nama merek
seperti `niumination` pernah tertranskrip `newmination` oleh dua sistem berbeda — belum
pasti itu salah ucap mesin atau sekadar normalisasi. **Kalau ragu, dengarkan sendiri.**

---

## 6. Harness yang memakai logika subjeknya akan "hijau tapi menipu"

**Aturan:** pemeriksa harus ditulis dari harapan yang berdiri sendiri — bukan dari logika
yang sedang diperiksa.

Sebuah harness pernah melaporkan hampir semua kasus bersih, padahal rusak: pemeriksanya
memakai fungsi yang sama dengan yang diperiksa, sehingga kesalahannya ikut termaafkan.
Gantinya: uji dengan **harapan eksplisit yang ditulis tangan**, lalu bandingkan keluaran
nyata terhadap harapan itu.

---

## Ringkas dalam satu baris

> Kirim naskah apa adanya; atur gaya lewat prompt; buktikan dengan telinga; jangan tambal
> apa pun sebelum terbukti perlu.
