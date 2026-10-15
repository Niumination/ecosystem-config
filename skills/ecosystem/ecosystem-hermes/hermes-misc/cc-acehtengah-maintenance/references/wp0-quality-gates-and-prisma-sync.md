# WP0.x quality gates, Prisma schema sync, and security hardening (01-Sep-2026)

Session record for the WP0.x series on `hotfix/meeting-ready` (commits 9d669f1..4df28e7,
then f9500c0/4df28e7 gelombang kedua). These are the durable patterns; each was
verified by `npx tsc --noEmit` (0 errors), `npx vitest run` (278 pass), and
`bash scripts/pii-gate.sh .` (LEAK_COUNT 0).

## Prisma schema-vs-runtime desync (WP0.4) — the big one
Symptom: `tsc --noEmit` reported `Property 'X' does not exist on type 'PrismaClient'`
for `warehouse-sync.ts` (16), `data-sync.ts` (4), plus scripts.

Root cause: `prisma/schema.prisma` contained a NEW model design
(`SapaIndicator`, `SapaObservation`, `SapaOpd`, `SapaSyncRun`, `IndicatorThreshold`,
`EwsAlert.indicatorId Int` etc.) that had **ZERO consumers in src/**, while runtime
code (`warehouse-sync.ts`, `data-sync.ts`, `src/lib/db-migration.ts`) used the OLD
design (`Skpd`, `Dataset`, `DatasetRecord`, `Indicator`, `SapaSnapshot`,
`SapaIndicatorValue`, `EwsAlert.indicatorId String` + `threshold`).

Diagnosis that revealed direction:
- There is NO `prisma/migrations/` — all DDL is manual in `src/lib/db-migration.ts`
  (`ensureWarehouseTables()`), which creates the OLD tables. `schema.prisma` is only
  used for `prisma generate` (client types).
- `grep -rn "prisma\.sapaIndicator|sapaObservation|..."` → 0 hits. Dead models.
- So the FIX direction is: **sync schema.prisma to runtime reality** (add the old
  models + fix `EwsAlert` relation), NOT the other way around.

What to check first when PrismaClient property errors appear:
1. `ls prisma/migrations` — absent means schema.prisma is not authoritative DDL.
2. `grep -rn "prisma.<Model>" src/ --include=*.ts` for each suspect model — count
   consumers; 0 consumers = orphan candidate.
3. Compare `db-migration.ts` CREATE TABLE columns vs schema model fields.
4. After editing schema: `npx prisma validate && npx prisma generate`, then tsc.

Relation naming gotcha: Prisma relation field name must match the API contract used
by consumers. `EwsAlertData.indicator.dataset` (lowercase `dataset`) required
`Indicator.dataset Dataset @relation(...)` — an earlier attempt named it `Dataset`
and tsc failed `did you mean 'Dataset'?`. Name relations to match the TS types that
read them.

Also removed orphaned enums `SyncStatus` and `ThresholdOperator` along with dead
models — be careful: `Severity` is still used by `ews-engine.ts`.

## Pre-commit + typecheck gate (WP0.5)
- `scripts/typecheck.sh` — `rm -rf .next` FIRST (`.next/types/**/*.ts` is in
  tsconfig include → ghost errors across branch switches), then `npx tsc --noEmit`,
  and report `error TS1` count separately (a single TS1005 stops tsc and hides all
  other errors — the classic "1 error" trap).
- Pre-commit now runs pii-gate over the WHOLE tree (not just `src/data/excel`) +
  typecheck. Override: `git commit --no-verify`.
- `next.config.ts` had `typescript.ignoreBuildErrors: true` → removed so Vercel
  build fails on TS errors. `npm run typecheck` = `bash scripts/typecheck.sh`.

## Protect a page via middleware (WP0.9/0.12h)
`middleware.ts` has TWO places to update — the `protectedPaths` array AND the
`config.matcher` list. `/dashboard/akun` was missing from both → 200 without login.
Also note: page already did client-side `/api/auth/me` redirect; middleware makes it
server-side 307 → `/login` with `?from=`.

## Honest source labels — DTSEN provenance (WP0.11)
`jalurLabel(status)` previously returned `status === 'API' ? ... : 'jalur impor manual'`,
but ReleaseRef.status is `PUBLISHED`/`STAGING`/`SUPERSEDED` for DB releases → every
release was mislabeled "impor manual". Fix: distinguish DB status
(`PUBLISHED`→`DB rilis (warehouse)`) from actual import path (`API`→`SPLP live`,
`MANUAL`→`impor manual`). Also: in `ai-orchestrator.ts` the source detection used
`provLabel.includes('bappeda')` which wrongly flagged the DB release
`BAPPEDA-DES-2025` as "offline" JSON. Correct order: demo → db rilis → offline → SPLP.

Mirror rule: label honesty matters for legal reasons (UU PDP); don't let string
substring matching guess the source class from ambiguous tokens.

## Stray file cleanup (WP0.2)
File `~/Desktop/...`-style literal path inside repo (actually tracked as
`~/Desktop/Niumination/services/cc-acehtengah/src/lib/bapokting-client.ts`, 0
consumers, old scraper). Before `git rm`: salvage the diff to /tmp
(`diff src/lib/bapokting-client.ts <stray>` + copy). Confirmed `fetchBapoktingPrices`
used 0 times, `fetchLatestBapoktingPrices` 2 times but via the REAL import path.

## Old routes / EWS (WP0.6)
- `/api/ews` existed only as `route.ts.bak` while `EwsPanel.tsx` fetched `/api/ews`
  → 404 → panel silently lied "Semua indikator dalam batas normal". Re-enabled the
  route AND added `ready` flag (`sapaSnapshot.count() > 0`) so the panel can say
  "EWS belum aktif — snapshot warehouse belum dibuat" when warehouse is empty.
- `/api/datasets` + `/api/datasets/[slug]` `.bak` routes had 0 consumers → removed
  (git history keeps them).

## Branch governance (WP0.13)
Documented in `docs/STATUS-CC.md` "Tata Kelola Branch": `hotfix/meeting-ready` is
the ONLY source of truth (live Vercel); `main` 157+ commits behind; no merges to
`main` without explicit user approval; quality gates before any merge:
`npm run typecheck` + `npx vitest run` + `bash scripts/pii-gate.sh .`.