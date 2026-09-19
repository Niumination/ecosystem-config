---
name: git-security-sanitization
description: Clean credential/PII leaks and add secret-scanning gates.
---

# Git Security Sanitization

Class-level workflow for removing leaked credentials and PII from repositories, plus hardening gates to prevent recurrence.

## When to Use

- Credentials, API keys, passwords, or NIK/personal data found in tracked files or git history
- Need to redact secrets across docs, tests, source code, and golden fixtures
- Setting up `pii-gate`-style pre-commit or CI secret scanning
- Post-breach cleanup where syntax must remain valid after redaction

## Hard Rules

1. **Never break syntax during redaction.** Replace whole literals, not substrings inside tokens.
   - Bad: `'1108010101801234'` → `'[NIK TEST REDACTED]` (missing closing quote)
   - Good: exact string replacement preserves quotes/brackets
2. **Exclude generated/vendored paths from scans:** `.git`, `node_modules`, `.next`, `.vercel`, `__tests__` (if fixtures use synthetic PII), `.cache`
3. **Self-exclusion:** the scanner script must not flag its own credential patterns
4. **`.env` exclusion:** env files are allowed to contain secret-shaped strings; exclude them from doc/code scans
5. **Pre-commit must not block on false positives.** If a gate triggers on its own config, fix the exclusion before enforcing it
6. **Never print the secret value.** Audit scripts read the value from the source file themselves and emit only masked context, counts, or byte lengths — the value never reaches stdout, a log, a doc, or a commit message. Grepping with the literal on the command line is the same leak in a different stream.
7. **Before committing a document, check repo visibility and grep the document — filenames included.** A status-check tool can recommend "commit these dirty files" for a file whose *name* carries a NIK and whose target repo is public; following that recommendation manufactures a fresh leak. PII hides in filenames, evidence lists, and personal-document inventories, not just in bodies.
8. **Inspect the commits you are about to publish, not only your own.** In a repo where other agents or threads commit, a plain `git push` publishes their commits too. Run `git log --oneline origin/main..HEAD --name-only` before pushing a public repo; a credential-bearing path in that list is a leak you are about to create even though you did not author it.
9. **`git rm --cached` is mitigation, not containment.** It stops future tracking and leaves the blob in history, and it often lands as its own commit seconds later, which reads like a fix. Treat any "removed .env from tracking" commit as evidence the leak is still live until history is purged and the host blob stops answering.
10. **Never `git add -f` an ignored path.** A parent-directory ignore is not a credential gate — forcing an ignored file in is exactly how a `.env` reaches a repo whose `.gitignore` looked like it protected it. When a project directory is ignored wholesale, that is a reason to `git init` the project, never to force-add single files into the parent.
11. **A gate that checks "is this path ignored?" must call `git check-ignore --no-index -q <path>`.** Without `--no-index`, a path that is already staged counts as tracked, so `check-ignore` answers "not ignored" — the `git add -f` branch never fires, and it fails exactly on the case it was written for. The content branch keeps passing, so the gate looks healthy.
12. **A gate self-test must not leave a commit behind.** Exercising the hook with a throwaway file is the only way to know it blocks, but when the gate misses, the test itself creates a real commit. After every gate test: confirm the tip SHA is unchanged, and if a commit appeared, `git reset --soft HEAD~1` plus unstage the file before any push — on a public repo the next push publishes whatever the test carried.
13. **Never bypass the gate with `--no-verify` to get a fixture committed.** The gate firing on a deliberately-planted bait token is the gate working. Remove the trigger instead of the guard: **assemble the token at run time** from concatenated fragments (`BAIT="sk-""EXAMPLE""$(printf '%08d' 0)"`) so no key-shaped literal ever exists in the tree, then substitute it into the generated fixture. Reject `--no-verify` even when the file is provably fake — a bypass becomes the precedent for the next commit.
14. **A gate self-test fixture must be able to fire.** Align the bait with the scanner's actual rule regex: a rule like `\bsk-[A-Za-z0-9]{20,}\b` requires 20+ characters, so a "realistic-looking" short bait (`sk-abc...6789`, 3 chars) can never match — the fixture's expectation is unsatisfiable and the self-test reports detection loss that is really a fixture bug. Read the rule, size the bait to it, and after any scanner rule change re-run the self-test.
15. **Exempt provably-placeholder tokens from your own scanner, and only those.** Fixtures, docs and installer templates legitimately contain token-shaped strings; a scanner that flags them trains people to bypass it. Exempt a match only when the token itself carries a placeholder marker (`...`, `<`, `>`, `{{`, `${`, `xxxx`, `REDACTED`, `PLACEHOLDER`, `YOUR_`, `EXAMPLE`) — never exempt by path alone, which is how a real key in an excluded directory survives.

## Workflow

### 1. Triage

```bash
git grep -nE "\b[0-9]{16}\b|sk-[A-Za-z0-9_-]{20,}|password\s*=" -- . ':!src/data/excel' ':!node_modules'
```

### 2. Redact Safely

- Use exact-string replacement on whole literals: `"oldvalue"` → `"[REDACTED]"`
- For JSON fixtures, load → replace → write back with a script
- For tests with NIK fixtures, replace the entire 16-digit token including quotes/brackets
- After redaction, run `npx tsc --noEmit` to catch broken syntax immediately

### 3. Expand PII Gate

The scanner must cover:
- `src/data/excel` (JSON/XLSX)
- `docs/`
- `src/services/__tests__/`
- `.` root

Exclusions:
- `.git`, `node_modules`, `.next`, `.vercel`, `.cache`
- The scanner script itself
- `.env*` files

### 4. Pre-Commit Hook

Minimal, fail-closed pattern:

```bash
#!/usr/bin/env bash
set -euo pipefail
rm -rf .next
npx tsc --noEmit >/tmp/tsc-$$.log 2>&1 || { echo "[typecheck] FAIL:"; cat /tmp/tsc_$$.log; rm -f /tmp/tsc_$$.log; exit 1; }
echo "[typecheck] OK"
bash scripts/pii-gate.sh .
```

### 5. Verify

```bash
bash scripts/pii-gate.sh .                 # expect 0 leaks
npx tsc --noEmit 2>&1 | grep -c "error TS1" # expect 0
npx vitest run                             # expect 0 failed
git status --short                         # only intended files
```

Then prove the gate itself still blocks, one branch at a time. The two branches fail independently: a gate can reject secrets and silently skip ignored paths (or the reverse), and neither test reveals the other's miss.

```bash
BEFORE=$(git rev-parse HEAD)

# branch 1: ignored path, innocuous content (the `git add -f` case)
printf 'note\n' > <ignored-dir>/gate-test.txt
git add -f <ignored-dir>/gate-test.txt
git commit -m gate-test        # EXPECT refusal naming the ignore rule

# branch 2: secret-shaped content in a normal, tracked path
printf 'PI_API_KEY=%s\n' "$(python3 -c 'print("x"*64)')" > gate-test.env
git add gate-test.env
git commit -m gate-test        # EXPECT refusal naming the credential pattern

# cleanup + proof nothing slipped through
git reset -q HEAD <ignored-dir>/gate-test.txt gate-test.env 2>/dev/null
rm -f <ignored-dir>/gate-test.txt gate-test.env
[ "$(git rev-parse HEAD)" = "$BEFORE" ] || echo 'LEAK: the gate let a test commit through'
```

## Pitfalls

- **A self-test that cannot fire looks like a detection regression.** When the bait is shorter or otherwise shaped differently from the scanner's rule, the expectation never matches and the fix appears to be "loosen the rule" — which would be the exact opposite of the intent. Compare the bait against the rule regex before touching the scanner.
- **Over-aggressive regex redaction:** replacing `\d{16}` inside arrays/objects without preserving quotes breaks TS syntax. Always redact the complete literal.
- **Test fixtures contain synthetic NIKs:** do not blindly exclude `__tests__`; redact the test data instead.
- **Scanner self-trigger:** if the scanner contains its own credential pattern, it will always fail.
- **`.env` false positives:** secret-shaped strings in `.env` are expected; exclude `.env*`.
- **Pre-commit + tsc in `.next`:** stale `.next/types/` can emit phantom TS errors. Always `rm -rf .next` before typecheck.

## Reference

- `references/redaction-patterns.md` — exact-string replacement recipes
- `references/pii-gate-config.md` — tested scanner config, the two staged-file branches (ignored path vs credential content), and per-clone hook activation
- `references/public-repo-leak-audit.md` — auditing a public repo, and what to leave alone
- `references/history-rewrite-dry-run.md` — backup → dry run → verify → apply → force-push sequence
- `references/secret-alert-triage.md`, `references/github-secret-alert-triage.md` — host alert triage (overlapping; consolidate)
- `scripts/masked_pii_triage.py` — masked triage scan, never prints the value
- `scripts/history_secret_scan.py` — scan every blob in every ref for known secret values (plain + separator-formatted), no size cap; answers "is it really gone from history?"
