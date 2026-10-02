---
name: sealed-evidence-bundle-production
description: Use when sealing a verified evidence bundle for review.
---

# Sealed evidence bundle production

Producing a `.tar.gz` + manifest + detached hash that an external party will
independently verify and grade. The bundle is the deliverable; the conversation
is not. Assume the recipient re-derives every number and re-runs every hash.

This is a **correction-friendly** class: the same host is usually probed more
than once, and each round the reviewer downgrades statuses you overclaimed.
Getting the status honest is worth more than getting it high.

## Non-negotiables

1. **Read-only by default.** Probes read. The only writes are inside the new run
   root and the manifest. Never install a tool, restart a service, change a bind,
   edit a config, mount or write a disk, or enable a security control inside a
   collection pass — each needs its own approved change task.
2. **Never escalate privilege.** If a check needs `sudo`, do not request or pipe a
   password. Either route it to the owner as a command they run locally, or record
   `BLOCKED_PRIVILEGE_REQUIRED`.
3. **Never read a credential value.** Inventory variable *names* and categories.
   Count, classify, and stop. Negative auth probes use a deliberately invalid
   literal, never a real key.
4. **Fresh run per attempt.** A sealed run root is never edited. New timestamp,
   new directory. Corrections produce a new bundle that supersedes the old one.
5. **No overclaim.** A command completing is not a PASS. `PARTIAL`, `UNKNOWN`,
   `BLOCKED`, and `NOT_RUN` are correct answers more often than they feel.
6. **One source of truth for counts.** Every count in every document is rendered
   from a single JSON object. Hand-typing the same number into three files is how
   a bundle ships with a statement that contradicts its own evidence.

## Status ladder

`PASS` · `PARTIAL` · `FAIL` · `UNKNOWN` · `BLOCKED` · `NOT_RUN`

A status is only `PASS` when the acceptance criterion is met by a command you ran.
Reserve `FAIL` for a state that is genuinely wrong and cannot be waved through —
no backup destination really is `FAIL`, not `PARTIAL`. Report a missing preference
domain as `UNKNOWN`, never as `0` and never as healthy.

## Procedure

1. **Quarantine and preflight.** Mark prior bundles as not-final. Re-verify protocol
   input hashes. Create `on-host-probe-<timestamp>/{meta,probe,summary}` — no
   sibling metadata subtree, and keep the archive and detached hash *outside* it.
2. **Probe**, serially, one file per probe ID. Every file records method,
   limitation, and `production_mutation: false`.
3. **Reconcile claims.** Any prior statement's claim that is now wrong gets an
   explicit correction line naming the old claim and the correct one.
4. **Redact, then harden.** Redact PII to placeholders, then `chmod 600` every
   file and `chmod 700` every directory **before** building the manifest.
5. **Manifest last**, excluding itself, covering every non-manifest payload file.
6. **Seal, then self-check independently.** Build the archive, the detached hash,
   and a machine-readable self-check that measures every gate. If any gate fails,
   the bundle is not final — fix and re-seal rather than shipping with a caveat.

See `references/status-and-packaging-gates.md` for the full gate list and the PII
rule table. `scripts/seal-and-verify.sh` performs steps 4–6 in the required order.

## Pitfalls

- **`launchctl path` is the plist file, not the executable.** The executable is the
  `program` key. Comparing `ProgramArguments[0]` against `path` reports drift on
  every healthy unit and destroys the signal. Also treat a plist with no
  `EnvironmentVariables` inheriting just `PATH` as inheritance rather than drift,
  and exclude launchd-injected names (`SSH_AUTH_SOCK`, `XPC_SERVICE_NAME`) from the
  comparison.
- **A failing command is not an absence.** A `sqlite3` call that exits nonzero
  looks identical to a missing database if you only inspect the absence of output.
  Always assert on the exit code before concluding a file is missing, and prefer
  full `PRAGMA integrity_check` over `quick_check` when the claim is "intact".
- **File mtime is not event time.** An mtime window says when a file was last
  written, never when events happened. Parse a timestamp per record, and prove the
  window boundaries with a synthetic fixture of known-age events **before**
  trusting any host number. If the fixture gate fails, report FAIL and publish no
  host counts.
- **Category counts overlap unless you make them exclusive.** A line matching both
  a timeout and a provider pattern is two hits, one event. Never present the sum of
  category counts as a unique-incident total.
- **Separate active worktrees from archived copies when totalling.** A stale
  archive carrying thousands of uncommitted files is expected state; folding it
  into an active dirty total makes the number meaningless.
- **Provenance cannot come from a filename, a version string, or strings inside a
  binary.** Byte-level hash against the official release is the only accepted
  evidence. A file the release does not ship is a data artifact, not a mismatch —
  classify it and mark the upstream pin `UNKNOWN` rather than guessing.
- **Do not redact files whose hash is a protocol gate.** Findings inside
  externally supplied protocol inputs are reported as `protocol_input_content` so
  the hash gate still holds; rewriting them silently invalidates the input.
- **The archive and its detached hash must live outside the run root.** Inside,
  they are counted as payload and break the file-count-equals-manifest-entries
  gate. A self-check that records the archive's own hash must also live outside the
  archive, or the hash refers to itself and the seal breaks.
- **The detached hash line uses the basename**, not the absolute path, so
  verification works from any directory.

## Two-party exchange

When the counterpart only accepts a subset of file types, stage the bundle on a
share the counterpart can reach and hand over a link rather than attaching
binaries. Keep the whole exchange two-directional and scoped: everything outbound
is a decision-support artifact, never an authorization to merge or apply. Report
path, size, hash, manifest result, and gate summary; keep raw evidence, private
identifiers, and secrets out of chat.
