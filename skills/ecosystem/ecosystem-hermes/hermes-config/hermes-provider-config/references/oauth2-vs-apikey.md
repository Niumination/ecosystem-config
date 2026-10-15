# OAuth2 vs API-Key Providers in Hermes

## The Two Mechanisms

Hermes Agent supports two distinct provider authentication mechanisms. Understanding which applies to which provider is essential for configuration and debugging.

### API-Key Providers

**Characteristics:**
- Authenticate via static API key
- Key stored in environment variable
- Configuration lives in `config.yaml` under `providers:` section
- Example providers: 9router, OpenRouter, AgentRouter (when working)

**Config.yaml structure:**
```yaml
providers:
  provider-name:
    base_url: https://api.example.com/v1
    api_mode: chat_completions
    key_env: PROVIDER_API_KEY_ENV_VAR
```

**How Hermes resolves the key:**
1. Reads `key_env` value from config.yaml (e.g., "OPENROUTER_API_KEY")
2. Looks up that env var in the process environment
3. Uses the value as the Bearer token in API requests

### OAuth2 Providers

**Characteristics:**
- Authenticate via OAuth2 access tokens + refresh tokens
- Token state managed outside config.yaml (via `hermes auth` commands)
- NOT listed in `config.yaml` `providers:` section
- Example provider: Nous Portal

**Where auth state lives:**
- Access token, refresh token, expiry stored in Hermes auth state (not config.yaml)
- Managed via `hermes auth add <provider>`, `hermes auth status`, `hermes auth reset <provider>`
- Referenced by provider name (e.g., "nous") in model_catalog.json and session overrides

**Why OAuth2 providers don't appear in config.yaml:**
The `providers:` section in config.yaml is specifically for API-key-based providers. OAuth2 providers use a different code path that reads from auth state, not from config.yaml.

## How Hermes Decides Which Mechanism to Use

When Hermes needs to make a request to a provider:

1. **Check if provider is in config.yaml `providers:` section**
   - If yes → use API key from env var
   - If no → check if it's an OAuth2 provider

2. **For OAuth2 providers:**
   - Look up auth state via `hermes auth` subsystem
   - Use access token if valid, refresh if expired
   - Fail if no valid token available

3. **Model selection:**
   - Model choice can come from config default, channel override, or session override
   - Session overrides stored in state.db can persist provider references

## Common Confusion Points

### "Why isn't Nous Portal in config.yaml?"
Because it's OAuth2. Look in `model_catalog.json` → `providers.nous` and check auth via `hermes auth status`.

### "I added a provider to config.yaml but it still doesn't work"
Check: Is it really an API-key provider? If it uses OAuth2, config.yaml won't help — you need `hermes auth add`.

### "Provider works in some sessions but not others"
Session-level `/model` overrides in state.db can persist provider references. Check:
```bash
sqlite3 state.db "SELECT session_key, model FROM gateway_routing WHERE session_key LIKE '%telegram%';"
```

## Debugging Provider Issues

1. **Identify provider type:**
   - API-key: has `base_url` + `key_env` in config.yaml
   - OAuth2: not in config.yaml, has entry in model_catalog.json providers

2. **For API-key providers:**
   - Check config.yaml has valid `base_url`
   - Check env var is set: `echo $ENV_VAR`
   - Test connectivity: `curl $base_url/v1/models -H "Authorization: Bearer $ENV_VAR"`

3. **For OAuth2 providers:**
   - Check auth state: `hermes auth status`
   - Re-auth if needed: `hermes auth add <provider>`
   - Check model_catalog.json has the provider entry

## Adding a New Provider

### If it's API-key based:
1. Add entry to `config.yaml` `providers:` section
2. Set env var with the API key
3. Optionally add to model_catalog.json if it's a known provider

### If it's OAuth2 based:
1. Use `hermes auth add <provider>` to authenticate
2. Verify model_catalog.json has the provider (or add it)
3. Model selection via config default or session override

## Reference
- `references/model-catalog-structure.md` — model_catalog.json schema details
