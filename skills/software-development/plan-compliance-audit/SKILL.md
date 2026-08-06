---
name: plan-compliance-audit
description: "Audit a running ecosystem against its written specification/plan document — check each layer (scripts, crons, hooks, configs, DB, credentials, docs) for compliance, categorize gaps by severity, and produce actionable fix recommendations."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [compliance, audit, plan, specification, gap-analysis, ecosystem-health]
    related_skills: [codebase-audit, project-orientation, systematic-debugging]
---

# Plan Compliance Audit

Audit a running system/ecosystem against its **written specification or master plan**. The spec document makes claims about what should exist, how it should behave, and what guarantees it provides. This skill systematically verifies each claim against the actual implementation.

## When to Use

- User asks "periksa kondisi terkini sesuai [document]" — check current state against a plan
- User says "cek apakah semua sudah di terapkan?" — verify full implementation
- User asks "cari anomali atau celah yang bisa merusak sistem" — find gaps that could break things
- Pre-launch readiness review against a design doc or roadmap
- Post-implementation compliance check after a multi-phase rollout
- Any time a formal specification or master plan exists and the user wants to know if reality matches it

### Auto-Trigger Phrases

These user messages are strong signals to load this skill:

- "pelajari apa tujuan [document] di buat" — learn the spec's purpose
- "cek kondisi terkini sesuai [document]" — compliance check
- "apakah semua sudah di terapkan?" — full implementation verification
- "apakah masih ada anomali atau celah" — gap/risk analysis
- "periksa semua konfigurasi yang telah di kerjakan" — config audit
- "apa yang bisa merusak sistem" — failure mode analysis

## Relationship to Other Skills

| Skill | Domain | Difference |
|-------|--------|------------|
| **codebase-audit** | Code quality | Reads every source file for bugs, security, architecture issues. This skill audits a **system against a plan**, not code for code's sake. |
| **project-orientation** | Situational awareness | Establishes what exists and where. This skill checks if what exists **matches what's specified**. |
| **systematic-debugging** | Bug investigation | Finds root cause of a specific bug. This skill finds **gaps between spec and reality** — not bugs per se, but missing pieces, misconfigurations, and plan violations. |

## Methodology — 5 Phases

### Phase 1: Understand the Specification

Read the specification/plan document fully before touching any part of the system. You cannot audit against a document you haven't absorbed.

**What to extract from the spec:**

1. **Purpose & Principles** — Why does this plan exist? What constraints does it encode? (e.g., SSOT, zero manual sync, survivability)
2. **Component inventory** — Every artifact the spec says should exist: scripts, cron jobs, config files, directories, templates
3. **Behavioral claims** — What each component should DO: parse format X, run on schedule Y, block commit Z
4. **Data flow claims** — Which way data moves: BACKLOG → kanban, kanban → dashboard, etc.
5. **Quality criteria** — Success criteria (SC1-SC10), verification methods, failure modes
6. **File references** — Every file path mentioned in the spec. These are your audit checklist.

**Action:**

```bash
# Read the full spec document
read_file(path="MASTERPLAN.md")  # or whatever the spec is named
```

> ⚠️ **Critical:** Read the ENTIRE document, not just the headings. Skip nothing. Specs often bury implementation details in later sections (edge cases, failure modes, prerequisites) that are essential audit criteria.

### Phase 2: Map Current State

For each claim in the spec, determine the **actual** state:

| Spec Claim | Reality | Source of Truth |
|------------|---------|-----------------|
| Should exist | Does it exist? | `ls`, `file_exists` |
| Should have content X | Does it have content X? | `read_file`, `grep` |
| Should run on schedule Y | Does it have a cron with schedule Y? | `cronjob action=list` |
| Should behave as Z | Does it behave as Z? | `terminal` to test, check logic |
| Should have config A | Is config A set correctly? | `cat config`, direct check |

**What to check for each component type:**

**Scripts:**
- Does the file exist? (check absolute path from spec)
- Does the first/lock pattern match the spec? (`mkdir`-based lock, `trap` cleanup)
- Does the logic match the spec's description? (status mapping, URL lists, error handling)
- Does the script reference the correct file paths and database locations?

**Cron jobs:**
- Is the cron registered? (`cronjob action=list`)
- Does the schedule match the spec?
- Is `no_agent=true` set as specified?
- Are `workdir` and `profile` set if the spec requires them?
- Has it ever run? (check `last_run_at`, `last_status`)

> ⚠️ **FOUR scheduler layers on a Hermes-portable Mac — never audit just `cronjob list`.** Scheduled jobs hide in four independent places; missing one layer means reporting "no crons" when jobs ARE running (exact mistake, 5 Agu 2026):
> 1. **Hermes cron** — `cronjob action=list` → `/Volumes/HermesAgent/HermesAgentUSB/data/cron/jobs.json` (source of truth; also read raw JSON for enabled/script/schedule details)
> 2. **macOS launchd agents** — `~/Library/LaunchAgents/com.*.plist` (NOT visible to cronjob list). Check `launchctl list | grep <keyword>`, plist files, AND `data/logs/launchd/<name>.log` — but see the log-mtime trap in `macos-daemon-lifecycle`: a fresh log proves a PAST run, not current activity. Verify activity in order: `launchctl list` → plist exists → `ps aux` → log mtime (historical only).
> 3. **User crontab** — `crontab -l` (completely invisible to Hermes cron + launchd). **READ THE FULL OUTPUT — never grep-filter it.** A `crontab -l | grep "gitleaks\|scripts"` check concluded "no crontab" while a real `0 */6 * * * ... skills/sync-to-agents.sh` entry was hidden by the narrow pattern. The entry's path was `skills/...` not `scripts/...`, so the grep missed it.
> 4. **GitHub Actions (cloud)** — `.github/workflows/*.yml` with `on: schedule:` cron expressions. Grep `schedule:` across workflow files; these run even when the Mac is off.
>
> Report each layer separately with its own active count. Scripts found on disk that are NOT registered in any of the four layers are "orphans" — flag but don't delete without asking.

**Configuration files:**
- Does the file exist? (credentials, gitleaks config, git template dir)
- Are the permissions correct? (`chmod 600` for .env)
- Does the content match what the spec defines?

**Git hooks:**
- Is the hook installed? (`find . -name pre-commit -path '*/.git/hooks/*'`)
- Does it contain all the checks the spec requires? (DOX check, .env blocker, gitleaks)

**Data integrity:**
- Does the database have expected data? (counts, status distribution)
- Do scripts correctly parse the data format they consume? (BACKLOG format → parser regex)
- Are there inconsistencies between what the spec claims and what the DB shows?

**Action:**

```bash
# Check all scripts exist
ls -la scripts/

# Check all cron jobs
cronjob action=list

# Check DB state
sqlite3 /path/to/kanban.db "SELECT COUNT(*), COUNT(DISTINCT status), COUNT(CASE WHEN status='in_progress' THEN 1 END) as active FROM tasks;"

# Check git hooks
git config --global init.templateDir
find /project/root -name 'pre-commit' -path '*/.git/*' | wc -l

# Check config files
ls -la ~/.gitleaks.toml
ls -la ~/.hermes/profiles/*/.env
```

### Phase 3: Cross-Reference Claims vs Reality

This is the core gap-finding phase. For EVERY claim in the spec, compare against Phase 2's reality.

**Common gap categories:**

| Category | Spec Says | Reality | Severity |
|----------|-----------|---------|----------|
| Missing file | `scripts/generate-X.sh` should exist | File doesn't exist | 🟠 High |
| Broken logic | Script parses `[~]` as in_progress | Script parses `[o]` instead | 🔴 Critical |
| Incomplete hook | Hook has 3 checks (DOX, .env, gitleaks) | Hook has only 1-2 checks | 🔴 Critical |
| Schedule drift | Cron runs every 30m | Cron runs every 6h | 🟠 High |
| Missing config | `~/.gitleaks.toml` with custom rules | File doesn't exist | 🔴 Critical |
| Missing docs | Project DOX should be N+ lines | DOX is 5 lines of comments | 🟠 High |
| Stale file | File should be archived | File still at root | 🟡 Medium |
| No credential load | Cron should set `profile=opencode` | Cron has no profile | 🟡 Medium |

**Check each spec section against reality:**

```
For each layer/section in the spec:
  For each component mentioned:
    - Does it exist? (filesystem)
    - Does it work? (test execution, parse logic)
    - Does it match spec? (content, schedule, config)
    - Does it integrate correctly? (data flow, dependencies)
```

### Phase 4: Categorize Findings by Severity

Every gap gets a severity based on **potential impact**:

| Severity | Label | Criteria | Response |
|----------|-------|----------|----------|
| 🔴 Critical | `critical` | Can cause data loss, silent failure of core feature, security breach, or system-wide breakdown | Fix immediately |
| 🟠 High | `high` | Significant deviation from spec that reduces functionality or exposes risk, but doesn't break the whole system | Fix next |
| 🟡 Medium | `medium` | Non-critical deviation — different behavior than specified, missing convenience feature, incomplete but functional | Fix when convenient |
| 🟢 Low | `low` | Cosmetic — different schedule than spec but reasonable, file in wrong location but works, sparse doc | Fix if worth it |
| ✅ OK | `ok` | Matches spec exactly | Note and move on |

**Framing rule:** Never categorize based on your opinion of the spec's correctness. Categorize based on **what the user asked**: "cari celah yang bisa merusak sistem." A script that silently ignores 12 active tasks IS critical — it breaks monitoring, notifies nothing, and the user thinks everything is fine.

### Phase 5: Execute Fixes (Root Cause, Not Symptoms)

Executing fixes is NOT optional after finding gaps. The user's expectation is: find the gaps, fix them thoroughly, then re-audit to confirm closure. Repeat until zero gaps remain.

**Core principle — "Jangan menambal kesalahan, perbaiki semua dengan teliti":**
- Fix the **root cause**, not the symptom
- A parser that silently misreads 12 active tasks isn't fixed by manually updating the DB — you fix the **parser regex**
- A missing config file isn't fixed by bypassing the check — you **create the file**
- A broken hook isn't fixed by disabling it — you **add the missing checks**

**Fix execution rules:**

1. **Surgical patches only** — never rewrite entire files unless the user explicitly requests it
2. **One gap at a time** — apply a fix, verify it works, then move to the next
3. **Verify after each fix** — re-run the relevant script, re-check the data, confirm the gap is closed
4. **Document device-specific workarounds** — If a script needs to check two possible paths (e.g., `~/.gitleaks.toml` AND `/Users/zaryu/.gitleaks.toml`) because of Hermes container vs host filesystem differences, capture the rationale in a comment

**Common fix techniques from real audits:**

**Bash subshell counters:** Don't use `grep ... | while read count` — the pipe creates a subshell and variable increments are invisible to the parent shell. Use temp files instead:
```bash
# ❌ WRONG — counter stays 0 after the loop
count=0
grep ... | while read line; do
    count=$((count + 1))
done
echo "$count"  # always 0

# ✅ CORRECT — use temp file for subshell-safe counting
tmp=$(mktemp)
echo 0 > "$tmp"
grep ... | while read line; do
    c=$(<"$tmp"); echo $((c + 1)) > "$tmp"
done
count=$(<"$tmp")
rm -f "$tmp"
```

**`grep -c || echo 0` double-zero bug:** `grep -c` prints `0` AND exits 1 when no match — so `total=$(grep -c ... || echo 0)` yields `"0\n0"` and `$((total - ...))` throws `syntax error in expression (error token is "0")` (hit twice on 5 Agu 2026: `changelog-writer.sh`, `daily-heartbeat.sh`). Fix: capture grep's own output, then default with `${var:-0}`:
```bash
# ❌ WRONG — variable becomes "0\n0"
total=$(grep -cE 'pattern' file 2>/dev/null || echo 0)

# ✅ CORRECT — grep already prints 0 on no-match; only default when output is EMPTY
total=$(grep -cE 'pattern' file 2>/dev/null)
total=${total:-0}
```

**Pre-commit hook deployment:** `git init` and `git clone` read templateDir, but do NOT overwrite existing hooks in already-cloned repos. To force-deploy to existing repos:
```bash
# For each existing repo:
cp -f "$TEMPLATE/pre-commit" "$REPO/.git/hooks/pre-commit"
chmod +x "$REPO/.git/hooks/pre-commit"
```

**Config file path resolution:** In Hermes container context, `~` may resolve to `/Volumes/HermesAgent/...`, not the macOS host home. Always provide fallback paths:
```bash
# Check both paths
for try_path in "$HOME/.gitleaks.toml" "/Users/zaryu/.gitleaks.toml"; do
    [ -f "$try_path" ] && CONFIG="$try_path" && break
done
```

### Phase 6: Re-Audit (Close the Loop)

After executing ALL fixes, **re-run the full audit** to confirm every gap is closed.

**Why this matters:** Fixes can interact, regress, or miss edge cases. The only way to confidently say "zero gaps" is to re-check every spec claim against the new reality.

**Re-audit checklist:**

1. Re-read every patched file — confirm the fix is syntactically correct and logically sound
2. Re-run every changed script — confirm expected output (counts, statuses, file generation)
3. Re-check the database — confirm data has the correct distribution
4. Re-query the system — do crons list with correct schedules? Are hooks installed in all repos?
5. Re-check the original spec claims — all of them, not just the ones you fixed

**Report the re-audit as:**

```
## Re-Audit Results

| Gap | Status | Notes |
|-----|--------|-------|
| 🔴 Gap 1: [title] | ✅ Fixed | [verification evidence] |
| 🟠 Gap 2: [title] | ✅ Fixed | [verification evidence] |
| 🟡 Gap 3: [title] | ✅ Fixed | [verification evidence] |
| ✅ All | 15/15 closed | [summary] |
```

**Zero gaps is the only acceptable outcome.** If any gaps remain (even 🟡 Medium), continue the fix → re-audit loop.

### Phase 7: Sync Documentation

After all fixes are verified, update every surface that references the spec or ecosystem state. This prevents the "fixed but not documented" gap — the most common post-audit failure.

| Surface | What to update |
|---------|---------------|
| **BACKLOG.md** | Mark fixed items ✅ with count. Update scoreboard (e.g. "15/15 gaps closed"). Update HEAD hash. |
| **AGENTS.md** | Bump DOX version. Update phase status. Update the ecosystem directory tree if files changed. |
| **MASTERPLAN (or spec doc)** | If fixes changed behavior vs spec table, update the spec to match reality. |
| **Cron jobs** | If new scripts were created, register crons. If schedules changed, update them. |
| **Kanban DB** | Re-sync after BACKLOG changes. Verify status distribution matches reality. |
| **Memory** | Update memory with new HEAD, completed fixes, and any new stable facts. |

---

### When the User's Preferred Workflow Is Two-Phase (Report First, Fix Later)

Some users want a clean "cek dulu → betulin sekarang" split. If so:
1. Phase 1-5: Report findings only — no fixes, no judgement
2. Ask: "Mau aku perbaiki semua, atau prioritasin yang critical dulu?"
3. After user decides, execute Phase 6-7

But if the user's instructions combine the two (e.g., "Perbaiki semua terus audit lagi, kalau masih ada celah, lanjut perbaiki lagi sampai semua bersih tanpa celah"), go straight to fix-and-re-audit loop.

---

## Reference Examples (from a real audit)

For a detailed worked example of this methodology applied to a 936-line master plan with 10 crons, 11 scripts, and 28 projects, see `references/real-audit-findings.md`. The reference includes:
- Critical status-mismatch bug (`[~]` vs `[o]` in parser scripts)
- Pre-commit hook missing spec-required checks (DOX, .env)
- Missing security config (`~/.gitleaks.toml`)
- Files referenced in spec but absent from filesystem
- Incomplete Tier 1 documentation (5-line AGENTS.md)
- Cron schedule drift from spec
- Credential profile gaps

For a worked example of the full fix → re-audit → document loop (15 gaps closed across 4 layers), see `references/iterative-audit-loop.md`. Includes:

For **inventory cross-reference** — comparing a declared project listing (PROJECTS array, README table, JSON manifest) against the actual live inventory (GitHub API repos + filesystem) to find missing projects, stale entries, and duplicates — see `references/inventory-cross-reference.md`. This covers the normalization rules, GitHub API pagination, and duplication detection needed when auditing a 70+ project dashboard.
- Re-audit report showing all gaps with ✅/❌ status after fixes
- Post-fix kanban verification (status counts before vs after)
- Cron alignment table before vs after
- Pre-commit hook deployment to 20 repos
For a **post-implementation feature compliance audit** — verifying recently-built dashboard/feature code against a MASTERPLAN roadmap and TECHSPEC — see `references/post-implementation-feature-audit.md`.
For **org-wide GitHub PR detection** as one phase of an ecosystem status check — single `gh search prs --owner` query (no per-repo loops), draft/stale flagging, and the Hermes-env `$HOME` auth fix — see `references/org-wide-pr-detection.md`.

## Pitfalls

### ❌ Skipping the spec read
You cannot audit against a document you haven't fully read. The spec's appendices, footnotes, and edge-cases sections often contain essential audit criteria. Read the ENTIRE document.

### ❌ Confirming existence without checking behavior
A script file exists but might parse the wrong format. A cron is registered but might have the wrong schedule or missing profile. "It exists" is not the same as "it works as specified." Always verify behavior for at least the critical components.

### ❌ Not checking data integrity
A parser that silently maps 12 active tasks to "todo" is worse than a missing file — it creates the illusion of working while quietly losing data. Always check downstream effects: "if this script runs, does the database have the expected state?"

### ❌ Assuming the spec is correct
The spec may itself contain errors, stale version numbers, or impossible requirements. When reality differs from the spec, distinguish between:
- **Spec violation** — the implementation is wrong (should fix)
- **Spec drift** — intentional deviation that should update the spec (document it)
- **Spec error** — the spec asks for something impossible or contradicts itself (flag it)

### ❌ Only checking primary sections
Skip sections like "Edge Cases & Failure Modes", "Prerequisites Checklist", and "Appendix" at your peril. These often reference files, configs, or behaviors that don't exist because "they're just in an appendix."

### ❌ Missing the downstream data flow
A parser bug doesn't just affect that one script. It cascades:
- Script A misparses → kanban DB has wrong data → dashboard shows wrong stats → user gets wrong information → alert systems don't fire → issues go unnoticed

Trace the full chain for each critical finding.

### ❌ Reporting without fix recommendations
The user asked "cari celah" AND expects to know what to do about them. Every finding needs a concrete, actionable fix recommendation — not just a description of the problem.

### ❌ Fixing symptoms instead of root causes ("menambal kesalahan")

The user explicitly said *"jangan menambal kesalahan, perbaiki semua dengan teliti"* — don't patch over errors, fix everything thoroughly. This means:

- If a parser misreads `[~]` as `[o]`, don't just rename the kanban statuses to match the broken parser — fix the **parser** to match the spec
- If a config file is missing, don't just hardcode a safe default — **create the file** with the correct content
- If a cron has the wrong schedule, don't just note it in the report — **update the cron**

**Test for symptom-fixing:** Ask yourself "If I apply this fix and run the full audit again, will this specific gap still appear?" If yes, you're fixing a symptom, not the root cause.

### ❌ Not iterating — stopping after one fix round

The user expects the fix → re-audit loop until **zero gaps remain**. Stopping after "all critical gaps fixed" when medium gaps exist is premature unless the user explicitly asked to prioritize. Complete the full loop.

### ❌ Forgetting pre-existing user context
If the user has a preferred two-phase workflow ("cek dulu" → "betulin sekarang"), report findings first, let them decide which to fix, then execute. Don't fix-and-report in one step unless explicitly asked.

## Related Skills

- `codebase-audit` — For auditing code quality specifically (bugs, architecture, security in source code)
- `project-orientation` — For establishing what exists before starting work
- `systematic-debugging` — For root-causing a specific bug found during audit
- `writing-plans` — For writing the implementation plans that this skill later audits
- `ecosystem-state-sync` — Standalone doc sync without a prior audit. Use when user asks "cek status ekosistem" or "update semua dokumentasi".
