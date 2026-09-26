# Verifying deployment status (Vercel) against a registry

A registry that says "5 Live" while three are paused and two do not exist is
worse than no registry: it is confidently wrong, so nobody checks. The fix is
not to patch the numbers by hand — it is to make the numbers impossible to
write from memory.

## Never record a status you did not probe

Status drift has one cause: a row was written once, from memory or from an old
run, and nobody re-derived it. Pausing a deployment is a silent, out-of-band
action — nothing in the repo records it, so the registry keeps claiming the old
state indefinitely.

Rule: **every status row gets re-derived from a live probe in the same session
that writes it.** A row carried over from a previous edit is unverified by
definition.

## What the CLI does and does not tell you

```
vercel whoami
vercel project ls              # name + production URL + age per project
vercel project inspect <name>  # id, created, root dir, node version, framework
```

`project ls` is the source of truth for **which projects exist in the account**.
It answers "is this project even here" — a question the registry never asks,
and the reason two phantom projects survived for weeks.

`project inspect` does **not** expose paused status. Do not go looking for it;
the human-readable output and `--json` / `--format json` both omit the field.
Pause state is only observable over HTTP.

## 503 is not a status

Probing the hostname is necessary and not sufficient. A paused deployment
returns `503`, and so do build errors, crashed runtimes, expired certificates,
and DNS pointing at a retired project. Record "503" as the observation and
resolve it before recording a conclusion.

Read the body. A paused deployment is unambiguous:

```
$ curl -s https://<host>.vercel.app | head -c 200
The deployment is currently unavailable

DEPLOYMENT_PAUSED

sin1::vlckt-...
```

That literal marker is the only thing that distinguishes paused from broken.
Always confirm it before writing `PAUSED` into a registry.

## Hostname is not the project name

Project names and hostnames diverge. Probe the URL column from
`vercel project ls`, never a hostname reconstructed from the project name — a
guessed hostname can return 200 from an unrelated app, or 404 from a host that
never existed, and both read as a real status.

Some projects have no production URL at all. `--` in the URL column means
**never deployed** — a distinct state from paused and from broken. Preserve it
as its own status; collapsing it into "down" loses the fact that nothing was
ever shipped.

## Statuses worth distinguishing

| Observation | Meaning |
|---|---|
| `200` | live |
| `308` then `200` | live behind a redirect — still live, record the chain |
| `503` + `DEPLOYMENT_PAUSED` | paused; no request reaches app code |
| `503`, no marker | broken — do not file under paused |
| no URL in `project ls` | never deployed |
| absent from `project ls` | not in this account; DNS may 000 or 404 |
| `000` | DNS/connection failure — not an app status |

## Custom domains decouple from project hostnames

A custom domain can be live while the project it was meant to point at is
paused, because an A/ALIAS record can be aimed at a different project. Verify
the custom domain separately and state which project actually answers it.
Otherwise the registry implies a live custom domain proves a live project, which
is not a safe inference.

## A hosted credential is a different risk from a deployed one

When deciding whether a leaked secret needs rotating, the question is whether
anything reachable is using it. A credential for a **paused** deployment has no
reachable endpoint to exploit; a credential for a live app does. Pausing is a
legitimate mitigation, and the owner may reasonably accept the residual risk of
the value still sitting in a public git archive.

Record that decision where the next session will read it, with the condition
that invalidates it: "accepted while paused — must rotate before unpausing."
An undocumented decision gets re-litigated, and the condition is what makes the
risk bounded rather than open-ended.

## Make the check cheap enough to actually run

A verification procedure that takes ten minutes will not be run every time, and
a manual re-probe before each status edit is exactly what stops happening. Keep
a list of `host -> project` pairs (one source, not two copies), probe them in a
loop, and diff the result against the registry. The whole check should be a
command, not a project.
