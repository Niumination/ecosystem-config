# Session 29-Agu-2026 (late): status page, roles, formatting — deltas after v2 import

Captures the UI/UX + data-integrity changes from the final stretch of the session.
Companion to `dtsen-v2-import-fixes.md` (data layer) and `dtsen-bappeda-import.md`
(import recipe). If SKILL.md sections below were already applied, treat this as
the authoritative detail.

## Source priority (fetchDtsenAgregatPublik) — FINAL

SPLP API → **DB (DtsenRelease PUBLISHED)** → BAPPEDA offline JSON. Demo data
DELETED entirely (`fetchDtsenDemoData` + `DemoFilter` + "DTSEN Demo" label
removed from ai-orchestrator, commit `64ada17`). If all real sources fail,
answer honestly "DTSEN tidak tersedia" — NEVER simulated numbers (user explicitly
required real-source-only output; the old demo mislabeled 48.200 jiwa desil 1 as
if it were API data).

## Case-insensitive kecamatan filter (Linge bug — user reported)

DB stores kecamatan UPPERCASE ("LINGE"); `detectKecamatan` returns dictionary
form ("Linge"). Postgres equality is case-sensitive → query returned "Tidak ada
baris agregat ... Kecamatan Linge · desil 1, 2" with 0 rows even though 181
LINGE rows existed. Fix: `mode: 'insensitive'` on kecamatan AND desa filters in
BOTH `src/app/api/dtsen/query/route.ts` wilayahFilter and
`src/services/dtsen-planner.ts` fetchDtsenAgregatDb. Also fixed `jiwa/kk` field
names (schema actual) vs `jumlahJiwa/jumlahKeluarga` (stale) in that DB fallback.

## Role-aware NIK lookup in public /api/query (commit 2bbd706)

Before: `/api/query` never read the session → NIK queries deflected even for
DTSEN-role admins. Fix: route calls `getAdminFromRequest(req)`, passes
`{ role }` to `processAIQueryStreaming(query, onStatus, onChunk, opts)`;
`tryDtsenDeflection` runs `lookupDtsenByNik(nik)` when
`role ∈ {DTSEN_LOOKUP, SUPERADMIN}` AND `plan.scope==='PERSONAL'` AND `plan.nik`
→ HMAC + DtsenIndividu on PUBLISHED release + `buildLookupNarasi` + table +
audit. Public users still deflected. Verify BOTH chat AI and admin console give
the same answer for the same NIK.

## Accounts & auth (all passwords in vault/cc-acehtengah.env)

- `admin` (ADMIN), `prakom_dtsen` (DTSEN_LOOKUP), `master_admin` (SUPERADMIN —
  created this session; user asked for it explicitly).
- `AdminRole` enum had only ADMIN/SUPERADMIN → data-gate rejected all DTSEN
  access; added DTSEN_ANALYST/DTSEN_LOOKUP to prisma schema + `ALTER TYPE` on
  live DB + `POST /api/setup/dtsen-role` endpoint.
- Change password: `POST /api/auth/change-password` (validate old, min 8,
  re-sign with `createToken` — NOT `signToken`), UI at `/dashboard/akun`.

## Role visibility / nav gating (Sidebar.tsx + dashboard/layout.tsx)

- NAV_ITEMS gained `public: true|false`. Sidebar fetches `/api/auth/me` on mount
  → `visibleItems = NAV_ITEMS.filter(i => i.public || isAuthed)`. Publik hanya
  lihat Beranda/Analitik/GIS; semua akun login lihat semua halaman.
- Header Akun/Logout buttons render ONLY when `isAuthed` (checked via
  `/api/auth/me` on mount) — user complained logout button persisted after
  logout; now it disappears.

## Status page (standalone, not sub-admin)

- Moved `dashboard/admin/dtsen/status` → `dashboard/status` (own sidebar entry
  "Status Sumber", 🗂️). Guard: redirect `/login` if not authenticated.
- `GET /api/dtsen/status` (RESTRICTED_AGGR): 7-source DataSource registry +
  releases per source (status PUBLISHED/STAGING/SUPERSEDED, individu/agregat
  counts) + ringkasan cards + SVG relation diagram (sumber mentah → warehouse →
  query planner → output). Seed DataSource via upsert when empty (7 slugs:
  sapa, dtsen, dtsen-splp, dtsen-kominfo, dtsen-stunting, bapokting, dokumen).
- SUPERSEDED = normal: publishing release v2 flips v1 to SUPERSEDED; data kept
  for audit; same-source releases never both active; cross-source fusion happens
  at query layer. Legend on the status page explains this.

## Number formatting — id-ID everywhere (user asked)

- `AIResponseRenderer.tsx`: helper `formatAngka(v)` — numbers AND numeric strings
  → "12.345"; used in TableRenderer cells, MetricRenderer, ChartTooltip.
- Backend `summarizeEvidence` uses `fmtNilaiId` (numeric-only → toLocaleString
  id-ID; already-formatted strings untouched).
- SAPA API sends values as raw strings that may or may not already have
  thousands separators — never trust source formatting.
