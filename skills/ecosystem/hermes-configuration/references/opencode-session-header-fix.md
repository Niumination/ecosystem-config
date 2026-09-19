# OpenCode Go Session Header Fix (2026-09-18)

## Problem

OpenCode Go API requires `x-opencode-session` header on every request. Without it:
```
HTTP 400: MissingSessionID — Request is missing x-opencode-session
```

## Solution for External Apps (e.g., sapa-ai)

Add `customHeaders` to your AI client config and pass `x-opencode-session` header.

### Implementation Pattern

```typescript
// 1. Add to config interface
interface AiConfig {
  customHeaders?: Record<string, string>;
}

// 2. Merge into request headers
function headers(cfg: AiConfig): Record<string, string> {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${cfg.apiKey}`,
    ...cfg.customHeaders,
  };
}

// 3. Load from env var (JSON)
customHeaders: process.env.AI_CUSTOM_HEADERS 
  ? JSON.parse(process.env.AI_CUSTOM_HEADERS) 
  : undefined,
```

### Env Var Setup (Vercel)
```
AI_CUSTOM_HEADERS={"x-opencode-session": "your-session-id"}
```

## How to Obtain Session ID

- Log into OpenCode dashboard / app
- Check network requests to find `x-opencode-session` header value
- Or follow: https://opencode.ai/docs

## Applicability

- OpenCode Go API (`/zen/go/v1`)
- OpenCode Zen API (`/zen`)
- NOT Nous Portal (separate auth mechanism)
- NOT 9router (different provider)

## Related Pitfall

hermes-configuration skill — **Pitfall 27: OpenCode 400 MissingSessionID** covers the same issue for Hermes native provider configuration.