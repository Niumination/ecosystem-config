# macOS Gateway Lifecycle — Marker Files, Launchd Agents, and Restart Blocking

## Startup Notification Mechanism

`_send_home_channel_startup_notifications` (gateway/run_notifications.py) only fires when marker
`~/.hermes/.restart_pending.json` exists. The marker is created by `/restart` and `hermes update`,
NOT by normal launchd boot. Result: after a Mac reboot, the gateway starts silently and the user
receives no "Gateway Online" ping.

**Marker format:**
```json
{"platform":"telegram","chat_id":"<chat_id>","thread_id":null,"user_id":"<user_id>","source_platform":"telegram"}
```

**Fix pattern — launchd agent that writes marker before gateway starts:**
1. Create `~/.hermes/scripts/mark-gateway-restart.sh` that waits for `~/.hermes/gateway.sock` (max 60s),
   then writes the marker JSON.
2. Create `~/Library/LaunchAgents/ai.hermes.gateway-marker.plist` with `RunAtLoad=true` pointing at the script.
3. Load with `launchctl load`.

On next boot: launchd runs marker script → marker written → gateway starts → reads marker → sends
notification → clears marker. Idempotent; safe to leave loaded.

## Gateway Restart Blocking

The gateway **blocks restart/stop/kill operations issued from inside its own process tree**.
`hermes gateway restart`, `kill <gateway-pid>`, and `launchctl stop` all fail with:
`"Blocked: command or referenced script cannot restart, stop, or uninstall the gateway from inside the gateway process."`

This is by design — the gateway would SIGTERM its own child commands before they complete.

**Rule:** Any operation that restarts or kills the gateway MUST be run from a separate shell
outside the gateway process (Terminal.app, kitty, SSH session). Never attempt from inside a Hermes
chat session.

**Safe restart sequence from external shell:**
```bash
kill $(pgrep -f "hermes_cli.main gateway")   # launchd revives via KeepAlive=true
# wait ~30s (ThrottleInterval) for revival
```

## Diagnostic Commands

```bash
# Check if startup notification was sent
grep "Sent home-channel startup notification" ~/.hermes/logs/gateway.log | tail -3

# Check if marker exists
ls -la ~/.hermes/.restart_pending.json 2>&1

# Check launchd marker agent status
launchctl list | grep ai.hermes.gateway-marker

# Verify gateway socket (confirms gateway is alive)
ls -la ~/.hermes/gateway.sock
```

## Pitfall: Marker Written After Gateway Start

If the marker script runs AFTER the gateway has already passed the startup-notification gate, the
marker is written but never consumed — it sits on disk and fires a spurious notification on the
NEXT restart. Mitigation: the script waits for `gateway.sock` (which appears ~1s before the
notification gate), ensuring the marker is written in time. If you observe a notification firing
on a restart you didn't expect, check for stale markers with `ls -la ~/.hermes/.restart_pending.json`.
