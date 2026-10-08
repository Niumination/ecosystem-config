# Rebase Execution Mechanics

Depth for the execution half of `hermes-fork-reconciliation`. Load when actually running the
rebase, not when planning it.

## Drive `rebase --continue` non-interactively

A rebase that stops on a conflict re-invokes the editor for the commit message. With no editor
configured the process blocks until it is killed — it looks like a hang, not a prompt, and a
foreground timeout just kills the wrapper while `rebase-merge/` stays behind.

```bash
GIT_EDITOR=true git rebase --continue
```

Use it on the FIRST continue, not after diagnosing a hang. `GIT_EDITOR=true` accepts the
existing message unchanged, which is what a conflict resolution wants.

## Resolve conflicts in-place, then verify no markers survive

`git checkout --ours/--theirs` cannot express coexistence — it picks one side wholesale. For a
patch that must survive alongside upstream's newer implementation, edit the file directly and
remove the conflict block by hand.

```bash
grep -n '^<<<<<<<\|^=======\|^>>>>>>>\|^|||||||' <file>   # must be empty
python3 -c "import ast; ast.parse(open('<file>').read()); print('syntax OK')"
```

The marker grep is the load-bearing check: a leftover `|||||||` line (diff3 base marker) is valid
Python in no case, but a partially-removed block can still parse while having dropped upstream's
branch. Read the resolved region once after editing.

## Keep the live checkout on its running branch

A long-lived process may be executing from the checkout you are about to rebase. Never `git
checkout` a different branch there, and never let a test run against new code in that tree.

- Do the rebase in a **separate worktree**: `git worktree add /tmp/<name> <branch>`.
- Before returning the primary checkout to its branch, assert nothing is uncommitted:
  ```bash
  git status --porcelain | grep -v '<known-untracked>' | wc -l   # must be 0
  ```
- Run the test suite from the worktree too, so the running process never imports half-applied
  code.

## Attribute every test failure before believing it

Establish an **upstream-only baseline before porting anything**. Without it, a failure after the
rebase cannot be attributed and will be misread as a regression you caused.

Three-way triangulation:

| Run | Purpose |
|---|---|
| upstream tip, unmodified | proves the test passes without your patches |
| your branch, full suite | the failure you are investigating |
| your branch, failing files only | isolates flake from real breakage |

Passes in runs 1 and 3 with a failure only in run 2 ⇒ **flaky**, not a regression. Confirm with a
second signal: grep your own diff for the symbols the failing test exercises — zero hits means
your change cannot be the cause.

Timing-sensitive tests (sleep-poll loops, supervision counters) flake under a wide parallel
runner. That is a property of the runner, not evidence about your patch.

## Never re-run the full suite to answer a narrow question

A gateway-sized suite costs tens of minutes. To attribute a failure, run only the failing files
(`scripts/run_tests.sh <file> <file>`) in the worktree — seconds to minutes, and it answers the
same question.
