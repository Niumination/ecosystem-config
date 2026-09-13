# Renderer Topic-Gating Pitfall — sapa-ai (2026-09-03)

## Symptom
Chip `ASN` rendered teacher rows under a "Basis Data · Balita Dipantau" card plus a
`Prevalensi: ~33.16%` badge. API lead was correct (`Jumlah ASN 9.610`) — the bug was
purely in `ExecutiveAnswerRenderer.tsx`.

## Root cause
- `bucketGroup` default branch: unknown `Orang` rows → bucket B, `Persen` → C.
- `ContextKPICards`: `B[0]` + hardcoded desc `Balita Dipantau`.
- `PrimaryMetric` badge: `C.find(prevalensi || satuan === 'Persen')` matched
  `Persentasi Guru ASN 33,16%`.

## Fix pattern (commit `879a0bc`)
- `isStuntingEvidence(evidence)`: `/stunt|gizi|balita|bkb|posyandu|hamil|bayi/i`
  over indicator names; stunting labels only when true.
- Prevalence badge only when the indicator itself contains `prevalensi`.
- Generic card desc falls back to the row's own short indicator label.
- Rule of thumb: no renderer string may assume a topic — derive framing from the
  evidence actually returned.

## Verify before committing
`npx tsx` calling `buildExecutivePresentation` on a real `/api/query` response JSON
(e.g. query `ASN`); assert `stuntingCtx` false + badge absent; then `npm run build`.
