# Restore route .bak + import data sensitif + lookup NIK role-aware (cc-acehtengah, 29 Agu 2026)

Lanjutan dari `cc-acehtengah-role-auth-2026-08-29.md`. Setelah role bisa dibuat,
user tanya "belum bisa melihat data sensitif". Dua lapis akar masalah + fix:

## Akar masalah 1: route DTSEN masih `.bak` (nonaktif)

Commit `1c5809d` (27 Agu, "skip TS build errors utk meeting ready") me-rename
5 route DTSEN ke `.bak` karena schema belum ada di DB. Saat DB sudah punya
tabel, `.bak` TIDAK bisa di-copy begitu saja:

- Route `.bak` ditulis untuk **schema LAMA**: `DtsenRelease{versi, jalur,
  totalBaris, ditolak, checksum, uploadedBy}`, `DtsenIndividu{statusBansos
  JSONB}`, `DtsenAgregatWilayah{jumlahJiwa, jumlahKeluarga}`.
- DB aktual (dibuat db-migration + prisma) memakai **schema BARU**:
  `releaseNumber`, `metadata Json`, `DtsenIndividu{bansos Boolean}`,
  `DtsenAgregatWilayah{jiwa, kk, pkh, bpnt, pbi_kredit, pbi_nonkredit}`.

**Pelajaran:** saat merestore route `.bak`, cek struktur KOLOM aktual DB
(`information_schema.columns`) dan `prisma/schema.prisma` — jangan asal
`mv .bak route.ts`. Adaptasi field: versi/jalur/totalBaris → taruh di
`metadata` (Json), `statusBansos{pkh,bpnt,pbi}` → `bansos: pkh||bpnt||pbi`,
`jumlahJiwa/jumlahKeluarga` → `jiwa/kk`. Audit: `buildAuditEntry` mengembalikan
`{adminId, adminNama, aksi, detail, rowCount, ip}` tapi model `DataAccessAudit`
pakai kolom `action` (bukan `aksi`) — map manual saat create.

## Akar masalah 2: DB kosong + DTSEN_NIK_KEY tidak konsisten

- Import via API gagal: **Vercel serverless punya batas payload ~4.5MB**
  (`FUNCTION_PAYLOAD_TOO_LARGE`) — CSV 6.7MB ditolak walau limit route 10MB.
- `DTSEN_NIK_KEY` (HMAC NIK) hanya ada di Vercel env (hidden, tidak bisa di-pull
  `vercel env pull` → placeholder `[SENSITIVE]`). Import lokal dengan key beda →
  hash beda → lookup di Vercel "NIK tidak tercatat".

**Fix konsisten key (pola penting):** jangan coba baca key lama — generate key
BARU, set di KEDUA sisi, baru import:
1. `NEWKEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")`
2. `vercel env rm DTSEN_NIK_KEY production --yes` lalu `echo "$NEWKEY" | vercel env add DTSEN_NIK_KEY production`
3. Tulis ke `.env.local` juga.
4. ⚠️ **Setelah ganti env Vercel, WAJIB redeploy** (`vercel deploy --prod --yes`)
   — env baru tidak berlaku pada deployment lama. Gejala: import OK tapi lookup
   "NIK tidak tercatat" → tandanya deployment masih pakai key lama.

## Import data besar langsung ke DB (bypass payload limit)

CSV 222.655 baris → script node di repo (resolve `@prisma/client`):
- Parse CSV template `nik,nama,no_kk,kecamatan,desa,desil,pkh,bpnt,pbi_jk`
  (bukan delimiter `|` BAPPEDA asli — transform dulu ke koma + header template).
- Per baris: `nikHash = hmac(nik, SECRET)`, `namaMasked` (char pertama + '*'
  tengah + char terakhir), `bansos = pbi_jk||pkh||bpnt`.
- `DtsenRelease.create` dengan `id: crypto.randomUUID()` (prisma `@id` tanpa
  default — wajib isi eksplisit), `metadata` berisi versi/jalur/checksum.
- `dtsenIndividu.createMany` chunk 5000.
- Publish atomik: aggregate `buildAgregatWilayah`-style (kelompok
  kecamatan|desa|desil, sensor k<5) → `dtsenAgregatWilayah.createMany` →
  `status: 'PUBLISHED'` + `publishedAt` → rilis lama `SUPERSEDED` → purge
  individu rilis lama.

## Lookup NIK di jalur publik /api/query (role-aware)

Awalnya `/api/query` TIDAK membaca sesi sama sekali → semua query NIK di-defleksi
(privacy) walau user sudah login DTSEN_LOOKUP/SUPERADMIN. Fix (`2bbd706`):

1. Route: `const admin = await getAdminFromRequest(req)` → pass
   `{ role: admin?.role ?? null }` sebagai arg ke-4 `processAIQueryStreaming`.
2. Orchestrator: `tryDtsenDeflection(..., role)` — jika
   `role === 'DTSEN_LOOKUP' || 'SUPERADMIN'` DAN `plan.scope === 'PERSONAL'` &&
   `plan.nik` → panggil `lookupDtsenByNik(nik)`:
   - cari rilis `PUBLISHED` terbaru → `nikHash = hmac(nik, DTSEN_NIK_KEY)` →
     `dtsenIndividu.findFirst({releaseId, nikHash})`.
   - narasi via `buildLookupNarasi(found, releaseRef)`; visualisasi tabel
     `[Nama (termask), Wilayah, Desil, Status Bansos]`; `dataSource:
     'DTSEN (lookup by-NIK — role DTSEN)'`; simpan ChatSession + cache.
   - NIK mentah TIDAK pernah masuk respons; nama termask; audit via saveChatSession.
3. Pengguna publik / role lain: tetap defleksi (tidak berubah).

**Verifikasi:** login SUPERADMIN → query NIK asli → nama termask + desa/kecamatan
tampil; tanpa login query NIK sama → tetap pesan defleksi UU 27/2022.

## Akun tambahan yang dibuat sesi ini

- `master_admin` (SUPERADMIN) — via script DB langsung (pola sama seperti
  prakom_dtsen: `crypto.randomBytes(12).toString('base64url')`, bcrypt 12).
- Semua kredensial cc-acehtengah disalin ke `vault/cc-acehtengah.env`
  (chmod 600, git-ignored) + pointer `CC_VAULT` di `vault/secrets.zsh`.
  Env yang HANYA di Vercel (hidden: JWT_SECRET, ADMIN_SETUP_TOKEN, CRON_SECRET,
  DTSEN_NIK_KEY, NEXT_PUBLIC_SITE_URL) ditandai butuh copy manual.
