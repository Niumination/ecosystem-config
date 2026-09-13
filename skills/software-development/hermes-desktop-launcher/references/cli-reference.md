# Hermes Desktop CLI Reference

This file contains condensed CLI reference for Hermes Desktop commands.

## Main Commands

```bash
# Launch desktop app
hermes desktop
hermes gui  # alias

# Start dashboard (web admin panel)
hermes dashboard

# Check desktop status
hermes desktop --status
```

## Options

| Flag | Description |
|------|-------------|
| `--cwd <path>` | Set working directory for desktop |
| `--profile <name>` | Use specific profile |
| `--host <addr>` | Bind address (default: 127.0.0.1) |
| `--port <n>` | Port for dashboard |
| `--stop` | Stop running dashboard |
| `--status` | Show dashboard status |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HERMES_DESKTOP_CWD` | Working directory override |
| `HERMES_HOME` | Custom Hermes home directory |
| `HERMES_DESKTOP_DEV_SERVER` | Dev server URL (for development) |

## Common Issues

### App Won't Launch
```bash
# Check if already running
pgrep -f "Hermes.app"

# Kill and restart
pkill -f "Hermes.app"
open /Applications/Hermes.app
```

### Config Not Loading
```bash
# Verify Hermes home
echo $HERMES_HOME
ls -la ~/.hermes/config.yaml
```

### Permission Issues
```bash
# Fix Gatekeeper blocking
xattr -cr /Applications/Hermes.app
```

## See Also

- Official docs: https://hermes-agent.nousresearch.com/docs/user-guide/desktop
- Full CLI reference: see `hermes-agent` skill
