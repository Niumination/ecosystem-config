---
name: hermes-fork-reconciliation
description: Use when rebasing a diverged fork onto upstream.
---

# Hermes Fork Reconciliation

Carrying N local patches onto a much newer upstream. The failure mode is not a merge
conflict — it is a patch that upstream already superseded being re-applied on top of the
newer implementation, silently reverting a fix. Classify before you rebase.

This is the execution half. The audit half (detecting and measuring the divergence) is
`hermes-fork-maintenance`.

## Before planning: classify every carried patch

Three states. Decide each with evidence, never from the commit subject.

| State | Test | Action |
|---|---|---|
| UNIQUE | symbol absent upstream | must survive the rebase |
| PARTIAL | upstream has the feature, not the specific symbol | carry only the missing part |
| SUPERSEDED | upstream implements the same guard by another mechanism | DROP it |
| **CONTRADICTED** | upstream implements the **opposite** policy, test-pinned | **PORT — adapt to upstream's mechanism** |

CONTRADICTED is the trap: from a symbol grep it looks identical to SUPERSEDED. Both touch the
same feature area; only the *policy* differs. Detect it by reading upstream's comment rationale
and its tests, never the function names:

```bash
grep -rn "<issue-number>" tests/ gateway/     # upstream cites the issue it fixed
head -30 tests/<relevant-test>.py             # the docstring states the CONTRACT
```

Tell-tale signs:

- Upstream's test docstring says "must NOT" where your patch says "suppress".
- Your patch reads a *private* attribute (`_foo`); upstream exposes a *public* method (`foo()`) —
  upstream replaced the mechanism, not just the call site.
- Upstream's comment cites an issue number whose rationale argues against your patch's premise.

Real case: a local patch suppressed the normal final send when a stale finalize had already
delivered content ("avoid a duplicate"). Upstream chose the opposite — always resend the complete
answer, because a successful finalize edit can carry only the last preview snapshot and the
missing tail would otherwise be lost with no retry. Upstream pins that with
`tests/gateway/test_stale_finalize_suppression.py` ("the result must NOT silently suppress").

When CONTRADICTED and the owner requires the patch to survive: **port it**, don't drop it and
don't apply it raw. Porting means adapting the patch to upstream's new mechanism:

1. **Add a guard branch before upstream's path** — not after, not instead of. Your branch
   handles the narrow case upstream doesn't cover; upstream's branch handles the rest.
2. **Tighten the condition** — only fire when upstream's mechanism returns "no opinion"
   (e.g. `None`), never when it returns a definitive answer (`False` = mismatch, upstream
   will resend).
3. **Upgrade the API call** — if upstream renamed the method (`has_delivered_text` →
   `has_durably_delivered_text`), use the new one. The new one is usually stricter and safer.
4. **Verify with upstream's test** — if their test still goes red, the guard is too loose.
   Tighten it or accept as a known failure with a comment explaining the design conflict.

The goal is coexistence: your patch handles a case upstream doesn't, upstream's patch handles
a case yours doesn't, and neither silently reverts the other.

```bash
git log --oneline upstream/main..main                        # the carried set
git show upstream/main:<file> | grep -c '<symbol>'           # 0 = absent upstream
git show upstream/main:<file> | grep -n '<nearby-symbol>'    # read the newer mechanism
```

Why dropping beats merging: a rebase applies carried patches in order and resolves
same-function overlaps arbitrarily — one implementation wins, and it may be the stale one.
Two patches touching one function is a defect to remove, not a conflict to resolve.

## Attribute every test failure before you believe it

A rebase that leaves tests red tells you nothing until you know *whose* red it is. Never assume a
failure is yours, and never assume it is pre-existing. Triangulate:

```bash
# 1. the failure set on your rebased branch
# 2. the SAME files on pristine upstream (worktree, never a checkout that a live process uses)
git worktree add /tmp/upstream-check upstream/main
cd /tmp/upstream-check && scripts/run_tests.sh <the-failing-files>
# 3. any file that failed ONLY on your branch, re-run isolated on your branch
```

Three outcomes: fails on both refs (pre-existing), fails only on yours but passes isolated
(flaky/environmental), fails only on yours and fails isolated (real regression — the only case
that blocks the rebase).

**A 5-commit patch touches 6 files; a suite of 1010 has ~39k tests. Assume nothing about the
rest.** Without the pristine-upstream baseline you will read a pre-existing failure as your own
regression and roll back a correct rebase.

### Run test suites one at a time on a shared machine

`scripts/run_tests.sh` provisions a *generation* of the test environment per invocation under
`~/.hermes/installs/<hash>/test-environment/gen-<hash>/`. Overlapping or back-to-back runs shift
which generation is active, and `tests/home_io_guard.py` then sees the test install's own path as
the "REAL hermes home" — producing collection errors and assertion failures with nothing to do
with your change. Symptoms: `TEST BUG: file I/O against the REAL hermes home: .../test-environment/gen-.../`.
Wait for one suite to exit before starting the next; never run two Hermes suites in parallel.

### Never rebase in a checkout a live process is running from

`hermes update`, the gateway, and the CLI execute from the checkout itself. Rebasing or
`git checkout`-ing a branch there swaps `.py` files under a running process — a crash or a
half-loaded module, not a merge conflict. Do the rebase on the branch but run tests in a
`git worktree` of it, and return the main checkout to its original branch before doing anything
else. Verify with `git status --porcelain` that nothing is uncommitted before switching.

## Measure the operation before committing to it

```bash
git merge-base main upstream/main                        # the divergence point
git diff --numstat <merge-base> upstream/main -- <file>  # upstream churn per file
git cat-file -e upstream/main:<file> && echo exists      # file still there?
```

High upstream churn against a small local patch is the expensive conflict. A file that no
longer exists upstream is a port to a new location, not a resolve. Report which files carry
the risk — a total commit count says nothing about where the work will be.

## Prove the update channel is stalled from the receipt, not the banner

`~/.hermes/logs/update_receipts/latest.json` records `pre_update.sha` and `post_update.sha`.
Identical SHAs with `"outcome": "success"` means the update ran and changed nothing. That is
stronger evidence than the version banner's "N commits behind" line, which measures against
whatever `origin` points at — on a fork, not upstream.

## Execute on a scratch branch, never on the live one

1. **Recovery tag first, pushed to the remote.**
   ```bash
   git tag recovery-<branch>-pre-rebase-<yyyymmdd> <branch>
   git push origin recovery-<branch>-pre-rebase-<yyyymmdd>
   git ls-remote origin refs/tags/recovery-<branch>-pre-rebase-<yyyymmdd>
   ```
   A tag that exists only locally is not a recovery point.
2. **Scratch branch off the live branch**, rebased onto upstream:
   ```bash
   git checkout -b reconcile-upstream-<yyyymmdd> <live-branch>
   git rebase --onto upstream/main <merge-base> reconcile-upstream-<yyyymmdd>
   ```
   The live branch stays untouched until the result is proven.
3. **Resolve by choosing one implementation**, never by concatenating.
   `git checkout --theirs <file>` when the carried patch is SUPERSEDED, then `git add` +
   `git rebase --continue`.
4. **Confirm the result holds only the carried patches:**
   ```bash
   git rev-list --count upstream/main..HEAD   # the small number, not thousands
   git log --oneline upstream/main..HEAD
   ```

## Test upstream without touching the live checkout

```bash
git worktree add /tmp/<name>-upstream-test upstream/main
cd /tmp/<name>-upstream-test && <repo test runner> ...
cd - && git worktree remove /tmp/<name>-upstream-test
```

Use the repo's own test runner — it sets the isolation env (temp home, timezone, unset
credentials) that a bare invocation misses, so a pass there means something. This is also
how you answer "did upstream already fix what my patch fixes?": run upstream's tests for
that behavior instead of reading the diff and guessing.

## Swap, then verify at runtime

- Stop the service **from an outside shell**. A restart issued from inside the running
  process is killed by signal propagation before it completes.
- Fast-forward the live branch: `git merge --ff-only reconcile-upstream-<yyyymmdd>`.
- **Sweep bytecode before starting**:
  `find . -name __pycache__ -type d -prune -exec rm -rf {} +`
  Stale `.pyc` against a new source tree raises ImportError on start.
- Verify each carried patch by **exercising it**, not by grepping: the picker filter, the
  notification path, an ordinary message send. A duplicate send is the regression signature
  when a delivery-guard patch was dropped.
- Push the live branch to the fork with `--force-with-lease`, never bare `--force`.

## Rollback

```bash
<service> stop
git checkout <live-branch>
git reset --hard recovery-<branch>-pre-rebase-<yyyymmdd>
find . -name __pycache__ -type d -prune -exec rm -rf {} +
<service> start
```

Because the recovery tag is on the remote, this works even if the machine is lost.

## Write the plan before executing a multi-hour reconciliation

A reconciliation spanning thousands of commits is a multi-hour, service-stopping operation
with a go/no-go point. Write it up in the repo's docs tree first: ordered tasks, each ending
in a verification command; an explicit go/no-go gate before the destructive step; the
recovery tag; the rollback section; measured risk per file; and the decisions still open for
the owner. Then stop and wait for the go — do not start the rebase in the same turn that
discovered it. "Lanjutkan" after a report means continue the investigation, not begin the
destructive phase.

## Pitfalls

- **A patch whose subject says "already ported" may be ported only in part.** Diff the file
  LISTS, not the subjects — a port can move the code change while dropping auxiliary files
  (setup bundles, docs) that then exist nowhere else.
- **`git merge` is not the safe alternative to a rebase when a service runs from the
  checkout.** It rewrites files on disk under a live interpreter with no restart
  coordination; a force-push touches only the remote. Prefer the scratch-branch rebase.
- **"N commits behind" is measured against the configured `origin`.** On a fork that is not
  upstream. Confirm with `git remote -v` before quoting any currency figure.
- **A long fetch belongs in the background.** A full fetch of a large upstream exceeds a
  foreground command timeout. Run it with completion notification and do other work, or read
  the live ref with `git ls-remote <remote> refs/heads/main` without fetching at all.
- **Bound the sole-copy search.** Sweeping every ref (`for-each-ref`) to prove a path exists
  in only one place blows past any timeout on a repo with thousands of branches. Query only
  the refs that can hold it: the live branch, the remote branch being overwritten, upstream,
  and the merge-base.
- **A new skill appearing in the bank mid-session may be the autonomous curator, not another
  thread.** Check `~/.hermes/skills/.curator_ledger.jsonl` for an `actor: curator` entry
  naming the originating session before assuming concurrent work and holding back a commit.
