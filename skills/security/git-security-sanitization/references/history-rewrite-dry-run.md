# History Rewrite — Dry Run and Verification

Use when redaction in a new commit is not enough: the leak must disappear from history, which means
rewriting every commit that carries the blob and force-pushing. This is irreversible without a backup,
so the sequence is: back up → test on a throwaway clone → verify → apply → force-push with lease →
re-verify remotely.

## 1. Backup (non-negotiable)

```bash
git clone --mirror <repo> /tmp/<repo>-mirror.git
tar -czf /tmp/<repo>-git.tgz -C <repo> .git
# sanity: both must print the same SHA
git --git-dir=/tmp/<repo>-mirror.git rev-parse HEAD
git -C <repo> rev-parse HEAD
```

The backup *is* a copy of the leak: it holds the pre-rewrite history with the secret in it. Keep it
only until the rewrite is verified end-to-end, then delete both artifacts and say so — a forgotten
mirror in `/tmp` leaves the credential on disk after the repo was cleaned. Same for the patterns file:
write it outside the repo, mode 600, delete it when the run is done.

## 2. Test on a throwaway clone

`git filter-repo` refuses to run on a clone that has already been used; clone fresh from the mirror.
It also removes the `origin` remote from the rewritten clone, which is a useful safety property — a
test rewrite cannot be pushed by accident.

```bash
git clone /tmp/<repo>-mirror.git /tmp/test-rewrite
cd /tmp/test-rewrite
git ls-tree -r HEAD > /tmp/tree-before.txt        # baseline for the comparison below
```

Build the patterns file in a script, not on the command line, and keep it mode 600. `--replace-text`
takes lines of `<old>==><new>` (no prefix = literal match).

```bash
chmod 600 /tmp/redact-patterns.txt
git filter-repo --replace-text /tmp/redact-patterns.txt --force
```

Two modes, and the choice changes what "success" looks like afterwards:

| Mode | Use for | Commits |
|---|---|---|
| `--replace-text <patterns>` | a value to scrub wherever it appears | unchanged |
| `--path <file> --invert-paths` | a file that must never have existed at all | drops by the commits left empty |

`--invert-paths` is the right mode for a leaked `.env` or key file: the whole path is removed from
every commit, and a later commit whose only content was "remove this file from tracking" becomes empty
and is pruned — so a dropping commit count is expected there, not a failure. Confirm with
`git log --all --oneline -- <path>`, which must return nothing.

On a repo of a few hundred commits and tens of MB this takes seconds.

## 3. Verification checklist

Run all of these on the throwaway clone. Any failure means stop and restore from the mirror.

| Check | Expected |
|---|---|
| path count before vs after | identical (no file lost, none invented) |
| blobs that differ | only the files you intended to redact |
| `160000` gitlink count + `.gitmodules` | unchanged / still present |
| old blob reachable | `git cat-file -e <old-blob>` must FAIL |
| pattern occurrences in worktree | 0, with the redaction marker present |
| commit count | unchanged with `--replace-text`; with `--invert-paths` it drops by exactly the commits that became empty |
| all-history blob scan | 0 leaks, including deleted files and separator-formatted variants |

Scan every blob, with no size cap — a filter that skips large blobs exempts them silently and a leak
can sit inside a multi-MB archive blob. If you did cap the scan, re-scan the skipped set explicitly
before calling history clean.

Comparing trees needs the blob SHA included in the key; a comparison built from `mode`+`type` alone
reports "nothing changed" even when a blob was replaced:

```python
lines = sorted("\t".join(l.split()[:3]) + "\t" + l.split("\t", 1)[1] for l in ls_tree_output.splitlines())
#                      ^^^ mode, type, sha  — [:2] drops the sha and blinds the check
```

## 4. Why more SHAs change than the files you touched

`git filter-repo` strips `gpgsig`/`mergetag` from signed commits. Any merge performed through a web UI
is signed, so that commit's hash changes even though its tree, parents, author, and committer are
byte-identical — and every descendant's hash then changes by parent chaining. Confirm this per commit
by diffing the raw commit objects: identical `tree` and `parent` lines with a missing `gpgsig` block is
the signature of this effect, not of a content change.

```bash
# earliest changed commit, then its descendant count
git --git-dir=/tmp/<repo>-mirror.git log --reverse --format=%H | head -1
# mapping old->new for every commit lives here:
cat /tmp/test-rewrite/.git/filter-repo/commit-map
# verify the set: every changed SHA should be a descendant of the earliest one
python3 - <<'PY'
import subprocess
M = "/tmp/<repo>-mirror.git"
mapping = dict(l.split() for l in open("/tmp/test-rewrite/.git/filter-repo/commit-map").read().splitlines()[1:] if len(l.split()) == 2)
changed = [o for o, n in mapping.items() if o != n]
earliest = min(changed, key=lambda s: len(subprocess.run(["git", "--git-dir", M, "rev-list", "--count", s], capture_output=True, text=True).stdout))
desc = sum(subprocess.run(["git", "--git-dir", M, "merge-base", "--is-ancestor", earliest, o]).returncode == 0 for o in changed)
print(f"changed={len(changed)} descendants_of_earliest={desc}")
PY
```

Report the real number to the user before pushing. A rewrite whose blast radius is "16 commits" when it
is actually "all descendants of a signed merge" changes what they may need to fix afterwards.

Blast radius only matters if something points at those SHAs. Before recommending a rewrite at all, count
references to the repo's short SHAs across the ecosystem's docs and reports
(`grep -rEo "<sha1>|<sha2>|<sha3>" --include="*.md" .`): zero references is what makes a rewrite cheap, and
it is worth stating to the user; a non-zero count means every reference must be updated and the user may
prefer a different mitigation (private repo, purge request) over rewriting. For a repo whose commits are
cited in delivered or submitted documents, that reference count — not the commit count — is the deciding
input.

## 5. Apply in the working repo

Require a clean status first — no tracked modifications, so a later `reset`/checkout cannot eat work.
Then run the same command in the working repo; the rewrite is deterministic, so **HEAD must come out
equal to the throwaway clone's HEAD**. A different SHA means the two runs saw different inputs: stop
and compare before pushing.

`git filter-repo` deletes every remote, so restore it, and `--force-with-lease` needs a lease to
compare against — fetch before pushing or the lease has nothing to check:

```bash
git filter-repo --replace-text /tmp/redact-patterns.txt --force
git remote add origin <url>          # filter-repo removed it
git fetch origin                     # establishes the lease

git push --force-with-lease origin main          # never plain --force
git fetch origin && git rev-parse origin/main    # must equal local HEAD
```

Verify the remote copy itself rather than trusting the push: fetch the file back from the host's raw
URL and count occurrences there. Then clean the local object store — the old blob survives in reflogs
after the rewrite:

```bash
git reflog expire --expire=now --all && git gc --prune=now
git cat-file -e <old-blob>           # must FAIL on the local repo too
```

The host is a separate question: an unreachable blob is not deleted, so `<host>/git/blobs/<old-sha>`
keeps answering until garbage collection. Say that plainly and offer the real options — a purge
request to platform support, or making the repo private while waiting.

In a shared repo, inspect what the push will publish before running it:
`git log --oneline origin/main..HEAD --name-only` lists every incoming commit with its files,
including commits other agents or threads authored. Their commit riding along on your push is still
your push that puts it on the internet, and it is how a `.env` that someone else committed and then
declared "removed from tracking" two commits later ends up publicly reachable.

Host-side alerting cannot be assumed either: `gh api repos/<owner>/<repo>/secret-scanning/alerts`
answers `404 Secret scanning is disabled on this repository` where scanning was never enabled, so no
notification will ever arrive. Check the exposure directly — `gh api repos/<owner>/<repo>/git/blobs/<sha>`
— instead of waiting for an alert that will not come.

Finally re-sync every downstream copy of the same file (skill targets, mirrors, other clones — a
redacted repo does not clean a copy that was synced from it), regenerate any checksum manifest that
covers it, verify the sync reports zero problems, and delete the patterns file. Forks or clones taken
before the push still hold copies: state that as residual risk instead of implying the leak is gone.
