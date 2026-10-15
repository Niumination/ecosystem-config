---
name: model-mapping-repair
description: Use when a model mapping points at a dead provider.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [hermes, model-mapping, provider, cron, telegram, verification]
    related_skills: [hermes-provider-config, niu-9router-maintain, pre-cleanup-artifact-preservation]
---

# Model Mapping Repair

A provider can vanish from the router/gateway catalog while `config.yaml` still points at it. The
failure appears as `HTTP 404: No active credentials for provider: <name>` — and only on the paths
that use that mapping (one cron job, one Telegram channel, delegation, x_search), so it can run
broken for weeks without anyone noticing.

## When to Use

- `No active credentials for provider: <name>` in logs, a cron job's `last_error`, or a chat channel.
- A provider/model disappeared from `/v1/models`, or a thread silently stopped answering.
- Any time routing is being blamed: **dump the live mapping, never diagnose from a remembered map**.
  Per-path mappings (cron / auxiliary / x_search / channel_overrides) drift independently — one dead
  entry can sit beside four healthy ones, and paths that used to route through a local router may
  since have been pointed at a hosted provider. Read the config, then compare each mapped provider
  against what that provider's catalog actually serves.
- Before declaring "provider X is dead" — see the OAuth/`key_env` trap below.

## Rules

1. **A mapping is a pair.** Every entry stores `model` AND `provider` (cron also uses
   `model_provider`). Replacing only the model leaves the dead provider in place; the path still fails.
2. **Listed ≠ usable.** Presence in `/v1/models` proves nothing. Probe — and probe for
   **tool-calling**: cron, channel, and delegation sessions run with toolsets, so a model that
   answers text but returns no `tool_calls` fails in production anyway.
3. **Free tiers expose only `:free` models.** Paid entries in the same catalog answer
   `404 … requires available credits`. Report that limit instead of promising the exact old model name.
4. **An OAuth provider has no API key.** `model.key_env` may point at another provider's key;
   probing with it returns a FALSE 401 while Hermes itself works fine. The authoritative proof is a
   real Hermes session, not your curl.
5. **Prove with a real session before reporting a fix, and keep test output out of shared
   channels.** Fire the job once with its delivery switched to local, then restore delivery.
6. **Change only what is broken.** A misleading-but-working line (e.g. `key_env` naming the wrong
   provider) gets documented, not "fixed" while it still works — unless the owner asks for that fix
   explicitly: then deleting the line IS the repair for an OAuth provider (Hermes needs no `key_env`
   for it — the credential lives in `auth.json`), and it must be proven with a real session after.
7. **Classify a config model reference before probing it.** Only chat mappings are probeable:
   `model.default`, `auxiliary.<chat-task>`, `x_search`, `platforms.telegram.channel_overrides.*`,
   `cron`. Entries under `tts.*` / `stt.*` / `image_gen` speak other protocols, and `provider: auto`
   has no endpoint of its own — probing them against a chat endpoint answers 404 and looks like
   breakage. Report those as "not a chat mapping", never as failed.

## Procedure

1. **Inventory every reference to the dead provider.** Back up the config, then
   `grep -n -i <name> ~/.hermes/config.yaml` and dump the mapping table (`cron`, `auxiliary.*`,
   `x_search`, `platforms.telegram.channel_overrides.*`) by reading the YAML — the entries carry
   `model`+`provider` (+ `base_url`/`api_key` for auxiliaries).
2. **Measure the blast radius with evidence, not inference.** Count
   `No active credentials for provider: <name>` in `~/.hermes/logs/*.log`, and bucket the models of
   recent sessions from `state.db`:
   `SELECT model FROM sessions ORDER BY rowid DESC LIMIT 200`. Sessions with `source='cron'` on
   that model prove the path is broken in reality.
3. **Choose replacements from the target provider's catalog and verify each one** with
   `scripts/probe-tool-calling.py` — `--auth-json <provider>` for OAuth, `--key-env <VAR>` for
   API-key providers. Keep the original intent where a same-family name exists; a `:free` suffix is
   a real constraint, not decoration.
4. **Apply** the new `model`+`provider` (plus `base_url`/`api_key` where present) through a python
   string replace guarded by `assert t.count(old) == 1`, then re-read the YAML and confirm the dead
   provider name now returns 0 hits.
5. **Verify in order:** a one-shot Hermes session (`hermes -m <model> --provider <p> -z "Balas: OK"`),
   then a fired cron job with delivery switched to local (check `last_status` in
   `~/.hermes/cron/jobs.json`, then restore delivery). Other jobs on the same code path are
   "expected to pass on their schedule" — never report them as verified.
6. **Document** the active mapping (location, model, provider) plus a "do not use anymore" list in
   the ecosystem's mapping registry, and name the config backup in the report.

## Pitfalls

- **A green text probe is not a green mapping.** Tool-calling is what sessions actually need.
- **Reasoning models need a larger `max_tokens`** before they emit content or tool calls; a small
  budget reads as "empty" and looks like a dead model.
- **Never conclude "dead" from a probe that used the wrong credential source.** Check
  `~/.hermes/auth.json` → `credential_pool.<provider>` (`auth_type`, `last_status`, `request_count`)
  first. Print field names and value lengths only — never the secret values.
- **Firing a cron job to test it posts to its delivery target.** Switch delivery to local for the
  test run and restore it after; forgetting the restore silently mutes a job that used to report.
- **Do not swap a working provider for cosmetic consistency.** If the user wants everything on one
  provider, first prove that provider's tier can actually serve the models being moved.
- **A one-shot CLI check can hang for many minutes.** Always
  `timeout 90 hermes -m <model> --provider <p> -z "Balas: OK" </dev/null` — without the stdin
  redirect the CLI can block on input and burn the whole turn. "Refusing this startup model override
  in non-interactive mode" is a CLI guard, not a provider failure: do not read it as a dead model.
- **Size the model to the slot, subject to the free-tier quota.** Give the demanding paths
  (delegation, the heavy channel) the strongest verified free model, and keep the chat paths on the
  provider with the looser quota — a daily-capped free tier survives one call a day and 429s under
  real conversation.
- **A wall of failures in a bulk audit is more often a broken probe than a broken system.** Before
  reporting any single one, validate the probe against a target known to be healthy: force a tool
  call with the prompt ("run `pwd`") instead of asking for a bare "OK", give reasoning models a
  large `max_tokens`, and treat an empty message as *inconclusive* rather than dead — then re-run
  only that subset. Publishing probe artifacts as findings pushes the owner into a needless config
  change and burns your credibility for the real ones.

## References

- `references/mapping-repair.md` — full recipe: inventory snippets, evidence commands, repair and verification sequence
- `scripts/probe-tool-calling.py` — probe a provider catalog for HTTP 200 **and** `tool_calls`; token from `--auth-json <provider>` or `--key-env <VAR>`; never prints the token
- `references/free-tier-routing.md` — building a mapping that only ever uses free tiers: how to classify a provider tier, inventory its free models, prove them, and which slot each one belongs in
