---
name: document-content-pipeline
description: "High-accuracy PDF extraction (opendataloader-pdf / ODL-PDF), batch markdown cleanup, and content pipeline for website injection. Covers PPT→PDF→Markdown→JSON→Next.js page workflows."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [PDF, extraction, ODL, content-pipeline, website, markdown, modul, batch]
    related_skills: [ocr-and-documents, nextjs-tailwind-setup]
---

# Document Content Pipeline

High-accuracy PDF extraction and content migration pipeline for batch processing documents (especially PPT→PDF→Markdown) and injecting them into websites.

When to use:
- User needs to extract 10+ PDF/PPT files to Markdown
- PDFs contain complex tables, multi-column layouts, or mixed text+images
- Extracted content needs cleaning (remove PPT headers/footers, normalize headings)
- Content needs to be structured as JSON for website injection
- Building a Next.js page from batch-processed document modules
- **Auditing Pemdi evaluation evidence**: cross-referencing module page criteria, Excel working documents, and scan output to detect level naming mismatches — see `references/pemdi-evaluation-evidence-audit.md`

---

## Step 0: DOX-Audit — Verify Reality vs Documentation

Before extracting anything, **verify that the documentation matches the filesystem**. AGENTS.md often references stale paths, nonexistent subdirectories, or projects that moved. Building a plan on stale DOX = wasted work.

### Phase 1: Root Structure Claims vs Reality

```bash
# 1. Check root AGENTS.md directory claims vs reality
ls -d /Users/zaryu/Desktop/Niumination/*/
# Does it claim Production/ but reality shows apps/? Flag and correct first.

# 2. Check app/services/etc directory contents
for dir in apps services sites desktop agents labs sandbox; do
  echo "=== $dir/ ==="
  ls -d "/Users/zaryu/Desktop/Niumination/$dir/"*/
done
```

### Phase 2: DOX Chain Verification — Check Every Claimed AGENTS.md

The DOX chain table in root AGENTS.md often lists files that don't exist (moved, renamed, never created). Verify every single entry:

```bash
claims=(
  "brain/AGENTS.md"
  "apps/Niu-LKH/AGENTS.md"
  "apps/PemdiAcehTengah/AGENTS.md"
  "services/niu-cast/AGENTS.md"
  "desktop/flame-ade/AGENTS.md"
  "agents/orchestrator/AGENTS.md"
)
for claim in "${claims[@]}"; do
  test -f "/Users/zaryu/Desktop/Niumination/$claim" && echo "✅ $claim" || echo "❌ $claim"
done
```

Any ❌ is either a stale DOX claim or a missing AGENTS.md that should be created. Document the discrepancy; do not silently ignore it.

### Phase 3: Fix the DOX Before Building

If discrepancies exist (they will), fix `AGENTS.md` before doing anything else:

1. **Bump DOX version** in header
2. **Replace Directory Structure** — the entire tree, not individual lines
3. **Fix Project Catalog paths** — every table row that references a wrong path
4. **Fix DOX Chain list** — remove nonexistent entries, add missing ones
5. **Update Quick Links + Footer** — version, date, changelog
6. **Commit** separately so the DOX fix is its own reversible change

See `references/agents-md-migration-case-study.md` for a complete v3.0→v4.0 migration walkthrough with 15+ path corrections and detection methodology. See `references/agents-md-migration-quickref.md` for a 30-second detection checklist.

### Common DOX Stale Claims (v3.0 → v4.0 migration)
| Stale Claim | Reality |
|-------------|---------|
| `Production/PemdiAcehTengah/` | `apps/PemdiAcehTengah/` |
| `Production/cc-switch/` | `apps/cc-switch/` |
| `projects/niu-dash/` | `apps/niu-dash/` |
| `projects/cc-acehtengah/` | `services/cc-acehtengah/` |
| `projects/flame-ade/` | `desktop/flame-ade/` |
| `projects/x-downloader/` | `desktop/x-downloader/` |
| `projects/niu-cast/` | `services/niu-cast/` |
| `PI/` | `vault/` |
| `brain/AGENTS.md` | Often nonexistent — verify before relying on |
| `services/niu-cast/` | Exists (may be missed due to truncated ls) |

When DOX claims 40+ local projects but only ~20 exist on disk, the discrepancy itself is a finding — document it before planning. See `references/modul-indikator-website-pattern.md` for a real DOX-audit output.

---

## Step 1: ODL-PDF Extraction (opendataloader-pdf)

**opendataloader-pdf** (#1 benchmark, 0.907 overall accuracy) extracts PDFs to Markdown, JSON (with bounding boxes), HTML, and Tagged PDF.

### Prerequisites
- Java 11+ (`java -version`) — ODL-PDF runs a Java engine under the hood
- Python 3.10+

### Install
```bash
# 1. Install JDK if missing
brew install openjdk@21
ln -sf /usr/local/Cellar/openjdk/*/libexec/openjdk.jdk/Contents/Home/bin/java ~/.local/bin/java
export JAVA_HOME="/usr/local/Cellar/openjdk/*/libexec/openjdk.jdk/Contents/Home"

# 2. Install Python package
pip install opendataloader-pdf

# Verify
python3 -c "import opendataloader_pdf; print('OK')"
```

### Usage — Basic
```python
import opendataloader_pdf

# Single file
opendataloader_pdf.convert(
    input_path="document.pdf",
    output_dir="/tmp/output",
    format="markdown,json"
)
```

### Usage — Batch
```python
opendataloader_pdf.convert(
    input_path=["doc1.pdf", "doc2.pdf", "/path/to/folder"],
    output_dir="/tmp/output",
    format="markdown,json"
)
```

### Output
| Format | Description |
|--------|-------------|
| `.md` | Clean Markdown — ready for RAG/chunking |
| `.json` | Per-element detail with bounding boxes, font info, heading levels |
| `.html` | HTML representation |

### Batch Wrapper Script
Save to `scripts/odl-pdf.py`:
```python
#!/usr/bin/env python3
"""ODL-PDF batch extractor."""
import sys, os, json
HERMES_PY = "/Users/zaryu/.hermes-portable/venv/bin/python3"
JAVA_HOME = "/usr/local/Cellar/openjdk/*/libexec/openjdk.jdk/Contents/Home"
import subprocess
code = f"import opendataloader_pdf; opendataloader_pdf.convert(input_path='{sys.argv[1]}', output_dir='{sys.argv[2] if len(sys.argv)>2 else '/tmp/odl-output'}', format='markdown,json')"
os.environ.update({"JAVA_HOME": JAVA_HOME, "PATH": f"/Users/zaryu/.local/bin:{os.environ.get('PATH','')}"})
subprocess.run([HERMES_PY, "-c", code])
```

---

## Step 2: Cleanup Markdown (PPT→PDF Noise Removal)

PPT→PDF extraction often includes:
- Slide headers/footers ("Milik Kementerian PANRB", page numbers)
- Redundant whitespace
- Inconsistent heading hierarchy
- H4 used as emphasis instead of bold text

### Cleanup Script Pattern

Save as `scripts/cleanup-pdf-md.py`:

```python
import os, re

HEADER_NOISE = [
    r"(?i)^Milik\s*$",
    r"(?i)^Kementerian\s*$", 
    r"(?i)^PANRB\s*$",
    r"(?i)^slide\s*\d+\s*$",
    r"(?i)^halaman\s*\d+\s*$",
]

def clean_file(fpath, dry_run=False):
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 1. Remove first N lines if they're header noise
    cleaned = []
    noise_ended = False
    text_started = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not text_started and not stripped:
            continue
        if not text_started:
            text_started = True
        if not noise_ended and i < 15:
            if is_header_noise(line):
                continue
            noise_ended = True
        # 2. Remove inline single-word noise followed by image
        if is_header_noise(line) and i > 0:
            next_lines = lines[i+1:i+3]
            if any(l.strip() and l.strip().startswith('![') for l in next_lines):
                continue
        cleaned.append(line)
    
    text = ''.join(cleaned)
    
    # 3. Add H1 title if missing
    if not re.search(r'^# ', text, re.MULTILINE):
        title = os.path.basename(fpath).replace('.md','').replace('.pptx','')
        text = f"# {title}\n\n{text}"
    
    # 4. Normalize heading levels
    # 5. Remove excessive blank lines (max 1)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text
```

### Key Cleanup Rules
| Issue | Fix |
|-------|-----|
| H4 headers (`####`) | Convert to `**bold**` — not real headings |
| Extra H1 headings | Add H1 as document title, demote rest to H2 |
| Slide footers in body | Detect single-word lines followed by images, remove |
| H1→H1 in same file | Keep first as title, demote subsequent to H2 |
| Image paths with `<` `>` | Strip angle brackets: `![](<path>)` → `![](path)` |

---

## Step 2b: Locate & Render Specific PDF Pages for Screenshots

When you need screenshots of specific pages (e.g. evidence pages for a website section), **never convert printed page numbers to physical indices by arithmetic** — government PDFs (RPJMD, Qanun, regulations) have a printed page footer (II-116, III-28) that does NOT match physical page count (verified 4 Aug 2026: "II-116" was physical page 144, "II-141" was 169 — offset varies and is non-linear through the doc). Instead, locate pages by **text content** with PyMuPDF, then render to PNG:

```python
import fitz  # PyMuPDF — in /Users/zaryu/.hermes-portable/venv/bin/python3

doc = fitz.open("/path/to/large.pdf")  # 409 pages, 9.9MB — full-text scan is fast

# 1. Find physical page numbers by keyword (use the exact phrase that appears on the target page)
for i in range(len(doc)):
    if "evaluasi terhadap pelaksanaan SPBE" in doc[i].get_text().lower().replace("\n", " "):
        print("page", i + 1)  # ← physical page number

# 2. Sanity-check the found page before rendering (printed footer ≠ physical index)
print(doc[p-1].get_text()[:450])  # starts with "  II - 141  | ..." → confirms

# 3. Render at 150-160 dpi for a readable screenshot
pix = doc[p-1].get_pixmap(dpi=160)
pix.save("/tmp/pages/h178_tabel_spbe.png")
```

- Search terms should be a distinctive phrase from the page body, NOT the heading alone (headings repeat in the table of contents).
- Always print the found page's first ~400 chars to confirm you got the right page before rendering a batch.
- `get_text()` returns layout-jumbled text (tables read column-first) — that's normal; the search still works because words are present.
- Rendered PNGs → `public/docs/<slug>/` in the Next.js project, then reuse the existing preview modal for click-to-zoom.

---

## Step 2c: Offline OCR for Scanned PDFs (macOS Vision — no API quota)

When cloud vision (`vision_analyze`) is quota-exhausted/offline and ODL-PDF's easyocr path is unavailable (torch wheel issues on macOS arm64/Py3.14), use the **built-in macOS Vision framework via pyobjc** — free, local, no model downloads, ~1-2s/page. Verified 5 Agu 2026: extracted 7 scanned evidence PDFs (SK, KAK, laporan) fully offline.

```bash
pip install pyobjc-framework-Vision pyobjc-framework-Quartz   # often already in Hermes venv
```

**Script:** `scripts/ocr_vision.py <image.png> [...]` — prints OCR text per image.

**Batch pattern (scanned PDF → per-page text):**
```python
import fitz
doc = fitz.open("scan.pdf")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    pix.save(f"/tmp/ocr/{i:02d}.png")     # then: ocr_vision.py /tmp/ocr/*.png
```

**Pitfalls (learned 5 Agu 2026):**
- Naive pyobjc Vision calls can **hang indefinitely** — wrap with `signal.alarm(50)` timeout; keep recognition level **fast** (`VNRequestTextRecognitionLevelFast`) and **one language** (`en-US`). First attempt with `id-ID` + accurate level hung at 60s; `en-US` + fast returned text in seconds (Indonesian text still OCRs acceptably).
- Always test `page.get_text()` (pymupdf) first — OCR only when the text layer is empty.
- swiftc-based OCR compile takes minutes — prefer pyobjc (no compile step).

### 2d: ODL Re-extraction as Ground Truth — Audit JSON Content Against the Source

When user suspects page content is "kacau" (garbled) after many stacked edits, **re-extract from the original PDFs with ODL and diff against the derived JSON** instead of trusting the JSON. Verified 6 Agu 2026 on `Modul Indikator 1-20` → `data/modul-indikator.json`:

1. Run the batch extractor (`scripts/odl-pdf-batch.py`) — 20 PDFs → 20 `.md` + per-file `_images/` in ~1-2 min. **Check the output dir first** — a previous batch may be empty (0 files), which means the JSON was derived from something else or hand-transcribed.
2. **Corruption patterns to hunt in the JSON:**
   - **Duplicated phrase merge**: `"...dalam tahap penyusunan. Nasional Pemerintah Digital pada perencanaan Instansi Pemerintah dalam tahap penyusunan"` — a table cell's text concatenated twice. Detect: normalize (lowercase, collapse whitespace) then `norm.count(frag) > 1` for fragments of 20-30 chars.
   - **Description = heading**: a module's `deskripsi` contains "Aspek 1 - Indikator 2 ..." (a slide title, not prose).
   - **Cross-module identical criteria**: L1/L2 criteria across different modules share RAN-Pemdi phrasing — verify against source before calling it a bug; level-1 criteria legitimately share the planning-substance template.
3. **PITFALL — criteria tables are often IMAGES in PPT→PDF**: the level criteria/table content may live in `imageFileNNN.png` inside the extracted `_images/` folder, not in the `.md` text. OCR of those images yields garbage (logos, "panrb", "rAKHLA") — **do not OCR the images; grep the `.md` text** (`grep -n "<phrase>" <module>.md`) to find the real text rows that ODL did extract around the tables.
4. Ground truth order: `.md` text from ODL > re-render + read the PDF page > JSON. Fix the JSON from the `.md`, never the reverse.
5. **REBUILD STRATEGY (the fix half)**: after auditing, rebuild `level_kriteria` from the `.md` when the source has enough structure, else fall back to artifact-cleanup of the old JSON. Verified 6 Agu 2026:
   - **Level labels in PPT→PDF** follow the pattern `Kurang/Initiate (1 < nilai < 1,5)`, `Cukup/Emerging (1,5 < nilai < 2,5)`, `Baik/Developing`, `Sangat Baik/Embedded`, `Memuaskan/Leading` — but they vary wildly per module (some have 0 labels, some 7, some concatenated into headings like `...PemerintahDigitalCukup/Emerging(1,5<nilai<2,5)` with no spaces). Regex must allow both `Label (` and `Label(` and bare-boundary matches.
   - Per level, the `.md` has `## Kondisi` then `## Kriteria` (or `### Kriteria`); take text AFTER the last `Kriteria` heading, strip images (`![](` lines), floating slide numbers (bare `\d{1,2}` lines), and merge wrapped lines (join continuation lines that don't end in `.` or `:`).
   - **Rebuild only if ≥4 of 5 labels found**; otherwise cleanup old JSON artifacts (heading markers glued mid-sentence: `([^\s#])(\s*)(#{2,6}\s+)` → `\1\n\3`, `<br>` → `\n`, collapse 3+ newlines). 12 of 20 modules rebuilt cleanly; 8 fell back.
   - **Missing-level merge**: a rebuild can LOSE a level (e.g. only 4 labels in md). Fix: merge from the pre-rebuild JSON backup (`.bak-odl`) — for each level id in {1..5} absent from the rebuilt list, append the cleaned old-JSON criteria, then sort by level. This guarantees all 20 modules end at L1-L5 (some legitimately include L0 "Baseline").
   - `## Kondisi` vs `## Kriteria`: keep both blocks in the same `kriteria` string separated by their headings — the page's `formatKriteria()` renderer already splits headings/lists; the corruption came from merging them WITHOUT the heading markers, not from having them.
   - Keep the pre-rebuild JSON as `.bak-odl` / `.bak-odl2` — the merge step depends on it.
   - **BACKUP-ALSO-EMPTY → manual line-mapping recovery (no OCR)**: when the pre-rebuild backup is ALSO empty for a level (the JSON never had it), recover from the `.md` by block position, not by OCR of `_images/`. The text IS in the markdown — the labels are just missing or glued. Verified 6 Agu 2026 on 8 empty levels across I1/I14/I17/I20:
     - Label variants to hunt with `grep -n`: missing entirely (I14 L1 = first unlabeled `## Kriteria` block), glued into heading without spaces (`...PemerintahDigitalCukup/Emerging(1,5<nilai<2,5)`), or N unlabeled `### Kriteria` blocks in sequence (I17 has five blocks at lines 431/475/622/734/823 → assign L1→L5 by reading content progression: Initiate=perencanaan/substansi, Emerging=sebagian layanan, Developing=referensi untuk sebagian, Embedded=seluruh layanan + reviu, Leading=konsisten >2 tahun + reviu berkala).
     - Method: `grep -n "Kriteria" <module>.md` lists all blocks; read the first 3 lines of each block to identify which level it belongs to; then extract by line range (e.g. `sed -n '825,838p'`), strip the `### Kriteria`/`## Kondisi` marker lines, clean, and write into the JSON with `## Kriteria\n` prefix.
     - Verified fill map (start,end line ranges, 1-indexed): I1 L4 (825-838), I14 L1 (104-109), I14 L2 (211-216), I14 L3 (261-266), I17 L1 (431-436), I20 L2 (364-370), I20 L3 (520-530), I20 L4 (676-686). After this pass: 0 empty levels remain across all 20 modules.
   - **UI PREFERENCE (Pemdi modul-indikator page) — level criteria must render as CARDS in a GRID, not a table and NOT stacked vertically**: a previous tool (JCode) converted the per-level criteria to a `<table>` and the user explicitly rejected it. A later stacked-vertical version (`flexDirection:column`) was ALSO rejected as "kacau / tidak rapi... harusnya disusun lebih rapi, bukan disusun ke bawah" (verified 6 Agu 2026). The accepted pattern is a **responsive CSS grid**:
     - Wrapper: `display:'grid'; gridTemplateColumns:'repeat(auto-fill, minmax(340px, 1fr))'; gap:'0.75rem'; alignItems:'start'` → 2-3 cards per row on desktop, single column on narrow screens. Verify horizontally: 3 cards in the same row must share the same `y` with increasing `x` (check via `getBoundingClientRect()` in browser console).
     - Each level a card with `borderRadius:10px; overflow:'hidden'`, `display:'flex'; flexDirection:'column'; height:'100%'` (equal-height rows), header row `background:${lvColor}12` containing a solid `L{n}` badge (`background:lvColor; color:'#fff'`) + `LEVEL_LABEL`, body with `formatKriteria()` output and `overflowWrap:'break-word'`.
     - **Descriptions must also render markdown**: `{modul.deskripsi}` as a plain `<p>` shows raw `- 1. ...` / `#### Dasar Hukum` as literal text. Render via `<div className="kriteria-render" dangerouslySetInnerHTML={{__html: formatKriteria(modul.deskripsi)}} />` inside a `surface-2` panel. Never "improve" layout back to table or stacked column without asking.
   - **WORKFLOW — focus mode + localhost-first**: when the user says "fokus dulu di <X>" / "sembunyikan section lain", hide every section except the ones they name by wrapping each in `{false && ( ... )}` (keeps code intact, drops it from the production bundle — verify via bundle size drop in `next build` output). Then verify on localhost (`npx next build && PORT=3457 npx next start`), and DO NOT `git push` / `vercel --prod` until the user explicitly approves. The user works section-by-section and wants each step verified visually before anything ships.

### 2e: Post-Rebuild Artifact Cleanup — fix "inject mentah" (verified 6 Agu 2026)

⚠️ **ROOT CAUSE (verified 6 Agu 2026) — READ FIRST**: the source files (`~/Documents/Modul Indikator 1-20/`) are **PPT→PDF exports** (`1 20260602 Revamp Modul Indikator 1.pptx.pdf` — real PPT decks saved-as-PDF), NOT native PDFs. ODL-PDF's table/reading-order heuristics mangle absolute-positioned PPT text boxes → garbled output. **Artifact cleanup on such output is polishing garbage — the real fix is extracting from the original `.pptx` via python-pptx (see "Alternative: PPT Source" below)**, or if only PDFs exist, position-based extraction: PyMuPDF `page.get_text("blocks")` sorted by `(y0, x0)` reconstructs slide reading order far better than ODL. Use cleanup (this section) only as a stopgap, never as the final answer.

Even after the 2d rebuild, `data/modul-indikator.json` still showed raw-extraction artifacts on the page ("hasil yang kulihat masih kacau"). Final cleanup lives in `apps/PemdiAcehTengah/scripts/cleanup-modul-indikator.py` — idempotent, backs up to `data/modul-indikator.json.bak-clean`:

- **Scale**: 102 level_kriteria items — 15 patched manually from verified `.md` text (I1 L1/L5, I4 L0, I8 L0, I17 L1/L5, I19 L1-5, I20 L2-5 — worst-corrupted), 87 auto-cleaned. `data_dukung_modul` went 498 fragments → 261 clean bullets; `deskripsi` tables stripped.
- **Corruption patterns found AFTER the rebuild pass** (all handled by the script):
  - Heading glued mid-sentence: `## Kriteria Substansi Rencana...` → strip leading `Kriteria `/`Kondisi ` when followed by a capital letter.
  - Standalone heading labels (`## Kriteria` / `## Kondisi` / `## Data Dukung:`) → inline labels `Kondisi:` / `Data Dukung:` (renderer shows them as paragraphs); `Kriteria` dropped entirely because the card header already shows the level.
  - Raw markdown tables in `deskripsi` (`|A| |---| |B|` — e.g. I20 "Objek yang diukur") → split cells into lines, drop `---` separators; call `clean_core(text, strip_label_headers=False)` for descriptions so `Dasar Hukum` / `Objek yang diukur` sections survive as labels.
  - `data_dukung_modul` as per-line wrapped-paragraph fragments (`["Rancangan dokumen", "perencanaan Instansi", ...]`) → join wrapped lines into sentences, then re-split into clean bullets.
  - ODL paired italic markers `*teks*` → strip, but NEVER across newlines (cross-line match merges two bullets into one); leftover bare `*` before a capital → strip.
  - Wrapped list items (bullet ends mid-sentence, continuation starts lowercase) → join into the bullet; but never join bullet→bullet.
  - Duplicate/substring phrases (normalized fragment ≥40 chars appears inside another bullet) → keep the longer, drop the shorter. Beware false positives: L1..L3 across modules legitimately share RAN-Pemdi phrasing — dedup is per-level only.
- **Verification gates**: after cleanup the JSON must have 0 `|`, 0 `<br`, 0 `![](`/`imageFile`, 0 `^#{1,6}` lines, 0 levels < 60 chars, and no leading `Kriteria `/`Kondisi `. Then `next build` (expect 0 errors) + restart `next start` + verify in browser via `document.querySelector('main').innerText` slices per module (works on text-only models; vision may be unavailable).
- **Data completeness**: add `label: LEVEL_LABEL[lv]` (Baseline/Initiate/Emerging/Established/Leading/Transformative) to every level_kriteria item — cheap, harmless, consumed by downstream scripts.

---

## Step 3: Build JSON for Website

Convert cleaned markdown files to a structured JSON data file for Next.js/any frontend.

```python
import os, json, re, html

def build_json(clean_dir, output_json, module_meta=None):
    """Build website-ready JSON from cleaned markdown files."""
    modules = []
    files = sorted([f for f in os.listdir(clean_dir) if f.endswith('.md')])
    
    for fname in files:
        with open(os.path.join(clean_dir, fname)) as f:
            raw = f.read()
        
        # Extract identifier (e.g. number from "1 Title.pptx.md")
        match = re.search(r'(\d+)\s', fname)
        num = match.group(1) if match else "0"
        
        meta = module_meta.get(num, {"nomor": 0, "aspek": "General", "judul": fname})
        
        modules.append({
            "nomor": meta["nomor"],
            "aspek": meta["aspek"],
            "judul": meta["judul"],
            "ringkasan": extract_summary(raw),
            "html": md_to_html(raw),
            "gambar": len(re.findall(r'!\[\]\(', raw)),
        })
    
    return {"total_modul": len(modules), "modules": modules}
```

### Website Page Pattern (Next.js)
For injecting into a Next.js Pages Router site:

```jsx
// pages/modul-page.js
import moduls from '@/data/modul.json';
import { useState, useMemo } from 'react';

export default function ModulePage() {
  const [cari, setCari] = useState('');
  const [bukaModul, setBukaModul] = useState(null);
  
  const filtered = useMemo(() => {
    let list = moduls.modules;
    if (cari) list = list.filter(m => 
      m.judul.toLowerCase().includes(cari.toLowerCase()));
    return list;
  }, [cari]);

  return (
    <>
      <input type="text" value={cari} onChange={e => setCari(e.target.value)} 
             placeholder="Search modules..." />
      
      {filtered.map(modul => (
        <div key={modul.nomor}>
          <button onClick={() => setBukaModul(
            bukaModul === modul.nomor ? null : modul.nomor)}>
            {modul.nomor}. {modul.judul}
          </button>
          
          {bukaModul === modul.nomor && (
            <div dangerouslySetInnerHTML={{__html: modul.html}} />
          )}
        </div>
      ))}
    </>
  );
}
```

---

---\n\n## Step 4: Website Injection (Next.js Pages Router)\n\nAfter building the JSON data file and cleaning markdown, inject content into an existing Next.js site.\n\n### 4a: Serve Images via public/ Symlink\n\nImage-heavy content (500MB+ for 20 PPT decks) must be accessible to the Next.js static server. \n\n```bash\n# Create symlink inside public/ for image directories\nln -sf /abs/path/to/modul-indikator-clean public/docs\n\n# In JSON, reference images relative to this symlink:\n# /docs/modul-indikator-clean/_images/imageFile2.png\n# Resolves → public/docs/modul-indikator-clean/_images/imageFile2.png\n```\n\n### 4b: Create Accordion Page with Search + Filter\n\nCreate `pages/modul-indikator.js`:\n```jsx\nimport Head from 'next/head';\nimport { useState, useMemo } from 'react';\nimport moduls from '@/data/modul-indikator.json';\n\nexport default function ModulePage() {\n  const [cari, setCari] = useState('');\n  const [aspekFilter, setAspekFilter] = useState('all');\n  const [bukaModul, setBukaModul] = useState(null);\n\n  const filtered = useMemo(() => {\n    let list = moduls.modules;\n    if (aspekFilter !== 'all') list = list.filter(m => m.aspek === aspekFilter);\n    if (cari) list = list.filter(m =>\n      m.judul.toLowerCase().includes(cari.toLowerCase()));\n    return list;\n  }, [aspekFilter, cari]);\n\n  const semuaAspek = [...new Set(moduls.modules.map(m => m.aspek))];\n\n  return (\n    <>\n      <h1>📋 Modul Indikator</h1>\n      <input value={cari} onChange={e => setCari(e.target.value)} \n             placeholder=\"Cari...\" />\n      <select value={aspekFilter} onChange={e => setAspekFilter(e.target.value)}>\n        <option value=\"all\">Semua Aspek</option>\n        {semuaAspek.map(a => <option key={a}>{a}</option>)}\n      </select>\n\n      {filtered.map(modul => (\n        <div key={modul.nomor}>\n          <button onClick={() => setBukaModul(\n            bukaModul === modul.nomor ? null : modul.nomor)}>\n            {modul.nomor}. {modul.judul}\n          </button>\n          {bukaModul === modul.nomor && (\n            <div dangerouslySetInnerHTML={{ __html: modul.html }} />\n          )}\n        </div>\n      ))}\n    </>\n  );\n}\n```\n\n### 4c: Register Navigation\n\n```diff\n// components/AppShell.js — breadcrumbLabels\n+  '/modul-indikator': 'Modul Indikator Pemdi',\n\n// components/Sidebar.js — menuGroups\n+ { label: 'Modul Indikator', href: '/modul-indikator', icon: '📋', badge: '20' },\n```\n\n### 4d: Verify + Deploy\n\n```bash\ncd /path/to/nextjs-project\nnpx next build           # Expect 0 errors\n\ngit add pages/modul-indikator.js data/modul-indikator.json public/docs components/*.js\ngit commit -m \"feat: add modul indikator page — N modules\"\ngit push origin main      # Vercel auto-deploys\n```\n\n---\n\n## Alternative: PPT Source (Via JCode / python-pptx)\n\nWhen source files are `.pptx` (not PDF), extraction is better done via **python-pptx** (e.g., by JCode) — it preserves text box positions and slide structure. The output is still Markdown in the same directory structure; cleanup → JSON → website injection steps remain identical.\n\n| Source | Tool | Requires |\n|--------|------|----------|\n| PDF | ODL-PDF (Hermes) | Java 11+, Python 3.10+ |\n| PPT/PPTX | python-pptx (JCode) | python-pptx only |\n| Scanned PDF | ODL-PDF hybrid mode | OCR model (optional) |\n\n---\n\n## Pitfalls

1. **Java not found**: ODL-PDF requires `java` on PATH. Always verify with `java -version` before using. Install with `brew install openjdk@21`, symlink to `~/.local/bin/java`.
2. **Easyocr/torch fails on macOS**: ODL-PDF Python deps include `easyocr` which requires `torch`. On macOS, `torch` has no binary wheel for arm64 Python 3.14+. Solution: `pip install -e . --no-deps` then manually install deps except easyocr. OCR features degrade gracefully (lazy import) — only OCR path fails, not the default deterministic path.
3. **PPT→PDF reading order**: ODL-PDF is #1 for tables/text but PPT absolute positioning can still cause fragmented reading order. The cleanup script fixes most artifacts (noise removal, heading normalization).
4. **Image heavy output**: PPT slides render each text-box as individual PNG when the PPT uses images for text. Output can be 500MB+ for 20 files. Mitigation: cleanup script strips redundant images, compress remaining, or host externally.
5. **H1 inconsistency across files**: PPT extraction often produces 0 H1 or 29 H1 depending on slide structure. Always normalize programmatically after batch extraction.
6. **DOX stale = wasted build**: AGENTS.md often references v3.0 paths (Production/, projects/, PI/) while the real filesystem is v4.0 (apps/, services/, desktop/). Always verify the directory structure against reality before planning the pipeline. A stale DOX claim about where files live can cascade into broken paths, missing symlinks, and failed deployments. See references/agents-md-migration-quickref.md for a 30-second detection checklist.
7. **Stow symlinks break silently after folder rename**: When a folder tracked by GNU Stow is renamed (e.g. `rekap/` to `dotfiles/`), ALL existing stow symlinks across the users home directory silently become dead links - every ~/.zshrc, ~/.gitconfig, ~/.config/nvim, ~/.config/kitty/kitty.conf, etc. The symlink target path is frozen at creation time inside the symlink inode, so renaming the source folder does NOT update them. Stow has no built-in rebase command. Fix: delete all broken symlinks (find ~ -type l ! -exec test -e {} \; -delete), then re-run stow --target="$HOME" <package> for each stow-managed package. Do NOT attempt to use ln -sf to recreate them individually - let stow rebuild the entire tree. Verification: run file ~/.zshrc ~/.gitconfig ~/.config/starship.toml ~/.config/nvim and confirm none say "broken symbolic link".
8. **Printed page number ≠ physical PDF index**: Jangan hitung mapping linear — lihat Step 2b. Cari halaman via PyMuPDF text-search frasa unik isi halaman, verifikasi print 400 chars, baru render `get_pixmap(dpi=160)`.
9. **Bukti xlsx tanpa headless office**: render tabel PNG via PIL (`ImageDraw.text` + `ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)`), kolom fixed-width. Alur lengkap "dokumen kebijakan → substansi per indikator → section additive" ada di skill `pemdi-evidence-management` section 11-13.
