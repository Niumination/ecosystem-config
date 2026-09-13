---
name: ecosystem-bulk-push
description: "Use when pushing many ecosystem repos to GitHub at once."
tags: [ecosystem, git, github, push, niumination]
---

# Ecosystem Bulk Push

Push many repos under `~/Desktop/Niumination/` to GitHub in one run without pushing
anything that should not move: third-party upstreams, untracked work, or dirty WIP.

## When to Use

- User says "update semua repo ke github" / "push everything" or names several repos at once.
- Any bulk `git push` spanning more than two repos.

## Workflow

### 1. Brief before executing

State the push set and the exclusion set in one short message before running any
push. A bulk command cannot carry per-repo intent, so the user must see what moves
and what stays.

### 2. Audit every repo read-only first

```bash
cd ~/Desktop/Niumination
for d in $(find . -maxdepth 3 -name .git -type d | sed 's|/.git||;s|^\./||' | sort); do
  b=$(git -C "$d" branch --show-current 2>/dev/null)
  s=$(git -C "$d" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  u=$(git -C "$d" remote get-url origin 2>/dev/null || echo NO_REMOTE)
  ah=$(git -C "$d" rev-list --count '@{u}..HEAD' 2>/dev/null || echo ?)
  bh=$(git -C "$d" rev-list --count 'HEAD..@{u}' 2>/dev/null || echo ?)
  echo "$d | br=$b | dirty=$s | ahead=$ah behind=$bh | $u"
done
```

Inspect the ahead commits (`git log --oneline '@{u}..HEAD'`) and the dirty files
(`git diff --stat`) of every candidate before pushing — push only what you have
actually reviewed.

### 3. Push only the safe set

- Push ONLY repos with ahead>0 on remotes owned by the user's org, with plain
  `git push` (never force). A non-fast-forward reject is a safe stop, not an
  error to override.
- Commit selectively (`git add <files>`, never blind `git add -A`) and only files
  whose content you verified; each commit carries a clear message.

### 4. Exclude and report — never touch

- Remotes owned by third parties (upstream forks of someone else's project).
- Repos with no upstream tracking (`ahead=?`) — do not attach tracking unasked.
- Dirty WIP the user has not approved for commit — report the file list, leave it.
- Repos that are fully in sync — say so, skip them.

### 5. Prove every push

`git log --oneline '@{u}..HEAD'` must return empty afterward. `gh repo create
--push` leaves an HTTPS remote even under an SSH policy — set-url to SSH
immediately after the first push, then re-verify.

## Pitfalls

- **Never auto-commit inside a bulk run** — a bulk push moves already-reviewed
  commits only, because one command cannot know the intent behind each repo's
  uncommitted work.
- **`ahead=?` means no upstream, not zero commits** — rev-list fails without a
  tracking ref; check `git status -sb` before concluding a repo is clean.
- **Dirty working tree does not block a push** — push moves commits, not files;
  say explicitly which dirty files stayed local.
