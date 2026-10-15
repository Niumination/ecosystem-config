# Root Cleanup — 22 Jun 2026

Real session artifact: scanned Niumination root for files not tracked by ecosystem manifest, analyzed, recommended, and executed cleanup with user approval.

## Discovery

eco-collect.py v2 auto-discovery found 30 items (18 git + 12 non-git) but missed 4 standalone files in root:

| File | Size | Date | Type |
|------|------|------|------|
| `MASTERPLAN.md` | 46 KB | 20 Jun | Architecture masterplan v1.3 |
| `REKAP-NIU-DASH.md` | 10 KB | 3 Jun | Stale Niu-Dash snapshot |
| `AGENTS.md.bak` | 20 KB | 21 Jun | Redundant backup |
| `.gitleaks.toml` | 1.3 KB | — | Secret scanner config |

**Root cause:** eco-collect.py only discovers **directories** (checking for `.git` subdirectory or listing top-level dirs). Standalone files in root are invisible. Root Niumination dir itself is not a git repo, so `brain/` is scanned as a git repo but root-level files are never enumerated.

## Analysis

### MASTERPLAN.md (46 KB, 941 lines)
- Architecture masterplan v1.3 — comprehensive but **partly outdated**
- Claimed 28 projects in Tiered System 3×28 → real state: 30 items
- Claimed 8-10 cron jobs → real: 6 Hermes cron + 7 launchd
- Listed 14 script references → only 3 existed (eco-collect.py, kanban-sync.sh, health-checker.sh)
- Roadmap showed Phase 0 in progress → real: Phase 0 complete, Phase 1 partial
- **Action:** Revise → brain/docs/masterplan-ecosystem.md v2.0, then delete original

### REKAP-NIU-DASH.md (10 KB, 208 lines)
- Static snapshot of Niu-Dash project list from 3 Jun 2026
- Listed 76 projects categorized (READY 23, DEVELOPMENT 25, HOLD/IDEA 28)
- Completely stale — current ecosystem has 30 real items
- **Action:** Delete

### AGENTS.md.bak (20 KB, 376 lines)
- Exact copy of active AGENTS.md (DOX Framework v2.1)
- Backup from 21 Jun 23:02 — redundant with live file
- **Action:** Delete

### .gitleaks.toml (1.3 KB)
- Secret scanner configuration for `gitleaks detect`
- Valid standalone — no better home in brain vault
- **Action:** Keep in root

## Execution

1. **Read full MASTERPLAN.md** — 941 lines across 2 read_file calls
2. **Wrote brain/docs/masterplan-ecosystem.md v2.0** — 464 lines, 27 KB
   - Revised header: v2.0 dated 2026-06-22
   - Counts: 30 items (18 git + 12 non-git), not 28
   - Cron: 6 Hermes + 7 launchd, not 8-10
   - Script inventory: 3 existing + 11 missing (honest gap analysis)
   - Prerequisites: 13 items with actual status (not all "done")
   - Roadmap: Phase 0 ✅, Phase 1 ⏳, Phase 2-3 ⏳
   - Added gap analysis per integration layer
3. **Deleted 3 files:** `rm REKAP-NIU-DASH.md AGENTS.md.bak MASTERPLAN.md`
4. **Verified:** `ls -1A *.md *.toml` → AGENTS.md, BACKLOG.md, .gitleaks.toml ✅

## Key Insight

Ecosystem auto-discovery only catches directories. Any standalone file at root level (`.md`, `.toml`, `.bak`, `.yml`) is invisible. For a truly complete inventory, the scan must explicitly enumerate non-directory entries at root level. Consider adding a `root_files` section to eco-manifest.json if tracking becomes important.

## Revised Doc Location

`brain/docs/masterplan-ecosystem.md` — replaces MASTERPLAN.md as the canonical architecture document. Living document, not final.
