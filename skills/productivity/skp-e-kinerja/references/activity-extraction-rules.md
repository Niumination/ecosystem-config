# Activity Extraction & Categorization Rules

## Purpose
Rules for extracting work activities from Hermes session data and Niumination ecosystem reports for SKP (Surat Keterangan Pelaksanaan) concepts.

## Source Data

### Hermes Session History
- Path: `~/.hermes/state.db` (SQLite, FTS5)
- Messages: 19,720+ messages
- Sessions: 24 sessions recorded
- Query: `session_search(query="kegiatan OR project OR laporan", limit=10, sort="newest")`

### Ecosystem Reports
- Path: `~/Desktop/Niumination/docs/reports/*.md`
- Count: 28+ report files
- Key files:
  - `ECOSYSTEM-STATUS-2026-08-30.md`
  - `LAPORAN-EKSEKUSI-2026-08-23.md`
  - `audit-pekerjaan-breakdown-2026-08-20.md`
  - `laporan-perubahan-2026-08-20.md`
  - `prioritas-urutan-kerja-2026-08-20.md`

### Git Log
- Command: `git log --oneline --since="2026-07-01" --until="2026-09-01"`
- Provides: commit dates, messages, authors

### Deployment Evidence
- Vercel: `vercel --version`, deployment URLs
- GitHub Pages: `https://niumination.github.io/`
- Mission Control: `curl -s http://localhost:5200/api/health`

## Extraction Rules

### Rule 1: Verify Activity Date
- Extract date from session timestamp or report header
- Map to correct month (July or August 2026)
- Use Unix timestamps for precise date filtering:
  - July 2026: 1751328000 - 1754006400
  - August 2026: 1754006400 - 1756771200

### Rule 2: Categorize by Domain
- Use the 10 domain categories defined in SKP skill body
- Each activity = exactly one domain
- Don't double-count across domains

### Rule 3: Extract Evidence
- File path: `~/Desktop/Niumination/docs/reports/FILENAME.md`
- Git commit: hash + message
- Deployment URL: verify with curl
- Session data: timestamp + content snippet

### Rule 4: Classify Activity Type
- **Kegiatan Teknis:** Technical implementation, deployment, audit
- **Inovasi & Pengembangan Teknologi:** New tools, methods, architectures
- **Dokumentasi:** Reports, DOX updates, documentation
- **Pemeliharaan:** Maintenance, cleanup, config updates

### Rule 5: Skip Non-Work Activities
- Personal exploration without deliverables
- Failed experiments without follow-up
- Routine chat without technical output

## Categorization Decision Tree

```
Is the activity technical implementation?
  → Yes: Development & Deployment or Ekosistem AI & Platform
  → No: Is it audit/review?
    → Yes: Audit & Dokumen
    → No: Is it infrastructure/config?
      → Yes: Infrastruktur & Config
      → No: Is it documentation/writing?
        → Yes: Dokumentasi
        → No: Is it skill development?
          → Yes: Skill Bank
          → No: Is it legal/governance?
            → Yes: Legal & Governance
            → No: Frontend or Knowledge Management
```

## Anti-Patterns

- Don't include activities without evidence
- Don't mix domains
- Don't skip verification
- Don't forget bukti column
- Don't rely on memory alone — always query session history