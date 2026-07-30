---
name: up-eco
description: Ecosystem status check & sync workflow. Triggered via Telegram /up-eco command. Checks git status, detects unknown/foreign folders, syncs BACKLOG/docs with filesystem, and recommends actions to align local ecosystem with GitHub.
tags:
  - ecosystem
  - sync
  - git
  - status
  - niumination
last_updated: "2026-07-30"
version: 2.0.0
changes:
  - Added Phase 6: Skill Bank Integrity (frontmatter, INDEX sync, duplicates)
  - Added Phase 7: Skill Sync Status (sync-to-agents.sh, Jcode/Hermes/USB targets)
  - Added Phase 8: Mission Control Dashboard (Skill Monitor API, stale, conflicts, stats)
---

# 🔄 /up-eco — Ecosystem Status & Sync Check

## Trigger
User sends **`/up-eco`** from Telegram (or says "cek ekosistem" / "up-eco").

## Workflow

### Step 1: Run the checker script
```bash
cd /Users/zaryu/Desktop/Niumination && bash scripts/up-eco.sh
```

Output will show:
- **Git status** root ecosystem + profile README
- **Dirty repos** across all sub-repos
- **Unknown/foreign folders** (detected on filesystem but not in BACKLOG.md)
- **BACKLOG sync** (projects referenced but missing from disk)
- **GitHub Pages** health check
- **🧠 Skill Bank Integrity** — SKILL.md count vs INDEX.md, frontmatter validation, duplicate detection
- **🔄 Skill Sync Status** — sync-to-agents.sh last run, Jcode/Hermes/USB divergence
- **🎛️ Mission Control Dashboard** — Skill Monitor API reachable, stale skills, conflicts, usage stats
- **Recommendations list** (numbered)

### Step 2: Interpret results for the user

Report in a clean format:

**Git Status:**
- ✅ / ❌ Root ecosystem (Niumination/ecosystem-config)
- ✅ / ❌ Profile README (Niumination/Niumination)

**Dirty Repos:**
- List repos with uncommitted changes

**Unknown Folders (detected):**
→ Folders found on filesystem that are NOT tracked in BACKLOG.md or AGENTS.md
→ These are likely created by JCode or manual work
→ Recommend: register in BACKLOG.md, categorize into pipeline, create AGENTS.md entry

**Recommendations:**
→ Numbered action items

### Step 3: Detect source of changes

When the script finds unknown/foreign folders, identify:
- **Hermes-made changes** (documented in this conversation)
- **JCode-made changes** (new repos, new folders mentioned in user messages)
- **Manual user changes** (user worked directly on new project folders)

Use session_search if needed to find what was discussed before suggesting.

### Step 4: Offer to execute

After presenting the report, ask the user (if not already instructed):
- "Gas/lanjut?" to execute ALL recommendations
- Or individually approve each action

### Command Rules
- `/up-eco` → run script, report
- `/up-eco --fix` → run script + execute all non-destructive fixes (commit, push, register projects)
- `/up-eco --dry-run` → run script without output colors (for cron/automation)

## Known Categories
```
Pipeline: sandbox💤 → labs🔬 → services/sites/desktop/agents🔧 → apps🏭 → archive📦
```
| Category | Path | Description |
|----------|------|-------------|
| apps/ | production | Deployed & battle-tested |
| services/ | backend | Servers & engines |
| sites/ | frontend | Web applications |
| desktop/ | native | Desktop & mobile apps |
| agents/ | AI | Agents & automation |
| labs/ | experiments | Active research |
| sandbox/ | dormant | Dormant playground projects |

## Registration Template
When adding a new project to BACKLOG.md:
```markdown
| **ProjectName** | `Category/ProjectName/` | Status | Stack | Deploy |
```
