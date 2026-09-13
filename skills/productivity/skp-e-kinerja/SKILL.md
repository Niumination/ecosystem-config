---
name: skp-e-kinerja
description: "Generate SKP concept from session data for reporting."
version: "1.0.0"
author: Afrizal Munthe
license: MIT
metadata:
  hermes:
    tags: [skp, e-kinerja, reporting, diskominfo, activity-tracking]
    related_skills: [ai-agency, routines, second-brain]
---

# SKP e-Kinerja Concept Generator

Generate SKP concepts from Hermes session history and Niumination ecosystem activity for Pegawai ASN reporting.

## Overview

Converts raw session data into structured SKP concepts using DOX as source of truth. All activities verified against filesystem evidence, git commits, and log files.

## When to Use

- User requests SKP concept for a period
- User asks to summarize work activities for reporting
- User wants to extract kegiatan from session history
- User needs to categorize activities by domain for eKinerja evaluation

## Workflow

### Step 1: Collect Session History

```bash
session_search(query="kegiatan OR project OR laporan", limit=10, sort="newest")
```

### Step 2: Collect Ecosystem Reports

```bash
ls ~/Desktop/Niumination/docs/reports/*.md | sort
read_file(path="~/Desktop/Niumination/docs/reports/ECOSYSTEM-STATUS-2026-08-30.md")
read_file(path="~/Desktop/Niumination/docs/reports/LAPORAN-EKSEKUSI-2026-08-23.md")
read_file(path="~/Desktop/Niumination/docs/reports/prioritas-urutan-kerja-2026-08-20.md")
```

### Step 3: Extract & Categorize Activities

**Domain categories:**

| Domain | SKP Field |
|--------|-----------|
| Ekosistem AI & Platform | Pengembangan Sistem |
| Audit & Dokumen | Pengawasan & Pelaporan |
| Infrastruktur & Config | Pengelolaan Infrastruktur |
| Skill Bank | Pengembangan Kompetensi |
| Development & Deployment | Implementasi Teknologi |
| Git/DevOps | Manajemen Versi |
| Legal & Governance | Kepatuhan Regulasi |
| Knowledge Management | Pengelolaan Pengetahuan |
| SKP/eKinerja | Pelaksanaan Tugas |
| Frontend | Pengembangan Antarmuka |

### Step 4: Verify Against Evidence

Every activity must have:
- ✅ File DOX or report as evidence
- ✅ Git commit or log as evidence
- ✅ Deployment URL or status as evidence
- ✅ Session or chat log as evidence

If unverified, mark as "Dikumpulkan dari memori — perlu verifikasi ulang."

### Step 5: Generate SKP Concept

```markdown
# KONSEP SKP — [PERIODE]
**Pegawai:** [Nama] (NIP. [NIK])
**Jabatan:** [Jabatan]
**Unit Kerja:** [Unit]
**Periode:** [Bulan] [Tahun]

## 1. Ringkasan Eksekutif

## 2. Kegiatan [Bulan]

## 3. Inovasi & Pengembangan Teknologi

## 4. Rekapitulasi

## 5. Keterangan
```

## Common Pitfalls

1. Include unverified activities — always require evidence
2. Mix domains — each activity belongs to one domain
3. Skip verification step
4. Use generic categories (use domain table above)
5. Forget bukti column
6. Generate SKP without session history

## Verification Checklist

- [ ] Session history queried
- [ ] Ecosystem reports collected
- [ ] Activities categorized by domain
- [ ] Every activity has verifiable evidence
- [ ] No unverified activities included
- [ ] SKP follows output format
- [ ] Domain categories match eKinerja criteria
- [ ] Total kegiatan/inovasi counted
- [ ] Deployment URLs included
- [ ] SKP saved to `docs/reports/`

## Quick Recipe

```bash
session_search(query="kegiatan project laporan", limit=10, sort="newest")
ls ~/Desktop/Niumination/docs/reports/*.md | sort
# Generate SKP concept using workflow above
write_file(path="~/Desktop/Niumination/docs/reports/SKP-KONSEP-[PERIODE].md", content="...")
```

## References

- `references/skp-draft-jul-aug-2026.md` — SKP concept draft (Jul-Aug 2026)
- `references/activity-extraction-rules.md` — Activity extraction & categorization rules
- `references/evidence-standards.md` — Standards for verifiable evidence
- `~/Desktop/Niumination/docs/reports/` — Ecosystem reports (source of truth)
- `~/Desktop/Niumination/labs/eKinerja-AfrizalMunthe/` — eKinerja evidence archive

## Related Skills
- `ai-agency` — Generate laporan otomatis
- `routines` — Routine workflows
- `second-brain` — Second Brain PKM
