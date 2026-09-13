# Verifikasi Ketersediaan Data Historis Bapokting

**Tanggal verifikasi:** 31 Agustus 2026
**API endpoint:** `https://api-splp.layanan.go.id/bahan-pokok-penting-kabupaten-aceh-tengah/1.0/api/bapokting/harga`

## Temuan

### Data Tersedia
| Tanggal | Jumlah Item | Status |
|---------|-------------|--------|
| 2026-08-31 | 76 | ✅ Live |
| 2026-08-30 | - | ❌ NO DATA |
| 2026-08-24 | 76 | ✅ Live |
| 2026-08-17 | 76 | ✅ Live |
| 2026-08-01 | - | ❌ NO DATA |
| 2026-07-02 | - | ❌ NO DATA |
| 2026-06-02 | - | ❌ NO DATA |
| 2026-03-04 | - | ❌ NO DATA |
| 2025-08-31 | - | ❌ NO DATA |

### Struktur Response
```json
{
  "status": "success",
  "sumber": "DISPERINDAG",
  "tanggal": "2026-08-31",
  "filter_komoditi": "all",
  "total_komoditas": 76,
  "daftar_harga": [
    {
      "id": 3123,
      "komoditi": "Beras 88",
      "kategori": "BARANG KEBUTUHAN POKOK PANGAN PENTING DAN STRATEGIS",
      "satuan": "Kg",
      "harga_borongan": 0,
      "harga_eceran": 16000
    }
  ]
}
```

### Variasi Beras (5 item)
1. Beras 88 - Rp 16.000/Kg
2. Beras 2 Mawar - Rp 16.600/Kg
3. Beras Cap Udang - Rp 14.500/Kg
4. Beras Yusima Super - Rp 16.600/Kg
5. Beras UB - Rp 16.000/Kg

## Kesimpulan

1. **API hanya menyimpan data mingguan** (setiap Senin/Rabu) untuk Agustus 2026.
2. **Tidak ada data historis sebelum Agustus 2026.**
3. **Tidak ada data bulanan/tahunan agregat** — hanya snapshot mingguan.
4. **Implementasi harus handle missing dates gracefully** — skip tanggal tanpa data, jangan asumsikan fill dengan interpolasi.

## Rekomendasi untuk Future Implementation

- Gunakan `weekDates` pattern (interval mingguan) bukan `daily` pattern.
- Tampilkan maksimal 4 titik data di chart line (sesuai ketersediaan API).
- Jika API menambahkan historis di masa depan, update logic dengan validasi dulu.
- Dokumentasikan keterbatasan ini di skill untuk future agent reference.
