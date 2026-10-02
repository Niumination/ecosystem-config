---
name: documentation-reconciliation
version: 1.0.0
description: Use when docs, BACKLOG, or registry drift from measured truth.
---

# Documentation Reconciliation

Bring written records into line with measured reality without destroying the audit trail.
The governing idea: **a claim in a document is a measurement taken at some past time.
Re-measure, then decide whether the document is a ledger (supersede) or a contract
(annotate).**

## Workflow

1. **Re-measure every claim you are about to change, from the live source.** Never edit a
   status claim from a previous document. `gh repo view <repo> --json visibility` for repo
   secrecy, `curl` the health/status endpoint for service state, `git rev-parse` for hashes,
   `git ls-remote` for remote truth. If you cannot re-measure it, leave it and say so.
2. **Classify the document before editing it.**
   - *Ledger / status index* (`BACKLOG.md`, `docs/registry/*.md`, `project-catalog.md`,
     dashboard rows) → **replace** the row. A stale row is a live misreport.
   - *Contract / handover / sign-off* (BAST, `docs/serah-terima/`, KAK, RAB, audit
     reports) → **never delete the original claim.** Append a dated correction block that
     names the single endpoint or command now authoritative.
   - *Work log* (per-task reports, numbered iteration docs) → leave alone. It records what
     was true when written, which is its purpose.
3. **Point every corrected document at one source of truth.** A correction that says
   "status is now X" without saying *how to check X* goes stale again. Name the endpoint or
   command.
4. **Give every backlog item an acceptance criterion that is a command.** "Improve eval" is
   not checkable; "artefact names the model and is diffed against baseline, count of changed
   answers recorded" is. State what must be true, not what must be built.
5. **Verify encoding artifacts after each write, not at the end.** See pitfalls.

## Pitfalls

- **A repo labelled private in its own README may be public.** A wrong privacy label removes
  the standing warning that keeps PII out of a world-readable repo, and it invalidates every
  "safe to store here" judgement built on it. Read `visibility` from the forge before writing
  any note that assumes secrecy.
- **Correcting the files does not correct the commit message.** A long heredoc commit message
  can silently truncate into unrelated prose while the committed *files* stay clean. Check the
  two separately: `git show --stat` for content, `git log -1 --format='%B'` for the message.
  Amend from a message file you have re-read since writing it.
- **Scan written prose for foreign-script contamination.** Long generated documents pick up
  stray CJK/Hangul characters at word boundaries; the sentence still reads fine to the eye that
  just wrote it. Scan the final bytes for non-target Unicode blocks, not for "does this look
  right". Check every file you touched, including ones you only appended to.
- **A backlog inherited from a third party's report inherits that report's blockers.** When the
  report says an item is blocked on a missing subscription, key, or person, verify the blocker is
  still real before carrying it forward. Blockers that have evaporated move items from "waiting
  on others" to ordinary work, and that reordering is the most valuable thing the
  reconciliation produces.
- **A new backlog document must state what it supersedes.** Say plainly which older sections are
  now historical, or the next session will read both and pick the wrong one.
- **Never reconcile a protected instruction file silently.** If a status header lives in
  `AGENTS.md`, prepare the change but surface it for explicit approval; a timed-out approval
  prompt is not consent, and routing around the refusal defeats the point of the gate.

## Bukti (verified 2026-10-01)

Twelve stale claims reconciled across a service repo and the ecosystem root: repo labelled
private while the forge reported `PUBLIC`; a feature described as disabled while its toggles were
on and answering real requests; a release declared "0 tags" after the tag was pushed; pushed-and-
synced work recorded as pending; an item marked "blocked on subscription" that was in fact
answering live traffic in ~12 s. Ledger rows were replaced, six contract documents received dated
correction blocks naming the service status endpoint as authoritative, work logs left untouched.
Root commit, service commit, and manifest regen each verified by command.
