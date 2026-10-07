# Reconciling a diverged fork safely

Before any operation that can drop commits from the fork (`--force`, `--force-with-lease`, branch
reset, remote branch delete), prove that nothing on the remote is a sole copy. "Non-ancestor" and
"unique content" are different questions.

## Step 1 — Classify each remote-only commit

```bash
git log --oneline --format="%h %s" main..origin/main
```

For each one, ask two separate questions:

1. **Is its payload already re-implemented locally?** A port counts. When upstream decomposes a god
   file, a patch written against the old file may have been re-applied to the new sibling — the local
   commit supersedes the remote one functionally, even though git sees them as unrelated.
   `git show <local-sha> --stat` next to `git show <remote-sha> --stat` exposes this: same feature,
   different target file.
2. **Does it carry files the local branch never received?** This is the question that bites. A commit
   can be *partly* superseded: its code change ported, while auxiliary files (scripts, docs, setup
   bundles) were dropped in the port and exist nowhere else.

## Step 2 — Hunt for sole copies with `ls-tree`, not `git log`

Commit subjects lie about scope. Check the actual trees:

```bash
git ls-tree -r <ref> --name-only | grep -c "path/to/dir"
```

Run it against every candidate ref — local branch, remote branch, `upstream/main`, and the
merge-base — to locate which ref is the only holder:

```bash
git ls-tree -r main          --name-only | grep -c "scripts/portable-setup"
git ls-tree -r upstream/main --name-only | grep -c "scripts/portable-setup"
git ls-tree -r origin/main   --name-only | grep -c "scripts/portable-setup"
git ls-tree -r $(git merge-base main origin/main) --name-only | grep -c "scripts/portable-setup"
```

A `0 / 0 / 5 / 0` result means the remote ref is the sole holder of five files — a force-push would
erase the only copy.

Sweeping *all* refs (`for ref in $(git for-each-ref ...)`) is tempting but scales badly: a repo with
thousands of remote branches will blow past any reasonable timeout. Check the handful of refs that
can actually hold the content — local branch, the remote branch being overwritten, upstream, and the
merge-base — and stop.

## Step 3 — Preserve to the REMOTE before anything destructive

A local backup branch is not preservation if the risk is losing remote state, and it is not
preservation at all if the machine is the thing that fails.

```bash
git branch <backup-name> origin/main
git push origin <backup-name>
git ls-remote origin refs/heads/<backup-name>    # confirm the SHA landed
```

Name it for what it holds (`backup-<remote>-<ref>-<yyyymmdd>`), so a future session recognises it as
insurance rather than abandoned work. Once it is on the remote, the force operation is fully
reversible and the approval conversation gets much shorter.

## Step 4 — Choose force-push over merge when the checkout is live

The instinct is to avoid a force-push by merging the remote branch in locally. That is often the
*worse* option when a gateway or service is running from the checkout:

- `git merge` rewrites files **on disk**, under a live process, with no restart coordination. A
  half-applied tree under a running interpreter is how you get import errors at the next tool call.
- A force-push touches **only the remote**; the working tree the process is running from is untouched.
- A merge also drags in the superseded remote commit, re-introducing the ported patch — the exact
  "two patches touching one function" conflict that reconciliation is supposed to remove.

So: preserve (Step 3), then force-push. Use `--force-with-lease`, never bare `--force` — the lease
refuses the push if the remote moved since your last fetch, which is the only guard against
clobbering someone else's push.

## Step 5 — State plainly what the push does NOT achieve

Pushing the local branch to the fork does **not** enable upstream updates. If the branch still carries
local-only commits, the updater keeps skipping upstream sync — the condition is unchanged by the push.
Say so explicitly, so the owner does not read "fork synced" as "updates flowing again". Reconciling
with upstream is a separate, later operation with its own risk profile.

## Pitfalls

- **Non-ancestor does not mean unique.** A remote commit can be functionally superseded while still
  holding files that exist nowhere else. Classify payload and files separately.
- **A merge-base file count of zero proves nothing about the remote branch.** Query each ref
  individually; the merge-base and upstream are different trees from the remote head.
- **A commit that was "already ported" may have been ported only in part.** Diff the file *lists*, not
  the subjects, before trusting the port.
- **Never force-push before the backup branch is confirmed on the remote.** A local-only backup dies
  with the machine and does not survive a bad push on a shared repo.
- **Do not sweep every ref looking for sole copies.** Bound the search to refs that can hold the
  content; an unbounded `for-each-ref` walk over thousands of branches will time out.
