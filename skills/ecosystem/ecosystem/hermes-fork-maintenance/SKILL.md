---
name: hermes-fork-maintenance
description: Use when auditing a forked Hermes install's updates.
---

# Hermes Fork Maintenance

When the Hermes install is a **git fork** rather than a plain upstream clone, `hermes update` is not
the upstream updater any more — it pulls whatever the fork's `origin` points at. Everything below
follows from that.

## Rule 1 — Prove which remote `hermes update` targets before trusting its numbers

`hermes --version` prints a line like:

```
v0.21.1 (2026.9.7) · upstream 02244472 · local 6872e8e8 (+7945 carried commits)
Update available: 2 commits behind — run 'hermes update'
```

The word **`upstream` on that line is the fork's `origin/main`, not `NousResearch/hermes-agent`.**
The updater compares local `main` against the configured origin. Reading that label as "the real
upstream" produces the wrong conclusion about how current the install is: "2 commits behind" can sit
on top of a fork that is tens of thousands of commits behind the real project.

Confirm from git, never from the version string:

```bash
cd <hermes checkout> && git remote -v
```

- `origin` = the fork — the update channel.
- `upstream` = `https://github.com/NousResearch/hermes-agent.git` — the real source.

If there is no `upstream` remote, the install has no path to real upstream at all; say so rather than
implying updates are flowing.

## Rule 2 — Measure drift with `rev-list --left-right --count`, not `git status`

```bash
git rev-list --left-right --count upstream/main...main   # left = upstream-unique, right = local-unique
git rev-list --left-right --count origin/main...main     # left = fork-unique,   right = local-unique
```

Read it as `behind<tab>ahead` from the local branch's perspective. Report **both** pairs — fork-vs-local
and upstream-vs-local answer different questions ("is the update channel current?" vs "how far has the
project moved?").

## Rule 3 — Fetch the big remote in the background

A full `git fetch upstream` on the Hermes repo takes minutes and **blows past a foreground timeout**.
Run it as a background process with completion notification, do other work, then measure. Do not retry
it in the foreground with a bigger timeout — the wait is the same.

To learn how stale a local ref is **without** any fetch, ask the remote directly:

```bash
git ls-remote upstream refs/heads/main    # live HEAD SHA
git log -1 --format="%h %ci %s" upstream/main   # where your local ref still sits
```

A large gap between those two timestamps is the whole finding.

## Rule 4 — Enumerate carried local patches as a list the owner can decide on

```bash
git log --oneline upstream/main..main                     # commits only local has
git diff --stat $(git merge-base main upstream/main) main # files those commits touch
```

Present them as a table (SHA · date · subject · files) — this is the set that must survive any
rebase, and the owner needs to recognise each one. Watch for **two patches touching the same function**
(one already on the fork, a newer one local): flag the pair explicitly, because a rebase silently
resolves them in whichever order it happens to apply, and one may be dead code that should be dropped
instead of carried.

## Rule 5 — Source-tree patches do not survive updates; treat re-apply as the design

A patch applied to the checkout (`hermes_cli/...`, `gateway/...`) is reverted by the next update. Two
non-negotiables:

- **Commit it to the local branch immediately.** An uncommitted patch in the working tree is the one
  thing an update can destroy with no trace.
- **Keep the re-apply procedure in a skill**, so a future session restores it without re-deriving it
  from scratch. Record the failure mode you actually hit, not just the happy path.

## Rule 6 — Never restart the gateway from inside the gateway

A restart command issued from the agent's own shell is killed by SIGTERM propagation before it
completes, and Hermes blocks it outright. Hand the user the outside-shell command
(`hermes gateway restart`, or the `launchctl kickstart` equivalent) instead of trying variants.

## Rule 7 — Reconciliation is owner-gated; report and recommend

Pushing the fork, re-syncing it with upstream, and rebasing carried patches is a large, risk-bearing
change to the code that is currently running. Do the measurement, write the recommendation, and
**stop**. Wait for an explicit trigger before rewriting branch history or pushing thousands of commits.

## Pitfalls

- **The `upstream` label in `hermes --version` is not upstream.** See Rule 1 — this is the single
  easiest way to report a healthy install that is actually far behind.
- **A fork can be the update channel and still be stale.** `origin` being reachable says nothing about
  whether anyone has synced it. Compare `origin/main`'s commit date against today.
- **A fork with its own commits disables upstream sync entirely — by design.** The updater offers
  upstream sync only when the fork has **zero** commits upstream lacks (`origin_ahead == 0`); otherwise it
  prints "Skipping upstream sync to preserve your changes" and returns. And even when reached, the sync is
  `git pull --ff-only upstream main`, which cannot succeed when the local branch has diverged. So carrying
  local patches means upstream never flows in automatically — do not describe `hermes update` as an update
  path in that state. Re-apply or reconcile manually instead.
- **`updates.check: true` means "check", not "apply".** There is no auto-update. `~/.hermes/.update_check`
  holds `{"behind": N}` measured against the **fork**, so its number can look healthy while upstream is
  thousands of commits ahead.
- **`git rev-list --left-right --count A...B` returns `behind\tforward` relative to the branch named
  second.** Swapping the arguments silently inverts the report.
- **`git ls-remote` output carries a trailing tab.** Strip whitespace before comparing a local SHA to
  a remote one, or identical trees compare as diverged.
- **Many carried commits is not automatically a problem.** It usually means the fork is the working
  branch and upstream was never merged in. Report the count and the age; let the owner judge.
- **A new skill appearing in the bank mid-session may be the autonomous curator, not another thread.**
  Check `~/.hermes/skills/.curator_ledger.jsonl` for `{"actor": "curator", "evidence": {"session_id": …}}`
  before assuming concurrent work. The ledger names the originating session, so provenance is decidable.

## Related

- `ecosystem/ecosystem/hermes-model-catalog-management` — source-tree patch that must be re-applied after
  any update (Rule 5's re-apply discipline in practice).
- `docs/reports/FILTER-MODEL-GRATIS-DAN-STATUS-FORK-HERMES-2026-10-06.md` — the measurement run this
  skill was distilled from.

## Bukti

- `git remote -v` → `origin=git@github.com:Niumination/hermes-agent.git`, `upstream=https://github.com/NousResearch/hermes-agent.git`.
- `git rev-list --left-right --count upstream/main...main` → `16185  5`.
- `git rev-list --left-right --count origin/main...main` → `2  7945`.
- `git rev-list --count upstream/main..origin/main` → `2` — the fork carries its own commits, which is
  exactly the condition that makes `_sync_with_upstream_if_needed()` skip.
- `hermes --version` → reports `upstream 02244472` while `git ls-remote upstream refs/heads/main` returns a
  far newer SHA — the label points at the fork.
- Background `git fetch upstream --no-tags` completed after ~5 min; foreground attempts timed out at 120s and 300s.
- `~/.hermes/skills/.curator_ledger.jsonl` → `{"actor": "curator", "action": "create", "skill":
  "hermes-fork-maintenance", "evidence": {"session_id": "20261006_090400_966fac9b"}}` — this skill's origin.
