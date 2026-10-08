# Merging a branch that has gone stale

A reconciliation branch is a snapshot of the day it was rebased. Upstream keeps moving, so
"it exists in my branch" never means "it is the current version" — and merging a stale branch
imports stale code, including files upstream has since fixed.

## Measure staleness before proposing the merge

```bash
git rev-list --count <rebase-base>..upstream/main      # commits upstream gained since

git log --oneline <rebase-base>..upstream/main -- <file>   # did upstream touch the file?
git cat-file -s <branch-blob>                             # compare against upstream's
```

If upstream touched the same file after the rebase, the branch copy is behind. Do not merge it
as-is; re-rebase first, or you ship the older revision under a newer-looking commit.

## A carried file can be OLDER than upstream's

Two branches both containing a path says nothing about which is current. Confirm by size and
diff, not presence:

```bash
git cat-file -s $(git rev-parse upstream/main:<file>)
git cat-file -s $(git rev-parse <branch>:<file>)
git diff upstream/main <branch> -- <file>
```

A smaller blob plus a diff that only *removes* logic is the signature of a branch that
predates upstream's fixes to that file.

## Cherry-picking a single file rarely works

A file that carries its own dependencies cannot move alone. Check its imports against the
target branch before offering "just cherry-pick the file" as the fast path:

```bash
git show <branch>:<file> | grep -n "^from \|^import "
git ls-tree <target-branch> -- <package>/ | wc -l     # 0 → the import will fail
```

An absent package means `ModuleNotFoundError` at import, not a merge conflict — a failure that
surfaces only when something runs.

## Rules

- **Report staleness as a number.** "The branch is 1,157 commits behind upstream" is actionable;
  "the branch may be stale" is not.
- **Re-rebase before merging, or say plainly that the merge ships older code.** Do not present a
  stale merge as equivalent to a fresh one.
- **Verify a file's currency by diff, never by existence.** `git ls-tree` proves presence only.
