---
name: non-provider-secret-detection
description: Use when a vendor-neutral key may reach a public repo.
version: 1.0.0
---

# Non-provider secret detection

Provider-prefix gates (`sk-`, `ghp_`, `AKIA`, `xoxb-`) only catch credentials
issued by those vendors. A self-hosted or internal service key
(`SERVICE_API_KEY=`, `*_ACCESS_KEY=`, `*_ADMIN_KEY=`) has no recognisable prefix,
so it passes every pre-commit hook and secret scan while sitting in a PUBLIC
repo. This skill covers that blind spot.

## Rule 1 — add a suffix rule, not another prefix

Extend the gate on the env-assignment shape rather than the value shape: any
assignment whose key ends in `_KEY` / `_TOKEN` / `_SECRET` / `_PASSWORD` and
whose value is not a `$(...)` command, a `<...>` placeholder, or an empty string
is a finding. A self-hosted key is identified by where it points, not by how it
spells its first six characters.

Prove the new rule with a synthetic positive before trusting a green run. A gate
that has never fired is indistinguishable from a gate that is not wired up.

## Rule 2 — a secret-shaped literal in a doc is presumed live

Before reporting or deleting, confirm the literal is the production credential
rather than an example. Derive the value from the file, then compare hashes
against the live store; equal digests mean the documented value IS the running
credential:

```python
import hashlib, os, re

doc = open(path).read()
lit = re.search(r'SERVICE_API_KEY="?([A-Za-z0-9_\-]+)"?', doc).group(1)

live = None
for line in open(os.path.expanduser("~/.hermes/.env"), errors="replace"):
    if line.strip().startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    if k.strip() == "SERVICE_API_KEY":
        live = v.strip().strip("\"'")

print("match:", hashlib.sha256(lit.encode()).hexdigest()
      == hashlib.sha256((live or "").encode()).hexdigest())
```

Report the leak with masked shape only: length, first and last few characters,
and a short hash prefix. Never the value, never via a command line — a `grep`
for the literal puts it in shell history and process args, which is the same
leak in a different stream. Walk the tree in Python and count matches instead.

## Rule 3 — rotate before purging history, never after

A key that is live in a public repo stays live until it is rotated. Purging
history first, then rotating, hands out a fresh key into a repo whose history is
about to be republished. The order is: rotate, verify the old value is dead,
then purge.

Rotation and history rewriting are production mutations. Report the exposure
with the evidence and the recommended order, and get explicit approval before
touching either.

## Rule 4 — widen the search to every copy, then classify per repo

One leaked literal usually has siblings: a template in a service repo, a
reference in an unrelated skill, a fixture in a script. Walk the whole tree and
for each hit record path, occurrence count, and whether that repo is public or
private — visibility decides urgency, and a private hit is not a
notification-level event. Untracked files (templates, generated output) still
matter because a later `git add` promotes them.
