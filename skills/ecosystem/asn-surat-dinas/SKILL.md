---
name: asn-surat-dinas
description: Generate surat dinas. Use for Diskominfo Aceh Tengah.
---

# asn-surat-dinas

Generate surat dinas, nota dinas, dan telaahan staf sesuai Permendagri 1/2023 dan pola penomoran Aceh Tengah.

## Konteks
- Pemilik: Afrizal Munthe, Pranata Komputer Terampil, Diskominfo Aceh Tengah
- Regulasi: Permendagri 1/2023 (Format Naskah Dinas)
- Referensi: dinas/asn-admin/references/FORMAT-NASKAH-DINAS.md
- Identitas: dinas/asn-admin/references/IDENTITAS-PEGAWAI.md

## Jenis Surat
1. Surat Dinas — komunikasi resmi antar OPD/instansi
2. Nota Dinas — komunikasi internal dalam satu OPD
3. Telaahan Staf — analisis dan rekomendasi untuk pimpinan

## Struktur Surat Dinas (Permendagri 1/2023)
```
KOP SURAT (logo + nama instansi + alamat)

NOMOR    : [nomor surat]
LAMPIRAN : [lampiran]
HAL      : [perihal]

Yth. [penerima]
Di [tempat]

[isi surat]

Hormat kami,
[tanda tangan + nama + NIP + jabatan]

Tembusan: [daftar tembusan]
```

## Penomoran Aceh Tengah
Format: [nomor]/[kode OPD]/[bulan]/[tahun]
- Kode OPD Diskominfo: DISKOMINFO
- Contoh: 001/DISKOMINFO/05/2026

## Aturan
- Bahasa Indonesia baku dan formal
- Gunakan kop surat dari references/KOP-SURAT.md
- Tanda tangan manual (agent tidak menandatangani)
- Output ke output/surat-dinas/YYYY-MM-DD-<slug>/ berisi .md + .docx + .pdf + meta.json
- Jangan tulis ke repo publik — repo ini PRIVAT
- Jangan masukkan NIP di nama file (gunakan slug tanpa NIP)

## Template
Lihat dinas/asn-admin/templates/ untuk template surat dinas.

## Integrasi
- Identitas pegawai: references/IDENTITAS-PEGAWAI.md
- Format: references/FORMAT-NASKAH-DINAS.md
- Regulasi: references/REGULASI-KINERJA-ASN.md
