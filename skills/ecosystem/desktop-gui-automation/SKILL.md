---
name: desktop-gui-automation
description: "Use when driving a desktop GUI with computer_use."
version: 1.0.0
license: MIT
platforms: [macos, windows, linux]
metadata:
  hermes:
    tags: [computer-use, desktop, gui, automation, cost-control, latency]
    category: desktop
    related_skills: [computer-use]
---

# Desktop GUI automation — cost-controlled

Driving a native app through `computer_use` is a *paid* loop: every capture ships a
large element payload into context and may trigger a second (vision) model call. The
common failure is not a wrong click — it is spending 20 tool calls and minutes to make
one correct click.

## When the user says it is slow

**Measure, then report. Do not keep retrying.** A user reporting that a task is very slow
is asking for a diagnosis with numbers, not another attempt.

Measure each layer separately before naming a culprit — see
`references/latency-attribution.md` for the exact probes and the trap that makes a
*failing* probe look like a *fast* one.

## Procedure

1. **Locate the target before touching it.** Prefer a searchable list over a blind
   click. In most chat/mail/IDE clients, `cmd+f` (or the platform search shortcut) then
   typing a distinctive substring then `return` reaches a target with no coordinates at
   all. Do this first; it is both faster and more reliable than pixel work.
2. **Capture with `app=` always set.** Omitting it captures the whole AX tree of the
   focused app *plus the global macOS menu bar*, which on a typical desktop is the
   majority of elements and the bulk of the tokens. `references/capture-cost.md` has the
   measured ratio and the privacy reason this matters beyond speed.
3. **Choose the cheapest capture mode that answers the question.**
   - `ax` — text/structure questions. Does not invoke a vision model.
   - `vision` — only when you must judge pixels (layout, image content, rendering).
   - `som` — numbered overlays, for when you intend to click by index.
4. **One action, then read the verdict.** Every input action returns
   `verdict.decision`. If it is `done` / `effect: "confirmed"`, the step succeeded — do
   not re-capture to "make sure". Only `unverifiable` or `suspected_noop` justifies a
   fresh look, and then that look should be the *cheapest* mode that can confirm it.
5. **Re-capture only when state actually changed.** Element indices are snapshot-scoped;
   an index from a previous capture is not merely stale but may resolve to a different
   element now. Re-capture after any action that opens, closes, or navigates.
6. **Batch verification.** Where the tool allows it, request the post-action capture with
   the action instead of spending a separate round trip.

## Pitfalls

- **Unscoped `capture` is the single largest cost in GUI sessions.** The global menu bar
  is invisible to the user's intent but fully present in the payload; it is why
  "capture the screen" returns far more elements than the app on screen has controls.
  Always pass `app=`.
- **The menu-bar subtree leaks the user's recent filenames into context** — documents,
  media, project names. Never paste a raw unscoped capture into a report, log, or
  screenshot summary.
- **A refused click is not a retry.** A driver may reject a bare element index and
  require a snapshot-scoped token that the calling tool does not surface. If a click is
  refused with a schema complaint, re-probe once after any driver upgrade; if it still
  refuses, switch to the search/keyboard path in step 1 rather than burning calls on
  coordinate retries.
- **Background delivery is not guaranteed for every app.** Synthetic events can be
  swallowed by Electron/Chromium surfaces, games, and canvas widgets. When a result
  reports the input did not land, escalate to foreground delivery as a *reaction*, then
  re-verify — never predict the escalation from the app's framework.
- **Foreground delivery visibly steals focus.** It is only appropriate when the user is
  not actively working. Batch a foreground sequence rather than alternating modes.
- **A long GUI session can outlive its own helpers.** The app or its driver backend may
  exit mid-task. Re-check liveness once rather than assuming the earlier successful call
  still holds.

## Reporting a GUI task

State what was *verified*, not what was attempted. "Message sent — bubble present with
timestamp" is a result; "clicked the send button" is not. If a target could not be
reached, say so plainly and name the last verified state.

`references/latency-attribution.md` — layer-by-layer latency probes, and why a fast
rejection is not a healthy endpoint.
`references/capture-cost.md` — payload/token math, mode selection, privacy of the
unscoped tree.
