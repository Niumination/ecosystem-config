# PII Gate Config

Tested scanner exclusions and self-exclusion rules.

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
