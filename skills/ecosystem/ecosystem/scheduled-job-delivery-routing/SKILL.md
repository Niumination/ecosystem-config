---
name: scheduled-job-delivery-routing
description: Use when cron output posts to the wrong chat or thread.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cron, scheduled-jobs, delivery, telegram, routing, hermes-cli]
    related_skills: [niu-mission-control-ops, telegram-router-orchestration, ecosystem-live-status-reporting]
---

# Scheduled Job Delivery Routing

A cron job that runs on time but posts to the wrong place is a **routing** bug, not a
scheduling bug. The schedule is fine; the delivery target is wrong. Diagnose the target
before touching the schedule.

## Core semantic: `origin` means CREATION context, not intent

`origin` resolves to **the thread/session where the job was created** — not to wherever the
job "belongs" and not to wherever it is useful. Two consequences:

- A job created from a DM will always post to that DM, forever, even after its purpose moves.
- Sibling jobs can look correct purely because they happened to be created from the thread you
  wanted. There is no special handling per job; no per-job special-case exists to find.

So when a user says "job X goes to the wrong place but the others are fine", the correct
hypothesis is **creation context differs**, not "X has special treatment".

## Delivery target values

| Value | Effect |
|---|---|
| `origin` | Post back to the thread/session where the job was created |
| `local` | Save to `~/.hermes/cron/output/` only — **no message sent anywhere** |
| `telegram:<chat_id>:<thread_id>,local` | Post to that specific thread AND save a local copy |

Prefer the explicit form `telegram:<chat_id>:<thread_id>,local` over `origin` for any job
whose destination is known. `local` alone is correct when the user wants the artefact and no
chat noise. The trailing `,local` is what gives you both without losing the file.

Get real IDs from the thread registry (`docs/registry/telegram-threads.md`); chat IDs are
negative supergroup IDs, thread IDs are the trailing component.

## Procedure

1. **Inventory what exists and where each one points.** Never assume from names.
   ```bash
   hermes cron list
   ```
   Record every job's ID **and** its deliver target. This is the only authoritative listing.

2. **Classify each job**: does its current target match intent? Mark the mismatches. Expect
   the set of mismatches to correlate with creation context, not with job type or age.

3. **Get the exact job ID from step 1 — never construct or guess it.** IDs are hex strings of
   varying length; a truncated or invented ID fails.
   ```bash
   hermes cron edit <id-from-list> --deliver local
   ```
   A wrong ID returns `Job not found: <id>` and changes nothing. That error is the guard
   working, not a partial success.

4. **Confirm the write landed** — re-run `hermes cron list` and read the deliver value back.
   The edit command exiting 0 is necessary but is not the confirmation.

5. **Judge by the next fire, not by the edit.** One scheduled interval is the minimum to prove
   routing. Until a run lands in the right place, the fix is *unverified*, and you must say so.

## Pitfalls

- **`hermes cron update` is not the verb; `hermes cron edit` is.** Check `--help` on the
  subcommand rather than assuming an update/edit pair exists.
- **Never hand-type a job ID from memory or from an old transcript.** IDs are opaque; a stale
  ID either misses the target job or, worse, edits a different job. Always re-read the list.
- **Changing a delivery target does not require a gateway restart.** Do not recommend one; it
  reads as "this was fragile" and costs the user a restart.
- **`local` silences chat entirely.** If a user asks for a file *and* a heads-up, `local` alone
  is wrong — use the explicit `telegram:<chat_id>:<thread_id>,local` form.
- **Cron output does not enter the target thread's conversation history.** By design each cron
  delivery runs in its own session with a header/footer frame, so the main thread's message
  alternation stays intact. Do not add a job to a thread expecting it to become conversational
  context there.
- **A DM is a legitimate destination.** Do not "fix" a `local` job into a DM because output was
  expected somewhere. Confirm the intended destination before editing.

## Reporting

State the semantic difference explicitly when a user asks why one job misroutes and its
siblings do not — the answer is creation context, and that is reassuring rather than alarming:
nothing is special-cased or broken. Then show the target table, the before/after IDs, and
name the next fire time as the verification point.