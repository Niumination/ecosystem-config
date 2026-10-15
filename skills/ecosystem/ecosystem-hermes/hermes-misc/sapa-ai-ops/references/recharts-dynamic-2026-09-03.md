# Recharts Dynamic Split + Dead-Component Purge (2026-09-03)

Keep recharts out of the home initial bundle; results verified with `npm run build` + `vitest 4/4`.

## Dynamic ssr:false recipe

- Home (`dashboard/page.tsx`): `DefaultDashboard` (SapaStats) and `AIResponseRenderer`
  (pulls recharts via ExecutiveAnswerRenderer) via `next/dynamic(..., { ssr: false })` with a
  text `loading` fallback. `KpiPanel` has no recharts — stays static.
- Analytics: page used recharts inline → moved whole content to `ChartsView.tsx`
  (rename default export), `page.tsx` becomes a thin dynamic wrapper.
- **Pitfall (build-breaking): `ssr: false` is illegal in a Server Component.**
  Turbopack fails with `Ecmascript file had an error at page.tsx:<line>` pointing at the
  `dynamic(...)` call. Fix: add `'use client'` to the wrapper file.

## Dead-component verification (before `git rm`)

```bash
for n in <Name>; do echo "$n: $(grep -rln "$n" src/ | wc -l) files"; done
```

Count of 1 = self-reference only = dead. Removed this way: `TrendChart`, `EwsPanel`,
`BreakdownExplorer`. Repo-wide zero-hit check (exclude `node_modules`, `.next`) cleared
`lib/prisma.ts` + `lib/auth.ts` for deletion too.

## localStorage / next/image audit (no change needed)

- `laporan`: `useState<HistoryItem[]>([])` + load inside `useEffect` (SSR-safe, no hydration mismatch).
- `dashboard`: localStorage only inside an event handler (client-only).
- `next/image`: zero usage in `src/` — nothing to migrate.
- Rule: envelope pattern above is the approved shape; flag any direct `localStorage` read in
  a `useState` initializer or render path.
