# Live state vs cached snapshot

Three ways a reported number stops describing the system, all of which render as a confident,
well-formatted figure rather than an error.

## 1. The reporter reads a cache, not the service

A state/lock file the service last wrote is a snapshot. A reporter that pulls its number from it
prints what was true when the cache was written, indefinitely.

Probe the live endpoint and diff it against the cache:

```
curl -s -m 10 http://127.0.0.1:<port>/<models-path> -o /tmp/live.json
python3 -c "import json;print('live:',len(json.load(open('/tmp/live.json'))['data']))"
python3 -c "import json;d=json.load(open('<state.json>'));print('cache:',d['count'],'at',d['updated_at'])"
```

Set difference both ways, not just totals — the totals can match while membership churns:

```
state-only: sorted(set(cache) - set(live))   # retired
live-only:  sorted(set(live) - set(cache))    # newly appeared
```

When they disagree, **the cache's staleness is the finding and the reporter is what to fix.** Report
both numbers plus the cache's own timestamp. Never publish the cached number alone, and never
normalize the cache to match the probe — the cache is derived output; regenerate it.

## 2. A self-healing "create if missing" path duplicates instead of no-opping

An ensure-exists repair whose presence check misses adds a member on every run.

Snapshot before and after — invoking the tool is itself a mutation:

```
hermes cron list 2>&1 | grep -c '<name>'    # before
hermes <tool>                                 # the "verification" run
hermes cron list 2>&1 | grep -c '<name>'    # after — must be equal
```

If the count grew, the presence check failed to see a member that exists. Prove the negative case
before trusting green: a member that is present must suppress the create branch. When the check is a
substring/grep over *formatted output*, it is fragile by construction — match on a stable identifier,
and confirm the identifier is actually in that output.

**Never use a self-healing tool as a verification step.** A verifier that creates is not a verifier.
This is how a single "let me confirm" call turns one stale duplicate into two.

## 3. A numeric field's unit is undeclared, so a wrong divisor yields a plausible number

Epoch fields ship as seconds, milliseconds, or microseconds depending on the writer. Dividing by the
wrong power of ten produces a small plausible integer, never an error.

```
date +%s                                     # ~1.79e9  -> seconds
```

Compare the field's magnitude against that anchor before deriving elapsed time. Cross-check against a
source in the same directory that carries an explicit unit (ISO-8601 logs, human-readable markers):
when the derived interval contradicts it, believe the one that declares its unit. Report derived
intervals as `UNCHECKED` until the unit is confirmed — a fabricated duration reads exactly like a
measured fact.
