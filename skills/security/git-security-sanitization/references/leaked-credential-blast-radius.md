# Leaked-Credential Blast Radius

Use after a leak is located: this file answers "what does holding this value actually reach?" and
"which trust entries have to be removed?". It is the difference between reporting a leak and
reporting an incident.

## Report two things separately

1. **Identifier exposure** — the string is public.
2. **Access exposure** — the string still authenticates somewhere.

A public half with no private half, an alert for an already-revoked credential, and a key whose
private half never left a dead host are all *identifier only*. State which one you proved. Never let
"the value is public" imply "the account is reachable", and never let "it is a public key anyway"
dismiss a finding — the question is where the private half lives.

## Per-type reach (severity ordering for the response list)

| Type | What holding it reaches | Neutralizing step |
|---|---|---|
| `service_role` / admin DB key (Supabase, Firebase admin, DB URI) | every row in that project, bypassing row-level security | rotate in the provider dashboard |
| Code-hosting credential (account SSH key, PAT, deploy key) | push to repos — and therefore to whatever deploys from them | delete the trust entry (`gh api -X DELETE user/keys/<id>`, deploy key, PAT) |
| Billing key (OpenAI and similar) | the owner's balance | revoke at the provider |
| Telegram bot token | that bot only: send as the bot, read updates **while polling**, change its own name/description | revoke in @BotFather, or delete the bot |
| Public-by-design web key (Firebase web config, Maps key) | APIs billed to the owner if unrestricted | add referrer/API restrictions; do not rotate blindly |
| Short-lived OAuth access token | whatever grant was active, until expiry | revoke the grant in the account |
| Third-party key inside a committed browser cache | someone else's quota | not the owner's to rotate — stop committing the profile |

## What a leaked bot token does NOT reach

No login to the owner's messenger account, no reading of chats the bot is not in, no shell on the
owner's machine, no access to code hosting, no code execution anywhere. Profile vandalism is
reachable with the token alone (`setMyName`/`setMyDescription` need nothing else), so a renamed bot
is **not** evidence that the owner's account was compromised — say that plainly instead of alarming
them, and name the residual risk that does apply: messages arriving from a bot the owner trusts.

## Match leaked material against live trust state

An SSH public key in a leak is not a secret — it is a name tag for a private half stored somewhere
else. Compare it against every place that trusts it:

```bash
# fingerprint of the leaked key (base64 body only — the comment is not part of the key)
printf '%s\n' 'ssh-ed25519 <LEAKED_B64> x' > /tmp/k.pub && chmod 600 /tmp/k.pub
ssh-keygen -lf /tmp/k.pub
gh api user/keys --jq '.[] | "\(.id) \(.title) \(.created_at)"'   # account keys
gh api repos/<owner>/<repo>/keys                                    # deploy keys
```

Compare the **base64 body**, never the whole line: the trailing comment is free-form and will differ
between the leaked copy and the registered entry. An account-key match reaches every repo the owner
can write to; a deploy-key match reaches one repo. Report which, because the response changes from
"rotate one repo's key" to "delete the account key and review what deploys from what it could push".

## Classify before prescribing

Telling the owner to rotate a credential that is not theirs wastes their time and buries the real fix:

- **browser-cache artifacts** (`CacheStorage`, IndexedDB logs under a browser profile directory) carry
  third-party keys scraped from visited sites → the fix is to stop committing the profile, plus the
  privacy problem of publishing browsing artifacts at all;
- **public-by-design config** (`firebase-applet-config.json`) → restrict by referrer/API, do not rotate;
- **documentation examples** (masked samples, redaction skill files) → not a leak; say so and move on.

## Two keys in one file: decode the role before touching either

Client-served config usually ships a public and a privileged key side by side, in the same object,
with names that hide which is which. Read the role from the JWT payload — never infer it from the
variable name, which may be camelCase, snake_case, or hyphenated:

```bash
python3 - <<'PY'
import base64, json
p = "<candidate-jwt>".split(".")[1]
p += "=" * (-len(p) % 4)
print(json.loads(base64.urlsafe_b64decode(p)).get("role"))   # 'anon' | 'service_role'
PY
```

| Role | Action |
|---|---|
| `anon` (or a `-anon-key`) | Public by design and **required** by the browser client. Leave it in place; constrain it with RLS policies and referrer/API restrictions. Blanking it breaks the deployment mid-incident. |
| `service_role` / admin | Bypasses RLS. Must not exist in client code at all — remove the line, after `grep -rn <identifier>` confirms nothing reads it. |

Supabase rotation semantics: rotating the **JWT secret** replaces the `anon` and `service_role` keys
**together**. Every deployed env var and client config holding either key must be updated in the same
pass or the app loses its database connection. Two repos leaking keys whose fingerprints differ are
two projects — say "two rotations", not "one".

## Confirm exposure at the served path

When the repo publishes (GitHub Pages and similar), a file committed to it is fetched by every
visitor with no authentication; "it is only in the repo" is not a mitigating factor.

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://<owner>.github.io/<repo>/<path>   # 200 == served
```

After pushing the fix the CDN may keep answering with the cached copy for a minute or two, so a single
check right after the push proves nothing. Poll with a cache-busting query and read the `age` header to
tell the stale response from the new one; stop when the served copy no longer carries the privileged
value. Files that are not published (a `.env.example` that 404s) still leak through the repo itself —
check both, and report them as different exposures.
