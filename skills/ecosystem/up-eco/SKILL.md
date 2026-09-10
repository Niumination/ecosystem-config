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
  - Added Phase 7: Skill Sync Status (sync-to-agents.sh, Hermes/USB targets)
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
- **🔄 Skill Sync Status** — sync-to-agents.sh last run, Hermes divergence
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

### Step 4: Archive inactive repos (Phase 9d)

When repos are >60 days dormant:
1. Move repo directory to `inactive-2026-09/` at ecosystem root
2. Add as git submodule: `git submodule add --name inactive-<repo> file:///abs/path inactive-2026-09/<repo>`
3. Update `.gitignore`: remove `archive/` if present (blocks submodule tracking)
4. Update `BACKLOG.md`: increment archive count, mark repo as ~~Archived~~
5. Update `AGENTS.md`: directory tree reflects archive move
6. Remove JCode references from the repo's active files if any
7. Commit: `chore: archive <repo> as submodule`

**Why submodules, not git archive:** `archive/` is in `.gitignore` which prevents git tracking. Moving to `inactive-2026-09/` at root allows submodule tracking while preserving the directory structure.

### Step 5: Purge JCode references (Phase 9e)

After archiving, scan ALL active files for stale JCode references:
```bash
grep -r "JCode\|jcode\|Jcode" --include="*.md" --include="*.sh" --include="*.py"   ~/Desktop/Niumination/scripts/ ~/Desktop/Niumination/skills/   ~/Desktop/Niumination/AGENTS.md ~/Desktop/Niumination/BACKLOG.md 2>&1
```

Fix each hit:
- **Scripts**: Replace JCode bridge comments with Niumination ecosystem references
- **Skill SKILL.md**: Remove `~/.jcode/skills` as sync target, replace with `~/.hermes/skills`
- **BACKLOG.md/AGENTS.md**: Remove JCode deprecated rows, update skill counts
- **ekosistem-status.md**: Change `Jcode + Hermes + USB` to `Hermes + USB`
- **trio-watch.sh**: Keep `jcode_status()` as a documented compatibility wrapper returning static zero state

**Pitfall**: `skills/ecosystem/*` SKILL.md files themselves contain JCode references — these MUST be updated too, not just scripts and root docs.

**Why purge**: Stale JCode references confuse future sessions into thinking JCode is still an active sync target, causing wasted effort on `--verify-target ~/.jcode/skills`.

### Step 6: Offer to execute

After presenting the report, ask the user (if not already instructed):
- "Gas/lanjut?" to execute ALL recommendations
- Or individually approve each action

### Command Rules
- `/up-eco` → run script, report
- `/up-eco --fix` → run script + execute all non-destructive fixes (commit, push, register projects)
- `/up-eco --dry-run` → run script without output colors (for cron/automation)

## Current-State Addendum (2026-09-10)
From a real `/up-eco` run on macOS, these additional checks and fixes are now part of the standard workflow:

- **SOUL.md style section:** `up-eco` now checks for a `## Gaya jawab` section in `~/.hermes/SOUL.md`. If missing, add a concise 3-5 line section covering: answer style, language default, structure preference.
- **Hermes display config:** Verify `display.compact=true`, `agent.task_completion_guidance=false`, `display.turn_completion_explainer=false`, `display.personality=""`. These suppress verbose Telegram output.
- **SOUL/dotfiles drift check:** `up-eco` compares SHA-256 of `~/.hermes/SOUL.md` vs `dotfiles/zaryu-terminal-dotfiles/hermes/SOUL.md`. If they differ, or if the symlink target is missing, report a drift incident and recommend repair before any session restart.
- **`.gitignore` hygiene:** Ensure root `.gitignore` covers runtime/local artifacts: `logs/`, `.vscode/`, `.9router-state.json`, `skills-lock.json`, `.sync-log`, `.git-backup-*/`. Missing entries cause `up-eco` to flag them as unknown folders.
- **Skill sync mismatch:** After `sync-to-agents.sh`, Hermes may show mismatch skills even when target is clean. Known non-fatal divergence; do not block on it.
- **Mission Control v3.0 (Next.js-only):** Legacy `server.py` (FastAPI port 5200) DELETED. Modern MC = `services/niu-mission-control/apex-ui/` (Next.js 15 + React 19). Dev: `npm run dev` (port 3000). Production: `npm run build && npm start`. `HTTP 404` on `/api/*` while UI returns `HTTP 200` is NORMAL — Next.js frontend only, no FastAPI backend. Not a failure.
- **`ROOT: unbound variable` error:** If `scripts/up-eco.sh` ends with `ROOT: unbound variable`, check line ~790 for a shell variable expansion issue. This is a script bug, not an ecosystem bug.

## MC Architecture Transition (2026-09-10)
**Legacy (deleted):** `services/niu-mission-control/server.py` (FastAPI port 5200)
**Current (v3.0):** `services/niu-mission-control/apex-ui/` (Next.js 15 + React 19, port 3000 dev)
- `build_unified.py` → generates `index.html` single-file dashboard
- `server.py` at root is legacy snapshot only (`legacy-ui` branch)
- Health check: `curl -s http://localhost:3000/` → HTTP 200
- Do NOT reference port 5200 as active — it was removed

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
| inactive-2026-09/ | archived | Dormant repos as git submodules |

## Registration Template
When adding a new project to BACKLOG.md:
```markdown
| **ProjectName** | `Category/ProjectName/` | Status | Stack | Deploy |
```
