---
name: ekosistem-content-verification
description: "Verify web/JSON content accuracy against source documents (DOCX/XLSX) for Niumination ecosystem projects — extract, compare, report, fix. Covers Pemdi data verification and general content audit patterns."
tags: [verification, audit, content, docx, xlsx, pemdi, niumination, data-integrity]
---

# Ekosistem Content Verification

Verify structured web content (JSON, JS data files) against authoritative source documents (SK DOCX, Excel bukti dukung). Produces a discrepancy report and automated fixes.

## When to Use

- The user asks you to check whether web content matches source documents
- A batch of new SK / telaahan / nota dinas documents arrives and needs to be reflected in the project data
- Pemdi evaluation data (aspek, indikator, PICs, bukti dukung counts) needs reconciliation against official documents
- Any project where JSON data files are the single source of truth for web rendering and need re-syncing with paper/Word/Excel originals

## Workflow

### Step 0: Inventory Source Documents

```bash
ls -la docs/<project-evaluasi-2026>/
# Expected files:
#   * SK_Tim_Koordinasi_Pemdi_*.docx
#   * Draft_SK_Tim_Asesor_Internal_*.docx
#   * Nota_Dinas_Pengantar_*.docx
#   * Telaahan_Staf_Pengesahan_*.docx
#   * Daftar_Lengkap_Bukti_Dukung_*.xlsx
```

### Step 1: Extract Structured Data from DOCX

Use Python with zipfile + ElementTree:

```python
import zipfile, xml.etree.ElementTree as ET

def extract_docx(path):
    z = zipfile.ZipFile(path)
    xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    paragraphs = []
    for p in root.findall('.//w:p', ns):
        texts = [t.text or '' for t in p.findall('.//w:t', ns)]
        if texts: paragraphs.append(''.join(texts))

    tables = []
    for tbl in root.findall('.//w:tbl', ns):
        rows = []
        for row in tbl.findall('.//w:tr', ns):
            cells = []
            for cell in row.findall('.//w:tc', ns):
                texts = [t.text or '' for t in cell.findall('.//w:t', ns)]
                cells.append(''.join(texts))
            rows.append(cells)
        tables.append(rows)

    z.close()
    return paragraphs, tables
```

**Where to find structured data inside DOCX:**

| Content | Where it lives |
|---------|---------------|
| SK Lampiran I (struktur tim) | Table with headers: No., Jabatan/Kedudukan, Kedudukan dalam Tim |
| SK Lampiran II (uraian tugas pokja) | Paragraphs after each Pokja heading — includes Koordinator, Cakupan, Uraian Tugas |
| Dasar Hukum | Numbered list items under "Mengingat" section |
| Nota dinas dasar hukum | Compact list (1a–1d) in the paragraph body |

### Step 2: Extract Tabular Data from XLSX

```python
import openpyxl

def extract_xlsx(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    result = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = [list(row) for row in ws.iter_rows(values_only=True)]
        # Convert None to empty string
        rows = [[str(c) if c is not None else '' for c in row] for row in rows]
        result[sheet_name] = rows
    wb.close()
    return result
```

**Key sheets to inspect:**

| Sheet | What it contains |
|-------|-----------------|
| `01_Ringkasan` | Per-aspek summary: Aspek name, Indikator names, manual/external/total counts, Penanggung Jawab |
| `02_Daftar_Lengkap_Bukti_Dukung` | Detailed 177-item breakdown with level, output type, PIC |
| `04_Matriks_PJ_per_Pokja` | Coordinator cross-reference: SK Tim Koordinasi appointees vs Asesor Internal appointees |
| `05_Rekap_Jenis_Output` | Output type categorization |
| `06_Daftar_Produk_Dokumen_Kunci` | Key product planning |

### Step 3: Compare Against Web Data Files

For each data point in the web files (pemdi.json, index.js, pemdi.js, Footer.js), check against the extracted document data:

1. **Aspek names** — compare Excel `01_Ringkasan` column B vs JSON `aspek[].nama`
2. **Indikator names** — compare Excel column D vs JSON `aspek[].indikator[].nama`
3. **Item counts** — compare Excel totals vs JSON `aspek[].total_item`
4. **Koordinator/PIC** — compare SK Lampiran II (paragraph headings) vs JSON `aspek[].koordinator` and `tim_koordinasi.pokja[].koordinator`
5. **Total counts** — Global totals (manual, eksternal, overall) from Excel Ringkasan header

### Step 4: Systematic Comparison Pattern

For each data field, apply this checklist:

```
[ ] Field exists in source document?
[ ] Field exists in web data?
[ ] Values match exactly? (if not, which is authoritative?)
[ ] If PIC has multiple names, are ALL present?
[ ] Naming convention consistent (short vs formal names)?
```

**Tip:** Print extracted document data side-by-side with web data for manual review. Group findings by severity:
- 🔴 **Mismatch** — wrong value, must fix
- 🟡 **Missing** — value absent from web data but present in source
- 🔵 **Inconsistency** — minor naming variance (e.g. "Keterpaduan" vs "Keterpaduan Layanan Digital")

### Step 5: Fix and Verify

1. **Patch the JSON/JS files** using `patch()` tool for precision
2. **Validate JSON** — `node -e "require('./data/pemdi.json')"` to check parseability
3. **Build test** — `npm run build` (Next.js) and verify 0 errors
4. **Re-check** — re-run the comparison for the fixed fields to confirm

### Step 6: Report

Present findings in this format:

```
## Hasil Audit [Project Name] vs [Source Docs]

### 🔧 Diperbaiki
- **Aspek X — [field]**: [was] → [now] (reason)

### ✅ Sudah sesuai
- [List of verified-correct items]

### ℹ️ Catatan
- [Minor inconsistencies, future work, data limitations]
```

**Key thing to watch for:** Also check related pages for hardcoded references to the same data — e.g. `lapor.js`, `dashboard-kepuasan.js`, `skm.js` may have copied the short indikator names as display text. These are human-readable labels, not authoritative field names, but updating them improves consistency.

## Pitfalls

- **DOCX XML namespace is required** — Always use `ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}` and prefix all element paths with `w:`.
- **XLSX `data_only=True` reads calculated values** — use this for bukti dukung counts (SUM formulas). Without it, formulas appear as `None`.
- **Excel Ringkasan names may differ from SK official names** — the Ringkasan sheet uses short names ("Keterpaduan") while the SK uses full names ("Keterpaduan Layanan Digital"). The SK/permen name is authoritative for web display; the Excel name is administrative convenience.
- **DOCX paragraph splitting** — A single logical paragraph can span multiple `w:p` elements when it contains structured elements (nested tables, images). Join adjacent paragraphs heuristically for coherent extraction.
- **PIC count mismatch** — Pokja in SK may list multiple coordinators (e.g. 5 for Keterpaduan Layanan Digital). The web data must list ALL of them, not just the primary.
- **Build succeeds but data is stale** — `npm run build` doesn't validate data correctness; it only checks parseability. Always do a manual spot-check on rendered fields after fixing.
- **total_item must match sum of indikator items** — Recalculate after any indikator-level change. Double-check against the Excel row-by-row total.

## References

See `references/pemdi-audit-structure.md` for the authoritative Pemdi Aceh Tengah field mapping (aspek names, indikator names, koordinator assignments, and item counts as of the 2026 SK documents).
