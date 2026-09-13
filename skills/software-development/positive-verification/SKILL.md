---
name: positive-verification
description: "Verify hand-edited escapes before claiming the fix correct."
---

# Positive Verification

## Trigger
After hand-editing escapes or nested-language strings, before compiling, committing, or claiming correctness. After any check that reports 'clean'.

## Core rule
A negative-only check passes vacuously when the whole construct is gone. Always pair absence-of-bad with presence-of-good:

1. COUNT the required form (`grep -c` the idiom you intended — e.g. every shell `$` inside a Kotlin string written as `${'$'}` must number-match the shell variables).
2. SCAN for the bad form (bare `$` + identifier where an escape/idiom was required; doubled backslashes where singles belong).
3. A zero on check 2 means nothing if check 1 is also zero. Stronger: check 1 must match the EXPECTED total derived from the design (N shell vars → N idioms; M host interpolations → M bare). A nonzero count that misses expectation is as suspicious as a zero — it means the check itself is blind, not that the file is clean.
4. RUN the embedded language's own parser on the decoded output. Counts catch escaping; only the real parser catches structure. Extract the string literals, decode host escapes, write to a temp file, and syntax-check (`sh -n` for shell, `python -m py_compile` for Python) before committing.

## Mismatch fingerprint
A compiler error naming an identifier that exists ONLY in the embedded language is the lost-escape fingerprint — e.g. Kotlin's `Unresolved reference 'PKG'` where `PKG` is a shell variable means the `$` lost its escape/host idiom and was parsed as a host template, NOT that a symbol is missing. The fix is to rewrite every `$` in that literal with the host's literal-safe idiom and re-run the extract-and-parse check; do not go looking for a missing declaration, and do not trust the surrounding hunks because one of them survived.

## Nested-language escapes
When embedding one language inside another's string literals, prefer the host's literal-safe idiom over backslash escapes (Kotlin: `${'$'}` for a literal `$` — no backslash to lose). Type exactly one backslash per remaining genuine escape; never copy escape sequences out of displayed diffs or tool output, the transport doubles backslashes on display.

## Per-hunk independence
Escape survival is per-edit nondeterministic: one surviving block proves nothing about the next. Re-run both checks on every edited hunk, not just the file.
