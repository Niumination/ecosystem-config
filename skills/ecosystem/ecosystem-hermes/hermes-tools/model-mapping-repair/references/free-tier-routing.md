# Free-Tier Routing

How to build and keep a mapping that never leaves the free tier — and how to tell which "free"
actually serves an external client.

## 1. Classify the tier before designing anything

| Tier shape | How it authenticates | What it means for routing |
|---|---|---|
| **OAuth / free account** (portal account with no credits) | credential in `~/.hermes/auth.json` → `credential_pool.<provider>` (`auth_type`, `last_status`, `request_count`) | Usable, but paid catalog entries answer `404 … requires available credits`. Only free-suffixed entries work. |
| **API key with a free quota** | `key_env` in `config.yaml` | Usable until the daily cap; 429 shows up mid-conversation, not in a one-shot probe. |
| **Keyless relay** (no credential at all) | anonymous request | **Verify the tier is not app-gated.** A keyless free tier can be restricted to the vendor's own client and refuse every outside caller — no header, client-id, or base-url tweak fixes that, and such a provider must not become a routing target. |
| **Local router** with mixed providers | local API key | Free-tier providers inside it disappear without notice when the upstream revokes access; keep router-served models as *backup* and the primary mapping on a provider that serves the model itself. |

Reading `auth.json` is the fastest way to see which tier a provider is on — print field names, types
and value **lengths** only, never the secret values.

## 2. Inventory the free options

For each candidate provider:

1. List the catalog (`GET <base_url>/models`) with the credential that provider actually uses —
   OAuth providers need the token from `auth.json`, API-key providers `env:VAR`, keyless ones get
   **no** `Authorization` header at all.
2. Filter to the free entries (`:free`, `-free`, provider-specific free markers).
3. Probe each candidate for **HTTP 200 plus a tool call** — a free tier is exactly where tool
   calling silently degrades, and every cron / channel / delegation session runs with toolsets.
4. Record hits and misses with the response code; a tier-specific refusal message is useful output
   because it names the limit.

## 3. Distribute across the slots

- **Demanding slots** (delegation, the heavy channel): the strongest *verified* free model.
- **Conversational slots** (threads, DM, x_search, cron): the provider whose quota is loosest — a
  daily-capped tier survives one scheduled call a day and 429s under real conversation.
- **Never** point a mapping at a tier that was not proven to serve external clients.
- Hand the owner the quota caveat with the mapping: which slots will 429 first and what the
  one-line fallback to the looser provider is.

## 4. Keep it honest

- A name present in the catalog is not a promise: prove it, then write down the verification.
- When a tier changes underneath you the mapping does not "break" — it starts failing only on the
  paths that use it. Re-run the inventory and re-distribute; do not patch the single symptom.
- Free-tier policy is vendor-controlled and can move without notice, so re-probe before trusting an
  old inventory: an inventory is evidence about the day it was taken, not a durable fact.
