---
name: official-regulation-extraction
description: Use when research needs official Indonesian regulation text.
---

# Official Regulation Extraction

Working with a regulation — drafting a document that must follow it, or citing it
— requires the **actual regulation text, not a search snippet and not remembered
content**. The failure mode this skill exists to prevent: writing `UNCHECKED`
for one section of a document and then treating the whole document as done, when
the rest of it was always readable.

Extraction target: official Indonesian regulations (Permen, Perpres, Permendagri,
Perda, UU) published as PDFs on JDIH domains.

For citing what you have extracted, use `grounded-citations`.

## When to Use

- Drafting a document that must comply with a regulation (naskah dinas, SKP,
  laporan, surat — anything with legal formatting requirements)
- Any task that states a rule about formatting, limits, or obligations as if it
  were verified, when it was not verified
- Auditing a previously-written document that claims to follow a regulation

## Extraction: the recipe that actually works

```bash
# 1. Download the PDF directly — NOT via a web extractor
curl -sL -A "Mozilla/5.0" -o p.pdf "<peraturan.bpk.go.id / jdih URL>"
file p.pdf        # expect: PDF document, version 1.7, NN pages

# 2. Extract every page to text
gs -q -dNOPAUSE -dQUIET -dBATCH -dSAFER -sDEVICE=txtwrite -sOutputFile=out.txt p.pdf

# 3. Extract only a page range (annexes, specific sections)
gs -q -dNOPAUSE -dQUIET -dBATCH -dSAFER -sDEVICE=txtwrite \
   -dFirstPage=19 -dLastPage=74 -sOutputFile=lampiran.txt p.pdf
```

### Mandatory cleanup step

`txtwrite` output **contains carriage returns inside lines**. Without stripping
them, patterns like `^Pasal` do not match at all — the text looks present but
is silently unparseable, which reads as "the data is missing".

```bash
LC_ALL=C sed 's/\r//' out.txt
```

Filter the JDIH running footer when grepping for real content:

```bash
LC_ALL=C sed 's/\r//' out.txt \
  | grep -vE '^\s*$|www\.peraturan|jdih' \
  | grep -vE '^[ ]*-?[0-9]+ ?20[0-9]{2}, No\.[0-9]+|20[0-9]{2}, No\.[0-9]+ ?-?[0-9]+'
```

## Distinguish "not extractable" from "not extracted"

An annex being image-only is a property of the source document, not of your
method. Prove which one you are dealing with **before** claiming it is
unavailable:

```bash
# if an annex range yields almost nothing after the footer is stripped:
LC_ALL=C sed 's/\r//' lampiran.txt | grep -vE 'www.peraturan|2023, No' | wc -l
# a count of 2-3 across dozens of pages = genuinely image-only, verified
```

Only after that check may you report `NOT ACCESSIBLE (image annex, verified)`.
An `UNCHECKED` marker with no command output behind it is an admission that the
source was never tried — which is the exact error this skill prevents.

**Ghostscript handles body text only.** Image-based pages need OCR by another
route; do not loop on `gs` expecting different options to produce text that is
not there. Report the annex as an image and note that a manual transcription or
OCR run is required, then move on to the rest of the document.

## Counting enumerations literally

The single most common accuracy error with enumerations is stating a total
without counting. **Always recount from the source before publishing any total.**

```bash
# list every lettered item under an article
LC_ALL=C sed 's/\r//' out.txt | awk '/Pasal 14/,/Pasal 17/' | grep -E '^\s+[a-zv]\.\s'
```

Rules:
- Count **letters and articles literally**, never from memory and never from a
  prior draft — earlier numbers in the same document may themselves be wrong.
- A total that disagrees with the table under it is an error, not a rounding
  note. Fix the number, not the table.
- Alphabeted lists do not always end where you assume. Verify the final letter
  explicitly rather than assuming the range ends early.
- When a total changes, correct every place it was previously stated, including
  audit and summary documents that quoted the old figure.

## Citing format requirements precisely

Formatting rules are cited as `Bab P, Pasal N ayat (n) huruf x` — never
"praktik umum", never approximate. Before writing any figure, font name, or
dimension, grep the extracted text and confirm the exact value:

```bash
LC_ALL=C sed 's/\r//' out.txt | grep -n -E 'Arial|Bookman|spasi|cm|gram' | head -30
```

Do not carry a remembered figure into a document. A remembered font or margin
that differs from the regulation is worse than a blank — it produces a
compliant-looking document that is legally non-compliant.

## Archiving

Save both the PDF and the extracted text so a later session does not redo the
extraction:

```bash
mkdir -p ~/references/regulasi/<short-name>/
cp p.pdf ~/references/regulasi/<short-name>/
LC_ALL=C sed 's/\r//' out.txt > ~/references/regulasi/<short-name>/teks.txt
```

Regulation PDFs are large; keep them in a gitignored references directory rather
than committing them.

## Pitfalls

- **Web extractors mangle official regulation PDFs.** Page numbering, running
  headers, and annex pages are routinely lost, and the extractor may fail
  silently while returning a plausible partial document. Download the PDF
  directly and extract with Ghostscript; only fall back to a web extractor if
  the PDF URL is unreachable.
- **Stopping at the first unextractable section.** One unreadable annex is not a
  reason to skip 60 readable articles. Finish the readable text first, then
  report what is missing.
- **`UNCHECKED` as an untested claim.** If you cannot produce the command output
  behind a `NOT ACCESSIBLE` statement, you have written `UNCHECKED`. The two are
  different and only one is defensible.
- **Not stripping carriage returns.** Everything looks missing and grep returns
  nothing. Strip `\r` before any pattern work.
- **Citing from a search snippet or from memory.** Snippets support only what
  they literally say; remembered figures drift. Quote the extracted text.
- **Publishing a total before counting.** Recount every enumeration from the
  source. Recompute figures in your own earlier drafts too — they are as likely
  to be wrong as a guess.
- **Treating a blank annex as a method failure.** Retry a different extraction
  option once, confirm the page count yields nothing but footer, then stop and
  report it as image-only. Do not burn time on options that cannot produce text
  that is not in the file.

## Verification

Before relying on anything extracted:

```bash
file p.pdf                                        # page count is plausible
LC_ALL=C sed 's/\r//' out.txt | grep -c 'Pasal'   # articles present
LC_ALL=C sed 's/\r//' out.txt | grep -E 'Pasal 1[0-9]' | head   # structure intact
```

A readable article count on the order of the document's stated article count
means extraction worked. Fewer than that means the extraction is partial and the
result is not reliable.
