---
name: compliance-checklist-dashboard
description: "Build compliance/evaluation checklist dashboards from structured documents (Markdown, Excel, PermenPANRB instruments). End-to-end: parse checklist → JSON with status tracking → Next.js dashboard with filters, progress bars, grouped expandable items, and embedded document previews (iframe for HTML, PDF viewer). Covers document-to-indicator mapping, batch status updates from verified sources, and the 'lampiran' pattern for linking evidence files. Use when building dashboards for government compliance (Pemdi, SPBE, IKD, RB), audit tracking, or any scenario where a checklist of items needs status visualization with embedded source documents."
tags: [pemdi, spbe, compliance, dashboard, nextjs, government, checklist, evidence, bukti-dukung]
---

# Compliance Checklist Dashboard

End-to-end pattern for building compliance/evaluation checklist dashboards — from a structured checklist document (Markdown, Excel, PermenPANRB instrument) to a live Next.js dashboard with status tracking, progress visualization, and embedded document previews.

## Trigger
- "Build checklist dashboard for [compliance framework]"
- "Add bukti dukung / evidence tracking to dashboard"
- "Map documents to indicators and show status"
- "Embed document previews in checklist UI"
- Government compliance evaluation (Pemdi, SPBE, IKD, RB, LAKIP)

## Architecture

```
Source Document (MD/XLSX)
  ↓ parse
data/<project>.json (aspek → indikator → bukti_dukung)
  ↓ 
pages/<project>.js (filters, progress bars, expandable groups)
  ↓
public/bukti-dukung/<files> (HTML/PDF evidence documents)
  ↓
PreviewModal (iframe embed + "Open in new tab")
```

## Phase 1: Structured JSON Data Model

### Root fields
```json
{
  "tentang": "Framework name — PermenPANRB X/YEAR",
  "tahun": 2026,
  "target_indeks": 2.5,
  "total_item_bukti": 57,
  "aspek": [...]
}
```

### Aspek → Indikator → Bukti Dukung (3-level hierarchy)
```json
{
  "id": 1,
  "nama": "Tata Kelola dan Manajemen",
  "singkat": "Tata Kelola",
  "bobot": 10,
  "target": 2.5,
  "nilai": 1.0,
  "indikator": [
    {
      "id": "I1",
      "nama": "Tingkat Kematangan Tata Kelola",
      "nilai": 1.0,
      "target": 2.5,
      "bobot": 5,
      "penanggung_jawab": {
        "lead": "BAPPEDA",
        "support": ["Diskominfo", "Bag. Organisasi"]
      },
      "bukti_dukung": [
        {
          "id": "B1.1",
          "level": 1,
          "nama": "Draf RPJMD / Renstra",
          "detail": "Deskripsi spesifik dokumen yang dibutuhkan",
          "opd": ["Bappeda", "Diskominfo"],
          "status": "belum",
          "catatan": "Opsional: verifikasi notes",
          "lampiran": [
            {
              "file": "/bukti-dukung/01-tata-kelola/renstra_diskominfo.pdf",
              "label": "Renstra Diskominfo",
              "type": "pdf"
            }
          ]
        }
      ]
    }
  ]
}
```

### Status values
- `"belum"` — Item belum dikumpulkan
- `"proses"` — Bukti publik ditemukan, perlu verifikasi/resmi
- `"lengkap"` — Dokumen tersedia dan terverifikasi

### Lampiran field (document preview linking)
The `lampiran` array links bukti items to files stored in `public/bukti-dukung/`. Each entry:
- `file`: path relative to public/ (e.g., `/bukti-dukung/01-tata-kelola/file.pdf`)
- `label`: display name for the preview button
- `type`: `"html"` or `"pdf"` (determines iframe behavior)

## Phase 2: Document-to-Indicator Mapping

### Mapping workflow
1. Read source document (MD/XLSX checklist with item descriptions)
2. Create `bukti_dukung` array per indicator with unique IDs (`B{aspek}.{number}`)
3. For each item: `id`, `level` (1=Initiate, 2=Emerging), `nama`, `detail`, `opd`, `status`
4. Verify totals: `total_item_bukti` must equal sum of all bukti items across all indicators

### Batch status update pattern
When verifying documents against indicators:
```python
status_updates = {
    "B1.1": {"status": "proses", "catatan": "Document found, needs verification"},
    "B19.2": {"status": "lengkap", "catatan": "Full evidence available"},
}
for aspek in data["aspek"]:
    for ind in aspek["indikator"]:
        for bkt in ind.get("bukti_dukung", []):
            if bkt["id"] in status_updates:
                update = status_updates[bkt["id"]]
                bkt["status"] = update["status"]
                bkt["catatan"] = update["catatan"]
```

### Document analysis for mapping
When analyzing a set of public documents (HTML/PDF) to map to indicators:
1. Read each file, strip HTML tags, extract readable text
2. Identify key facts (who, what, when, which indicator)
3. Classify as: **Kuat** (strong evidence) / **Parsial** (partial) / **Pendukung** (supporting) / **Tidak relevan**
4. Map to specific indicator IDs
5. Only set `status: "lengkap"` when document FULLY satisfies the indicator requirement
6. Use `status: "proses"` for partial/supporting evidence

## Phase 3: Dashboard UI Components

### Component structure
```
PemdiPage
├── Hero Header (TopographicBackdrop)
├── KPI Summary Cards (baseline, current, target)
├── Progress Overview (overall + per-aspek cards)
├── Aspek Grid (clickable cards → DetailModal)
├── Checklist Section (filters + grouped expandable items)
│   ├── FilterBar (aspek, level, status selects)
│   └── GroupedChecklist (by indicator)
│       └── BuktiItem (status icon, badge, detail, OPD, preview buttons)
├── DetailModal (side panel with indikator + bukti checklist)
└── PreviewModal (full-screen iframe/PDF viewer)
```

### Key patterns

**Status badges with colors:**
```js
const STATUS_META = {
  belum:   { icon: '⬜', label: 'Belum', color: 'var(--muted)', bg: 'var(--surface-2)' },
  proses:  { icon: '🔄', label: 'Proses', color: 'var(--gold)', bg: 'var(--gold-light)' },
  lengkap: { icon: '✅', label: 'Lengkap', color: 'var(--ok)', bg: 'var(--ok-bg)' },
};
```

**Grouped checklist by indicator:**
- Flatten all bukti items with parent context (aspekId, indId)
- Group by `${aspekId}|${indId}`
- Each group has expand/collapse toggle
- Shows progress count (done/total) in header

**Filter system:**
- 3 independent filters: Aspek, Level (L1/L2), Status
- `useMemo` for filtered results
- Count display: "X item ditampilkan"

## Phase 4: Embedded Document Preview

### PreviewModal component
- Full-screen overlay with backdrop blur
- iframe `src={file.file}` for both HTML and PDF
- Header with file label, type badge, "Open in new tab" link, close button
- Escape key to close
- Body scroll lock when open

### PreviewButton component
- Shows only when `bukti.lampiran` array exists and is non-empty
- Renders one button per lampiran entry
- Button style: outlined with primary color, icon based on type (📄/🌐)
- Hover effect: fill primary color
- `e.stopPropagation()` to prevent parent click handlers

### File storage pattern
```
public/bukti-dukung/
├── 00-manifest/        (general docs)
├── 01-tata-kelola/     (governance docs)
├── 02-keamanan/        (security docs)
├── 03-infrastruktur/   (infrastructure docs)
└── 04-layanan/         (service docs)
```

Files are committed to the repo so they're available on GitHub Pages / Vercel deployment.

## Phase 5: Data Validation

### JSON integrity checks
```python
# 1. Total matches actual count
assert data["total_item_bukti"] == len(all_bukti)

# 2. All required fields present
for field in ["id", "level", "nama", "detail", "opd", "status"]:
    assert field in bkt

# 3. Valid status values
assert bkt["status"] in ["belum", "proses", "lengkap"]

# 4. No duplicate IDs
assert len(ids) == len(set(ids))

# 5. Every indicator has bukti_dukung
for ind in all_indicators:
    assert "bukti_dukung" in ind and len(ind["bukti_dukung"]) > 0
```

### Build verification
```bash
node -e "const d=require('./data/file.json'); console.log(d.total_item_bukti, 'items')"
# Quick syntax + structure check before commit
```

## Pitfalls

### 1. `total_item_bukti` drift
After adding/removing bukti items, the root `total_item_bukti` must be recalculated. Always verify: `sum(len(ind["bukti_dukung"]) for all indikator) == total_item_bukti`.

### 2. Lampiran path must be relative to public/
The `file` field in lampiran is an absolute URL path from the site root, not a filesystem path. Use `/bukti-dukung/folder/file.ext` not `public/bukti-dukung/...`.

### 3. HTML files may render blank in iframe
Some HTML pages rely on JavaScript that doesn't execute in iframe context, or have CSS that makes content invisible. Test each preview. Fallback: provide "Open in new tab" as primary action.

### 4. PDF size in repo
PDFs can be large (1-8MB each). 42 files = ~31MB. This is fine for GitHub but may slow initial clone. Consider `.gitattributes` for LFS if total exceeds 100MB.

### 5. Status "proses" vs "lengkap"
"Proses" means evidence exists but isn't fully verified (e.g., a news article about a program, not the official document). "Lengkap" means the actual required document is available and verified. Err on the side of "proses" — it's safer.

### 6. Grouped checklist performance
With 57+ items, the grouped checklist renders fine. If scale exceeds 200+ items, consider virtual scrolling or pagination.

### 7. PreviewModal body scroll lock
When the modal opens, set `document.body.style.overflow = 'hidden'`. On close, restore to `''`. Without this, the background page scrolls behind the modal.

### 8. `e.stopPropagation()` on preview buttons
Preview buttons are inside clickable parent elements (expandable groups). Without `stopPropagation()`, clicking Preview also toggles the expand/collapse.

## Example: Pemdi Aceh Tengah

- **Framework:** PermenPANRB No. 8 Tahun 2026
- **Structure:** 7 Aspek, 20 Indikator, 57 Bukti Dukung
- **Data file:** `data/pemdi.json`
- **Page:** `pages/pemdi.js`
- **Evidence:** `public/bukti-dukung/` (42 files from gov websites)
- **Preview:** iframe for HTML, PDF viewer for PDFs
- **Status after analysis:** 2 lengkap, 22 proses, 33 belum

### 9. Subagent batch file analysis is unreliable for document mapping

`delegate_task` subagents frequently fail when analyzing sets of HTML/PDF files due to model availability issues (404 on free models, iteration budget exhaustion on large file sets). The reliable pattern is `execute_code` with direct Python file reading:

```python
import os, re
for root, dirs, files in os.walk(base_dir):
    for f in sorted(files):
        if f.endswith('.html'):
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                raw = fh.read()
            text = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL|re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.IGNORECASE)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            # Use first 600-800 chars as summary for mapping
```

For PDFs, use `pymupdf` or `marker-pdf` (see `ocr-and-documents` skill) rather than raw file reading.

## References
- `references/pemdi-data-structure.md` — full JSON schema for Pemdi Aceh Tengah
- `references/document-mapping-pattern.md` — how to analyze and map document sets to indicators
