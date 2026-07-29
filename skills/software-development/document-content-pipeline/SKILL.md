---
name: document-content-pipeline
description: "High-accuracy PDF extraction (opendataloader-pdf / ODL-PDF), batch markdown cleanup, and content pipeline for website injection. Covers PPT→PDF→Markdown→JSON→Next.js page workflows."
version: 1.1.0
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

---

## Step 0: DOX-Audit — Verify Reality vs Documentation

Before extracting anything, **verify that the documentation matches the filesystem**. AGENTS.md often references stale paths, nonexistent subdirectories, or projects that moved. Building a plan on stale DOX = wasted work.

```bash
# 1. Check root AGENTS.md directory claims vs reality
ls /Users/zaryu/Desktop/Niumination/
# Does it claim Production/ but reality shows apps/? Flag and correct first.

# 2. Check claimed child AGENTS.md files actually exist
for claim in "brain/AGENTS.md" "services/niu-cast/AGENTS.md" "desktop/x-downloader/AGENTS.md"; do
  [ -f "$HOME/Desktop/Niumination/$claim" ] && echo "✅ $claim" || echo "❌ $claim (stale claim)"
done
```

### Common DOX Stale Claims (v3.0 → v4.0 migration)
| Stale Claim | Reality |
|-------------|---------|
| `Production/PemdiAcehTengah/` | `apps/PemdiAcehTengah/` |
| `Production/cc-switch/` | Remote-only (not cloned) |
| `projects/niudash/` | `apps/niu-dash/` |
| `PI/` | `vault/` |
| `services/niu-cast/` | Exists (may be missed due to truncated ls) |
| `brain/AGENTS.md` | Often nonexistent — verify before relying on |

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
6. **DOX stale = wasted build**: AGENTS.md often references v3.0 paths (Production/, projects/, PI/) while the real filesystem is v4.0 (apps/, services/, desktop/). Always verify the directory structure against reality before planning the pipeline. A stale DOX claim about where files live can cascade into broken paths, missing symlinks, and failed deployments.
