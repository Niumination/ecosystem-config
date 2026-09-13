# RSC Analytics Pilot — 2026-09-04 (branch feat/perf-rsc-cache)

## Context
- Pre: `/dashboard/analytics/page.tsx` was `'use client'` with `dynamic(ssr:false)` ChartsView that did `fetch('/api/sapa')` client-side → extra roundtrip.
- Goal: Server Component fetches SPLP server-side, eliminates client→API hop (audit #3).

## Recipe (reproducible)

1. **Extract single source** `src/services/analytics-data.ts`:
   - Move aggregation from `api/sapa/route.ts` (opdMap/indFreq/satuanMap/jadwalMap + kecamatan/bounds/kabupaten/dataScope/sumber) into `getAnalyticsData(): Promise<AnalyticsData>`.
   - Keep `fetchSapaData()` from `sapa-client.ts` as only data fetch (LRU 10m per-instance).

2. **Thin API route** `src/app/api/sapa/route.ts`:
   ```ts
   import { getAnalyticsData } from '@/services/analytics-data';
   export const dynamic='force-dynamic'; export const runtime='nodejs';
   export async function GET(){ return NextResponse.json(await getAnalyticsData()); }
   ```

3. **Client ChartsView** `src/app/dashboard/analytics/ChartsView.tsx`:
   - `export default function ChartsView({initialData=null}:{initialData?:AnalyticsData|null})`
   - `const [data,setData]=useState(initialData); const [loading,setLoading]=useState(!initialData);`
   - `useEffect(()=>{ if(initialData) return; fetch... },[initialData])`
   - Keep `useMemo` for opdData/compData/satData/topInd + `dynamic OpdDrilldown`.

4. **Wrapper** `src/app/dashboard/analytics/AnalyticsClient.tsx` (`'use client'`):
   ```ts
   'use client'; import nextDynamic from 'next/dynamic';
   const ChartsView = nextDynamic(()=>import('./ChartsView'),{ssr:false});
   export default function AnalyticsClient({initialData}){ return <ChartsView initialData={initialData}/>; }
   ```
   **Pitfall:** `ssr:false` is NOT allowed in a Server Component. `page.tsx` (server) must import the wrapper, not call `nextDynamic` directly.

5. **Server page** `src/app/dashboard/analytics/page.tsx`:
   ```ts
   import AnalyticsClient from './AnalyticsClient'; import { getAnalyticsData } from '@/services/analytics-data';
   export const dynamic='force-dynamic';
   export default async function AnalyticsPage(){
     const data = await getAnalyticsData();
     return <Suspense><AnalyticsClient initialData={data}/></Suspense>;
   }
   ```

## CacheComponents Pitfall (#4 — deferred)

- Attempted: `next.config.mjs` `experimental:{cacheComponents:true}` + `'use cache'; cacheTag('sapa-analytics'); cacheLife({stale:60,revalidate:600,expire:3600})` in `getAnalyticsData`.
- **Build error:** `ssr: false is not allowed with next/dynamic in Server Components` + `dynamic` conflict on all 6 `force-dynamic` API routes (Next 16 cacheComponents forbids `export const dynamic='force-dynamic'`).
- **Resolution:** Reverted `next.config.mjs` to `{}` and removed `'use cache'`; kept LRU. Distributed cache requires phase 4b: remove `dynamic` exports from all routes → replace with `cacheLife`/`revalidate` (keep `/api/status` `noStore`). Documented as deferred.

## Verification
- `npx vitest run` → 5 files 36 passed
- `npm run build` → `ƒ /dashboard/analytics` Dynamic, `✓ Generating static pages (9/9)`
- `git log` → `e15a62f perf(rsc): analytics RSC pilot`
