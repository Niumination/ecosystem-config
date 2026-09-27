# Attributing a resource figure before reporting it

A bare percentage ("disk 87% full") is not a finding — it is a symptom with no
address. The owner cannot act on it, so they either guess where to look or
defer the whole item. Attribution is the difference between a status report and
a diagnostic.

## Rank first, then drill

```bash
du -sh ~/* 2>/dev/null | sort -rh | head -15     # rank top-level consumers
du -sh ~/path/to/suspect/* 2>/dev/null | sort -rh # drill the top offender
```

`du -sh` is the whole technique. It costs one call and it converts every vague
storage claim into a path the owner can act on. Report the ranked list, name the
single largest item and its full path, and state the free space in absolute
terms as well as a percentage.

## A percentage without attribution usually hides one huge file

Recurring pattern worth expecting: the headline number is explained by a small
number of outliers, not by distributed growth. Look for a single multi-GB media
file, a build artifact tree, or an unbounded state database before concluding
"the machine is filling up".

A bare-repo git store (checkpoint/snapshot dirs) is easy to miss because `du`
reports it as one opaque figure while `file`/inspection reveals hundreds of MB
of packfiles. Where a directory is unexpectedly large, identify what it actually
is before reporting its size.

## Bounds vs on-disk size

Config-declared retention and actual disk usage are different facts. When a
limit is declared in config (max snapshots, max total size, log rotation) and a
measured value exceeds it, report **both**: the declared bound, the measured
value, and the gap. That pairing turns a raw number into evidence that a
configured mechanism is not working.

## Log files escape declared rotation

A `max_size_mb` / `backup_count` pair in config governs a specific rotating log
and nothing else. Sibling log files in the same directory — stderr mirrors,
diagnostic dumps, supervisor output — often have no rotation at all and can be
the largest files in the directory.

Inventory the whole log directory by size, not just the file whose name matches
the configured rotation setting:

```bash
ls -laS <logdir>/*.log | head -12
```

Then state plainly which files are unrotated.

## Read-only is the default for a status report

Every probe in a status pass is read-only: `du`, `df`, `ps`, `lsof`, `curl`,
`sqlite3` (prefer `mode=ro` for a live database), `git status`/`log`. Running
`git gc`, a prune, a vacuum, or any cleanup to make a number look better
destroys the evidence the report exists to present. If a measurement itself
errors, report the error as the finding.

Related: [deployment-status-verification.md](deployment-status-verification.md)
covers the deploy-status half; the governing rule for both is that a status is
re-derived live in the session that writes it.
