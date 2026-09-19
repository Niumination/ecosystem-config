# AgentRouter Authentication

AgentRouter (`https://agentrouter.org/docs/index.html`) requires a specific header pattern for authentication to work.

## Required Headers (ALL requests)

```
Authorization: Bearer <API_KEY>
Content-Type: application/json
User-Agent: hermes-agent/0.19.0    ← THIS HEADER IS REQUIRED
```

Without `User-Agent: hermes-agent/0.19.0`, ALL endpoints return `401 Unauthorized` regardless of correct credentials.

## Model Response Codes

| Model | Response | Meaning |
|-------|----------|---------|
| `glm-5.3` | 200 OK | Free, usable |
| `deepseek-v4-flash` | 200 OK | Free, usable |
| `gpt-6-astra` | 402 Payment Required | Need top-up |
| `gpt-5.6-sol` | 402 Payment Required | Need top-up |
| `claude-opus-5` | 402 Payment Required | Need top-up |
| `claude-opus-4-8` | 402 Payment Required | Need top-up |

## Top-Up

402 models need token purchase at `https://ps.air-outer.com/console/token`.

## System Access Token

A system access token (`bJlvZAq0Wsgsu7JyQ44bgc607s7rLrY=`) may be required for certain endpoints alongside the API key. Store both in `vault/agentrouter-key.md`.

## Storage Location (Niumination ecosystem)

- `vault/agentrouter-key.md` — API key + system token
- `~/.hermes/.env` — `AGENTROUTER_API_KEY`, `AGENTROUTER_SYSTEM_TOKEN`
- `secrets.zsh`, `hermes.env.bak` — rotated copies
