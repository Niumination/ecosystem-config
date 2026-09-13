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

## Pitfalls

- **Over-aggressive regex redaction:** replacing `\d{16}` inside arrays/objects without preserving quotes breaks TS syntax. Always redact the complete literal.
- **Test fixtures contain synthetic NIKs:** do not blindly exclude `__tests__`; redact the test data instead.
- **Scanner self-trigger:** if the scanner contains its own credential pattern, it will always fail.
- **`.env` false positives:** secret-shaped strings in `.env` are expected; exclude `.env*`.
- **Pre-commit + tsc in `.next`:** stale `.next/types/` can emit phantom TS errors. Always `rm -rf .next` before typecheck.

## Reference

- `references/redaction-patterns.md` — exact-string replacement recipes
- `references/pii-gate-config.md` — tested scanner config with exclusions
- `references/pre-commit-template.sh` — copy-paste pre-commit hook template
