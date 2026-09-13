# OpenCode Go — Workspace & Key Quirks

## Session 2026-08-31: SAPA Smart AI Migration Attempt

### Problem
User wanted to switch SAPA Smart AI from OpenCode Zen to OpenCode Go for better model quality.

### Key Findings

**1. Workspace-scoped keys**
- API keys are bound to specific workspaces
- Key from workspace A does NOT work for workspace B
- Error pattern:
  - `AuthError`: key doesn't belong to this workspace
  - `RegionError`: model needs opt-in in workspace settings
  - `CreditsError`: payment method not set for workspace

**2. Key types matter**
- Key `sk-VUc...` (from Hermes): works for `/models` endpoint but NOT for `/chat/completions`
- Key `sk-8qZ...` (OPENCODE_API_KEY): works for chat but linked to OLD workspace
- Solution: Generate NEW key specifically in the Go workspace settings

**3. Payment method required per workspace**
- Subscription ≠ payment method attached
- Must manually add card at: `https://opencode.ai/workspace/<workspace-id>/billing`
- Without payment: all chat endpoints return `CreditsError`

**4. OpenCode Go API was DOWN during this session**
- Issue tracked: https://github.com/anomalyco/opencode/issues/35276
- All POST to `/zen/go/v1/chat/completions` returned 500
- Workaround: fallback to Zen free tier (`nemotron-3-ultra-free`)

### Resolution
- Kept OpenCode Zen (`nemotron-3-ultra-free`) as production provider
- Documented Go setup for future when API recovers

### Verification Commands
```bash
# Test key validity for models
curl -s https://opencode.ai/zen/go/v1/models \
  -H "Authorization: Bearer $KEY"

# Test chat (may fail if API down)
curl -s -X POST https://opencode.ai/zen/go/v1/chat/completions \
  -H "Authorization: Bearer $KEY" \
  -d '{"model":"deepseek-v4-flash","messages":[...],...}'
```

### Related
- Zen endpoint (still works): `https://opencode.ai/zen/v1`
- Go endpoint (was down): `https://opencode.ai/zen/go/v1`
