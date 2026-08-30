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
- **💬 Telegram Thread Status** — 5 mission-control thread activity, model/provider mapping, last error
- **🔑 Credential Broker** — central AI-API key control plane (scripts/keys.sh): canonical terdefinisi vs tersimpan di Keychain, status migrasi (Phase B HOLD), scan plaintext leak di store lama (~/.hermes/.env, ~/.gemini/.env, ~/.continue/.env, vault/secrets.zsh)
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

## Current-State Addendum (2026-08-30)
From a real `/up-eco` run on macOS, these additional checks and fixes are now part of the standard workflow:

- **SOUL.md style section:** `up-eco` now checks for a `## Gaya jawab` section in `~/.hermes/SOUL.md`. If missing, add a concise 3-5 line section covering: answer style, language default, structure preference.
- **Hermes display config:** Verify `display.compact=true`, `agent.task_completion_guidance=false`, `display.turn_completion_explainer=false`, `display.personality=""`. These suppress verbose Telegram output.
- **`.gitignore` hygiene:** Ensure root `.gitignore` covers runtime/local artifacts: `logs/`, `.vscode/`, `.9router-state.json`, `skills-lock.json`, `.sync-log`, `.git-backup-*/`. Missing entries cause `up-eco` to flag them as unknown folders.
- **Skill sync mismatch:** After `sync-to-agents.sh`, Hermes may show 4 mismatch skills (`hermes-provider-config`, `niu-mission-control-ops`, `simplify-code`, `telegram-router-orchestration`) even when Jcode is clean. This is a known non-fatal divergence; do not block on it.
- **`ROOT: unbound variable` error:** If `scripts/up-eco.sh` ends with `ROOT: unbound variable`, check line ~790 for a shell variable expansion issue. This is a script bug, not an ecosystem bug.
- **Mission Control Skill API:** `HTTP 404` on `/api/*` while dashboard UI returns `HTTP 200` is normal if only the Next.js frontend runs without the FastAPI backend process. Not a failure.

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
