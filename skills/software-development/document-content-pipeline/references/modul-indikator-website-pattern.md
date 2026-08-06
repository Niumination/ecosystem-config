# Modul Indikator Website Injection Pattern

Concrete example from PemdiAcehTengah website — 20 modul indikator from PPT→PDF→Markdown→JSON→Next.js page.

## Module Metadata Structure
```json
{
  "tentang": "Modul Indikator Pemdi — PermenPANRB 8/2026",
  "tahun": 2026,
  "total_modul": 20,
  "total_gambar": 1281,
  "modules": [
    {
      "nomor": 1,
      "aspek": "Aspek 1 — Tata Kelola",
      "judul": "Regulasi & Tata Kelola Pemdi",
      "file": "1 20260602 Revamp Modul Indikator 1.pptx.md",
      "ringkasan": "Tata kelola Pemdi adalah kerangka kerja...",
      "html": "<h3>Deskripsi</h3><p>...</p>",
      "gambar": 100
    }
  ]
}
```

## Aspek Grouping
| Aspek | Indikator |
|-------|-----------|
| Aspek 1 — Tata Kelola | 1, 2, 3 |
| Aspek 2 — Infrastruktur & Layanan | 4, 5, 6, 7, 8, 9, 10 |
| Aspek 3 — Layanan Digital | 11, 12, 13, 17, 18 |
| Aspek 4 — Pendanaan & SDM | 14, 15, 16 |
| Aspek 5 — Proses Bisnis | 19, 20 |

## Key Implementation Details

### HTML Conversion (md_to_simple_html)
- H1 → `<h1 class="modul-title">` (hidden in page CSS)
- H2 → `<h2>` (visible section headers)
- H3 → `<h3>` (subsection headers)
- H4 → `<strong>` (not real headings)
- Images → `<img src="/docs/...">` with `loading="lazy"`
- Tables → simple `<table><tr><td>` (ODL-PDF outputs pipe tables)
- Lists → consecutive `<li>` wrapped in `<ul>`

### Noise Removal (files without H1 before cleanup)
Before cleanup, 4 files had 0 H1 headings and Modul 5 had 29 H1. After normalization, all 20 files have exactly 1 H1.

### Static Image Serving
Gambar output (1281 files, 502MB) too large for git. Solution options:
1. Optimize PNG→WebP (~90% reduction) → commit
2. Host on CDN/cloud storage → reference via URL
3. Public symlink: `ln -sf /path/to/_images public/docs` (works for local dev only)

## Accordion Page CSS
```css
.modul-content :global(h1.modul-title) { display: none; }
.modul-content :global(img) { max-width: 100%; border-radius: 8px; }
.modul-content :global(table) { width: 100%; border-collapse: collapse; }
```
