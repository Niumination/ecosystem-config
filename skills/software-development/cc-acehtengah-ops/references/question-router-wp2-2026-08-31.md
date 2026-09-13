# Question Router WP2 — Integrasi Notes

> Catatan implementasi 31-Agu-2026: semantic layer + archetype routing ke ai-orchestrator.

## Ringkasan

Question Router (`routeQuestion`) diimplementasikan sebagai komponen WP2 dari PR Lapis 2. Berbasis scoring keyword, bukan first-match. Menghasilkan `QuestionPlan` dengan archetype + confidence + concepts + geo + period.

## Arsitektur

```
query string
    │
    ▼
scoreArchetype(query)          ← keyword banking per archetype
    │
    ▼
sort by score descending
    │
    ├─ personal (100) ────────→ DTSEN deflection (existing)
    ├─ meta (80) ──────────────→ meta-query (existing)
    ├─ trend (60+) ────────────→ buildTrendResponse (existing)
    ├─ comparison (55+) ───────→ buildComparisonResponse (existing)
    ├─ ranking (50+) ──────────→ NEW: bar chart top 5
    ├─ distribution (50+) ─────→ NEW: pie chart per OPD
    ├─ correlation/anomaly (45+) → NEW: table top 3 evidence
    └─ level (10) ─────────────→ LLM fallback
```

## Field Mapping: SapaRecord vs EvidenceItem

**SapaRecord** (`ctx.filteredData`):
```typescript
{
  id: number;
  id_kode_indikator: number;
  kode_indikator_nama_indikator: string | null;  // nama indikator
  opds_nama_opd: string;                          // nama OPD
  satuan: string;
  tahun: string | null;
  variabel: string;                               // nilai numerik string
}
```

**EvidenceItem** (`ctx.evidence`):
```typescript
{
  opd: string;
  indikator: string;
  nilai: string;
  satuan: string;
  tahun: string | null;
  id: number | string;
}
```

**Pola akses di handler:**
- Ranking: map `ctx.filteredData` → `{nama, nilai, satuan, tahun, opd}`, sort by `parseFloat(variabel)` desc
- Distribution: group `ctx.filteredData` by `opds_nama_opd` (SapaRecord tidak punya field kecamatan/desa)
- Correlation/Anomaly: pakai `ctx.evidence` langsung (top 3 sorted by index order)

## Pitfalls

1. **SapaRecord tidak punya field geografis** (kecamatan/desa). Distribution handler harus pakai OPD sebagai proxy, atau warning "geo data tidak tersedia di SAPA".

2. **EvidenceItem tidak punya field `skor`** — sorting berdasarkan urutan insertion (sudah urut relevansi dari buildContext). Jangan pakai `(b.skor ?? 0) - (a.skor ?? 0)`.

3. **DIST_KW regex** perlu include `tiap` (bukan hanya `per`):
   ```typescript
   const DIST_KW = /per\s+(kecamatan|desa|wilayah|opd)\b|setiap\s+kecamatan|masing.masing\s+kecamatan|tiap\s+kecamatan/i;
   ```

4. **parseNumericId** perlu handle satuan di belakang angka dengan spasi:
   ```typescript
   // "730 Orang" → 730
   s = s.replace(/^[^\d-]+/, '');    // buang prefix
   s = s.replace(/ [^\d,.-].*$/, ''); // buang suffix satuan
   ```

## Test Cases (69/69 hijau)

```typescript
// Dari semantic-layer.test.ts
['tren stunting 5 tahun terakhir', 'trend']
['bandingkan kemiskinan antar kecamatan', 'comparison']
['kecamatan tertinggi stunting', 'ranking']
['persen desil 1 per kecamatan', 'distribution']
['hubungan kemiskinan dan stunting', 'correlation']
['berapa OPD yang melaporkan data', 'meta']
['data NIK warga Bebesen', 'personal']
['jumlah penduduk Aceh Tengah 2025', 'level']
['berapa persen keluarga desil 1', 'level']  // tanpa geo breakdown
```

## Integration Point

Di `ai-orchestrator.ts` → `tryDeterministicDomainQuery`, setelah block Bapokting:

```typescript
if (!result) {
  const plan = routeQuestion(query);
  const top3 = [...ctx.evidence].slice(0, 3);
  
  if (plan.archetype === 'ranking' && top3.length > 0) {
    // ... handle ranking
  }
  if (plan.archetype === 'distribution' && plan.geo.level !== 'kabupaten') {
    // ... handle distribution
  }
  if ((plan.archetype === 'correlation' || plan.archetype === 'anomaly') && top3.length >= 2) {
    // ... handle correlation/anomaly
  }
}
```

## Commits

- `215803b` feat(ai): PR Lapis 2.1 — Question Router (WP2)
- `81003e1` docs: update STATUS-CC.md — PR Lapis 2.1
