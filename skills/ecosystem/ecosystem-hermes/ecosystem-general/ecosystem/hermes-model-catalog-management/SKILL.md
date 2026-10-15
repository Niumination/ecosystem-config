---
name: hermes-model-catalog-management
description: Manage Hermes model catalog and free-only provider filtering.
---

# Hermes Model Catalog Management

## Overview

Hermes model catalog (`~/.hermes/cache/model_catalog.json`) contains all available models from configured providers. The `/model` picker in Telegram/CLI shows a limited subset (typically ~42 models) with pagination. This skill covers filtering, aliasing, and managing the catalog.

## Key Facts

- **Catalog location**: `~/.hermes/cache/model_catalog.json`
- **Picker limit**: ~42 models visible, rest hidden behind "N more available — type /model <name> directly"
- **Native free-only filter EXISTS for provider catalogs** (see "Free-only provider filtering" below) — `model.free_only` is a DIFFERENT key that only applies to `auxiliary` OpenRouter fallback
- **All models accessible via name**: Even hidden models work via `/model <provider/model-id>`

## Free-only provider filtering (source patch)

The picker's Nous model list comes from `hermes_cli/models.py::get_curated_nous_model_ids()`, which calls
`hermes_cli/model_catalog.py::get_curated_nous_models()`. Patching the latter to honour a per-provider
`free_only` flag makes the picker show zero-priced models only.

**Why a source patch is required:** the shipped `model_catalog` config block only supported
`providers.<name>.url` (self-hosted curation list). There is no shipped free-only gate for the picker, and
the cached manifest carries no pricing field — free/paid can only be resolved by querying the provider API.

### Applying the patch (after `hermes update` wipes it)

1. **Config** — `hermes config set model_catalog.providers.nous.free_only true`
2. **`hermes_cli/config_defaults.py`** — inside the `"model_catalog"` block, document the new per-provider
   option above `"providers": {}` (comment only; no key change needed, deep-merge handles it).
3. **`hermes_cli/model_catalog.py`** — add `_fetch_nous_free_models()` and gate
   `get_curated_nous_models()` on the flag. Key details:
   - Read the token from `get_hermes_home() / "auth.json"` → `providers.nous.access_token`.
   - Base URL comes from the SAME auth block: `providers.nous.inference_base_url`
     (`https://inference-api.nousresearch.com/v1`). **The portal URL is NOT the models API** —
     `portal.nousresearch.com/api/v1/models` returns nothing usable.
   - Endpoint: `<inference_base_url>/models`; free = `pricing.prompt == 0` AND `pricing.completion == 0`
     (values are strings like `"0.0000000000"`).
   - Cache the result in-process for ~5 min (`_nous_free_models_cache`) — the picker calls this on every open.
   - Return `free_ids or None` so a fetch failure falls back to the manifest list instead of an empty picker.
4. **Restart the gateway from an OUTSIDE shell** — `hermes gateway restart`. A restart triggered from inside
   the gateway process is blocked by design (SIGTERM would kill the command mid-flight).

### Verifying

```bash
cd ~/src/hermes-agent && python3 -c "
import sys; sys.path.insert(0, '.')
from hermes_cli.model_catalog import _fetch_nous_free_models
r = _fetch_nous_free_models()
print(len(r), 'free models'); [print(' ', m) for m in r]"
```

Then confirm the picker path resolves the same list:
`get_curated_nous_models()` and `get_curated_nous_model_ids()` should both return the filtered ids.

## Workflow: Filter Free Models from Nous Portal

### 1. Fetch and Filter Free Models

Nous Portal API returns `pricing.prompt` and `pricing.completion` fields. Free models have both = `"0.0000000000"`.

```python
import json, urllib.request

with open('/Users/zaryu/.hermes/auth.json') as f:
    d = json.load(f)

creds = d['providers']['nous']
token = creds.get('access_token', '')
base = creds.get('inference_base_url', 'https://inference-api.nousresearch.com/v1')

url = base.rstrip('/') + '/models'
req = urllib.request.Request(url, headers={
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
})

with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())
    models = data.get('data', data) if isinstance(data, dict) else data
    
    free_models = []
    for m in models:
        if isinstance(m, dict):
            pricing = m.get('pricing', {})
            prompt_price = float(pricing.get('prompt', '1'))
            completion_price = float(pricing.get('completion', '1'))
            if prompt_price == 0.0 and completion_price == 0.0:
                free_models.append(m['id'])
    
    print(f"Free models: {len(free_models)}")
    for m in sorted(free_models):
        print(f"  {m}")
```

### 2. Options for Restricting Picker to Free Models

| Option | Pros | Cons |
|--------|------|------|
| **Patch `model_catalog.py`** (ADOPTED) | Picker shows only free models; provider-agnostic shape | Core code modification; wiped by `hermes update` — re-apply |
| **Aliases** | No core code changes; `/model <alias>` works immediately | Picker still shows all models |
| **Cache override** | Quick test | Overwritten by Hermes refresh |

### 3. Create Aliases (Recommended)

```bash
hermes config set model.aliases.<alias-name> <provider/model-id>
```

Example:
```bash
hermes config set model.aliases.ling31 inclusionai/ling-3.1-flash
hermes config set model.aliases.longcat2 meituan/longcat-2.0:free
```

Then use `/model ling31` directly.

## Pitfalls

- **Picker pagination is not a bug**: The "N more available" message is a UI limitation, not stale cache. All models work via `/model <name>`.
- **`model.free_only` is auxiliary-only**: The key `model.free_only` does NOT filter the `/model` picker — it only affects OpenRouter fallback in auxiliary calls. The picker filter lives under `model_catalog.providers.<name>.free_only` and requires the source patch above.
- **Wrong base URL is the #1 failure mode**: `portal.nousresearch.com/api/v1/models` silently yields zero models. The models API lives on the inference host recorded in `auth.json`.
- **Catalog has no `free` field**: The cached catalog (`model_catalog.json`) does not include pricing info. Must query the provider API directly to determine free vs paid.
- **Token location**: Nous Portal token is in `~/.hermes/auth.json` under `providers.nous.access_token`, NOT in `~/.hermes/.env`.
- **The patch does not survive updates**: `hermes update` pulls upstream `main` and reverts both files. Re-apply, then restart the gateway from an outside shell.
- **Never restart the gateway from inside the gateway**: the command is killed by SIGTERM propagation before it finishes.

## References

- `references/nous-portal-free-models.md` — Nous models API schema, free-model detection, current free list
