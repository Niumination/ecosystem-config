# Cleanup & Build Scripts — Actual Files (29 Jul 2026)

Two scripts developed for the PemdiAcehTengah modul-indikator pipeline (20 PPT→PDF→Markdown→JSON→Website).

## Cleanup Script

**Path:** `~/Desktop/Niumination/scripts/cleanup-modul.py`

Normalizes batch-extracted markdown: removes slide header/footer noise, normalizes H1/H2/H3/H4 hierarchy, collapses excessive blank lines, strips angle brackets from image paths, makes image paths relative.

### Key mappings
| PPT file number | Clean title |
|:---:|---|
| 1 | Pilar 1 — Regulasi & Tata Kelola Pemdi |
| 2 | Aspek 1 — Indikator 2: Manajemen Layanan Digital |
| 3 | Aspek 1 — Indikator 3: Manajemen Keamanan Informasi |
| 4 | Aspek 2 — Indikator 4: Infrastruktur Pemdi |
| 5 | Aspek 2 — Indikator 5: Aplikasi & Layanan Digital |
| 6 | Indikator 6: Berbagi Pakai Data & Informasi Geospasial |
| ... | (modul 7-20 follow same pattern) |

### Noise removal
```python
HEADER_NOISE = [
    r"(?i)^Milik\s*$",
    r"(?i)^Kementerian\s*$", 
    r"(?i)^PANRB\s*$",
    r"(?i)^slide\s*\d+\s*$",
    r"(?i)^halaman\s*\d+\s*$",
]
```

## Build JSON Script

**Path:** `~/Desktop/Niumination/scripts/build-modul-json.py`

Converts cleaned markdown files to `data/modul-indikator.json` — website-ready JSON with pre-rendered HTML. Each module gets `nomor`, `aspek`, `judul`, `ringkasan`, `html`, `gambar`, `file_gambar`.

### Aspek groupings
| Aspek | Indikator |
|-------|-----------|
| Aspek 1 — Tata Kelola | 1, 2, 3 |
| Aspek 2 — Infrastruktur & Layanan | 4, 5, 6, 7, 8, 9, 10 |
| Aspek 3 — Layanan Digital | 11, 12, 13, 17, 18 |
| Aspek 4 — Pendanaan & SDM | 14, 15, 16 |
| Aspek 5 — Proses Bisnis | 19, 20 |

## Website Page

**Path:** `~/Desktop/Niumination/apps/PemdiAcehTengah/pages/modul-indikator.js`

Next.js Pages Router page with:
- Search bar (filters by title/ringkasan)
- Aspek dropdown filter (5 aspek)
- Accordion expand (click to show/hide content)
- Color-coded per-aspek
- Image paths: `/docs/modul-indikator-clean/_images/...` via public symlink
