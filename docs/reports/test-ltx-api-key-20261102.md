# Test LTX API — Hasil & Kesimpulan
**Tanggal:** 2026-11-02  
**Key:** `ltxv_Otmj***WxEa0` (dari Downloads/ltx-api.md)  
**Status:** Key valid ✅, tapi **saldo kredit kosong** ❌

---

## 1. Verifikasi Key

- Key format valid (`ltxv_...`) ✅
- Endpoint V2 reachable ✅
- Auth diterima (bukan 401) ✅

## 2. Test Generate — Gagal Karena Nol Saldo

```
POST /v2/text-to-video → 202 Accepted
GET /v2/text-to-video/{id} → status: failed
Error: {"type":"insufficient_funds_error","message":"Insufficient funds. Required: 36 cents"}
```

4 detik video 720p fast = **$0.36**. Akun kosong.

## 3. Sistem Billing LTX API

- **Pre-paid credits**, bukan subscription bulanan
- **Minimum purchase: $5** per transaksi
- Credit expire: **1 tahun** dari pembelian
- Non-refundable
- Harga per detik:
  - Fast 720p: $0.09/s → 4s = $0.36
  - Pro 720p: $0.12/s → 4s = $0.48
  - Pro 1080p: $0.17/s → 4s = $0.68

## 4. Cara Top Up

1. Buka https://console.ltx.video
2. Masuk ke **Billing** section
3. Pilih preset ($10, $25, $100) atau custom ($5 minimum)
4. Klik **Pay** → masukkan payment detail (transaksi pertama)
5. Credit masuk **segera** setelah pembayaran

## 5. Estimasi Biaya Pilot

| Skenario | Durasi | Model | Resolution | Biaya |
|---|---|---|---|---|
| Pilot 5 clip | 4s × 5 = 20s | fast | 720p | **$1.80** |
| Pilot 10 clip | 4s × 10 = 40s | fast | 720p | **$3.60** |
| Pilot 20 clip | 4s × 20 = 80s | fast | 720p | **$7.20** |

Dengan top-up minimum $5, bisa generate ~138 detik video 720p fast.

## 6. Rekomendasi

**Langkah berikutnya:**
1. Top up minimal **$5** di https://console.ltx.video/billings/
2. Setelah saldo ada, test lagi 3-5 clip via API
3. Simpan hasil di `project/<slug>/output/` untuk evaluasi quality

**Catatan penting:**
- LTX V1 API sudah **dipensiunkan 26 Okt 2026** — semua request harus pakai `/v2/`
- Flow V2: submit job → poll status → download dari URL
- Key sudah tersimpan di `~/.hermes/.env` sebagai `LTX_API_KEY`

---

## Bukti
- `POST /v2/text-to-video` → 202, job ID `58e32ab8...`
- `GET /v2/text-to-video/58e32ab8...` → 200, `status: failed`, error `insufficient_funds_error`
- Required: $0.36 untuk 4s video 720p fast
- Minimum purchase LTX API: $5 (sumber: help.ltx.io)
