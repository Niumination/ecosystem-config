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
   - **GitHub tokens**: probe `/user` endpoint FIRST, then `/repos/<owner>/<repo>`, then `/orgs/<org>`. See `references/github-token-probe.md`. `/orgs/<org>` 404 means insufficient scope, NOT invalid token.

3. **Classify result**
   - ACTIVE — token/account present, probe succeeds, expected fields returned.
   - EXPIRED — account exists but probe fails or status indicates expiry.
   - MISSING — no account entry, SDK init fails, or endpoint unreachable.
   - **PARTIAL** — token valid for `/user` but not for specific org/repo endpoint. Token works, scope is limited. Report as ACTIVE with scope caveat.

4. **Report with evidence**
   - State + evidence fields + exact status or error.
   - Include next action when not ACTIVE.

## Pitfalls
- **A vendor listing your tool as "supported" is not evidence the integration exists in YOUR install.**
  Marketing pages, partner rails, and changelogs describe the interface the vendor *targets*, not the
  binary, protocol dependency, or endpoint on this machine. When asked to evaluate an integration,
  verify the local side of the seam before assessing the tool: does the required protocol exist here,
  and at what version?

  ```bash
  # Claimed: "supports <your tool> via protocol X"
  <your-tool> <x> --check          # does the subcommand exist and do its deps import?
  grep -n '<x>' <project>/pyproject.toml   # is the protocol a declared dependency, or a lookalike name?
  ls <project>/<x>_adapter/                # is there a real adapter, or only a marketing entry?
  ```

  Then confirm the *transport* matches, not just the name: a protocol implemented over stdio and one
  over HTTP share a name and nothing else. Look for the statement of transport in the entry point
  (e.g. "stdout is reserved for JSON-RPC") before telling the user the two ends can talk.

  Report both halves separately — "the vendor supports it" and "this machine can serve it" are
  different claims, and only the second one is yours to verify. When the second half is false, that
  is the finding, regardless of how prominently the first half is advertised.
## Auditing blast radius before wiring two agents together

Before connecting an external host, GUI, or orchestrator to your own agent runtime, measure what the
connection would **expose** — not just whether it works. A seam that functions correctly can still hand
the other side your entire production surface. Run these four steps in order.

1. **Find out which config the entry point actually loads.** A subcommand that starts your agent for
   an external caller usually loads the SAME config as normal operation. Read the entry point rather
   than assuming a sandbox:

   ```bash
   grep -nE "HOME|load_config|\.env" <runtime>/<adapter>/entry.py <runtime>/<adapter>/server.py
   ```

   If it calls the normal config loader, then every skill, MCP server, provider credential, and hook
   policy in your production config is reachable by whatever the other side runs.

2. **Enumerate what that config actually grants, from the file, and report it as a list.** Count of
   skills/files, MCP server names, provider names. Those names *are* the blast radius — a bare
   "it works" hides them.

3. **Confirm an isolation seam exists and prove it redirects**, before recommending the wiring:

   ```bash
   env -u <VAR> <venv>/python -c "...get_home()"      # control: variable ABSENT
   <VAR>=/tmp/probe <venv>/python -c "...get_home()"  # test: variable set
   ```

   Use the runtime's own interpreter, not the system one — a wrong interpreter raises an import error
   that looks like a failure of the seam rather than of the test.

4. **Report both halves separately.** "The seam exists and redirects" is a measurement; "the wiring is
   therefore safe" is a recommendation. State the first, then argue the second. When the seam exists
   but the surrounding gap is real, recommend the cheap no-tool-call path first if one exists — a
   text-only driver that cannot operate files or apps is the honest way to trial a host without
   opening anything.

### Audit the host you are connecting to, not just your own side

Check where the *other* side keeps secrets and whether it is reachable beyond loopback: read its
config file (redacting values, reporting only structure and key names), find its credential store, and
confirm the bind address. A host on `127.0.0.1` with secrets in an OS-encrypted store is a different
proposition from one on a LAN port with plaintext keys in its config — and the vendor's own docs may
describe only the worst case (server mode) while the desktop install does the right thing. Verify
rather than inherit the warning.

### Write the recommendation as a staged path, not a verdict

When the seam works but the risk is real, the useful output is an escalation ladder: leave it as-is
(if already neutral), then the cheapest safe connection, then the full connection gated on explicit
preconditions. Name the preconditions as checkable items. "Don't do it" is rarely actionable; "do this
first, and here is the command that proves it" is.

## Pitfalls
- **Isolating a runtime by pointing its home variable at a bare empty directory does not work.** The
  runtime treats the empty home as an unprovisioned install, tries to bootstrap, and **hangs rather
  than failing fast** — a probe that never returns is easy to misread as "isolation is broken". The
  seam is real; the directory was not provisioned. Provision the isolated home properly (run the
  runtime's own repair/setup step against it) before pointing anything at it.
- **Attribute a failed probe before reporting it as an outage.** During an audit you are often running
  your own long or hanging probes; a service that answers fine can return a timeout or connection
  failure under that self-inflicted load. Kill the stray probes, wait a moment, and **re-measure** — if
  the retry succeeds and the service's listener and process are intact, there is no outage to report.
  Never leave a transient failure out of the report entirely either: say it happened, what caused it,
  and what the re-measurement showed. Reporting a non-event as a defect wastes the user's time;
  silently dropping a failure that appeared in the transcript looks like concealment.
- **Surface-only checks:** installed CLI ≠ integration; env var ≠ valid token; config key ≠ connected.
- **SDK discovery traps:** some SDKs require exact session/tool calls to reveal usable tools. Inspect returned objects/fields, not just names.
- **Auth expiry:** OAuth tokens often expire silently. Always check scopes/expiry when available.
- **GitHub PAT scope mismatch:** A fine-grained PAT may work for `/user` but return 404 for `/orgs/<org>`. This does NOT mean token is invalid — it means the token lacks `repo` or `read:org` scope. Verify at the `/user` level first.
- **`/orgs/<org>` 404 is not "token invalid"**: GitHub returns 404 for org endpoints when the PAT lacks org membership or read:org scope, even though the token is perfectly valid for user-level API calls. See `references/github-token-probe.md`.

## References
- `references/composio-sdk-patterns.md` — verified Composio Python SDK patterns from session.
- `references/hermes-config-inspection.md` — grep + read_file pattern for Hermes config.yaml.
