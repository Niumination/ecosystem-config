# AgentRouter Integration -- Verified 15 Sep 2026

## Current Status: WORKING (native Hermes config, no extension needed)

AgentRouter is a **native Hermes config.yaml provider** (OpenAI-compatible). No TypeScript extension required.

## Credentials (vault: `vault/agentrouter-key.md`)

- API Key: `sk-Od2...Jbmu`
- System Access Token: `bJlvZAq0Wsgsu7JyQ44bgc607s7rLrY=`
- Config section: `providers.agentrouter` in `~/.hermes/config.yaml`

## Auth: TWO things needed (verified 15 Sep 2026)

1. **API Key** via `key_env: AGENTROUTER_API_KEY` in config.yaml + env var in `~/.hermes/.env`
2. **User-Agent header** -- AgentRouter WAF whitelists only `hermes-agent/<version>`. Hermes native `extra_headers` handles this automatically when configured in provider section.

**Without UA header -> 401 `unauthorized client detected`** (WAF blocks curl, Python-OpenAI, hermes-cli UAs).

## Config (verified working)

```yaml
providers:
  agentrouter:
    base_url: https://agentrouter.org/v1
    api_mode: chat_completions
    key_env: AGENTROUTER_API_KEY
    extra_headers: {User-Agent: hermes-agent/0.19.0}
```

## Models (15 Sep 2026 -- `GET /v1/models` = 200, 6 models)

| Model | Status | Notes |
|-------|--------|-------|
| glm-5.3 | OK chat | Working |
| deepseek-v4-flash | OK chat | Working |
| gpt-6-astra | QUOTA 402 | Registered, chat -> Payment Required (needs top-up at console) |
| gpt-5.6-sol | QUOTA 402 | Registered, chat -> Payment Required |
| claude-opus-5 | QUOTA 402 | Registered, chat -> Payment Required |
| claude-opus-4-8 | QUOTA 402 | Registered, chat -> Payment Required |

## Verification

```bash
# Quick probe (MUST include UA):
curl -s -m 15 -H "Authorization: Bearer $AGENTROUTER_API_KEY" \
  -H "User-Agent: hermes-agent/0.19.0" \
  https://agentrouter.org/v1/models | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['data']),'models')"

# Chat test:
curl -s -m 15 -H "Authorization: Bearer $AGENTROUTER_API_KEY" \
  -H "User-Agent: hermes-agent/0.19.0" -H "Content-Type: application/json" \
  -d '{"model":"glm-5.3","messages":[{"role":"user","content":"reply with exactly: OK"}],"stream":false}' \
  https://agentrouter.org/v1/chat/completions
```

## DOCS

- Official docs: `https://ps.air-outer.com/docs/hermes.html`
- Token console: `https://ps.air-outer.com/console/token` (domain DIFFERENT from docs)
- `https://agentrouter.org/docs/index.html` -- general overview

## History

- **13 Aug 2026 (STALE -- superseded):** AgentRouter required custom TS extension, key was unverified, provider removed from config. WRONG as of 15 Sep 2026.
- **15 Sep 2026:** Key + system token rotated (sk-Od2...Jbmu / bJlvZAq0Wsgsu7JyQ44bgc607s7rLrY=). Native config works. 4/6 models return 402 (quota issue, not auth).
