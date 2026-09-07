---
name: integration-verification
description: Verify whether external services, APIs, or toolkits are actually connected and working end-to-end. Use when checking Composio, API keys, providers, webhooks, or local gateways.
---

# Integration Verification

## Trigger
- User asks whether something is connected, integrated, live, or working.
- User shares an API key or provider URL and asks to verify it.

## Core Rule
Verify live connectivity before declaring status. Do not rely on config entries, env vars, CLI presence, or past session success as proof of current integration.

## Workflow

1. **Identify integration surface**
   - Use provider SDK/library if available.
   - If no SDK, use HTTP probes against authenticated endpoints.

2. **Probe live state**
   - Generic APIs: `/whoami`, `/health`, `/v1/models`, or equivalent lightweight authenticated call.
   - Composio: instantiate client, list connected accounts, inspect status fields.
   - Local gateways: probe `localhost:<port>` with expected protocol.

3. **Classify result**
   - ACTIVE — token/account present, probe succeeds, expected fields returned.
   - EXPIRED — account exists but probe fails or status indicates expiry.
   - MISSING — no account entry, SDK init fails, or endpoint unreachable.

4. **Report with evidence**
   - State + evidence fields + exact status or error.
   - Include next action when not ACTIVE.

## Pitfalls
- **Surface-only checks:** installed CLI ≠ integration; env var ≠ valid token; config key ≠ connected.
- **SDK discovery traps:** some SDKs require exact session/tool calls to reveal usable tools. Inspect returned objects/fields, not just names.
- **Auth expiry:** OAuth tokens often expire silently. Always check scopes/expiry when available.

## References
- `references/composio-sdk-patterns.md` — verified Composio Python SDK patterns from session.
- `references/hermes-config-inspection.md` — grep + read_file pattern for Hermes config.yaml.
