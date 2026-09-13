---
name: hermes-desktop-launcher
description: "Install Hermes Desktop to /Applications for Launchpad."
tags: [hermes, desktop, macos, launchpad, electron]
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Hermes Desktop Launcher for macOS

Install Hermes Desktop to `/Applications` so it appears in macOS Launchpad and can be launched without terminal.

## When to Use

- User wants Hermes Desktop accessible from Launchpad/Applications folder
- `hermes desktop` only works via terminal command
- Building Hermes from source and want to create a distributable .app
- User mentions "Launchpad", "Applications", or "desktop app" on macOS

## Prerequisites

- Hermes Agent installed (git or pip)
- Node.js v22+ installed (required for Electron build)
- Hermes source code available at `~/src/hermes-agent/` (or wherever cloned)

## Installation Steps

### Method 1: Quick Install (Recommended for git-installed Hermes)

```bash
# Find the pre-built Hermes.app in source
find ~/src/hermes-agent -name "Hermes.app" -path "*/release/*" 2>/dev/null
# Output typically: ~/src/hermes-agent/apps/desktop/release/mac/Hermes.app
```

If `.app` exists:
```bash
sudo cp -R ~/src/hermes-agent/apps/desktop/release/mac/Hermes.app /Applications/
```

### Method 2: Build from Source (if no pre-built .app)

```bash
cd ~/src/hermes-agent
npm run install:desktop  # Install desktop dependencies
cd apps/desktop
npm run dist:mac         # Build macOS .app
# Output: release/mac/Hermes.app
sudo cp -R release/mac/Hermes.app /Applications/
```

### Method 3: Official Installer

Download from https://hermes-agent.nousresearch.com/desktop and run installer.

## Post-Installation

Add terminal aliases to `~/.config/zsh/aliases.zsh`:

```bash
cat >> ~/.config/zsh/aliases.zsh << 'EOF'
# === Hermes Desktop Launcher ===
alias hd='open /Applications/Hermes.app'
alias hermes-desktop='open /Applications/Hermes.app'
alias hermes-gui='open /Applications/Hermes.app'
EOF
```

Reload: `source ~/.zshrc`

## Verification

```bash
# Check installation
ls -la /Applications/Hermes.app
file /Applications/Hermes.app/Contents/MacOS/Hermes

# Test launch
open /Applications/Hermes.app

# Verify process running
pgrep -f "Hermes.app" | head -3
```

## Pitfalls

- **No sudo needed if already in /Applications**: Check if user already has Hermes.app elsewhere
- **Source mode vs dist**: Development builds use `npm run dev`, production uses `npm run dist:mac`
- **Electron download timeout**: If `npm run builder` hangs on Electron download, check network/firewall
- **Code signing**: Development builds may need `xattr -cr /Applications/Hermes.app` if Gatekeeper blocks
- **Path matters**: Hermes reads `~/.hermes/` for config - ensure `$HERMES_HOME` isn't overridden
- **Build stamp**: Check `~/.hermes/desktop-build-stamp.json` for build verification

## Files Referenced

- `references/desktop-build-stamp.json` - Build timestamp and hash verification
- `references/cli-reference.md` - CLI command options for `hermes desktop`

## Related Skills

- `hermes-agent` - General Hermes configuration and usage
- `dotfiles-maintenance` - Adding aliases to shell configs
