---
name: sapa-ai-ops
description: Operate sapa-ai SPLP service.
---

# sapa-ai Ops — SAPA SPLP Public Service

Operational playbook for `~/Desktop/Niumination/services/sapa-ai/` — Next.js SPLP-gateway (no Prisma, no DTSEN, no Bapokting). Data source: `api-splp.layanan.go.id` (2048 records, 8 curated KPI). Sibling of `cc-acehtengah` but **SPLP-only public** — all DTSEN/Bapokting/login logic must be stripped when porting features.

## Branch & Source Model

- `main` = production (SPLP-only). `dev` = mirror of `cc-acehtengah/feat/ai-executive-answer-v3` (contains DTSEN, BreakdownExplorer, DTSEN lookups).
- When cherry-picking from `dev` → `main`, **strip DTSEN artifacts**: `BreakdownExplorer`, `programHint`/`isDtsen` checks, DTSEN role gates. See `references/executive-port-splp-2026-09-02.md`.
- Never merge `dev` directly into `main` — use `git checkout dev -- <files>` then patch.

## KPI Panel — Curated vs Naive

- Naive (removed 2026-09-02): `records.find` by regex `stunting|kemiskinan|ipm|...` — first match, wrong variant (e.g., "usulan kenaikan pangkat" for ASN), `deltaPct=null`.
- Curated (current): `computeKpis(records)` in `src/services/kpi.ts` — 8 KPI with `preferIncludes/avoidIncludes` + scoring v2 + multi-year delta. `/api/kpi` and `/api/report` now share `computeKpis` (single source of truth). See `references/kpi-curation-2026-09-02.md`.

## Deterministic Smart AI — Maximize Before Hybrid

Strategy (user-approved, 2026-09-02): **Phase A deterministic maximal, Phase B hybrid LLM**.

- Phase A (current): `POST /api/query` uses `buildDeterministicNarasi` + `buildVizFromEvidence` + `formatRibuan` from `src/services/grounding.ts` (ported from cc-acehtengah). Returns `HybridResponse` (narasi/visualisasi/rekomendasi) + legacy `answer/source/matched/aggregated/results/evidence` for compatibility. No `llm-client`, no `isMockMode`, live SPLP data.
- Phase B (stored): `callLLM` only as language polisher over deterministic `narasi` + `groundOutput` (numbers must be from evidence). Do not start B until A is maximal.
- Do not regress to `isMockMode`/`mockStream` — always real SPLP.

## Executive Answer Porting

- Source: `ExecutiveAnswerRenderer.tsx` (343 lines) + `executive-presentation.ts` (387 lines) + `ExecutivePresentation` types from `dev`.
- `AIResponseRenderer` delegates: `if (NEXT_PUBLIC_AI_EXECUTIVE_UI !== 'false') → ExecutiveAnswerRenderer` (rollback switch preserved).
- SPLP adaptation: remove `BreakdownExplorer` import/usage (DTSEN-only). Wire `onFollowUp={handleQuery}` in `dashboard/page.tsx` so follow-up chips work.

## Executive Renderer — Duplicate Evidence + Headline 16.936 vs 730 Pitfall

`buildVisual(table)` title + `EvidenceSummary` both render `visual.rows` sorted by `nilai desc` → headline shows `16.936` (total balita) instead of `730` (stunting). Fix (Tahap 4):
1. `EvidenceSummary` guards `if (visual.type === 'table') return null`.
2. `buildExecutivePresentation` **re-ranks evidence by topic token hit** before rendering `metrics` + `visual.rows`.
3. PrimaryMetric reads from `bucketA[0]` not `metrics[0]`.
4. `ExecutivePresentation` adds `buckets: Record<string, ExecutiveEvidence[]>` + `bucketSummary: string`.

## Deterministic 4-Stage Pipeline (rekons.md — user-approved architecture)

**Principle: Rules (Deterministic) carry 100% data truth; LLM is only Narrative & Reasoning Layer.**

| Stage | Function | File | Commit |
|-------|----------|------|--------|
| **1. Intent Scoring** | `scoreIntent(records, topic)` in `src/lib/sapa-client.ts`: +100 exact topic match, +50 synonym (kurus/gizi/vitamin), **-50 aggregate terms** (seluruh/total/pemeriksaan). Dedup `JAB(5)` vs `Jumlah Balita Stunting` (same 730 → keep specific label). | `sapa-client.ts` | `1b47be5` |
| **2. Context & Calculation** | `toRecordMetasFromRows` + `scoreIntent` + denominator search (`dipantau`/`seluruh`). Compute `prevalencePct = (stunting / dipantau) * 100` deterministically (e.g., `4.42% = 730/16523`). | `api/query/route.ts` | `742495b` |
| **3. Grouping & Unit Isolation** | `bucketGroup(evidence)` → 4 buckets: A=Masalah Kesehatan (730,294), B=Pemantauan (16.523,16.936), C=Intervensi (99,9% Vit A, 935 vaksin), D=Dukungan (1.018 BKB, 830 sarana). `cleanNarasi` strips `Dari X record SAPA...` metadata. | `executive-presentation.ts` + `types/index.ts` | `7880046` |
| **4. Output JSON Schema + UI** | `ExecutivePresentation` adds `buckets` + `bucketSummary`. UI: PrimaryMetric shows **730 from bucket A** not `metrics[0]` (16.936); badge `Prevalensi: ~4.42%`; `ContextKPICards` (Basis Data 16.523 | Risiko 294 | Intervensi 99,9%); evidence table 3-tab; sidebar `Audit trail`. | `ExecutiveAnswerRenderer.tsx` | `5381573` |

**Verification**: `curl -X POST :3104/api/query -d '{"query":"stunting"}'` → lead contains `730 Orang` + `4.42%` badge + 3 KPI cards + bucket table. `16.936` appears ONLY when query is `penerima paket pemeriksaan balita`.

## References

- `references/executive-port-splp-2026-09-02.md` — full cherry-pick + SPLP-strip recipe
- `references/kpi-curation-2026-09-02.md` — KPI scoring, prefer/avoid, delta logic
- `references/grounding-maximal-2026-09-02.md` — deterministic narration + viz + grounding before hybrid
- `references/rekons-4stage-pipeline-2026-09-02.md` — full 4-stage deterministik architecture (Intent→Calculation→Grouping→UI)
- `references/executive-lead-2026-09-02.md` — buildLead headline format + vectors
