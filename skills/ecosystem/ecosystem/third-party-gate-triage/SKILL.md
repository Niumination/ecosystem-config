---
name: third-party-gate-triage
description: "Use when a vendor's acceptance gate fails after a patch."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [verification, triage, external-patches, harness, flake]
    category: ecosystem
    related_skills: [arena-patch-adoption, external-patch-adoption]
---

# Third-Party Gate Triage

An external agent hands you a patch bundle plus its own acceptance harness.
The harness fails. The obvious conclusion — "their patch broke the code" — is
wrong often enough to be expensive. Two failure classes masquerade as a code
regression and neither is a code defect:

1. the harness ran against the wrong fixture, and
2. the check itself is racy.

Deciding which one it is costs a few minutes. Guessing wrong costs you either a
false bug report against correct work, or a false "all good" against broken
work. Triage before reporting, always.

## Procedure

### ① Read the vendor's own instructions before running anything

Patch bundles ship a top-level instructions file (often `00-START-HERE`,
`00-UNTUK-HERMES`, or similar) listing the exact commands, the expected counts,
and the known traps. It is the highest-signal document in the archive and it is
the first thing to read. Extract it before extracting anything else.

Extract the expected numbers into a checklist up front — test count, build
result, gate exit code, any claimed file counts. You will need them to judge
pass/fail later, and they are what you compare your run against.

### ② Prove the tree landed before judging behavior

Compare your post-apply tree hash against the hash the vendor claims. This is
the strongest single check available: it separates "the wrong code is running"
from "the right code fails the gate" in one command, and it costs nothing.

If the hashes match, the behavior difference is environmental or flaky, not
content. That one match eliminates the entire class of "the patch didn't apply
correctly" hypotheses before you start testing.

### ③ Inventory the bundle before applying

Cumulative bundles repeat earlier patches. Establish which ones you already
have rather than applying all of them:

- list every patch file with its number
- compare your current HEAD subject against the numbered patch subjects to
  find the high-water mark you already hold
- apply only the contiguous range after it, in numeric order

If a cumulative bundle offers both an all-commits file and a shorter
continuation file, pick the one whose base matches your branch. Applying the
wrong base produces conflicts that look like real breakage.

### ④ Audit new patches for secrets before applying

Scan only the new range for token/key patterns and for changes to dependency
manifests and CI workflow definitions. A patch touching a workflow or a
lockfile deserves a read before it lands.

## Pitfalls

- **Reporting a gate failure as a regression before checking the fixture.**
  Harness checkers usually query a local stub or fake server. If that stub
  defaults to a small built-in sample instead of the real dataset, the gate
  measures the stub, not your code. Confirm the record/count the stub is
  actually serving before attributing any failure to the patch. A retrieval or
  relevance suite scoring far below threshold on many items with
  near-perfect grounding on the ones it does answer is the signature of a
  starved fixture, not of broken ranking.
- **Passing a fixture path without confirming the tool reads it.** Stubs
  commonly take an optional dataset path and silently fall back to a tiny
  built-in default when it is absent. After starting any stub, read its
  startup log and confirm the record count it reports matches what the gate
  needs.
- **Treating one red check as a regression.** Re-run the failing script
  several times before concluding anything. A check that compares a cached
  timestamp across a request boundary will flake whenever a background refresh
  lands in the gap — the value is legitimately different. Three to five clean
  runs after one failure is a flake; a consistent failure is real. Report the
  run distribution, not the first result.
- **Trusting a vendor's stated file counts.** Vendor docs routinely claim a
  count their own checklist under-enumerates. Recompute counts from the repo
  and reconcile the difference explicitly; do not silently adopt either number.
- **Running a long gate in the foreground.** Multi-server acceptance gates run
  for many minutes and the harness usually starts nothing itself. Start the
  required servers first, confirm each answers, then run the gate as a
  background job and poll. A foreground timeout kills the servers mid-run and
  you lose the result.
- **Leaving harness servers running after the gate.** Kill the stub, mock, and
  app processes before pushing. They hold ports the next run needs and a stale
  process serving an old build produces a confusing second failure.
- **Letting a claim of "all green" rest on a run whose sections were skipped.**
  Optional-server sections report as passed-by-omission. Count the substantive
  results and name which sections were skipped for want of a server.

## Verification

Triage is done when you can state which of the three it is — content mismatch,
environment/fixture, or flake — and support it with a command output. If the
root cause is not identified, say so plainly and report the failing check
verbatim rather than guessing a cause. Attach the reconciliation under a
`## Bukti` section: hashes compared, stub record counts, run distribution.
