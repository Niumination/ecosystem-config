# ISR 4B Propagasi — kpi/stats/report + revalidateTag (2026-09-04, feat/perf-rsc-cache 129f1e2..b702b92)

## Context
4A stabilized `sapa` + `dashboard/analytics` with `unstable_cache` + `revalidate 600`. Opsi B propagates same pattern to remaining aggregate APIs so every heavy aggregation hits distributed cache 10m, not per-request fetchSapaData (2048 records).

## Recipe

### kpi / stats / report — inline unstable_cache → revalidate
Each heavy route had `export const dynamic='force-dynamic'` + direct `fetchSapaData()` + inline aggregation (report had manual `let cache:{body,expiresAt}|null` TTL 10m). Replace with:

```ts
// src/app/api/kpi/route.ts
import { unstable_cache } from 'next/cache';
import { fetchSapaData } from '@/lib/sapa-client';
import { computeKpis } from '@/services/kpi';
export const revalidate = 600;
async function fetchKpiPayload(){ const {records,origin}=await fetchSapaData(); return {status:'ok', source: origin==='splp'?'SAPA SPLP':origin, kpis: computeKpis(records)}; }
const getCachedKpi = unstable_cache(fetchKpiPayload, ['kpi'], {revalidate:600, tags:['kpi']});
export async function GET(){ return NextResponse.json(await getCachedKpi()); }
```

Same for `stats` (aggregation over opdCounts/indicatorCounts/yearCounts → overview/opds/topIndicators/dataByYear/kategoriDistribusi) and `report` (computeKpis + buildReport). Remove manual `cache` var in report.

**Extraction for RSC reuse:** Create `src/services/kpi-data.ts`:
```ts
import { unstable_cache } from 'next/cache';
async function fetchKpiPayload(){ ... }
export const getKpiData = unstable_cache(fetchKpiPayload, ['kpi'], {revalidate:600, tags:['kpi']});
```
Then `api/kpi/route.ts` becomes thin wrapper `import { getKpiData }`.

Route table after: `○ /api/kpi 10m`, `○ /api/stats 10m`, `○ /api/report 10m`, `○ /api/sapa 10m`; `ƒ /api/query`, `ƒ /api/analytics/opd/[slug]`, `ƒ /api/status`, `ƒ /api/revalidate` stay Dynamic (per-request).

### Cache bust — POST /api/revalidate
```ts
// src/app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache';
export const dynamic='force-dynamic';
const ALLOWED_TAGS = new Set(['sapa-analytics','kpi','stats','report']);
export async function POST(req:Request){
  const body = await req.json() as {tag?:string;tags?:string[];secret?:string};
  // optional auth: if REVALIDATE_SECRET set, require header x-revalidate-secret or body.secret
  const tags = body.tags ?? (body.tag ? [body.tag] : []);
  const toRevalidate = tags.includes('all') ? [...ALLOWED_TAGS] : tags.filter(t=>ALLOWED_TAGS.has(t));
  for(const t of toRevalidate) (revalidateTag as any)(t);
  return NextResponse.json({status:'ok', revalidated: toRevalidate});
}
```
Note double-cache: LRU 10m in `sapa-client.ts` remains per-instance; `revalidateTag` busts Next distributed layer only. Next cold after bust still ~0.15s (LRU hit) not 1.2s. True cold requires LRU expiry.

## Verification
- `npm run build` → `○ /api/kpi 10m`, `○ /api/stats 10m`, `○ /api/report 10m` (was ƒ), `ƒ /api/revalidate`
- `curl /api/kpi` hit-1 1.25s → hit-2 0.007s; `curl -X POST /api/revalidate -d '{"tag":"kpi"}'` → `{"revalidated":["kpi"]}` → next hit 0.15s (LRU warm)
- `vitest` 5 files 36 passed
