# Bapokting Deterministic Query — Pattern & Pitfalls

> Catatan dari implementasi 31-Agu-2026: fix output Bapokting yang "masih sama seperti lama" saat klik chip keyword.

## Problem Statement

Output AI untuk query harga komoditas (chip Bapokting) tidak berubah — masih menampilkan hasil SAPA/DTSEN yang tidak relevan, bukan data harga Bapokting.

## Root Causes (3 bug)

### Bug 1: Regex escape salah di `grounding.ts`

**Symptom:** semua `harga: 0` di chart Bapokting.

**Cause:** regex `/[^\\d.-]/g` (4 backslash) di file TypeScript literal regex. Di JavaScript/TypeScript, `/[^\\d.-]/g` berarti "selain karakter `\`, `d`, `.`, `-`". Akibatnya digit `1`,`6`,`0` dianggap "bukan digit" → dibuang semua → string kosong → `Number("")` = `0`.

**Fix:** gunakan 2 backslash: `/[^\d.-]/g`.

```typescript
// SALAH (4 backslash):
harga: Number(String(e.nilai).replace(/[^\\d.-]/g, '')) || 0;

// BENAR (2 backslash):
harga: Number(String(e.nilai).replace(/[^\d.-]/g, '')) || 0;
```

**Verify dengan node:**
```bash
node -e "console.log('16000'.replace(/[^\\\\d.-]/g, ''))"  # → "" (kosong)
node -e "console.log('16000'.replace(/[^\d.-]/g, ''))"     # → "16000" (benar)
```

### Bug 2: Tidak ada jalur deterministik Bapokting

**Symptom:** query harga jatuh ke LLM dengan evidence campuran SAPA+DTSEN.

**Fix:** tambahkan blok di `tryDeterministicDomainQuery` di `ai-orchestrator.ts`:

```typescript
if (!result && ctx.bapoktingEvidence.length > 0) {
  // Jawab langsung dari data Bapokting, TANPA LLM
  // - Filter komoditas spesifik dari query
  // - Fetch historis 7 hari untuk tren
  // - Return chart line (tren) atau bar (perbandingan)
  // - dataSource = "Bapokting Aceh Tengah (SPLP API)"
}
```

### Bug 3: Evidence Bapokting tidak ter-filter

**Symptom:** query "harga beras" menampilkan 76 komoditas campur (beras, cabai, minyak, gula, dll).

**Fix:** ekstrak keyword dari query, filter evidence hanya komoditas yang relevan:

```typescript
const targetKomoditas = ['beras', 'cabai', 'bawang', 'minyak', 'gula', 'sapi', 'ayam']
  .filter((k) => new RegExp(`\\b${k}\\b`, 'i').test(queryLower));

const relevantEvidence = targetKomoditas.length > 0
  ? bk.filter((e) => targetKomoditas.some((k) => (e.indikator ?? '').toLowerCase().includes(k)))
  : bk;
```

## Implementation Notes

### SPLP API Historical Fetch

Endpoint mendukung parameter `tanggal`:
```
GET https://api-splp.layanan.go.id/bahan-pokok-penting-kabupaten-aceh-tengah/1.0/api/bapokting/harga?tb=data_aset&s=kecamatan&f=desil&tanggal=2026-08-24
```

Response structure:
```json
{
  "status": "success",
  "sumber": "DISPERINDAG",
  "tanggal": "2026-08-24",
  "daftar_harga": [
    { "id": 3123, "komoditi": "Beras 88", "harga_eceran": 16000, "satuan": "Kg" }
  ]
}
```

### Trend Calculation

Untuk setiap komoditas target:
1. Ambil harga hari ini (`latest`)
2. Ambil harga 7 hari lalu (`weekAgo`)
3. Hitung perubahan: `((latest - weekAgo) / weekAgo) * 100`
4. Klasifikasi: `naik` jika > 2%, `turun` jika < -2%, `stabil` lainnya

### Chart Types

- **Line chart** (tren): `config.type = 'line'`, `config.lines = ['hargaTerakhir', 'persentasePerubahan']`
- **Bar chart** (perbandingan): `config.type = 'bar'`, `config.bars = ['harga']`

### Frontend Compatibility

`ChartRenderer` di `AIResponseRenderer.tsx` expects:
- `config.type`: `'bar' | 'line' | 'area' | 'pie' | 'donut'`
- `config.data`: array of objects
- `config.xKey`: key untuk sumbu X
- `config.lines` atau `config.bars`: array string key untuk series

## Commits

- `ca41442` — Jalur Bapokting deterministik
- `71560cb` — Fix regex escape `[^\\d.-]` → `[^\d.-]`
- `dc4f411` — Filter komoditas spesifik di query
- `b9895af` — Analisis tren harga 7 hari terakhir
