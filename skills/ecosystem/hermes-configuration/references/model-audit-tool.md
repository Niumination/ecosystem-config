# Model Audit Tool — `hermes_model_audit.py`

Location: `~/Desktop/Niumination/scripts/hermes_model_audit.py`

Purpose: Read Hermes runtime model state from `~/.hermes/state.db` and report actual active models per session/channel.

## When to Use

Run this script BEFORE answering any question about runtime model state:
- "what model is active in channel X"
- "which model am I currently using"
- "report all active models"
- When troubleshooting model-related errors (wrong model, quota exceeded)
- Before making config changes (know current runtime state first)

## Usage

```bash
python3 ~/Desktop/Niumination/scripts/hermes_model_audit.py
```

## Output

Lists all active sessions (DM, group channels, cron, delegations) with:
- Session key and display name
- Actual model and provider
- Last activity timestamp

## Why This Exists

Config.yaml contains DEFAULTS only. Runtime state lives in state.db. Every session can override model via:
- `/model` switch
- Telegram channel overrides
- Delegation defaults
- Cron job settings

A session's actual model can differ from config.yaml without any config change. Reading config.yaml to answer runtime questions produces wrong answers that cause user harm.

## Implementation Notes

- Reads `~/.hermes/state.db` sessions table
- Filters to sessions active in last 7 days
- Groups by DM vs group channels
- Compares against config.yaml default for drift detection
