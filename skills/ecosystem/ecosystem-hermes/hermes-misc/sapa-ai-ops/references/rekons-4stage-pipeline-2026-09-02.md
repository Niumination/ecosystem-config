# Rekons: 4-Stage Deterministic Pipeline — 2026-09-02

## Architecture Principle
**Rules (Deterministic) carry 100% data truth; LLM is only Narrative & Reasoning Layer.**
If the deterministic engine is strong, you never get number manipulation, data hallucination, or misleading answers.

## Source
`rekons.md` in `services/sapa-ai/` — user-provided architecture spec.

## Stage 1: Intent & Scoring Engine (select headline indicator)

- **File**: `src/lib/sapa-client.ts` → `scoreIntent(records, topic)` + `dedupIndicators(records)`
- **Keyword extraction**: extract entity from user query (e.g., `stunting`).
- **Scoring rules**:
  - `+100` if indicator name contains exact topic match (`stunting`).
  - `+50` if contains synonym/variant (`kurus`, `gizi`, `vitamin`, `vaksin`, `bkb`).
  - `-50` if indicator name contains aggregate term (`seluruh`, `total`, `pemeriksaan`, `penerima`).
- **Dedup**: if two indicators share same value+unit+opd (e.g., `JAB(5) P stunting` = `Jumlah Balita Stunting` = 730 Orang), keep the more specific label.
- **Result**: `730 Orang — Jumlah Balita Stunting` selected as Primary Headline, NOT `16.936` (total balita).

## Stage 2: Context & Calculation Engine (derive metrics)

- **File**: `src/app/api/query/route.ts` → `toRecordMetasFromRows` + `scoreIntent` + denominator search.
- **Denominator search**: find `dipantau`/`seluruh`/`total` indicator in evidence.
- **Formula**: `prevalencePct = (stunting / dipantau) * 100` → `4.42% = 730/16523`.
- **Derived context** sent to UI: `{ prevalencePct, denominatorNilai, denominatorLabel }`.
- **Tag logic** (deterministic template):
  - Cakupan Vitamin A > 95% → "Sangat Tinggi"
  - Prevalensi Stunting < 10% → "Kategori Rendah (Terpantau)"
  - Prevalensi > 20% → rekomendasikan percepatan intervensi gizi

## Stage 3: Grouping & Unit Isolation (4 buckets)

- **File**: `src/services/executive-presentation.ts` → `bucketGroup(evidence)` + `cleanNarasi`.
- **Bucket A (Masalah Kesehatan)**: stunting, kurus, gizi buruk (satuan: Orang).
- **Bucket B (Cakupan Pemantauan)**: dipantau, seluruh balita, total (satuan: Orang).
- **Bucket C (Intervensi Medis)**: Vitamin A, vaksin, pemeriksaan gratis (satuan: % / Orang).
- **Bucket D (Dukungan Sosial/BKB)**: BKB, sarana, materi (satuan: Kelompok / Paket).
- **Narasi cleanup**: strip `Dari X record SAPA, topik mencakup Y indikator...` technical metadata from executive narrative.
- **`bucketSummary`**: one-line summary for UI header.

## Stage 4: Output JSON Schema + UI Rendering

### Output Schema (`ExecutivePresentation`)
```ts
interface ExecutivePresentation {
  version: 'v1';
  answerType: ExecutiveAnswerType;
  title: string;
  lead: string;               // headline with conclusion + recommendation
  narrative: string;           // clean narrative (no technical metadata)
  metrics: ExecutiveMetric[];
  visual: ExecutiveVisual;
  insights: ExecutiveInsight[];
  quickWins: ExecutiveQuickWin[];
  dataQuality: Array<{...}>;
  evidence: ExecutiveEvidence[];
  followUps: string[];
  provenance: {...};
  buckets: Record<string, ExecutiveEvidence[]>;  // NEW: 4 buckets
  bucketSummary: string;       // NEW: one-line summary
}
```

### UI Rendering (`ExecutiveAnswerRenderer.tsx`)
- **PrimaryMetric (Hero)**: shows value from `bucketA[0]` (730) not `metrics[0]` (16.936); badge `Prevalensi: ~4.42%`.
- **ContextKPICards**: 3 cards — Basis Data (16.523 Orang) | Tingkat Risiko (294 Orang) | Intervensi Utama (99,9%).
- **Evidence per Kategori table**: 3-tab grouped table (Masalah Kesehatan | Pemantauan | Intervensi | Dukungan) with category column.
- **Audit trail sidebar**: bucket summary, evidence count, tahun+satuan (replaces old "Kualitas jawaban").

## Commits
- `1b47be5` — Stage 1: intent scoring + dedup
- `742495b` — Stage 2: prevalence calculation
- `7880046` — Stage 3: bucket grouping + clean narrative
- `5381573` — Stage 4: UI Hero + 3 KPI cards + 3-tab evidence + audit trail

## Verification
```bash
curl -X POST :3104/api/query -H "Content-Type: application/json" -d '{"query":"stunting"}'
# Expected: lead contains "730 Orang" + "4.42%" badge + 3 KPI cards + bucket table
# 16.936 appears ONLY when query is "penerima paket pemeriksaan balita"
```
