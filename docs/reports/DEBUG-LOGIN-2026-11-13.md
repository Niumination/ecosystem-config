# Laporan Debug Login — Presensi ASN

**Tanggal:** 2026-11-13  
**Status:** ✅ Error sudah di-fix, pesan server ditampilkan dengan benar

---

## Masalah

User mencoba login dengan NIP `199407272022031004` dan mendapat error:
```
Network error: badResponse - status code 422
```

Error ini terjadi karena Dio library secara default melempar exception untuk semua response selain 2xx (200-299). Server mengembalikan 422 Unprocessable Entity untuk validasi gagal, yang seharusnya diparse menjadi pesan error yang User-friendly.

---

## Root Cause

Server merespons dengan format:
```json
{
  "message": "Akun Anda terikat pada perangkat lain! Silakan hubungi Admin BKPSDM untuk reset perangkat.",
  "errors": {
    "device_id": ["Akun Anda terikat pada perangkat lain! ..."]
  }
}
```

Tapi app menangani ini sebagai exception karena `validateStatus` Dio default hanya accept 2xx.

---

## Perbaikan

### 1. `lib/core/api/client.dart`
Tambahkan `validateStatus` untuk accept semua response < 500:
```dart
_validateStatus: (status) => status != null && status < 500,
```

### 2. `lib/features/auth/login_provider.dart`
Tambahkan handler khusus untuk `DioException`:
```dart
on DioException catch (e) {
  print('DEBUG: DioError type=${e.type}, message=${e.message}...');
  state = LoginState(loading: false, error: 'Network error: ${e.type.name}...');
}
```

---

## Hasil Setelah Fix

Login dengan NIP `199407272022031004` sekarang menampilkan pesan error dari server:
```
Akun Anda terikat pada perangkat lain! Silakan hubungi Admin BKPSDM untuk reset perangkat.
```

Ini adalah **behavior yang benar** — NIP tersebut sudah terdaftar di device lain.

---

## Solusi Untuk User

Untuk bisa login, user perlu:
1. **Hubungi Admin BKPSDM** untuk reset device binding akun tersebut, ATAU
2. **Gunakan NIP lain** yang belum terdaftar di device lain

---

## API Test Verification

```bash
# CSRF Cookie
curl -X GET https://presensi-asn.acehtengahkab.go.id/sanctum/csrf-cookie
# Response: 204, Set-Cookie: XSRF-TOKEN, presensi-asn-session

# Login endpoint
curl -X POST https://presensi-asn.acehtengahkab.go.id/api/mobile/login \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"nip":"TEST","password":"TEST","device_name":"Test","device_id":"test"}'
# Response: 422 {"message":"NIP atau password salah."}
```

API server berfungsi normal. Error yang muncul adalah validasi bisnis dari server (akun sudah terikat device lain), bukan bug aplikasi.

---

## Commit

- `20570b3` Fix: handle 422 response properly, show server error messages
