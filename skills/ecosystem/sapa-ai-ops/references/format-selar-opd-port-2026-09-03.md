# Format Selaras + OPD Port — sapa-ai (2026-09-03)

Session learnings from the lead/headline alignment fix (`d505e18`), honest
sidebar status (`db5a87e`, `9987634`), and dev→main OPD drill-down port
(`a4caecb`, `5c32c38`).

## Single-source number formatting

All user-facing surfaces must render through `headlineParts` /
`singkatNarasi` (`src/lib/format-singkat.ts`): lead, bucket summary,
executive narrative, ContextKPICards, metric cards, `KpiPanel`, and
`kpi.ts seriesOf` (delta math). Evidence tables + history keep full
precision (detail level). Symptom of violation: lead shows
`11.503.360.000.000 Milyar` while headline shows `11,5 Triliun`.

## SPLP parser quirks (`parseNilaiSapa`)

- Trailing `.00` after thousand groups is an Indonesian decimal, not more
  thousands: `618.700.433.221.00` → 618,7 Miliar (naive strip-all-dots
  gives 61,87 Triliun — 100x wrong). Handled in the multi-dot branch.
- `parseNilaiSapa` is LENIENT: it strips letters (`12a` → 12). For trend
  series this fabricates data — wrap it strictly (`parseNumericId` in
  `opd-drilldown.ts` rejects `/[A-Za-z]/` first, then delegates).
  Negative numbers pass through (`-5` → -5); dev-era test expecting
  null was updated to match the unified parser.

## Live sweep pattern (verify all chips, then delete)

Ad-hoc `sweep-chips.ts` (repo root, NOT src/): fetch live SPLP once,
run all 10 chip queries through retrieve→aggregate→narasi→presentation,
print HEADLINE/LEAD/NARASI per chip, eyeball alignment, then `rm`.
tsx constraints: wrap in `async function main()` — top-level await fails
under cjs output. This sweep caught the 100x `.00` bug that unit tests
missed. Never commit the sweep script.

## OPD drill-down port recipe (dev → main)

Portable set (5 files, ~500 lines, zero DB/auth deps): pure service
(`services/opd-drilldown.ts`), slug route (`api/analytics/opd/[slug]`),
two client components (`TopOpdWidget`, `OpdDrilldown`), unit test.
Adaptations required: numeric parsing via `parseNilaiSapa`; `TopOpdWidget`
fetches existing `/api/sapa` (same `opdBreakdown` shape) instead of adding
a duplicate `/api/analytics` route; mount via `?opd=` + `useSearchParams`
(requires `<Suspense>` boundary in `page.tsx` — ChartsView is
`dynamic ssr:false`); strip emoji (repo style rule); dynamic-import
widgets on the home page. Non-portable from dev: auth, DTSEN, EWS,
warehouse, `api/health` (superseded by `/api/status`), `api/geodata`
(dep `data-source.ts` already deleted).

## Honest status (`/api/status` + sidebar)

SAPA state from the real SPLP fetch (shared LRU, no double fetch); AI
state is `active` ONLY if `AI_MODEL` env is set AND the `AI_WIRED`
constant in the route is flipped (currently `false` — no LLM path exists,
so env residue like `ling-3.0-flash-free` from another project must NOT
read as active). Sidebar shows `model belum dikonfigurasi` placeholder
when inactive; collapsed mode inherits dot color.
