---
name: ecosystem-live-status-reporting
description: Use when producing live verified ecosystem status reports.
tags: [ecosystem, status, audit, verification, niumination]
---

# Ecosystem Live Status Reporting

Produce a report of the Niumination ecosystem that matches CURRENT live conditions. The owner asks variants of "laporan status lengkap" / "pastikan sesuai kondisi aktual" / "tidak ada yang terlewat" — the deliverable must be re-verified against the machine right before handoff, never copied from docs or an earlier snapshot.

## Procedure

1. **Probe live state first, in one batch.** Run the parallel probes (below) in a single turn — they are independent.
   - **Layer the pass by scope, deepest last.** A three-layer ask (host, then agent, then ecosystem) should probe in that order and in batches, because later layers reinterpret earlier ones — the ecosystem's git gate changes how you describe the host's secret exposure, and the agent's `auto_prune` setting explains an ecosystem-level disk finding. Probing all three at once loses that context and produces three disconnected lists instead of one causal picture.
2. **Capture a fresh timestamp.** `date "+%Y-%m-%d %H:%M:%S %Z"` and `uptime`; label EVERY number you later report with its capture time. Name the report file with the ACTUAL current date (`date +%Y-%m-%d`), not the day drafting started.
3. **Probe set (read-only, batchable):**
   - Hardware/OS: `system_profiler SPHardwareDataType`, `sw_vers`, `df -h /`, `uptime`, `memory_pressure -Q`.
   - Launchd services: `launchctl list 2>/dev/null | grep -iE 'niu|9router|hermes|camofox|nosleep|mission'`.
   - Listening ports: `lsof -iTCP -sTCP:LISTEN -P | grep -E '5200|20128|9377'`.
   - HTTP health: curl each of `:5200/`, `:20128/v1/models`, `:9377/` and record the code.
   - Hermes runtime: sqlite3 on `~/.hermes/state.db` (sessions, per-thread model + `datetime(last_activity_at,'unixepoch','localtime')`, message counts, 7d count).
   - Cron: `hermes cron list` — capture EVERY job's Name, Schedule, Last run, Dispatch ("late"/"GAGAL").
   - Git root: `git status --short` + top log.
   - Deploy status: `docs/registry/deployment-status.md` — but verify against live curl for the top N URLs; docs drift.
   - Repo-wide facts: count repos live (`find -maxdepth 3 -name .git`), then check every repo's branch, dirty count, and remote in one loop. Non-default branches, missing remotes, third-party remotes, and project folders with no `.git` at all are findings a root-level `git status` never surfaces.
- Compare config vs runtime and call out drift. `~/.hermes/config.yaml` channel_overrides often differ from what state.db shows as the active per-thread model — report the gap explicitly; do not normalize the number to match either source. Treat these as two different facts, not a conflict to resolve: config.yaml is the configured truth, state.db is the historical truth of what last ran.
5. **Document vs filesystem drift is a finding, not an error.** When AGENTS.md lists projects/services that are missing (e.g. cc-acehtengah hiatus) or filesystem has projects not in AGENTS.md (abstract-studio, kopi-aceh-app-android, mata-aihackfest-2026), list them as findings.
6. **Write the report to `docs/reports/`** (never new subfolders; never `docs/reference/`). Keep a `## Bukti` block with the exact commands + exit codes.
   - **Recommendations are CONDITIONAL on the ask, not a default section.** When the owner says "laporkan apa adanya" / "tidak perlu rekomendasi" / "cukup laporan", ship a pure report: findings, drift, and an explicit "not verified" list — zero recommendations, zero priority rankings, zero proposed actions. Offering advice after being told not to is a correction, not helpfulness. When recommendations ARE wanted, keep them numbered and separated from the findings so the report stays usable as a status record.
7. **Before handoff, re-verify.** If user asks "pastikan / periksa lagi", re-run the probe set and diff every number you cited; update the file in place.

## Always-on rules

- Verification-first: do not claim success from docs, transcripts, or memory — only from commands you just ran, with evidence attached.
- Stale numbers are the #1 failure. Every count must have a capture timestamp. Never quote a figure from a skills file, an earlier report, or this skill's own text — count live even when a documented value looks recent.
- Report the truth even when it is uncomfortable (server down, idle threads, failed cron). Owner values honest status over optimistic gloss.
- When you find a doc that contradicts the machine, the MACHINE wins; note the drift, never "fix" the doc silently.

## Pitfalls (condensed)

- 9router catalog count: parse JSON with python3 and count `data[]` — `grep -o '"id"'` counts nested ids and inflates (718 vs real 252).
- Skill counts: THREE distinct numbers exist and all three are correct for different definitions — manifest `skillCount`, live `SKILL.md` count minus `.archive`, and Hermes target `~/.hermes/skills` (which adds bundled skills). A fourth number from a status script may use yet another definition. **Report the three SOURCES you counted, never hardcoded values** — the numbers drift weekly, and a value baked into this skill is wrong by the next sync. Same rule for repo counts and folder sizes: count live, never quote a remembered figure.
- Cron jobs: `hermes cron list` renders only a FEW entries per invocation, so a job showing "active" is not one that ran. Check EACH job's Last run / Dispatch ("late", "catch-up after missed fire", "GAGAL") and its `last_error`, then cross-read `~/.hermes/cron/jobs.json` for the model/pin each job actually carries. Historical `Last failure` lines are NOT open incidents — a "recovered since" suffix is the tell.
- MC health: HTTP 000 + LaunchAgent absent = down. ALSO verify `start.sh` runs `npx next start` from a directory that HAS package.json — MC app lives in `apex-ui/`; root has none, so the LaunchAgent path fails structurally.
- Timestamps/PIDs/message counts drift minute-to-minute — always fresh `date`; a PID captured in one session is not the running PID later.
- `.env` can contain a key twice (AUXILIARY_VISION_API_KEY duplicate) — check `grep -oE '^[A-Z_]+=' ~/.hermes/.env | sort | uniq -d`.
- When a docs folder recurs, expect it to hide diff collisions: skills/... names exist in BOTH `~/Desktop/Niumination/skills/` and `~/.hermes/skills/`, so `skill_view(name)` can be ambiguous. Prefer absolute paths, and if a tool refuses to guess, read the BANK copy directly at `~/Desktop/Niumination/skills/...`.

## Before/after (sebelum vs sesudah) reports

When the ask is "what changed, and what is different now", the anchor is the **pre-change backup copy**, not a remembered baseline. Ecosystem projects routinely sit next to their own backup — `AGENTS.md.bak-<ts>`, `config.yaml.good.<ts>`, `.gitleaks.toml.bak-<ts>`, `jobs.json.bak-<ts>`. `diff <backup> <current>` yields the exact before/after table; a paragraph describing the old state from memory yields nothing quotable and usually gets one row wrong.

- **"Re-run N times" is a batching directive, not repetition.** Interpret it as N sweeps over different evidence sources, each appended to one accumulating file, then a single synthesized report — never N identical full re-runs. Identical calls cost the same as one and produce nothing new.
- **Mining an agent's session history for what it changed.** An agent's own SQLite (`~/.local/share/<agent>/…db`, or the Hermes `state.db`) is read-only probeable: `sqlite3 "file:<db>?mode=ro" "select … from session_message"`. Session records reveal intent and reasoning the artifacts cannot. Treat what you extract as a CLAIM to verify against the machine, not as evidence — see `references/verifying-machine-generated-changes.md`.
- **Every state protection drifts, so re-probe it before asserting it.** FileVault, a service loopback binding, a permission bit, an allowlist entry: a report that asserted one of these last week is evidence about last week. Re-run the probe (`fdesetup status`, `diskutil apfs list | grep -i filevault`, `lsof -nP -iTCP:<port> -sTCP:LISTEN`) and report the current value.
- **A drifted doc goes in the report as its own numbered section**, headed something like "penyimpangan dokumen vs kondisi live", not as a footnote. A reader who trusts the earlier report will act on it; the divergence list is the most actionable part of the deliverable.

## Verification tools

- `scripts/eco-guard-verify.sh` — the ecosystem's own composite health probe (services, ports, secrets hygiene, DR paths, repo duplication). Run it FIRST for any status/health ask; it classifies findings as MASALAH / PERIKSA / OK and surfaces what the docs do not mention. Same probe as `bash ~/.hermes/scripts/eco-guard.sh verify` when the cron wrapper path will not resolve.
- `hermes cron list` — job inventory + last-run status (render is truncated; see the cron pitfall above).
- `gitleaks detect --no-banner --redact` — confirm the secret gate's own "no leaks found" claim instead of inheriting it from a prior report.
- `sqlite3 "file:<db>?mode=ro" "pragma integrity_check;"` — a DB that must not be written (live `state.db`, an agent's session db) is probed read-only this way.
- `unzip -t <archive> >/dev/null; echo $?` — proves a backup artifact is intact before reporting it as a valid restore path; a `.partial` sibling file is NOT a completed backup.

## Arithmetic and attribution gates

These four produce confidently-wrong numbers, which is worse than a missing number because they get acted on.

- **Confirm a numeric field's UNIT before deriving anything from it.** A restart log of 13–15 digit values is microseconds; assuming milliseconds and dividing by `1e3` invents rates and durations out of nothing (and dividing the real microseconds by `1e6` makes every event look like it happened decades ago). Cross-check the unit against a sibling log that carries ISO timestamps, or against mtime deltas, BEFORE doing arithmetic.
- **A failure count is not an open incident.** Before reporting "failing N times" as ongoing, check whether the fix already landed (`git log --date=iso` on the affected repo). A gate that broke one run and was patched the next day is a closed incident; reporting it as a live recurring failure inflates severity and sends the owner chasing a resolved bug. State both: the failure, and the evidence the fix exists.
- **Read a protection before reporting it absent.** A small hook file's existence says nothing about whether a secret gate is wired; `cat` it and confirm it actually invokes the scanner and that `core.hooksPath` is set in the live clone. `.gitignore` alone is a weak claim — verify the gate exists rather than asserting the gap.
- **Attribute a resource figure or do not report it.** "Disk 87% full" is not a finding. Rank the consumers (`du -sh` per top-level dir, then drill into the offenders) and report the attribution; an unattributed percentage sends the owner looking in the wrong place. Name the single largest item and its path.
- **Check PPID before declaring a process conflict.** A port held by a `next-server` whose parent is the tray process you expected is a child, not a squatter. `ps -p <pid> -o pid,ppid,command` and `lsof -p <pid> | grep cwd` settle it in one call.

## When revising a report you already delivered

Corrections get their own visible table, not silent edits. Add a short "corrections" section naming each wrong claim, what the verified value is, and the command that settled it. A revised report that quietly changes three numbers leaves the owner unable to tell which version to trust — and the ones you got wrong are exactly the ones they would have acted on.

## References

- `references/deployment-status-verification.md` — deriving deploy status from live probes: 503 vs paused, hostname ≠ project name, never-deployed as its own state, hosted-vs-deployed credential risk.
- `references/resource-attribution.md` — turning a bare usage percentage into an addressable finding: rank-then-drill, config bounds vs measured size, unrotated logs, read-only probing.
- `references/verifying-machine-generated-changes.md` — auditing changes an agent or job made that you did not: split into verified-true / verified-false / untestable before touching git; never paraphrase a failure cause you did not reproduce; run the changed program before trusting the change.
