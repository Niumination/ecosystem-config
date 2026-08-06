# Pemdi Evaluation Evidence Audit — Cross-Reference Methodology

> **Class:** Multi-source content verification for Pemdi (Pemerintah Digital) evaluation evidence.
> **Source:** PermenPANRB No. 8 Tahun 2026 tentang Evaluasi Kinerja Pemerintah Digital.
> **Context:** Kabupaten Aceh Tengah — 20 indikator × 5 level, 177 item bukti (L1-L5).

## The Core Pattern

When auditing Pemdi evaluation evidence, **always cross-reference at least 3 sources** before trusting any single one:

```
1. MODULE PAGE      → Official criteria from PermenPANRB (live web page)
2. EXCEL            → Working document (Daftar Lengkap Bukti Dukung.xlsx)
3. SCAN RESULT      → PemdiArena/deep scan output (evidence collected)
```

## Step-by-Step Cross-Reference

### 1. Extract Module Page Criteria

The module page (`/modul-indikator`) embeds a JSON payload in the Next.js chunk:

```python
import re, json

with open('modul_chunk.js') as f:
    content = f.read()

m = re.search(r"JSON\.parse\('(.+?)'\)", content, re.DOTALL)
if m:
    raw = m.group(1)
    raw = raw.replace("\\'", "'").replace('\\n', '\n')
    data = json.loads(raw)
    inds = data['q']  # Array of 20 indicators
```

Each indicator has: `indikator_id`, `judul`, `aspek`, `deskripsi`, `level_kriteria[1-5]`, `data_dukung_modul`.

Official level naming (PermenPANRB 8/2026):
| Level | Nama Resmi |
|:-----:|------------|
| L1 | Initiate |
| L2 | Emerging |
| L3 | **Established** |
| L4 | **Leading** |
| L5 | **Transformative** |

### 2. Load Excel Working Document

```python
import openpyxl
wb = openpyxl.load_workbook('Daftar_Lengkap_Bukti_Dukung.xlsx', data_only=True)
ws = wb['02_Daftar_Lengkap_Bukti_Dukung']
```

Key columns: `Level Kematangan` (e.g. "Developing/Baik"), `No. Level`, `Item Bukti Dukung`, `Bentuk Output Nyata`, `Penanggung Jawab`, `Unit Kerja`.

### 3. Load Scan Evidence (PemdiArena)

```python
import csv
with open('02_INDEKS_BUKTI_FINAL.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pass  # indikator, level, file_lokal, url_asal, sha256
```

### 4. Cross-Reference Checklist

| Check | What to Compare | Tool |
|-------|----------------|------|
| **Level naming** | Excel `Level Kematangan` vs Module `level_kriteria[n].level` | Python dict mapping |
| **Indicator count** | Excel items per indikator vs Scan items | Group by indikator |
| **Coverage by level** | Excel L1-L5 vs Scan collected items | Filter by level |
| **File availability** | Excel `Bentuk Output Nyata` vs actual files | os.walk + matching |
| **Rejected candidates** | Arena rejected list vs Excel items | CSV comparison |
| **External indicators** | I05 (SDI) & I18 marked "Eksternal" in Excel | Verify if auto-valued |

### 5. Common Discrepancies Found

**Kritis — Level naming mismatch (from real audit):**
```
Modul Page: L3=Established, L4=Leading, L5=Transformative
Excel:      L3=Developing/Baik, L4=Embedded/Sangat Baik, L5=Leading/Memuaskan
```
Excel uses a naming scheme from an *earlier* PermenPANRB version. MUST be aligned before SIAP Digital submission.

**Eksternal vs Manual — I05 & I18:**
Module page has full L1-L5 criteria with data dukung, but Excel marks them "Eksternal". Clarify which source prevails.

**Gap L3-L5:** Zero evidence collected for levels above L2 in most Pemdi evaluations, because evidence requires internal OPD documents (audit reports, SKs, governance docs).

## Audit Output Format

### Gap Analysis Per OPD

```
Indikator | Level | Artefak | OPD | Status
I04       | L2    | SK Tim Koordinasi Pemdi (bernomor) | Diskominfo | ❌ Draf ada, belum TTE
I09       | L2    | LHA Audit Keamanan TIK | Inspektorat | ❌ Rahasia publik
I12       | L2    | SK CSIRT + STR BSSN | Diskominfo | ❌ Rahasia publik
```

### Level Naming Correction

```
Excel "Developing/Baik"     → "Established"         (L3)
Excel "Embedded/Sangat Baik" → "Leading"            (L4)
Excel "Leading/Memuaskan"   → "Transformative"      (L5)
```

## Pitfalls

1. **Single-source trust**: Never trust Excel alone without module page verification. Excel is a working document, module page is the official specification.
2. **Stale data**: ZIP extracts often contain expired files (LAKIP 2021, Renstra 2012-2017). Always check dates.
3. **Berita/siaran pers** are NOT evidence — they describe activity but lack legal force. Reject them.
4. **Draf tanpa pengesahan** are NOT evidence — SK, SOP, Perbup must have nomor, tanggal, and TTE to count.
5. **OCR/encoding issues**: PDF scans may have corrupted text. Verify SHA-256 checksums when possible.
6. **Module page JSON escapes**: Use `.replace("\\'", "'").replace('\\n', '\n')` before `json.loads()`.
7. **Two skills with same name**: `document-content-pipeline` exists in both `documentation/` and `software-development/` — the `documentation/` one (v1.2.0) is the mature version with references.
