# 9router as Local Free Provider for OpenCode

## Working Config

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "9router": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "9router (Local, Free)",
      "options": {
        "baseURL": "http://localhost:20128/v1",
        "apiKey": "<real-key-from-.hermes-.env>"
      },
      "models": {
        "nous/meituan/longcat-2.5-preview:free": {
          "name": "Longcat 2.5 Preview (Free)"
        },
        "nous/meituan/longcat-2.0:free": {
          "name": "Longcat 2.0 (Free)"
        },
        "nous/stepfun/step-5-preview:free": {
          "name": "Step 5 Preview (Free)"
        },
        "nous/upstage/solar-mini4:free": {
          "name": "Solar Mini4 (Free)"
        }
      }
    }
  },
  "model": "9router/nous/meituan/longcat-2.5-preview:free",
  "ignore": [
    ".config/zsh-abbr",
    ".config/opencode/snapshot",
    ".local/share/opencode/snapshot"
  ]
}
```

## Key Points

- 9router runs locally at `http://localhost:20128/v1`
- No external API key needed — uses local key from `~/.hermes/.env`
- Free models available: `nous/meituan/longcat-2.5-preview:free`, `nous/stepfun/step-5-preview:free`, `nous/upstage/solar-mini4:free`
- `combo-delegasi` is a Hermes concept, NOT a 9router model ID — use actual model IDs from `/v1/models`
- Config file: `~/.config/opencode/opencode.json`
- If `opencode.jsonc` exists, it overrides `opencode.json` — disable it with `mv opencode.jsonc opencode.jsonc.disabled`

## Keeping the model catalog in sync

The generic OpenAI-compatible package has no `/v1/models` discovery, so the provider block in
`opencode.json` only lists what is hand-written into it — a stale, partial catalog. The fix is a
**plugin** in `~/.config/opencode/plugins/<id>/index.ts` that polls the gateway every ~30 s and
publishes every model under the provider, so CLI and Desktop share one live catalog.

Verify the catalog is actually in sync rather than assuming the config covers it:

```bash
opencode models | grep -c '^9router/'          # models OpenCode knows about
curl -s http://localhost:20128/v1/models | python3 -c 'import sys,json;print(len(json.load(sys.stdin)["data"]))'   # gateway truth
opencode plugin list                            # plugin registered and loaded
```

Equal counts mean the integration works; a config-only catalog will show a much smaller number.
Confirm with `opencode plugin list` that the plugin is present, and with `opencode reload` after
editing the plugin file.

## Filtering inactive models in the plugin

The plugin publishes **every** model from `/v1/models`, including inactive `off-*` combos and models from dead provider connections. To show only usable models:

1. In `loadModels()`, filter `raw.id.startsWith("off-")` → return [] (skip)
2. 9router does not expose per-model health status — upstream 404s (e.g., `nous/meituan/longcat-2.5-preview:free`) are provider-side, not filterable via the API
3. After editing the plugin: `opencode reload`, then verify `opencode models | grep -c '^9router/'` dropped by the filtered count

## Verification

```bash
opencode run --model 9router/nous/meituan/longcat-2.5-preview:free "Reply with exactly: OK"
```

## File Permissions

Config contains API key — set to 600:
```bash
chmod 600 ~/.config/opencode/opencode.json
```
