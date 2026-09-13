---
name: github-auth-recovery
description: Recover broken GitHub auth and rotate compromised keys.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# GitHub Auth Recovery

Recover when GitHub access breaks: SSH key flagged by audit, stale PAT claims,
or push rejected while `ssh -T` succeeds. Diagnose with live probes first —
never trust remembered auth state (a PAT remembered as "401" may test `200` today).

## Symptom matrix (probe, don't guess)

```bash
git remote -v                                    # https or ssh?
ssh-add -l                                       # agent identities (may be empty while ~/.ssh files work)
ssh -o BatchMode=yes -o ConnectTimeout=8 -T git@github.com
git push --dry-run origin main                   # real push test, zero side effects
curl -s -m 10 -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer $(cat <pat-file>)" https://api.github.com/user
```

| Observation | Meaning |
|---|---|
| `ssh -T` → `Hi <user>!` but push → `ERROR: ... SSH key audit ... private key found in a public repository` | Key leaked into a public repo; GitHub locked it. ROTATE (below), never approve it |
| PAT probe → `200` | PAT valid, regardless of what memory/notes claim |
| PAT probe → `401` | PAT dead — regenerate at github.com/settings/tokens |
| dry-run shows `old..new main -> main`, no error | Auth healthy; safe to push for real |

## Rotation recipe (proven Sep 2026)

```bash
# 1. Identify the flagged key id (ids/titles only — safe to display)
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/user/keys \
  | python3 -c "import json,sys; [print(k['id'],'|',k['title']) for k in json.load(sys.stdin)]"

# 2. Generate replacement (ed25519; empty passphrase only for automation hosts)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_<name> -N "" -C "<name>-<date>"
chmod 600 ~/.ssh/id_ed25519_<name>

# 3. Register via API (needs admin:public_key; else paste the .pub at github.com/settings/keys)
PUB=$(cat ~/.ssh/id_ed25519_<name>.pub)
curl -s -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H Accept:application/vnd.github+json \
  -d "{\"title\":\"<name>\",\"key\":\"$PUB\"}" https://api.github.com/user/keys

# 4. Pin it (IdentitiesOnly stops the flagged key being offered first)
printf '\nHost github.com\n  IdentityFile ~/.ssh/id_ed25519_<name>\n  IdentitiesOnly yes\n' >> ~/.ssh/config

# 5. Verify BEFORE deleting anything
git push --dry-run origin main

# 6. Only then: revoke old key (expect 204) + delete local compromised files
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE \
  -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user/keys/<OLD_ID>
rm -f ~/.ssh/<old_key> ~/.ssh/<old_key>.pub
```

## Rules

- Never display secret values (private keys, tokens) — HTTP codes, key ids, and fingerprints only.
- Never approve/re-arm a leaked key; the leaked copy in the public repo stays compromised.
- Update stored auth notes after recovery — stale "blocked" claims mislead future sessions.
