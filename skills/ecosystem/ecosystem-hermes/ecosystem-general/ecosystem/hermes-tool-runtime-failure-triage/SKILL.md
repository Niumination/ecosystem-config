---
name: hermes-tool-runtime-failure-triage
description: "Use when a Hermes tool errors or times out mid-session."
version: 1.0.0
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [hermes, triage, timeout, backend, daemon, restart, version-drift]
    related_skills: [hermes-configuration, hermes-gateway-dm-troubleshooting, hermes-tool-backend-triage]
---

# Hermes Tool Runtime Failure Triage

## When this applies

A Hermes tool call returns `timeout`, `Connection closed`, `backend unavailable`, or a
startup error — not a config or credential error. The tool worked earlier in the session, or
its `doctor` subcommand reports everything green.

## Order: version drift, then restart state, then code

Check these in order. Each step is cheap and rules out the next.

### 1. Read the tool's own version notice before diagnosing anything

An available-upgrade notice means the binary you are testing is not the one maintainers
recommend, and a stale binary is a sufficient explanation on its own. Upgrade first, then
re-measure. Editing source before upgrading produces a patch for a bug the upgrade already
fixed, and the patch gets harder to justify than the fix was.

```bash
hermes computer-use doctor
hermes computer-use install --upgrade
```

Re-measure the operation that failed and compare against your earlier number before concluding
anything about the code. Only a change that survives the upgrade is a code problem.

### 2. Establish the version of the thing actually running

Upgrade replaced the app bundle, so any daemon spawned from the old bundle is gone while the
long-lived parent still holds a handle to it:

```bash
stat -f '%Sm' -t '%d %b %H:%M:%S' /Applications/CuaDriver.app/Contents/MacOS/cua-driver
ps -o pid,lstart,command -ax | grep -iE 'gateway|serve' | cut -c1-120
ps -o pid,etime,command -ax | grep -c '[c]ua-driver serve'
```

A `Connection closed` where a startup timeout used to appear is the signature of a transport
pointing at a process that no longer exists. Confirm the driver is healthy on its own — start
it standalone, probe it, read the status output — so the missing piece is isolated to the
parent, not the driver.

### 3. Only then compare the parent start time against the last change

```bash
git log --oneline -1 --format='%h %ci'    # when the fix was committed
ps -o lstart= -p <parent-pid>              # when the parent started
```

Constants and config are read at import. A commit landing after the parent's start time is
invisible to the running process regardless of what is on disk. Verify the constant is correct
on disk, then say the restart is required rather than asking the user to guess.

A restart you cannot perform yourself is a real stop, not a formality. If restarting from
inside the parent process is refused, stop and hand that one step to the user, then continue
with everything that does not depend on it.

## Reproduce the code path, not the wrapper

`doctor` and thin wrappers are the first things to lie: they can be green while the real path
fails. Drive the actual function the tool uses, in the project's own interpreter, so timings
and error text are the shipped ones:

```bash
cd <project> && .venv/bin/python -c '<call the real start routine>'
```

A swallowed exception is a second liar. When a probe returns empty, re-run it without the
quiet wrapper to see the exit code and stderr it is hiding — a `None` return is a symptom of
suppression, not of absence.

## Pitfalls

- Do not kill processes before proving they are orphans. Registered launchd entries and
  gateway-spawned daemons are legitimate; a `PPID` of 1 proves reparenting, not abandonment.
- A timeout ceiling below the cost of the operation it waits on guarantees the failure it
  reports, because the loop can never observe success. Measure the operation once, then set
  the ceiling above that measurement and the overall budget above the worst case.
- Prefer fixing the stale-binary cause over widening a budget, and keep the budget change
  only as a guard, labelled as such.
- A tool that hides page contents from its own surface is a separate capability from a
  browser-automation tool, and a decision model on a non-chat endpoint cannot join a
  chat-completions pipeline. Check the wire format before proposing to combine them.
