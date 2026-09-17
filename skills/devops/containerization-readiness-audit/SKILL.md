---
name: containerization-readiness-audit
description: Use when asked which projects need Docker.
tags: [docker, containers, audit, deployment, ecosystem]
---

# Containerization Readiness Audit

Answers "which projects actually need Docker?" with a per-repo verdict and a reason — never a
containerize-everything pass. Most repositories in a PaaS-deployed, desktop-heavy tree are a hard NO
for structural reasons, and saying so is the correct answer.

## Procedure

1. **Map the repos, not the directories.** Count `.git` directories under the active category folders
   (`apps/ services/ sites/ desktop/ agents/ labs/ sandbox/ tools/`). Exclude `archive/`,
   `inactive-*`, `node_modules`, `vault/`, `brain/` — they carry credible-looking Dockerfiles that
   would invent a false "we already use Docker".
2. **Scan for signals.** Run `scripts/scan_docker_need.py [root]` → per-repo stack, existing docker
   artifacts, deploy target, DB hints, long-running service hints. Read it with the table below.
3. **Descend one level for `?` stacks.** Monorepo-ish layouts keep the manifest in a subfolder
   (`<proj>/apex-ui/package.json`); a top-level-only check wrongly concludes "no stack".
4. **Confirm how the project runs today** before proposing a container: look for a launchd plist,
   systemd unit, `start.sh`, or a workflow file. A vendored `Dockerfile` from upstream means *the
   upstream project ships one*, not *this project needs containerizing*.
5. **Report the verdict table**, then the ranked candidates. Stop there — see Reporting Shape.

## Verdict Table (always-on)

| Condition found in the repo | Verdict | Why |
|---|---|---|
| Deployed to PaaS (`vercel.json`, `netlify.toml`, Pages workflow, `fly.toml`) | NO | The platform owns the runtime; a container just adds a second deploy path to keep in sync |
| Desktop app (Tauri, Electron, `.xcodeproj`, installer scripts) | NO | Needs the host OS surface a container hides |
| GUI automation (pyautogui, mss, screen capture, accessibility-tree driver) | NO | Requires a real display plus the host accessibility tree; containerizing removes the feature |
| Host-bridge device tooling (ADB, USB, on-host daemon) | NO | Depends on host device access |
| Self-hosted long-running service (systemd unit / launchd plist), or a host that no longer exists | **YES — first candidate** | Re-creatable deploy, isolation for the loop/cron, reproducible data mount |
| Local relational DB needed for dev or migrations (ORM `provider = "postgresql"` + `localhost` URL) | **YES for dev only** | `docker compose up <db>` beats installing a server; production stays on the managed DB |
| Network infrastructure service (TURN, cache, proxy, queue) | **YES** | Genuinely a workload: isolate, pin the image digest, drop capabilities |
| Static site / CLI / WASM build | NO | It is a build step, not a runtime |

Runtime-version drift is NOT by itself a reason to containerize: if the tree has no `.nvmrc`,
`.python-version`, or `.tool-versions` anywhere, nothing is pinned yet, so a container buys no
reproducibility a version file would not. Pin the version first.

## Pitfalls

- **A local `.env.example` pointing at `localhost:<db-port>` is the strongest dev-DB signal** — it
  means someone had to run that database locally to develop or migrate. That is the compose-worthy
  case even when production uses a managed cloud database.
- **Do not read the presence of a `Dockerfile` as a requirement.** Check what is actually running on
  the machine before recommending migration.
- **Repo count is not project count.** Nested `.git` directories (submodules, worktrees) double-count;
  report the per-category tally from the scan, not a raw `find | wc -l`.
- **Absence of containers in a tree is usually a deployment fact, not an oversight** — say which
  mechanism replaced them (PaaS runtime, cloud DB, native desktop) rather than implying a gap.

## Reporting Shape

1. Verdict table: project → verdict → one-line reason.
2. A short root cause for *why* containers are rare here (what replaced them).
3. Ranked candidates, each with the concrete win (what breaks today that a container fixes).
4. One question offering which candidate to start with.

Per this user: close with a `## Bukti` section carrying the probe commands and their real output, and
never start containerizing on an audit request — "periksa" means study and report, execution only
after an explicit "gas"/"kerjakan". If the user then approves a candidate, write the plan before the
Dockerfile, since a `Dockerfile` + `compose.yaml` for a live service is a state-changing change.

## Support Files

- `scripts/scan_docker_need.py` — repo scanner producing the raw verdict input table.
