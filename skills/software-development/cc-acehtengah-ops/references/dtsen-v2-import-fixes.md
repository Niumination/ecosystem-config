# DTSEN v2 Import Fixes (29-Agu-2026) — lessons from the second import

## Critical fix: DON'T skip members whose KK is missing from CSV1

**Symptom (user-reported):** a real NIK from the export (`[16-DIGIT-REDACTED]`)
returned "NIK termaksud TIDAK tercatat" at lookup, both in the AI chat and the
DTSEN admin console, even though the NIK exists in `*_2_1.csv`.

**Root cause:** v1 transform joined CSV2 (members) against CSV1 (families) to
get `desil` per `no_kk`, and **skipped every member whose KK had no family row**
— 12.330 members / 1.855 KKs were silently dropped → those NIKs were never
imported. The user's test NIK had KK `[16-DIGIT-REDACTED]`, absent from CSV1.

**v2 fix (validated, 235.011 members imported):**
- Take `kecamatan`/`desa`/`bansos` **directly from CSV2** (`kecamatan_ktp`,
  `kelurahan_desa_ktp`, `pbi_nas`, `pbi_pemda`) — per-individual, most accurate.
- Make `desil` **nullable** — empty string when the KK is not in CSV1; still import.
- Never drop a row that has a valid 16-digit NIK.
- CSV1 is only used for the desil lookup, not as a membership gate.

Verify: pick a NIK whose `no_kk` is absent from CSV1 (`grep` CSV1), import, and
confirm lookup finds it.

## Case-insensitive kecamatan filter (Linge bug)

**Symptom (user-reported):** "berapa jiwa desil 1-2 di Kecamatan Linge" →
"Tidak ada baris agregat untuk scope Kecamatan Linge · desil 1, 2" — yet the
DB had 181 LINGE rows (26 per desil).

**Root cause:** DB stores kecamatan **UPPERCASE** (`"LINGE"`); `detectKecamatan`
returns the dictionary form (`"Linge"`). Prisma/Postgres equality is
case-sensitive → `{ kecamatan: plan.kecamatan }` matches 0 rows.

**Fix — always use `mode: 'insensitive'` in BOTH places:**
- `src/app/api/dtsen/query/route.ts` wilayahFilter
- `src/services/dtsen-planner.ts` `fetchDtsenAgregatDb` where clause

```ts
...(plan.kecamatan ? { kecamatan: { equals: plan.kecamatan, mode: 'insensitive' as const } } : {}),
...(plan.desa ? { desa: { equals: plan.desa, mode: 'insensitive' as const } } : {}),
```

## DB priority: warehouse before BAPPEDA offline JSON

Once the DB has a PUBLISHED release (235.011 individuals), `fetchDtsenAgregatPublik`
order is **SPLP API → DB → BAPPEDA offline → demo**. The offline JSON is now only
a fallback for an empty DB. This keeps chat AI answers identical to the DTSEN
admin console (both read the same DB rows).

## SUPERSEDED is normal, not data loss

Publishing release v2 flips v1 to `SUPERSEDED`. Data stays for audit; queries use
the newest PUBLISHED release. Releases of the SAME source are never both active;
cross-source fusion (SAPA + DTSEN + Dokumen + Bapokting) happens at the query
layer, not by publishing two releases of one source. `/dashboard/admin/dtsen/status`
shows the registry + a legend explaining this.

## Role-aware NIK lookup in the public /api/query chat

`/api/query` did not read the session → NIK queries were always deflected even
for DTSEN-role admins. Fix (`2bbd706`): route calls `getAdminFromRequest(req)`,
passes `{ role }` to `processAIQueryStreaming`, and `tryDtsenDeflection` runs
`lookupDtsenByNik` when `role ∈ {DTSEN_LOOKUP, SUPERADMIN}` AND
`plan.scope === 'PERSONAL'` AND `plan.nik` — HMAC + DtsenIndividu on the
PUBLISHED release + `buildLookupNarasi` + table + audit. Public users still get
deflected (privacy). If a superadmin sees "TIDAK tercatat" in chat but the
console finds the NIK, the role plumbing is missing.

## Change-password + account page

- `POST /api/auth/change-password` — validates old password, min 8 chars,
  re-signs JWT with `createToken` (NOT `signToken` — that name doesn't exist).
- `/dashboard/akun` page + logout button in the GLOBAL dashboard header
  (`/dashboard/layout.tsx`) so logout is available on every page incl. Admin DTSEN.
