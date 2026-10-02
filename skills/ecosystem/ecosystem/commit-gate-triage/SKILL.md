---
name: commit-gate-triage
version: 1.0.0
description: Use when a pre-commit gate blocks a legitimate change.
---

# Commit Gate Triage

A pre-commit gate blocks your commit. The instinct is to reach for `--no-verify`. That is
almost always wrong: the gate is the only thing standing between a typo and a published
secret. Triage it instead, and treat "gate is wrong" as a claim to prove.

## Workflow

1. **Read the hit literally first.** Which rule fired, on which file, on which line. A gate that
   names a specific pattern in a specific file is reporting, not refusing.
2. **Determine whether the file can even reach the commit.** Check the ignore rule and tracked
   status before touching anything: `git check-ignore -v <path>`, `git ls-files --error-unmatch
   <path>`. A gate that walks the whole working tree — rather than the staged set — will flag
   untracked local fixtures and caches that could never be published. That is the single most
   common false positive, and it is worth identifying before touching code.
3. **Distinguish a synthetic test value from a real one.** Look at the shape and the count of the
   flagged values without printing them: prefix, last digits, length, whether they are sequential,
   how many distinct values. Sequential/placeholder values that appear in a test fixture are
   generated data, not leaked records. Never echo the value itself into chat or a commit.
4. **Prove the gate still bites.** Before accepting any mitigation, plant a planted violation in a
   throwaway file and confirm it is caught. A gate you have not re-tested is a gate you have not
   checked. Then delete the file and confirm the tree is clean again.
5. **Fix at the generator, not the allowlist.** If a generator writes fixtures that trip the gate,
   make it emit the gate's documented declaration marker (the escape hatch usually exists and is
   intentionally public, e.g. a declaration string the scanner recognises). Embed it in a field no
   consumer parses as data. Do not widen the exclusion list and do not special-case the filename.
6. **Verify the whole gate output, not the exit code.** Read every line: many gates print `LEWATI`
   (skipped) lines alongside the verdict, and the skip lines are how you audit which declarations
   are currently in force.

## Pitfalls

- **A whole-tree scanner will trip on gitignored fixtures.** Most PII/secrets scanners walk the
  directory tree instead of the staged file list, so a locally generated test corpus sitting in a
  gitignored path blocks the commit even though it can never be published. Confirm with
  `git check-ignore -v` before assuming a real leak — then fix the fixture, not the scanner's scope.
- **Never reach for `--no-verify` as the first move.** It disables the secret gate for this commit
  and, more importantly, marks the change as unreviewed. Resolve the hit or report that you
  cannot.
- **An escape hatch that lives in the first N characters of a file is a declaration, not a
  bypass.** If the gate's own comment says the skip is not a hidden allowlist, honour it: put the
  marker where the gate reads it, in content the generator already controls. Placing it inside a
  payload field that a consumer might echo back into an LLM prompt is a mistake — pick a field no
  consumer reads.
- **Report a blocked gate, do not route around it.** If the fix would require weakening the gate
  itself, or the commit touches a protected instruction file whose approval times out, stop and
  surface it. A timed-out approval prompt is not consent.
- **When the same gate fires twice in a session, fix the fixture and regenerate.** Editing a
  generated artefact by hand is what causes the next failure — change the generator, re-run it,
  then re-check the gate.

## Bukti (verified 2026-10-01)

A PII gate blocked a docs-only commit on a synthetic national-ID-shaped value inside a
gitignored test-corpus fixture. `git check-ignore -v` proved the file was untracked; the value was
one sequential placeholder, not a real record. The generator was amended to emit the gate's
documented declaration marker in a field nothing parsed, the corpus was regenerated, and the gate
returned clean. A planted real-looking value was then confirmed to still be caught, proving the
mitigation was not a bypass.
