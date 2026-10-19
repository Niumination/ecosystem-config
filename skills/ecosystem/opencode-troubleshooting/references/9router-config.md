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

## Verification

```bash
opencode run --model 9router/nous/meituan/longcat-2.5-preview:free "Reply with exactly: OK"
```

## File Permissions

Config contains API key — set to 600:
```bash
chmod 600 ~/.config/opencode/opencode.json
```
