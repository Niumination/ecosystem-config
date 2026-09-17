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

### 3. Remove redundant launch agents

If multiple agents run the same script:

```bash
# List agents
launchctl list | grep <script-name>

# Remove redundant agent
launchctl unload ~/Library/LaunchAgents/com.niumination.<redundant>.plist
rm ~/Library/LaunchAgents/com.niumination.<redundant>.plist
```

### 4. Reload primary agent

```bash
launchctl unload ~/Library/LaunchAgents/com.niumination.<primary>.plist
launchctl load ~/Library/LaunchAgents/com.niumination.<primary>.plist
```

## Pitfalls

- **Don't notify on every change.** Polling scripts that trigger notifications on every state change cause spam when the source is unstable. Always debounce.
- **Avoid redundant launch agents.** Two agents running the same script at different intervals causes race conditions. Consolidate to one agent.
- **Use WatchPaths for file-based triggers.** If the trigger is a file change, use `WatchPaths` instead of `StartInterval` for efficiency.
- **Set appropriate intervals.** 60s is too aggressive for most polling. 300s (5 min) is usually sufficient.
- **Clear debounce markers on stable state.** When the value returns to the previous stable hash, clear the debounce marker to avoid false positives.

## Verification

```bash
# Check agent status
launchctl list | grep <script-name>

# Monitor logs for 2-3 cycles
tail -f ~/.cache/niumination/<script>.log
```
