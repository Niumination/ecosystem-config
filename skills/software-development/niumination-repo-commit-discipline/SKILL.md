---
name: niumination-repo-commit-discipline
version: 1.0.0
description: Committing changes to Niumination git repos.
---

# Niumination Repo Commit Discipline

Committing changes to the Niumination ecosystem without breaking repo boundaries, leaking secrets, or committing another thread's work.

## Standing rules

- **Approval gate.** Destructive or risky actions — deleting, force-push, `git reset --hard`, mass chmod, editing a config marked "under repair" — only after an explicit trigger word: "gas" / "kerjakan" / "fix". "Pelajari" means study, report, wait.
- **Verify before committing, not after.** Confirm `git diff --cached --name-only` is exactly your files. In a multi-user setup, other agents edit concurrently, so unmodified-by-you files appearing in `git status` is normal — leave those unstaged and uncommitted.
- **Secrets never go in a repo.** Never `git add -f` anything a `.gitignore` excludes. Secrets live in `~/.hermes/.env` or `vault/` only; repos carry `.env.example`.
- **No new cron, no daemons.** The machine is a laptop, not a server. Scheduled work runs manually on demand. Standing owner decision.
- **Verification-first.** Never claim done from memory or a subagent's report; only from a command you ran, with output attached.

## Pre-flight scan

Grep all changed files before staging. Expect zero hits:

```
sk-[A-Za-z0-9]{20,}   ghp_[A-Za-z0-9]{20,}   AKIA[0-9A-Z]{16}
<KEY>=<value> assignments
```

A nonzero result needs one contextual read, not immediate action: a document that *prohibits* forbidden spellings necessarily quotes them, so a hit inside the rule is not a violation. Also sanity-check that your pattern actually matches somewhere in the corpus — a pattern that never matches proves nothing.

## Checking the repo boundary

`apps/` is excluded from the root repo, so nothing under it enters root history, and a nested `.git` does not inherit the parent's index. Confirm before assuming:

```bash
git check-ignore -v apps/abstract-studio/docs/reports/file.md
git -C apps/abstract-studio rev-parse --show-toplevel
```

A match means the path belongs to the nested repo. **No** match is the alarm — the path is tracked by the current repo and you are about to commit into the wrong history. Stop and confirm.

## Cross-repo changes: two commits, two commands

```bash
cd ~/Desktop/Niumination/apps/abstract-studio
git add <paths> && git diff --cached --name-only    # must be exactly yours
git commit -m "..." && git push origin main

cd ~/Desktop/Niumination
git add <paths> && git diff --cached --name-only
git commit -m "..." && git push origin main
```

`git add` in the root does not reach the nested repo, and vice versa. Every commit runs the ecosystem pre-commit gate (`secret-scan-staged.py`); a silent pass is the expected output.

## Verifying a push

```bash
local=$(git rev-parse HEAD)
remote_sha=$(git ls-remote origin refs/heads/main | tr -d '\t' | cut -d' ' -f1)
[ "$local" = "$remote_sha" ] && echo synced || echo diverged
```

The `tr -d '\t'` is not optional cosmetics. Without it, identical trees report as diverged because `git ls-remote` emits a trailing tab. Then confirm `git status --porcelain` is empty — and check each repo separately, since the root `git status` cannot see ignored nested repos.

## What the pre-commit gate rejects (and what to do)

Every commit in this ecosystem runs gates that fail **before** the commit is created. A failed
gate looks like an unexplained "nothing committed": check `git log --oneline -1` — if it still
points at the previous commit, the gate refused, not git. Read the gate output and fix in place;
do not work around it.

| Gate | Trigger | Fix |
|---|---|---|
| `stray-glyphs` | A CJK / non-Latin script character anywhere in the staged files — including text you pasted into prose | Replace with an ASCII/Latin word. **Never bypass with a no-verify flag** |
| `skill-manifest.py --check` | `skills/manifest.json` stale after any edit to a skill body | `python3 scripts/skill-manifest.py` (regenerates), then commit |
| `manifest sinkron` | Same as above | Same |

- **Scan for foreign-script glyphs in your own prose before committing.** The gate flags characters
  in *any* staged file, so a CJK word that slipped into a skill body or a commit message fails the
  whole commit. Catch it with a quick `grep -lP` over the staged paths rather than waiting for the
  gate to name the file and line.
- **A skill-body edit forces a manifest regeneration, so do them together.** Editing a SKILL.md
  leaves `skills/manifest.json` stale and the gate refuses; regenerate in the same pass. A commit that
  only touched a skill body is never complete until the manifest is current.
- **Never use a no-verify / `--no-verify` flag on this repo.** The gates exist to keep the public repo
  clean; skipping them publishes the defect permanently.

### Ambiguous push states

On this machine pushes commonly fail with `The remote end hung up unexpectedly` or `failed to read response body from server`. Those messages describe the connection dropping, not the push being rejected — the ref update may already be on the server.

Do not re-push to "fix" it. Diagnose once:

```bash
git fetch origin
git log --oneline -3 origin/main      # is my commit already there?
git status --porcelain
```

If your commit appears in `origin/main`, the transfer succeeded and the local side is simply stale: reconcile with `git reset --hard origin/main` (or a fetch-driven rebase) and stop. If it is genuinely missing, then — and only then — retry the push. Note that concurrent commits from other threads move the remote twice during one push; the end state can still be correct even though the command reported failure. Re-pushing a commit that already landed produces a non-fast-forward rejection, and a retry that lands twice produces two commits where one was intended.

## Pitfalls

- **Never `git add` in one repo expecting nested files to follow.** They will not.
- **Never trust root `git status` for nested repos.** They are invisible there because they are ignored.
- **Treat a divergence report as suspect before the push is.** Diagnose the comparison once, cleanly, and move on — do not re-push to "fix" a divergence that was never there.
- **Never commit another thread's edits.** Leaving their uncommitted changes alone is the correct outcome, not an incomplete one. Removing them is the owner's decision.
- **Generated aggregate files absorb every other thread's work, and the pre-commit gate demands they be current.**
  `skills/manifest.json`, `INDEX.md`, `.promotion-ledger.json`, and `docs/registry/skill-registry.md` are
  regenerated from the whole tree, so after any skill change they carry hashes and rows belonging to threads
  you did not touch — sometimes including an untracked skill from another agent. Meanwhile the gate
  (`skill-manifest.py --check`) fails the commit when they are stale. The resolution is **regenerate, do not
  stage**: run the generator so the gate passes against the filesystem, then stage only your own paths and say
  in the commit message which aggregates were deliberately left out and why. Staging them publishes another
  thread's unfinished work under your commit; leaving them stale blocks the commit. Regenerating satisfies the
  gate without either.
- **Stage by explicit path, never `git add -A` or `git add .`, whenever aggregates are dirty.**
  `git add <your paths>` then read `git diff --cached --name-only` back is the only way to keep a
  whole-tree regeneration from riding along.
- **Pushing directly to a protected branch is rejected, and the fix is a PR — not a flag.** A repo
  whose `main` is protected answers `GH006: Protected branch update failed ... Changes must be made
  through a pull request`, or `remote rejected ... (protected branch hook declined)`. Create a branch,
  push it, open a PR, and merge it. Check the protection first — when `required_approving_review_count`
  is 0 the merge can go straight through, so a PR round-trip is not the same as waiting for review:
  ```bash
  gh api repos/<owner>/<repo>/branches/main/protection \
    --jq '{reviews: .required_pull_request_reviews.required_approving_review_count, enforce_admins: .enforce_admins.enabled}'
  ```
  Then branch → push → `gh pr create` → `gh pr merge <n> --merge` → `git checkout main && git pull --ff-only`.
- **A local commit with no remote is not a push failure to retry.** When `git remote -v` prints
  nothing, there is nothing to push and `fatal: Tidak dapat membaca dari repositori remote` is expected.
  Creating the GitHub repo is an assertive external action — ask before doing it. The local history is
  safe; the commit exists regardless of whether a remote ever gets attached.
- **`git add -A` is the wrong tool when a concurrent thread has left unrelated untracked files.**
  Stage by explicit path and read `git diff --cached --name-only` back. Untracked scratch files in the
  working tree (a stray `*LOCKFILE`, a zero-byte artifact) ride along with `-A` and land in the commit.
- **Never copy a sibling file's value just because it looks like precedent.** Existing files sometimes record values that no longer match the artifact they describe. Confirm the sibling's value against what it describes; if it is wrong, record the correct value and report the discrepancy.
- **Prefer `patch` over `write_file` for edits.** `write_file` overwrites the whole file. On a file you have only partially read, re-read it before any full rewrite.

## Cross-checking content that appears in more than one file

A project's metadata JSON, script, shot list, and brief all describe the same artifact and they drift apart. Edit both sides in one change, then assert equality in code.

Normalize prose before judging — comparison across file types is noisy:

```python
import re
def norm(t):
    t = " ".join(t.split())                  # collapse whitespace runs
    t = re.sub(r"\s+([.,!?;:])", r"\1", t)   # drop spaces before punctuation
    return t.strip()
```

Report only items that still differ, and print both sides to find the real differing token. Never stop at a mismatch *count* — it says nothing about whether anything is actually wrong. This pattern reduced a six-item comparison of "all different" to one genuine one-word difference.

Before adding a row to a living index that records status or a score, confirm the artifact it points at exists (`test -d project/<slug>`). A row pointing at a missing folder while carrying a score is an unauditable claim — report it and hold for the owner rather than backfilling to make the registry look complete.

Any JSON you write must round-trip (`json.load`) before commit, plus field-level assertions on the values downstream code depends on. A valid JSON file with a wrong value is a successful parse and a failed project.

## Skill-editing constraints

- **Skill edits go to the central bank** at `~/Desktop/Niumination/skills/`, not `~/.hermes/skills/`, which is a sync destination. Write only to the target and the next sync guard refuses.
- **If `skill_manage` reports a skill lives in `skills.external_dirs`, it is read-only to autonomous curation** — creation may succeed but patches and support-file writes are refused. Put all depth in the SKILL.md body; do not leave pointers to `references/` files you could not write, since a future session will follow the broken path.
- **`skill_view` may refuse to load a skill whose name exists in two roots** (local skills dir plus an external bank). Pass the categorized path; if that still collides, patch the bank copy with the file tools.
- **`skill-manifest.py --verify-target` defaults to `structure=flat`** while the Hermes target uses the `domain` layout. Without `--structure domain` it reports over a hundred skills missing when every file is present. Regenerate with `python3 scripts/skill-manifest.py`, then check with `--check`.

## Bukti

- `git check-ignore -v apps/abstract-studio/docs/reports/x.md` → `.gitignore:27:apps/` — confirms the nested boundary.
- Dual commit sequence: nested `abstract-studio` and root `ecosystem-config` each pushed as separate commits, both verified synced with the whitespace-stripped SHA comparison.
- Normalization pass on a 6-scene script comparison: 6 raw mismatches → 1 real one-word difference.
- `skill-manifest.py --check` → 0 mismatch after regeneration.
