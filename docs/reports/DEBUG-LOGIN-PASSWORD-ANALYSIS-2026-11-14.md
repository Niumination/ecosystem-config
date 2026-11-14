# Debug Login: Password Analysis & Device Binding Issue

**Tanggal:** 2026-11-14  
**Status:** 🔍 Ditemukan - Ada masalah device binding yang perlu Admin

---

## Temuan Kunci: Dua Password Berbeda!

Dari file `Downloads/akunSSO-presensi.md`:

| Aplikasi | NIP | Password |
|----------|-----|----------|
| Presensi ASN (direct) | 199407272022031004 | `199407272022031004` (NIP itu sendiri!) |
| Portal ASN SSO | 199407272022031004 | `Met@l666` |

**Password untuk presensi-rekon TIDAK SAMA dengan SSO password!**

User sebelumnya mencoba login dengan password SSO (`Met@l666`) ke presensi-rekon, padahal seharusnya pakai `199407272022031004`.

## Testing Hasil

### Dengan Password SSO (Met@l666):
```
{"message":"NIP atau password salah."} HTTP: 422
```
❌ Password salah untuk direct login.

### Dengan Password NIP (199407272022031004):
```
{"message":"Akun Anda terikat pada perangkat lain!"} HTTP: 422
```
✅ Password benar! Tapi device_id belum terdaftar di server.

### Semua device_id yang dicoba → selalu "device bound":
- Fixed UUID dari APK: `0d5dafd8-d08f-4093-bdbd-4e47f0fe3330`
- Random UUID baru setiap test
- Android ID: `f55eca002861ff92`

## Root Cause

Server presensi-asn melakukan **device binding** per akun NIP:
- Setiap akun hanya bisa login dari **satu device_id tertentu**
- Original app sudah terdaftar dengan device_id spesifik di server
- Presensi-rekon menggunakan device_id berbeda → ditolak

## Solusi

**Admin BKPSDM perlu mereset device binding kembali:**
1. Buka halaman admin presensi
2. Cari akun NIP `199407272022031004`
3. Reset/unbind device
4. User coba login lagi dengan password: `199407272022031004`

## Informasi Teknis Tambahan

- Login endpoint: `POST /api/mobile/login`
- SSO endpoint tersedia: `POST /api/mobile/sso/login`
- Portal ASN menggunakan SSO flow (webview Keycloak) yang mungkin bypass device binding
- App package: `id.go.acehtengahkab.presensi_asn` (belum ada shared UID dengan portalasn)
- Different signatures: portalasn=`194fb7e3`, presensi_asn=`e5a9b169`

## Rekomendasi

1. **Short term:** Hubungi Admin BKPSDM untuk reset device binding sekali lagi
2. **Long term:** Pertimbangkan untuk integrate SSO login flow (menggunakan `/api/mobile/sso/login` dengan token dari Keycloak) agar tidak tergantung device binding

---
