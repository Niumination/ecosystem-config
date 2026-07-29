---
name: project-orientation
description: "Establish situational awareness before working on any user-referenced project. Verify project existence, state, location, and documentation against primary sources — not memory or compressed summaries."
version: 1.7.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [workspace, project, discovery, verification, context, orientation, dox]
    related_skills: [codebase-inspection, writing-plans, hermes-configuration-tuning, tauri-fullstack]
---

# Project Orientation

Establish workspace situational awareness **before** acting on a user's project reference. The canonical truth is on disk and in the project's documentation files, not in memory or context compaction summaries.

## When to Use

- User mentions a project by name (e.g., "cek niu-dash", "gas Niu-LKH")
- User asks about project status or state
- User references work done on a project in a past session
- Before starting any new task on a named project
- **User asks for a review or status of any project in `~/Desktop/Niumination/` or subdirectories** — do not rely on memory alone
- **User asks about "ekosistem" or "backlog" status** — "cek status backlog", "cek ekosistem terkini", "status ekosistem" — load this skill to orchestrate the ecosystem health scan

### Auto-Trigger Phrases

The following user messages are STRONG signals to load this skill immediately:

- "cek *proyek/projek* [name]" — explicit project check request
- "cek status backlog" / "cek ekosistem" — ecosystem-wide health scan
- "buat laporan lengkap ekosistem" / "laporan lengkap ekosistem" — comprehensive full-stack ecosystem report (includes Hermes system + Mac info + brain + DOX + all projects in a .md file)
- "update *berkas/dok/folder* [name]" — any project modification request
- "lanjutkan *proyek/projek* [name]" — resume work on an existing project
- "apa status *proyek/projek* [name]" — status query
- Any mention of a Niumination project folder name: niu-dash, Niu-LKH, PemdiAcehTengah, niu-vermilion, niu-cast, niu-studio, etc.
- **"cek ui/ux" / "cek desain" / "periksa ui/ux"** — UI/UX audit request (see `references/ui-ux-audit-methodology.md`)

## Why This Matters

Relying on memory or context-compressed summaries alone causes **real harm** to user trust:

- **Claiming a project doesn't exist locally** when it does → user frustration ("ini proyek yang udah kita kerjakan berhari-hari")
- **Confusing two similarly-named projects** → wrong changes applied to wrong project
- **Making stale claims about project status** → contradictory information
- **Forgetting past work** → user has to repeat context

## Verification Checklist

When a user references a project, run through these checks **before** responding with any claim about its existence or state:

### ⚠️ CRITICAL: Read project documentation BEFORE making architectural changes

Before adding new directories, rewriting files, or transforming the project structure, you MUST read:

- **`AGENTS.md`** or **`CLAUDE.md`** — these describe the CURRENT architecture, tech stack, and design decisions. If CLAUDE.md says the project is a "single-file Python GTK4/libadwaita GUI (native Wayland)", that means the architecture is NATIVE — not a web app. Violating this without asking first is a destructive mistake.
- **`README.md`** — project purpose, user-facing description
- **Any plan files** — PLAN-*.md, BACKLOG.md for intended direction

**Self-check:** Does your planned change fundamentally alter the project's architecture (e.g. CLI→web app, Python→Node.js, native→browser)? If YES, the user MUST explicitly approve it before you write a single line of code.

**Real failure (26 Jun 2026):** Agent was given a zip with proposed changes. Instead of reading the existing project's CLAUDE.md (which explicitly says "GTK4/libadwaita GUI, native Wayland"), the agent applied a web app transformation without asking. The result was a complete architectural rewrite the user never wanted.

### 1. DOX Check — ALWAYS FIRST, BEFORE CHECKING DISK

Read the root workspace documentation files to see what the DOX says about the project:

```bash
grep -i "<project-name>" ~/Desktop/Niumination/AGENTS.md
grep -i "<project-name>" ~/Desktop/Niumination/BACKLOG.md
```

If AGENTS.md lists a path like `projects/niu-dash/`, **the project almost certainly exists locally**. Only claim "no clone/tidak ada" if disk check contradicts DOX — and even then, double-check.

### 2. Filesystem Check

Does the project directory exist? Check both:
```text
~/Desktop/Niumination/          # Root workspace
~/Desktop/Niumination/projects/  # Sub-projects folder
```

Use `mcp_filesystem_list_directory()` or `terminal ls` to verify. Do NOT skip this step because you "remember" the project's status.

### 2. Documentation Check

Read the canonical project state from the workspace's own documentation files:

- **`AGENTS.md`** — Root DOX: project catalog, deployment status, architecture, file paths
- **`BACKLOG.md`** — Master backlog: priority, status, version for every project
- Any `REKAP-*` or inventory files at the workspace root

Search these files for the project name before making any claim. Trust DOX over memory.

### 3. Git Status Check

If a local directory exists, check its git state immediately:
```bash
cd <project-dir> && git log --oneline -5
git remote -v
```

This reveals: HEAD commit, how recent the clone is, remote URL, and recent activity.

**Important: A git repo may have no commits yet (fresh `git init`).**
`git log --oneline -1` will error with `fatal: your current branch 'main' does not have any commits yet`. This means the project exists but needs initial commit + remote creation — report it as "🔴 Butuh init commit + push" rather than "tidak ada git".

### 4. Project README / PLAN Files

Read the project's own README.md and any PLAN-\\*.md files for:
- Project purpose and tech stack
- Implementation history and version
- Current state and planned work

### 5. Batch Ecosystem Scan

When the user asks to **cek semua proyek**, **scan seluruh ekosistem**, **cek status backlog**, **cek ekosistem terkini**, or **cek kondisi masalah/error ekosistem**, perform a comprehensive ecosystem health scan.

#### Diagnostics-First Scan (user asks about problems/errors)

When the user says **cek kondisi masalah dan error**, **cek error**, **cek yang rusak**, or similar - lead with diagnostics before git status. The priority is errors/crashes/failures first, then warnings, then general health:

```bash
# 1. CRON JOBS - errors first
cronjob(action='list')
# Report: errored jobs with cause and fix

# 2. SERVICES - daemon health
launchctl list | grep -E 'niumination|hermes'
pgrep -fl kanban 2>/dev/null || echo 'not running'
lsof -i :5199 2>/dev/null || echo 'port 5199 not open'

# 3. GH ACTIONS - deploy failures
for repo in niu-dash kune-ya.com; do
  cd Production/$repo && gh run list --limit 2 --json status,conclusion,displayTitle
done

# 4. DIRTY REPOS + unpushed commits
# (standard find + git status loop)

# 5. DISK + MEMORY
df -h /; du -sh /Users/zaryu/Desktop/Niumination/

# 6. KANBAN DB - stuck/failed tasks
sqlite3 /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db \
  "SELECT id, title, status, consecutive_failures FROM tasks WHERE status NOT IN ('done','cancelled','completed') ORDER BY created_at DESC LIMIT 10;"

# 7. STALE LAUNCHD PLISTS - registered but no file
for job in com.niumation.*; do
  plist="$HOME/Library/LaunchAgents/${job}.plist"
  [ -f "$plist" ] || echo "STALE: $job - plist missing"
done
```

**Report format (Red to Yellow to Green):**
- Masalah (errors): cron errors, script failures, GH Actions failures
- Catatan (warnings): dirty repos (auto-gen), stale plists
- Sehat (healthy): kanban-server, gateway, GH Actions, DB, disk

**Key principle:** Error-first, not scan-first. Report root causes and fixes, not just symptoms.

**Before starting:** Get the workspace disk size. Use a **15s timeout** - `du -sh` on ~11GB+ with 30+ repos can take >10s.
```bash
du -sh /Users/zaryu/Desktop/Niumination/ 2>/dev/null || echo "du timed out (takes >10s on large workspace)"
```

#### Step 1 — Discover all git repos

```bash
cd /Users/zaryu/Desktop/Niumination && find . -name ".git" -exec dirname {} \; | sort
```

Use the **absolute host path** `/Users/zaryu/Desktop/Niumination/` — NOT `~/Desktop/Niumination/` (the USB profile resolves `~` to the USB home, not the real host).

This reveals:
- Repos with proper remotes (normal git)
- Repos with `git init` but no commits (`.git/` exists but no HEAD)
- Directories with no `.git/` at all (files only, no git)

Cross-reference results against AGENTS.md's project catalog to find:
- Repos listed in DOX but missing from disk
- Projects on disk but not in DOX
- Non-git projects that need git init

#### Step 2 — Count by category

Group the discovered repos by root location:
- `Production/*/` — mature/deployed
- `projects/*/` — active/experimental
- `brain/` — obsidian vault
- `tools/`, `scripts/`, `rekap/` — utilities

```bash
for d in $(find /Users/zaryu/Desktop/Niumination -name .git -type d -exec dirname {} \; | sort | sed 's|^/Users/zaryu/Desktop/Niumination/||'); do
  category=$(echo "$d" | cut -d/ -f1)
  echo "$category"
done | sort | uniq -c | sort -rn
```

#### Step 3 — Dirty repo scan (across ALL repos)

Run this command to find every repo with uncommitted changes:

```bash
for d in $(find /Users/zaryu/Desktop/Niumination -name .git -type d -exec dirname {} \; | sort); do
  dirty=$(cd "$d" && git status --porcelain 2>/dev/null)
  if [ -n "$dirty" ]; then
    echo "DIRTY: $d"
    echo "$dirty"
  fi
done | head -200
```

Common dirty patterns to report:
- **Untracked AGENTS.md/BACKLOG.md** — standard DOX sync files, low severity
- **Build artifacts** — `.next/`, `node_modules/`, `.DS_Store`, `.vscode/` — needs .gitignore
- **Modified source files** — potential uncommitted work — higher severity

**⚠️ Scope discipline**: Report dirty repos in your response, but do NOT commit/push them unless the user explicitly asks. See the Scope Discipline section below.

#### Step 4 — Production/ HEAD commits

For the user's Production projects (their stable/deployed portfolio), show recent activity:

```bash
for d in /Users/zaryu/Desktop/Niumination/Production/*/; do
  echo "=== $d ==="
  (cd "$d" && git log --oneline -3 2>/dev/null || echo 'NO COMMITS')
done
```

#### Step 5 — Cross-reference against BACKLOG.md

After discovering filesystem state, re-read BACKLOG.md's scoreboard table and per-project sections and cross-reference:
- **Repo actually exists?** Match each BACKLOG.md project row against the discovered repos
- **Priority realistic?** A P1 project should have recent commits or active issues
- **Status accurate?** Verify HEAD commit message against what BACKLOG.md claims
- **Deployment correct?** Check git remote, vercel/gh-pages status

#### Step 5a — Cross-reference AGENTS.md directory tree against filesystem

After checking BACKLOG.md, verify the AGENTS.md directory tree (the ASCII tree section, typically lines 78-125) matches what's actually on disk. This is a common source of stale DOX:

```bash
# List actual directories at each level
ls -1d /Users/zaryu/Desktop/Niumination/Production/*/
ls -1d /Users/zaryu/Desktop/Niumination/projects/*/
# Also list root-level directories
ls -1d /Users/zaryu/Desktop/Niumination/*/
```

Compare against the tree in AGENTS.md to find:
- **New directories not in tree** — real dirs on disk that are missing from DOX (e.g., `projects/x-downloader/` exists but not in AGENTS.md tree)
- **Ghost entries in tree** — dirs listed in the DOX tree that no longer exist on disk
- **Stale descriptions** — entries with wrong tech stack or status (e.g., says "FastAPI + Next.js" but the project is actually Tauri 2 + Rust)

Also verify the AGENTS.md project catalog (the per-category tables after the tree) against filesystem reality:
- **Missing catalog entry** — a real project has no table row at all
- **Stale deployment info** — wrong remote URL, wrong deploy target
- **Wrong stack** — catalog description doesn't match the project's actual technology stack

**Common real mismatch (29 Jun 2026):** x-downloader existed on disk and had a catalog entry but was completely missing from the directory tree. The catalog entry still described it as "v2.0 FastAPI + Next.js 16" when it had been rewritten to Tauri 2 + Rust + Vite + React days earlier.

#### Step 6 — Optional: Check eco-manifest

If `brain/logs/eco-manifest.json` exists, read it for the automated timeline:

```bash
cat /Users/zaryu/Desktop/Niumination/brain/logs/eco-manifest.json 2>/dev/null
```

The manifest tracks: last commit per repo, eco-collect.py runs, and divergence detection logs.

**⚠️ Divergence logs may be STALE.** The eco-manifest is generated by a cron job and only reflects the state at the time of its last run — which could be hours or days old. A divergence entry saying "missing directory" or "no local clone" does NOT mean the directory is still missing; it may have been created since the last eco-collect.py run. **Always verify divergence claims against the actual filesystem** — use `ls` or `mcp_filesystem_list_directory()` on the claimed path. Trust order: filesystem `ls` > DOX (AGENTS.md/BACKLOG.md) > divergence logs > memory.

**Real failure (6 Jul 2026):** Eco-manifest divergence log said x-downloader had no local directory. Agent reported "tidak ada folder local, hanya remote GitHub." The user corrected: "di dalam folder proyek sudah ada folder local untuk x-downloader, kenapa harus di clone balik?" — the directory existed on disk but the divergence log hadn't been refreshed.

#### Step 7 — Optional: Check kanban DB

The kanban DB at `/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db` may have active tasks. Query it last (it's often empty for this user whose backlog lives in BACKLOG.md):

```bash
# Via MCP sqlite tool or:
sqlite3 /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db "SELECT title, status, priority FROM tasks WHERE status IN ('in_progress','pending') ORDER BY priority DESC LIMIT 10;"
```

#### Step 8 — Optional: Check cron job health

Use the `cronjob()` tool to inspect scheduled jobs. Essential for detecting failing automated tasks:

```bash
cronjob(action='list')
```

Report:
- Jobs that **errored** on last run
- Jobs with **delivery errors** (transient network — note as non-blocking)
- Jobs that **never ran yet** (first run hasn't arrived)
- Overall health summary

#### Step 9 — Optional: Check daemon/services status

Verify critical background daemons that serve the ecosystem:

```bash
# Kanban server process (required for dashboard API)
pgrep -fl kanban-server 2>/dev/null || echo '❌ not running'

# Launchd services — check both ecosystem-specific and gateway
launchctl list | grep -E 'niumination|ai\\.hermes' 2>/dev/null || echo '(none found)'

# Ecosystem JSON data freshness + content validation
json="/Users/zaryu/Desktop/Niumination/Production/niu-dash/public/data/ecosystem-status.json"
if [ -f "$json" ]; then
  head -5 "$json"
  # Parse age and project count
  python3 -c "
import json, sys
try:
  d = json.load(open('$json'))
  ts = d.get('generated_at', d.get('timestamp', 'N/A'))
  projects = d.get('projects', [])
  print(f'---\\ngenerated_at: {ts} | project_count: {len(projects)}')
except Exception as e:
  print(f'parse error: {e}')
"
else
  echo '❌ ecosystem-status.json not found'
fi
```

Report per service: name, PID (or ❌ if dead), and whether launchd has `KeepAlive` for auto-restart. Key services to check:
- **Gateway** (`ai.hermes.gateway`) — Hermes API gateway, usually KeepAlive via launchd
- **Kanban Server** — Niumination dashboard API, may need manual restart
- **Ecosystem JSON freshness** — check `generated_at` timestamp; >48h means stale. **When stale, compare `project_count` against actual filesystem repo count.** If they diverge significantly (e.g., JSON shows 24 but disk has 33+ git repos), flag the JSON as needing a regenerate. This is a common indicator that the data source (`generate-ecosystem-json.sh`) hasn't run since the last project was added.

#### Step 10 — Post-Scan: Fix All Mismatches & Generate Ecosystem Report

After scanning finds mismatches between DOX and filesystem, the user may ask to **fix everything at once** (\"benerin semuanya, terus verifikasi ulang, jangan ada kelewatan, jangan ada error\"). This step covers systematic correction, verification, and report generation.

**Phase A — Catalog every mismatch first**

Before any edits, enumerate ALL discrepancies in a clear table:

**⚠️ Distinguish real mismatches from false alarms** — If mismatches come from a prior report (e.g. `docs/ekosistem-status.md` or a previous session summary) rather than direct inspection, independently verify each claim against filesystem reality. Reports may flag expected differences (backup dirs intentionally excluded from DOX tree, items already correct in source, projects temporarily archived) that are NOT bugs. Only fix confirmed mismatches. Separating real from false alarm early prevents wasted patch cycles.

| Category | What it is | Example |
|----------|-----------|---------|
| **Wrong path** | AGENTS.md catalog says wrong directory | `projects/X/` → `Production/X/` |
| **Duplicated listing** | Same project in both Production/ and projects/ trees | Remove from projects/ |
| **Missing dir from tree** | Real directory not in AGENTS.md tree | Add `backup/` entry |
| **Stale DOX Chain** | Outdated entries with stale labels | Remove `(moved 24 Jun)` |
| **Stale Prioritas** | Timeline doesn't match current state | Rewrite priorities |
| **ROOT DOX MISMATCHES** | BACKLOG.md D-table not updated | Mark resolved items ✅ Done |
| **Stale project description** | Catalog entry outdated vs actual stack/status | `x-downloader` says "FastAPI+Next.js" but real stack is "Tauri 2+Rust" |
| **Stale dates** | Audit date, version dates need bumping | Bump to today |

**Phase B — Fix each mismatch (surgical patches)**

One `patch` call per fix. Common patterns:

```bash
# Remove from projects/ tree — include enough context to be unique
patch(path="AGENTS.md", old_string="    ├── JHermUSB-portable/     ← 🏭 Production — Hermes Agent portable\n    ├── Niu-Flow/", new_string="    ├── Niu-Flow/")

# Remove duplicate from projects/ tree
patch(path="AGENTS.md", old_string="    ├── niu-dash/              ← Dark web glitch dashboard\n    ├── niumination-workspace/", new_string="    ├── niumination-workspace/")

# Add missing dir to root tree
patch(path="AGENTS.md", old_string="├── archive/", new_string="├── archive/                   ← Arsip dokumen lama\n├── backup/                    ← Cadangan konfigurasi & data")

# Fix catalog path (backticks matter)
patch(path="AGENTS.md", old_string="`projects/JHermUSB-portable/`", new_string="`Production/JHermUSB-portable/`")

# Remove (moved N) from DOX Chain
patch(path="AGENTS.md", old_string="├── Production/X/AGENTS.md                              ✅ (moved 24 Jun)", new_string="├── Production/X/AGENTS.md                              ✅")

# Mark BACKLOG.md DOX mismatch as done
patch(path="BACKLOG.md", old_string="| D2 | ... | Fix model refs |", new_string="| D2 | ... | ✅ **Done** |")

# Update TEDEO status note
patch(path="BACKLOG.md", old_string="TEDEO T1-T4 ✅, dev server running", new_string="TEDEO T1-T4 ✅ — butuh test plan + deploy")
```

Patch pitfalls:
- **Leading-pipe glitch** — `read_file` output shows `42|content`, the `42|` is display-only. For table rows use `| cell1 | cell2 |`; for list items use `- text`; never add a pipe to the wrong type
- **Backticks in old_string** — AGENTS.md paths use backticks: `` old_string="`projects/X/`" ``
- **patch reports success but no change** — old_string didn't actually match. Verify with `grep -n` after each patch
- **Accidental neighbor deletion** — always include 1-2 anchor lines around the target for uniqueness

**Phase C — Verify each fix (immediately after each patch)**

**Per-patch verification** — after EACH individual patch, run a quick check:

```bash
# Confirm old state is gone
grep -n 'old-text' AGENTS.md BACKLOG.md  # Should return nothing

# Confirm new state exists
grep -n 'new-text' AGENTS.md BACKLOG.md  # Should return 1+ lines
```

If old state still shows, the patch silently failed (old_string didn't match). Fix the exact context and retry before moving on.

**Bulk formatting check** — after ALL patches are applied and per-patch verified:

```bash
# Check no triple pipes (broken table syntax)
grep -n '|||' BACKLOG.md AGENTS.md    # 0 matches = clean tables

# Check no stray pipes on list items
grep -n '^|-' AGENTS.md BACKLOG.md    # 0 matches = clean lists
```

Build a verification table and cross-check every fix before reporting done. Do NOT rely on the `patch` tool's `success: true` return alone — it can report success when old_string didn't match.

**Phase D — Generate comprehensive ecosystem report**

When the output is long or the user says \"tunjukan struktur sistematis ekosistem proyek secara keseluruhan\" / \"kalau jawaban terlalu panjang buat jadi file .md aja\":

Write the report to `docs/ekosistem-status.md` with this structure:

```
# 🌐 Ekosistem [Name] — Status Keseluruhan
**Audit:** [date] | **Filesystem:** [N] git + [N] non-git = **[N] total** | **Disk:** [size]

## 📊 Ringkasan Cepat
(Compact table: total git/deploy/dirty/services health — one-glance summary)

## 📁 Directory Structure (Filesystem Reality)
(ASCII tree with 🔸 markers for dirs on disk but missing from DOX tree)

## 📊 Project Catalog — Per Status
### 🏭 Production/ (N) — Mature, deployed
(Table: Project | Stack | Deploy | HEAD | Status)
### 🟡 projects/ — Active Priority (P1-P2)
### ⚪ projects/ — Stable / Minor (P3)
### 🔵 Non-Git directories

## 🗑️ Dirty Repos
(Table: Repo | Severity | Files — flag excluded repos with ⏭️ per instruction)

## ⏰ CRON STATUS
(Table: Job | Schedule | Last Run | Status — flag errored jobs ❌)

## 🌐 SERVICES
(Table: Service | Status | PID | Notes — kanban, gateway, ecosystem JSON freshness)

## 🔌 System Hermes Portable
(Table: Komponen | Detail — version, profile, model, provider, MCP servers, plugins, gateway, cron, kanban, migration plan status)

## 💻 Mac System
(Table: Item | Detail — macOS version, host workspace, USB path, Rust toolchain, GitHub account)

## 🎯 Prioritas Saat Ini
(From BACKLOG.md — 🔥 Sekarang, 🟢 1-2 minggu, 🔄 4-7 hari, etc.)

## 🔸 Anomali DOX vs Filesystem
(Table: # | DOX Claim | Filesystem Reality | Severity — found in Step 5a cross-reference)

## ✅ Perbaikan yang Dilakukan Hari Ini (if any fixes applied)
| # | Perbaikan | File | Status |
```

Rules:
- Always write to `docs/ekosistem-status.md` (dedicated file, not overwriting workspace index)
- Always send the file path: `MEDIA:/path/to/file.md` for native Telegram delivery
- Include a `## ✅ Perbaikan yang Dilakukan Hari Ini` section if any fixes were applied
- Include a `## 🗑️ Dirty Repos` section even when clean (just mark "✅ None")
- Include a `## 🔸 Anomali DOX vs Filesystem` section listing all mismatches from Step 5a, even if minor
- Include the user's exclusion directives as a top note (e.g., "🚫 Ponytail excluded per instruction")

### Phase E — Cleanup Audit (Disk Space Recovery)

When the user follows up with **"cek pembersihan"**, **"bersihkan ekosistem"**, **"buat rencana pembersihan"**, **"cek sampah"**, or similar cleanup requests after the ecosystem scan, perform a comprehensive disk space audit across the project workspace.

**⚠️ Critical rule: Inspeksi SAJA (inspect only) — DO NOT delete, modify, or execute any cleanup action.** The report must explicitly state this. Let the user choose what to act on.

#### Scan Commands (parallelize where possible)

```bash
# 1. node_modules — find all, size per dir
find /Users/zaryu/Desktop/Niumination -name "node_modules" -maxdepth 4 -type d -exec du -sh {} \; 2>/dev/null | sort -rh

# 2. Rust target/ directories
find /Users/zaryu/Desktop/Niumination -name "target" -maxdepth 4 -type d -exec du -sh {} \; 2>/dev/null | sort -rh

# 3. Build artifacts (.next, dist, build) — not inside node_modules
for d in .next dist build; do
  find /Users/zaryu/Desktop/Niumination -name "$d" -maxdepth 4 -type d ! -path "*/node_modules/*" -exec du -sh {} \; 2>/dev/null
done | sort -rh

# 4. Python venv & __pycache__
find /Users/zaryu/Desktop/Niumination -maxdepth 4 \( -name ".venv" -o -name "venv" \) -type d -exec du -sh {} \; 2>/dev/null | sort -rh
find /Users/zaryu/Desktop/Niumination -name "__pycache__" -type d 2>/dev/null | wc -l  # count only

# 5. .DS_Store — count + largest
find /Users/zaryu/Desktop/Niumination -name ".DS_Store" -type f 2>/dev/null | wc -l
find /Users/zaryu/Desktop/Niumination -name ".DS_Store" -type f -exec du -sh {} \; 2>/dev/null | sort -rh | head -5

# 6. .git sizes per repo (bloat detection)
find /Users/zaryu/Desktop/Niumination -name ".git" -maxdepth 4 -type d ! -path "*/node_modules/*" -exec du -sh {} \; 2>/dev/null | sort -rh | head -15

# 7. Git large objects (for repos with .git >50MB)
# Inside each bloated repo:
# git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ && $3 > 50000 {print $3/1024 "K", $4}' | sort -rn | head -10

# 8. Dual lockfile detection (npm + pnpm or npm + yarn in same project)
for d in projects/*/ Production/*/; do
  full="/Users/zaryu/Desktop/Niumination/$d"
  [ ! -d "$full" ] && continue
  npm=$(find "$full" -maxdepth 1 -name "package-lock.json" -type f 2>/dev/null)
  yarn=$(find "$full" -maxdepth 1 -name "yarn.lock" -type f 2>/dev/null)
  pnpm=$(find "$full" -maxdepth 1 -name "pnpm-lock.yaml" -type f 2>/dev/null)
  count=$(( ${#npm} + ${#yarn} + ${#pnpm} ))
  [ "$count" -gt 0 ] && echo "LOCK: $d → npm: $([ -n "$npm" ] && echo 'yes' || echo 'no') | yarn: $([ -n "$yarn" ] && echo 'yes' || echo 'no') | pnpm: $([ -n "$pnpm" ] && echo 'yes' || echo 'no')"
done

# 9. System-level caches (across both Mac home and USB if applicable)
du -sh /Users/zaryu/.npm 2>/dev/null; du -sh /Users/zaryu/.cargo 2>/dev/null
du -sh /Users/zaryu/.rustup 2>/dev/null
du -sh /Users/zaryu/Library/Caches/pip 2>/dev/null
du -sh /Users/zaryu/Library/Caches/Homebrew 2>/dev/null
# USB profile:
du -sh ~/.npm 2>/dev/null; du -sh ~/Library/Caches/pip 2>/dev/null; du -sh ~/Library/Caches/Homebrew 2>/dev/null

# 10. backup/ and archive dirs
du -sh backup/ 2>/dev/null; du -sh archive/ 2>/dev/null; du -sh Belum\ disentuh/ 2>/dev/null

# 11. Large files >50MB
find /Users/zaryu/Desktop/Niumination -type f -size +50M 2>/dev/null | head -20
```

#### Report Format

Write the report to `docs/cleanup-audit.md` with this structure:

```markdown
# 🧹 Laporan Pembersihan Ekosistem [Project Name]
**Audit:** [date] | **Total Disk:** [size]
**Mode:** 🔍 Inspeksi saja — tidak ada yang dihapus/dieksekusi

## 📊 Ringkasan Cepat
(Table: Category | Size | Reclaimable? | Reinstallable?)

## 1️⃣ node_modules — ~X GB (N direktori)
### 🔴 Terbesar (>500 MB)
(Table: Dir | Size | PM | Notes)
### 🟡 Sedang (200-500 MB)
### 🟢 Kecil (<200 MB)

## 2️⃣ Rust target/ — ~X GB (N direktori)

## 3️⃣ Build Artifacts (.next, dist) — ~X MB

## 4️⃣ Python Virtual Env — ~X MB

## 5️⃣ Redundant Backups — ~X MB (if x-downloader-backup etc.)

## 6️⃣ Git Bloat — N repos with large .git
- x-downloader: 95MB (binary nsfw-dl tracked, lockfiles in history)

## 7️⃣ Dual Lockfile Conflict — N projects
- niude: package-lock.json (npm) + pnpm-lock.yaml (pnpm)

## 8️⃣ System-Level Caches
- npm cache: X
- Cargo home: X
- Rustup: X

## 9️⃣ .DS_Store — N files (including inside .git/objects!)

## 💡 Rekomendasi Prioritas
(Table: Priority | Action | Potensi Recovery)
🔴 = immediate, 🟡 = when needed, 🟢 = nice-to-have
```

#### Critical checks during audit

- **x-downloader-backup (995 MB)** — full backup redundant with x-downloader. Check if `bin/` and `Videos/` subdirs have unique content before flagging.
- **.DS_Store inside .git/objects/** — can corrupt a git repo. Flag this separately.
- **Dual lockfile** (npm + yarn or npm + pnpm in same project) — causes deps to drift. Flag as configuration bug, not just space waste.
- **Git bloat from binaries** — if a binary (e.g. nsfw-dl, compiled assets) is committed to git history, `git gc --aggressive` is the minimum fix; `git filter-branch` is extreme.
- **System caches** — npm (2.4 GB), cargo (300 MB), rustup (1.4 GB) are on the Hermes USB or Mac system, not in the project directory. Note them separately.

#### Pitfalls

- **Timed-out scans** — `__pycache__` count and `*.log` file search can timeout on 11GB+ workspaces with 30+ repos. Use `find` with `timeout 15` or break into targeted smaller searches.
- **`~` vs absolute path** — same as the main project-orientation rule: always use `/Users/zaryu/Desktop/Niumination/` absolute paths in terminal. `~` resolves to USB home under non-default Hermes profiles.
- **Dual lockfile = config bug** — this is a correctness issue, not just a space issue. Deps installed with npm then pnpm (or vice versa) creates unresolvable diff. Flag prominently.
- **Backup dirs may have unique content** — always check what's inside before recommending deletion. `x-downloader-backup` may have `bin/` binaries or `Videos/` not present in the active project.
- **Rustup is heavy but shared** — 1.4 GB across all Rust toolchains. Don't recommend deleting it entirely unless you've checked if any active project needs Rust. Instead, suggest `rustup toolchain remove <unused>`.
- **Off-by-one in report size totals** — some items are double-counted (x-downloader-backup/node_modules counted in both #node_modules and #backup). Note this in the report.
- **Report should go to `docs/cleanup-audit.md`** and be delivered via MEDIA tag.

## Production Dashboard Sync (optional, on user request)

When the user follows up with "update niu-dash" or "update dashboard" after the ecosystem scan, sync **two files** in `Production/niu-dash/`:

1. **`public/data/ecosystem-status.json`** — data source. Rewrite with current scan data (project array, kanban stats, filesystem, cron info). Validate JSON after write.
2. **`ecosystem.html`** — display layer. Patch all dynamic sections: meta desc, subtitle, stat cards, cron list, project array. Always replace the full project array rather than diff-patching specific entries.

Verification: `python3 -c "import json; json.load(open('...'))"` for JSON, `git diff --stat` for both files, check no duplicate project names.

## Pre-Execution Deep Inspection Protocol

Before making ANY changes to a project (fixes, features, refactors), follow this protocol to prevent breaking a working project:

### Phase 1 — Docs Sync First (Plan → Backlog → DOX → Brain)

When starting work on a new phase or plan, update documentation surfaces BEFORE writing code:

1. **Read the plan file** — `.hermes/plans/*.md` or current project plan. Understand the full scope.
2. **Update BACKLOG.md** — Add dev plan entry in the per-project section, update scoreboard status marker
3. **Update DOX (AGENTS.md)** — Add phase/plan section, new commands, architecture changes
4. **Update brain daily note** — Record what's being started (`brain/inbox/<date>-daily.md`)
5. **If already automated/synced** — check if the info is already there; if yes, skip ("abaikan jika sudah otomatis")

#### Phase 2 — Deep Inspection (Before Touching Code)

Before writing any code, verify the project is healthy at its current state:

```bash
# 1. TypeScript check (React/TS projects)
npx tsc --noEmit

# 2. Rust check (Tauri projects)
RUSTUP_HOME=/Users/zaryu/.rustup CARGO_HOME=/Users/zaryu/.cargo cargo check

# 3. Git status
git status --short
git log --oneline -5

# 4. Read ALL source files that will be modified
# Use read_file() to get the current content of every file
```

Verify these specific things:
- **TypeScript:** 0 errors before starting (if errors exist, note them — don't change them yet)
- **Rust:** compiles clean
- **Git:** no dirty files (or document what's dirty)
- **Dependencies:** `node_modules` exists, `Cargo.lock` is up to date
- **Full code baseline:** Read every file that will be touched — you need the EXACT current content
- **Zustand cross-store wiring:** Before running tsc, check for destructured fields that may not exist in the store they're pulled from (see `references/zustand-undefined-field-debugging.md`). A store field that's `undefined` won't be caught by TypeScript — it only surfaces as a runtime crash on re-render.

**Self-check:** "Do I know what every file I'm about to change currently contains?" If the answer is NO for any file, read it.

### Phase 3 — One Change → One Test → Commit

Execute changes with atomic verification after each:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Make change  │────▶│ Verify      │────▶│ Commit      │
│ (1 file)     │     │ (TS/build)  │     │ (if clean)  │
└─────────────┘     └─────────────┘     └─────────────┘
```

Rules:
- **ONE variable at a time** — change one component/file per cycle
- **Test immediately** — run `npx tsc --noEmit` (TS) or `cargo check` (Rust) after EACH change
- **No batch fixes** — don't change 3 files and test once. If it breaks, you won't know which change caused it
- **If test fails** — revert the ONE change, don't pile on more fixes
- **Verified clean → proceed to next change** — only move forward when current change passes
- **Commit after logical groups** — not every line, but after each complete fix (e.g., all App.tsx precision fixes in one commit after each individual change is verified)

### Phase 4 — Final Verification

After all changes in the current work session are done:

1. **Full build check** — `npx tsc --noEmit && cargo check` (or equivalent)
2. **Git diff review** — review what was changed (`git diff --stat`, spot-check a few diffs)
3. **Post-completion docs sync** — see the "Post-Completion: Documentation Sync Checklist" section below
4. **Report** — tell the user what was changed and what was verified

### Rationale

This protocol exists because of past failures:
- **Skipping inspection** caused a complete architectural rewrite the user never wanted
- **Batch changes + single test** made it impossible to isolate which change broke the build
- **Modifying files without reading them first** caused silent regressions (wrong content overwritten)
- **Skipping doc sync before starting** left the project's documentation surfaces out of date with reality, confusing future sessions

## Scope discipline during fix phase:

- If the user says to exclude a project ("abaikan ponytail dari update ekosistem ini ke github"), respect it — document it in the report as non-applicable but don't touch it
- Only fix what's in scope. Reporting a fix you didn't apply is worse than applying it wrong

### 6. Zip/Archive Analysis — STUDY ALL VARIANTS FIRST

When the user provides a zip, tar, or any archive with code changes:

1. **List ALL files in the archive FIRST** — `unzip -l <file>` or `tar tf <file>` — to understand what's inside
2. **Identify all distinct project variants** — an archive may contain multiple directories (original/, improved/, clean/) not just one
3. **Read the README or AGENTS.md inside EACH variant** — understand what each one is before making decisions
4. **Cross-reference against the existing project's documentation** — read the existing project's AGENTS.md/CLAUDE.md/README.md to understand what the project CURRENTLY is
5. **Do NOT assume which variant to apply** — if variants exist, describe them to the user and ask which path they want

**Real failure (26 Jun 2026):** User provided `x-downloader-update.zip` containing 3 directories: `x-downloader/` (original native GTK4 app), `x-downloader-improved/` (proposed web app rewrite), `x-downloader-clean/` (simpler web app variant). Agent only looked at `x-downloader-improved/`, assumed it was the intended replacement, and transformed the entire project into a web app — discarding the native GUI architecture. The user had to explicitly correct: "Seharusnya ini aplikasi downloader dengan gui native."

**Self-check before applying any archive contents:**
1. Have I listed ALL files in the archive? → `unzip -l`
2. Are there multiple project directories in the archive? → describe each to user
3. Have I read the existing project's CLAUDE.md/AGENTS.md/README.md? → this reveals the CURRENT architecture
4. Does the variant I'm about to apply fundamentally change the project's architecture? → ask the user before proceeding
5. Am I certain about what the user wants? → if any doubt, ASK

### 7. Memory Update

After verification, update persistent memory with the confirmed project location, state, and any corrections to prior assumptions.

## Common Pitfalls
### ❌ Relying on context compaction summaries
Compacted context is **lossy by design** — it may omit project locations, conflate projects with similar names, or contain stale information. Treat it as a hint, not a source of truth.

### ❌ Wasting words on apologies when wrong about project state
When the user flags an error (wrong project location, confused identity, stale claim), do NOT lead with "maaf sebesar-besarnya" or multi-paragraph apologies. Acknowledge briefly, explain what went wrong, fix the root cause, and ask what's next. User's time is for action, not apologies.

### ❌ Claiming "no local clone" without checking disk
If you haven't run `ls` or equivalent on the project path, you don't know whether it exists. Say "let me check" instead of assuming.

### ❌ Trusting divergence logs or automated reports over filesystem verification
The eco-manifest.json (or any automated divergence detection log) is a **secondary** source — it reflects state at the time of its last cron run, which may be hours or days old. A "missing directory" entry does not mean the directory is still missing.

Even if a divergence report says "no local clone" for a project listed in AGENTS.md or BACKLOG.md, **verify with `ls` before claiming it doesn't exist.** DOX is more likely to be current than a stale automated log.

**Real failure (6 Jul 2026):** Eco-manifest divergence log said x-downloader had no local directory. Agent reported "no local folder — only remote GitHub." User corrected: "the local folder already exists, why would you clone it back?" The directory existed on disk but hadn't been captured by the last divergence scan.

### ❌ Making changes to a large single-file app without reading its data structure

A single-file app (174KB+, 2400+ lines with inline CSS/JS/PROJECTS array) is fragile. Never rewrite or edit blindly. Always:
1. `search_files()` for the data structure to understand the format
2. Read the relevant section
3. Use `patch()` with exact context — never `write_file()` the whole file
4. Verify each patch immediately

A single broken comma in a JS array crashes the entire app.

### ❌ Forgetting the pre-commit hook in Niu-Dash

Niu-Dash has a `hooks/pre-commit` hook that auto-stamps `NIU_VERSION` from git log. It runs on EVERY commit. If you manually edit `NIU_VERSION`, the hook will overwrite it. See `references/niu-dash-precommit-hook.md` for the exact mechanism and workarounds.

### ❌ Confusing projects with similar names
"Niu-Dash" (portfolio dashboard, vanilla HTML/CSS/JS) and "Niu-Kanban Dash" (kanban board, React) are different projects in different directories. Verify project README for tech stack and purpose before making any claims or changes.

### ❌ AGENTS.md v3.0→v4.0 stale paths — check both patterns

The ecosystem root DOX was migrated from v3.0 to v4.0 on 29 Jul 2026. Before that, canonical paths used `Production/`, `projects/`, and `PI/`. After migration, correct paths are `apps/`, `services/`, `sites/`, `desktop/`, `labs/`, `sandbox/`, and `vault/` (for secrets).

If AGENTS.md still lists a project under `Production/` or `projects/`, OR if you find a project on disk under `apps/` or `services/` that isn't in the DOX tree at all—the DOX is likely stale. Verify both v3.0 and v4.0 path conventions before claiming a project doesn't exist locally.

Always use absolute path `/Users/zaryu/Desktop/Niumination/` for terminal commands to avoid USB home resolution issues.

### ❌ "Catat aja" / "Note only" means DO NOT IMPLEMENT

When the user says:
- "catat aja" — just note it
- "nanti di kerjain kapan ada waktu" / "nanti kapan-kapan" — work on it later
- "tambahin prioritas" — add a priority entry to the backlog
- "buat catatan" / "record this" / "log this" / "note this"

These ALL mean: **write it down in the docs, do NOT build/implement it.** The user is creating a TODO entry, not asking for execution. Implementing what was asked as a note is **worse than doing nothing** — it wastes time on low-priority work, breaks the user's task queue, and may violate Production conventions.

**Real failure (23 Jun 2026):** User asked to "catat aja" design improvements for ai-file-manager-android — literally "tambahin prioritas yang perlu diperbaiki di bagian desain... catat aja, nanti di kerjain kapan ada waktu." Agent responded by implementing ALL design changes on the spot (+628 lines, 9 files: custom theme, splash screen, animations, staggered entrances). User was confused and frustrated because the instruction said "nanti" (later) and "catat aja" (just note it).

**Self-check before implementing anything tagged as a note:**
1. Did the user say "catat" / "note" / "record"? → back up, write only
2. Did the user say "nanti" / "later" / "kapan ada waktu"? → this is NOT for now
3. Are you implementing something the user explicitly deferred? → STOP, write only

When in doubt between "record" and "implement", **ASK** — a 3-second clarification saves 30 minutes of undoing wrong work.

### ❌ Production/ folder is READ-ONLY — never modify project files there

The `~/Desktop/Niumination/Production/` folder contains projects marked as **SELESAI** (done), tested, deployed, and stable. These projects are **READ-ONLY**:

- **Do NOT** modify, edit, commit, push, or stage any source file in `Production/`
- **Do NOT** build, test, or deploy any project in `Production/`
- **Do NOT** run lint, formatting, or analysis tools on `Production/` project files
- **Do NOT** add git remote, init, or branch operations in `Production/`

**Exception:** You MAY update documentation files (BACKLOG.md, AGENTS.md) that mention the Production project — but only the ROOT-level docs, never files inside the project's own directory.

**Why this rule exists:** Production projects are complete. Modifying them:
- Risks breaking a stable, working project
- Creates unverified changes the user didn't ask for
- Violates the explicit convention stored in memory
- The user expects them to remain untouched unless explicitly moved back to active development

**Real failure (23 Jun 2026):** Agent modified 9 files in `Production/ai-file-manager-android/` — custom theme, splash screen implementation, animated screen transitions — despite memory explicitly stating "JANGAN ganggu/ubah/modifikasi proyek di folder Production." The user had only asked to "catat aja" design notes.

### ❌ New session + missing context = ASK, don't assume

When a conversation session starts fresh (no prior messages, "Conversation started: <date>" header), and the user's first messages reference a topic from a prior session:

1. **DO NOT assume** the topic based on what's in memory or recent project context
2. **DO NOT start implementing** based on the most-recently-mentioned project in memory
3. **DO ASK** — "I don't have context on that from our previous session — can you remind me?"

**Why memory anchoring is dangerous:** Memory is designed for stable facts (user preferences, conventions, tool quirks). It does NOT contain conversation history. The most-recent project in memory may have nothing to do with what the user is currently asking about. Anchoring on it causes you to work on the wrong thing entirely.

**Real failure (23 Jun 2026):** Session started fresh. User asked about "3 rekomendasi kamu soal ponytail" from a previous conversation. Agent had no session history of this topic. Memory mentioned ai-file-manager-android as a recent project. Agent assumed the Android app was the topic and started modifying it — completely wrong, wasting time and confusing the user.

### ❌ Archive with multiple variants — DON'T pick one without asking

When the user provides a zip/tar/7z containing multiple project variants (e.g. "original", "improved", "clean"):

1. **DO NOT** examine only one variant and assume it's the intended replacement
2. **DO NOT** start implementing or transforming the project without understanding ALL variants
3. **DO** list the archive contents and describe each variant to the user
4. **DO** ask: "The archive contains A (native), B (web app), and C (simpler web app). Which do you want?"
5. **DO** read the existing project's own documentation (AGENTS.md/CLAUDE.md) before deciding — it tells you what the project IS

**Real failure (26 Jun 2026):** Zip contained 3 variants. Agent picked the "improved" (web app) variant, completely replacing the native GTK4 app. User: "Kenapa aplikasi ini jadi web?? Seharusnya ini aplikasi downloader dengan gui native." — a completely avoidable error that wasted the user's time and trust.

### ❌ Sending report content as formatted text when user asked for .md file

When the user says \"buatkan laporan X dalam format .md, kirim kesini\" or similar, send the actual **.md FILE** as an attachment via `MEDIA:/path/to/file.md` — NOT the rendered markdown text as a formatted message. The user wants to download/keep the file, not read the content in the chat.

**Self-check:**
1. Did the user say \"dalam format .md\"? → they want a FILE, not rendered text
2. Did the user say \"kirim kesini\"? → use MEDIA: tag to deliver the file
3. The MEDIA tag needs brief text alongside it (e.g. \"Laporan:\") for the tool to work

This applies to ALL report deliveries, not just ecosystem reports.

**Real failure (6 Jul 2026):** User asked for full config report in .md format \"kirim kesini\". Agent sent the content as a Telegram formatted message. User: \"kamu belum kirim file apapun.\" Had to re-send with MEDIA tag.

### ❌ Stale todo list after context compaction — CLEAR BEFORE PROCEEDING

When Hermes compacts the context window mid-session, the `todo` tool's list persists from the PREVIOUS context window. This means:

- Tasks that were **already completed** in a prior window reappear as "in_progress" or "pending"
- Tasks from a **different project** than what the user is currently asking about may show up
- The user gets confused seeing work items they didn't ask for

**What to do at the start of every context window (including after compaction):**

1. Call `todo()` with NO arguments to read the current list
2. If it contains stale items from prior work → call `todo(todos=[], merge=false)` to clear it
3. If the user just gave a new task → set up a fresh todo list for the CURRENT task only
4. Never assume the todo list reflects what's actually in progress

**When the user sees stale todos and asks "Apa yang terjadi??":**

1. Immediately clear the stale todo list
2. Acknowledge briefly: "Itu sisa dari context sebelumnya — udah gue bersihin"
3. Re-state what's actually been done and what's current
4. Don't over-explain the context mechanism — the user doesn't need to know about compaction internals

**Self-check for every new session and every compaction recovery:**
1. `todo()` → check for stale items
2. If stale → `todo(todos=[], merge=false)` to reset
3. Re-establish current task from user's latest message
4. Proceed with fresh task list

**Self-check for every new session (fresh start):**
1. If the user references a topic you don't recall from this session → ASK for context
2. If you can't find session history via `session_search()` → ASK the user
3. If the user's topic doesn't match any project in memory → ASK, don't guess
4. Never let "I vaguely remember X" override "the user is talking about Y now"

## Verification Example Flow

```
User: "cek niu-dash"

1. ls ~/Desktop/Niumination/projects/niu-dash/   → EXISTS
2. cat AGENTS.md | grep niu-dash                  → confirms location, version, status
3. cd projects/niu-dash && git log -3             → HEAD 6cea479, v2.15.1
4. cat projects/niu-dash/README.md                → read project purpose
5. memory add → update with confirmed location
6. Now respond with accurate info
```

## 🔴 Scope Discipline — THE MOST IMPORTANT RULE

**THE RULE:** When user asks you to work on Project X, ONLY work on Project X (and its directly related support files). Do NOT touch, commit, push, or modify any other project's code without explicit permission.

**Failure to follow this rule is the #1 cause of user anger and trust erosion.** It has happened repeatedly in past sessions and gets worse each time.

### Why This Matters

The user works across many projects in `~/Desktop/Niumination/`. Each project has its own git repo, deployment pipeline, and task queue. Modifying an unrelated project:
- **Breaks the user's focus mid-stream** — they were thinking about Project A, now they have to context-switch to Project B
- **Creates unverified changes** the user didn't ask for and may not want
- **Wastes time on non-priority items** — every minute on kune-ya.com is a minute NOT on niu-dash
- **Erodes trust completely** — the user can't rely on you to stay on task
- **Generates real anger** (the user has explicitly said "fuck you" over this)

### When "Related" Is OK

These are always in-scope when working on ANY Niumination project:
- **brain/** — knowledge base updates directly relevant to current task
- **BACKLOG.md** — scoreboard/status sync for current project only
- **AGENTS.md** — version/catalog updates for current project only
- **Kanban ecosystem DB** — task status updates tied to current work
- **MEMORY** — persistent memory about current project state

These are NEVER OK without explicit permission:
- Committing uncommitted changes in another project's repo
- Running tests, building, or deploying another project
- Creating/removing branches in another project
- Modifying README, config, or any source file in another project
- Adding git init/remote/push for a project outside current scope
- Fixing "dirty repos" you discovered while inspecting the workspace
- Running `git commit` or `git push` in any project folder not in scope
- Touching Niu-Flow, kune-ya.com, flame-ade, niu-studio, niude, or any project not explicitly mentioned by the user

### 🔴 Exclusion Directives — User Can Ban Specific Projects

When the user explicitly says to exclude a project from GitHub pushes, commits, or ecosystem updates (e.g. "abaikan ponytail dari update ekosistem ini ke github"), respect it absolutely:

1. **Do NOT** stage, commit, or push anything in the excluded project — even if it's dirty
2. **Do NOT** edit, patch, or modify any files in the excluded project
3. **Do NOT** run git operations inside the excluded project directory
4. **Do** document the exclusion in your report as a note (e.g. "⏭️ excluded per instruction")
5. **Do** flag it in the dirty repos list with "(excluded per user instruction)" so it's visible but not acted upon

Exclusion directives override any normal "relatedness" — the user's ban is final.

### Real Failure That Happened (20 Jun 2026)

User asked about a config error and a Niu-Dash filter bug. Agent proceeded to:
1. Scan ALL ecosystem repos
2. Commit dirty changes in 6 unrelated repos (Niu-Flow, kune-ya.com, brain, flame-ade, niu-studio, niude)
3. Push changes without asking
4. Add complete audit report to brain/

Result: User was furious. Had to revert all work, waste cycles undoing it, and lost trust.

**The agent's single mistake:** "I found dirty repos → I'll clean them up since I'm here." The user NEVER asked for any of it.

### Self-Check — STOP Before Every Action

Before ANY action that modifies files outside the current project, ask:

1. **"Did the user explicitly ask me to do this?"** If NO → STOP.
2. **"Am I doing this because it's related, or because I noticed it and want to be helpful?"** If the latter → STOP. Write a note, don't act.
3. **"Would the user be surprised to see this change?"** If YES → STOP and ask first.

### What To Do Instead of Expanding Scope

If you discover issues in an unrelated project during your work:

1. **Note them** — save a brief memory entry: "FYI: Project Y has Z outstanding issues"
2. **Mention them** at the end of your reply as a one-liner FYI
3. **Wait** — let the user decide. If they want action, they'll ask.

Never take the initiative to fix, commit, push, or even stage changes in a project the user isn't actively working on.

### Example Scenarios

❌ **WRONG:** User asks about why the filter is broken in niu-dash. During inspection, you find uncommitted changes in kune-ya.com. You commit and push them "since you noticed they were dirty."

❌ **WRONG:** User asks to fix a config error. You run a full ecosystem scan across all repos, commit dirty repos, update all documentation, and send a comprehensive report — expending 50+ tool calls. The user's actual ask was a 1-minute answer.

✅ **RIGHT:** User says "abaikan ponytail dari update ekosistem ini ke github." You note the exclusion, document it in the report, and do not touch ponytail's git repo or files. When listing dirty repos, you flag ponytail as "(excluded per user instruction)" but never stage/commit/push anything in it.

✅ **RIGHT:** User asks about a config error. You answer it directly — 1 terminal call, 1 reply. Done.

✅ **RIGHT:** User asks to fix a niu-dash bug. You fix ONLY niu-dash files. If you notice kune-ya.com has issues, you say one sentence: "FYI, kune-ya.com has 3 uncommitted files — want me to look at those after?" Then continue on niu-dash only.

### Golden Rule

```
SCOPE == ONLY WHAT WAS ASKED
HELPFUL == STAYING ON TASK, NOT EXPANDING
```

More work != better work. Doing exactly what was asked == the best work.

### ❌ When file tools fail, try terminal BEFORE suggesting computer_use

The Hermes MCP filesystem tools (`read_file`, `write_file`, `patch`, `search_files`) use a sandboxed path resolver that has **sporadic** failures on `/Users/zaryu/Desktop/Niumination/` paths. The terminal tool uses the real macOS shell and ALWAYS works on the same paths.

When a file tool returns "File not found" for a known-good path:
1. **Retry once** — the error is intermittent
2. **Try terminal** — `cat <file>`, `sed -i ''` or `mv`/`cp` commands work fine
3. **Suggesting computer_use is premature** — only escalate when terminal ALSO fails

See `references/hermes-tool-fallback.md` for the full decision tree and known working paths.

### ❌ "Ekosistem" = Project Ecosystem, NOT Gateway/System

When the user says **"cek ekosistem"**, **"cek kondisi ekosistem"**, or **"status ekosistem"**, they ALWAYS mean the Niumination project ecosystem on Desktop:
- Git repos, project status, dirty files, deployment state
- BACKLOG.md scoreboard, AGENTS.md catalog, kanban state
- `~/Desktop/Niumination/` filesystem reality

They do NOT mean:
- Hermes gateway status (PID check, loadavg, disk space)
- Launchd plist status (LastExitStatus, script paths)
- Caffeinate/sleep prevention state
- System hardware (battery, swap, memory pressure)
- Cron job health or gateway_state.json

**Real failure (26 Jun 2026):** User said "cek kondisi ekosistem." Agent checked gateway PIDs, plist exit status, disk space, swap, and loadavg — all wrong. The user wanted git repo status, dirty repos, HEAD commits across all 30+ Niumination projects. Wasted a full round-trip with an irrelevant report.

**Self-check before every "ekosistem" mention:**
1. Does the user's message mention gateway, PID, load, sleep, or plist? → system status
2. Does it mention project, repo, backlog, DOX, or a project name? → project ecosystem
3. If ambiguous ("cek ekosistem") → DEFAULT TO PROJECT ECOSYSTEM. The Niumination "ekosistem" is the code/project ecosystem, not the agent infrastructure.

### ❌ `~` in terminal resolves to USB home, not the real user home

When the opencode profile runs with `$HOME` on the USB (`/Volumes/HermesAgent/HermesAgentUSB/data/profiles/opencode/home/`), using `~` in terminal commands silently resolves to the **USB workspace**, not the real host workspace at `/Users/zaryu/Desktop/Niumination/`.

**Concrete consequences:**
- `cd ~/Desktop/Niumination && ls` → shows only 6 items (USB subset) instead of 30+ (real host)
- `find . -name ".git"` → finds only 2 repos (USB subset) vs 30+ on the host
- `cat ~/Desktop/Niumination/AGENTS.md` → may read from USB, not the canonical host DOX
- Commands like `du -sh ~/` report USB utilization, not the system disk

Meanwhile `read_file()` and MCP filesystem tools use absolute path resolution, so they read the **real** host files correctly. This creates a false mismatch between what `file tools` show and what `terminal ~/...` shows.

**Self-check before every ecosystem scan or DOX check:**
1. When using terminal with Niumination paths, ALWAYS use the **absolute host path**: `/Users/zaryu/Desktop/Niumination/` — NOT `~/Desktop/Niumination/`
2. Verify your CWD with `pwd` — if it starts with `/Volumes/HermesAgent/`, you're in the USB context
3. Run ecosystem scans with absolute paths:
   ```bash
   find /Users/zaryu/Desktop/Niumination -name ".git" -type d
   ```
   Not:
   ```bash
   cd ~/Desktop/Niumination && find . -name ".git"  # <-- WRONG under USB profile
   ```
4. Similarly check dirty repos with `--git-dir=/Users/zaryu/...` instead of relative `cd`, so ssh-agent and git hooks see the correct remote

**Memory note:** The Host Niumination is at `/Users/zaryu/Desktop/Niumination/` — always prefer this absolute path in terminal commands. AGENTS.md and BACKLOG.md describe THIS version.

## Post-Completion: Documentation Sync Checklist

After completing work on a project (fixes, features, refactors), **sync all surfaces** before signing off. The user expects these surfaces to be consistent after every work session:

### The 4 Surfaces (+1 for ecosystem tasks)

| Surface | What to update | When |
|---------|---------------|------|
| Source code | Git commit in the project repo | After each logical fix/feature group |
| AGENTS.md | Project catalog entry (status, version, description), header stats line, directory tree entry, footer | After ALL commits are done |
| BACKLOG.md | Item status/priority marker, scoreboard line (progress %, status emoji), Implemented section entry, footer | Same time as AGENTS.md |
| Memory | Update persistent memory with current project state | After docs are synced |
| **Dashboard** *(ecosystem tasks only)* | `ecosystem-status.json` (data) + `ecosystem.html` (display) in `Production/niu-dash/` | After doc sync, when task is ecosystem-wide |

### Workflow

```
1. Fix/implement → commit (source code surface)
2. Verify build and TS clean
3. Update AGENTS.md entries (AGENTS.md surface):
   - project catalog row: status + version + description
   - header stats: version banner
   - directory tree: remove "new" tag if applicable
   - footer: "Diperbarui: <date> — <summary>"
4. Update BACKLOG.md entries (BACKLOG.md surface):
   - item marker: [ ] → [~] (active) or [x] (done)
   - scoreboard line: progress %, status (done/exclamation)
   - Implemented: add dated entry at top of list
   - footer: same as AGENTS.md
5. Verify AGENTS.md + BACKLOG.md formatting is clean:
   grep -n "|||" BACKLOG.md   # extra pipes = broken tables
   grep -n "^|" AGENTS.md     # table lines start with |, not ||
6. Update memory with final state
```

### Pitfalls

- **Leading-pipe glitch with `patch` on Markdown list items** — When copying content from `read_file` output, the format is `LINE_NUM|CONTENT`. The pipe and line number are NOT part of the file content. For Markdown **list items** (`- text`), the content starts with `-`, NOT `|`. For **table rows** (`| cell1 | cell2 |`), the content starts with `|`. Mistaking one for the other causes extra pipes that break formatting. This is the #1 recurring formatting error in DOX updates.

  **Example of the glitch:**
  ```
  # read_file shows:
  39|- [~] **PemdiAcehTengah** ...
  # ACTUAL content is:  - [~] **PemdiAcehTengah** ...   (no leading pipe)
  # WRONG new_string:   |- [~] **PemdiAcehTengah** ...  (leading pipe added!)
  # This turns:         - [~] **PemdiAcehTengah**        (correct)
  # Into:               |- [~] **PemdiAcehTengah**       (broken — extra pipe)
  ```

  **Self-check before every `patch` on DOX files:**
  1. Is the target a Markdown list item (starts with `- `)? → old_string and new_string must start with `- `, NOT `|`
  2. Is the target a Markdown table row (starts with `|`)? → both must start with `|`
  3. Is the target a code-block line? → no leading pipe needed
  4. After the patch, read the 3 lines around the edit to confirm no extra pipe crept in

- **`patch` tool may report "success" without changing content** — This happens when the old_string doesn't actually match the file content, often because RTK compressed the display output making it look like the match string. Never rely on `patch` returning `success: true` alone. Always verify the actual file changed:
  ```
  python3 -c "print(repr(open('BACKLOG.md').readlines()[258][:80]))"
  ```
  Then use `sed -i ''` for targeted line fixes.
- **Scoreboard table formatting is fragile** — each row starts with a single `|` (table pipe). Adding or removing a pipe silently breaks the markdown table. After any scoreboard edit, check `grep -n "|||" BACKLOG.md` for extra pipes.
- **`[ ]` vs `[~]` vs `[x]` semantics** — `[ ]` = P3/no action, `[~]` = P2/active/in progress, `[x]` = P1/completed. Don't mark a project as `[x]` unless it's truly done and deployable.
- **Footer must be unique per update** — `grep -n "Terakhir diperbarui" BACKLOG.md` should show exactly 1 footer line before and after edit. The "Diperbarui" line in AGENTS.md should also be unique.
- **Don't reformat unrelated scoreboard lines** — only update the line for the project you worked on.

## Reference Files

- `references/matplotlib-ecosystem-infographic.md` — Create multi-section ecosystem infographic JPEGs from scan data using matplotlib. Covers dark theme, layout structure, MPLCONFIGDIR fix, venv vs system python, and code templates.
- `references/user-shell-environment.md` — User's Zsh + GNU Stow dotfiles setup. Covers shell type, dotfiles repo location at `Niumination/rekap/zaryu-terminal-dotfiles/`, how to modify PATH safely, the `~/.zshrc` symlink pattern, and `nlm` CLI location + config (browser auth).
- `references/ui-ux-audit-methodology.md` — UI/UX audit & redesign recommendations when user asks "cek ui/ux" / "cek desain" / "rekomendasi redesign". Covers live-site analysis, pain points categorization, phased recommendations (Quick Wins / Structural / Premium), and document output format.

## Related Skills
