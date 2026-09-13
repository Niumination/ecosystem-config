# KPI Curation — 2026-09-02

## Problem
`/api/kpi` (KpiPanel) and `/api/report` (ExecutiveReport) diverged:
- KpiPanel: naive `records.find(r => regex.test(r.nama_indikator))` for 8 keys (`stunting|kemiskinan|ipm|...`) — first match wins, no scoring, `deltaPct=null`, hardcode year fallback 2025. Wrong variant picked (e.g., "usulan kenaikan pangkat" for ASN).
- Report: `computeKpis(records)` curated — 8 KPI (`stunting/IPM/ASN/kemiskinan/kopi/PDRB/jalan/putus-sekolah`) with `preferIncludes/avoidIncludes` + v2 scoring + multi-year delta.

## Fix
`src/app/api/kpi/route.ts` rewritten to use `computeKpis`:
```ts
import { fetchSapaData } from '@/lib/sapa-client';
import { computeKpis } from '@/services/kpi';
const records = await fetchSapaData();
return NextResponse.json({ kpis: computeKpis(records), count: records.length });
```
Contract `KpiResult` unchanged, so `KpiPanel.tsx` untouched.

## Verify
```bash
curl /api/kpi | jq '.kpis[].label'        # 8 curated
curl /api/report | jq '.report.kpi[].label' # identical 8
# 2048 records, build ✓ dedb858
```
