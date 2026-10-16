# Model Default Update — Complete ✅
**Date:** 31 Ags 2026

## Change
- **Before:** `upstage/solar-pro4:free` (Nous provider)
- **After:** `gh/gpt-5.4-mini-free-auto` (9router provider)

## Rationale
- FREE tier model with 400K context
- 128K max output
- Has vision, tools, search, reasoning
- Independent quota from Google
- Fastest free model available

## Config Change
```yaml
model:
  provider: nous
  default: gh/gpt-5.4-mini-free-auto
  base_url: https://inference-api.nousresearch.com/v1
```
