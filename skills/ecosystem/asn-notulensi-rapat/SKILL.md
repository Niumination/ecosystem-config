---
name: asn-notulensi-rapat
description: Generate notulensi rapat. Use for Diskominfo meetings.
---

# asn-notulensi-rapat

Menit rapat → notulensi + action items + surat undangan berikutnya.

## Konteks
- Pemilik: Afrizal Munthe, Pranata Komputer Terampil, Diskominfo Aceh Tengah
- Regulasi: Permendagri 1/2023 (Format Naskah Dinas)

## Struktur Notulensi
```
NOTULENSI RAPAT

Hari/Tanggal : [hari, tanggal]
Waktu        : [jam mulai] - [jam selesai]
Tempat       : [tempat]
Agenda       : [agenda]
Pimpinan     : [nama pimpinan]
Peserta      : [daftar peserta]

I. PEMBAHASAN
[ringkasan pembahasan per poin agenda]

II. KEPUTUSAN
[daftar keputusan]

III. ACTION ITEMS
| No | Tugas | PIC | Tenggat |
|----|-------|-----|---------|
| 1  | ...   | ... | ...     |

IV. RAPAT BERIKUTNYA
Tanggal: [tanggal]
Agenda: [agenda]
```

## Aturan
- Bahasa Indonesia baku
- Action items wajib ada PIC dan tenggat
- Output ke output/notulensi/YYYY-MM-DD-<slug>/ berisi .md + .docx + .pdf + meta.json
- Jangan tulis ke repo publik — repo ini PRIVAT
- Jangan masukkan NIP di nama file

## Integrasi
- Surat undangan berikutnya: gunakan skill asn-surat-dinas
- Action items: gunakan skill document-to-action-items (jika tersedia)
