# Executive Lead — Kesimpulan Padat + P1/P2 (2026-09-02)

## Problem
`buildLead` awal = `narasi.slice(0,320)…` → duplikat narasi, tidak menjawab pertanyaan user. Lead harus berisi **kesimpulan** dari evidence yang dipakai.

## Solution — `buildLead(evidence, answerType, narrative)` in `src/services/executive-presentation.ts`

### Helpers
```ts
extractTopic(narrative) // regex /untuk "([^"]+)"/ → "stunting"
shortLabel(indikator) // strip /^Jumlah / + /(JAB…)/, collapse spaces, 44-char truncate
distinct(values) // dedup + Bappeda/Diskominfo normalization
tahunSummary(evidence) // distinct tahun sorted
```

### Lead Format (deterministic, grounded)
```
{topic}: {nilai} {satuan} — {indikator_singkat} ({tahun}) · {nilai2} {satuan2} — {indikator2} ({tahun2}) — {M} indikator · {OPD} {coverage}
```
- Primary = `evidence[0]`, Secondary = first with different `satuan` (covers Orang vs Persen, USD vs Ha)
- If single satuan multi-indikator: append `— {M} indikator terkait`
- Cap 220 chars

### Vectors (verified 2026-09-02)
- stunting (4 rows Dinkes/Bappeda 2024,2025) → `stunting: 730 Orang — anak balita yang mengalami stunting … (2025) · 31,4 Persen — Prevalensi Stunting (2025) — 4 indikator · Dinkes & Bappeda · 3/4 bertahun`
- IPM (1 metric BPS 2025) → `IPM: 78,09 Indeks — Indeks Pembangunan Manusia (2025) — 1 indikator · BPS`
- kopi arabika (USD+Ha) → `kopi arabika: 30.751.904,8 USD — nilai ekspor kopi (green beans) (2024) · 50.162 Ha — Luas areal kopi arabika (2024) — 2 indikator · Disdag & Disbun`

### Insights P1
- `Keriangan tahun`: `withTahun/evidenceCount` → `3/4 bertahun (2024, 2025); 1 tanpa tahun`
- `Satuan campur` warn when `distinct(satuan) > 1`
- `DataQuality Tahun/periode` → `3/4 bertahun · 2024, 2025` (ok/info/warn)

### QuickWins & FollowUps P2
- Owner = `distinct(opd)` actual, not generic; rekomendasi from `grounding` enriched
- FollowUps: `Filter hanya {OPD}`, `Bandingkan {tahun} vs {tahun}`, `Tampilkan rincian: {indikator.slice(0,28)}` — all wired via `onFollowUp={handleQuery}` in `dashboard/page.tsx`

## Commits
- `b7a566f` P1+P2 (distinct/tahunSummary/insights/quickWins/followUps)
- `205c20f` Headline kesimpulan (extractTopic/shortLabel/conclusion)
