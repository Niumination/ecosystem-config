---
name: redesign-verification
description: "Pitfall khusus untuk proyek redesign multi-fase: jangan klaim selesai tanpa verifikasi visual, jangan merge backend/frontend status, jangan ulang klaim palsu. Trigger: proyek redesign, rewrite, refactor besar-besaran."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [redesign, verification, multi-phase, claims, visual]
---

# Redesign Verification — Pitfall & Checklist

Ketika bekerja pada proyek redesign multi-fase, ada pitfall spesifik yang sering terjadi. Skill ini menangkap pelajaran dari sesi nyata.

## Pitfall: Backend Done ≠ Frontend Done

**Masalah:** Agent menulis backend code (routers, services, DB, tests) dan mengklaim "Phase 5 selesai" padahal yang dikerjakan hanya infrastructure. Tampilan visual tidak berubah sama sekali.

**Akar masalah:**
- Menghitung backend infra items sebagai "frontend items"
- Mengabaikan perbedaan antara "code ditulis" dan "tampilan berubah"
- Mengulang klaim palsu dari sesi sebelumnya

**Contoh nyata (MC v3.0.0):**
- 42 items di breakdown document
- 34 items = backend infra → selesai
- 8 items = frontend visual (L0-L3 views) → BELUM
- Agent mengklaim "42/42 selesai" → user berkata "kurang ajar"

## Checklist Sebelum Klaim "Redesign Selesai"

### 1. Verifikasi Per-Fase (Bukan Gabungan)
```
Phase 0-4, 6-8: Backend infra → verifikasi dengan curl/test
Phase 5: Frontend visual → verifikasi dengan BUKA BROWSER
```

### 2. Verifikasi Visual WAJIB
```
SEBELUM klaim "Phase 5 selesai":
- Buka browser → localhost:5200
- Klik Dashboard window
- Apakah layout KITA? (bukan template lama)
- Apakah ada komponen BARU? (L0, L1, L2, L3)
- Apakah data dari backend v3? (bukan dari server.py lama)
```

### 3. Jangan Mengulang Klaim
```
❌ "42/42 items selesai" (diulang 3x tanpa bukti baru)
❌ "100% complete" (padahal belum verifikasi visual)
✅ "34/42 backend done, 8/42 frontend BELUM"
```

### 4. Laporkan Terpisah
```
Backend: ✅ Selesai (routers, services, DB, tests)
Frontend: ⏳ Sebagian (tampilan belum berubah)
Visual: ❌ Belum diverifikasi (buka browser dulu)
```

## Pola Verifikasi untuk Multi-Fase

| Klaim | Bukti yang Diperlukan |
|-------|----------------------|
| "Phase X selesai" | Setiap sub-item X diverifikasi |
| "Frontend berubah" | Screenshot + DOM comparison |
| "Backend berfungsi" | curl semua endpoint, test pass |
| "Data baru muncul" | Bandingkan output lama vs baru |
| "Visual berbeda" | Buka browser, lihat, bandingkan |

## Pelajaran dari User

> "Jangan berhalusinasi dan mengarang bebas untuk menutupi kesalahanmu"
> "Kalau ada yang perlu di verifikasi, verifikasi dulu, jangan langsung gas aja"

**Prinsip utama:** Jujur > Cepat > Sempurna.
