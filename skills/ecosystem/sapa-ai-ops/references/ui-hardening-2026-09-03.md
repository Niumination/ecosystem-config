# UI Hardening 2026-09-03 — 6 localhost findings (sapa-ai)

Root cause family: hero/headline rendered RAW `nilai` strings; `formatAngkaPresentasi`
only touched narasi/table/metric viz — never the executive hero metric.

## 1. formatSingkat (src/lib/format-singkat.ts + .test.ts, 17 tests)
- Parse ID formats: `1.438.857.592.538,6` / `11.503.360.000.000` / `4,47` / `6285`.
  Single-dot + 3 digits = thousands (`Rp 12.500`→12500); single dot otherwise = decimal.
- Abbreviate from MILLIONS only (user correction: thousands stay full):
  `≥1T→Triliun, ≥1M→Miliar, ≥1jt→Juta, else full id-ID` (`9610→9.610`, `4,47→4,47`, `0,0036`).
- `headlineParts(nilai, satuan)`: scale-word satuan absorbed when number already scaled
  (`11.5T + "Milyar" → "11,5 Triliun", unit:null`); kept+normalized when not
  (`4,5 + "Milyar" → "4,5 Miliar"`); real units (`rupiah`, `persen`, `orang`) always shown.
- Applied ONLY in `PrimaryMetric` hero; evidence/tables keep full values.

## 2. Live sidebar status (src/app/api/status/route.ts + Sidebar.tsx + route.test.ts)
- SAPA active/down from real SPLP fetch (shares server LRU with /api/query).
- AI active ONLY if `AI_MODEL` env set (repo is deterministic, no LLM) → default
  inactive + placeholder `model belum dikonfigurasi`; active shows `provider · model`.
- Sidebar fetches per navigation; dots green/grey/red; collapsed tooltips carry detail.
- Activate later: set `AI_PROVIDER` + `AI_MODEL` env — no code change.

## 3. Beranda-no-response (two causes)
- (a) `absolute` button inside non-`relative` parent → mispositioned/covered click
  target. Fix: `relative` on QueryBar header div.
- (b) Abort race: reset aborts in-flight fetch → catch re-sets `ai-response` mode.
  Fix: generation token (`genRef`; `handleReset` increments; stale catch returns early).

## 4. Chip caption removed
`SAPA · SPLP · 2.048 record…` span deleted from QueryBar display (kept in aria-label)
on explicit user request.

## Verify
`npx vitest run` (20 tests) + `npm run build` green before commit.
Localhost must be restarted (`npm run dev`) — old code keeps serving otherwise.
