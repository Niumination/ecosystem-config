---
name: kanban-ecosystem-management
description: "Track Niumination project portfolio via Hermes kanban. Covers: mapping AGENTS.md project catalog → kanban tasks by category/priority, syncing BACKLOG.md, fixing empty-dashboard DB_PATH issues, and the Plan→DOX→Execute workflow for ecosystem-wide kanban updates."
tags: [kanban, project-management, portfolio, hermes, ecosystem-tracking]
related_skills: [ecosystem-state-sync, portfolio-data-maintenance, plan-compliance-audit]
---

# Kanban Ecosystem Management

Manage the **Niumination Ecosystem** kanban board — a project portfolio tracker containing all 66+ repos and 25 local folders across 7 categories.

## ⚠️ Pitfall: Root AGENTS.md Sering Terlewat dari Commit

**Masalah:** Saat melakukan reorganisasi root repo (`ecosystem-config`), file `AGENTS.md` dan `BACKLOG.md` di root sering tidak ikut di-commit karena fokus ke subdirektori. Ini menyebabkan state root repo tidak sinkron dengan realita — laporan versi tidak update.

**Penyebab:** File-file ini ada di root direktori yang sama dengan `.git/` tetapi tidak terlihat saat bekerja di subdirektori (`Production/`, `projects/`, dll).

**Solusi — Checklist Wajib Sebelum Selesai:**

```bash
cd /Users/zaryu/Desktop/Niumination
# 1. Cek SEMUA perubahan — jangan cuma subdirektori
git status

# 2. Pastikan AGENTS.md dan BACKLOG.md ikut di-stage
git add AGENTS.md BACKLOG.md   # jika ada perubahan

# 3. Commit dengan pesan yang mencakup update dokumentasi
git commit -m "docs: update AGENTS.md vX.X — [deskripsi perubahan]"
git push
```

**Verifikasi:** Setelah push, selalu cek bahwa commit terakhir menyertakan AGENTS.md:
```bash
git log --oneline -1 --name-only
```

## Quick Ecosystem Health Check

Fast diagnostic — use when the user says **"cek status ekosistem proyek"** / "check ecosystem status" / any ad-hoc health query. Does NOT involve kanban task ops.

Supports **three topologies**: 
1. **Local-filesystem workspace** (Desktop/Niumination with Production/, projects/, incubator/, brain/) 
2. **GitHub-org remote** (most repos on GitHub, few local clones)
3. **Root-git workspace** (same as #1 but Desktop/Niumination itself is a git repo tracking AGENTS.md, BACKLOG.md, and submodule references)

Detect which one by checking the current filesystem layout and the presence of `.git` at root.

### Topology detection

```
if /Users/zaryu/Desktop/Niumination exists with Production/ projects/ brain/ → Local workspace topology
  if /Users/zaryu/Desktop/Niumination/.git exists → Root-git workspace (ecosystem-config repo)
else if only /Volumes/Mac Win/PemdiAcehTengah/ has .git → GitHub-org topology
```

### What to report (both topologies)

Return a compact summary:
- **Total repos** — from GitHub org API count OR local filesystem count
- **Active repos (pushed ≤2 weeks)** — repos with recent activity
- **Local clones & dirty state** — which repos are cloned locally + uncommitted changes
- **Kanban projects** — project-level tasks from the Hermes kanban DB
- **Unpushed commits** — repos with `git log @{u}..HEAD`
- **Recent commits (last 2 days)** — per-repo summary of recently committed work; critical when user mentions jcode, Claude Code, or other AI coding tools since those changes are already committed+ pushed and won't appear in dirty/unpushed checks
- **Ponytail exclusion** — note it was skipped if relevant

⚠️ **Pitfall — dirty-only report misses committed work.** If the user says they've been fixing projects with jcode (or any AI coding tool), the changes are likely already committed and pushed. A `git status --short` check alone will report everything as clean — falsely implying nothing changed. Always also check `git log --since="2 days ago"` for recent commits when the user signals active work.

### Pattern A — Local workspace (Desktop/Niumination)

```bash
cd /Users/zaryu/Desktop/Niumination

# Production repos
for d in Production/*/; do
  [ -d "$d/.git" ] && echo "### $(basename "$d"): $(cd "$d" && git status -sb)"
done

# Project repos (excluding ponytail)
for d in projects/*/; do
  name=$(basename "$d")
  [ "$name" = "ponytail" ] && echo "### ponytail (Skipped)" && continue
  [ -d "$d/.git" ] && echo "### $name: $(cd "$d" && git status -sb)"
done

# Brain (separate due to expected log noise)
cd brain && git status -sb

# Recent commits (last 2 days)
echo ""
echo "=== RECENT COMMITS (last 2 days) ==="
for d in Production/*/ projects/*/; do
  [ ! -d "$d/.git" ] && continue
  n=$(basename "$d")
  [ "$n" = "ponytail" ] && continue
  c=$(git -C "$d" log --oneline --since="2 days ago" 2>/dev/null)
  [ -n "$c" ] && echo "### $n:" && echo "$c"
done
echo "=== brain ==="
git -C brain log --oneline --since="2 days ago" 2>/dev/null
```

### Pattern B — GitHub-org topology (repos remote, few local clones)

Use when the ecosystem is primarily GitHub-based with sparse local clones. Run these three parallel scans:

**1. GitHub org inventory** — list all repos via GitHub API:
```
gh search repos --owner Niumination --json name,description,updatedAt,pushedAt,defaultBranch
```
Or via MCP: `mcp_github_search_repositories(query="org:Niumination")`

Then filter: **active** (pushed ≤2 weeks) vs **stale** (pushed >1 month).

**2. Local clones** — scan all volumes for Niumination git repos:
```bash
for vol in /Volumes/*/; do
  find "$vol" -maxdepth 4 -name ".git" -type d 2>/dev/null | while read gitdir; do
    repo=$(dirname "$gitdir")
    remote=$(cd "$repo" && git remote -v 2>/dev/null | grep fetch | head -1)
    if echo "$remote" | grep -q "Niumination"; then
      branch=$(cd "$repo" && git branch --show-current 2>/dev/null)
      changes=$(cd "$repo" && git status --short 2>/dev/null | wc -l | tr -d ' ')
      echo "$repo | $branch | ${changes} perubahan"
    fi
  done
done
```

**3. Kanban project tasks** — read from Hermes SQLite kanban DB:
```sql
SELECT id, title, status FROM tasks ORDER BY created_at DESC LIMIT 30;
```

**4. Compose compact report:**

```
🌐 EKOSISTEM NIUMINATION — STATUS

📦 GitHub: {N} repositori total

🟢 Aktif (push ≤2 minggu):
  {repo1} — {desc} — {last push}
  {repo2} — {desc} — {last push}

🟡 Stale / One-shot (push >1 bulan):
  {repo5}, {repo6}, ...

💻 Local Clone
  {repoX} — {path} — {N perubahan uncommitted}

📋 Kanban Projects
  {task1} — {status}
  {task2} — {status}
```

This pattern is faster than reading `eco-collect.py` state or the full kanban API — it reads filesystem state directly and uses the GitHub API for remote inventory.

### Common readings

| Signal | Meaning |
|--------|---------|
| All repos show `## main...origin/main` with no other lines | Everything clean and synced |
| `brain` has `M docs/` `?? inbox/` `?? logs/` | **Expected** — daily auto-log noise. NOT actionable for the user. Note it but don't flag as a problem |
| `projects/X-kebab` shows `?? node_modules/` or `dist/` | Expected — build artifacts; check .gitignore |
| `tools/ponytail` dirty | Expected — excluded from ecosystem. Skip in report |
| Any repo behind/diverged from remote | **Actionable** — flag for the user |

### When to escalate to full workflow

If the quick check finds dirty repos the user didn't expect, OR if the user says "update semua ke github" after the check, switch to the **[Batch Push All Dirty Repos](#batch-push-all-dirty-repos--workflow)** workflow below.

## Workflow: Plan → DOX → Execute

**This is the ONLY valid sequence for ecosystem updates.** Never skip steps.

### Step 1: Read Current State

Before touching anything:

```bash
# Read kanban stats
hermes kanban stats
hermes kanban boards list

# Read DOX
cat BACKLOG.md | head -20   # Audit master + scoreboard
cat AGENTS.md | head -40    # Project catalog summary

# Read kanban list
hermes kanban list
```

Cross-reference: kanban tasks ↔ AGENTS.md project list. Identify gaps.

**Project health check reference:** `references/project-health-check.md` — standard checklist for git + deploy + package integrity inspection.

### Single-Commit Layout Rollback Pattern

When applying visual/structure changes to an ecosystem page (like niu-dash index.html), use the **single-commit pattern** so the change is easy to revert:

**Workflow:**
1. Make all changes to **one file** (typically `index.html`)
2. Keep the diff lean — prefer targeted `patch()` calls over rewriting entire sections
3. Commit once with a descriptive subject line
4. Verify the GH Pages deploy went green

**Why:**
- `git revert <hash>` undoes the entire layout change in one command
- No complex merge conflict resolution needed
- User can easily roll back if the layout doesn't match expectations

**Example commit message:**
```
layout: <short description> — <key changes comma-separated>
```

**User preference:** "sekali commit dan push, agar tidak banyak perubahan dan bisa sekali rollback jika tidak sesuai" — do NOT stage multiple commits for a single visual change.

### Step 2: Plan (get approval)

Present to user:
- Category breakdown (Government, Web Apps, AI, TEDEO, Dotfiles, Knowledge, Lain)
- Priority distribution (P1=🔴 urgent bugs, P2=🟡 active, P3=🟢 monitoring)
- Task counts per category
- Any structural decisions (archive vs ready vs scheduled)

**Do NOT skip approval.** The user must sign off on the plan before execution.

### Step 3: Documentation Sync — 4-Surface Update

When the user says "tandai proyek selesai", "update backlog/dokumentasi/dox/brain", or any project state change is committed, **sync all 4 surfaces** simultaneously:

| # | Surface | File / Tool | What to update |
|---|---------|------------|----------------|
| 1 | **Master Backlog** | `BACKLOG.md` | Scoreboard counts, project status row, version bump, audit section, last-verified date |
| 2 | **Root DOX (Project Catalog)** | `AGENTS.md` | Bump DOX version, update project status/version/audit-column, kanban status line |
| 3 | **Brain Vault** | `brain/inbox/<topic>-<YYYY-MM-DD>.md` | Summary note of what changed, key decisions, any open questions |
| 4 | **Memory Checkpoint** | `memory()` tool | Save durable facts so next session starts from current state |

**Sequence matters:**
1. Execute the actual work (fix bugs, update data, commit code)
2. Update BACKLOG.md with what actually changed
3. Update AGENTS.md (bump DOX version, sync project row)
4. Create brain/inbox note with summary + decisions + open questions
5. Update memory with durable facts (version, HEAD, completion status)

**Do not skip any surface.** The user expects all 4 to be consistent. A stale memory while BACKLOG is updated will cause contradictory claims in the next session.

Update AGENTS.md + BACKLOG.md **before** creating kanban tasks (when applicable):

- `AGENTS.md` — bump DOX version, update kanban status line
- `BACKLOG.md` — update audit master date, scoreboard, kanban section

### Step 4: Create Kanban Tasks

Use `hermes kanban create` with integer priorities:

```bash
hermes kanban create --priority 1 --body "Description with status and deploy URL." "Project Name"
hermes kanban create --priority 2 --body "..." "Project Name"
hermes kanban create --priority 3 --body "..." "Project Name"
```

- **P1 (priority=1)**: Active critical bugs (kune-ya.com, TEDEO)
- **P2 (priority=2)**: Active/maintained projects (PemdiAcehTengah, LKH, niu-vermilion, etc.)
- **P3 (priority=3)**: Monitoring/registry (stale projects, dotfiles forks, knowledge vaults)

**Batch strategy**: Create tasks by category in groups (Government → AI → Web Apps → TEDEO → Dotfiles → Knowledge → Other). Use parallel terminal calls where possible.

### Step 5: Update BACKLOG.md Post-Creation

After all tasks exist, patch BACKLOG.md:
- Replace kanban system section with new stats
- Update scoreboard with new counts
- Update last-verified line

### Step 6: Verify Dashboard

The dashboard reads from a **kanban.db** file. Common failure: the dashboard reads from the wrong DB.

```bash
# Check which DB the dashboard is using (server.js line 9)
grep DB_PATH server.js

# Compare with actual kanban.db locations:
ls -la /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db   # OpenCode profile (CURRENT)
ls -la ~/.hermes/kanban.db                                   # Default profile (STALE)

# Test the API
curl -s http://127.0.0.1:5199/api/tasks | python3 -c "import sys,json; print(f'{len(json.load(sys.stdin))} tasks')"
```

If the dashboard shows empty (0 tasks) but `hermes kanban stats` shows tasks:
1. The DB_PATH in `server.js` points to the wrong database
2. Fix: update `DB_PATH = process.env.KANBAN_DB || '/actual/path/to/kanban.db'`
3. Kill old server, restart with new path
4. Refresh browser

## Kanban DB locations (opencode profile)

| Instance | DB Path |
|----------|---------|
| **OpenCode profile (CURRENT)** | `/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db` |
| **Default profile (STALE)** | `~/.hermes/kanban.db` |
| **Dashboard default** | Must match OpenCode's DB — edit `server.js` line 9 if wrong |

## Task Creation Parameters

| Flag | Value | Notes |
|------|-------|-------|
| `--priority` | Integer 1-4 | P1=1 (critical), P2=2 (active), P3=3 (monitoring) — NOT strings like "P1" |
| `--body` | String | Description with status emoji, deploy URL, last commit info |
| Title | Positional arg | Required, must NOT contain shell-special chars that break command |

### Finding the Active Kanban DB

The kanban dashboard server uses a configurable DB path. When it's read-only or shows stale data, find the actual DB:

1. **Check server.js** for the DB path:
   ```bash
   grep -E 'DB_PATH|KANBAN_DB' /path/to/niu-kanban-dash/server.js
   # Typically: const DB_PATH = process.env.KANBAN_DB || '/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db';
   ```

2. **The active DB is set via `KANBAN_DB` env var**, often pointing to the USB path:
   ```
   /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db  ← OpenCode profile (ACTIVE)
   ~/.hermes/kanban.db                                   ← Default profile (STALE)
   ```

3. **Verify by counting tasks directly:**
   ```sqlite3
   sqlite3 /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db "SELECT COUNT(*) FROM tasks;"
   ```

### Kanban API is Read-Only

The kanban Express server at port 5199 only serves **GET routes** (`/api/tasks`, `/api/stats`, `/api/ecosystem`). POST/PUT requests return 404 or HTML. Task status updates **must go directly to the SQLite DB** — they cannot be done through the API.

### Fallback: Direct sqlite3 Insert (Bash)

When `hermes kanban create` is unavailable (e.g., MCP sqlite tools in read-only mode), create tasks via direct `sqlite3` insert into the kanban DB:

```bash
# Find the active kanban DB
DB="/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db"

# Generate a unique task ID (kebab-case from title)
TASK_ID="kanban-$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9_' '-' | sed 's/^-//;s/-$//')"

# Insert — generate a random-ish priority order if needed
sqlite3 "$DB" "INSERT INTO tasks (id, title, description, status, priority, priority_order, created_at, updated_at)
  VALUES ('$TASK_ID', '$TITLE', '$DESC', 'pending', $PRIORITY, $(date +%s), '$(date -u +"%Y-%m-%dT%H:%M:%SZ")', '$(date -u +"%Y-%m-%dT%H:%M:%SZ")');"

# Verify
sqlite3 "$DB" "SELECT id, title, status, priority FROM tasks ORDER BY created_at DESC LIMIT 5;"
```

**Note:** Title/description must not contain single quotes. Escape or filter them with `sed "s/'/''/g"`.

This is a maintenance workaround only — prefer `hermes kanban create` for normal operations.

### Fallback: Direct sqlite3 Update (Python) — Preferred for Existing Tasks

For **updating existing tasks** (changing status, adding results), Python sqlite3 is more robust than bash since it handles quoting automatically and supports richer workflows:

```python
import sqlite3, time

db = "/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db"
conn = sqlite3.connect(db)

# Check task first
t = conn.execute("SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)).fetchone()
print("Before:", t)

# Update status + result
now = int(time.time())
conn.execute(
    "UPDATE tasks SET status = ?, completed_at = ?, result = ? WHERE id = ?",
    ('done', now, 'MATURE ✅ — Butuh VPS untuk production deployment.', task_id)
)
conn.commit()

# Verify
t2 = conn.execute("SELECT id, title, status, result FROM tasks WHERE id = ?", (task_id,)).fetchone()
print("After:", t2)

# Read kanban stats
stats = conn.execute("SELECT status, COUNT(*) as c FROM tasks GROUP BY status").fetchall()
print("Stats:", stats)

conn.close()
```

**Why Python over bash:**
- No shell escaping issues — task titles with special characters work naturally
- Complex workflows (check-then-update, batch operations) are trivial
- `SELECT` before `UPDATE` to verify the task exists and see current state
- Parameterized queries (`?` placeholders) prevent SQL injection from task content

Use this when: updating kanban task status after marking a project as done/mature/completed.

## Backlog-Driven Kanban Sync (Automated Cron)

A `no_agent=true` cron job that parses `BACKLOG.md` and syncs tasks into the kanban SQLite DB. The script runs every hour, reading the parseable format and upserting into the `tasks` table.

### BACKLOG.md Parseable Format

For the cron to consume tasks, BACKLOG.md MUST use this exact format:

```
- [STATUS] **Title** — Description — @project-tag
```

| Component | Rule |
|-----------|------|
| `STATUS` | ` ` (todo), `o` (in_progress), `x` (done) |
| `**Title**` | Task name in bold — maximum one bold segment per line |
| `— Description` | Short description after the em-dash |
| `@project-tag` | Lowercase kebab-case project identifier — last `@tag` on the line wins |

Example:
```
- [o] **TEDEO T1** — JWT fallback for expired tokens — @tedeo
- [x] **Niu-LKH v3.1.1** — Released, 100% done — @niu-lkh
- [ ] **Feature X** — Planning phase — @some-project
```

The parser (`sed` + `grep`) extracts:
- Status character from `[...]`
- Bold title from `**...**` (falls back to the text after the status marker)
- Project tag from the trailing `@tagname`
- Description from the text between `—` and `@`

### The Kanban-Sync Script (`scripts/kanban-sync.sh`)

The script lives in the project root (`/Users/zaryu/Desktop/Niumination/scripts/`). ~~The profile copy is what cron invokes~~ — **update 5 Agu:** cron tidak lagi menjalankan script ini (tidak terjadwal).

Key techniques:

**Task ID generation:**
```bash
task_id="backlog-$(echo "$title" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9_' '-')-${project}"
```

**Upsert pattern:**
```bash
existing=$(sqlite3 "$DB" "SELECT id FROM tasks WHERE id='$task_id'")
if [ -z "$existing" ]; then
  sqlite3 "$DB" "INSERT INTO tasks (...) VALUES (...)"
else
  sqlite3 "$DB" "UPDATE tasks SET ... WHERE id='$task_id'"
fi
```

**Status mapping:** `[ ]`→`todo`, `[o]`→`in_progress`, `[x]`→`done`

### Script Safety — `mkdir` Lock Pattern

Every `no_agent=true` cron script MUST use mkdir-based locking to prevent concurrent runs (cron can fire a new tick before the previous run finishes):

```bash
LOCKDIR="/tmp/<script-name>.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ Lock exists — another run in progress"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT
```

**Why `mkdir` over `flock`:** Portable across macOS, Linux, WSL. No PID file management. Atomic on all Unix. Works even when `/tmp` is on a different filesystem.

### Cron Registration (no_agent script)

```bash
hermes cronjob action=create \
  schedule="every 1h" \
  name="kanban-backlog-sync" \
  no_agent=true \
  script="kanban-sync.sh" \
  workdir="/Users/zaryu/Desktop/Niumination" \
  deliver="local"
```

**Rules for no_agent cron:**
1. Script must be in the profile's scripts dir: `/Volumes/HermesAgent/HermesAgentUSB/data/profiles/opencode/scripts/`
2. `script` field takes JUST the filename — NOT an absolute or relative path
3. Copy/move the script there: `cp scripts/kanban-sync.sh /Volumes/HermesAgent/HermesAgentUSB/data/profiles/opencode/scripts/`
4. Always set `workdir` to the project root so relative paths work
5. `deliver=local` keeps output off the user's feed (silent watchdog pattern)
6. If the script produces stdout that the user should see during dev, test it with `bash scripts/kanban-sync.sh` first, then register the cron

### Divergence Detection (in kanban-sync.sh)

The cron script includes automatic divergence detection that flags inconsistencies between BACKLOG.md and the actual filesystem:

**What it checks:**
1. **Orphaned @tags** — BACKLOG.md references a `@project-tag` whose mapped directory doesn't exist on the filesystem
2. **Unregistered git repos** — A directory has `.git` but no matching `@project-tag` appears in BACKLOG.md

**How it works:**
- Script maps tags → directory names via a `case` statement with directory-name normalization
- Remote-only repos (no local directory expected) are filtered via a `continue` list in the `case` block — prevents false-positive alerts
- Findings are logged to `brain/logs/divergence-<YYYYMMDD>.log` with an ISO timestamp
- The script silently exits (exit 0, no stdout) when no divergence is found

**Extending the tag→dir mapping:**
```bash
case "$tag" in
  # Local dirs (should exist on filesystem)
  tedeo) dir_name="TEDEO" ;;
  niu-dash) dir_name="projects/niu-dash" ;;
  # Remote-only repos — skip (no local dir expected):
  kms-spbe|niu-startpage) continue ;;
esac
```

When adding a new project to BACKLOG.md, register its tag→dir mapping in the case block. When a remote-only repo already has tasks in BACKLOG, add its tag to the skip list.

**Expected noise: @tag mismatches from `projects/` subdirectory projects** — The divergence check maps @tags to directory names at root level (e.g. `@tedeo` → `TEDEO/`). Projects that live under `projects/` (like `projects/niu-cast`, `projects/TEDEO`) will NOT match when the script scans root — producing false-positive "no directory found" entries in the divergence log every hour. These are pre-existing and NOT actionable. Fix: extend the tag→dir case block to include the full subdirectory path (e.g. `tedeo) dir_name="projects/TEDEO" ;;`). Until the mapping is updated, ignore these entries as routine noise.

**Why temp files instead of variables:** The detection loop uses `grep | while-read` which runs in a subshell. Shell variables set inside the pipe are lost to the parent. The script uses `mktemp` to write divergence state to a temp file, which the parent reads after the pipe exits:

```bash
DIVERGE_FILE=$(mktemp /tmp/kanban-diverge.XXXXXX)
echo "0" > "$DIVERGE_FILE"
grep ... | while read tag; do
  if [ ! -d "$dir" ]; then echo "1" > "$DIVERGE_FILE"; fi
done
diverged=$(cat "$DIVERGE_FILE")
rm -f "$DIVERGE_FILE"
```

## Ecosystem Monitoring Cron Scripts

> 📌 **Update 5 Agu 2026:** Semua cron monitoring script ini **TIDAK LAGI dijadwalkan**. Launchd agents `com.niumation.*` dihapus, Hermes cron dirampingkan jadi `memory-checkpoint` saja. Script tetap tersedia di `scripts/` (path sudah diupdate ke struktur baru) — siap dipasang ulang jika dibutuhkan. Scheduler aktif sekarang: `memory-checkpoint` (Hermes cron, 6h) + `sync-to-agents.sh` (crontab macOS, 6h) + 2 GitHub Actions.

### Script Inventory

| # | Script | Schedule (lama) | Delivery | Status (5 Agu) |
|---|--------|----------|----------|---------|
| 1 | `kanban-sync.sh` | every 1h | local | 🟡 Ada, path diupdate, tidak terjadwal |
| 2 | `health-checker.sh` | every 6h | local | 🟡 Ada, path diupdate, tidak terjadwal |
| 3 | `remote-poller.sh` | every 6h | telegram | 🟡 Ada, path diupdate, tidak terjadwal |
| 4 | `daily-heartbeat.sh` | 08:00 daily | telegram | 🟡 Ada, path diupdate, tidak terjadwal |
| 5 | `changelog-writer.sh` | 20:00 daily | local | 🟡 Ada, path diupdate, tidak terjadwal |
| 6 | `gitleaks-weekly.sh` | Sun 08:00 | local | ❌ Dihapus 5 Agu (CPU 721%) |
| 7 | `eco-collect.py` | 15m (cron) + 30m (launchd) | telegram (cron) / local (launchd) | 🟡 Ada, auto-discover 39 repos, tidak terjadwal |

### Silent Watchdog Delivery Pattern

Scripts that should only message the user when something is wrong **exit 0 with empty stdout**. The `no_agent=true` cron engine skips delivery when stdout is empty:

```bash
# Remote poller: silent when all clean
[ "$HAS_CHANGES" -eq 0 ] && exit 0  # No output → no Telegram message
echo "⚠️ Changes detected:"  # Only reaches Telegram when there's news
```

### health-checker.sh
Checks three surfaces:
- **Disk usage** — warning if `>80%`
- **Git dirty repos** — walks the Tier 1 project list for uncommitted changes
- **Deploy health** — HTTP status code check on GH Pages and Vercel endpoints

### remote-poller.sh
Does `git fetch --timeout=10` on each Tier 1 repo with a 10-second timeout per fetch to avoid hanging on unreachable remotes. Silently exits on all-clean. Emits warnings on:
- Branches behind their remote
- Fetch failures (timeout, no route to host)

### daily-heartbeat.sh
Delivers a morning digest to Telegram at 08:00 WIB:
- Active task count from BACKLOG.md
- Dirty repo count
- Number of active cron jobs
- Random project highlight

### changelog-writer.sh
Appends a daily stats snapshot to `brain/docs/ecosystem-changelog.md` at 20:00:
- Total / done / active / pending task counts parsed from BACKLOG.md
- Number of dirty git repos
- Active cron job count

### gitleaks-weekly.sh
Runs `gitleaks detect -v` on every git repo in the ecosystem. Reports findings grouped by severity level. Designed to be quiet on clean runs (no leaks = no output).

### eco-collect.py — Auto-Discovery Ecosystem State Collector

The ecosystem state collector replaces hardcoded path lists with **auto-discovery** — scanning the filesystem for `.git` directories and listing non-git directories dynamically. This prevents staleness when the user moves or adds projects.

**Architecture:**
- **Collector** (`scripts/eco-collect.py`): Python script that discovers all items and compares against a saved state file
- **State file** (`brain/logs/eco-manifest.json`): Persistent JSON that survives reboot, records the last-known-good manifest
- **NO_CHANGES guard**: When the filesystem matches the saved state, the script outputs `NO_CHANGES` (exit 0) — the cron LLM sees this and skips processing (zero cost)
- **Dual scheduling**:
  - Hermes cron `ecosystem-auto-sync` (every 15m): collector → LLM agent → potential manifest patch
  - Launchd `com.niumination.eco-collect` (every 30min, RunAtLoad): collector in `--save` mode, silently updates state file

**Output modes:**
| Mode | Command | Behavior |
|------|---------|----------|
| Normal | `python3 scripts/eco-collect.py` | Compares vs state file → `NO_CHANGES` or full manifest |
| Force | `python3 scripts/eco-collect.py --force` | Always rebuilds manifest, updates state file |
| Save | `python3 scripts/eco-collect.py --save` | Silent update without stdout (launchd mode) |

**Auto-discovery technique:**
The script scans Niumination root dirs AND `projects/` subdirectory AND `incubator/` AND `Production/`:
```python
def auto_discover_git_repos(root):
    git_repos = {}
    scan_dirs = []  # Start with root-level dirs
    # Level 1: root-level dirs
    for item in os.listdir(root):
        git_dir = os.path.join(root, item, '.git')
        if os.path.isdir(git_dir):
            git_repos[item] = os.path.join(root, item)
    # Level 2: inside projects/
    projects_dir = os.path.join(root, 'projects')
    if os.path.isdir(projects_dir):
        for item in os.listdir(projects_dir):
            git_dir = os.path.join(projects_dir, item, '.git')
            if os.path.isdir(git_dir):
                git_repos[item] = os.path.join(projects_dir, item)
    # Level 3: inside incubator/
    incubator_dir = os.path.join(root, 'incubator')
    if os.path.isdir(incubator_dir):
        for item in os.listdir(incubator_dir):
            git_dir = os.path.join(incubator_dir, item, '.git')
            if os.path.isdir(git_dir):
                git_repos[item] = os.path.join(incubator_dir, item)
    # Level 4: inside Production/ (each sub-repo)
    scan_dirs += sorted(Path(root, "Production").glob("*"))
    for item_path in scan_dirs:
        item = item_path.name
        git_dir = os.path.join(item_path, '.git')
        if os.path.isdir(git_dir) and item not in git_repos:
            git_repos[item] = str(item_path)
    return git_repos
```

Non-git dirs are discovered by listing root + projects/ + incubator/ directories and filtering out anything with a `.git` subdirectory.

**Key design decisions:**
1. `brain/` is itself a git repo — scanned at root level, included in git repos count
2. `scripts/` is a non-git collection — tracked under non-git section
3. Root Niumination dir is NOT a git repo — skipped (it contains sub-repos)
4. State file lives at `brain/logs/eco-manifest.json` — follows brain vault conventions
5. Empty `--save` run on launchd means the state file is always warm

**Pitfall — eco-collect.py needs executable permission after editing:** After creating or editing `scripts/eco-collect.py`, the file may lose its executable bit (especially if written via `write_file` or `patch`). This causes `Permission denied` when cron or launchd tries to run it. Always verify: `ls -l scripts/eco-collect.py | grep 'x'` and fix with `chmod +x scripts/eco-collect.py` if the `x` bits are absent. This is a routine deployment step after any edit to the script.

**Reference:** `references/eco-collect-architecture.md` for full architecture, source code patterns, and state file format.

### Ecosystem Page (Niu-Dash index.html)

The ecosystem view is a **built-in view** in `index.html` via `window.renderEcosystem()` / `showEcosystem()`, accessed by clicking **Ecosystem** in the sidebar. No separate page needed.

### Architecture
- **Data source:** `KANBAN_API_URL=http://localhost:5199/api/ecosystem` (kanban Express server)
- **Fallback:** When API unreachable, builds data from local `flatProjects` array (already loaded in the page) — no external fallback URL needed
- **Header count:** Dynamic from `ecosystemData.projects.length` — NOT hardcoded
- **Status:** Shows count + "synced" when data loaded, "loading..." initially, count alone when fallback active
- **Kanban Dashboard (React):** `http://127.0.0.1:5199` → click **Ecosystem** in nav

### Render flow
1. `showEcosystem()` calls `renderEcosystem()` 
2. First render: shows loading state, calls `fetchEcosystemData()`
3. `fetchEcosystemData()` tries Kanban API → if fails, builds from `flatProjects` locally
4. Second render: shows data with real project count

### Pitfall — Hardcoded counts
Always show real dynamic counts from loaded data. If a static number like "30 projects" appears in the header while the list is empty, the render is showing a placeholder before/after data loads — or the fallback produced empty results. Fix: use `data.projects.length` when loaded, "—" while loading.

### Pitfall — Fallback URL must exist
The old fallback fetched `https://raw.githubusercontent.com/Niumination/Niumination/refs/heads/main/BACKLOG.md` which is a 404 — the `Niumination/Niumination` repo doesn't exist. Always verify fallback URLs return valid data before shipping. Better approach: use already-loaded local data (like `flatProjects`) instead of network fallbacks.

### Access (Legacy standalone page)
- **Old standalone:** `file:///Users/zaryu/Desktop/Niumination/projects/niu-dash/ecosystem.html` (may not exist in recent versions)
- **Deployed:** `https://niumination.github.io/niu-dash/` → Ecosystem in sidebar

### Auto-Date/Stats Pattern for Static Pages

When maintaining static `.html` files (like `ecosystem.html`) that display ecosystem data from a hardcoded project array, replace hardcoded dates and counts with JS-generated dynamic values to prevent staleness:

**Pattern — auto-date:**
```js
// Replace "Diperbarui 27 Jun 2026" with:
document.querySelector('.subtitle-class').textContent = 
  'Diperbarui ' + new Date().toLocaleDateString('id-ID', {day:'numeric', month:'short', year:'numeric'});
```

**Pattern — auto-stats from array:**
```js
// Derive counts from the existing project array instead of hardcoding
const ready = projects.filter(p => p.status === 'ready').length;
const dev = projects.filter(p => p.status === 'dev').length;
// ...then update DOM with these computed values
```

**When to apply:** Any time you touch a static ecosystem page that has a "last updated" date or manually counted stats. If the data array exists in the same file (inline JS), always compute stats from it rather than hardcoding numbers.

### React Ecosystem Page (Kanban Dashboard)

The Kanban Dashboard at `projects/niu-kanban-dash/` has a React ecosystem page accessed via the **Ecosystem** tab in the header nav. It's an alternative to the standalone Vanilla HTML page.

**Architecture:**
- Backend: `server.js` → `GET /api/ecosystem` scans the filesystem and returns project list + kanban stats + phase status
- Frontend: `src/components/EcosystemPage.jsx` renders the data
- Integration: App.jsx uses a 3-way view switch (`board` | `ecosystem` | `stats`) via `view` state
- **Project scan is dual-depth**: root Niumination dir + `projects/` subdirectory — captures all 28-30 projects

**Git HEAD reading trick (no `git` subprocess):**
Instead of shelling out to `git rev-parse HEAD`, the endpoint reads `.git/HEAD` directly:
```js
const gitLog = readFileSync('.git/HEAD', 'utf-8').trim();
if (gitLog.startsWith('ref: refs/')) {
  const refPath = '.git/' + gitLog.split(' ')[1];
  commitMsg = readFileSync(refPath, 'utf-8').trim().substring(0, 12);
} else {
  commitMsg = gitLog.substring(0, 12); // detached HEAD
}
```
This is faster and has zero subprocess overhead — important for a synchronous API call.

**Safe Vite build command:**
`npx vite build` can trigger the tool's background-detection false-positive. Use the direct binary instead:
```bash
node ./node_modules/vite/bin/vite.js build
```
Then kill and restart the Express server (port 5199) to pick up the new `dist/`.

**Adding a view to the Kanban Dashboard:**
1. Create component in `src/components/`
2. Add API endpoint in `server.js` (if needed)
3. Import component in `App.jsx`, add `view === 'newView' ? <Component /> : ...` in main render
4. Add nav button in `Header.jsx` view toggle
5. Rebuild: `node ./node_modules/vite/bin/vite.js build`
6. Restart server

**API endpoint `GET /api/ecosystem`** returns:
```json
{
  "projects": [{
    "name", "tier", "hasGit", "hasDox", "hasBacklog", "hasReadme", "gitHead", "isEmpty",
    "priority": "P1|P2|P3",          // derived from tier
    "git": "github.com/Niumination/...", // null if no git
    "dox": true|false,
    "cron": true|false,
    "status": "pending|active|completed",
    "desc": "",
    "deployUrl": "https://..."          // null if unknown
  }],
  "phases": [{"id", "name", "total", "done"}],
  "tasks": {"byStatus": [{"status", "count"}], "total": N, "byPriority": [{"priority", "count"}]},
  "git": 20,        // count of git repos
  "dox": 12,        // count of projects with DOX
  "crons": 9,       // count of cron jobs
  "tasks": 107,     // total kanban tasks
  "cronCount": 9,
  "summary": {"totalProjects", "gitRepos", "withDox", "withBacklog", "emptyDirs"}
}
```

**EcosystemPage.jsx sections:**
1. Summary cards (total projects, git repos, DOX count, cron count, kanban tasks)
2. Phase completion bars (auto-calculated percentage, gradient fill)
3. Kanban task breakdown (color-coded status pills + priority pills)
4. Project registry table with filter toggle (All / Git / No Git / No DOX / Empty)

**Pitfall — Kanban server must be running for API:** The ecosystem view relies on `localhost:5199`. This is now handled by launchd agent `com.niumination.kanban-server` (auto-starts at login, restarts on crash). To check: `curl -s http://localhost:5199/api/ecosystem | head -1`. If down: `launchctl load ~/Library/LaunchAgents/com.niumination.kanban-server.plist`.

### Post-Push Verification

After pushing a new feature or fix to GH Pages, the user expects you to verify nothing broke. Do NOT wait for them to ask:

1. **Check the server is still running** — Kanban API must be live (port 5199)
2. **Test the API response format** — Use `curl` to check the raw response shape matches what the frontend expects. Don't assume it does.
3. **Verify JS syntax** — Run `node -e` with `new Function()` on all `<script>` blocks to catch syntax errors before reload
4. **Check CSS variable existence** — If the new feature uses custom CSS vars (e.g. `--text-muted`, `--neon-purple`), confirm they're defined in `:root`
5. **Check for no-event-handler gaps** — If sidebar has a `data-action` or `case 'show-X'` switch, confirm the new action is handled
6. **Report findings** — Tell the user what's clean and what needs fixing. If the feature works but the data is incomplete (schema mismatch), that's a fix, not a pass.

**Schema mismatch is the most common post-push defect.** It produces no errors — just silently wrong display. Always verify the actual API output against the frontend's expectations.

## Batch Push All Dirty Repos — Workflow

When the user says **"update semua ke github"** / "update all to github" / "push semuanya", execute this sequence. Do NOT skip steps.

### Step 1: Inventory — Find every dirty repo

```bash
for d in $(find /Users/zaryu/Desktop/Niumination -name ".git" -type d -maxdepth 5 \
  -not -path "*/plugins/*" -not -path "*/backup/*" -exec dirname {} \; | sort); do
  name=$(echo $d | sed 's|/Users/zaryu/Desktop/Niumination/||')
  dirty=$(cd "$d" && git status --porcelain 2>/dev/null)
  if [ -n "$dirty" ]; then
    echo "=== $name ==="
    echo "$dirty"
  fi
done
```

Also check for **unpushed commits** (committed but not pushed):

```bash
for d in $(find /Users/zaryu/Desktop/Niumination -name ".git" -type d -maxdepth 5 \
  -not -path "*/plugins/*" -not -path "*/backup/*" -exec dirname {} \; | sort); do
  name=$(echo $d | sed 's|/Users/zaryu/Desktop/Niumination/||')
  unpushed=$(cd "$d" && git log --oneline @{u}..HEAD 2>/dev/null)
  if [ -n "$unpushed" ]; then
    echo "=== $name ==="
    echo "$unpushed"
  fi
done
```

**Distinguish dirty files vs unpushed commits:**
| Signal | Meaning | Action |
|--------|---------|--------|
| `git status --porcelain` shows files | Uncommitted changes | `git add` + `git commit` + `push` |
| `git log @{u}..HEAD` shows commits | Committed but not pushed | `git push` only |
| Both | Mix of committed+unpushed + dirty | Commit dirty first, then push all |
| Neither | Clean | Skip |

Important: `git status -sb` `ahead` only shows committed-but-not-pushed. A missing ahead with dirty files means files are uncommitted — you still need to commit before push.

### Step 2: Apply Exclusion Filter

Before committing **anything**, check the **Ecosystem GitHub Push Exclusions** section below. **Skip all excluded projects entirely** — no branches, no pushes, no remote modifications.

Quick exclusion check:
```bash
list=("ponytail" "other-excluded-project")  # Add known exclusions
for name in "${list[@]}"; do
  # Remove from dirty list
done
```

### ⚠️ Step 3 — Commit ALL untracked + modified files — do NOT filter by assumption

When the user says **"update semua perubahan"** / **"push semuanya"** — they mean EVERY file in EVERY dirty repo. Do NOT skip untracked files because you think they're "WIP" or "not ready for GitHub." That judgment belongs to the user, not the agent. If you're unsure whether to commit something, ask — do not silently exclude.

**Real example (13 Jul 2026):** mac-web-dashboard had 3 modified files plus untracked new features (hexstrike/, AIWorksuite with 12 components, agents API). Committing only modified files triggered "kenapa mac-web-dashboard di lewati?" — the user expected ALL changes pushed. The untracked files were not WIP; they were ready for GitHub.

**What gets skipped (and ONLY these):**
1. Projects in the **Ecosystem GitHub Push Exclusions** list (ponytail)
2. Files that match `.gitignore` patterns (venv/, __pycache__, *.pyc, *.log, .DS_Store, node_modules/, .next/, etc.)
3. Nested git repos (submodules) — unstage via `git rm -r --cached`, don't include their `.git/` directory. Source files inside the submodule are tracked by its own remote.
4. Garbage artifacts (site-packages, multi-MB logs) — but update `.gitignore` first, then stage the rest.

**Workflow when a dirty repo has source files mixed with garbage:**
1. Check existing `.gitignore`
2. Add patterns for garbage (e.g. `venv/`, `hexstrike/*.log`, `__pycache__/`)
3. Stage ALL remaining untracked + modified files via explicit `git add <file1> <file2> ...`
4. Commit + push

### Step 4: Commit Each Dirty Repo With Context-Appropriate Message

Read the diff first to understand what changed:

```bash
git diff --stat  # File-level summary  
git diff | head -40  # First 40 lines of detail
```

Use matching commit type based on the diff:

| Diff content | Commit type | Example |
|-------------|-------------|---------|
| Operational logs, inbox notes, daily updates | `chore:` | `chore: daily ecosystem update 2026-07-09 — inbox + divergence logs` |
| Feature addition, new UI component | `feat:` | `feat: add lokal-only counter to dashboard stat cards` |
| Config/infra fix (.gitignore, CI) | `chore:` | `chore: add .DS_Store to .gitignore` |
| Data file update (JSON, ecosystem status) | `update:` | `update: ecosystem-status.json — 9 Jul 2026, 24 projects` |

**Commit pattern:** `git add <file1> <file2> ...` (explicit, not `-A`) → `git commit -m "type: description"` → `git push origin main`

For **.DS_Store** only — do NOT commit it. Add to `.gitignore` instead:
```bash
echo ".DS_Store" >> .gitignore && git add .gitignore && git commit -m "chore: add .DS_Store to .gitignore" && git push
```

### Step 5 — Regenerate Ecosystem Manifest

```bash
cd /Users/zaryu/Desktop/Niumination && python3 scripts/eco-collect.py --force
```

### Step 6 — Update DOX Counts

Four updates in the root AGENTS.md and BACKLOG.md:

| Doc | Update | Detail |
|-----|--------|--------|
| **AGENTS.md** footer | `Diperbarui:` line | Bump version (v2.x), date + summary of what was pushed |
| **AGENTS.md** catalog | Project status row | Date, status, version if changed |
| **BACKLOG.md** header | Filesystem Audit line | Bump git count if new repo, date |
| **BACKLOG.md** scoreboard | `Git + Remote (proj)` row | Bump count, add new project to example list |

### Step 7 — Verify No Leftover Dirty Repos

Re-run the Step 1 inventory scan. Report the final state. Only projects in the exclusion list (ponytail) should remain dirty.

### Step 8 — Fix Cron Script Dependencies (if applicable)

After batch-push, check if any cron jobs were erroring. Common issue: brain-capture.py (or any cron script) is missing from the USB scripts directory:

```bash
ls /Volumes/HermesAgent/HermesAgentUSB/data/scripts/<script-name>.py 2>/dev/null || echo "MISSING"
```

If missing, find the actual location and copy it:

```bash
find /Users/zaryu/Desktop/Niumination -name "<script-name>.py" 2>/dev/null
cp <found-location> /Volumes/HermesAgent/HermesAgentUSB/data/scripts/<script-name>.py
```

**Pitfall — brain-capture.py location is `Production/niu-dash/data/scripts/`** (not `brain/` or `scripts/`). After copying, test the script runs cleanly:
```bash
python3 /Volumes/HermesAgent/HermesAgentUSB/data/scripts/brain-capture.py
```

### Step 9 — Check for Stale Launchd Plists (if ecosystem-wide cron migration occurred)

After migrating from launchd one-shot services to Hermes cron, some plists may remain registered but orphaned (file deleted from disk). Detect:

```bash
for job in com.niumation.eco-collect com.niumation.gitleaks-weekly com.niumation.kanban-sync com.niumation.brain-daily-capture com.niumation.health-checker com.niumation.changelog-writer; do
  plist="$HOME/Library/LaunchAgents/${job}.plist"
  [ -f "$plist" ] && echo "ACTIVE: $job" || echo "STALE: $job — plist missing, service still loaded"
done
```

Stale entries show as `- 78` or `- 0` in `launchctl list` but have no plist. They're harmless — launchd keeps the job definition in memory until next boot. If cleanup is desired, run `launchctl bootout gui/$(id -u)/<label>` per job, or just ignore them.

### Pitfalls

- **DOX root is a git repo now** — AGENTS.md, BACKLOG.md, .gitleaks.toml, and .gitignore are tracked in `github.com/Niumination/ecosystem-config` (private). Commit changes via `cd /Users/zaryu/Desktop/Niumination && git add -A && git commit -m "msg" && git push origin main`. A `.gitignore` exists that excludes PI/ (secrets), .DS_Store, node_modules, build artifacts, and archive binary dirs.
- **"No remote" claims in BACKLOG.md may be stale** — Always verify `git remote -v` before accepting a "no remote" claim in BACKLOG.md. Projects may have had remotes pushed since the last doc sync. Trust the filesystem, not the doc, for remote status.
- **Order matters: commit → push → eco JSON → DOX** — Don't update DOX counts before the actual pushes finish. The DOX update "freezes" the state after the pushes are confirmed.
- **Commit message granularity** — One commit per repo, not one commit for all repos. Use `-m` with short descriptions. Keep `git log` clean.
- **Skipping ponytail is a permanent user directive** — Check `tools/ponytail` in the dirty list every time. If it's dirty, do NOT touch it. Document in your response that you skipped it.

### Ecosystem GitHub Push Exclusions ⛔

Some projects in the ecosystem should NOT be included in ecosystem-wide batch pushes to GitHub — they are kept local-only by user preference.

**Current exclusion list:**

| Project | Reason | Source |
|---------|--------|--------|
| ponytail | User directive: "abaikan ponytail dari update ekosistem ini ke github" — kept local, never pushed to GitHub | Memory + explicit instruction 29 Jun 2026 |

**Rules:**
1. When performing any ecosystem-wide GitHub operation (pushing ecosystem-status.json, regenerating GH Pages data, batch-committing across repos), **skip all excluded projects entirely** — no PRs, no branches, no pushes, no remote modifications for those projects.
2. The list is maintained in **memory** AND this section. When updating one, update the other.
3. If the user later says "include X in ecosystem pushes" for a previously excluded project, remove it from this list AND the corresponding memory entry.
4. The exclusion applies to the ecosystem push workflow only — local development, commits, and workspace maintenance are unaffected.
5. When a new project is added to the ecosystem and the user gives a specific instruction about its GitHub treatment (push or don't push), record it here immediately.

**Why not just memory:** Memory captures the fact (ponytail excluded); this section captures the workflow pattern so any future agent performing ecosystem pushes knows to check for exclusions without rediscovering the rule by violating the user's preference.
## GitHub Repo Setup for New Projects

After a project has been identified as worth pushing to GitHub (no remote, or local-only git), use the `gh` CLI to create the remote repo and push. Three patterns apply depending on the project's git state:

#### Pattern A: Existing git repo (has commits, needs remote)

```bash
cd /path/to/project
gh repo create Niumination/<repo-name> --private --source=. --push --remote=origin
```

This:
- Creates the repo on GitHub (`Niumination/<repo-name>`)
- Sets `origin` as the remote
- Pushes the current branch

**Best for:** niumination-workspace (had 4 commits), TEDEO (migrated from different remote)

#### Pattern B: New project (no git yet)

```bash
cd /path/to/project

# Init git
git init
git checkout -b main

# Create .gitignore for the stack
cat > .gitignore << 'EOF'
node_modules/
dist/
.env
*.log
.DS_Store
EOF

# First commit
git add -A
git commit -m "init: initial project scaffold"

# Create remote + push
gh repo create Niumination/<repo-name> --private --source=. --push --remote=origin
```

**Best for:** niu-kanban-dash, orchestrator, Ultra (no prior git history)

#### Pattern C: Root ecosystem repo (Niumination root with submodules)

When the target directory contains sub-git-repos (e.g., Production/*, projects/*, brain/ all have their own `.git/`):

```bash
cd /Users/zaryu/Desktop/Niumination

# Create .gitignore FIRST — critical! This directory contains PI/ and secrets
cat > .gitignore << 'GITIGNORE'
# macOS
.DS_Store
._*
# Secrets
PI/
credentials-backup.zip
*.env
# Build
node_modules/
dist/
*.zip
__pycache__/
# Archive binary dirs
archive/Belum disentuh/
archive/backup/
archive/labs/
GITIGNORE

# Initialize git repo
git init
git checkout -b main
git add -A
git commit -m "init: root ecosystem config & tracking"
gh repo create Niumination/ecosystem-config --private --source=. --push --remote=origin
```

The resulting repo tracks:
- Root files (AGENTS.md, BACKLOG.md, .gitignore, .gitleaks.toml)
- Submodule references (gitlinks) for every top-level subdir with its own `.git/`
- Archive .md files (text only — binary dirs excluded via .gitignore)

`git status` will show `m <path>` for submodule directories — this is expected, not a dirty repo. The `m` means the submodule's HEAD doesn't match the root repo's recorded gitlink.

**Best for:** Niumination ecosystem root, project catalogs, documentation surfaces.

#### Verification

After push, verify the remote is set and the repo exists:

```bash
git remote -v              # Should show origin → github.com/Niumination/<repo>
gh repo view Niumination/<repo-name>  # Should show repo details
```

#### DOX Sync After Push

Every new GitHub push requires updating 2 DOX surfaces:

| Surface | What to update |
|---------|---------------|
| **AGENTS.md** | Tree entry (add `✅ github.com/...`), catalog table row (add URL), timeline/Eksekusi Selanjutnya |
| **BACKLOG.md** | Task marker `[ ]` → `[x]`, scoreboard (Git + Remote → ✅), summary stats (Git + Remote count +1, No Git count -1) |

Then run the ecosystem pipeline to sync the manifest:

```bash
# Step 1: Update NON_GIT_DIRS if needed
# Step 2: Refresh manifest
python3 scripts/eco-collect.py --force
```

### Pitfall — Pre-commit hook warnings on `gh repo create`

When creating a GitHub repo via `gh repo create --push`, the local repo's pre-commit hooks fire during `gh`'s internal push. Some hooks (like `[ : 0\n0 : integer expression expected`) are cosmetic — they indicate the hook script had a minor shell evaluation issue but the push succeeded. Verify by checking `git push` succeeded despite the warning. As long as `git remote -v` shows the remote and `gh repo view` works, the push is fine.

### Pitfall — Naming consistency between local dir and GitHub repo

For consistency, the GitHub repo name should match the local directory name or the project's canonical name (lowercase kebab-case). Examples:

| Local dir | GitHub repo | Rationale |
|-----------|------------|-----------|
| `Ultra/` | `ultra-automation` | Project name is "Ultra Automation" |
| `projects/orchestrator/` | `orchestrator` | Matches dir name |
| `projects/niu-kanban-dash/` | `niu-kanban-dash` | Matches dir name |

If they differ (like `Ultra/` → `ultra-automation`), add a note in AGENTS.md explaining the mapping.

### Updating project data

Edit the `projects` array in the `<script>` section. Each entry:
```js
{name: 'Project Name', desc: 'Description', tier: 1, stack: ['Tag1','Tag2'], status: 'in_progress', gh: 'Niumination/repo'}
```

### Status values
| Status | Badge color | Meaning |
|--------|-------------|---------|
| `done` | Green (#22c55e) | 100% complete |
| `in_progress` | Amber (#f59e0b) | Active work |
| `pending` | Gray (#6b7280) | Not started |
| `active` / `live` | Green | Deployed and running |
| `stale` | Red (#ef4444) | Abandoned |

## Reference Files

| File | When to Use |
|------|------------|
| `references/db-corruption-recovery.md` | Kanban DB returns "invalid SQLite header" or dashboard shows 0 tasks — detection + recovery steps |
| `references/alternative-pm-tools.md` | User asks for project management alternatives outside Hermes kanban (Linear, Airtable, Notion, Obsidian, Niu-Dash rebuild) |
| `references/project-health-check.md` | Standard git + deploy + package integrity checklist |
| `references/dashboard-dbpath-debug.md` | Dashboard reads from wrong DB_PATH — debug steps |
| File | When to Use |
|------|-------------|
| `references/frontend-backend-data-contract.md` | Debugging schema mismatch between frontend feature expectations and backend API response — bidirectional fix pattern with real Ecosystem View example |
| `references/eco-collect-architecture.md` | Ecosystem state collector architecture: auto-discovery logic, state file format, dual-scheduling strategy, and cost-efficient NO_CHANGES guard |
| `references/root-cleanup-2026-06-22.md` | Real session artifact: scanned root for unregistered files (MASTERPLAN.md, REKAP-NIU-DASH.md, AGENTS.md.bak), analyzed, got approval, executed cleanup — full walkthrough of the inventory cleanup workflow |
| `references/ecosystem-dashboard-json.md` | `generate-ecosystem-json.py` pipeline: output format, migration history (sh->py), path pitfall (projects/ vs Production/), regeneration workflow after GitHub pushes |
| `references/brain-capture-location.md` | brain-capture.py script location (Production/niu-dash/data/scripts/), copy-to-USB fix for cron, verification steps |
| `references/notebooklm-ecosystem-docs.md` | Using NotebookLM as an AI-augmented documentation surface: notebook creation, source selection heuristics, CLI tips, known limitations |
| `references/government-api-audit.md` | Probing CRUDBooster/Laravel government APIs — platform ID, auth probe matrix, IP restriction diagnosis, API Generator workflow, custom get-token Bearer flow, error decoding |
| `references/third-party-integration-assessment.md` | Evaluating external tools/platforms for ecosystem fit — research framework, integration mapping, Observer AI example, PLUS blueprint documentation workflow for creating structured integration docs |
| `references/government-api-audit.md` | Probing CRUDBooster/Laravel government APIs — platform identification, auth probe matrix, diagnosing IP restriction, data schema discovery |

## Pitfalls

- **`--priority` takes an integer**, not "P1" / "P2" — pass `--priority 1`, not `--priority P1`
- **Title with special chars** (`—`, `&`, `|`, `(`, `)`) breaks shell parsing in terminal — use simple titles or wrap in double quotes
- **Dashboard empty ≠ kanban empty** — check DB_PATH in server.js, the dashboard reads from a hardcoded path
- **DOX before tasks** — always update AGENTS.md/BACKLOG.md first, then create tasks, then update BACKLOG.md again with final numbers
- **Kanban stats before/after** — run `hermes kanban stats` before and after creation to confirm changes took effect
- **Gateway safety** — never run `hermes gateway` commands from the opencode profile. It can trigger a second gateway instance and disconnect Telegram. Use readonly commands only (`hermes config`, `hermes kanban list`, `hermes profile get`).
- **Subshell variable loss in divergence detection** — The `grep | while-read` pipe runs in a subshell. Variables set inside the pipe (`diverged=1`) are lost to the parent. Always use a `mktemp` file to communicate divergence state across the pipe boundary.
- **Cron script must be in profile scripts dir** — `script="kanban-sync.sh"` (filename only). The actual file must be at `/Volumes/HermesAgent/HermesAgentUSB/data/profiles/opencode/scripts/kanban-sync.sh`. Always `cp` after editing the canonical copy in the project root.
- **`no_agent=true` scripts with deliver=telegram** — Empty stdout = no delivery. Use `exit 0` with no output for silent watchdog. Non-empty stdout always triggers delivery. Design scripts so they only emit output when there's something worth reporting.
- **Ecosystem page data source — multiple layers:** The ecosystem view fetches from Kanban API (port 5199). If API is unreachable, falls back to local `flatProjects` data. After adding/removing a project, either restart the Kanban server or refresh the page so `flatProjects` is current.
- **Kanban server auto-start via launchd:** A launchd agent `com.niumination.kanban-server` handles auto-start at login (`RunAtLoad=true`) with `KeepAlive=true`. The plist is at `~/Library/LaunchAgents/com.niumination.kanban-server.plist`. The server runs `node /Users/zaryu/Desktop/Niumination/projects/niu-kanban-dash/server.js`. After a Vite rebuild, kill the server (`lsof -ti:5199 | xargs kill -9`) and launchd restarts it automatically. To prevent launchd from restarting during maintenance: `launchctl unload ~/Library/LaunchAgents/com.niumination.kanban-server.plist`, do maintenance, then `launchctl load ...`.
- **Frontend-backend schema mismatch is SILENT** — A new frontend feature fetching from an API may display wrong tier colors, missing tags, or empty stats without any JS error.
- **Shared-remote repos cause non-fast-forward push failures** — When two local directories point to the same GitHub remote (e.g., `x-downloader/` primary and `x-downloader-backup/` both with `origin → github.com:Niumination/x-downloader.git`), committing in the backup and trying to push will fail with `Updates were rejected because the remote contains work that you do not have locally`. This happens because the primary repo's pushes have already moved the remote HEAD forward. Detection: check `git remote -v` on both repos and notice identical URLs. Fix: determine which is the canonical repo (primary). If the backup commit introduces files the primary already has (e.g., analysis docs), the backup commit is redundant — rebase or reset to drop it. If the backup commit has genuinely new content, cherry-pick it into the primary repo. To recover a commit lost during `git pull --rebase`: `git reflog` → find the lost SHA → `git cherry-pick <hash>`.

## Auto-Discovery Pattern (Filesystem Scanning)

When maintaining a project manifest or ecosystem index, **prefer auto-discovery over hardcoded lists**. Hardcoded lists silently become stale when the user moves directories (e.g., `TEDEO/` → `projects/TEDEO/`) or adds new projects. Auto-discovery is trivial (one `os.listdir` + `os.path.isdir` check) and eliminates an entire class of staleness bugs.

**Two-level scan pattern:** Most Niumination ecosystems have both root-level and `projects/` subdirectory-level items. Scan both:
```python
def scan_two_levels(root):
    items = {}
    for level in ['', 'projects/']:
        target = os.path.join(root, level)
        if not os.path.isdir(target):
            continue
        for item in os.listdir(target):
            full_path = os.path.join(target, item)
            if not os.path.isdir(full_path) or item.startswith('.'):
                continue
            items[item] = full_path
    return items
```

**Change detection with state file:** Write the discovered manifest to a JSON file (convention: `brain/logs/eco-manifest.json`). On next run, read it back and compare. If identical, skip LLM processing (cost savings). The state file serves as both cache and persistent record.

**Cost design: NO_CHANGES guard pattern**
```
Python collector (mechanical, zero-token cost)
  → compares vs state file
  → if NO_CHANGES: exit 0, short stdout
  → if CHANGES: emit full manifest JSON for LLM processing
```
The LLM only runs when there's actually something to update. For a check-every-15m cron, this reduces token spend from ~$0.013/run to ~$0.0004/run — ~97% savings.

**Dual scheduling pattern:** Same script, two schedules with different purposes:
- **Hermes cron** (short interval, LLM-driven): collector stdout feeds into agent → agent decides whether to patch manifest
- **Launchd** (longer interval, silent `--save`): keeps the state file warm even when no cron runs

### Pitfall — `NON_GIT_DIRS` must be maintained when non-git projects gain git repos

The `eco-collect.py` script has a `NON_GIT_DIRS` list (hardcoded exceptions) that skips auto-discovery on directories that should remain in the non-git list despite possibly having `.git` (e.g., `Production/`, `scripts/`). But when a **previously-non-git project** gains a git repo and gets pushed to GitHub, it must be **removed from `NON_GIT_DIRS`** — otherwise the collector skips it and it stays in the non-git count even though it now has a remote.

**Checklist after pushing a new repo:**

1. Check if the project name appears in `NON_GIT_DIRS` in `scripts/eco-collect.py`
2. If yes, remove it from the list
3. Run `python3 scripts/eco-collect.py --force` to refresh the manifest
4. Regenerate ecosystem-status.json
5. Commit + push to brain/ and Production/niu-dash/

**Common items that have been removed from NON_GIT_DIRS (historical):** niu-kanban-dash, orchestrator, Ultra

### Cron Agent: Processing Manifest Output

When the ecosystem auto-sync cron fires and the pre-run collector has output, the agent receives `CHANGED ITEMS` (delta) and a full `FULL MANIFEST` JSON. Follow this workflow:

**Pre-flight — LOCK_EXISTS / LOCKED state:**
If the pre-run collector output is `LOCK_EXISTS` or `LOCKED`, the collector's `mkdir`-based lockfile was held by another instance (overlapping cron or launchd still running). This is NOT an error — re-run the collector manually: `python3 scripts/eco-collect.py`. The lock auto-releases when the holding process exits. If a stale lock from a crashed instance blocks the run, verify no process is active (`pgrep -f eco-collect.py`), then clean up: `rm -rf /tmp/eco-collect.lock && python3 scripts/eco-collect.py`. Always produce fresh data from an agent-side re-run — do NOT report stale state from a failed collection.

**Step 1: Verify every changed item against the actual filesystem**

The manifest is a pre-collected snapshot — it can be stale or transient. Always cross-check:

```bash
git -C <path> status --short          # Confirm dirty flag
git -C <path> rev-parse --short HEAD  # Confirm commit hash
git -C <path> log -1 --format="%h %s %ai"  # Confirm timestamps
ls <path>/.git 2>/dev/null            # Confirm it's actually a git repo
```

Common findings:
| Manifest claim | Filesystem reality | Cause |
|----------------|-------------------|-------|
| `dirty: true` | `clean — nothing to commit` | Transient — e.g. fresh clone resolved the delta |
| `dirty: true` | Clean but untracked files excluded | `.gitignore` or checkout race |
| `brain dirty: true` | Uncommitted operational logs in `docs/` or `logs/` | **Expected** — cron scripts (divergence, issue-bridge, eco-manifest, changelog) write to brain/ automatically. These are transient log artifacts, NOT actionable changes. Do NOT commit them unless specifically asked. |
| Path exists | Path doesn't exist | Stale entry in state file (deleted dir) |
| HEAD `abc1234` | HEAD `def5678` | Repo was re-cloned between collection and processing |
| `Missing repo: projects/X` | Found at Production/X/ | Intentional move — pre-run only scans projects/ + root |

**"Missing repo" in Production/:** When CHANGED ITEMS lists `Missing repo: projects/<name>`, check Production/ immediately — `ls -d Production/<name> 2>/dev/null`. If found at Production/, this is an intentional relocation, not data loss. Document the verified move in your patch summary. Do NOT mark it as deleted.

When the dirty flag resolves to clean on verification, the delta is transient — **do not patch docs for it** unless a doc explicitly recorded the dirty state.

**Step 1.5: Detect renames — "Missing repo" paired with "Added repo" is a likely rename, not a deletion**

When CHANGED ITEMS shows both `- Missing repo: projects/old-name` and `+ Added repo: projects/new-name`, treat this as a potential rename first, not a deletion+addition. Check the new directory's identity-bearing files to confirm:

```bash
# Check package.json (JS/TS projects)
grep '"name"' projects/new-name/package.json 2>/dev/null
# Check Cargo.toml (Rust projects)
grep '^name =' projects/new-name/Cargo.toml 2>/dev/null
# Check setup.py/pyproject.toml (Python)
grep 'name=' projects/new-name/setup.py 2>/dev/null
```

If the identity file still carries the OLD name (e.g. `"name": "niu-dash-fullstack"` inside `projects/niumination-workspace/`), it **is a rename** — the files were moved but the internal project name wasn't updated. Document as a rename, not a new project. Add a note in the project's DOX about the name discrepancy.

**Consequences of misclassifying a rename as deletion+addition:**
- Unnecessary new AGENTS.md rows and BACKLOG.md entries (duplication)
- Loss of git history (same repo, same `.git/`, just moved)
- Confusion in the project catalog (two entries for one codebase)

**Verifying clean vs dirty rename:**
After confirming the rename, check if any `.md` files still reference the old directory name:

```bash
grep -rn "old-name" AGENTS.md BACKLOG.md 2>/dev/null
```

- **Clean rename (this session):** Zero stale references → only date/count headers needed updating
- **Dirty rename:** Stale task entries, catalog rows, or `@project-tag` references found → patch each with `patch()` tool

If clean, just update the header dates and counts. Skip the old-name→new-name find-and-replace entirely — that step is only needed for dirty renames.

**Step 2: Check for stale duplicate paths in manifest**

The collector may report the same repo under two paths (root + `projects/`) if the state file has stale entries from a prior move. Only the canonical path needs doc updates.

A second scenario: the same-named repo legitimately exists in TWO scan levels — e.g. `JHermUSB-portable` at both `projects/JHermUSB-portable/` (has `.git`) AND `Production/JHermUSB-portable/` (also has `.git`). The collector's two-level auto-discovery finds both independently, inflating the manifest's `total_git` count by one. This is NOT a stale-state issue — both copies are real. To detect: check if a repo name appears twice in the manifest's `git_repos` list with different paths. Report unique counts to the user rather than the inflated manifest total.

**Step 3: Cross-reference BACKLOG.md and AGENTS.md**

After verifying the delta, scan the docs for stale version numbers, counts, and dates — even if they aren't the CHANGED ITEM:

- Version numbers — the most common doc staleness (e.g. niu-dash v2.16.5 → v2.16.8)
- Audit counts (22/22 → 27/27)
- File counts in headers
- HEAD hashes in project sections

Surgical patching rules:
- Use `patch()` tool with unique old_string + surrounding context
- One patch per change — never rewrite entire files
- Only touch BACKLOG.md, AGENTS.md, and brain/ docs
- Keep the formatting exactly as-is — only change stale data

**Step 3b — HEAD hash cross-reference:**
The manifest includes HEAD hashes for every tracked repo. BACKLOG.md per-project sections (`|- **HEAD:** ...`) are prone to two errors:
  - **Swapped hashes** — same two hashes appear in the wrong projects' sections (e.g. niu-vermilion shows kune-ya.com's hash and vice versa). Detect by comparing each section's HEAD against the manifest hash for the matching project.
  - **Stale hashes** — a project's HEAD line hasn't been updated since the last doc sync. Detect when the manifest hash for a project does not appear in any BACKLOG.md section under that project.
  Always verify every BACKLOG.md HEAD against the manifest hash for the same project. When patching, include 3+ lines of surrounding context (project header + description + blank line + HEAD line) to guarantee uniqueness. If a hash is swapped, you'll likely need two coordinated patches — one for each affected project.

**Step 4: Handle count discrepancies**

Three sources of project counts exist and may not agree:
| Source | What it captures | Reliability |
|--------|-----------------|-------------|
| **eco-collect.py manifest** | Auto-discovered dirs at scan time | 🟢 High (mechanical) |
| **AGENTS.md / BACKLOG.md headers** | Human-curated counts, may lag | 🟡 May be stale |
| **Actual filesystem** | What currently exists on disk | 🟢 Highest — but may differ from both |

Prefer actual filesystem counts for patches. Do not update doc headers unless the discrepancy is clearly stale.

**Step 4b — Filesystem audit table structural update:**
When Production/* repos transition from one aggregated non-git entry to individually-detected git items, the BACKLOG.md Filesystem Audit table needs a new category row (e.g. `Git + Remote (prod)`). The total stays the same, but the composition shifts: non-git count decreases, git count increases. Update the non-git item list under the table when dirs are added to or dropped from tracking. Always preserve the existing table format — only change stale counts, row labels, and item names.

**Step 4c — Cross-register new repos:**
When the manifest lists a repo not seen before, check both AGENTS.md and BACKLOG.md:
  1. If the repo IS in AGENTS.md but NOT in BACKLOG.md's project task list or scoreboard → add it to P3 (pending/monitoring) and append a row to the scoreboard table matching the format of existing P3 entries.
  2. If the repo is NOT in AGENTS.md → add a brief catalog entry under the appropriate category, then add to BACKLOG.md P3.
  3. If already listed in both → only header dates and counts need refreshing.
  New repos always land in P3 (monitoring) unless the user has explicitly promoted them to active development.

**Step 5: When nothing is stale — skip**

If the CHANGED ITEM resolved to a transient state and no doc version numbers, counts, or dates are stale, report findings without patching. "No changes needed" is a valid outcome.

**Pitfall — "Missing dir" ≠ directory deletion — collector scope change:** Non-git directories flagged as `Missing dir` by the eco-collector may still exist on disk. The signal means the collector stopped tracking them (scope change in auto-discovery logic), NOT that the user deleted them. Always verify with `ls <path>/<dir> 2>/dev/null`. If the directory exists, the agent's job is to document the scope change (and optionally investigate WHY the collector dropped it), not to mark the directory as deleted in DOX.

**Pitfall — "Missing repo" for Production/ items is a scope change, not deletion:** When CHANGED ITEMS lists `Missing repo: Production/<name>`, the repo almost certainly still exists at `Production/<name>/` with its `.git` intact. The collector collapsed the 10+ Production/ sub-repos into one umbrella `Production/` entry (file_count: ~113K). This is a deliberate collector aggregation change. Verify with `ls -d Production/<name> 2>/dev/null && git -C Production/<name> rev-parse --short HEAD`. If found, update DOX counts (total items decreased, Production/ entry count increased) and note the aggregation — do NOT create a "deleted repo" narrative.

**Pitfall — Same-named repos at multiple scan levels inflate git count:** When a repo name exists at both `projects/<name>/` AND `Production/<name>/` (both with `.git`), the collector's three-level auto-discovery finds both independently, inflating `total_git` by 1. Always check for duplicates in the manifest's `git_repos` list. Report deduplicated counts rather than the raw manifest total when constructing DOX headers.

**Pitfall — Stale state file causes false-positive change alerts on the next run:**
When a prior agent run patched docs (e.g., moved a repo from root to `projects/`, or marked a project as REMOVED FROM DISK) but did NOT update the state file, the next cron run re-discovers the *original* discrepancy. The manifest diff compares against the stale saved state, not the newly-patched docs. The result: `CHANGED ITEMS` shows a "missing repo" that the docs already account for.

Fix: After any doc restructuring or project-move surgery, run `python3 scripts/eco-collect.py --force` to persist the current filesystem state. This prevents 15-minute-later crons from re-raising an already-resolved delta. The `--force` flag rebuilds the entire manifest from scratch rather than comparing against the stale file.

When you encounter a false-positive "missing repo" alert during a routine cron pass (no active restructuring work happening):
1. Check the docs first — does AGENTS.md already show the project at its new path? If yes, the state file is stale.
2. Run `ecosystem-sync` → view manifest path — confirm `brain/logs/eco-manifest.json` shows the old path.
3. Run `python3 scripts/eco-collect.py --force` to refresh the state file.
4. Verify the next cron pass (15 min later) is silent.

This is different from true staleness (where the docs themselves haven't been updated yet). Always check the docs first before touching the state file.

**Common pitfalls:**
- **`git status` returns no output for clean repos** — Not an error. Check the exit code.
- **Manifests may list repos under `projects/` that no longer exist** — Always `test -d` before referencing a path in a patch.
- **Pre-run data ≠ current state** — Between collection and processing, a repo could be cloned (resetting dirty state) or a branch switched. Always verify.
- **Sibling subagent overwrites patches with fabricated data** — The pre-run collector may spawn a subagent that continues writing ecosystem docs AFTER you make your patches. This subagent has no access to your verified git state and may emit false claims (e.g. "✅ Published — 41 files, CI ready" for a repo with zero commits and no remote). Defend against this by: (1) making your patches in rapid succession and re-verifying immediately, (2) checking for and reverting false claims after each patch round, and (3) being explicit in the old_string about the CURRENT (possibly incorrect) content rather than assuming only your changes exist.
- **Patch tool with `|||| |` table-formatted markdown** — AGENTS.md uses multi-pipe table rows (`|||| | ...`) for its header banner. The patch tool's fuzzy matching can double up pipes when old_string has fewer pipes than the actual file content. Always cross-check the exact pipe count before and after a patch on these lines. If fuzzy matching produced an extra pipe, fix with a targeted second patch using the wrong output as old_string.
- **BACKLOG.md `|- **HEAD:**` lines are easy to patch wrong** — BACKLOG.md uses `|- **HEAD:** ...` format for commit hashes in per-project sections. These lines contain only a short hash (7 chars) and `|` pipe prefix — the tool's fuzzy matching can accidentally match across sections when multiple projects share the same leading characters. Always include 3+ lines of surrounding context (the `### project — \`path/\`` header + description + empty line) to guarantee uniqueness. Verify the diff shows exactly one replacement.
- **Non-git composition shifts require structural edits, not just count bumps** — When the non-git dir list changes (e.g. `tools/` dropped, `scripts/`, `aistudio-google`, `arena.ai` added), the BACKLOG.md Filesystem Audit table needs its non-git item rows replaced and the non-git count adjusted. Do NOT just bump the total — replace the stale items with current ones and add or remove category rows as needed.
**Pitfall — Pre-run LOCK_EXISTS is recoverable** — When the pre-run collector output shows `LOCK_EXISTS`, it does NOT mean the data is lost. The collect script's `mkdir` lockfile is a concurrency guard, not a crash signal. Re-run with `python3 scripts/eco-collect.py` on the agent side to produce fresh data. If the lock is stale (holding process confirmed dead), clean the lockfile first: `rm -rf /tmp/eco-collect.lock && python3 scripts/eco-collect.py`.

**Pitfall — Hermes USB portable mount shadows the real filesystem, causing false-positive changes** — When Hermes runs from a USB portable install, the terminal's `~` resolves to `/Volumes/HermesAgent/.../home/` (the USB's synthetic home), NOT `/Users/<user>/`. Commands like `cd ~/Desktop/Niumination` land on the USB's sparse copy — which may only have 6 dirs and 2 git repos — instead of the real filesystem at `/Users/zaryu/Desktop/Niumination/` which has the full 39-item tree. The eco-collect script hardcodes `NIUMINATION = Path("/Users/zaryu/Desktop/Niumination")` so it reads the correct path IF run via its absolute path (e.g. `python3 /Users/zaryu/Desktop/Niumination/scripts/eco-collect.py`). But if the pre-run wrapper invokes it with a relative path from the wrong CWD, or if the Hermes cron runner's working directory is the USB mount, the scan sees only the sparse USB copy and reports 22 "changes" (missing repos, missing dirs, cleaned dirty states) that don't exist on the actual filesystem.

**Detection — how to tell it happened:**
  - The pre-run CHANGED ITEMS shows `Total items: 39 → 29` (or any large drop) while AGENTS.md still documents 39 items
  - "Missing repo: Production/*" for ALL Production/ subdirs simultaneously — Production/ simply wasn't at the scanned path
  - "Missing dir" for scripts/, aistudio-google, arena.ai — these still exist on the real filesystem
  - Running `eco-collect.py --force` via terminal produces different counts than the pre-run output

**Fix:**
  1. Run the collector from the real filesystem using the absolute path:
     ```bash
     cd /Users/zaryu/Desktop/Niumination && python3 scripts/eco-collect.py --force
     ```
  2. Verify the result shows 39 items (30 git + 9 non-git), not 29
  3. Confirm `python3 scripts/eco-collect.py` now outputs `NO_CHANGES`
  4. No doc patching needed — the docs were already correct

**Prevention for cron scripts:** Any `no_agent=true` script or cron pre-run wrapper that invokes eco-collect.py must either (a) `cd /Users/zaryu/Desktop/Niumination` first (absolute real path), or (b) invoke python with the absolute script path: `python3 /Users/zaryu/Desktop/Niumination/scripts/eco-collect.py`. Never rely on `~/` resolution or the cron workdir setting to reach the correct Niumination root when running from a Hermes portable install.
- **New repos in manifest may already be in AGENTS.md but not BACKLOG.md** — The eco-collect manifest reflects filesystem reality (all repos). AGENTS.md is usually synced. BACKLOG.md — specifically the P3 task list and scoreboard table — is the lagging surface. New projects need a P3 entry plus a scoreboard row before the next read.
- **Filesystem Audit table totals must match the breakdown sum** — When bumping the Filesystem Audit total count in BACKLOG.md (e.g. 39→42), verify the individual category rows sum to the new total. If the header says 42 but `Git+Remote (root)+Git+Remote (proj)+Git+Remote (prod)+Git No Remote+No Git (root)+No Git (proj)` adds up to 39, you've created an arithmetic contradiction. The breakdown must be updated (adding missing category items or adjusting row counts) to match the claimed total. Patch the breakdown rows before or simultaneously with the total line — never bump the total without verifying the math. This matters because the Filesystem Audit table uses a different categorization methodology (by location/function) than the header's git+non-git breakdown, and the two can diverge when repos move categories.
- **HEAD hashes can be SWAPPED between projects, not just stale** — A swapped hash looks identical to a stale hash (it doesn't match this project's manifest entry), but the hash WILL match a different project's manifest entry. Always cross-reference every HEAD against the manifest for BOTH the current project AND nearby projects when a mismatch is found.
- **Filesystem Audit date ≠ Scoreboard date ≠ Kanban date — check all three** — BACKLOG.md has at least three independent date stamps: the Filesystem Audit section header, the Scoreboard section header, and the Kanban system line at the top. Each can be a different stale value. When updating dates, verify all three independently rather than assuming they share a single stale anchor.

### Ecosystem Reorganization — Active vs Dormant

When the root ecosystem has accumulated dormant/stale projects mixed with active ones, reorganize into a clear three-tier structure:

```
Production/   🏭  Deployed, stable, mature
projects/     🔧  Active development
incubator/    💤  Dormant — not currently worked on
```

**Trigger:** User says "rapikan ekosistem", "pisahkan proyek aktif dan belum dikerjakan", or the projects/ directory is cluttered with stale repos.

### Step 1 — Audit & Identify Status

For each directory in `projects/`, determine status:

| Signal | Status | Move to |
|--------|--------|---------|
| `git log --oneline --since="1 month ago"` has commits | Active | Stay in `projects/` |
| Last commit >3 months ago, no user mentions | Dormant | `incubator/` |
| User explicitly says "done/hapus" | Mature/Remove | `Production/` or delete |
| Duplicate of Production/ entry | Clean up | Delete the projects/ copy |

### Step 2 — Create incubator/

```bash
mkdir -p /Users/zaryu/Desktop/Niumination/incubator
mv /Users/zaryu/Desktop/Niumination/projects/<dormant-projects> /Users/zaryu/Desktop/Niumination/incubator/
```

Projects moved retain their `.git` history and files — only the location changes.

### Step 3 — Archive Redundant Files

Files that are truly obsolete (old backups, experimental labs, stale documentation, vendor zip files) go to a single `archive/` directory rather than being scattered at root:

- **archive/Belum disentuh/** — Promising ideas never explored (usually zips)
- **archive/backup/** — One-off backups of project state
- **archive/labs/** — Experiments, prototypes, one-off HTML exercises
- **archive/media-lib/** — Old media asset indices
- **archive/*-docs/** — Documentation sets for tools no longer in use
- **archive/terax-ai-analysis/** — One-off research reports

Binary files in archive (zips, pngs, backups) should be excluded from git tracking via `.gitignore`. Only `.md` and other text files remain tracked.

### Step 4 — Recategorize AGENTS.md & BACKLOG.md

- Move entries from `projects/` section to `incubator/` section (or create one)
- Bump `projects/` dir count down, `incubator/` dir count up
- Mark dormant project tasks as P3 (monitoring) or archived

### Step 5 — Update eco-collect.py Scan Scope

The auto-discover in `eco-collect.py` must be told about `incubator/`:

```python
# Add to auto_discover_git_repos():
incubator_dir = os.path.join(root, 'incubator')
if os.path.isdir(incubator_dir):
    for item in os.listdir(incubator_dir):
        git_dir = os.path.join(incubator_dir, item, '.git')
        if os.path.isdir(git_dir):
            git_repos[item] = os.path.join(incubator_dir, item)
```

Then run `python3 scripts/eco-collect.py --force`.

### Pitfalls

- **Don't move active projects** — if a project has commits in the last month, it belongs in `projects/`, not `incubator/`. Verify with `git log --oneline -5` before moving.
- **incubator/ not scanned by eco-collect** — The auto-discover only scans root + projects/. Add incubator/ explicitly to the script. Without this, moved repos vanish from the eco-manifest count.
- **Archive zips inflate git repo size** — Add `archive/Belum disentuh/` and other archive binary dirs to `.gitignore` before committing the restructured root. Remove them from git tracking with `git rm -r --cached`.

## Ecosystem Inventory Cleanup

Clean up standalone files in the Niumination root that aren't tracked by the ecosystem manifest. Auto-discovery (eco-collect.py) only finds **directories** (git and non-git) — standalone files like `*.md`, `*.toml`, `*.bak` in root are invisible to it and silently accumulate.

**When to use:**
- User asks "cek apa aja yang ada di root yang belum terdaftar" / "check root for unregistered files"
- After noticing root-level files that don't appear in any ecosystem scan
- User requests ecosystem cleanup / "rapihin root"

**Step 1: Scan — Identify unregistered items**

```bash
# List root files (not dirs)
ls -1A ~/Desktop/Niumination/ | grep -v '^\.' | grep -v '/$'

# Read current manifest
python3 -c "import json; d=json.load(open('brain/logs/eco-manifest.json')); print('Git:', len(d.get('git',[]))); print('Non-git:', len(d.get('non_git',[])))"
```

Common unregistered root file types:

| File type | Examples | Typical cause |
|-----------|----------|---------------|
| Stale architecture docs | `MASTERPLAN.md` | Written before brain/vault system existed |
| Backup files | `AGENTS.md.bak` | Auto-backup never cleaned up |
| Old snapshots | `REKAP-NIU-DASH.md` | One-time report never archived |
| Config files | `.gitleaks.toml` | Valid standalone with no registration |

**Step 2: Analyze — Read & classify each file**

Read every unregistered file fully. Determine:

| Class | Meaning | Typical Action |
|-------|---------|----------------|
| **Stale duplicate** | Content redundant with active docs | Delete |
| **Outdated original** | Architecture doc that predates brain vault | Revise → `brain/docs/` → delete original |
| **Valid standalone** | Config/tool file with no better home | Keep, optionally note in eco-manifest |
| **Garbage** | Scratch notes, old logs, temp exports | Delete |

**Step 3: Recommend — Present proposal with action per file**

Include: purpose, size, freshness, recommended action. Get user approval before destructive actions.

**Step 4: Execute — Apply the plan**

For revise+move:
- Read full contents with `read_file`
- Write revised version to `brain/docs/` with `write_file`
- Delete original with `rm`

For delete-only: `rm STALE-FILE.md`

**Step 5: Verify — Confirm root is clean**

```
ls -1A *.md *.toml 2>/dev/null    # Only expected files remain
```

**Step 6: Sync — Update documentation surfaces**

1. If AGENTS.md file counts changed, update Directory Structure tree
2. Log cleanup in `brain/logs/` or `brain/docs/ecosystem-changelog.md`
3. Run `python3 scripts/eco-collect.py --force` to refresh manifest
4. If `brain/docs/` received new content, update file reference there

**Masterplan revision methodology** — converting stale architecture docs into living documents.

When revising an outdated architecture/blueprint doc (e.g. MASTERPLAN.md v1.3 → brain/docs/masterplan-ecosystem.md v2.0):

1. **Read the entire doc** — don't skim; gaps hide in cross-references
2. **Map every claim to current reality** — for each section check "does this exist?"
3. **Replace hardcoded counts** with real values from eco-manifest (e.g. "28 projects" → "30 items: 18 git + 12 non-git")
4. **Mark planned-vs-existing** — for every tool/script/system show ✅ existing or ⏳ planned + gap note
5. **Add gap analysis** — compare original blueprint vs actual state with honest "not yet built" markers
6. **Preserve architectural vision** — theoretical framework (tiers, layers) is valuable even unimplemented; keep with annotations
7. **Living document** — v2.0 (not "final"), include revision date + "reflects current state" note

Reference: `references/root-cleanup-2026-06-22.md` — real session artifact with full walkthrough.

## Move Project to Production/ 🏭

Moves a project from `projects/<name>/` to `Production/<name>/`. Changes the maturity tier — the project goes from "experimental/active" to "mature & finished."

**Trigger:** User says "pindahin X ke production" for a project that's deployed and stable.

### Eligibility Check

Before proposing a move, verify:

| Criteria | Check | 
|----------|-------|
| Deployed & live | GH Pages returns 200, Vercel shows green, or the app is in real-world use |
| Not already in Production/ | `ls Production/<name>` should not exist |
| Has a working git remote | `git remote -v` shows a valid GitHub URL |
| Build passes (if applicable) | `npm run build` or equivalent succeeds |

Projects still in active P1/P2 development with no public deploy should stay in `projects/`. Only mature/released projects qualify for Production/ 🏭.

### Move Steps

**Step 1 — Physical move**
```bash
mv projects/<name> Production/<name>
```

**Step 2 — Update project's own AGENTS.md** (if exists)
- Change `Lokasi:` → `Production/<name>/`
- Add `🏭 Production/` marker if there's a status line
- Commit: `git add -u && git commit -m "mv: <name> → Production/" && git push`

**Step 3 — Update root AGENTS.md** (4 sub-updates)

| Sub-update | Where | What |
|-----------|-------|------|
| Tree count | Line `├── Production/` | Bump count (e.g. `7 dir` → `10 dir`) |
| Tree entries | Production/ tree section | Add new entry with description |
| Tree removal | projects/ tree section | Remove the entry from projects/ |
| Catalog table | Catalog section | Change `projects/xxx/` → `Production/xxx/ 🏭`, update date |
| Eksekusi Selanjutnya | Top section | Remove from "immediate" list if there |

**Step 4 — Update root BACKLOG.md** (6 sub-updates)

| Sub-update | What |
|-----------|------|
| Header line | Add `🏭 di Production/` marker |
| Task marker | `[~]` → `[x]` if the task was P1/P2 audit, or add `moved to Production/ 🏭` |
| Scoreboard | Append `🏭 Production` to the project's rightmost column |
| D1 entry | Add `[date] Production move — <name> → Production/ — @<tag>` |
| Done count | Bump header `5 ✅ done` → `N ✅ done` |
| Filesystem header | Bump `**N pindah ke Production/**` if this is tracked |

**Step 5 — Update eco-collect scan scope**
```python
# If the move requires a new scan level (e.g. Production/* was not scanned before), add:
scan_dirs += sorted(NIUMINATION.glob("Production/*"))
```
Then run: `python3 scripts/eco-collect.py --force`
### Step 6 — Refresh ecosystem manifest

```bash
python3 scripts/eco-collect.py --force
```

### Step 7 — Commit brain + Niu-Dash

```bash
# brain — eco-manifest.json

# Production/niu-dash — ecosystem-status.json  
cd ../Production/niu-dash && git add public/data/ecosystem-status.json && git commit -m "sync: ecosystem status — moved <name> to Production/" && git push
```

### Pitfalls

- **eco-collect.py doesn't scan Production/ by default.** The original `auto_discover_git_repos()` only scanned root + `projects/`. After the first Production/ move, add `scan_dirs += sorted(NIUMINATION.glob("Production/*"))` to the script. Without this, moved repos disappear from the eco-manifest count.
- **AGENTS.md tree has TWO sections** — The Production/ tree and the projects/ tree are independent. You must add to one AND remove from the other. Leaving the old projects/ entry creates a stale reference that the user will spot.
- **BACKLOG.md scoreboard is line-length-sensitive** — The rightmost column aligns with word-wrapped monospace. Don't add 🏭 if it breaks the alignment; use `🏭 Production` (with a space) to match the column width.
- **The `scripts/` dir is in `NON_GIT_DIRS`** — This is correct, don't remove it. `scripts/` is a non-git collection by design.
- **`Production/` entry in NON_GIT_DIRS** — The line `"Production"` in `NON_GIT_DIRS` is correct because `Production/` dir itself is not a git repo. The `Production/*` sub-repos are discovered via the explicit `scan_dirs += ...` line in `auto_discover_git_repos()`, not by scanning NON_GIT_DIRS.
- **Verify the GH Pages deploy** — After commit+push, `curl -sI "https://niumination.github.io/<repo>/"` should return 200. If the CI hasn't deployed yet, wait a minute and retry.

### Reference Files

| File | When to Use |
|------|-------------|
| `references/ecosystem-dashboard-json.md` | After Production/ move, to regenerate the ecosystem-status.json and commit to Niu-Dash |
| `references/eco-collect-architecture.md` | To verify auto-discovery logic includes Production/* scan level |

## Mark Project as Mature (No Production Move) 🏁

When a project is **done** but not deployable to Production/ (requires VPS, external hardware, etc.), mark it as **mature** on GitHub and clean up the local clone.

**Trigger:** User says "tandai X sebagai mature" or "hapus X dari lokal, tandai mature."

### Steps

**Step 1 — GitHub Maturity Markers**

Set description with maturity note:

```bash
cd /path/to/project
gh repo edit Niumination/<repo> \
  --description "MATURE — <original description>. Butuh VPS untuk production deployment." \
  --add-topic "mature" \
  --add-topic "production-ready"
```

Push existing work one last time (ensure everything is committed and pushed):

```bash
git add -A && git commit -m "chore: final push — project mature" && git push
```

**Step 2 — Create Priority Issue**

```bash
gh issue create \
  --repo "Niumination/<repo>" \
  --title "PRIORITAS: butuh VPS untuk production" \
  --body "Project ini sudah mature dan siap production deployment, membutuhkan VPS (DigitalOcean/Vultr/Linode)." \
  --label "priority"
```

If the `priority` label doesn't exist, create it first or use a different approach:

```bash
gh label create priority --repo Niumination/<repo> --color "#FF0000" --description "High priority"
```

**Step 3 — Delete Local Clone**

```bash
rm -rf /Users/zaryu/Desktop/Niumination/projects/<repo>/
rm -rf /Users/zaryu/Desktop/Niumination/incubator/<repo>/
```

**Step 4 — Update Ecosystem Docs**

| Surface | Update |
|---------|--------|
| **AGENTS.md** | Remove from projects/ tree, add note under a "Mature (remote only)" section if one exists, or mark with `📦 Mature` tag |
| **BACKLOG.md** | Task marker → `[x]`, add `mature — butuh VPS` note, bump done count |
| **Kanban** | Set task status to `done` |

**Step 5 — Refresh eco-manifest**

```bash
python3 scripts/eco-collect.py --force
```

### Pitfalls

- **Local delete is irreversible on Hermes USB** — The deleted repo only exists on GitHub after push. Make sure `git push` succeeded (verify on GitHub.com) before deleting locally.
- **No local dir = no eco-collect scan** — The mature project disappears from the manifest's git count. Back-fill the AGENTS.md count or the manifest will drop by 1.
- **`priority` label may not exist** — `gh label create priority` first. If the repo was cloned from a fork or is a plain `gh repo create`, it may have zero labels.
- **`gh repo edit` requires permission** — Work in the canonical repos (github.com/Niumination/*) where the user has admin access.

## Ecosystem Blueprint Documentation — Observer AI

As part of the ecosystem documentation set, a full integration blueprint for **Observer AI** (screen-monitoring micro-agent platform) has been created:

| Doc | Path |
|-----|------|
| Blueprint Set | `docs/observer-ecosystem-integration/` (6 files) |
| Status | Blueprint — BELUM dieksekusi |
| Priority | 🔴 Phase 1: Foundation → Phase 2: Agent Deployment → Phase 3: Data Integration |
| Assessment | `references/third-party-integration-assessment.md` (Observer AI example + workflow) |

**Key takeaway:** Observer AI is a sensor layer (screen/OCR/mic → local LLM → notifications), NOT a replacement for Hermes or herdr. Runs as a separate desktop app. AGPL-3.0 — communicate via file/API, not code linking.

### Git Security Pitfall

**Create .gitignore BEFORE first `git add`** — When initializing a new git repo (especially for a directory that contains PI/ or credentials), write the .gitignore FIRST, then `git add`. If PI/ or other secrets get tracked in the initial commit, they persist in git history even if removed in a later commit. For a private repo this is lower risk, but still ideal to avoid. If secrets were already committed, use `git rm -r --cached <secrets_dir>` to stop tracking them going forward. Full history purge requires `git filter-branch` or `bfg`.

### Submodule Tracking Note

The root ecosystem-config repo tracks submodules (gitlinks) for Production/*, projects/*, brain/, etc. `git status` showing `m <path>` is expected — the `m` means the submodule HEAD differs from the index, not that there's uncommitted work in the root repo itself.

## Ecosystem Asset Integration — External Knowledge Base / Reference Collection

When the user has a large external directory (like `~/Desktop/AI-Memory-Collection/`) that is NOT a project itself but contains valuable configs, hooks, models, or documentation from multiple tools, follow this assessment + integration workflow.

### Phase 1 — Scan & Size

```bash
# Total size & structure
du -sh /path/to/external-collection/
find /path/to/external-collection -maxdepth 3 -not -path '*/\.*' | head -80
```

Determine: is it a compact config dump (~10-50MB) or a large asset cache (~500MB+)? Large ones (models, DB dumps, caches) are reference-only; compact ones may be actionable.

### Phase 2 — Read the Index Documents

External collections often have a README.md or index doc. Read these first — they tell you what the collection was, why it was collected, and when:

```bash
cat /path/to/external-collection/README.md
cat /path/to/external-collection/memory.md 2>/dev/null
```

Key data to extract: tool names, session counts, model sizes, config file locations, hooks/scripts that are re-runnable.

### Phase 3 — Classify Each Component

| Class | Definition | Ecosystem Action |
|-------|-----------|-----------------|
| **⚡ Actionable** | Re-runnable scripts, hooks, configs the ecosystem can use | Copy into `scripts/hooks/`, `scripts/templates/`, or `tools/` |
| **📄 Reference-only** | memory dumps, session logs, endpoint caches | Document in BACKLOG.md + create `docs/<asset>.md` as pointer |
| **📦 Static assets** | Model files (GGUF), large DBs, media | Leave in place, note their path + purpose in docs — NEVER copy into ecosystem dir |
| **🗑️ Stale / Duplicate** | Tool configs that are superseded by live ecosystem config | Skip — don't copy, don't document unless user asks |

**Detection rules:**
- Hooks and scripts: search for `#!/bin/`, `.sh`, `.bash`, `.py` — these are re-runnable
- Configs: JSON, TOML, YAML config files for AI tools — check if they contain API keys (if yes, DON'T copy, just reference)
- Models: `.gguf`, `.bin`, `.pt` files >10MB — reference only, too large for ecosystem dir
- Caches: endpoint cache, model catalog, session DB — reference only, session-specific

### Phase 4 — Integrate Actionable Parts

```bash
# Copy hooks into ecosystem scripts
mkdir -p ~/Desktop/Niumination/scripts/hooks
cp -R /path/to/external-collection/<hooks-dir>/* ~/Desktop/Niumination/scripts/hooks/
```

Verify the hooks don't contain hardcoded absolute paths or credentials before copying.

### Phase 5 — Create Documentation Pointer

Create `docs/<asset-name>.md` in the ecosystem describing:
- Location on disk
- Total size & what it contains
- Table of components with class (actionable/reference/static/stale)
- Key actionable parts already integrated (hooks, scripts)
- Which BACKLOG.md section was updated
- Any known caveats (stale data, embedded secrets)

### Phase 6 — Reference in BACKLOG.md

Add an entry to the AI ECOSYSTEM (or analogous) section:

```markdown
| **<Asset Name>** | <source> | <size> | ✅ **Referenced** |
```

### Pitfalls

- **Large model files (~1.4GB+)** — NEVER copy into ecosystem dir. The ecosystem is a git repo and should stay lean. Note the path and move on.
- **API keys in config files** — Scan every file before copying. Config files from tools like JCode, OpenCode, or Claude may contain API key remnants. If found: don't copy the file, document the path with a ⚠️ instead.
- **Cache data is session-stale** — Endpoint cache, model catalogs, and session logs from 1-2 days ago are already stale. They're reference-only for understanding past behavior, not for re-use.
- **memory.md may duplicate ecosystem data** — The external collection's memory.md likely contains Hermes memory, BACKLOG.md content, and user profile info extracted at snapshot time. It's a copy, not canonical. Don't update it — update the canonical ecosystem docs instead.
- **Hooks from "Orca" or other tools may assume specific paths** — Check each hook for hardcoded `~/.config/`, `~/Library/`, or `/Applications/` references. These hooks were designed for the original environment, not the ecosystem. Document the assumption rather than patching the hook unless the user asks.
- **Don't confuse "integrated" with "canonical"** — Adding a docs pointer means "we know this exists and where to find it." It does NOT mean the ecosystem depends on it. The external collection can be deleted any time without breaking anything.

## Category Reference (Niumination)

| Category | Typical count | P1 examples | P2 examples |
|----------|:------------:|-------------|-------------|
| 🏛️ Pemerintahan & SPBE | 11 | — | PemdiAcehTengah, LKH |
| 🤖 AI & Coding Ecosystem | 10+ | — | Flame-ADE, JHermUSB, Niu-Flow |
| 🌐 Web Apps & Tools | 18 | kune-ya.com | niu-vermilion, niu-cast |
| 🎬 TEDEO | 2 | TEDEO (4 bugs) | TEDEO-Kanban |
| 🖥️ Dotfiles | 6+ | — | — |
| 📚 Knowledge | 5 | — | — |
| ❌ Archived | 1+ | AgentRouter | — |
