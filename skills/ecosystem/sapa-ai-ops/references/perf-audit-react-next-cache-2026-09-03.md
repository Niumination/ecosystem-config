# Perf Audit sapa-ai — react-best-practices + next-cache-components (2026-09-03)

## Context
User: `skill apa yang bisa digunakan untuk tingkatkan performa di sapa-ai saat ini?` → probed `.agents/skills/` 20 autoskills; `frontend-design`, `accessibility`, `seo` duplikat bank pusat.

## Relevant skills for sapa-ai (verifikasi via header SKILL.md, bukan klaim)
- **react-best-practices** (Vercel, 70 rules) — bundle/client, dynamic, memo — paling berdampak
- **next-cache-components** (Next 16 PPR, use cache/cacheLife/cacheTag) — ganti/komplemen LRU
- **next-best-practices** — RSC boundary/metadata
- **composition-patterns** — pecah ChartsView/ExecutiveRenderer agar memo efektif
- Tidak relevan: `nodejs-backend-patterns` / `nodejs-best-practices` (Express/Fastify), `vitest`/`zod`

## Baseline probe (bukan klaim)
```
npm run build → Compiled successfully in 7.9s, Route (app) 6 API ƒ Dynamic / 5 page ○ Static, .next 641M
npx vitest run → 5 files 36 passed (36)
force-dynamic → sapa, kpi, query, report, stats, status (6 routes)
dynamic ssr:false → dashboard/page.tsx (SapaStats, AIResponseRenderer, TopOpdWidget) + analytics/page.tsx→ChartsView + gis/page.tsx (react-leaflet)
recharts imports → 5 files (ChartsView, OpdDrilldown, SapaStats, ExecutiveRenderer, AIResponseRenderer)
useMemo → hanya ExecutiveRenderer chartData; ChartsView opdData/compData/satData/topInd tanpa memo (sort tiap render)
```

## Findings (matriks)
1. ChartsView derivasi tanpa useMemo — Med, Low effort → `useMemo([data])`
2. OpdDrilldown static inside ChartsView — Low-Med → `dynamic(()=>import(...),{ssr:false})` lazy
3. Semua dashboard pages 'use client' + fetch('/api/sapa') client-side — Med, High → pilot RSC direct fetchSapaData()
4. LRU 10 mnt per-instance (sapa-client.ts:102) lost on cold start — Med, Med-High → branch experimental.cacheComponents:true + cacheLife/cacheTag, keep /api/status force-dynamic

## Pitfall
Jangan klaim perf improvement dari header skill saja — selalu probe `grep from 'recharts'`, `grep useMemo`, `npm run build` route table. `nodejs-backend-patterns` jangan dibawa ke Next Route.

## Workflow
Plan mode: `.hermes/plans/2026-09-03_230500-audit-perf.md` (8 tasks bite-size). Owner prefers sequential in-session `kerjakan di sesi ini saja pelan pelan berurutan` over subagent dispatch — tanya preferensi setelah plan.
