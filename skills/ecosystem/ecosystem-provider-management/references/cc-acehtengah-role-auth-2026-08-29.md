# Role DTSEN auth — enum Prisma vs data-gate mismatch (cc-acehtengah, 29 Agu 2026)

Kasus: user bertanya "akun dtsen role sudah dibuat belum?" — jawaban investigasi
adalah BELUM DAN TIDAK BISA, karena bug sistem. Pelajaran: saat role tertentu
"tidak bisa dibuat", cek DUA sumber kebenaran yang bisa tidak sinkron.

## Gejala

- Akun dengan role `DTSEN_ANALYST`/`DTSEN_LOOKUP` tidak pernah ada; admin yang
  ada cuma `role: ADMIN`.
- Simulasi `decideDataAccess('ADMIN', 'RESTRICTED_AGGR')` → `403 ROLE_INSUFFICIENT`,
  padahal app punya fitur role-gated DTSEN (`/api/dtsen/source`, `/api/dtsen/query`).

## Root cause: dua sumber kebenaran role tidak sinkron

| Sumber | Isi | Peran |
|--------|-----|-------|
| `prisma/schema.prisma` → `enum AdminRole` | `ADMIN, SUPERADMIN` (tadinya) | menentukan role yang bisa DISIMPAN di DB |
| `src/lib/data-gate.ts` → `ROLES_AGGR` / `ROLES_PERSONAL` | `DTSEN_ANALYST`, `DTSEN_LOOKUP`, `SUPERADMIN` | menentukan role yang DITERIMA saat akses |

Gap di enum = role yang dibutuhkan gate **tidak bisa dibuat lewat app** (setup
admin hanya seed role `ADMIN`).

## Fix 3 lapis (commit `2a47a50`)

1. **Schema:** tambah `DTSEN_ANALYST` + `DTSEN_LOOKUP` ke `enum AdminRole`.
2. **DB live** — enum Postgres TIDAK auto-migrate dari edit schema saja:
   ```sql
   ALTER TYPE "AdminRole" ADD VALUE IF NOT EXISTS 'DTSEN_ANALYST';
   ALTER TYPE "AdminRole" ADD VALUE IF NOT EXISTS 'DTSEN_LOOKUP';
   ```
   via script node `prisma.$executeRawUnsafe(...)`. Verifikasi:
   `SELECT enumlabel FROM pg_enum e JOIN pg_type t ON e.enumtypid=t.oid WHERE t.typname='AdminRole'`.
   Juga update `CREATE TYPE "AdminRole" AS ENUM (...)` di
   `src/app/api/setup/admin/route.ts` (fallback SQL manual) agar fresh setup konsisten.
3. **Endpoint baru** `POST /api/setup/dtsen-role`:
   - body `{username, password (min 8), role: DTSEN_ANALYST|DTSEN_LOOKUP, nama}`
   - wajib header `x-setup-token` cocok env `ADMIN_SETUP_TOKEN` (fail-closed 403 tanpa env)
   - upsert: akun ada → upgrade role; tidak ada → create (bcrypt cost 12)
   - SUPERADMIN sengaja tidak dibuat lewat endpoint ini

## Cara cepat: buat akun langsung di DB (tanpa token)

Saat user tidak punya `ADMIN_SETUP_TOKEN` dan setuju jalur DB langsung:
- script node di repo (biar resolve `@prisma/client`): Prisma + bcryptjs +
  `crypto.randomBytes(12).toString('base64url').slice(0,16)` → password acak sekali-tampil,
  hash bcrypt cost 12, `prisma.admin.create({username, password: hash, nama, role})`.
- ⚠️ Password hanya dicetak sekali di stdout — ingatkan user segera ganti.
- Taruh script di repo dulu (`cp` dari /tmp), jalankan, lalu `rm` — jangan biarkan
  file dengan password tersisa.

## Verifikasi role-gate live (pola penting)

1. `POST /api/auth/login` dengan kredensial baru → cek `admin.role` di respons = role yang diharapkan.
2. Panggil route role-gated (mis. `GET /api/dtsen/source?type=aggr&source=splp`) dengan cookie login.
3. Interpretasi: **error DATA** (mis. `SPLP API error 401`) = gate role LOLOS (403 tidak muncul);
   **error `403 ROLE_INSUFFICIENT`** = gate menolak. Jangan salah kaprah: error data
   eksternal justru bukti otorisasi sukses.

## Kaitan dengan konteks DTSEN yang lebih luas

- SPLP DTSEN API masih 401 (`Invalid Credentials`) — butuh JWT baru dari tim SPLP
  (Portal SDI Kemensos). Ganti `SPLP_API_KEY` di Vercel env + `.env.local`; pipeline
  otomatis pakai SPLP dulu, lalu BAPPEDA offline (`DTSEN (BAPPEDA Des 2025 — offline)`).
- Data sensitif TIDAK tampil di output AI publik: NIK/per-orang di-defleksi,
  output agregat k-anonymity k≥5, raw CSV PII git-ignored, LLM hanya lihat statistik.
- Role: `DTSEN_ANALYST` = agregat saja; `DTSEN_LOOKUP` = agregat + lookup by-NIK
  (nama dimasked, audit trail, UU 27/2022).
