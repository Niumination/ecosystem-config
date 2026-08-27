# 9Router Crash-Loop Fix — 2026-08-27

## Symptom
9router (local LLM gateway on :20128) in infinite crash loop: launchd `KeepAlive`
restarted it 130+ times, each printing `Exiting...` then dying. opencode/jcode
model calls via `baseURL: http://127.0.0.1:20128/v1` failed. Temp spiked to 85C.

## Root cause
9router CLI shows an **interactive TUI menu** to pick interface (web/terminal/tray/exit).
Launchd runs with no TTY (stdin=/dev/null) → menu reads EOF → selects "exit" →
`cleanup()` kills its own server child → process exits → KeepAlive restarts → loop.

Earlier it worked because it was launched *with* a TTY into tray mode.

## Fix
Launch with `--tray --skip-update` (skips menu, keeps server alive under launchd).
Updated `~/Library/LaunchAgents/com.9router.plist` ProgramArguments:
  node 9router --tray --skip-update --no-browser --port 20128 --host 127.0.0.1

## Verify
- `launchctl list | grep 9router` → running
- `lsof -iTCP:20128 -sTCP:LISTEN` → listening
- `curl localhost:20128/v1/models` → model list
- chat probe via `gratislonggar` combo → streams OK
