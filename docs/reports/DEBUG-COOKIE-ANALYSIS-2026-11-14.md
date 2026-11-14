# Analisis: Menggunakan Cookie Portal ASN untuk Presensi-Rekon

**Tanggal:** 2026-11-14  
**Status:** ❌ TIDAK BISA langsung pakai cookie SSO

---

## Temuan Penting

### 1. API Presensi Tidak Menerima Cookie SSO Langsung
Endpoint `/api/mobile/login` hanya menerima:
```json
{
  "nip": "...",
  "password": "...",
  "device_id": "...",
  "device_name": "..."
}
```
Tidak ada endpoint untuk menukar SSO token → API token.

### 2. Device Binding Adalah Kunci Utama
Server presensi-asn memvalidasi **device_id** per akun:
- Portal ASN bekerja karena device_id-nya sudah terdaftar di server
- Presensi-rekon gagal karena menggunakan device_id berbeda (UUID acak vs fixed UUID)

### 3. Password yang Benar
Dari file `akunSSO-presensi.md`:
- Presensi ASN (direct): password = **NIP itu sendiri** (`199407272022031004`)
- Portal ASN SSO: password = `Met@l666` (berbeda!)

Semua test dengan password yang benar tetap gagal karena device binding aktif.

### 4. Instalasi ID vs Device ID
APK strings menunjukkan:
- `installation_id` = Firebase Installation ID (unik per install app)
- `device_id` = device identifier yang di-hash ke UUID

Portal ASN diinstall dari Play Store → punya installation_id & device_id unik yang terdaftar di server.
Presensi-rekon kita install via ADB → device_id baru belum terdaftar.

## Mengapa Cookie Tidak Bisa Digunakan

| Faktor | Penjelasan |
|--------|-----------|
| Session isolated | WebView cookie di Portal ASN tidak bisa diakses apps lain |
| No shared storage | Different signatures → different userIds → no shared SharedPreferences |
| No token exchange | Tidak ada endpoint untuk konversi SSO session → API auth |
| Device-bound | Server check device_id, bukan session cookie |

## Solusi yang Tersedia

### Opsi 1: Admin Reset Device Binding (PALING SEDERHANA)
Hubungi Admin BKPSDM untuk reset perangkat akun `199407272022031004`.
Setelah reset, coba login di presensi-rekon dengan:
- **NIP:** `199407272022031004`
- **Password:** `199407272022031004` (NIP itu sendiri!)

### Opsi 2: Gunakan Portal ASN Sementara
Karena Portal ASN sudah terkoneksi dan berfungsi, gunakan aplikasi tersebut untuk absen sampai presensi-rekon selesai diselesaikan.

### Opsi 3: Integrasikan SSO Flow (Long-term)
Tingkatkan presensi-rekon untuk menggunakan flow SSO seperti Portal ASN:
1. Buka WebView ke `https://sso.acehtengahkab.go.id`
2. User login dengan kredensial SSO
3. Ambil auth code / session
4. Tukar dengan API token via `/api/mobile/sso/login`

Ini akan bypass device binding karena SSO session tidak terikat device_id.

---
