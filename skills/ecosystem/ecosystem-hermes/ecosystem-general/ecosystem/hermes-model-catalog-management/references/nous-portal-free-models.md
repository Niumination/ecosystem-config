# Nous Portal models API — free-model detection

## Endpoint

```
GET <inference_base_url>/models
Authorization: Bearer <providers.nous.access_token>
Accept: application/json
```

Both values come from `~/.hermes/auth.json` → `providers.nous`:

- `inference_base_url` — `https://inference-api.nousresearch.com/v1`
- `portal_base_url` — `https://portal.nousresearch.com` (web UI only; NOT the models API)

`portal.nousresearch.com/api/v1/models` does not return a usable model list. Using it as the base
silently produces zero free models — the failure is invisible unless you print the count.

## Response shape

The payload is `{"data": [ ... ]}`. Each entry carries:

```json
{
  "id": "inclusionai/ling-3.1-flash",
  "canonical_slug": "inclusionai/ling-3.1-flash-20261002",
  "name": "inclusionAI: Ling 3.1 Flash",
  "context_length": 262144,
  "pricing": {"prompt": "0.0000000000", "completion": "0.0000000000"},
  "architecture": {"modality": "text->text", "input_modalities": ["text"], "output_modalities": ["text"]},
  "supported_parameters": ["tools", "reasoning", "temperature", "top_p", "..."],
  "aliases": ["inclusionai/ling-3.1-flash-20261002"],
  "links": {"details": "/api/v1/models/<slug>/endpoints"}
}
```

Keys observed across the full set: `aliases, architecture, canonical_slug, context_length, created,
default_parameters, description, expiration_date, frontier, hugging_face_id, id, knowledge_cutoff,
links, name, per_request_limits, pricing, reasoning, supported_parameters, supported_voices,
synthesizedFreeVariant, top_provider`.

## Free-model rule

A model is free when BOTH prices are zero. Prices are STRINGS, so cast before comparing:

```python
pricing = m.get("pricing", {})
prompt_price = float(pricing.get("prompt", "1"))
completion_price = float(pricing.get("completion", "1"))
is_free = prompt_price == 0.0 and completion_price == 0.0
```

Do not test the `:free` suffix alone — `inclusionai/ling-3.1-flash` is free without it, and a suffix
can appear on keyed/paid twins. Pricing is the only reliable signal.

## Scale

At time of measurement: 425 total models in the payload, 9 zero-priced. Treat both as moving numbers —
re-measure, never hardcode.
