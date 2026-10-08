# Probing upstream without disturbing the running checkout

When the gateway (or any service) is running from the checkout you are about to reconcile, you
cannot swap branches to inspect upstream. Read upstream through git objects instead.

## Cheap reads — no working tree needed

```bash
git show upstream/main:<path> | grep -n '<symbol>'        # one file, no checkout
git show upstream/main:<path> | head -30                   # read a docstring in place
git ls-tree -r upstream/main --name-only | grep '<dir>'    # does the path exist upstream
git diff --numstat <merge-base> upstream/main -- <file>    # how much upstream churned this file
```

These are read-only and safe under a live process. Use them for the first pass: they answer
"does upstream have this symbol / does the file still exist / how big is the conflict surface".

## A real tree — `git worktree`, not `git checkout`

Some questions need the upstream tree on disk: running upstream's own test suite, resolving
imports, or reading several files in context.

```bash
git worktree add /tmp/<name>-upstream-test upstream/main
# ... probe ...
git worktree remove /tmp/<name>-upstream-test
```

`git worktree add` creates a second checkout at a detached HEAD **without touching the branch the
service is running from**. Verify that after the add:

```bash
git log -1 --format="%h %s" <running-branch>   # unchanged
git status --short                              # still only your own dirt
```

Running a test suite from inside the worktree is how you confirm what upstream actually pins —
see the CONTRADICTED state in SKILL.md. A symbol grep tells you a mechanism exists; only the
test tells you which policy it enforces.

## Sequence the work by risk, and front-load the non-destructive half

Split the reconciliation into two halves and run the safe half first:

| Safe (do first, no approval needed) | Destructive (owner-gated) |
|---|---|
| create + push a recovery tag for the running branch | rebase / merge carried patches |
| `git worktree add` and probe upstream | swap the branch the service runs from |
| classify every carried patch | force-push the remote branch |
| run upstream's suite in the worktree | restart the service |

The safe half is not busywork — it usually produces the decisive finding. Classifying patches
against upstream's current code and its tests is what determines *which* patches survive, so doing
it first means the destructive step is planned against measured facts instead of assumptions, and
the owner's decision is informed rather than speculative.

Confirm the recovery point is on the **remote** before the destructive half starts; a local-only
tag does not survive the machine it sits on. See `references/fork-reconciliation-safety.md`.

## Pitfalls

- **A full `git fetch` on a large upstream takes minutes and will exceed a foreground timeout.**
  Run it in the background with completion notification and measure after it lands; retrying in the
  foreground with a bigger timeout waits exactly as long.
- **Do not `git checkout upstream/main` to look around** in a checkout a service is running from.
  It rewrites files on disk under a live interpreter. Use `git show`, `git ls-tree`, or a worktree.
- **Do not sweep every ref looking for a symbol.** `for-each-ref` over thousands of remote branches
  blows past any timeout. Query the specific refs that can hold the content.
- **Remove the worktree when done.** A stale worktree keeps a full tree on disk and can confuse a
  later `git worktree`/branch operation.
