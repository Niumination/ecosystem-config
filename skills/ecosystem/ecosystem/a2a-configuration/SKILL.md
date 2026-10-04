---
name: a2a-configuration
description: Set up and debug A2A Hermes peer connections.
---

# A2A Configuration

## Overview

A2A (Agent2Agent) enables Hermes instances to call each other as peers. Typical setup: Mac (client) ↔ cloud VPS (server) via Tailscale.

## Setup Procedure

### 1. Server side (cloud/VPS)

```bash
# Enable A2A platform
hermes config set platforms.a2a.enabled true --force
hermes config set platforms.a2a.extra.port 9900 --force

# Set env vars
# NOTE: launchd does NOT auto-load ~/.hermes/.env — use launchctl setenv
launchctl setenv A2A_HOST 0.0.0.0
launchctl setenv A2A_BEARER_TOKEN "<40-char-hex>"
launchctl setenv A2A_PUBLIC_URL "http://<public-ip>:9900"

# Enable toolset
hermes tools enable a2a --platform cli
hermes tools enable a2a --platform telegram

# Restart gateway (from separate shell, NOT from inside gateway process)
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

### 2. Client Side (Mac)

```bash
# Register peer
hermes config set a2a_agents.cloud.url "http://<server-tailscale-ip>:9900" --force
hermes config set a2a_agents.cloud.auth.type "bearer" --force
hermes config set a2a_agents.cloud.token "<same-token-as-server>" --force

# Set host bind address (Tailscale IP, NOT 127.0.0.1)
# NOTE: launchd does NOT auto-load ~/.hermes/.env — use launchctl setenv
launchctl setenv A2A_HOST <tailscale-ip>
launchctl setenv A2A_BEARER_TOKEN "<same-token-as-server>"

# Enable toolset
hermes tools enable a2a --platform cli
hermes tools enable a2a --platform telegram

# Restart gateway (from separate shell, NOT from inside gateway process)
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

### 3. Verification

```bash
# From client → server
curl http://<server-ip>:9900/.well-known/agent-card.json

# From server → client (requires A2A_HOST set to Tailscale IP)
lsof -iTCP:9900 -sTCP:LISTEN
# Must show <tailscale-ip>:9900, NOT 127.0.0.1:9900
```

## Token Rotation

1. Generate new token: `openssl rand -hex 20`
2. Store in vault: `echo '<token>' > ~/Desktop/Niumination/vault/a2a-token.txt`
3. Update both sides:
   - Server: `echo 'A2A_BEARER_TOKEN="<token>"' >> ~/.hermes/.env`
   - Client: `hermes config set a2a_agents.cloud.token "<token>" --force`
4. Restart both gateways
5. Update `vault/README.md` and `docs/registry/a2a-hermes-mac-vps.md`

## Pitfalls

### Wrong platform name in `hermes tools enable`
- **Wrong:** `hermes tools enable a2a --platform a2a`
- **Right:** `hermes tools enable a2a --platform cli` (or `telegram`)
- **Why:** `--platform` expects a platform name (cli/telegram), not a toolset name. `a2a` is a toolset, not a platform.

### Wrong launchd service name
- **Wrong:** `ai.hermes_gateway` (underscore)
- **Right:** `ai.hermes.gateway` (dot)
- **Why:** macOS launchd service names use dots, not underscores. Verify with `launchctl list | grep hermes`.

### A2A server not listening
- **Symptom:** `lsof -iTCP:9900 -sTCP:LISTEN` returns empty
- **Cause:** `platforms.a2a.enabled` not set to `true` in config.yaml
- **Fix:** `hermes config set platforms.a2a.enabled true --force` then restart gateway

### A2A server bound to localhost only
- **Symptom:** `lsof` shows `127.0.0.1:9900` instead of `<tailscale-ip>:9900`
- **Cause:** `A2A_HOST` env var not set or set to `127.0.0.1`. For launchd-managed gateway, env vars in `~/.hermes/.env` are NOT auto-loaded — must use `launchctl setenv`.
- **Fix:** `launchctl setenv A2A_HOST <tailscale-ip>` and `launchctl setenv A2A_BEARER_TOKEN <token>`, then restart gateway from a separate shell.

### Gateway restart blocked from inside gateway
- **Symptom:** "Could not find service" or "Blocked: command cannot restart gateway"
- **Cause:** Running `launchctl kickstart` from a shell spawned by the gateway itself
- **Fix:** Run from a separate terminal session, not from a shell spawned by the gateway process

### Gateway restart blocked from inside gateway
- **Symptom:** "Could not find service" or "Blocked: command cannot restart gateway"
- **Cause:** Running `launchctl kickstart` from a shell spawned by the gateway itself
- **Fix:** Run from a separate terminal session, not from a shell spawned by the gateway process

### Gateway restart blocked from inside gateway
- **Symptom:** "Could not find service" or "Blocked: command cannot restart gateway"
- **Cause:** Running `launchctl kickstart` from a shell spawned by the gateway itself
- **Fix:** Run from a separate terminal session, not from a shell spawned by the gateway process

### Token mismatch after rotation
- **Symptom:** `401 Unauthorized` on A2A calls
- **Cause:** Token updated on one side but not the other
- **Fix:** Ensure token is identical on both sides. Store in vault, reference from both configs.

### launchd env vars do not persist across reboot
- **Symptom:** After reboot, A2A server binds to `127.0.0.1` again
- **Cause:** `launchctl setenv` is runtime-only; values are lost after reboot
- **Fix:** Set env vars again after reboot, or add `launchctl setenv` commands to login startup script (e.g. `.zprofile`/login item). Note: `~/.hermes/.env` is NOT auto-loaded by launchd-managed gateway.

## File Locations

| File | Purpose |
|------|---------|
| `~/.hermes/config.yaml` | `platforms.a2a` section, `a2a_agents` peer registry |
| `~/.hermes/.env` | `A2A_HOST`, `A2A_BEARER_TOKEN` |
| `~/Desktop/Niumination/vault/a2a-token.txt` | Token storage (single source of truth) |
| `~/Desktop/Niumination/vault/secrets.zsh` | `A2A_BEARER_TOKEN` export for shell |
| `~/Desktop/Niumination/docs/registry/a2a-hermes-mac-vps.md` | Reference doc |

## References

- Official docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a
- A2A Protocol: https://a2a-protocol.org/
