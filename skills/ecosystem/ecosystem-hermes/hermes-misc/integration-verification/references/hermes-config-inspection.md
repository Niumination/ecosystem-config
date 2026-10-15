# Hermes Config Inspection Patterns
**Context:** Auditing Hermes setup, model mapping, provider config, logs, cron.

## Config Inspection
```bash
# Current mapping/cron/provider lines
grep -n -E "model:|provider:|base_url|channel_overrides|cron:|browser:" ~/.hermes/config.yaml | head -40

# Section blocks
grep -A3 "^cron:" ~/.hermes/config.yaml
grep -A6 "^  compression:" ~/.hermes/config.yaml
grep -A4 "^  delegation:" ~/.hermes/config.yaml
grep -A12 "^  channel_overrides:" ~/.hermes/config.yaml
```

## Live Probe
```bash
# Gateway status
hermes gateway status

# Config check
hermes config check

# Provider/model discovery
curl -s http://localhost:20128/v1/models | python3 -c "..."
```

## Log Rotation
```bash
# Archive old log
cp ~/.hermes/logs/errors.log ~/.hermes/logs/errors.log.archive-YYYY-MM-DD
: > ~/.hermes/logs/errors.log

# Verify post-rotate
tail -100 ~/.hermes/logs/errors.log | grep -c "pattern"
```

## Cron Model Check
```bash
# View current cron model
grep -A3 "^cron:" ~/.hermes/config.yaml

# Update cron model
hermes config set cron.model <model>
hermes config set cron.model_provider <provider>
```

## Browser Engine Check
```bash
# Verify browser engine
grep -A2 "^browser:" ~/.hermes/config.yaml

# Update if needed
hermes config set browser.engine auto
```

## Protected Thread Models
- DM utama `/1`
- General `/802`
- Programmer `/803`
- QA `/804`
- Kreator `/1172`

Do not change these without explicit user request.
