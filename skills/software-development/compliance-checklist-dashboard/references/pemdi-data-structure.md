# Pemdi Aceh Tengah — Data Structure Reference

## Framework
- **Regulation:** PermenPANRB No. 8 Tahun 2026
- **Scope:** 7 Aspek, 20 Indikator, 57 Bukti Dukung
- **Baseline:** SPBE 2025 = 2.59 (Cukup)
- **Target:** Indeks ≥ 2.50 (Baik)

## Aspek Structure

| Aspek | Nama | Bobot | Indikators | Bukti Items | Koordinator |
|:---:|---|:---:|:---:|:---:|---|
| 1 | Tata Kelola dan Manajemen | 10% | I1-I2 | 6 | BAPPEDA |
| 2 | Penyelenggara | 10% | I3-I4 | 8 | BKPSDM; Bag. Organisasi; Bag. Hukum |
| 3 | Data | 15% | I5-I8 | 12 | Diskominfo – Bid. Statistik & Persandian |
| 4 | Keamanan Pemerintah Digital Siber | 15% | I9-I12 | 9 | Inspektorat; Diskominfo |
| 5 | Teknologi Digital | 10% | I13-I14 | 6 | Kabid TIK; Kabid E-Gov – Diskominfo |
| 6 | Keterpaduan | 15% | I15-I18 | 8 | Bag. Organisasi; BAPPEDA; Diskominfo |
| 7 | Kepuasan Pengguna | 25% | I19-I20 | 8 | DPMPTSP; Diskominfo |

## Indicator IDs and Names

| ID | Aspek | Nama |
|---|:---:|---|
| I1 | 1 | Tingkat Kematangan Tata Kelola Pemerintah Digital |
| I2 | 1 | Tingkat Kematangan Manajemen Layanan Digital Pemerintah |
| I3 | 2 | Tingkat Kematangan Sumber Daya Manusia Pemerintah Digital |
| I4 | 2 | Tingkat Kematangan Kolaborasi Pemerintah Digital |
| I5 | 3 | Tingkat Kematangan Tata Kelola Data (SDI) |
| I6 | 3 | Tingkat Kematangan Informasi Geospasial (SJIG) |
| I7 | 3 | Tingkat Kematangan Pembangunan Statistik (EPSS) |
| I8 | 3 | Tingkat Kematangan Pelindungan Data Pribadi |
| I9 | 4 | Tingkat Kematangan Pelaksanaan Audit Keamanan |
| I10 | 4 | Tingkat Kematangan Keamanan Siber (IKASANDI) |
| I11 | 4 | Tingkat Kematangan Kriptografi untuk Keamanan Data |
| I12 | 4 | Tingkat Kematangan Kapabilitas Penanganan Insiden Siber |
| I13 | 5 | Tingkat Kematangan Aplikasi Pemerintah Digital |
| I14 | 5 | Tingkat Kematangan Infrastruktur Pemerintah Digital |
| I15 | 6 | Tingkat Kematangan Keterpaduan Proses Bisnis |
| I16 | 6 | Tingkat Kematangan Integrasi Aplikasi |
| I17 | 6 | Tingkat Kematangan Portal Layanan Digital |
| I18 | 6 | Tingkat Kematangan Interoperabilitas Data |
| I19 | 7 | Tingkat Kematangan Fasilitas Dukungan Pengguna |
| I20 | 7 | Tingkat Kematangan Pengelolaan Kepuasan Pengguna |

## Bukti Dukung ID Convention

`B{aspek}.{number}` — sequential per aspek

Examples:
- B1.1, B1.2, B1.3, B1.4 (Aspek 1, items 1-4)
- B12.1, B12.2, B12.3 (Aspek 4/Indikator 12, items 1-3)
- B20.1, B20.2, B20.3, B20.4 (Aspek 7/Indikator 20, items 1-4)

## Pokja (Working Groups)

| Pokja | Nama | Koordinator |
|:---:|---|---|
| 1 | Tata Kelola dan Manajemen | Kepala BAPPEDA |
| 2 | Penyelenggara | Kepala BKPSDM; Kabag Organisasi; Kabag Hukum |
| 3 | Data | Kabid Statistik dan Persandian – Diskominfo |
| 4 | Keamanan Siber | Inspektorat; Diskominfo – Bid. Statistik & Persandian |
| 5 | Teknologi Digital | Kabid TIK; Kabid E-Gov – Diskominfo |
| 6 | Keterpaduan | Kabag Organisasi; Kepala BAPPEDA; Kabid E-Gov; Kabid TIK; Kabid Statistik & Persandian |
| 7 | Kepuasan Pengguna | Kepala DPMPTSP; Kabid E-Gov – Diskominfo |

## Status Distribution (after 42-file verification)

| Status | Count | Notes |
|---|:---:|---|
| Lengkap | 2 | SP4N-LAPOR (I19), SKM Dukcapil/Kebayakan (I20) |
| Proses | 22 | Public evidence found, needs formal verification |
| Belum | 33 | Must request from OPD |
| **Total** | **57** | |

## File Locations
- **Data:** `data/pemdi.json`
- **Page:** `pages/pemdi.js`
- **Evidence:** `public/bukti-dukung/` (42 files)
- **Original source:** `docs/pemdi-evaluasi-2026/` (official SK/XLSX)
