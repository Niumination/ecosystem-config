# Cleanup + Build Scripts Reference

Two companion scripts for the document-content-pipeline workflow used in the Modul Indikator Pemdi project.

## scripts/cleanup-modul.py

Location in ekosistem: `scripts/cleanup-modul.py`

**Purpose:** Clean 20+ markdown files extracted from PPT→PDF (by JCode/python-pptx) by:
1. Removing slide header/footer noise ("Milik Kementerian PANRB", page numbers, single-word noise)
2. Adding missing H1 title from filename mapping
3. Normalizing heading hierarchy (extra H1 → H2, H4 → bold)
4. Stripping angle brackets from image paths `![](<path>)` → `![](path)`
5. Removing excessive blank lines (max 1)
6. Copying `_images/` directories alongside cleaned files

### Module Metadata (CLEAN_TITLE_MAP)
```python
CLEAN_TITLE_MAP = {
    "1": "Pilar 1 - Regulasi & Tata Kelola Pemdi",
    "2": "Aspek 1 - Indikator 2: Manajemen Layanan Digital",
    # ... map all N modules by number
}
```

### Output Cleanup Stats (20 files)
```text
1: 915→877 lines | 100 img | H1:1 H2:2
2: 1744→1681 lines | 185 img | H1:1 H2:20
...
Total: 20 files, 1281 images, 261KB output
```

## scripts/build-modul-json.py

Location in ekosistem: `scripts/build-modul-json.py`

**Purpose:** Convert cleaned markdown files to `data/modul-indikator.json` by:
1. Reading cleaned markdown files from `docs/modul-indikator-clean/`
2. Matching filename number to module metadata (aspek grouping, label)
3. Converting Markdown to simple HTML (h2, h3, p, ul, img, table)
4. Extracting first meaningful paragraph as summary
5. Grouping by aspek for filter UI
6. Writing 428KB data file consumable by Next.js

### Module Metadata (MODULE_ORDER)
```python
MODULE_ORDER = {
    "1": {"nomor": 1, "aspek": "Aspek 1 — Tata Kelola", "label": "Regulasi & Tata Kelola Pemdi"},
    # ... 20 entries across 5 aspek groups
}
```

### Aspek Groups
- Aspek 1 — Tata Kelola: Indikator 1, 2, 3
- Aspek 2 — Infrastruktur & Layanan: Indikator 4, 5, 6, 7, 8, 9, 10
- Aspek 3 — Layanan Digital: Indikator 11, 12, 13, 17, 18
- Aspek 4 — Pendanaan & SDM: Indikator 14, 15, 16
- Aspek 5 — Proses Bisnis: Indikator 19, 20

## Execution Order
```bash
# 1. JCode extracts PPT->Markdown to docs/modul-indikator/
# 2. Cleanup
python3 scripts/cleanup-modul.py      # Output: docs/modul-indikator-clean/
# 3. Build JSON
python3 scripts/build-modul-json.py   # Output: data/modul-indikator.json
# 4. Symlink images for web
ln -sf ...public/docs docs/modul-indikator-clean
# 5. Create page, register nav, build, push
```
