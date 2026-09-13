# Executive Port SPLP — 2026-09-02

## Trigger
Port `ExecutiveAnswerRenderer` + `executive-presentation` from `dev` (`cc-acehtengah/feat/ai-executive-answer-v3`) to `sapa-ai/main` SPLP-only.

## Files Cherry-Picked
```bash
git checkout dev -- src/components/ExecutiveAnswerRenderer.tsx \
  src/services/executive-presentation.ts src/types/index.ts \
  src/components/AIResponseRenderer.tsx
```

## SPLP-Only Stripping (MANDATORY)
`sapa-ai` has no DTSEN/Bapokting/login. Remove after checkout:
- `ExecutiveAnswerRenderer.tsx`: delete `import BreakdownExplorer` + `<BreakdownExplorer sourceLabel={response.dataSource} />` block
- `AIResponseRenderer.tsx`: delete `import BreakdownExplorer`, delete `const isDtsen/programHint/showBreakdown` block + `{showBreakdown && <BreakdownExplorer .../>}`
- Verify: `grep -r Breakdown src/components/` must be empty (or only leftover file not imported)

## Wiring
- `AIResponseRenderer` keeps flag: `NEXT_PUBLIC_AI_EXECUTIVE_UI !== 'false' → ExecutiveAnswerRenderer` (rollback path)
- `dashboard/page.tsx`: `<AIResponseRenderer response={aiResponse} onFollowUp={handleQuery} />` — required for follow-up chips

## Pitfalls Hit
- `dev` `AIResponseRenderer` had DTSEN-specific `showBreakdown` logic that would break in SPLP (no DTSEN dataSource). Leaving it causes false-positive chips.
- `ExecutiveAnswerRenderer` badge said `Fallback SPLP` — wrong for sapa-ai where SPLP IS primary. Patched to `SAPA SPLP`.
- Duplicate evidence (see grounding-maximal-2026-09-02.md) discovered same session — fix in same commit.

## Verify
```bash
npm run build  # ✓ Compiled
curl -X POST :3102/api/query -d '{"query":"stunting"}' # deterministic + executive presentation builds
grep -n "Breakdown" src/components/*.tsx  # must be 0
```
