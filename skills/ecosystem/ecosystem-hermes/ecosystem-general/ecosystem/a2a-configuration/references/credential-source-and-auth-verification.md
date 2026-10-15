# Credential source, bind-host symptom, and auth verification

Depth for the case "A2A peer reachable in one direction only" or "peer says unauthorized".

## Symptom → root cause

**Symptom: the peer reports connection refused, and `lsof -iTCP:PORT -sTCP:LISTEN`
shows the socket bound to `localhost` / `127.0.0.1` instead of the tailnet IP,
even though the bind host variable is set correctly.**

The bind host is almost never the problem. `resolve_bind_host()` refuses any
non-loopback bind unless a credential is present:

```
localhost_only()  ==  not (bearer_token or peer_tokens)
```

With no credential, a requested wide host is logged as ignored and downgraded to
`127.0.0.1`. So **`A2A_HOST` set + localhost bind == missing token**, not a
misconfigured host. Look for `A2A_BEARER_TOKEN` or `A2A_PEER_TOKENS` before
touching the host.

Confirm the bind is genuinely wide, not just "listening":

```bash
lsof -iTCP:9900 -sTCP:LISTEN    # address column must show the tailnet IP, not 127.0.0.1
```

## Where a launchd-managed gateway actually reads credentials from

Two sources, and they do not merge the way people assume:

| Source | Loaded by | Precedence |
|---|---|---|
| `~/.hermes/.env` | gateway startup, `override=True` | **wins** on conflict |
| `LaunchAgents/*.plist` `EnvironmentVariables` | inherited by the process | used only for keys `.env` does not define |

Two consequences that cause outage windows:

- Because `.env` loads with `override=True`, a value present in both places takes
  the `.env` value. Adding a key to `.env` silently overrides the plist copy.
- Clearing on load is **narrow**, not blanket: only a small set of provider-routing
  keys are dropped when absent from `.env`. Any other plist-supplied variable stays
  live. So a plist-only credential keeps working across restarts.

**Rule: a credential present in exactly one source is live, and that source may be
the only one. Before removing a credential from its current location, confirm the
destination already holds it.** Add first, restart, verify, then remove. Removing
first leaves a window where the service is credential-less and silently degrades to
a localhost bind instead of failing loudly.

`launchctl setenv` is runtime-only and dies with the login session — it is a
diagnostic probe, never a fix.

## Verify auth with POST, never with the agent card

Agent cards are served **without** an auth check by design, so a `200` on
`/.well-known/agent-card.json` proves reachability and nothing about auth. The
unauthenticated GET also deliberately omits profile/tenant topology.

`POST` is the authenticated path:

```bash
TOK=$(cat <credential-file>)
# must be 401 without the credential
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://<peer>:9900/message/send \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"x","method":"message/send","params":{"text":"ping"}}'
# then the same call with -H "Authorization: Bearer $TOK" must return 200
```

Read `TASK_STATE_REJECTED` with a message like "Empty task" as **auth passing**:
the request was authenticated and then rejected on content. It is not an auth
failure — `401` / `unauthorized` is.

When a remote agent's report disagrees with local evidence, resolve it by reading
the adapter source for which env vars it reads and which routes check auth, then
prove the local side with a probe. Do not adopt a remote diagnosis that assumes a
credential is duplicated in two files when only one actually holds it.

## Credential hygiene on the host

Live credentials end up in more files than intended — config files, vault
pointers, and `*.bak` snapshots made by hand or by tooling.

```bash
chmod 600 <each file that embeds the live credential>
rm <backup snapshot that embeds the live credential>
```

A backup copy of a config is a second copy of every secret inside it. Prefer
re-derivable state over retained snapshots; if a snapshot must stay, redact the
credential in it rather than leaving a live value at rest.

Keep the file that must survive a service reinstall as the credential source, and
make sure its permission mode is tight. Note explicitly which single file holds the
credential, so a later reader does not assume it is duplicated.