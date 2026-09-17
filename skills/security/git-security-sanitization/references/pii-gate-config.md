# PII Gate Config

Tested scanner exclusions, self-exclusion rules, and the staged-file branches the gate must cover.

## Required exclusions
- `.git`
- `node_modules`
- `.next`
- `.vercel`
- `.cache`
- scanner script itself (`pii-gate.sh`)
- `.env*` files

## Synthetic NIK handling
- Do not blanket-exclude `__tests__`
- Prefer exact redaction of synthetic NIK literals in test fixtures
- Whitelist only known synthetic patterns if redaction is impossible

## Self-exclusion rule
If the scanner regex includes a known leaked password pattern, that pattern must either:
- not be matched against the scanner file itself, or
- be loaded from an external allowlist file

## Invocation
```bash
bash scripts/pii-gate.sh .
# expect: LEAK_COUNT 0
```

## Pre-commit gate over staged files

A gate that runs on `git diff --cached --name-only --diff-filter=ACM` must cover two independent
branches. Skipping either leaves the gate green while the leak path stays open:

1. **Ignored path staged anyway** — the `git add -f` case.
2. **Credential-shaped content** in a normal, tracked path.

```python
def is_ignored(path):
    # --no-index is required: a staged path counts as tracked, so plain
    # `git check-ignore` answers "not ignored" and branch 1 never fires.
    return subprocess.run(["git", "check-ignore", "--no-index", "-q", path]).returncode == 0
```

Name-based denial needs an allowlist for examples, or every template trips the gate:

```python
BANNED_NAMES = re.compile(r"(^|/)(\.env($|\.)|.*\.pem$|.*\.key$|credentials\.json$|api-key\.md$)")
ALLOWED_SUFFIX = re.compile(r"\.(example|sample|template)$")   # .env.example must pass
```

Keep the failure message actionable and masked: path + reason, never the value. Print the escape
hatch (`git commit --no-verify`, noting that using it must be reported) rather than hiding it —
an undiscoverable gate gets bypassed instead of fixed.

## Self-test procedure

Run both branches before trusting the gate, and assert the tip SHA did not move (a missed branch
leaves a real commit). Recipe: SKILL.md → Workflow → Verify.

## Activation per clone

Hooks are not versioned by git: store them in `.githooks/` inside the repo, then
`git config core.hooksPath .githooks` once per clone. Document that line wherever agents are told the
gate exists, or a fresh clone silently has no gate.
