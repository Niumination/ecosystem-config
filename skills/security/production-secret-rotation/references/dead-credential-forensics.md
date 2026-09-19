# Dead Credential Forensics

For a credential in a local env file that stopped authenticating (`FATAL: password authentication failed`
is the common shape). Goal: localize the failure **before** touching anything, then remove or replace it
without breaking a live consumer.

## 1. Localize: service alive, value wrong

| Observation | What it proves |
|---|---|
| Another credential of the **same project** works (app-level API key, live endpoint) | project not deleted/paused — the fault is scoped to this value |
| The server answers with an **auth error** (not DNS/connect/timeout) | host and port reachable — not a network problem |
| Both the stored URL **and** a re-encoded variant are refused | the *value* is stale, not the encoding |

Masked structural analysis — prints no secret:

```python
import re
m = re.match(r'^([a-z]+)://([^:]+):([^@]*)@(.+)$', u)
scheme, user, pw, rest = m.groups()
esc = re.findall(r'%([0-9A-Fa-f]{2})', pw)
print(f"len={len(u)} user={user} pw_len={len(pw)} pct={pw.count('%')} valid_escapes={len(esc)} at={u.count('@')}")
print("needs encoding:", sorted({c for c in pw if c in '#?/%:@[] '}))
```

Probe both readings of the password with a short connect timeout: as stored, and re-encoded from scratch
(`urllib.parse.quote(pw, safe='')`). Two failures = stale value. If the re-encoded form **succeeds**, the
file was written unencoded — fix the file, nothing was rotated.

## 2. State what is knowable and what is not

A stale value means the provider rotated it after the copy was saved. That is the conclusion; the **date**
is usually not recoverable client-side (password-reset audit logs are commonly a paid feature). Say so
instead of inventing a date.

## 3. Leak surface — dead is not harmless

A dead credential still names host, project ref, and user. Check publication:

```bash
git grep -l -F "<project-ref>" -- .     # 0 = absent from tracked files
git ls-files -s <suspicious-dir>        # mode 160000 = gitlink, contents are NOT in this repo
```

A hit inside a gitlink, an archived/private repo, or a git-ignored vault path is not a publication.

## 4. Remove or replace

```bash
cp ~/.hermes/.env ~/.hermes/.env.bak-$(date +%Y%m%d-%H%M%S) && chmod 600 ~/.hermes/.env.bak-*
```

Rewrite the file in Python (never `sed` on a secrets file), then prove the change by diffing the
**variable-name list** before and after — exactly one entry gone, everything else intact — and re-assert
`600`. `grep <VAR>` alone only proves the line you aimed at.

If the credential should work again, do not ask for the value in chat: have the user copy the provider's
current connection string, then read it locally (`pbpaste`) into the file with a script that prints only
the new length.

## 5. Report

App-level impact (often none — the app uses a different credential), consumers found and why the sweep is
complete, backup path, removal proof, and leak-check result. Persist it where local-only reports live,
never in a public repo.
