# Document-to-Indicator Mapping Pattern

## Overview

When analyzing a set of public documents (HTML/PDF from government websites) and mapping them to compliance indicators, follow this systematic approach.

## Step 1: Inventory

List all files, categorize by folder/topic:
```bash
find <folder> -type f | sort
```

## Step 2: Read and Extract

For HTML files: strip tags, extract readable text.
For PDF files: use pymupdf or marker-pdf for text extraction.

```python
import os, re

def extract_html_text(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    text = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()[:800]  # first 800 chars
```

## Step 3: Classify Evidence Strength

| Classification | Meaning | Status to set |
|---|---|---|
| **Kuat** (Strong) | Document directly satisfies the indicator requirement | `lengkap` |
| **Parsial** (Partial) | Document supports the indicator but doesn't fully satisfy it | `proses` |
| **Pendukung** (Supporting) | Document provides context but isn't primary evidence | `proses` |
| **Tidak relevan** | Document doesn't map to this indicator | skip |

**Key rule:** News articles are ALWAYS "proses" at best — they prove activity happened, not that formal documentation exists. Official documents (SK, LAKIP, SOP) can be "lengkap".

## Step 4: Map to Indicators

For each document, answer:
1. Which indicator(s) does it support? (I1-I20)
2. What level? (L1=Initiate, L2=Emerging)
3. What classification? (Kuat/Parsial/Pendukung)
4. What specific fact makes it relevant?

## Step 5: Batch Update

```python
status_updates = {
    "B12.1": {"status": "proses", "catatan": "CSIRT website active, formal SK needed"},
    "B20.1": {"status": "lengkap", "catatan": "SKM Dukcapil 2024: score 96.17, 100 respondents"},
}
# Apply to pemdi.json
```

## Step 6: What's Still Missing

After mapping all available documents, identify gaps:
- Indicators with NO public evidence → must request from OPD
- Indicators with only "proses" → need formal/official documents
- Common missing items: SK Tim Koordinasi, SK Forum SDI, LHA Audit, IKASANDI/IIV, Notulen rapat

## Common Government Document Types

| Document type | Typical indicator | Evidence strength |
|---|---|---|
| News article about program | I3, I19, I20 | Parsial |
| Portal/website screenshot | I5, I13, I17, I18 | Parsial |
| Official SK (Keputusan) | I1, I4, I5, I6, I12 | Kuat |
| LAKIP/LKIP | I1, I3, I13, I14 | Kuat |
| Renstra/Renja | I1, I3, I9 | Kuat |
| PKS/MoU | I4, I16 | Kuat |
| SOP/Pedoman | I2, I8, I19 | Kuat |
| Training certificate/report | I3, I11 | Parsial |
| Award/penghargaan | I19, I20 | Pendukung |
