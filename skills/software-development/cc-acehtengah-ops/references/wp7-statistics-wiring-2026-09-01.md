# WP7 Statistics Wiring — 01 Sep 2026

## Contract
- Flag: `STATISTICS_LAYER=1`
- Location: `src/services/ai-orchestrator.ts` inside `tryDeterministicDomainQuery`
- Goal: deterministic fusion + narrative before LLM; LLM only polishes language.

## Producers (`src/lib/statistics/to-metrics.ts`)
- `metricsFromExcelDoc(doc)` — Excel JSON → `Metric[]`
- `metricsFromSapa(rows)` — SAPA records → `Metric[]`
- `metricsFromDtsen(rows)` — DTSEN agregat → `Metric[]`
- `metricsFromBapokting(stats)` — Bapokting stats → `Metric[]`

## Wiring snippet
```ts
const excelMetrics = excelDocs.flatMap((d) => { try { return metricsFromExcelDoc(d); } catch { return []; } });
const sapaMetrics = (() => { try { return metricsFromSapa(ctx.filteredData as any); } catch { return []; } })();
const plan = (() => { try { return routeQuestion(query); } catch { return null; } })();
const fused = fuseMetrics([...excelMetrics, ...sapaMetrics]);
const cerita = buildNarrative({ fused, question: query, archetype: plan?.archetype });
```

## Narrative templates (`src/lib/statistics/narrative.ts`)
Supported `archetype`: `level`, `trend`, `ranking`, `distribution`, `comparison`, `composition`, `correlation`, `anomaly`. Fallback: `level`.

## Viz split rule
- `buildVizFromMetrics` lives in `src/lib/statistics/build-viz.ts`
- Groups by `measure|geo.level`
- Do NOT place in `grounding.ts` — causes recursive import via `HybridResponse`.

## Eval harness (`scripts/eval-harness.ts`)
- Uses live `metricsFromExcelDoc` from `src/data/excel/json/*.json`
- `reconcileMetrics()` supplies SAPA + DTSEN-BAPPEDA penduduk values for Q01 rekonsiliasi.
- Golden queries: 92/92 pass (31 Aug 2026)
- Never use `mkMetric` mock for Excel-covered concepts; use real producer or mark concept `expectEmpty=false`.

## SSE diff proof (`/tmp/after-wp7.sse`)
- Response now includes DokB + SAPA + UU PDP caveat + table 17 rows (14 kecamatan + 3 SAPA indicators)
- Before: 1894 chars; after: 585 chars narrative + structured table.

## Pitfalls
- `buildVizFromMetrics` MUST be in its own module; importing `HybridResponse` from `grounding.ts` creates circular dependency because `grounding.ts` imports viz helpers.
- `eval-harness.ts` must normalize `query` → `question` for merged golden queries.
- `expectEmpty=true` is only meaningful when `metrics.length === 0`; otherwise skip.
