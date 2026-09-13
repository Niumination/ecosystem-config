# Gateway Network-Wait Fix — 2026-08-30

## Symptom
Hermes Gateway fails to connect to Telegram on the first startup after boot/login:
- gateway logs show `nodename nor servname provided, or not known`
- followed by retries and a later successful reconnect

## Root cause
macOS can start `RunAtLoad` LaunchAgents before DNS/network stack is fully ready.
Network-dependent services therefore try to resolve outbound hostnames too early.

## Fix
Use a small wrapper script before the real service command. The wrapper waits for:
- basic IP reachability
- DNS resolution for an external hostname

Then it starts the real service.

### Files added to `macos-launchd-services`
- `scripts/wait-for-network.sh` — reusable wrapper
- `templates/network-wait-launchagent.plist.xml` — template LaunchAgent using the wrapper
- Hermes Gateway plist backup: `~/Desktop/Niumination/apps/JHermUSB-portable/config/launchd/ai.hermes.gateway.plist`

### Apply to another service
Replace `%LABEL%`, `%TARGET_CMD%`, `%SCRIPT_DIR%`, and `%LOG_DIR%` in the template,
then load via `launchctl`.

## Preferred execution pattern
Generate command bundles with `write_file`, then run them with:
```bash
terminal(command="bash /path/to/generated-script.sh")
```
Do not inline large heredocs or multi-line bash blocks directly in `terminal(command=...)`; Hermes blocks oversized inline payloads and saves them to `~/.hermes/cache/blocked-scripts/`. Using a separate file keeps the command small and re-runnable.

## Verification after deploy
- `launchctl list | grep <label>`
- `pgrep -fl <process>`
- `lsof -iTCP:<port> -sTCP:LISTEN -P -n`
- `curl` probe to a live endpoint, with bounded timeout
- confirm wrapper waits for network/DNS only within a short timeout so boot does not hang indefinitely
