---
name: scheduled-job-delivery-routing
description: Use when cron output is misrouted or must be routed. Fixes deliver targets.
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

## Routing to a chat thread raises the job's output contract

`local` is cheap: a job that speaks on every wobble only writes extra files nobody reads. The
moment the same job points at a shared thread, every false "changed" becomes a notification a
person has to dismiss. **A route is therefore not finished when the target is set — it is finished
when the job can only speak when something genuinely changed.** Check three things before
declaring the route done:

1. **Silent when unchanged.** Exit 0 with empty stdout produces no message. A job that prints
   "nothing to do" on every run posts that line every run — at a 30-minute cadence that is 48
   messages a day into a thread other work also uses.
2. **Stable sampling when the source fluctuates.** If the value the job compares is a live
   measurement of a flapping source (an aggregate endpoint, a catalogue, a service that drops in
   and out), the job sees a change on every wobble and reports each one. Read the source two or
   three times and act only when consecutive reads agree; when they do not agree, stay silent and
   let the next scheduled run catch the settled value. Distinguish the flapping layer from the
   underlying source by probing the source directly — if the source is steady and only the
   aggregate moves, the instability is in the aggregator, not the data.
3. **Verify a write against the same snapshot you wrote from.** Re-fetching the source to confirm
   the write races a fluctuating endpoint and fails a job that is actually correct. Compare the
   bytes on disk to the value already in hand.

A job pointed at a shared thread without these will be routed correctly and still be wrong. Say in
the report which of the three the job has — "silent when unchanged, stable-sampled, verified
against the write snapshot" is checkable; "routed correctly" is not.

## Finding the intended destination ("route it where it belongs")

When the user does not name a target, **do not ask and do not guess** — the convention is already
in the job list. Inventory every job, group by class (automation/monitor vs wiki-internal vs
owner-DM), and count targets:

```bash
hermes cron list | grep -E 'Name:|Deliver:' | paste - - | sed 's/  */ /g'
```

The **majority target within the class is the convention**; a job that is the lone outlier is the
bug, and the user's phrasing ("route it where it belongs") is them noticing exactly that. A job
sitting at `local` while eight siblings of the same class point at one thread is not a deliberate
choice — it is an unfinished route.

Say which jobs you counted when you report the change. "Nine of nine automation jobs point at
thread X; this one did not" is verifiable and closes the question; "X seemed right" does not.

## Procedure

1. **Inventory what exists and where each one points.** Never assume from names.
   ```bash
   hermes cron list
   ```
   Record every job's ID **and** its deliver target. This is the only authoritative listing.

2. **Classify each job**: does its current target match intent? Mark the mismatches. Expect
   the set of mismatches to correlate with creation context, not with job type or age. **Include
   `--failure-deliver` in the classification** — see the pitfall below.

3. **Get the exact job ID from step 1 — never construct or guess it.** IDs are hex strings of
   varying length; a truncated or invented ID fails.
   ```bash
   hermes cron edit <id-from-list> --deliver local
   hermes cron edit <id-from-list> --failure-deliver local   # both, not just the first
   ```
   A wrong ID returns `Job not found: <id>` and changes nothing. That error is the guard
   working, not a partial success.

4. **Confirm the write landed** — re-run `hermes cron list` and read the deliver value back.
   The edit command exiting 0 is necessary but is not the confirmation.

5. **Prove routing with a forced run, not by waiting for the next fire.**
   ```bash
   hermes cron run <id-from-list>
   ```
   Then read the artefact that run produced:
   ```bash
   ls -t ~/.hermes/cron/output/<id>/*.md | head -1
   ```
   That file is the evidence: it names the job, the run time, the mode, and the payload. A job whose
   stdout was empty records `Status: silent (empty output)` — which still proves it ran and that
   routing did not error. Fall back to waiting one interval only when the job cannot be forced.

6. **Say what the next scheduled fire will prove** if the forced run could not exercise the real
   payload (e.g. a job that only speaks when its source changes).

## Pitfalls

- **`hermes cron update` is not the verb; `hermes cron edit` is.** Check `--help` on the
  subcommand rather than assuming an update/edit pair exists.
- **`--failure-deliver` is a second, hidden misroute.** Fixing `--deliver` leaves failures still
  going wherever the failure override points — commonly `origin`, i.e. the creation thread. A job
  can look correctly routed on every successful run while every failure still lands in the wrong
  place. Read and set both fields in the same edit pass.
- **A silent-by-design job cannot be proven from the chat.** A watchdog that only speaks on change
  posts nothing, so "no message appeared" is consistent with both correct routing and a dead job.
  Prove it from `~/.hermes/cron/output/<id>/` instead: a `silent (empty output)` record plus a
  non-zero run count is the evidence.
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
nothing is special-cased or broken. Then show the target table, the before/after values **for both
`--deliver` and `--failure-deliver`**, the evidence from the forced run's output file, and what the
next scheduled fire will additionally prove.

When the route ends at a shared chat thread rather than `local`, also state the job's output
contract (silent when unchanged, stable-sampled if its source fluctuates, verified against the
write snapshot). Moving a job from `local` to a thread is the moment its noise becomes someone
else's problem, so that check belongs in the same report as the target change.