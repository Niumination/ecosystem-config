---
name: hermes-tool-backend-triage
description: "Use when a Hermes tool reports unavailable or timeout."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [hermes, tools, triage, computer-use, browser, backend, startup, verification]
    related_skills: [integration-verification, hermes-runtime-credential-resolution, hermes-provider-config, model-status-checker]
---

# Hermes Tool Backend Triage

Prove **which layer** of a tool backend failed before changing anything. A tool error
(`backend unavailable`, `startup timed out`, `Invalid URL`) names a symptom, never a cause —
and the layers fail independently, so guessing wastes a round-trip and can make things worse.

## When to Use

- A tool errors on every call, or the same call fails with a *different* message each time.
- A health/doctor command reports everything green while the tool itself never works.
- A service answers HTTP 200 but the tool built on it cannot do its job.
- You are about to kill a process, edit config, or upgrade a binary to "fix" a tool.

## Always-On Rules

1. **Reproduce against the real code path before theorising.** Instantiate the backend class and call its
   start/probe method directly, with timing. A reproduced failure isolates the layer in one step; a shell
   experiment that "looks the same" often differs in the one variable that matters. Compare before/after with
   the identical call.
2. **Measure every probe you blame.** A timeout verdict needs a number: what the operation costs when healthy,
   and what the budget allows. "Slow" without a measurement is a guess that will be committed as a fix.
3. **When you raise one budget, check the enclosing budget.** A readiness probe that costs 5-13s inside a 15s
   startup deadline cannot pass, no matter how the per-call ceiling is set. Raise both or state why the total
   suffices.
4. **A reachable service is not a working backend.** `200` on `/` or `/health` proves the listener, not the
   engine. Read the service's own log for its readiness line and for a *repeating* error.
5. **An error that is not 401/403 is usually routing, not auth.** `Invalid URL`, `No scheme supplied`,
   `ECONNREFUSED` inside a tool error, `404` on an internal path: the client never reached the backend. Verify
   the address is an **active** line in the credential/config store — a commented or `# ARCHIVED:` line reads as
   present in grep and is absent at runtime.
6. **Do not kill a process you have not classified.** Check whether it is launchd/registered before calling it
   stale; a managed process respawns and the kill hides the real cause. If you must remove something, name the
   classification that justified it.
7. **Distinguish "necessary" from "sufficient" checks.** Permissions, signatures, and versions passing does not
   clear a separate startup path. When both are true — green health, dead tool — the failure is in the layer the
   health check does not cover; go measure that layer.
8. **Retract a wrong cause in the open.** A wrong attribution reaches the user and may be acted on. State the
   correction plainly rather than silently moving on.
9. **Report the working method plus the fix, never "tool X is broken".** Environment and version facts go stale;
   the layer-isolation method and the budget arithmetic do not.

## Procedure

### 1. Read the tool's error verbatim, then the code that raises it

Find the raising line in the backend module. The message names the check that failed, which names the layer:

```bash
grep -rnE 'startup timed out|backend unavailable|did not become ready' <module>/
```

Then read the constants and the probe it calls. Note every timeout in that path — per-probe and total.

### 2. Get the health view for free, and treat it as partial

```bash
hermes computer-use doctor          # or the tool's own health verb
```

Record which layer it covers. Anything it does not check stays suspect.

### 3. Reproduce the failing call in isolation, with timing

```python
import time
t = time.monotonic()
try:
    backend.start()                                  # or the tool's probe/run
    print(f"OK in {time.monotonic() - t:.2f}s")
except Exception as e:
    print(f"FAIL in {time.monotonic() - t:.2f}s: {e}")
```

Drain the subprocess stderr the backend captures; a swallowed exception often hides the real diagnostic.

### 4. Bisect the variable you actually suspect

Change one variable per run and keep the timing. Instrument the internal probe rather than the whole call so the
cost per attempt is visible. Compare the same probe with and without the dependency present:

| Probe | Dependency absent | Dependency present |
|---|---|---|
| e.g. `status --socket` | 0.03s | 5.76-13.08s |

A gap like that is the finding. The healthy-looking shell run that also happened to have no dependency alive is
the trap — it "proves" nothing about the failing path.

### 5. Apply the fix, verify with the identical call, then run the suite

Same script from step 3 must flip FAIL -> OK. Then run the project's own test runner (never bare `pytest` in a
project that provides one) over the files touching the module, and record pass/fail/skip counts.

### 6. Report: layers, numbers, and what you deliberately did not touch

State which layer failed, the measurement that isolates it, the fix, the test result, and the restart the user
must perform — module-level constants are read at import, so a running process keeps the old values until it is
restarted.

## Pitfalls

- **Killing "stale" processes as a first move.** Registered/launchd processes respawn; unregistered leftovers may
  be symptoms, not causes. Classify first (registered vs orphaned, socket present vs deleted).
- **Proving a shell command works, then concluding the code path is fine.** The shell differed in a variable that
  mattered — most often whether the dependency was alive at all.
- **Reading a `doctor`/health green as clearance.** It covers permissions and versions; startup budget is a
  separate, unmeasured path.
- **Treating a swallowed/timeout exception as the diagnosis.** It is the wrapper; re-run without the swallow to
  get the real message.
- **Fixing the per-call timeout and leaving the total deadline below one call's cost.** The loop still dies.
- **Committed config values that a running process already loaded.** Say the restart is required; do not report
  the fix as live.
- **Recording a numeric budget as a permanent fact without the measurement next to it.** Future sessions will
  re-measure and overwrite; keep the "how to measure" line so the number stays honest.

## References

- `references/reproduction-recipe.md` — the layered repro harness (shell timing, in-process backend call,
  per-layer probe bisect) with copy-pasteable snippets.
- `references/hermes-tool-layer-map.md` — which layer each common tool error belongs to, and the health verb
  that covers it.
