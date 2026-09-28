---
name: github-upstream-pr-from-fork
description: "Use when a fix must reach upstream from a diverged clone."
version: 1.0.0
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [git, fork, upstream, pull-request, cherry-pick, diverged-history]
    related_skills: [github-pr-workflow, external-pr-audit, niumination-ecosystem-change-discipline]
---

# Upstream PR from a Diverged Local Clone

## When this applies

The working clone holds a long local-only history (local refactors and patches) and sits both
ahead of and behind its own fork, or the file you fixed exists only in the local tree because
the refactor that created it was never pushed. Pushing the branch is rejected as
non-fast-forward, and the fix cannot be cherry-picked onto the fork because its base does not
contain the file.

Keep the local-only commits on the local branch. They carry deliberate local patches that
survive updates only because they are not published. Send the upstreamable fix as a PR instead
of force-pushing.

## Procedure

### 1. Read the topology before touching anything

```bash
git fetch origin
git log --oneline @{u}..HEAD | cat      # ahead: local-only work
git log --oneline HEAD..@{u} | cat      # behind: what landed on the fork
git rev-list --count @{u}..HEAD
git rev-list --count HEAD..@{u}
```

If ahead is in the hundreds or thousands, do not rebase and do not attempt to push the branch.
A commit that already exists on the fork under a different hash means the histories diverged,
not that the local work is missing.

### 2. Find the ref that actually contains your file

A fork has two upstreams: the project and your own fork. Check both for the file you edited:

```bash
git ls-tree upstream/main path/to/dir --name-only | wc -l
git show upstream/main:path/to/file.py >/dev/null && echo ADA || echo TIDAK
git show origin/main:path/to/file.py  >/dev/null && echo ADA || echo TIDAK
```

The PR must target whichever ref has the file. If the fork lacks it and the project has it,
the PR goes to the project and the base is the project ref, not your fork.

### 3. Build the branch from that base, never from local main

```bash
git checkout -B pr/<slug> upstream/main
git cherry-pick <fix-commit>
```

Do not use `git reset --soft <base>` on a branch carrying local-only history: the diff then
spans the entire ahead-history instead of the fix, because the base has none of those files.
Recover with `git reset --hard <original-head>` — the commits are still on the branch you came
from. Note the original head before starting.

### 4. Prove the diff is the fix and nothing else

```bash
git diff upstream/main..HEAD --name-only
git diff upstream/main..HEAD --stat
```

More than one file means the cherry-pick landed on the wrong base. Discard and redo from
step 3. Re-read the changed constants or lines in the branch copy — a cherry-pick onto a moved
base can apply cleanly and still leave stale values.

### 5. Run the project's test entrypoint on the branch, not on main

A fix that only ever ran on local main proves nothing about the base it will be reviewed
against.

### 6. Push the branch, then open the PR against the other remote

```bash
git push -u origin pr/<slug>
gh pr create --repo <project-owner>/<repo> --head <your-fork>:<slug> --base main \
  --title "<imperative subject>" --body-file -
```

Auth: a stale `GITHUB_TOKEN` in the environment makes `gh` and the REST API fail with a
silent 401 even when a working token exists. Unset it and load the good one:

```bash
unset GITHUB_TOKEN
export GH_TOKEN=$(grep -E '^GH_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
```

## Writing the body

- Symptom, cause, fix, test counts, each with the command that produced it.
- Report only measurements taken against the code path the PR changes. Host-specific timings,
  host-specific version numbers, and incident dates read as verified claims the reviewer cannot
  reproduce — keep them out of the body and in your own notes.
- When a different root cause exists for the same symptom and your change is only a guard,
  say so plainly, name the fix for the real cause, and offer to narrow or drop the change. A
  maintainer may prefer the other layer, and saying so up front costs less than a rejected PR.
- Keep the subject imperative and scoped: what changes, not which session produced it.
