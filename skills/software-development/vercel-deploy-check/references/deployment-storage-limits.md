# Deployment Storage & Functions Storage (Vercel)

Two metrics, both priced at $0.10 per GB-month on Pro, both included in an
allowance on Hobby (10 GB). They are the usual cause of "the build just will not
start" when the platform status page shows nothing.

| Metric | What it counts |
| --- | --- |
| Deployment Storage | Build output and static assets kept with each retained deployment |
| Functions Storage | Function bundles, **stored once per region Vercel deploys them to** |

## How the number is produced (why it grows while nothing changes)

Vercel records the maximum stored amount for each project on each billing day and
adds those daily amounts across the billing period: 1 GB held for 30 days =
1 GB-month. So the dashboard figure is consumption over the cycle, not bytes on
disk right now — it climbs daily on unchanged content and resets with the cycle.
Do not tell the owner their repository grew; it did not.

Drivers, in order of leverage: retention period, size of each deployment's output,
number of retained deployments across all projects on the team.

## What is NOT the cause

- **Pausing a project.** Pause stops that project serving traffic; it adds nothing
  and removes nothing from counted storage. Paused projects keep counting in full,
  and Vercel's retention exceptions do not mention them — so pausing neither causes
  growth nor buys headroom, and an owner who paused projects to save quota has not
  saved any. State is readable per project: `vercel api "/v9/projects/<name>"` →
  `paused`. Visitors to a paused project get `503 DEPLOYMENT_PAUSED`, which is worth
  raising even when the quota question is settled.
- **A repository that grew.** Bundle size per deployment is a real driver, but the
  metric's accumulation pattern means it climbs on unchanged content too.
- **The platform incident.** An incident and a quota overage are independent; check
  both (`vercel ls` state + the status page) before choosing which to act on.

## Diagnosing

```bash
vercel api "/v9/projects?limit=100"                      # every project + framework
vercel api "/v6/deployments?projectId=<id>&limit=100"    # deployment count per project
vercel inspect <deployment-url>                          # status, target, aliases
```

Direct REST calls need the team scope and a durable token:

```bash
set -a; . ~/.hermes/.env; set +a          # VERCEL_TOKEN — never echo the value
T=<orgId>                                 # from <project>/.vercel/project.json → orgId
curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v9/projects?teamId=$T&limit=50"
curl -s -H "Authorization: Bearer $VERCEL_TOKEN" \
  "https://api.vercel.com/v6/deployments?projectId=<id>&teamId=$T&limit=100"
```

- Without `teamId`, `/v9/projects` answers **HTTP 200 with an empty list** — not an
  error. An empty project list means a missing scope, never a team with no projects.
- The CLI's session token (`~/.local/share/com.vercel.cli/auth.json`) can be stale for
  direct REST use: `{"error":{"code":"forbidden","invalidToken":true}}` while
  `vercel whoami` and `vercel ls` still work, because the CLI refreshes on its own.
  When REST says `invalidToken`, switch to the durable token in the env file before
  concluding the API is closed to you.
- `vercel usage` answers `404 Costs not found` for a token without billing scope. The
  Usage page is dashboard-only, so ask the owner for the current figure rather than
  estimating one.

Count deployments per project before proposing anything: a team of a dozen
Next.js projects accumulates hundreds of retained deployments, and one project
can hit the 100-row page limit on its own. **A count that lands exactly on `limit`
means "at least that many", never a total** — paginate before quoting a number, or
quote it explicitly as a floor. Compare the count against a local build output size
(`du -sh .next`) to show the mechanism instead of asserting it.

Attribution, once you have a list to aggregate:

- Split by `target` — production history and preview history age differently, and
  they have different retention exceptions.
- Count `readyState`: failed/canceled deployments still consume storage until
  retention removes them.
- Read the **age spread**, not just the count. A hundred deployments created inside
  a few days is one burst (automation, or a heavy editing stretch), which is a very
  different finding from steady growth over months — and only the burst points at a
  trigger worth fixing.
- The **list payload omits `alias`**; only a single-deployment detail carries it.
  A "zero protected deployments" count computed from the list is meaningless — do
  not quote it, and do not conclude protection status from it.

## Retention on Hobby (defaults)

- Default retention is 30 days for Canceled / Errored / Pre-Production / Production.
- Exceptions keep a deployment alive regardless of age: the last 3 deployments
  created, the last 3 Production deployments in state Ready, any deployment holding
  a production alias, custom-environment branch aliases, and the latest preview of
  an active Git branch.
- When a Hobby team is over the allowance, deployments outside those exceptions are
  deleted immediately instead of at the 30-day mark — storage can fall on its own,
  so re-check before recommending manual deletion. A figure that moved DOWN between
  two readings is this mechanism at work, not measurement noise.

## Reading vs proving the retention policy

The configured policy is **not readable from the CLI or the REST API**. No
`retention` field appears on `/v9/projects/<id>`, and
`vercel list <project> -p canceled=1d -p errored=1d -p preview=7d -p production=30d`
reports nothing about the project's stored values — it renders a *Proposed
Expiration* column computed from the values YOU passed, and prints `No expiration`
for anything an exception covers (a deployment holding a production alias never
expires). Read that column as a simulation, never as the setting in force.

So verify by effect: count deployments per project, split by `target`, and read the
age spread.

- **Governed and shrinking:** low count, recent age ceiling — nothing survives far
  past its policy window.
- **Not governed:** alias-free deployments far older than the window. That is the
  actionable finding — name those projects so the owner can open Project → Settings
  → Security.
- **Ambiguous:** a team-wide drop right after an overage is Vercel's own over-quota
  deletion, which looks identical in the count. Attribute before concluding that a
  policy you set is working.

Answering "do I need to set it again?": **no.** A retention policy is a standing rule
that covers every deployment created after it is saved; nothing is configured per
deployment. The catch is scope — a **team-level** policy governs **new projects
only**, and replaces every existing project's policy only if "Apply this policy to
all existing projects" was ticked at save time. A team policy saved without that box
leaves existing projects on their previous (usually default) behaviour, which is
exactly what "some projects still hold 100-day-old deployments" looks like from the
outside.

## Levers, cheapest first

1. Shorten the retention policy (available on all plans). Canceled/Errored to 1 day,
   Preview to 7 days, Production to 30 days is a sane start; keep Production long
   enough to cover the rollback window the owner actually wants.
2. Reduce per-deployment output: `outputFileTracingExcludes` for files functions
   never read, and remove region duplication (each configured region stores its own
   copy of every bundle).
3. Archive or delete dormant projects.
4. Upgrade if headroom is genuinely needed — at $0.10 per GB-month, tens of
   GB-months cost a few dollars.

Deleting individual deployments is possible (`vercel api -X DELETE
/v13/deployments/<id>`) but removes rollback history: propose, do not execute,
unless the owner explicitly asks. Background deletion jobs take up to ~48 hours and
re-evaluating previously protected deployments up to 30 days — measure again later,
not immediately.

## Dashboard paths (owner-facing)

Project-wide: **Project → Settings → Security → Deployment Retention Policy**.
Default for new projects: **Team → Settings → Security & Privacy → Deployment
Retention Policy**, leaving "Apply this policy to all existing projects" unchecked
unless the owner wants every project overwritten at once. Start with the projects
holding the most deployments — the Usage page breaks the totals down per project.
