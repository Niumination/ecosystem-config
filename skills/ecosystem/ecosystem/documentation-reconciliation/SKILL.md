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
5. **For a registry that enumerates runtime objects, diff the identifier sets — do not eyeball.**
   When the document is an index of live objects (cron jobs, threads, services, repos), pull the
   document's identifiers and the runtime's identifiers and compare them **as sets**:

   ```python
   import re, subprocess
   doc = set(re.findall(r'\| `([0-9a-f]{12})`', open('docs/registry/<file>.md').read()))
   rt  = subprocess.run(['hermes','cron','list'], capture_output=True, text=True).stdout
   run = set(re.findall(r'^  ([0-9a-f]{12}) \[', rt, re.M))
   print('missing from doc:', sorted(run - doc), '| stale in doc:', sorted(doc - run))
   ```

   Then assert the counts match (`len(doc) == len(run)`) so the next session can re-run the check
   instead of re-reading the table. This is the step that finds drift a manual read cannot.

6. **Report the reconciled count as a number, not an adjective.** "14/14 IDs match, zero drift in
   both directions" is checkable; "registry updated" is not.

## Pitfalls

- **An index drifts in four directions, and only a set diff finds all four.** A row can hold a wrong
  value, a live object can be **missing entirely**, the document can list an object that **no longer
  exists**, or a whole class of objects can have never been recorded. Reading the table top-to-bottom
  catches the first only — the other three are absences, and absences are invisible to a reader. Diff
  the identifier sets.
- **A class of objects that was never added is the most dangerous drift.** A registry that documents
  six of eleven sibling jobs looks complete and authoritative; the five missing ones are the ones no
  one will think to check. Group the runtime objects by class and confirm each class appears.
- **Re-measure the aggregate counters, not just the rows.** Thread count, skill count, job count, and
  process IDs live in headers and prose; they go stale independently of the tables they summarise.
  Count from the source (`launchctl list`, `manifest.json`, `hermes cron list`) and compare to the
  number written in the document — a header claiming "9 threads" beside a table listing 10 is the
  signature of a summary that was never regenerated.
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
- **A status field can be a *snapshot*, and snapshots of a moving target mislead.** When a document
  records a measurement of something that fluctuates (a catalogue size, a live count), label it as a
  snapshot with the command to re-read it, and say plainly that the number is not a constant. A bare
  number reads as a fact and will be trusted long after it stopped being true.
- **Re-measuring to update a document is how you find a live outage. Report it as a finding, do
  not bury it in the edit.** Fetching a provider's status endpoint to refresh a registry row is a
  live probe; when it returns an auth failure, the document is the least important output of that
  step. Finish the reconciliation, then lead the report with the defect and name who is affected.
- **Trace a dependency's blast radius through config references, not through the object itself.**
  A dead credential looks like one broken integration; the question that matters is which live
  consumers point at it. Grep the config for the identifier (`channel_overrides`, route tables,
  provider pins) and name each dependent surface — a thread whose pinned model is now unanswerable
  is the actual impact, and it is invisible from the provider's own record.
- **Check for a replacement before declaring something dead.** A stale value may exist in a second
  store (a vault, a backup, a shell secrets file). Compare the two by length and prefix/suffix rather
  than printing either; identical values mean no replacement exists and the fix needs a human. Saying
  "no replacement found" without that check invites the user to go looking for one that was never there.

## Bukti (verified 2026-10-01)

Twelve stale claims reconciled across a service repo and the ecosystem root: repo labelled
private while the forge reported `PUBLIC`; a feature described as disabled while its toggles were
on and answering real requests; a release declared "0 tags" after the tag was pushed; pushed-and-
synced work recorded as pending; an item marked "blocked on subscription" that was in fact
answering live traffic in ~12 s. Ledger rows were replaced, six contract documents received dated
correction blocks naming the service status endpoint as authoritative, work logs left untouched.
Root commit, service commit, and manifest regen each verified by command.
