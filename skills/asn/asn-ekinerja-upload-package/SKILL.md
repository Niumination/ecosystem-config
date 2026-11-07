---
name: asn-ekinerja-upload-package
description: Paket bukti dukung eKinerja. Use for upload packages.
---

# asn-ekinerja-upload-package

Paket bukti dukung: docx→pdf→zip + manifest_upload.csv.

## Konteks
- Pemilik: Afrizal Munthe, Pranata Komputer Terampil, Diskominfo Aceh Tengah
- Platform: eKinerja (Kementerian PANRB)

## Struktur Paket
```
output/ekinerja/YYYY-MM-DD-<slug>/
├── bukti-01.docx
├── bukti-01.pdf
├── bukti-02.docx
├── bukti-02.pdf
├── ...
└── manifest_upload.csv
```

## manifest_upload.csv
```
no,nama_file,jenis,tanggal,keterangan
1,bukti-01.pdf,docx→pdf,2026-05-01,Kegiatan rapat koordinasi
2,bukti-02.pdf,docx→pdf,2026-05-02,Laporan bulanan
```

## Pipeline
1. Generate docx dari template
2. Convert docx→pdf (LibreOffice headless)
3. Zip semua pdf
4. Generate manifest_upload.csv
5. Verifikasi: jumlah file, ukuran, integritas zip

## Aturan
- Bahasa Indonesia
- Output ke output/ekinerja/YYYY-MM-DD-<slug>/
- Jangan tulis ke repo publik — repo ini PRIVAT
- Jangan masukkan NIP di nama file
- Verifikasi zip sebelum lapor selesai

## Integrasi
- LibreOffice 26.8.0 (terpasang)
- Template: dinas/asn-admin/templates/
- Data: dinas/asn-admin/data/indikator-skp-*.csv
