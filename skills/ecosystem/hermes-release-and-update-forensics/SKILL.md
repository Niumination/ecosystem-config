---
name: hermes-release-and-update-forensics
description: "Use when auditing a Hermes release or update."
version: "1.0.0"
author: Hermes Agent + Niumination
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, update, releases, fork, drift, verification]
    related_skills: [hermes-fork-maintenance, hermes-fork-reconciliation, hermes-agent]
---

# Hermes Release & Update Forensics

Three questions land here: **"what does the new release add?"**, **"how far behind am I?"**, and
**"is updating safe?"** All three are answered from git evidence, never from a version banner or a
release note.

## A. Measure how far the install is behind

```bash
cd <hermes checkout>
git remote -v                       # origin = fork/update channel, upstream = real project
git rev-parse --short HEAD          # what is installed
git log -1 --format='%h %ad %s' --date=short upstream/main
git tag --sort=-creatordate | head -5
```

Report **installed commit**, **latest stable tag**, and **days/commits of drift**. Do not quote the
`upstream <sha>` label from `hermes --version` as "the real upstream" — on a fork that label is the
fork's `origin/main`. See `hermes-fork-maintenance` Rule 1.

`hermes update --check` / `--plan` are read-only but index the whole checkout and can exceed a
foreground timeout on a large repo. Give them a generous timeout or run them in the background, and
never report a timeout as a failed check. Verify any service PID the plan prints against the live
process list before repeating it.

## B. Prove each feature in a release note

A release note is marketing copy, not an inventory — it names a behaviour, not a file.

```bash
# read the TAG, not the working tree: main is ahead of the tag
git show <tag>:path/to/file.py | grep -c '<symbol>'
git ls-tree -r <tag> --name-only | grep -iE '<feature-slug>'
# one query covers the whole release window
git log --oneline <prev-tag>..<tag> --no-merges --grep='<feature>' -i
```

| Feature in the note | Symbol to grep |
|---|---|
| pluggable delegation backends | `register_delegation_provider`, `delegation_backends.py` |
| plugin slash commands pick an option | `ask_choice` |
| sign-in flow change | `auth_device_flow.py` |
| local LLM one-click | `llama_app_latest` in `pm/packages.py` |
| desktop framework bump | the pinned version in `package.json` |
| backend moved out of core | whether the file still exists in core |

Report two columns: **verified** (commit + file) and **unverified** (note claim only).

## C. Prove updating is safe — the merge dry run

```bash
git merge --no-commit --no-ff upstream/main    # names every conflicted file, writes nothing on a clean tree
git diff --name-only --diff-filter=U
git merge --abort
```

Then verify you left nothing behind:

```bash
git status --porcelain | wc -l     # 0
[ -f .git/MERGE_HEAD ] && echo ADA || echo tidak ada
git rev-parse --short HEAD         # unchanged
```

Quote the conflict count and file names. "1 conflict, in `gateway/run_notifications.py`" is a
decision the owner can act on; "probably fine" is not.

## Pitfalls

- **A "0 references" grep is not proof of absence.** Release notes and commits use different
  vocabulary — a wider `--grep` term usually finds the feature under a name you did not try.
- **Grep the source tree, not the docs tree.** Release notes live under a website/ directory.
- **Checking the working tree instead of the tag conflates released and unreleased work.**
- **A version claim in the note can be off by a patch release** — pin the exact version and quote it.
- **Never run a merge dry run while a service executes from that checkout** — it rewrites files on
  disk under a live interpreter. Use a worktree, and return the main checkout to its original state.
- **Do not upgrade while the gateway is live.** Check the running services first; a restart issued
  from inside the running process is killed by signal propagation.
- **An expiring OAuth key plus a gateway restart is a compounding failure.** Refresh the credential
  and verify the provider endpoint before restarting anything.

## Related

- `hermes-fork-maintenance` — the audit half of fork drift.
- `hermes-fork-reconciliation` — rebasing carried patches onto upstream; SUPERSEDED vs CONTRADICTED.
- `hermes-agent` — the product hub; load `llms.txt` for anything not covered here.
