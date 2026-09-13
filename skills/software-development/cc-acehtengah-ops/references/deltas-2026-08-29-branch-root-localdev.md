# Deltas 29-Agu-2026: Branch Sync, DTSEN_ROOT, Local Dev

Ringkasan perubahan operasional cc-acehtengah yang terjadi di sesi 29-Agu-2026,
melengkapi SKILL.md utama (yang mungkin belum memuatnya).

## 1. Branch state — main = hotfix (SUDAH SINKRON)

- `main` dan `hotfix/meeting-ready` **identik** (fast-forward, `e07edae`, 29-Agu).
  Jangan lagi menganggap main "tertinggal 44+ commit" — itu sudah usang.
- Branch dihapus: `hotfix/llm-reliability` (tanpa commit unik) dan
  `pabrik-aplikasi` (remote-only, proyek GAS nyasar) — `git push origin --delete <b>`.
- Branch arsip yang dipertahankan: `feat/ai-executive-answer-v1/v2/v3` +
  `backup/feat-v3-saved`. JANGAN di-merge — fiturnya sudah di-cover ulang di main
  dengan desain lebih baik (k-anonymity, audit trail, enkripsi).
- Verifikasi sinkron: `git rev-list --count main..hotfix` dan sebaliknya harus 0.

## 2. Role DTSEN_ROOT — otoritas tertinggi (di atas SUPERADMIN)

- `AdminRole` kini: `ADMIN`, `SUPERADMIN`, `DTSEN_ANALYST`, `DTSEN_LOOKUP`, **`DTSEN_ROOT`**.
- DTSEN_ROOT satu-satunya yang melihat **BNBA lengkap** (nama asli + NIK terdekripsi).
  SUPERADMIN tetap nama termask (UU PDP).
- Akun: `dtsen_root` (password di vault/cc-acehtengah.env — sudah diganti manual oleh user).
- Buat role: `ALTER TYPE "AdminRole" ADD VALUE IF NOT EXISTS 'DTSEN_ROOT'` di DB live
  + tambah enum di prisma/schema.prisma + `ROLES_AGGR`/`ROLES_PERSONAL` di
  src/lib/data-gate.ts (`'DTSEN_ROOT'` di kedua array) + `canWrite`/`canRead` di
  halaman admin DTSEN (`role === 'DTSEN_ROOT'`).
- Setup route `CREATE TYPE "AdminRole"` juga harus menyertakan `'DTSEN_ROOT'`.

## 3. Identitas terenkripsi — namaAsliEnc/nikEnc (AES-256-GCM)

- Kolom `DtsenIndividu.namaAsliEnc` + `nikEnc` (TEXT) menyimpan nama asli & NIK
  **terenkripsi AES-256-GCM** — TIDAK pernah plaintext. NIK lookup tetap via
  `nikHash` (HMAC).
- Key: `DTSEN_DATA_KEY` (base64url, ≥32 byte) — Vercel env Production + `.env.local`.
  **WAJIB dijaga**: tanpa key ini, data BNBA tidak bisa didekripsi.
- Helper: `src/lib/dtsen-crypto.ts` — `encryptField`, `decryptField`,
  `canSeeFullIdentitas(role)` (true hanya `DTSEN_ROOT`).
- Format ciphertext: `base64(iv(12B) || tag(16B) || ciphertext)`.
- Endpoint breakdown scope=individu: untuk DTSEN_ROOT kembalikan
  `{nama: decryptField(namaAsliEnc), nik: decryptField(nikEnc)}` + flag
  `fullIdentitas: true`; role lain `{nama: namaMasked}`. Audit `BREAKDOWN_INDIVIDU`
  tetap wajib untuk SEMUA role.
- Re-import data besar via script Node lokal (bukan API — Vercel payload limit):
  `node --env-file=.env.local script.mjs` (dotenv biasa TIDAK memuat .env.local!).

## 4. Local dev — menjalankan cc-acehtengah di localhost

```bash
cd ~/Desktop/Niumination/services/cc-acehtengah
npm run dev          # → http://localhost:3000 (Next.js Turbopack, ~1s ready)
```

- Prasyarat `.env.local`: `DATABASE_URL`, `AI_BASE_URL/API_KEY/MODEL` (huancheng),
  `DTSEN_NIK_KEY`, `DTSEN_DATA_KEY`, dan **`JWT_SECRET`**.
- **`JWT_SECRET` tidak ada di .env.local & tidak bisa di-pull dari Vercel
  (sensitive → placeholder `[SENSITIVE]`)**. Untuk dev lokal: generate sendiri
  (`python3 -c "import secrets; print(secrets.token_urlsafe(48))"`) dan append ke
  `.env.local`. Sesi lokal tidak harus kompatibel dengan produksi.
- Cek env lengkap: `python3 -c "..."` scan key yang dibutuhkan; health:
  `curl localhost:3000/api/health`, halaman `GET /dashboard` → 200.
- Node 26 OK (engine >=20). Port 3000 bebas.

## 5. Pitfall Node script + dotenv

`dotenv.config({ path: '.env.local' })` di script .mjs TIDAK memuat .env.local
dengan benar di environment ini (prisma konek ke host salah `db...:5432`).
**Selalu jalankan script Node yang butuh env dengan `node --env-file=.env.local`**
— terbukti berhasil (import 235.011 baris, migrate ALTER TYPE, dsb).
