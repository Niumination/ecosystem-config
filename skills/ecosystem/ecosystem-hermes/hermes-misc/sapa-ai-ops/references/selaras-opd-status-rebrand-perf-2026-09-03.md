# Selaras + OPD + Status Honesty + Rebrand + Perf Audit — 2026-09-03

## Number Formatting Unity (selaras)
`src/lib/format-singkat.ts` is single source. Do not duplicate scale logic elsewhere.
- `parseNilaiSapa` absorbs `SCALE_WORDS` (ribu/juta/milyar/triliun) and strips `.00` SPLP tail (`618.700.433.221.00` → `618700433221` → `618,7 Miliar` not `61 Triliun`).
- `headlineParts(nilai, satuan)` for lead/KPI/bucket cards; `singkatNarasi` for grounding narrative (keep `rupiah/%`, skip years 1900-2100, dedup `Triliun Milyar`).
- Table raw values stay full precision. Verify via `scripts/sweep-chips.ts` 10 chips + `format-singkat.test.ts` including ekor `.00` case (28 tests).

## OPD Drill-Down Port (dev → main SPLP-only)
Pure package: `services/opd-drilldown.ts` (`parseNumericId` = reject `/[A-Za-z]/` then `parseNilaiSapa`), `api/analytics/opd/[slug]/route.ts` (10m Map cache, `resolveExactOpdName`), `components/TopOpdWidget.tsx` (fetch `/api/sapa`), `components/OpdDrilldown.tsx` (≥2 yearly points for trends). Mount via `dynamic(ssr:false)` + `useSearchParams` + `Suspense` wrapper (`?opd=`). `kpi.ts:seriesOf` uses `parseNilaiSapa` so deltas respect `.00`.

## Status Honesty
`GET /api/status` (force-dynamic) shares SPLP LRU but AI `active` only if `AI_MODEL` && `AI_WIRED=true` (code flag default false). Sidebar fetches per navigation: `Active/Nonaktif/Down` + `model belum dikonfigurasi — belum dipakai` placeholder.

## Rebrand cc-acehtengah → sapa-ai
Rename: `package.json`/`package-lock.json` name, `.vercel/project.json` projectName, `src/app/globals.css` comment, `status/page.tsx`, `api/report`/`api/status` comments. Archive 16 lineage docs to `docs/archive/cc-lineage/` + `docs/archive/README.md`. `README.md` rewrite SPLP-only. `.env.local` host replace (gitignored). Run `vercel link` after.

## Perf Audit Phasing
Phase 1 inline (low-risk): `ChartsView` `useMemo` + `OpdDrilldown` `dynamic(ssr:false)` (commit `1e3f95b`, `5 files 36 passed`). Phase 2 branch: RSC server-fetch vs client waterfall; `use cache`/`cacheLife`/`cacheTag('sapa')` vs per-instance LRU; keep `/api/status` dynamic. Plan `.hermes/plans/2026-09-03_230500-audit-perf.md`.

## Dev Triage
`git log main..dev --oneline` (209), `git diff --name-status dev main | grep ^D` (70 files), `grep import` for `prisma|auth|dtsen|llm|mock-data|store|warehouse|bapokting` → buckets: portable / not portable (DB/auth/DTSEN/LLM) / redundant (merged into `/api/sapa`,`/api/status`) / archived docs. Only cohesive SPLP-only packages worth porting.
