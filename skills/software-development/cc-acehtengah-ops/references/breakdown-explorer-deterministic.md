# Breakdown "Pecah Jawaban" — deterministic drill-down (commit 7cc9a76, 29-Agu-2026)

User request (Afrizal): "sediakan tombol untuk merunutkan pecahan dari hasil output,
gunakan metode seperti mindmap di notebooklm, interaksi didalam output ai akan menjadi
lebih panjang dan terbatas **untuk menjaga usage model ai sapa**."

Translation into a hard rule: output-AI interactions may become richer/longer, but they
must NEVER add LLM calls. All drill-down is deterministic DB aggregation.

## Endpoint: GET /api/dtsen/breakdown

File: `src/app/api/dtsen/breakdown/route.ts` (no auth — aggregate data is public; k≥5
already applied at publish).

Query params:
- `scope=kecamatan|desa|desil` (default kecamatan)
- `kecamatan=<UPPER>` / `desa=<UPPER>` — filters (case-insensitive, see Linge pitfall)
- `program=pbi|pkh|bpnt` — count recipients per dimension instead of aggregate jiwa

Behavior:
- No program: `prisma.dtsenAgregatWilayah.groupBy` on PUBLISHED release → `{nama, jiwa, keluarga}`.
- `program=pbi`: `prisma.dtsenIndividu.groupBy` where `bansos: true` → `{nama, nilai}`.
- `program=pkh|bpnt` on the BAPPEDA release returns `rows: []` + a `note` explaining the
  data only distinguishes PBI (pbi_jk); pkh/bpnt are 0 in this import. Do NOT fabricate.
- Returns `{ok, scope, program, release:{releaseNumber, publishedAt}, total, rows}`
  sorted desc by jiwa/nilai.

## UI: BreakdownExplorer.tsx

Component at `src/components/BreakdownExplorer.tsx`, mounted from `AIResponseRenderer`.

- Button "🔍 Pecah Jawaban (rincian per wilayah)" toggles the explorer.
- Breadcrumb path state: `[{nama:'Kabupaten Aceh Tengah', scope:'kabupaten'}]` →
  kecamatan → desa → desil. `scopeFor(path)` maps path length → next scope.
- Each level fetched lazily from `/api/dtsen/breakdown`; clicking a row drills one
  level down; breadcrumb click goes back up. Bar shows % of total.
- Rows show `nilai ?? jiwa` with `toLocaleString('id-ID')`, keluarga count when present.
- `program` prop passed when the answer mentions PBI → level ≤2 fetches
  `?program=pbi` so a SAPA-sourced "Penerima PBI 129.946 Jiwa" metric can still be
  broken down via DTSEN per-kecamatan data.

## When the button appears (AIResponseRenderer)

```ts
const isDtsen = (response.dataSource ?? '').toLowerCase().includes('dtsen');
const programHint = /pbi|jaminan kesehatan|bantuan iuran|bantuan inisiatif/i.test(narasi ?? '') ? 'pbi' : null;
const showBreakdown = (isDtsen || programHint) && visualisasi && visualisasi.tipe !== 'none';
```

Note: the PBI chip answer's `dataSource` is `SAPA Aceh Tengah` (not DTSEN), so the
narasi-regex programHint is what surfaces the button there.

## Verified live numbers (for sanity checks)

- Total jiwa kabupaten (BAPPEDA release): 222.643 (agregat) — DB groupBy kecamatan sums.
- PBI per kecamatan total: 169.891; top: BEBESEN 24.182, SILIH NARA 20.438, PEGASING 19.313.
- PEGASING has 31 desa (top: SIMPANG KELAPING 2.894, KAYU KUL 1.412, KUNG 1.367).
- LINGE/LUMUT desil breakdown: desil1 309, desil2 155, desil3 155, desil5 95, desil4 63,
  desil6 43, desil7 24 (sum 844).
