---
name: production-secret-rotation
description: "Rotate a live production credential; prove the old is dead."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [secrets, credentials, rotation, env, vercel, verification]
    related_skills: [credential-vault-backup, integration-verification, git-security-sanitization]
---

# Production Secret Rotation

Replace a credential that is live in production — an admin password/token, an API key, a provider secret — stored in a hosting platform's env store, and prove the old value is dead. The value never enters the conversation.

## When to Use

- The user asks to rotate or replace a password, token, or key that a deployed app reads from environment variables.
- An audit turns up a weak, duplicated, or *non-sensitive* env variable on a hosting platform.
- A stored credential **stopped authenticating** on its own (nobody remembers rotating it): it needs the same discipline as a deliberate rotation — localize the failure, sweep the consumers, then remove.
- Before claiming a rotation is done: the verification half of this skill is the deliverable, not an optional epilogue.

## Rules

1. **The value never travels through the chat.** Generate it in the shell, pipe it straight into the platform, store it in the vault. Never `--value` on a command line, never an inline `export` in a command you will paste, never echoed back "for confirmation".
2. **Rotating one variable does not close the door when the code has a fallback.** Read the auth code first: `A || B` (or an env chain) means the second variable is a live second key, and rotating only `A` leaves the old secret working through `B`.
3. **Back up before changing anything.** Pull the platform's current env to a file and move it into the git-ignored vault at 600. Without the old value you cannot roll back — and cannot prove the new one took effect.
4. **Env changes need a new deployment.** Serverless env is snapshotted per deployment; pushing a commit you owe anyway (a docs pass) is the cheapest trigger.
5. **Verify by status code, never by reading the value back.** New credential → expected success, old credential → unauthorized, public endpoints → unchanged.
6. **Do not ask the user to paste a secret into the chat either.** Hand them the vault path instead.
7. **Never re-send a value you read back out of a platform env dump.** `env pull` writes dotenv-quoted, escaped text (`"...\n"`); a naive `cut -d= -f2- | tr -d '"'` leaves the escape as two literal characters and the re-installed credential is corrupt. Decode first, or install the value from its authoritative source. "I am only changing the type, the value stays the same" is the trap case, not the safe case.
8. **Once a variable is sensitive you cannot read it back.** `env pull` returns a placeholder (`[SENSITIVE]`) in place of the value, so the store no longer answers "did the value change?". That placeholder is not evidence of anything: verify with a request that needs the credential.
9. **Deleting a stored credential is its own change, with its own consumer sweep.** Before removing a variable, enumerate everything that reads it — repo scripts, CI, cron, *and the agent's own tooling* (`~/.local/share/*-mcp/`, `<agent-home>/data/.env`, agent config YAML, wrapper scripts). A repo-scoped grep that finds "nothing depends on it" is not a consumer sweep, and a live consumer loses its credential silently. If the first pass was narrow, say so and finish the sweep before acting on its conclusion.

## Procedure

### 1. Inventory the platform's env — names and types, not values

```bash
vercel env ls production      # console: name | value | type | environments | created
```

Read the **type** column. A value stored as *non-sensitive* is readable from the dashboard and by anyone who runs `env pull`: that is a finding in itself, and it is the class that leaks through screenshots, logs, and support handovers. Note every variable in the auth chain, plus any legacy twin sitting behind a fallback.

### 2. Back up the current state

```bash
vercel env pull /tmp/<app>-env-backup.env --environment=production --yes
install -d -m 700 <vault>/_backup-credentials
cp /tmp/<app>-env-backup.env <vault>/_backup-credentials/<app>-env-<YYYYMMDD>.env
chmod 600 <vault>/_backup-credentials/<app>-env-<YYYYMMDD>.env
git -C <repo> check-ignore -v <that file>    # must print a rule; never store secrets in a tracked path
```

The pull also returns platform-injected runtime variables (deployment ids, OIDC tokens); only the project's own names matter for the rotation.

### 3. Compare duplicated/legacy variables without printing them

Length plus a hash prefix answers "are these the same value?" without exposing either:

```python
print(name, len(v), hashlib.sha256(v.encode()).hexdigest()[:8])
```

A short legacy token (e.g. 10 characters) behind `A || B` is a weaker door than the password it shadows. Prefer **deleting** it to rotating it: deleting and rotating break the same unknown consumers, so the option with fewer live credentials wins. Say which one you chose and why.

### 4. Generate and install — value on stdin only

```bash
NEW="$(openssl rand -hex 32)"
printf '%s' "$NEW" | vercel env add ADMIN_PASSWORD production --sensitive --force --yes
vercel env rm ADMIN_TOKEN production --yes
```

- `--sensitive` makes the value unreadable afterwards. Sensitivity cannot be toggled on an existing variable, so re-adding is the conversion path — which is why rotation and hardening are one step.
- Write the new value into the vault at 600 with the rotation date, the authoritative variable name, and the path of the old-value backup.

**Type-only change (the value must stay identical)** — it comes from the backup dump, so un-escape it before sending it back:

```python
v = line.split("=", 1)[1]                         # raw text after KEY=
if v.startswith('"') and v.endswith('"'):
    v = v[1:-1].encode().decode("unicode_escape")  # \n -> real newline, \\ -> \
```

Compare the decoded length against the original before piping it to stdin — a length off by one or two is the leftover escape, and installing it that way breaks the app on the *next* deployment.

### 5. Deploy, then verify the old value actually dies

```bash
NEW=$(grep -m1 '^<VAR>=' <vault>/<file> | cut -d= -f2-)
OLD=$(grep -m1 '^<VAR>=' <vault>/_backup-credentials/<backup>.env | cut -d= -f2- | tr -d '"')
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $NEW" $APP/api/admin/laporan   # expect 200
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $OLD" $APP/api/admin/laporan   # expect 401
curl -s -o /dev/null -w '%{http_code}\n' $APP/api/health                                          # expect 200
```

Wait for the new deployment to report Ready before probing. Space the calls out: admin endpoints are commonly rate-limited per IP, and a burst turns a passing probe into a 429 that looks like failure.

**More than one variable to change → one per deployment, probe after each.** Batching them turns a breakage into a bisection run against live production; sequential changes keep the cause attached to the deploy that introduced it.

**Rollback while production is broken:** keep the last known-good deployment URL and `vercel promote <url>`. The promoted deployment carries its own env snapshot, so service returns in seconds. Promote never *applies* an env change — for that you need a fresh deployment (a commit you owe anyway is the cheapest trigger; an empty commit is the auditable fallback).

### 6. Docs pass — the rotation is unfinished without it

- Every doc, README, or AGENTS line naming the retired variable is now wrong, **including any documented default value** ("fallback: `'admin'` for development"). Fix the line; do not append a correction underneath it.
- **Sweep the whole tree for the retired name** (`grep -rn <VAR>` over parent DOX, child-DOX index rows, lib/README docs) — fixing only the file that surfaced the rotation leaves siblings stale, and the most damaging stale line is one that promises a default credential which no longer exists.
- Record in the project doc: which variable is authoritative, what was removed, and where the new value lives — **path only, and never inside a public repo**.
- Protected instruction files may be gated. If a write to an `AGENTS.md`/skill file is refused because approval timed out, that is a refusal, not consent: do not retry it and do not reach the same file through another tool. Report the pending edit and ask.

### 7. A credential that died on its own — forensics before deletion

Recipe with the exact probes: `references/dead-credential-forensics.md`. Order of operations:

1. **Localize the failure** before touching the value. Another credential of the *same project* still working (an app-level key, a live endpoint) rules out deletion/pause; a server that answers at the **auth layer** rules out network/DNS.
2. **Test the encoding hypothesis, do not assume it.** Percent-encoding and escaping both mangle stored URLs; analyze the value's structure masked (lengths, counts of `%`/`@`, whether every `%` is a valid `%XX` escape) and probe the stored form *and* a re-encoded variant. Two refusals = the value itself is stale, not the syntax.
3. **Say which part is unknowable.** "Rotated upstream after the copy was saved" is the conclusion; the *date* is not, when the provider's audit log is a paid feature. Do not invent one.
4. **Leak surface — dead is not harmless.** A dead credential still names the host/project/user. Confirm 0 hits in tracked files of public repos (`git grep -F <ref>`); a hit inside a gitlink (mode 160000), an archived/private repo, or an ignored vault path is not a publication.
5. **Remove or replace, with proof.** Timestamped 600 backup of the env file first; then diff the **variable-name list** before/after to show exactly one entry left (`grep <VAR>` proves only the line you aimed at); re-assert 600; confirm the other keys the tooling needs survived.
6. **If it should work again, never ask for the value in chat** — have the user copy the provider's current connection string and let a local script read the clipboard, printing only the length.

## Pitfalls

- **An unprobed rotation is an unverified claim.** The 401 on the old credential is the evidence; the platform's "success" message proves only that you wrote a value.
- **App alive + dependency failing right after a "type-only" env change is the escape trap, not a platform incident.** Symptom set: the health endpoint reports `app: ok` with the dependency in error, and endpoints that query the store return 5xx. Restore with `vercel promote` to the last good deployment first (service back in seconds), then decode the value and re-send it, then redeploy.
- **`--value` writes the secret into shell history and tool logs.** stdin only.
- **A "weak but not default" credential is still the finding.** Testing an endpoint with the obvious default token is worth doing — a 401 there is good news you can report, and it tells you whether full rotation or urgent revocation is required.
- **Do not merge this with git-history sanitisation.** A secret already committed stays readable after deletion; that class needs rotation plus history work, and the deletion alone is not remediation.
- **Confirm which environment you changed.** Most platforms store values per environment (production/preview/development) and the inventory will show it; rotating production while preview keeps the old value is a half-fix worth stating.
- **A failing credential is not automatically a deleted resource.** Localize first: same-project credential working + auth-layer error = the resource exists and the *value* is wrong. Concluding "the project is gone" sends the user chasing a provider that is fine.
- **A stale credential is not the same as no risk.** It still discloses host and project ref; run the tracked-file sweep and report the result rather than assuming there is nothing to say.
- **An incomplete consumer sweep reported as a conclusion is worse than no sweep.** "Nothing depends on it" from a repo-only grep is a claim about the places you searched, not about the system — the agent's own MCP/config data directories are exactly where such consumers hide.

## Verification

- [ ] Inventory read for types, not just names
- [ ] Old state backed up into a 600 file in a git-ignored path
- [ ] Fallback/legacy variables in the auth chain handled, not just the primary one
- [ ] New value set as *sensitive* via stdin
- [ ] New deployment Ready before probing
- [ ] New credential → success, old credential → unauthorized, public endpoints → unchanged
- [ ] Docs naming the retired variable corrected; pending gated edits reported rather than forced
- [ ] Dead credential: failure localized (auth layer vs connectivity) and the service proven alive by another credential
- [ ] Encoding hypothesis tested, not assumed
- [ ] Every consumer enumerated — repo, CI, cron, and agent-side paths — before deletion
- [ ] Removal proven by variable-name list diff, 600 re-asserted, unrelated keys intact, backup path reported
