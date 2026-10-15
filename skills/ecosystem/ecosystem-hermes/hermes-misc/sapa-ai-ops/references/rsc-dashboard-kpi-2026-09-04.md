# RSC Dashboard — KPI server-fetch (2026-09-04, af93476)

## Context
`/dashboard/page.tsx` was fully `'use client'` (QueryBar + mode/isLoading/aiResponse state + fetch `/api/query`) rendering `KpiPanel`/`TopOpdWidget`/`SapaStats` all client-side → 3 parallel `fetch('/api/*')` waterfalls even though APIs are now ISR 10m (7ms hit). Goal: eliminate KPI waterfall via RSC without breaking interactive query flow.

## Recipe

1. **Service extraction** `src/services/kpi-data.ts` (already used by `/api/kpi` after 4B):
   `export const getKpiData = unstable_cache(fetchKpiPayload, ['kpi'], {revalidate:600, tags:['kpi']});`

2. **KpiPanel accepts server data** `src/components/KpiPanel.tsx`:
   ```ts
   export default function KpiPanel({initialData=null}:{initialData?:{kpis:Kpi[];source:string}|null}){
     const [kpis,setKpis]=useState(initialData?.kpis ?? []);
     const [loading,setLoading]=useState(!initialData);
     useEffect(()=>{ if(initialData) return; fetch('/api/kpi')... },[initialData]);
   }
   ```

3. **Client wrapper** `src/app/dashboard/DashboardClient.tsx` (`'use client'`):
   - Copy all state/handlers from old `page.tsx` (genRef abort, handleQuery/handleReset, liveNarasi SSE).
   - Props: `{initialKpiData?:{kpis:any[];source:string}|null}`
   - Render: `<KpiPanel initialData={initialKpiData} />` + `TopOpdWidget` + `DefaultDashboard` when `mode==='default'`.

4. **Server page** `src/app/dashboard/page.tsx`:
   ```ts
   import DashboardClient from './DashboardClient';
   import { getKpiData } from '@/services/kpi-data';
   export const revalidate = 600;
   export default async function DashboardPage(){
     let initialKpiData=null; try{ const d=await getKpiData(); initialKpiData={kpis:d.kpis, source:d.source}; }catch{}
     return <DashboardClient initialKpiData={initialKpiData} />;
   }
   ```

## Pitfalls
- Do not make the whole dashboard server-only: `QueryBar` + `/api/query` streaming + `localStorage` history must stay client. Only prefetch default-mode data (KPI) server-side.
- `Kpi` type not exported from `KpiPanel` — use `any[]` or `KpiResult` in `DashboardClient` props to avoid TS `no exported member 'Kpi'`.
- `revalidateTag('kpi')` busts Next layer only; LRU in `sapa-client` keeps dashboard 0.05s hit even after tag bust.

## Verification
- `npm run build` → `○ /dashboard 10m 1y` (was client-only), `vitest` 5 files 36 passed
- `curl /dashboard` hit-1 1.51s → hit-2 0.05s (ISR hit, KPI no client fetch)
