---
name: polling-script-management
description: "Stop polling script notification spam via debounce."
version: "1.0.0"
author: Niumination (Afrizal Munthe)
license: MIT
platforms: [macos, linux]
tags: [polling, launchd, debounce, notifications, niumination]
---

# Polling Script Management

Manage polling scripts and launch agents to prevent notification spam and resource waste.

## Trigger

User reports notification spam, excessive polling, or resource waste from a scheduled script.

## Procedure

### 1. Diagnose the polling pattern

Check logs for frequency of changes:

```bash
tail -n 20 ~/.cache/niumination/<script>.log
```

Look for flip-flop patterns (value A → B → A → B) that indicate unstable state.

### 2. Add debounce logic

Two different problems both look like "the script is too noisy" and they need different fixes. Pick
by asking **where the instability lives**:

| Symptom | Instability is | Fix |
|---|---|---|
| Value settles, but notification fires on each wobble | in the *notification* | debounce on time (this section) |
| Source genuinely alternates (A → B → A) between reads | in the *source* | require two agreeing reads (next section) |

Time-based debounce only helps if the value eventually settles. If the source itself alternates — a
catalogue that loses and regains a whole provider, an upstream that errors and recovers — a debounce
window just picks whichever sample happened to land last, then rewrites the target again on the next
wobble.

Modify the script to:
1. Record timestamp of first change
2. Only commit/notify if change persists for DEBOUNCE_WINDOW seconds
3. Clear marker when state stabilizes

```bash
# Debounce variables
STABLE_FILE="$CACHE_DIR/<script>.stable"
DEBOUNCE_WINDOW=120  # seconds

# On change detection
NOW=$(date +%s)
LAST_CHANGE=0
[ -f "$STABLE_FILE" ] && LAST_CHANGE=$(cat "$STABLE_FILE")

if [ "$LAST_CHANGE" = "0" ] || [ $((NOW - LAST_CHANGE)) -ge $DEBOUNCE_WINDOW ]; then
  echo "$NOW" > "$STABLE_FILE"
  exit 0  # First change or window passed — record but don't notify
fi

# Stable for DEBOUNCE_WINDOW — commit change
```

### 2b. Require two agreeing reads (unstable source)

When the source itself alternates between reads, take the reading N times with a short gap and act
**only if two consecutive reads are identical**. A source still moving returns "unknown" — and
"unknown" must mean *skip this run silently*, never *write the last value seen*. The next scheduled
run catches the settled value; nothing is lost, because the target only needs to end up correct, not
to be corrected at the first opportunity.

```python
previous = None
for i in range(3):
    current = read_source()          # returns None on error
    if current is None:
        return None                  # unreachable → skip, do not act
    if previous is not None and current == previous:
        return current               # two agreeing reads → trustworthy
    previous = current
    time.sleep(3)
return None                          # still moving → skip this run
```

**Verify the source is actually unstable before building this** — read it several times in a row and
compare. If the direct provider endpoint is stable while the aggregated endpoint flaps, the
instability is in the aggregation layer and the guard belongs at the aggregation read.

### 2c. Do not re-read the source to verify your own write

After writing, verify the bytes **on disk** against the same snapshot that drove the write — never by
fetching the source a second time. On a flapping source the second read can differ from the first and
fail a job that did exactly the right thing. The check is "did my write land?", not "is the source
still saying the same thing?"

### 3. Stay silent when there is nothing to say

A periodic job that prints "unchanged" every run turns a quiet channel into noise. Exit 0 with **no
stdout** when nothing changed; emit output only when something actually changed or failed. With
`hermes cron --no-agent`, empty stdout is delivered as nothing — this is the contract that makes a
30-minute watchdog tolerable.

### 4. Remove redundant launch agents

If multiple agents run the same script:

```bash
# List agents
launchctl list | grep <script-name>

# Remove redundant agent
launchctl unload ~/Library/LaunchAgents/com.niumination.<redundant>.plist
rm ~/Library/LaunchAgents/com.niumination.<redundant>.plist
```

### 5. Reload primary agent

```bash
launchctl unload ~/Library/LaunchAgents/com.niumination.<primary>.plist
launchctl load ~/Library/LaunchAgents/com.niumination.<primary>.plist
```

## Pitfalls

- **Don't notify on every change.** Polling scripts that trigger notifications on every state change cause spam when the source is unstable. Always debounce.
- **Debounce is the wrong fix for a genuinely alternating source.** Time-based debounce assumes the
  value settles; when the source itself flips between reads, debounce merely delays the noise. Require
  two agreeing reads instead, and treat "still moving" as skip — not as "write what I last saw".
- **Never verify a write by re-reading the source.** A flapping source will disagree with the snapshot
  you wrote from and fail a healthy run. Verify the artefact on disk against the snapshot that drove
  the write.
- **A polling job that always prints something is noise.** Emit nothing when nothing changed.
- **Avoid redundant launch agents.** Two agents running the same script at different intervals causes race conditions. Consolidate to one agent.
- **Use WatchPaths for file-based triggers.** If the trigger is a file change, use `WatchPaths` instead of `StartInterval` for efficiency.
- **Set appropriate intervals.** 60s is too aggressive for most polling. 300s (5 min) is usually sufficient.
- **Clear debounce markers on stable state.** When the value returns to the previous stable hash, clear the debounce marker to avoid false positives.
- **Prefer an explicit delivery target over `origin` for periodic jobs.** `origin` means the context the
  job was *created* in, so a watchdog created from the wrong thread keeps posting there forever. See
  `scheduled-job-delivery-routing`.

## Verification

```bash
# Check agent status
launchctl list | grep <script-name>

# Monitor logs for 2-3 cycles
tail -f ~/.cache/niumination/<script>.log
```
