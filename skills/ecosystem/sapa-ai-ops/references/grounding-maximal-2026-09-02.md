# Grounding Maximal Before Hybrid — 2026-09-02

## Decision
User approved 2-phase: Phase A maximize deterministic, Phase B hybrid LLM (store option B).

## Phase A Implementation (`5978041`)
- Copied `src/services/grounding.ts` from `cc-acehtengah` (SoT Fase C: `buildDeterministicNarasi`, `buildVizFromEvidence`, `formatRibuan`, `groundOutput`).
- `POST /api/query` rewritten: no `isMockMode`, no `llm-client`:
  ```ts
  const evidence = retrieveRelevant + aggregateByIndicator
  const narasi = buildDeterministicNarasi(evidence) // enriched with record count + formatRibuan
  const visualisasi = buildVizFromEvidence(evidence) // metric/table/chart by shape + unit safety
  const rekomendasi = OPD-specific from evidence
  return { narasi, visualisasi, rekomendasi, dataSource, timestamp, evidence, ...legacy }
  ```
- `USE_MOCK_DATA`/`mock-data.ts` remains but unused — always live SPLP.

## Phase B (Stored, Not Yet Implemented)
`callLLM` as language polisher only: deterministic narasi → LLM rephrase → `groundOutput` (strip any numbers not in evidence). Same pattern as cc-acehtengah `processAIQueryStreaming` but SAPA-only (no DTSEN/Bapokting/Prisma).

## Duplicate Evidence Fix (`a2ca716`)
`ExecutiveAnswerRenderer` has `VisualSection(table)` (= evidence table titled "Evidence yang dipakai") + `EvidenceSummary` (= same table again). Fix: `EvidenceSummary` guards `if (visual.type === 'table') return null`. Badge `Fallback SPLP → SAPA SPLP` corrected in same commit. Follow-up chips wired via `onFollowUp`.

## Assessment After Phase A
Strengths: grounded numbers, adaptive viz. Weaknesses (P1-P3 backlog): lead/narasi duplicate (320char truncation), generic insights/quickWins, static followUps, redundant OPD column, weak empty-state. See SKILL.md for prioritized backlog.
