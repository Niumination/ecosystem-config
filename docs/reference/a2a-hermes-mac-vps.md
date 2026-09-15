# A2A Hermes — Mac ↔ VPS Connection Guide

> **Status:** REFERENCE (belum diimplementasikan)
> **Dibuat:** 2026-09-14
> **Protokol:** A2A v1.0 (Agent2Agent, Linux Foundation)

---

## Topology

```
┌─────────────────────────┐          ┌──────────────────────────────┐
│  Hermes Mac (lokal)     │  A2A     │  Hermes VPS (103.30.146.232)│
│  IP: 10.209.232.108    │ ◄──────► │  SSH: port 4422              │
│  A2A port: 9900        │  :9900   │  A2A port: 9900              │
│  Role: client + server  │          │  Role: server                │
└─────────────────────────┘          └──────────────────────────────┘
```

---

## Prerequisites

| Komponen | Mac | VPS |
|----------|-----|-----|
| Hermes version | v0.21.1+ | v0.21.1+ |
| A2A plugin | built-in | built-in |
| Network | outbound to VPS:9900 | inbound :9900 open |
| Token | same on both sides | same on both sides |

---

## Implementation Steps

### Step 1 — VPS (server)

Edit `~/.hermes/config.yaml`:
```yaml
gateway:
  platforms:
    a2a:
      enabled: true
      extra:
        port: 9900
```

Set environment variables:
```bash
export A2A_HOST=0.0.0.0
export A2A_BEARER_TOKEN="<generate-32-char-random>"
export A2A_PUBLIC_URL="http://103.30.146.232:9900"
```

Enable toolset + restart:
```bash
hermes tools enable a2a --platform a2a
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

Verify:
```bash
curl http://103.30.146.232:9900/.well-known/agent-card.json
```

### Step 2 — Mac (client)

Enable a2a tools:
```bash
hermes tools enable a2a --platform telegram
hermes tools enable a2a --platform cli
```

Register VPS peer in `~/.hermes/config.yaml`:
```yaml
a2a_agents:
  vps-mata:
    url: "http://103.30.146.232:9900"
    auth:
      type: bearer
      token: "<same-token-as-vps>"
    timeout: 120
    capabilities: [coding, research, vps-ops, git, deployment]
```

Restart gateway:
```bash
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

### Step 3 — Verification

From Mac terminal:
```bash
curl http://103.30.146.232:9900/.well-known/agent-card.json
```

From Hermes chat:
```
"Discover agent di http://103.30.146.232:9900"
"Ask vps-mata to run git log in repo mata-aihackfest-2026"
```

---

## Usage Examples

### Mac → VPS (outbound call)
```
"Ask vps-mata to pull the latest changes in mata-aihackfest-2026"
"Ask vps-mata to check the MATA dashboard status"
"Ask vps-mata to run a probe on INAPROC API"
```

### VPS → Mac (inbound call)
Requires tunnel (Tailscale / Cloudflare) since Mac is behind NAT.

---

## Security Rules

| Rule | Implementation |
|------|---------------|
| Token | Min 32 chars, random, same on both sides |
| Firewall | VPS:9900 allow only Mac IP |
| No public exposure | Mac A2A stays localhost unless tunneled |
| Audit | All exchanges logged to `~/.hermes/a2a_audit.jsonl` |
| Anti-loop | Max 5 ping-pong turns per context |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `401 Unauthorized` | Token mismatch — check `A2A_BEARER_TOKEN` on VPS |
| `Connection refused` | VPS A2A not running — check `hermes gateway status` |
| Card not reachable | Check firewall / `A2A_PUBLIC_URL` setting |
| Timeout | Increase `timeout` in peer config |

---

## Reference

- Official docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a
- A2A Protocol: https://a2a-protocol.org/
- Config reference: `hermes config show` → gateway.platforms.a2a
