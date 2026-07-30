---
name: verification-before-completion
description: "Use when ABOUT to claim work is complete, fixed, or passing — before committing or creating PRs. Requires running verification commands and confirming output before any success claims."
domain: software-development
subdomain: sdlc
tags: [verification, testing, quality, completion, claims, evidence]
version: "1.0"
author: obra/superpowers + Niumination
source: superpowers
license: MIT
---

# Verification Before Completion

> **Sumber:** Diadaptasi dari `obra/superpowers` (MIT).

**Core principle:** Evidence before claims, always.

Melengkapi `systematic-debugging` (debugging workflow) dan `hermes-zero-defect-architect` (zero-defect protocol). Skill ini adalah **HARD GATE** — jangan klaim selesai tanpa verifikasi.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Jika belum menjalankan verification command di pesan ini, jangan klaim passing.

## The Gate Function

```
SEBELUM mengklaim status atau menyatakan kepuasan:

1. IDENTIFIKASI: Command apa yang membuktikan klaim ini?
2. RUN: Eksekusi FULL command (fresh, complete)
3. BACA: Full output, check exit code, count failures
4. VERIFIKASI: Apakah output mengkonfirmasi klaim?
   - Jika TIDAK: State actual status dengan evidence
   - Jika YA: State claim DENGAN evidence
5. BARU THEN: Buat klaim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |

## Red Flags — STOP

- Menggunakan "should", "probably", "seems to"
- Expressing satisfaction sebelum verifikasi ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Berpikir "just this once"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Integrasi Ekosistem

| Skill | Hubungan |
|-------|----------|
| `systematic-debugging` | Verification adalah fase terakhir debugging |
| `hermes-zero-defect-architect` | Zero-defect memerlukan verifikasi absolut |
| `ponytail-core` | Minimal code + verified = efisien dan benar |
| `requesting-code-review` | Verifikasi sebelum kirim review |
