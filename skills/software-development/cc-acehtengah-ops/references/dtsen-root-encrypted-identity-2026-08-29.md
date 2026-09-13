# 29-Agu-2026 (final round): DTSEN_ROOT role, AES-encrypted full identity, demo removal

Companion to `breakdown-individu-login-ux-2026-08-29.md`. Captures the last user
round: **SUPERADMIN is NOT the top authority** — user demanded a higher role that
can see BNBA (By-Name By-Address) fully unsensitized, for application development.

## User decision (FIRST-CLASS)

- Asked: "apakah superadmin adalah otoritas paling tinggi? jika ada buatkan
  otoritas paling tinggi agar dapat mendapatkan hasil lengkap tanpa sensor".
- Answer implemented: **SUPERADMIN bukan tertinggi**. New role `DTSEN_ROOT` =
  tertinggi, dapat **nama asli + NIK lengkap** (decrypted server-side) di
  breakdown per-orang. Role lain tetap nama termask (UU 27/2022).

## Hierarchy (final)

```
publik < ADMIN / DTSEN_ANALYST < DTSEN_LOOKUP < SUPERADMIN < DTSEN_ROOT
```

## Data model: encrypted full identity (NOT plaintext)

- `DtsenIndividu` + kolom `namaAsliEnc TEXT?`, `nikEnc TEXT?` — AES-256-GCM.
- Key: `DTSEN_DATA_KEY` (43-char base64url, `secrets.token_urlsafe(32)`) di
  Vercel Production + `.env.local`. Simpan juga di vault.
- Helper `src/lib/dtsen-crypto.ts`: `encryptField` / `decryptField` /
  `canSeeFullIdentitas(role)` (hanya `DTSEN_ROOT` → true).
- Format: `base64( iv(12B) || tag(16B) || ciphertext )`.
- Re-import: `/tmp/transform_dtsen_v2.py` CSV → script node dengan
  `node --env-file=.env.local reimport_v3.mjs` — 235.011 baris, chunk 3000,
  purge semua rilis lama → STAGING → publish atomik → PUBLISHED. ~17 menit.

## Endpoint behavior (verified live)

- `GET /api/dtsen/breakdown?scope=individu&kecamatan=&desa=&desil=` :
  - publik → 401 + blocker + tombol **🔐 Login untuk melanjutkan**
    (`/login?from=%2Fdashboard` — login page pakai param `from`, bukan `next`).
  - DTSEN_LOOKUP/SUPERADMIN → `fullIdentitas:false`, nama termask.
  - DTSEN_ROOT → `fullIdentitas:true`, `nama` asli + `nik` 16 digit.
- Audit: action `BREAKDOWN_INDIVIDU` di union `AuditAction` (data-gate.ts),
  mapping `action: entry.aksi` manual.

## Pitfalls this round

- **Filter kecamatan/desa WAJIB `mode:'insensitive'`**: DB simpan UPPERCASE
  ("LINGE"), `detectKecamatan` kembalikan bentuk kamus ("Linge") → filter
  `{equals: x}` tanpa insensitive = 0 baris (Postgres case-sensitive). Gejala:
  "desil 1-2 di Kecamatan Linge" → "Tidak ada baris agregat" padahal data ada.
  Fix di `/api/dtsen/query` + `fetchDtsenAgregatDb` (dtsen-planner.ts).
- **Script Node lokal: `node --env-file=.env.local`** — `dotenv.config`
  TIDAK memuat .env.local dengan benar di script .mjs (koneksi Prisma ke host
  salah / `PrismaClientInitializationError`). Flag Node bawaan stabil untuk
  import/migrate 235k baris.
- Vercel env berubah → **REDEPLOY wajib** (env baru tidak ter-apply ke
  deployment lama). Gejala: hash key baru tidak match di prod sampai redeploy.
- Supabase direct 5432 sering unreachable dari lokal; pooler 6543 stabil.
