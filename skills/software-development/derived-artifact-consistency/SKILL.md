---
name: derived-artifact-consistency
description: Use when two tools report different totals for one set.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [verification, manifest, counters, generators, drift]
    related_skills: [verification-before-completion, audit-finding-triage, pre-cleanup-artifact-preservation]
---

# Derived Artifact Consistency

Whenever a set gets a generated artifact — a manifest, an index, a registry table, a lockfile, a
counter line, a size total — every consumer of that number must enumerate the set the same way.
When two of them disagree, the bug is almost never the data: it is a different enumeration predicate
in one of the tools.

## When to Use

- Two tools report different totals for the same set (manifest 145 vs index 144, LOC counts,
  coverage, audit finding counts, "N files synced").
- A generated artifact is regenerated and the diff is larger than the change you made.
- Before hand-editing a counter, a table row, or a regenerated file to make numbers match.

## Rules

1. **A set has one definition; the tools must share it.** Hidden/archived dirs, vendored trees,
   symlinks, and generated output are the usual divergence points. Pick one canonical predicate and
   patch every tool to it — do not patch the number.
2. **Checkers that both pass can still disagree.** Two green checks measuring different predicates
   hide the drift indefinitely; a mismatch that survives red-green cycles means the definitions
   differ, not that the count has tolerance.
3. **Never fix a total by editing data, rows, or regenerated output by hand.** Fix the tool, then
   regenerate — otherwise the next run reintroduces the discrepancy and the artifact now lies.
4. **Non-destructive copiers never remove.** After narrowing the definition, the destination still
   holds copies of whatever the old predicate let through; clean those separately and say so.
5. **State the excluded classes in the docs**, not just in the code: the next person re-derives the
   whole argument otherwise, and "why is this 144 not 145" becomes folklore.
6. **Ship the tool change and the regenerated artifacts in one commit.** A tool fix without
   regeneration leaves every consumer reading stale numbers.
7. **Prove the checker can go red before trusting a green result.** A sweep that reports "nothing
   found" must be shown to find a known-bad sample; without one, "no findings" and "never looked"
   render identically and the report reads exactly the same. Count the iterations (or read a
   `bash -x` trace) for any checker whose input arrives from a process substitution, `find`, or a
   pipeline — such a loop can run zero times and still print success.
8. **Prove a regenerator idempotent in memory before it writes to a tracked file.** Call the builder
   twice on the current text and require the second pass to report zero changes; a writer that is not
   convergent rewrites a tracked artifact on every run and corrupts it progressively ("run 1: 103
   changes, run 2: 15" is the signature, not progress).
9. **Read the artifact's real schema before writing a single row into it.** Column counts and header
   rows differ per section inside one file. A rebuild that inserts or deletes at cached line indices
   shifts those indices and deletes the wrong lines while still exiting 0 — split the file into
   blocks, rebuild each block in place, and reassemble while walking, never from positions collected
   earlier in the same pass.
10. **When a non-convergent writer has already corrupted the artifact, restore it from git and re-run
    the fixed generator.** Never hand-repair rows, and never let the corrupted text become the
    baseline for the next pass.
11. **Key generated rows by the identity the checker greps for, not by display metadata.** A
    frontmatter `name:` that differs from the directory name makes the generator treat a live row as
    stale and delete it — immediately before the checker reports that member missing.
12. **A row count is not a member count when the artifact lists members twice** (a featured table
    plus per-section tables). Compare unique identities, restrict the match to the row shape that
    denotes a member, and check whether summary rows (`| **Total** | 145 |`) satisfy the same regex.
13. **A scheduled auto-fixer may rewrite only artifacts that are 100% reconstructible from the source
    of truth.** Commits and pushes, deletions, config, credentials, and content judgement stay opt-in
    flags or manual steps — a nightly job that edits those unattended is indistinguishable from data
    loss.
14. **Meta-only churn is committed by a guard with explicit refusals, never by loosening the fixer.**
    Prove the churn meta-only by normalizing both revisions (meta key values replaced with a
    placeholder in structured files, timestamp lines dropped in text) and comparing; then refuse
    unless every precondition holds — HEAD exists, no merge/rebase in progress, nothing staged, and
    no tracked file outside the allowlist modified. Ignore untracked files (safe only because `git add`
    runs with explicit pathspecs) but print them, echo the commit's own file list as scope evidence,
    and never push. Prove it in a throwaway repo, negative scenarios first.
15. **An artifact that grows on every run has a writer bug, not regeneration noise.** Run the writer
    three times and compare line counts: constant means idempotent, +1 per run means the writer joins
    a suffix that already starts with a newline. Fix the writer (strip leading newlines from the
    suffix before joining, add a separator only when the suffix is non-empty), then clean the damaged
    file back to a single trailing newline.

16. **`|| echo 0` makes "cannot compare" indistinguishable from "nothing to compare".** A comparison
    whose command fails fatally renders as the clean answer: on a branch with no upstream tracking
    configured, the rev-list count against `@{upstream}` dies and the substituted zero reads as
    "nothing waiting" indefinitely. Prove the comparison can return a non-zero value against a
    known-different pair before trusting its zero, and resolve the reference per item — one repo in a
    workspace may be less configured than its neighbours, so uniformity is an assumption to test,
    not a starting point.
17. **A policy that deliberately never automates something needs a reporter for the backlog it
    defers.** "The fixer never pushes/deletes/commits" is only safe when the periodic report surfaces
    what has accumulated and names the command that clears it; otherwise the deferral is invisible
    until someone inspects the machine by hand. Report the deferred count next to the policy's status
    line, isolate it from unrelated work by the recognizable marker the fixer writes (its commit
    subject), and state both numbers so a genuine backlog cannot hide inside an expected one.

Depth for the generator side (harness, block-rebuild recipe, wiring a scheduled fixer):
`references/regenerator-authoring.md`.

## Procedure

1. **List every enumerator of the set.** Grep the repo for the walk/glob/find calls that produce or
   verify the number — generator, copier, reporter, checker, and any doc that hardcodes it.
   `grep -rn "rglob\|os.walk\|find .*SKILL\|\bglob(" --include='*.py' --include='*.sh' .`
2. **Dump each predicate side by side.** Compare the exclusion filters literally: `-not -path
   '*/.*'` vs `-not -path '*/.git/*'` vs `part in SKIP_DIRS` vs `dirs[:] = [...]`.
3. **Choose the canonical definition** (the one matching the user-visible meaning of the set) and
   align all tools to it, including the checker and the doc counters.
4. **Regenerate in dependency order** (source → generated artifact → lockfile), then re-run every
   checker and require the SAME number from all of them.
5. **Clean already-copied extras at the destinations** that the old predicate had allowed.
6. **Report** the old predicate, the new one, the number before/after, and every location changed —
   a bare "counts now match" hides which definition won.

## Pitfalls

- **Silent zero-iteration sweep.** `while read … done < <(find …)` can consume no input at all and
  fall straight through to the success branch, so a health check reports "all clean" while dozens
  of dirty items exist. The tell is not an error message but a missing one: no rows, no count, no
  negative case. Re-run the enumeration by hand (`git status --porcelain | wc -l`, `find … | wc -l`)
  and compare it against what the checker claims to have examined.
- **A clean report must state its denominator.** "0 findings" without "N items scanned" cannot be
  distinguished from a broken walk; print the examined count next to the verdict so the next reader
  can see the sweep actually looked.
- **An off-by-one that survives weeks is a definition bug, not a rounding bug.** Treat "it's only
  one" as a signal to diff predicates, never as noise.
- **Do not align the checker to the artifact.** If the manifest includes archived entries and the
  human-facing index excludes them, the index is usually the correct meaning; make the manifest
  match it, not the reverse.
- **`up-eco`-style guards that compare a hand-written counter to a generated total** will pass while
  the table underneath is stale — assert the ROW COUNT too, not only the number in the header.
- **A protected/owned aggregator may refuse your edit** (user-owned skill, bundled tool). Then the
  fix belongs in the code and the doc you do control, with the refusal reported rather than worked
  around by hand-editing the generated output.
- **Interpreter noise is not a finding.** A checker that emits `import: command not found` or
  `syntax error near unexpected token` was invoked with the wrong interpreter (a `.py` handed to
  `bash`). Fix the invocation and re-run before reporting anything as a repository problem — verify
  the verifier first, or you will file your own typo as a defect.
- **Nested-quote heredocs fail as silence.** Multi-line scripts sent through a tool layer can arrive
  mangled and produce empty output, which reads exactly like a passing test. Write the script to a file
  and run the file.
## Verification

- [ ] Every enumerator identified, with its predicate quoted in the report
- [ ] One canonical predicate applied to all of them
- [ ] All checkers re-run: identical totals, no tolerance
- [ ] Regenerated artifacts += tool change in the same commit
- [ ] Excluded classes documented where the next reader will look
