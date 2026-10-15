---
name: hermes-a2a-setup
description: Set up or troubleshoot A2A between Hermes instances.
---

# Hermes A2A Setup

## Topology

```
Mac (client + server)  ←──A2A :9900──→  Cloud/VPS (server)
```

Both sides run Hermes with `platforms.a2a.enabled: true`. Each side can act as client (calling peers) and server (receiving calls).

## Prerequisites

- Hermes v0.21.1+ on both sides
- Tailscale (or tunnel) for Mac ↔ cloud connectivity
- Shared Bearer token (min 32 chars, random)
- Token stored in `vault/a2a-token.txt` (Niumination convention)

## Setup Procedure

### 1. Server side (cloud/VPS)

```bash
# Enable A2A platform
hermes config set platforms.a2a.enabled true --force
hermes config set platforms.a2a.extra.port 9900 --force

# Set env vars in launchd (NOT just .env — launchd does not auto-load .env)
launchctl setenv A2A_HOST 0.0.0.0
launchctl setenv A2A_BEARER_TOKEN "<token>"
launchctl setenv A2A_PUBLIC_URL "http://<public-ip>:9900"

# Enable toolset
hermes tools enable a2a --platform cli

# Restart gateway (from separate shell, NOT from inside gateway process)
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

### 2. Client side (Mac)

```bash
# Enable A2A platform
hermes config set platforms.a2a.enabled true --force
hermes config set platforms.a2a.extra.port 9900 --force

# Register peer in config.yaml
hermes config set a2a_agents.<peer-name>.url "http://<server-ip>:9900" --force
hermes config set a2a_agents.<peer-name>.auth.type "bearer" --force
hermes config set a2a_agents.<peer-name>.token "<token>" --force

# Set env vars in launchd
launchctl setenv A2A_HOST <tailscale-ip>
launchctl setenv A2A_BEARER_TOKEN "<token>"

# Enable toolset
hermes tools enable a2a --platform cli
hermes tools enable a2a --platform telegram

# Restart gateway (from separate shell)
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

### 3. Verification

```bash
# Check server is listening
lsof -iTCP:9900 -sTCP:LISTEN
# Expected: 0.0.0.0:9900 or <tailscale-ip>:9900 (NOT localhost:9900)

# Test agent-card from client
curl http://<server-ip>:9900/.well-known/agent-card.json

# Test from Hermes chat
"a2a_discover http://<server-ip>:9900"
```

## Pitfalls

### `hermes tools enable a2a --platform a2a` is WRONG
`a2a` is a **toolset**, not a platform. Valid platforms: `cli`, `telegram`. Using `--platform a2a` silently succeeds but does nothing useful.

### launchd service name uses DOT, not underscore
Correct: `ai.hermes.gateway`
Wrong: `ai.hermes_gateway`
Verify with: `launchctl list | grep hermes`

### `~/.hermes/.env` is NOT auto-loaded by launchd
The gateway runs as a launchd service. Env vars in `.env` are only loaded by the Hermes CLI shell, not by the launchd-managed gateway process. **Always use `launchctl setenv` for A2A env vars** (`A2A_HOST`, `A2A_BEARER_TOKEN`).

Verify env vars reached the process:
```bash
launchctl getenv A2A_HOST
launchctl getenv A2A_BEARER_TOKEN
```

### Gateway restart from inside gateway process is blocked
Running `launchctl kickstart` from a shell that is a child of the gateway process will fail with SIGTERM propagation. **Always run gateway restart from a separate terminal/shell** that is not spawned by the gateway.

### `platforms.a2a` section must exist in config.yaml
Without `platforms.a2a.enabled: true` and `platforms.a2a.extra.port: 9900`, the A2A server will not start even if toolset is enabled. Check with:
```bash
grep -A3 'platforms:' ~/.hermes/config.yaml | grep -A3 'a2a'
```

### Server binds localhost when A2A_HOST not set
If `A2A_HOST` is not in launchd env, server binds `127.0.0.1:9900` — reachable locally but refused from remote. Symptom: `lsof` shows `localhost:iua (LISTEN)` instead of `0.0.0.0` or Tailscale IP.

## Token Rotation

1. Generate new token: `openssl rand -hex 20`
2. Store in `vault/a2a-token.txt`
3. Update both sides: `launchctl setenv A2A_BEARER_TOKEN "<new-token>"`
4. Restart gateway on both sides
5. Update `vault/README.md` and `docs/registry/a2a-hermes-mac-vps.md`

## References

- `references/a2a-config-examples.md` — full config.yaml snippets for common topologies
