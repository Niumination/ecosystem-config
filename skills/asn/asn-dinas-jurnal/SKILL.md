---
name: asn-dinas-jurnal
description: Log kegiatan harian. Use for daily activity journal.
---

# asn-dinas-jurnal

Log kegiatan harian dari obrolan chat → data/aktivitas-log.csv.

## Konteks
- Pemilik: Afrizal Munthe, Pranata Komputer Terampil, Diskominfo Aceh Tengah
- Sumber utama SKP: tanpa log, SKP jadi fabrikasi

## Format Log
```
Tanggal,Waktu,Kegiatan,Output,Durasi menit,Kategori
2026-05-01,08:00-09:30,Rapat koordinasi,Notulensi,90,Rapat
2026-05-01,09:30-11:00,Penyusunan surat dinas,Surat dinas,90,Surat
```

## Kategori
- Rapat
- Surat
- SKP/Kinerja
- Pemdi/SPBE
- Pengembangan sistem
- Lainnya

## Aturan
- Log minimal 1 entri per hari kerja
- Waktu dalam format HH:MM
- Durasi dalam menit
- Output ke data/aktivitas-log.csv (append)
- Jangan tulis ke repo publik — repo ini PRIVAT

## Integrasi
- Data SKP: data/indikator-skp-*.csv
- Skill terkait: skp-e-kinerja
