# ISR 4A Stable — 2026-09-04 (feat/perf-rsc-cache, 3e668e3)

## Why not cacheComponents
- Tried `next.config.mjs` `experimental:{cacheComponents:true}` + `'use cache'; cacheTag/cacheLife` in `analytics-data.ts`
- Build errors:
  - `ssr: false is not allowed with next/dynamic in Server Components` when `page.tsx` (server) does `nextDynamic({ssr:false})`
  - `export const dynamic='force-dynamic'` forbidden on all 6 API routes when cacheComponents enabled (Next 16 PPR forbids dynamic exports)
- Implication: full PPR migration requires removing `dynamic` from kpi/query/report/sapa/stats/status and replacing with `cacheLife`/`revalidate` — high blast radius.

## Chosen pattern — stable ISR (4A)
- Keep `next.config.mjs = {}` (no experimental).
- `src/services/analytics-data.ts`: extract `fetchAnalyticsData()` then wrap:
  ```ts
  import { unstable_cache } from 'next/cache';
  async function fetchAnalyticsData():Promise<AnalyticsData>{ const {records}=await fetchSapaData(); /* aggregation */ }
  export const getAnalyticsData = unstable_cache(fetchAnalyticsData, ['sapa-analytics'], { revalidate:600, tags:['sapa-analytics'] });
  ```
  LRU 10m in `sapa-client.ts` retained as second layer (per-instance fast, unstable_cache is distributed).
- Routes:
  - `src/app/api/sapa/route.ts`: `export const dynamic='force-dynamic'` → `export const revalidate=600` (now `○ /api/sapa 10m 1y`)
  - `src/app/dashboard/analytics/page.tsx`: same `revalidate=600` (now `○ /dashboard/analytics 10m`), Server Component `await getAnalyticsData()` → `AnalyticsClient(initialData)`
  - `src/app/api/status/route.ts` **kept** `ƒ Dynamic` — health must be live, never cached. Do not add revalidate there.
- Wrapper pitfall: Server Components cannot do `nextDynamic({ssr:false})`. Must use `'use client'` wrapper:
  `AnalyticsClient.tsx` (`'use client'` + `nextDynamic(()=>import('./ChartsView'),{ssr:false})`)

## Verification
- `npx vitest run` → 5 files 36 passed
- `npm run build` → `○ /api/sapa 10m`, `○ /dashboard/analytics 10m`, `ƒ /api/status` (dynamic), `✓ Generating static pages (11/11)`
- `git log` → `3e668e3 perf(cache): 4A stable ISR 10m`

## When to revisit 4B
- Only when Next 16 `cacheComponents` exits experimental and team is ready to remove `dynamic` exports from all 6 routes.
- Then replace `unstable_cache` + `revalidate` with `'use cache'` + `cacheTag('sapa-analytics')` + `cacheLife`.
