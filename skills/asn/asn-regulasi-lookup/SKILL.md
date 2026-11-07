---
name: asn-regulasi-lookup
description: Cari pasal peraturan. Use for regulation lookup.
---

# asn-regulasi-lookup

Cari & kutip pasal dari peraturan.go.id / JDIH BPK dengan verifikasi sumber.

## Konteks
- Pemilik: Afrizal Munthe, Pranata Komputer Terampil, Diskominfo Aceh Tengah
- Tujuan: mengurangi hal-hal [UNCHECKED] dalam dokumen kedinasan

## Sumber Resmi
1. **peraturan.go.id** — peraturan pusat (UU, PP, Perpres, Permen)
2. **jdih.bpk.go.id** — JDIH BPK (peraturan daerah, peraturan bupati)
3. **jdih.acehprov.go.id** — JDIH Aceh
4. **jdih.acehtengahkab.go.id** — JDIH Aceh Tengah (jika tersedia)

## Prosedur
1. Identifikasi peraturan yang dibutuhkan (nama, nomor, tahun)
2. Cari di sumber resmi (web_search atau web_extract)
3. Verifikasi: nomor, tahun, judul, status (berlaku/dicabut)
4. Kutip pasal yang relevan dengan nomor pasal dan ayat
5. Catat sumber: [UNCHECKED] jika belum terverifikasi, [VERIFIED] jika sudah

## Format Kutipan
```
Pasal X Ayat (Y) [Nama Peraturan] Nomor [nomor] Tahun [tahun]:
"[isi pasal]"
Sumber: [URL] — [VERIFIED/UNCHECKED]
```

## Aturan
- Selalu verifikasi sumber sebelum mengutip
- Jangan mengarang pasal — jika tidak ditemukan, tulis [UNCHECKED]
- Prioritaskan peraturan yang berlaku (bukan yang dicabut)
- Catat status peraturan (berlaku/dicabut/diganti)

## Integrasi
- Referensi regulasi: dinas/asn-admin/references/REGULASI-KINERJA-ASN.md
- Skill terkait: grounded-citations
