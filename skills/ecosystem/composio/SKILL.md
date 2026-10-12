---
name: composio
description: Route and complete Composio work across Composio For You and Composio Platform. Use when the user mentions Composio; wants an agent to use apps such as Gmail, Slack, GitHub, Notion, Calendar, or Linear; needs first-time setup, an SDK or MCP integration, CLI operation, migration guidance, current documentation, or help diagnosing a connection or tool call.
---

# Composio

Use this skill as a router. Identify the product and the job, load only the relevant guidance, consult canonical documentation for volatile details, and then answer or do the work the user requested.

## 1. Choose the product

Do not blend the products. They use different credentials and setup paths.

| | Composio For You | Composio Platform |
|---|---|---|
| Use when | Someone wants their own agent to use their own apps | A developer is building a product whose users connect accounts |
| Primary surface | MCP or the Composio CLI | SDK sessions inside an application |
| Credential | `ck_...` consumer key when the client requires a header | `COMPOSIO_API_KEY` project key |
| Dashboard | `dashboard.composio.dev` → For You | `dashboard.composio.dev` → Platform |

Ask one short question only when context does not establish the product:

> Is this for your own agent and accounts, or for a product where your users connect their accounts?

Treat a named personal AI client with no product code as For You. Treat an application codebase, SDK, user or tenant identity, backend, or product agent as Platform.

## 2. Choose the job

Identify the requested outcome before taking action:

- **Explain or discover:** answer a question, compare approaches, or find the current API.
- **Set up:** establish credentials, an MCP client, the CLI, or an SDK for the first time.
- **Build or change:** integrate Composio into an existing agent or application.
- **Operate:** find, connect, and run tools for a real task.
- **Debug or migrate:** diagnose a failure, update an older integration, or move from legacy direct execution or Tool Router.

Do not turn an explanation, documentation lookup, or narrow bug fix into onboarding.

## 3. Load only the relevant guidance

- For You: read [Composio For You](references/for-you.md).
- Platform: read [Composio Platform](references/platform.md).
- Provider, connection, or execution failure: also read [Errors and provider gotchas](references/errors.md).
- Provisioning cloud resources (e.g. a Supabase project) through Composio: read [Supabase provisioning](references/supabase-via-composio.md).
- Turning on OAuth sign-in for an app whose auth is brokered by a connected provider: read the `vercel-feature-activation` skill's `references/oauth-provider-activation.md`.

## Complete the selected job

- For a question, fetch current documentation when needed and give the concrete answer. Do not mutate a project or force a tool call.
- For setup or integration, inspect the existing environment, preserve its architecture and identity model, make the smallest useful change, and verify it with one safe real tool call when credentials and user authorization are available.
- For an operational request, connect only the apps the task needs and execute the requested workflow.
- For debugging, get the Composio log or request ID, identify the failing boundary, fix that boundary, and retry when the user authorized execution.

## Headless MCP access (no browser)

The shared For You endpoint `https://connect.composio.dev/mcp` accepts only an AuthKit JWT from a browser login — it returns `401` for no auth, for `x-api-key`, and for `Authorization: Bearer <COMPOSIO_API_KEY>` alike. Do not iterate on header variants there. For an agent that cannot open a browser, mint a Platform session with the installed SDK instead:

```python
from composio import Composio
s = Composio().create(user_id="<stable_user_id>")   # s.mcp.url, s.mcp.headers
```

`s.mcp.url` is an HTTP MCP endpoint on `backend.composio.dev`; `s.mcp.headers` carries the session key. Verify host and credential with the documented REST shape first — base `https://backend.composio.dev/api/v3.1`, header `x-api-key`. A JSON error body that contains a `request_id` means the host is up and the path or header is wrong, not an outage; `api.composio.dev` is not an API host.

Report only `session_id` and the MCP URL — never `session.mcp.headers`, which embeds a live key. If a key has already been printed anywhere, rotate it after integration and recreate the session.

### Rotation order against a running consumer

A live gateway caches the session key **in memory at process start**; rewriting the env file does not reach it. The visible symptom is a keepalive failure (`MCP server '<name>' keepalive failed, triggering reconnect (state: connected → degraded)`) while `hermes mcp test <name>` run from a shell still passes — the shell reads the new key, the daemon holds the old one. Sequence that avoids the dead window:

1. Write the new key to the env file; mint the replacement session.
2. Patch the session URL in the config to the new session id.
3. Restart the consuming process from outside itself (a gateway cannot restart from within — the signal reaches the child).
4. Confirm the connection: `hermes mcp test <name>` **and** a fresh heartbeat/registration line in the agent log naming the new URL.
5. Only then revoke the old key upstream.

Revoking before step 4 takes the integration down until the restart lands. Two provider behaviours worth knowing while doing this: **an existing session URL keeps answering after the key is rotated** (a session id is not bound to a key version, so both old and new URLs may return `200` — pick the new one for hygiene, not because the old one broke), and **a revoked key is distinguishable from a wrong one only by the response body** — read the JSON error (`Invalid API key: <masked>`, slug `APIKey_InvalidAPIKey`), not just the `401` status.

## Runtime re-auth pattern

If a toolkit tool returns `No active connection found for toolkit(s) '<slug>'`, do not change credentials. Start `COMPOSIO_MANAGE_CONNECTIONS` for that toolkit in the same session, return the Connect Link to the user, wait for authorization, and retry the original tool call. This pattern is especially common for email/inbox checks because a Gmail connection may be listed in the dashboard but still require session authorization in Tool Router sessions.

## Tool Router meta-tools (agent MCP)

When Composio reaches an agent as MCP (URL shaped `https://backend.composio.dev/tool_router/<router>/mcp` with `x-api-key`), the surface is a fixed set of meta-tools — discover (`COMPOSIO_SEARCH_TOOLS`), schemas (`COMPOSIO_GET_TOOL_SCHEMAS`), execute (`COMPOSIO_MULTI_EXECUTE_TOOL`), and `COMPOSIO_MANAGE_CONNECTIONS` — not the per-app tools themselves. Work the pipeline instead of guessing:

1. Discover slugs, then fetch each schema, then execute. Never invent a tool slug.
2. Discovery takes `queries:[{use_case, known_fields}]`; a session object alone is rejected as "missing required argument", and the query object accepts no extra keys — passing e.g. `toolkits` inside it fails `additionalProperties` validation. Scope the toolkit by naming it in the `use_case` text instead.
3. Carry ONE `session_id` through the whole workflow (`session:{"id":...}` on discovery, `session_id` on execute). Execute takes `tools:[{tool_slug, arguments}]` plus `sync_response_to_workbench:false`; the returned session block tells you to keep reusing the id.
4. `COMPOSIO_MANAGE_CONNECTIONS` reporting `enabled` or `successful` proves only that the toolkit is enabled in the workspace. Authorization is the separate `has_active_connection` / `connected_account_id` fields — quote those, never the former, when reporting readiness.
5. An authorization Connect Link expires within minutes. When the user says it is done, mint state fresh via a status call; do not reuse a stale link or re-derive success from an earlier reading.
6. Re-read connection state immediately before an irreversible call (resource create, publish, delete). "Enabled" and "connected a minute ago" are not evidence at execution time; a claim of active that no output actually showed must be re-verified, not restated.

## Stable rules

1. Establish the product before choosing credentials, URLs, SDKs, or commands.
2. Treat dashboard onboarding as a context, not the skill's identity. When the developer arrives with an existing `COMPOSIO_API_KEY` from Getting Started, use it and never create, rotate, replace, print, or request it in chat. Do not run `composio dev init` in that path.
3. For a general first-time Platform setup with no dashboard credential handoff, follow the current setup path in the Platform guide.
4. Never invent toolkit or tool slugs. Discover them at runtime or with the CLI.
5. Do not build a provider OAuth flow. Composio returns a Connect Link when authentication is needed.
6. Use sessions for new Platform integrations. Preserve the application's existing user identity and agent architecture.
7. Keep credentials out of source control, URLs, logs, chat, and command output.
8. Get the log or request ID before diagnosing a failed tool call.
9. Prefer the smallest configuration that completes the current job. Keep toolkit filters, tag policies, sandbox controls, custom auth, provider-specific hardening, and other advanced options out of the first path unless the request or existing code requires them.
10. Do not invent repository facts. Never claim that a file, framework, environment loader, identity field, agent path, or dependency exists until it was provided or inspected. If codebase context is unavailable, state the unknown and ask for access or one necessary detail.
11. In SDK or API examples, use exact identifiers and call shapes from a current public page or schema. Copy the documented shape for the requested language instead of translating names between TypeScript and Python; if a required detail is not documented, explain the behavior without inventing code.

## Canonical information

Use bundled references for stable decisions. A user-facing source list contains only public `https://docs.composio.dev/...` pages actually consulted; bundled reference names, local paths, and `file://` URLs are omitted. For versions, provider adapters, client-specific setup, toolkit behavior, or APIs that may have changed, use the current canonical documentation and current CLI or tool schemas as the primary sources before answering or editing code:

When sources disagree, prefer the current API reference and live endpoint behavior over any page marked Legacy, and name the REST API version explicitly.

```text
https://docs.composio.dev/llms.txt
https://docs.composio.dev/docs/<page>.md
https://docs.composio.dev/toolkits/<toolkit>.md
```

If those primary sources do not answer a Composio product or troubleshooting question, query the public unified knowledge search at `https://docs.composio.dev/api/knowledge-search?q=<question>`.

Results may be canonical docs, KB, toolkit, example, or reference pages. Use the returned evidence to answer the question; public records do not establish the live state of a user's account, project, connection, or tool call.

When knowledge search supplies evidence, cite the result's returned `canonicalUrl`, not the search API URL. If `canonicalUrl` is relative, prefix it with `https://docs.composio.dev` before citing it.

Only treat a result as evidence when its excerpt or page directly addresses the question. If no public source directly documents an exact error or symptom, say so instead of diagnosing from adjacent results; request the log or request ID, or the necessary live evidence.

Use the documentation to complete the task. Do not merely hand the user a link unless they asked for one.
