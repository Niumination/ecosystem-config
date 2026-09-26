---
name: sensitive-private-repo
description: Use when starting a private repo for sensitive/PII data.
---

# Sensitive Private Repo

Build a git repository that holds sensitive or PII-bearing material, hidden from a public parent repo, with commit gates that genuinely block leaks — then prove it before pushing.

Covers the **construction** side only. Leak remediation, redaction, and scanner **pattern** design belong in `git-security-sanitization` — read that one before designing patterns, and reuse its `--no-index`, no `git add -f`, test-commit cleanup, and bait-sizing rules rather than restating them here.

## When to Use

- A new repo will hold NIP/NIK, credentials, personal documents, or anything that must not be public
- The workspace parent repo is **public** and sensitive work lives inside it
- Adding a pre-commit gate to a sensitive repo and needing confidence it actually blocks

## Hard Rules

1. **Never hold sensitive material in a public repo.** Check parent visibility **first** — if public, the sensitive subtree gets its own private repo, or never ships.
2. **Hide the subtree in the parent `.gitignore`; never force-add.** `git add -f` is the mechanism by which ignored material reaches a parent whose `.gitignore` looked protective. A wholesale-ignored project directory is a reason to `git init` the project, not to force-add files into the parent.
3. **Keep the hook script free of regex patterns.** The gate scans staged file *contents* — a hook embedding credential-shaped regex flags itself. Make the hook a thin wrapper (resolve repo root, run a Python module) and put patterns in a separate module both layers import. A path-based whitelist exists only for that self-reference, and every entry needs a stated reason.
4. **Every guard needs a test that actually fires.** "The gate passes" on the happy path proves nothing. Test with material that genuinely matches the rule, not a shorter realistic-looking imitation that can never match. A gate can look healthy while its detection branch is dead.
5. **Verify the remote before and after push.** Private visibility, local SHA == remote SHA, remote tree free of secret-bearing filenames, and a clean content scan of the pushed tree.
6. **Test scripts on a copy with throwaway data, never on the real repo.** Testing in place pollutes production artifacts and can leave commits inside a repo that then gets published.
7. **Exit non-zero on partial success.** A pipeline that emits a partial artifact and exits 0 makes the caller believe output is complete. Distinguish "made the intermediate, could not finish" from "done" with a distinct exit code.
8. **macOS ships bash 3.2.** `${var,,}` lowercase expansion (and other bash 4+ syntax) aborts with `bad substitution`. Use `tr '[:upper:]' '[:lower:]'` instead. Verify shell scripts with `bash -n`.

## Workflow

### 1. Decide placement

```bash
git -C <parent> remote -v                # is the parent pushed anywhere?
# parent is public -> sensitive work gets its OWN private repo
```

Create the repo inside the parent tree, then add the parent-dir pattern to the **parent's** `.gitignore` and verify the rule actually matched before assuming the append worked — re-read the file, and confirm the parent's `git status` no longer lists the subtree.

```bash
git -C <parent> check-ignore -v <sensitive-dir>/<file>
git -C <parent> status --porcelain | grep -c '^?? <sensitive-dir>'   # expect 0
```

### 2. Restructure the gate

```
<githooks>/pre-commit        # thin wrapper only — no regex, ~20 lines
scripts/<scanner>.py         # scan engine, CLI-usable
scripts/<patterns>.py        # single source of truth for rules + whitelist
scripts/<hook-runner>.py     # layered logic, called by the wrapper
```

Layer order matters:

1. Reject files violating `.gitignore` (the `git add -f` check).
2. Scan the *contents* of staged files for secrets.

### 3. Test the gate — both branches

First record the tip SHA; a gate that fails to block will leave a real commit behind from the test itself.

```bash
BEFORE=$(git rev-parse HEAD)
git config core.hooksPath <githooks>

git add -f <ignored-secret-file> && git commit -m t   # MUST fail
<cleanup the staged file>
printf 'password = "realistic"' > bait.txt && git add bait.txt
<commit MUST fail>
git add -A && git commit -m '<real>'                    # MUST succeed

AFTER=$(git rev-parse HEAD)
# if AFTER != BEFORE and a test commit appeared:
git reset --soft HEAD~1 && git rm --cached -r .
```

### 4. Test the repo's own scripts (inside the repo, in a throwaway copy)

```bash
cp -R <repo> /tmp/probe
python3 /tmp/probe/scripts/<script> <dummy input>   # verify real behavior
rm -rf /tmp/probe
```

This is where scripts that "look right" usually break — a shell idiom that aborts, a build step that cannot finish because a dependency is missing, a parser that silently drops rows. Fix the real script, re-run, and confirm the actual repo's working tree is untouched and `git status` clean.

### 5. Push and verify

```bash
gh repo create <owner>/<name> --private
git push -u origin main
```

Confirm **before** treating it as done:

```bash
git ls-remote origin main | cut -f1              # == local HEAD
git rev-parse HEAD
git ls-tree -r --name-only origin/main           # count + inspect

# no secret-bearing filenames on the remote
git ls-tree -r --name-only origin/main | grep -E '\.env$|\.key|\.pem|\.p12|\.pfx|id_rsa|vault/'
# expect no matches

# content scan the PUSHED tree, not the working tree
tmp=$(mktemp -d)
git archive origin/main | tar -x -C "$tmp"
python3 <repo>/scripts/<scanner>.py --no-whitelist "$tmp"   # expect exit 0
rm -rf "$tmp"
```

## Pitfalls

- `check-ignore` without `--no-index` reports an already-staged path as *not* ignored, so the `git add -f` branch never fires — and it fails exactly on the case it exists for. Use `git check-ignore --no-index --stdin`.
- `git ls-files` has **no** `--name-only` (that belongs to `git diff`); it writes the error to stderr while stdout comes back empty, so the staged-file list is silently empty and the whole gate is skipped with no message.
- `git diff --cached` can return empty when `HEAD` does not exist (brand-new repo) even though the index holds files. Use `git ls-files --cached` for the authoritative list.
- On a one-commit repo `git reset --hard HEAD~1` fails because `HEAD~1` is undefined. Use `git update-ref -d HEAD` (plus `git rm -r --cached .` and `git read-tree --empty`), or just re-`git init` if nothing has been pushed yet.
- Verify a remote-content check **from inside the repo**. Running `git ls-tree origin/main` while standing in a scratch directory returns `fatal: not a git repository`, which reads as "no matches, clean" — a false pass.
- Appending to `.gitignore` can be lost or not applied; always re-read the file and confirm the pattern resolves before relying on it.
- `bash -n` catches syntax but not runtime substitution errors like `bad substitution` in bash 3.2 — actually run the script on sample data.
