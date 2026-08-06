# Real Audit Findings — MASTERPLAN v1.3 Compliance Check

**Date:** 2026-06-20
**Spec:** Niumination Ecosystem MASTERPLAN.md (936 lines, v1.3)
**System:** 28 projects, 10 crons, 11 scripts, 20 git repos
**Audit scope:** All 5 integration layers, 5 safety layers, 4 phases

## Summary

| Severity | Count | 
|----------|-------|
| 🔴 Critical | 4 |
| 🟠 High | 4 |
| 🟡 Medium | 4 |
| ✅ OK | 12 |

## 🔴 Critical Findings

### 1. Status Character Mismatch — Parser Ignores 12 Active Tasks

**Spec says:**
- BACKLOG format: `[~]` = in_progress, `[-]` = cancelled (section 4 Layer 1)
- Parser regex includes `- \[([ x~-])\]` (line 247)

**Reality:**
- `kanban-sync.sh` case statement: `"o") kanban_status="in_progress"` — expects `[o]`, not `[~]`
- `daily-heartbeat.sh`: `grep -cE '^- \\[o\\]'` — also expects `[o]`
- kanban.db confirmed: `107|3|0` — 107 tasks, 3 statuses, **0 active** (should be ~12)

**Root cause:** BACKLOG was reformatted from `[o]` → `[~]` during Phase 0.11, but the parser scripts were never updated to match.

**Impact:** All active tasks are silently classified as "todo" in kanban. Dashboard shows no active work. Daily heartbeat reports no active projects. Users see an empty board despite 12 active tasks.

**Cascade:** kanban-sync ← daily-heartbeat ← kanban board ← ecosystem dashboard — every component that reads status from kanban.db gets wrong data.

**Fix:**
```bash
# In kanban-sync.sh, add '~' case:
case "$status_char" in
    " ") kanban_status="todo" ;;
    "~") kanban_status="in_progress" ;;  # ADD THIS
    "o") kanban_status="in_progress" ;;  # Keep for backward compat
    "x") kanban_status="done" ;;
    "-") kanban_status="cancelled" ;;     # ADD THIS
    *) kanban_status="todo" ;;
esac

# In daily-heartbeat.sh, grep for both:
active=$(grep -cE '^- \\[[~o]\\]' "$BACKLOG" 2>/dev/null || echo 0)
```

### 2. Pre-commit Hook Missing Spec-Required Checks

**Spec says (Layer 3, line 328-340):**
- CHECK 1: DOX cross-reference — source code changes → warn if AGENTS.md/BACKLOG.md unchanged
- CHECK 2: .env blocker — any .env in stage → exit 1
- CHECK 3: Gitleaks staged scan

**Reality (30-line hook found at profile path):**
- ✅ Gitleaks scan (CHECK 3)
- ✅ Binary file blocker (NOT in spec — extra)
- ❌ NO DOX cross-reference (CHECK 1 — missing)
- ❌ NO .env blocker (CHECK 2 — missing)

**Impact:** Can commit .env files to any repo without being blocked. Source code can change without DOX update and no warning fires.

**Fix:** Add to `~/.git-template/hooks/pre-commit`:
```bash
# CHECK 2: .env blocker
if git diff --cached --name-only | grep -q '\.env$'; then
  echo "❌ [.ENV] .env files detected in commit. Blocked."
  exit 1
fi

# CHECK 1: DOX cross-reference (warning only, non-blocking)
staged_source=$(git diff --cached --name-only | grep -cE '\.(ts|tsx|js|jsx|py|go|rs)$' || true)
staged_dox=$(git diff --cached --name-only | grep -cE 'AGENTS\.md|BACKLOG\.md' || true)
if [ "$staged_source" -gt 0 ] && [ "$staged_dox" -eq 0 ]; then
  echo "⚠️  [DOX] Source files changed but AGENTS.md/BACKLOG.md not updated."
  echo "   Consider updating documentation for these changes."
fi
```

### 3. Gitleaks Custom Rules Config Missing

**Spec says (Safety E, line 573-587):**
- `~/.gitleaks.toml` should exist with custom rules for `supabase-url` and `niu-gh-token`
- Pre-commit hook should reference this file

**Reality:**
- `~/.gitleaks.toml` — MISSING (file doesn't exist)
- Pre-commit hook references `$(git rev-parse --show-toplevel)/.gitleaks.toml` (per-repo config) — but NO repo has a local `.gitleaks.toml`
- gitleaks runs with default rules only

**Impact:** Supabase URLs and `niu_gh_token` can pass through commits undetected. No custom rules for project-specific secret patterns.

**Fix:**
```bash
# Create ~/.gitleaks.toml
cat > ~/.gitleaks.toml << 'GITLEAKS'
title = "Niumination Gitleaks Config"

[extend]
useDefault = true

[[rules]]
id = "supabase-url"
description = "Supabase URL exposed"
regex = '''supabase\.co\/rest\/v1\/[a-zA-Z0-9]+'''
tags = ["supabase"]

[[rules]]
id = "niu-gh-token"
description = "Niu GitHub Token"
regex = '''niu_gh_token=['\"][A-Za-z0-9_]+['\"]'''
tags = ["github", "token"]

[[rules]]
id = "supabase-anon-key"
description = "Supabase anon key"
regex = '''eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'''
tags = ["supabase", "jwt"]
GITLEAKS

# Fix hook to reference global config instead of per-repo:
gitleaks git --pre-commit --config ~/.gitleaks.toml 2>/dev/null
```

### 4. Gitleaks Pre-commit Config Path Mismatch

**Spec says:** Pre-commit hook should reference gitleaks config
**Reality:** Hook references `$(git rev-parse --show-toplevel)/.gitleaks.toml` (per-repo path that doesn't exist anywhere)

**Impact:** If gitleaks exits non-zero when config is missing, EVERY commit in every repo is blocked as "secrets detected" (false positive). Currently errors are piped to `/dev/null`, but exit code still matters.

**Fix:** Change hook to reference `~/.gitleaks.toml` (global path that will exist after Fix #3).

---

## 🟠 High Findings

### 5. RAPI-RAPI-BESAR.md Not Archived

**Spec says (Phase 0.13):** Archive to `archive/2026-06-20-RAPI-RAPI-BESAR.md`

**Reality:** File still at `/Users/zaryu/Desktop/Niumination/RAPI-RAPI-BESAR.md` (root)

**Impact:** Root directory clutter. Not critical but breaks Phase 0 completeness claim.

**Fix:** `mv RAPI-RAPI-BESAR.md archive/2026-06-20-RAPI-RAPI-BESAR.md`

### 6. `generate-ecosystem-json.sh` Missing

**Spec says (Layer 5, line 405):** Script at `scripts/generate-ecosystem-json.sh` should generate `ecosystem-status.json`

**Reality:** File doesn't exist. `ecosystem-status.json` doesn't exist either. Ecosystem page works by fetching from Kanban API directly instead.

**Impact:** MASTERPLAN's specified data pipeline (health-checker → JSON → gh-pages → dashboard) is incomplete. The ecosystem page works via a different path (Kanban API), which means if the Kanban server is down, the ecosystem page relies on BACKLOG.md fallback only.

**Fix:** Either create the generator script, or update the MASTERPLAN to document the actual pipeline (Kanban API → dashboard).

### 7. `niu-vermilion/AGENTS.md` Is Not a Real DOX

**Spec says (Tier 1 requirement #1):** Each Tier 1 project MUST have `projects/<name>/AGENTS.md` with DOX-specific content (stack, env vars, deploy, architecture)

**Reality:** File exists but contains only 5 lines of Next.js agent rules comment. No project overview, no stack, no tasks, no credentials.

**Impact:** Fails Tier 1 requirement. Future sessions working on niu-vermilion get no orientation.

**Fix:** Write proper AGENTS.md for niu-vermilion covering: stack (Next.js 16, Supabase, TipTap), deploy status, directory structure, credentials needed, and current task status.

### 8. Cron Schedule Mismatches

**Spec says (final cron table, lines 634-643):**
| Cron | Spec Schedule | Actual |
|------|--------------|--------|
| remote-poller | every 30m | every 6h |
| health-checker | every 1h | every 6h |
| changelog-writer | every 1h | 20:00 daily |
| gitleaks-weekly | Sun 06:00 | Sun 08:00 |

**Impact:** Remote changes detected slower. Health dashboard data up to 6h stale. Changelog misses most changes (1 entry/day instead of 24).

**Note:** These may be intentional trade-offs for resource conservation on a dev machine. If so, the MASTERPLAN should be updated to document the actual schedules and the rationale.

---

## 🟡 Medium Findings

### 9. Profile Not Set on Most Crons

**Spec says (line 647-650):** Every cron MUST include `profile=opencode` to load .env credentials

**Reality:** Only `issue-bridge` has `profile=opencode`. The other 6 no_agent crons lack profile.

**Impact:** Credentials (GH_PAT, VERCEL_TOKEN) not automatically loaded. Some scripts may fail if they need these. Currently works because repos use SSH (not HTTPS) for git operations.

### 10. Health Checker Only Tests 3 of 10 Tier 1 URLs

**Spec says (daily heartbeat script logic):** Check all Tier 1 deploy URLs

**Reality:** `health-checker.sh` only checks 3 URLs (PemdiAcehTengah, Niu-LKH, kune-ya.com). Missing: TEDEO, niu-dash, niu-vermilion, Flame-ADE, niu-cast, Niu-Flow, brain

**Fix:** Add remaining Tier 1 URLs to the health check:
```bash
urls="https://tedeo.vercel.app https://pemdi-aceh-tengah.vercel.app \
      https://niumination.github.io/niu-dash https://niumination.github.io/Niu-LKH \
      https://kune-ya-com.vercel.app https://niu-vermilion.vercel.app"
```

### 11. Global Git Template at Profile-Specific Path

**Spec says:** Template at `~/.git-template/hooks/pre-commit`

**Reality:** `git config --global init.templateDir` points to `/Volumes/HermesAgent/HermesAgentUSB/data/profiles/opencode/home/.git-template`

**Impact:** If Hermes USB is mounted at a different path, all hooks break. Not portable.

### 12. SQL String Interpolation in kanban-sync.sh

**Spec says:** Script safety patterns mandate graceful degrade

**Reality:** SQLite queries use direct variable interpolation with sed-escaped single quotes. While source is controlled (BACKLOG.md), this pattern is fragile compared to prepared statements.

---

## ✅ OK — Correctly Implemented

- 10/10 Tier 1 sub-AGENTS.md exist (content quality varies)
- brain/templates/ — tier1, tier2, readme, daily templates exist
- brain/docs/ecosystem-changelog.md — 70 lines
- brain/logs/ — divergence + issue-bridge logs both present
- Global git template installed (30 lines, at working path)
- 10 cron jobs registered, all running
- gh auth — logged in as Niumination
- kanban.db — 107 tasks populated
- Niu-Dash ecosystem page — Kanban API + BACKLOG fallback works
- Issue labels — `ecosystem` + `tier-1` in 10/10 Tier 1 repos
- BACKLOG format — 50 tasks, 0 invalid
- All scripts have `mkdir`-based lock pattern
- All scripts use absolute paths
- pre-commit.template exists at scripts/

---

## Recommended Fix Order (Estimated 31 min)

1. **2 min** — Fix kanban-sync status mapping (`[~]` → in_progress)
2. **1 min** — Fix daily-heartbeat grep for `[~]`
3. **5 min** — Create `~/.gitleaks.toml` with custom rules
4. **10 min** — Update pre-commit hook: add DOX check + .env blocker + fix gitleaks path
5. **1 min** — Archive RAPI-RAPI-BESAR.md
6. **5 min** — Write proper niu-vermilion AGENTS.md
7. **2 min** — Update health-checker.sh with all Tier 1 URLs
8. **5 min** — Document schedule drift in MASTERPLAN or update cron schedules
