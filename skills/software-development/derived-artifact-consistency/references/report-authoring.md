# Authoring a verified current-state report

Applies whenever a deliverable is a *report of what is true now* rather than a change. The failure
modes are epistemic: a number that looks authoritative and is wrong is worse than no number.

## Sensor every secret, then verify the sensor worked

Format `4chars***2chars (len N)`. Before delivering, grep the finished file for full-value prefixes
and require every hit to be a sensor form:

```
grep -cE 'ghp_|github_pat_|sk-[A-Za-z0-9]{20}|ak_|vcp_|tvly-' report.md
```

A leaked key inside a "redacted" report is a real disclosure, not a formatting nit. Also check for
mojibake — decorative CJK or stray translation artifacts injected into generated prose, which read as
corruption even when the surrounding sentence is correct.

## Never copy a number from a prior report, a doc, or memory

Every figure gets a capture timestamp from a command run in this session. A value quoted from
documentation is labelled `UNCHECKED + reason`. A stale figure copied forward is indistinguishable
from a fresh one, which is precisely why it must not be done quietly.

## Enumerate what could not be checked, in its own section

A report that silently omits five unverifiable items reads as complete. A titled section listing each
unverified item with the reason it could not be verified is the honest shape, and it costs nothing when
the list is short.

## Config claims need the config file

Read the file and quote the block. Secondhand summaries of a config drift within days. When a config
contains both a default and an override, report which one is active and why.

## Two sources that disagree are both correct for different questions

A declared configuration file is the truth about *configuration*; a runtime state store is the truth
about *history*. Route mappings, per-thread models, session counts legitimately differ between them.
Report the gap as its own finding; never normalize one to the other to make the report tidier.

## Probe services live

Never infer a deployment's status from a registry's table — that is a claim, not a measurement. Probe
and report both the claim and the measurement, and when they disagree say which one is stale.

## Distinguish a crash from a controlled exit

Trace a non-zero exit code to the line that raises it before calling it a failure. A shutdown path that
raises its own exit code is a graceful restart. Reporting that as a crash-loop sends the reader after
an incident that does not exist, and the time spent is the cost.

## Re-verify before handoff

A report assembled from a multi-wave probe drifts from itself. Re-probe the headline figures and diff
them against what the body asserts; fix the file in place when they differ.

## Honour "report only" literally

When the ask excludes recommendations, produce findings and no proposals. No "next steps", no
"suggestion", no closing action list. Name a defect and stop; the user decides what to do about it.
Offering unsolicited fixes to a read-only request is a scope violation regardless of how useful they
are.
