# DTSEN BAPPEDA Import Recipe (validated 29-Agu-2026)

End-to-end workflow to get DTSEN data from the BAPPEDA zip into the cc-acehtengah
database, used when the SPLP API is 401 and the user provides the official export.

## Input files (from ~/Downloads/KABUPATEN_ACEH_TENGAH_050_3264_BAPPEDA.zip)

- `*_1_1.csv` — **Set Data Keluarga** (71.370 rows, 50 fields, `|`-delimited):
  `nomor_kartu_keluarga`, `jumlah_anggota_keluarga`, `desil_nasional` ('1'..'6','7+'),
  `pbi_nas`, `pbi_pemda`, `kecamatan`, `kelurahan_desa`. No NIK here.
- `*_2_1.csv` — **Set Data Anggota Keluarga** (235.011 rows, 47 fields):
  `nomor_induk_kependudukan` (NIK), `nama`, `nomor_kartu_keluarga`,
  `pbi_nas`, `pbi_pemda`, `kecamatan_ktp`, `kelurahan_desa_ktp`. No desil here.
- Metadata txt files confirm Data Version: DTSEN Versi 4 Desember 2025.

## Step 1 — Store raw safely (UU PDP)

```bash
mkdir -p services/cc-acehtengah/data/dtsen-raw
cp ~/Downloads/KABUPATEN_ACEH_TENGAH_050_3264_BAPPEDA.zip data/dtsen-raw/
# .gitignore: data/dtsen-raw/  ← NIK/nama/alamat MUST NEVER be committed
```

## Step 2 — Aggregate to bebas-PII JSON (for the offline source)

Python script reading `*_1_1.csv` (family level): count keluarga + jiwa per
kecamatan, per kecamatan×desil, per desa, per desil, and bansos PBI per
kecamatan. Emit `src/data/dtsen-agregat-bappeda.json` (committed, ~33KB).
Verify no PII columns remain (`nik`, `nama`, `alamat`, `kartu_keluarga`).

The `dtsenBappedaSource.ts` module converts this JSON to `PublicAgregatResult`
via `buildAgregatAnswer` (k≥5 sensor). Pipeline order in
`fetchDtsenAgregatPublik`: SPLP API → BAPPEDA offline → DB → demo.

## Step 3 — Transform to DTSEN template CSV (for DB import)

JOIN CSV2 (NIK/nama/pbi) against CSV1 (desil per no_kk). Template header:
`nik,nama,no_kk,kecamatan,desa,desil,pkh,bpnt,pbi_jk`.
- desil: `norm_desil('7+') → 7`, empty → skip row (12.330 rows skipped, no desil)
- pkh/bpnt = 0 (BAPPEDA family export doesn't split programs), pbi_jk = pbi_nas|pbi_pemda
- Validate NIK: 16 digits. Result: 222.681 valid rows (~17MB).

## Step 4 — DTSEN_NIK_KEY consistency (CRITICAL)

NIK is HMAC-SHA256'd with `DTSEN_NIK_KEY`; lookup hashes must match import
hashes. Vercel env is hidden (`vercel env pull` → `[SENSITIVE]`), so:

1. Generate a fresh key: `python3 -c "import secrets; print(secrets.token_urlsafe(24))"`
2. `vercel env rm DTSEN_NIK_KEY production --yes` then `echo <key> | vercel env add DTSEN_NIK_KEY production`
3. Add same key to `.env.local`
4. **REDEPLOY** — env changes do NOT apply to existing deployments
   (this bit us: lookup returned "TIDAK tercatat" until redeploy).

## Step 5 — Import directly to DB (bypasses 4.5MB Vercel payload limit)

Node script with `prisma` (run from repo root so `@prisma/client` resolves):
read transformed CSV → `hmac(nik, SECRET)` → `maskNama()` → createMany in
CHUNK=5000 → `DtsenRelease` (id: `crypto.randomUUID()`, status STAGING,
metadata JSON) → compute agregat groups (k≥5 sensor) → transaction:
createMany agregat + update PUBLISHED + supersede old releases + purge old
individuals. Validated: 222.655 individuals, 2.060 agregat groups, 12 jiwa
sensor.

## Step 6 — Verify live

- `POST /api/auth/login` (prakom_dtsen) → cookie
- `GET /api/dtsen/releases` → BAPPEDA-DES-2025 PUBLISHED, 222.655 rows
- `POST /api/dtsen/query` `{"query":"berapa jumlah jiwa desil 1..."}` → AGGR
- `POST /api/dtsen/query` `{"query":"cek data <16-digit-NIK>"}` → PERSONAL,
  nama masked + desa/kecamatan + status bansos; audit row `LOOKUP_NIK` written.

## Pitfalls

- CSV delimiter is `|`, not comma — `csv.DictReader(f, delimiter='|')`.
- `DtsenRelease.id` has no Prisma default (DB uses gen_random_uuid) — always set explicitly.
- `dataAccessAudit` columns are `action`/`detail`/`rowCount` (NOT `aksi`/`adminNama` from `buildAuditEntry`) — map manually when writing audit rows.
- `buildAgregatWilayah` expects `ValidDtsenRow` shape incl. `statusBansos` — map DB `bansos` boolean to `{pkh:false,bpnt:false,pbi:bansos}` before calling.
- Screen/audit a sample NIK BEFORE telling the user data is live.
