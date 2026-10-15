# Menyiapkan harness gerbang repo sendiri

Beberapa repo punya skrip verifikasi yang butuh server hidup dan fixture
tertentu. Menjalankan gerbang tanpa disiapkan menghasilkan GAGAL palsu yang
terlihat seperti regresi patch. Persiapan ini bagian dari adoptersi, bukan
langkah opsional.

## 1. Cek signature test sebelum menyiapkan server

Sebagian harness bercabang: bagian statis jalan tanpa server, bagian
server-sScoped di-skip diam-diam dan tetap keluar `LULUS`. Jadi `LULUS`
dengan banyak baris `· … dilewati` bukan bukti — hitung jumlah yang benar-benar
diperiksa:

```bash
grep -cE '^  ✓' log-gerbang
grep -E '^  ✗' log-gerbang     # pastikan bukan bagian dari "N ✓ / M ✗" di dalam baris ✓
```

## 2. Jangan jalankan gerbang berat di foreground

Gerbang penuh dapat berjalan 10-20 menit. Foregroundytooli timeout =
buka besar; proses ikut mati, termasuk server yang baru dihidupkan, dan
evidence hilang. Jalankan `background=true` + tulis log ke file, lalu poll
log dengan `tail`.

## 3. Fixture: stub tanpa argumen hampir selalu data contoh kecil

Stub HTTP yang menerima path fixture opsional akan jatuh ke data bawaan
saat argumen kosong. Data bawaan cukup untuk smoke test tapi JAUH dari
cukup untuk eval — hasilnya ~85/120 item dan gejalanya persis seperti
"retrieval patch rusak": banyak item "tidak menjawab padahal data ADA".

```bash
node stub.mjs <port> <path-fixture>     # WAJIB eksplisit
```

Verifikasi jumlah record dari log startup stub SEBELUM percaya angka eval
apa pun.

## 4. Server harness bentrok dengan `next build`

Selalu `pgrep` + `lsof` port harness sebelum build; build yang jalan
bersamaan dengan server hidup menggantung. Matikan dulu, baru build,
baru nyalakan server.

## 5. Uji yang gagal sekali belum berarti regresi

Rerun check yang sama 3-5× sebelum mendiagnosis. Gejala umum: pembanding
menilai nilai lewat endpoint yang di-cache (mis. cap waktu dari cache
10-menit), sehingga bisa membaca nilai yang sudah berubah di sela.
K overwhelmingly sering 4/5 hijau. Hanya anggap regresi bila signature-nya
konsisten di semua rerun.

## 6. Skrip yang TIDAK ikut gerbang utama harus dijalankan terpisah

Grep nama skrip uji tambahan di skrip gerbang. Yang tidak muncul di sana
tidak pernah dijalankan — jalankan manual dengan URL server yang sudah hidup,
dan hitung hasilnya sebagai bukti terpisah.