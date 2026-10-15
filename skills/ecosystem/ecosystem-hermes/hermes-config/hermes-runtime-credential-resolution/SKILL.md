---
name: hermes-runtime-credential-resolution
description: "Use when a provider looks broken; prove its real credential."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [hermes, providers, credentials, oauth, model-mapping, troubleshooting, verification]
    related_skills: [hermes-provider-config, provider-model-verification, model-status-checker, 9router-model-mapping]
---

# Hermes Runtime Credential & Model Resolution

Determine **what a provider or thread is actually using right now** — which credential source, which model, which layer wins — before declaring anything broken. Config files are a *fallback layer*; the running gateway is the truth.

## When to Use

- A user reports a provider "tidak bisa dipakai" / "not working" and the config looks correct.
- You are about to tell a user a provider is misconfigured or missing a key.
- Mapping seems inconsistent: `config.yaml` names one model, the thread answers with another.
- Any audit that probes providers — you need the real credential, not a guess.

## Always-On Rules

1. **Never conclude "no credential configured" from the absence of a `key_env` in `config.yaml`.** Some providers authenticate by OAuth and deliberately have no `key_env`. Absence of a key reference is not absence of a credential. Nous is the canonical case: OAuth in `~/.hermes/auth.json` under `providers.<name>.access_token`, plus a `refresh_token` and a short-lived `agent_key`. Proposing an API-key env var for an OAuth provider is a wrong answer that costs a round-trip to detect.
2. **Never probe with an invented or placeholder token.** A fabricated bearer string produces a 401 that is an artifact of your own probe, and you will report a healthy provider as broken. Extract the real credential from its authoritative store first, then probe. If you have already reported a failure from a placeholder probe, **retract it explicitly** rather than quietly moving on — the user may act on it.
3. **Read every credential store before declaring a credential missing.** At minimum: `~/.hermes/.env`, `~/.hermes/auth.json` (`providers` *and* `credential_pool`), `~/.hermes/shared/*_auth.json`. A provider can be present in one and absent from another, and a name in `.env` may be a *different* provider's key (e.g. an unrelated key present in the file is not proof it authenticates that provider).
4. **Never print credential values.** Report `len` + a SHA-256 prefix + the store path. That answers "same value?", "is it the current one?", and "which file holds it?" without disclosure.
5. **`config.yaml` is the lowest-priority layer.** Persisted per-thread `/model` selections live in the gateway routing table and silently supersede `platforms.telegram.channel_overrides`. Report a thread's active model from runtime state; note config drift as a separate finding rather than treating config as the defect.
6. **Probe the endpoint that actually validates auth.** A listing endpoint that returns 200 for any input proves nothing about the credential. Use a real completion call and compare against a deliberately-bad control key — status codes only, no bodies.
7. **A model name that 404s is a dead mapping, not a broken provider.** Keep the two verdicts separate: provider auth health, and that specific model's existence upstream. They fail independently and the user needs both.
8. **Report what you could not determine.** Absence of a key in the stores you read is a statement about the places you searched, not a conclusion about the system.

## Procedure

### 1. Inventory credential sources — names and fingerprints only

```bash
# .env: names + length + hash, never values
grep -oE '^[A-Z0-9_]+=' ~/.hermes/.env | tr -d '='
```

For `auth.json`, walk the tree and print `len` + `hash8` for any key matching `token|key|secret|access|refresh|auth`, plus non-secret metadata (`scope`, `expires_at`, `base_url`). `auth.json` carries three distinct regions — `providers`, `credential_pool`, `active_provider` — and they can disagree; report each separately. Note `credential_pool` entries also carry a `base_url` that may itself be stale.

### 2. Establish the auth *type* before troubleshooting

| Evidence | Auth type | Action |
|---|---|---|
| `key_env:` in `config.yaml` `providers.<name>` | API key from env | verify env value matches expectations |
| `providers.<name>.access_token` + `scope` in `auth.json` | OAuth | check `expires_at`; a `refresh_token` present means auto-refresh |
| entry only in `credential_pool` | pooled/rotated credential | check its `base_url` too |
| nothing anywhere | genuinely absent | say so, scoped to the stores you read |

### 3. Compare configured vs active model per thread

Read the gateway routing table read-only. Runtime state, not config:

```bash
python3 - <<'PY'
import sqlite3, pathlib, json
con = sqlite3.connect(f"file:{pathlib.Path.home()/'.hermes/state.db'}?mode=ro", uri=True)
for key, ejson, _ in con.execute("SELECT session_key, entry_json, updated_at FROM gateway_routing"):
    e = json.loads(ejson)
    print(key, "->", e.get("model_override"))
PY
```

A `None` override means the thread inherits the default — a thread whose `config.yaml` entry names a specific model may in fact be answering on the global default. That divergence is exactly what makes a thread look misconfigured when it is not.

### 4. Probe with the real credential, with a control

```python
# real credential from its store; control = a deliberately invalid key
probe(url, real_key)    # expect 2xx
probe(url, control_key) # expect 401
```

If the control does not return 401, the endpoint does not validate auth — a 200 from it is not evidence of anything. Re-probe against an endpoint that does.

### 5. Report as a matrix, with both verdicts

For each provider×model: `200` (live), `404` (model absent upstream), `401` (auth failed — and state which credential you used). Then a separate short list of config-vs-runtime drift. Keep these two sections apart: the first is "what is broken", the second is "what is stale".

## Pitfalls

- **Reporting a 401 caused by your own placeholder token as a provider fault.** The single most expensive mistake here: it sends the user to fix a healthy provider. Extract the credential first, or do not report a verdict.
- **Treating a missing `key_env` as a misconfiguration.** OAuth providers have no `key_env` by design. Check `auth.json` before proposing an env var.
- **Reading `config.yaml` as the source of truth for a thread's model.** Per-thread `/model` selections persist in the gateway routing table and win over `channel_overrides`; a thread can drift from config for months without either being wrong.
- **Probing `/models`-style listing endpoints and trusting the 200.** Many routers accept any key there. Only a real completion call against a known-bad control separates "auth works" from "endpoint ignores auth".
- **Assuming a name in `.env` is that provider's credential.** A file can hold a similarly-named key belonging to a different service; authenticate before concluding it is wired correctly.
- **Inferring "the old key is dead" from a 200.** A 200 on a non-validating endpoint is not proof of a live credential; probe the validating endpoint, and do not report a rotation verified until the old value returns an auth failure.
- **Silently dropping an earlier wrong claim.** A retracted error still reached the user and may have been acted on. State the retraction in the open.
- **Conflating a dead model with a dead provider.** Report both independently; they fail for unrelated reasons.
