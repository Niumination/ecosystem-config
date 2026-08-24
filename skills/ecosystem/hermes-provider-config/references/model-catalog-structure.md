# Model Catalog JSON Structure

## Location
`/Volumes/HermesAgent/HermesAgentUSB/data/cache/model_catalog.json`

## Top-Level Schema
```json
{
  "version": "<semver>",
  "updated_at": "<unix timestamp>",
  "metadata": {...},
  "providers": ["openrouter", "nous", ...],
  "provider": {
    "<provider_name>": {
      "metadata": {
        "display_name": "Human-readable name",
        "note": "Additional info about free-tier gating, etc."
      },
      "models": [
        {"id": "model-id", "default": true},
        ...
      ]
    }
  }
}
```

## Provider Entry: Nous Portal Example
```json
{
  "nous": {
    "metadata": {
      "display_name": "Nous Portal",
      "note": "Free-tier gating is determined live via Portal pricing..."
    },
    "models": [
      {"id": "anthropic/claude-fable-5"},
      {"id": "anthropic/claude-opus-5"},
      {"id": "openai/gpt-5.5"},
      {"id": "z-ai/glm-5.2", "default": true},
      ...
    ]
  }
}
```

## Key Points
- The `providers` array at top level lists ALL known providers (both API-key and OAuth2)
- Provider entries under `provider.` can be either type
- `default: true` marks which model Hermes uses when user never picked one
- Free-tier gating for Nous Portal is determined live, not from this manifest
- TTL is 1 hour (configurable via `model_catalog.ttl_hours` in config.yaml)
- Auto-fetch enabled when `model_catalog.enabled: true`

## When to Use This File
- Investigating which models are available for a given provider
- Understanding why a model "disappeared" (catalog wasn't refreshed)
- Debugging "model not found" errors — check if model is in catalog
- Adding a new provider — you'll need to add it here AND in config.yaml (for API-key) or hermes auth (for OAuth2)
