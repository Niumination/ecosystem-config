---
name: finishing-a-development-branch
description: "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work — merge, PR, keep, or discard."
domain: software-development
subdomain: sdlc
tags: [branch, merge, pr, cleanup, workflow, integration]
version: "1.0"
author: obra/superpowers + Niumination
source: superpowers
license: MIT
---

# Finishing a Development Branch

> **Sumber:** Diadaptasi dari `obra/superpowers` (MIT).

**Core principle:** Verify tests → Detect environment → Present options → Execute choice → Clean up.

**Integrasi Niumination:** Post-coding workflow setelah `subagent-driven-development` atau `executing-plans`. Menutup loop SDLC dari ide → desain → plan → code → review → merge.

**Announce:** "Saya menggunakan finishing-a-development-branch skill untuk menyelesaikan pekerjaan ini."

## Step 1: Verify Tests

Run full test suite. **Jika gagal:** report failures dan stop.

## Step 2: Detect Environment

```bash
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null && pwd -P)
GIT_COMMON=$(git rev-parse --git-common-dir 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

## Step 3: Determine Base Branch

Base branch adalah fork point. Tanya user jika tidak jelas.

## Step 4: Present Options

**Normal repo / named-branch worktree:**
```
1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
```

**Detached HEAD (2 options):**
```
1. Push as new branch and create a Pull Request
2. Keep as-is
```

## Step 5: Execute Choice

**Option 1 — Merge Locally:**
```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
# Run tests on merged result
# If green: cleanup worktree, delete branch
```

**Option 2 — Push and PR:**
```bash
git push -u origin <feature-branch>
# Create PR via forge CLI
```

**Option 3 — Keep:**
Report branch name and path.

**Discard (hanya jika user eksplisit minta):**
```bash
git branch -D <feature-branch>
# Cleanup worktree
```

## Step 6: Cleanup Workspace

- `.worktrees/` atau `worktrees/` — superpowers created it, we own cleanup
- Lainnya — leave in place

## Quick Reference

| Option | Merge | Push | Keep Worktree | Delete Branch |
|--------|-------|------|---------------|---------------|
| 1. Merge | yes | - | - | yes |
| 2. PR | - | yes | yes | - |
| 3. Keep | - | - | yes | - |
| Discard | - | - | - | yes (force) |

## Integrasi Ekosistem

| Skill | Hubungan |
|-------|----------|
| `subagent-driven-development` | **Input:** task execution selesai |
| `executing-plans` | **Input alternatif:** execution selesai |
| `requesting-code-review` | Final review sebelum finish |
| `verification-before-completion` | Tests must pass sebelum opsi disajikan |
