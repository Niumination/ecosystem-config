# Ecosystem Bulk Cleanup Workflow

**When to use:** User says "cek status ekosistem", "update semua dokumentasi", "bersihkan dirty repos", or any request to audit the entire Niumination ecosystem state and sync documentation across all 30+ repos.

**Contrast:**
- `project-health-check.md` → single project inspection
- `eco-collect-architecture.md` → automated manifest scanner
- **This file** → **manual full-ecosystem audit + cleanup + doc sync**

---

## Phase 0: Initial Status Capture

Run these in parallel to get a complete picture:

```bash
# 1. System-level (macOS)
date
uptime
df -h / /Volumes/HermesAgent

# 2. Overall ecosystem size
du -sh ~/Desktop/Niumination/

# 3. Dirty repos — scan all git dirs
for dir in ~/Desktop/Niumination ~/Desktop/Niumination/Production/* \
  ~/Desktop/Niumination/projects/* ~/Desktop/Niumination/brain; do
  [ -d "$dir/.git" ] || continue
  dirty=$(git -C "$dir" status --short 2>/dev/null | wc -l | tr -d ' ')
  name=$(basename "$dir")
  [ "$dirty" != "0" ] && echo "🔴 $name — $dirty dirty" || echo "✅ $name — clean"
done

# 4. Recent commit activity per project (14-day window)
find ~/Desktop/Niumination -name ".git" -maxdepth 4 -type d | while read gitdir; do
  proj=$(dirname "$gitdir" | xargs basename)
  count=$(git -C "$(dirname "$gitdir")" log --oneline --since="14 days ago" 2>/dev/null | wc -l)
  echo "$proj: $count commits"
done | sort -t: -k2 -rn
```

**Output shape:** A markdown table with all repos ✅/🔴, size overview, and 14-day activity heatmap.

---

## Phase 1: Analyze Dirty Repos

For each dirty repo, classify the changes:

```bash
cd /path/to/dirty/repo
git status --short
git diff --stat          # modified file counts
git diff                 # full diff content — read & understand
```

**Classification by change type:**

| Type | Signal | Action |
|------|--------|--------|
| **Ecosystem docs** | Modified `BACKLOG.md`, `AGENTS.md` | Commit as `chore: update BACKLOG.md & AGENTS.md` |
| **Runtime/generated** | `.DS_Store`, `*.log`, `__pycache__/` | Add to `.gitignore` if not already |
| **Active dev work** | Modified source files (`.js`, `.ts`, `.rs`, `.py`) | Review content, commit with descriptive message |
| **Config** | `.env`, `config/*.yaml`, `secrets` | NEVER commit `.env`. Config files: review, commit if intentional |
| **New untracked** | `?? path/to/file` | Check if intentional (CI workflows, JCode configs, etc.) |
| **Empty/zero-byte** | `file found but empty` | Remove or initialize properly |

**Pitfall:** Some dirty repos have legitimate active development — do NOT force-commit everything. Differentiate between:
- **Stale dirt** (leftovers from last session → commit)
- **Active dirt** (mid-development → leave as-is or ask user)
- **Generated dirt** (DS_Store, logs → gitignore)

---

## Phase 2: BACKLOG.md Sync

Run these BEFORE updating BACKLOG.md to capture current state:

```bash
# Commits since last BACKLOG update (usually ~17th of month)
for dir in ~/Desktop/Niumination/Production/*/ ~/Desktop/Niumination/projects/*/; do
  [ -d "$dir/.git" ] || continue
  name=$(basename "$dir")
  count=$(git -C "$dir" log --oneline --since="2026-07-17" 2>/dev/null | wc -l)
  [ "$count" -gt 0 ] && echo "$name: $count commits"
done

# Dirty repos (for listing in ⚠️ section)
for dir in ~/Desktop/Niumination ~/Desktop/Niumination/Production/* \
  ~/Desktop/Niumination/projects/* ~/Desktop/Niumination/brain; do
  [ -d "$dir/.git" ] || continue
  d=$(git -C "$dir" status --short 2>/dev/null | wc -l | tr -d ' ')
  [ "$d" -gt 0 ] && echo "$(basename $dir) — $d dirty"
done
```

**Update surfaces in BACKLOG.md:**

| # | Section | Update |
|---|---------|--------|
| 1 | Header date & update note | Change "UPDATE: MONTH DD" to today |
| 2 | Scoreboard (tabel kematangan) | Update status, aktivitas 14 hari, priority changes |
| 3 | Aktivitas 14 Hari | Add new section if missing; update commit counts |
| 4 | 🔴 Perubahan Hari Ini | Add entries for today's work |
| 5 | ⚠️ Dirty Repos | Update list with current state |
| 6 | AI ECOSYSTEM | Update model/provider if changed |
| 7 | All Priority promotions | Move P3→P2, P2→P1 when activity warrants |
| 8 | Production/projects counts | Verify against real filesystem |

**Priority promotion rules:**
- 10+ commits in 14 days → consider P3 → P2
- 25+ commits in 14 days → definite P2 candidate
- 0 commits in 30+ days → consider P2 → P3 (stale)
- Active production deployment (Vercel/GH Pages live) → minimum P2

---

## Phase 3: AGENTS.md Sync

Check and update project-specific AGENTS.md files where status or HEAD has changed:

```bash
# Find projects with activity
for dir in ~/Desktop/Niumination/projects/cc-acehtengah ~/Desktop/Niumination/projects/niu-mission-control; do
  [ -d "$dir/.git" ] || continue
  echo "=== $(basename $dir) ==="
  git -C "$dir" log --oneline -3
  head -6 "$dir/AGENTS.md" 2>/dev/null
done
```

**Update triggers:**
- Project had >5 commits → update AGENTS.md HEAD, status, phase info
- Priority changed → update priority badge
- Theme/brand changed → update description
- New features deployed → list in AGENTS.md overview

**Root AGENTS.md updates:**
- Directory tree: update `projects/` listing with new statuses
- Project Catalog table: update Last Push, Status, Description columns
- Total counts in any table headers

---

## Phase 4: Resolve Merge Conflicts

When `git push` is rejected (remote ahead of local):

```bash
# Pull with rebase
git pull --rebase origin main

# If conflict:
# 1. Read the conflict markers
# 2. Resolve manually (pick the right version)
git add <resolved-file>
git rebase --continue

# If HEAD conflicts with remote deletion (BACKLOG.md deleted on remote):
# Check which version is more current, then force-push if needed
git push --force origin main   # ONLY for ecosystem root repo
```

**Conflict resolution rules:**

| Conflict Type | Strategy |
|---------------|----------|
| BACKLOG.md deleted remotely, modified locally | Force push (local is authoritative — just written) |
| AGENTS.md content conflict | Merge both — keep local additions + remote additions |
| config.yaml conflict | Keep local config (it's the running config) + remote header comments |
| Auto-merged code files | Trust the merge, verify with build |

---

## Phase 5: Commit & Push Dirty Repos

Batch-friendly commit patterns:

```bash
# Ecosystem docs
git add -A && git commit -m "chore: update BACKLOG.md & AGENTS.md — sync real filesystem state MMM DD, YYYY"

# Dirty config/docs
git add -A && git commit -m "chore: sync config & docs with latest ecosystem state — MMM DD, YYYY"

# Active dev batch
git add -A && git commit -m "chore: batch <descriptive summary>"

# CI workflow files
git add .github/ && git commit -m "chore: add/update CI workflows"

# Specific files only
git add path/to/file && git commit -m "fix: <description>"
```

**Push order** (by dependency):
1. Project repos first (foundation)
2. Brain vault next (depends on project data)
3. Niumination root last (references everything above)

**When remote is ahead:**
```bash
git pull --rebase origin main
# resolve conflicts → git add → git rebase --continue
git push origin main
```

**When remote is ahead + force-push acceptable:**
```bash
git push origin main --force   # ecosystem root / non-collaborative repos only
```

---

## Phase 6: Sync Memory & Brain

After BACKLOG.md is finalized and dirty repos are pushed:

```bash
# Brain vault daily note
TODAY=$(date +%Y-%m-%d)
cat > ~/Desktop/Niumination/brain/inbox/ecosystem-update-${TODAY}.md << 'EOF'
# Ekosistem Update — $(date '+%d %b %Y')

## Perubahan Besar
- **BACKLOG.md** — Sync real filesystem state
- ...list major updates...

## Status Ekosistem
- Production: N proyek aktif
- projects/: N proyek
- incubator/: N dormant
- Dirty repos: list

## AI Model
- Hermes main: <current-model>
EOF

git -C ~/Desktop/Niumination/brain add -A && \
  git -C ~/Desktop/Niumination/brain commit -m "chore: daily note — ecosystem update $(date +%Y-%m-%d)" && \
  git -C ~/Desktop/Niumination/brain push origin main
```

**Memory update pattern:**
```bash
# Update memory with:
# - Total repo counts (Production, projects, incubator)
# - Most active projects (name + commit count)
# - Priority promotions
# - Current model/provider
```

---

## Phase 7: Final Verification

Confirm everything is clean:

```bash
dirty=0
for dir in ~/Desktop/Niumination ~/Desktop/Niumination/Production/* \
  ~/Desktop/Niumination/projects/* ~/Desktop/Niumination/brain; do
  [ -d "$dir/.git" ] || continue
  d=$(git -C "$dir" status --short 2>/dev/null | wc -l | tr -d ' ')
  [ "$d" -gt 0 ] && dirty=$((dirty+1))
done
echo "$dirty repos still dirty"
```

**Expected outcome:** 0 dirty repos across Production/, projects/, brain.

---

## Pitfalls

- **Do NOT force-push collaborative repos** — Only the Niumination root repo is safe for `--force`. Others like `PemdiAcehTengah`, `cc-acehtengah` have active remote state.
- **DS_Store in untracked repos** — Some projects (e.g. `latticesend`) don't have `.gitignore` yet. Add `.DS_Store` to `.gitignore` — don't commit it.
- **No remote = local-only repo** — Some projects are local-only (e.g. `latticesend`). The commit still fixes the dirty state; just note it has no remote.
- **BACKLOG.md supersedes other docs** — When conflicting date ranges exist between BACKLOG.md, AGENTS.md, and brain notes, BACKLOG.md is the canonical source.
- **Count is wrong? Double-check filesystem** — Root AGENTS.md and BACKLOG.md may show different numbers than reality. Use `find | wc -l` to verify actual git repo count before updating docs.
- **14-day window for activity tracking** — Use `--since="14 days ago"` (semantic) not a hard-coded date. This auto-adjusts.
- **Sesi tengah malam = next calendar day** — If it's past midnight, `date +%Y-%m-%d` gives tomorrow's date. Use yesterday's date for the daily note if the work was a continuation of the previous day's session.
