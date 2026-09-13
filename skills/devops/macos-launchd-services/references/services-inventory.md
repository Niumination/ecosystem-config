# Niumination macOS Service Inventory

Always-on services on Afrizal's Mac (zaryu). All user-scoped LaunchAgents live in
`~/Library/LaunchAgents/` and are NOT in any git repo — they get wiped silently by
any bulk-delete / wrong-directory incident (proven: 27-Agu-2026 jcode wipe).

## Service table

| Service | Port | Plist (in ~/Library/LaunchAgents) | Critical | Notes |
|---|---|---|---|---|
| Hermes Gateway | ephemeral (cmd-line `--replace`) | `ai.hermes.gateway.plist` | ✅ | `KeepAlive`+`RunAtLoad`; process cmd: `hermes_cli.main gateway run --replace`; spawns MCP watchdogs (github, filesystem); on boot/login, gateway may start before DNS/network is ready → use `wait-for-network.sh` wrapper (see below) |
| 9router (model router) | 20128 | `com.9router.autostart.plist` | ✅ | auto-restart; ALL 5 Telegram channels (1/802/803/804/1172) route here; CLI tray = `/usr/local/bin/mcp-server`? (actually `/usr/local/lib/node_modules/9router/cli.js --tray`) |
| 9router cache-watch | — | `com.niumination.9router-watch.plist` | ⚪ | NON-CRITICAL; `launchctl load` often fails I/O; safe to leave dead |
| Mission Control UI | 5200 | `com.niumination.missioncontrol.plist` | ⚠️ | Next.js `apex-ui` (`services/niu-mission-control/apex-ui`); if status `-9` it was SIGKILLed; FastAPI backend is a SEPARATE process not covered by this plist |
| No-sleep (caffeinate) | — | `com.niumination.nosleep.plist` | ✅ | `caffeinate -s -d -i -m`; prevents Mac sleep; lost in 27-Agu wipe, recreated this session |

## Health commands (copy-paste)

```bash
# ports
lsof -iTCP:20128 -sTCP:LISTEN -P -n      # 9router
lsof -iTCP:5200  -sTCP:LISTEN -P -n      # Mission Control UI
# launchd state
launchctl list | grep -iE "9router|missioncontrol|nosleep|hermes"
# processes
pgrep -fl caffeinate
pgrep -fl "hermes_cli.main gateway"
# live response
curl -s -o /dev/null -w "%{http_code}" -m 8 http://localhost:20128/v1/models
curl -s -o /dev/null -w "%{http_code}" -m 5 http://localhost:5200/
# no-sleep assertion (must show caffeinate preventing sleep)
pmset -g assertions | grep -i "PreventUserIdleSystemSleep"
pmset -g | grep sleep
```

## Restart recipes
```bash
launchctl kickstart -k gui/$(id -u)/com.9router.autostart        # 9router
launchctl kickstart -k gui/$(id -u)/com.niumination.nosleep       # caffeinate
launchctl load ~/Library/LaunchAgents/com.niumination.nosleep.plist  # first-time only
```

## Backup recommendation
After creating any plist, back it up so an incident can't wipe it:
```bash
cp ~/Library/LaunchAgents/com.niumination.*.plist ~/Desktop/Niumination/dotfiles/launchagents/ 2>/dev/null || echo "make that dir first"
```
