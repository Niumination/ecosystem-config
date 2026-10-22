# Naskah VO — Realisasi Pengadaan BPKK Agustus 2026 (60 detik)

## Hook (3 opsi)

1. "Rp1,67 miliar dikucurkan bulan ini. Berapa yang sudah jadi?"
2. "Laporan realisasi pengadaan BPKK Agustus 2026 — angka nyatanya begini."
3. "9 item selesai 100%, 6 ditunda ke 2027. Ininya detailnya."

**PILIH:** Hook 1 (utama)

## Naskah UTUH (60 dtk, ~150 kata)

```
Rp1,67 miliar anggaran revisi bulan Agustus. Ini realisasinya.

Selesai seratus persen: lemari arsip, kursi tamu, empat laptop Expertbook, satu laptop Ryzen AI, dan pelunasan komputer tahun lalu.

Masih dalam proses: rehabilitasi ruang pelayanan tujuh puluh persen, pemasangan jaringan lokal hampir rampung, dan pemeliharaan gedung empat puluh dua persen.

Ditunda ke dua ribu dua puluh tujuh karena Silpa: Honda Verza dua unit, iPad, printer, video conference, serta pengamanan aset strategis — Huawei Mate X7 dan Samsung Z Fold Seven.

Total realisasi keuangan delapan puluh lima koma dua persen. Sisa anggaran akan dipergunakan di bulan-bulan berikutnya.

Laporan lengkap tersedia di BPKK Aceh Tengah.
```

## Format untuk gemini_vo.py

Simpan ke naskah.txt (tanpa komentar, tanpa tag):

```
Rp1,67 miliar anggaran revisi bulan Agustus. Ini realisasinya.

Selesai seratus persen: lemari arsip, kursi tamu, empat laptop Expertbook, satu laptop Ryzen AI, dan pelunasan komputer tahun lalu.

Masih dalam proses: rehabilitasi ruang pelayanan tujuh puluh persen, pemasangan jaringan lokal hampir rampung, dan pemeliharaan gedung empat puluh dua persen.

Ditunda ke dua ribu dua puluh tujuh karena Silpa: Honda Verza dua unit, iPad, printer, video conference, serta pengamanan aset strategis — Huawei Mate X7 dan Samsung Z Fold Seven.

Total realisasi keuangan delapan puluh lima koma dua persen. Sisa anggaran akan dipergunakan di bulan-bulan berikutnya.

Laporan lengkap tersedia di BPKK Aceh Tengah.
```

## Perkiraan durasi per scene (berdasarkan karakter naskah)

- Hook: ~4s (28 karakter)
- Konteks: ~4s (25 karakter)
- Beat 1 (Selesai): ~12s (95 karakter)
- Beat 2 (Proses): ~14s (108 karakter)
- Beat 3 (Silpa): ~16s (125 karakter)
- Payoff: ~10s (82 karakter)
- CTA: ~6s (40 karakter)
- TOTAL: ~66 detik (target: 60-65dtk)

## Scene → Visual mapping

| Scene | Durasi | Teks On-Screen | Visual |
|-------|--------|----------------|--------|
| 1 | 4s | "Rp1,67 Miliar" | Teks besar + grid |
| 2 | 4s | "Realisasi Agustus 2026" | Dokumen header |
| 3 | 12s | "6 Item Selesai 100%" | Collage foto item (lemari, kursi, laptop) |
| 4 | 14s | "8 Item Proses" | Progress bar + foto proses |
| 5 | 16s | "9 Item → 2027 (Silpa)" | Foto item ditunda + label |
| 6 | 10s | "Realisasi: 85.2%" | Pie chart/gambar besar |
| 7 | 6s | "BPKK Aceh Tengah" | Logo + kontak |
