# macOS Vision Framework OCR — offline fallback (verified 5 Aug 2026)

**When to use**: `vision_analyze` (Gemini) quota exhausted (HTTP 429), no tesseract
installed, marker-pdf too heavy (~5GB), and the PDFs are pure scans. macOS-native,
free, no model downloads. Works in the Hermes portable venv (`import Vision` available).

## 1. Detect scan PDFs (no text layer)

```bash
pdftotext -l 2 file.pdf - | head          # output only "\f" → scan
```

or with PyMuPDF:

```python
import fitz
doc = fitz.open('file.pdf')
print(bool(doc[0].get_text().strip()))    # False → scan
```

## 2. Render pages to PNG

```python
import fitz
doc = fitz.open('file.pdf')
for p in range(len(doc)):
    pix = doc[p].get_pixmap(dpi=150)
    pix.save(f'/tmp/ocr/file_p{p+1}.png')
```

## 3. OCR with macOS Vision (pyobjc) — THE WORKING SCRIPT

```python
#!/usr/bin/env python3
"""OCR via macOS Vision framework (pyobjc) — offline, gratis."""
import sys, signal
import Vision
from Foundation import NSURL

def ocr_image(path):
    url = NSURL.fileURLWithPath_(path)
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    req = Vision.VNRecognizeTextRequest.alloc().init()
    # ⚠️ CRITICAL: Fast + en-US + NO language correction.
    # Accurate level or id-ID language HANGS (no output, >60s).
    req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelFast)
    req.setRecognitionLanguages_(["en-US"])
    req.setUsesLanguageCorrection_(False)
    ok, err = handler.performRequests_error_([req], None)
    if not ok:
        return f"ERROR: {err}"
    lines = []
    obs = req.results() or []
    # Reading order: top-to-bottom, left-to-right
    obs = sorted(obs, key=lambda o: (-o.boundingBox().origin.y, o.boundingBox().origin.x))
    for o in obs:
        c = o.topCandidates_(1)
        if c and len(c) > 0:
            lines.append(c[0].string())
    return "\n".join(lines)

def handler(signum, frame):
    print("TIMEOUT_OCR")
    sys.exit(124)

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(45)
    print(ocr_image(sys.argv[1]))
```

## 4. Batch pattern (10+ pages)

- Render ALL pages first, then OCR each → one `.txt` per source PDF with
  `===== HALAMAN N =====` delimiters.
- Run as a background process (each page ~5-15 s); poll progress. Never run
  dozens of pages in a foreground call.
- For scanned PDFs with embedded images, extract the embedded image
  (`page.get_images()` + `fitz.Pixmap(doc, xref)`) instead of re-rendering.

## 5. Gotchas

- **swiftc is a trap**: compiling a Vision swift script takes 180s+ and the
  result can still hang. Go straight to python pyobjc in the venv.
- **Accurate + id-ID = hang**: even with SIGALRM timeout. Only
  Fast + en-US + `usesLanguageCorrection=False` returns reliably.
- **XLSX preview thumbnails** (no office): `qlmanage -t -s 1200 -o /tmp file.xlsx`
  → `file.xlsx.png`, usable as `url_preview` for spreadsheet evidence.
- OCR quality on Indonesian government docs (scan of printed A4) is good
  enough to identify document title/nomor/tanggal and extract the substance
  needed for mapping to dokumen kunci — not for byte-exact transcription.
