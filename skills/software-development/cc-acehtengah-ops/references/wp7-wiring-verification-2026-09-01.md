# WP7 Wiring + Verification Recipe (Surat-4 Arena)

Snapshot: `hotfix/meeting-ready` HEAD `bbf884c` (01 Sep 2026). Tujuan: Sambungkan modul statistik yang sudah ada (`fusion`, `narrative`, `to-metrics`) ke jalur `/api/query` tanpa ubah kontrak lama.

## Konsep
- `buildContext` mengembalikan `ctx.filteredData`, `ctx.evidence`, dsb.
- `tryDeterministicDomainQuery` adalah titik wiring yang aman: sebelum handler deterministik lain/LLM, inject `fuseMetrics` + `buildNarrative` tanpa remove logic legacy.
- Gunakan feature flag `STATISTICS_LAYER=1` agar reversible.

## File yang disentuh
- `src/lib/statistics/to-metrics.ts` — baru, 4 fungsi: `metricsFromSapa`, `metricsFromDtsen`, `metricsFromExcelDoc`, `metricsFromBapokting`
- `src/lib/statistics/build-viz.ts` — baru, `buildVizFromMetrics` grouping `measure|geo.level`
- `src/services/ai-orchestrator.ts` — wiring + inject `__statisticsSummary`/`__statisticsCaveats` ke result
- `src/services/grounding.ts` — jangan taruh `buildVizFromMetrics` di sini (recursive import `HybridResponse`); pakai file terpisah.
- `src/lib/statistics/narrative.ts` — tambah `archetype` handler (trend/ranking/distribution/comparison/composition/correlation/anomaly)
- `scripts/eval-harness.ts` — ganti mock tiruan → `metricsFromExcelDoc` live + reconcileMetrics untuk Q01
- `data/golden-queries.json` — 6 → 92 kasus (merge repo + audit)

## Kriteria selesai WP7 (terverifikasi)
1. `git grep -n "statistics/fusion\|statistics/narrative" -- src/services src/app` → muncul di `ai-orchestrator.ts` (bukan hanya test/harness).
2. `git grep -nE "function metricsFrom" -- src/lib/statistics/to-metrics.ts` → 4 fungsi.
3. `git grep -n "parseFloat(" -- src/services src/lib | grep -v parse-numeric` → 0.
4. `/api/query` + `STATISTICS_LAYER=1` → SSE berubah; bukti: `/tmp/after-wp7.sse` (tabel 17 rows, narasi gabung DokB+SAPA, UU PDP caveat).

## Catatan penting
- `buildVizFromMetrics` TIDAK masuk ke `grounding.ts` karena recursive import `HybridResponse`. Letakkan di `src/lib/statistics/build-viz.ts`.
- `narrative.ts` `NarrativeInput` sekarang `archetype?: string`; wiring: `routeQuestion(query).archetype`.
- Excel docs default hanya `dok-b-01-stunting-2026-07.json`. Tambah `dok-a`/`dok-c` di `to-metrics.ts` bila nanti dibutuhkan.
- `eval-harness.ts` sekarang 92/92 lulus, tapi masih ada `excelMetrics.slice(0,5)` + security skips; bukan full live DB probe.
