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
- Stale numbers are the #1 failure. Every count must have a capture timestamp.
- Report the truth even when it is uncomfortable (server down, idle threads, failed cron). Owner values honest status over optimistic gloss.
- When you find a doc that contradicts the machine, the MACHINE wins; note the drift, never "fix" the doc silently.

## Pitfalls (condensed)

- 9router catalog count: parse JSON with python3 and count `data[]` — `grep -o '"id"'` counts nested ids and inflates (718 vs real 252).
- Skill counts: THREE distinct numbers exist and all three are correct for different definitions — manifest `skillCount`, live `SKILL.md` count minus `.archive`, and Hermes target `~/.hermes/skills` (which adds bundled skills). A fourth number from a status script may use yet another definition. **Report the three SOURCES you counted, never hardcoded values** — the numbers drift weekly, and a value baked into this skill is wrong by the next sync. Same rule for repo counts and folder sizes: count live, never quote a remembered figure.
- Cron jobs: `hermes cron list` shows up to FIVE (Tab Stash, Brain Top-10, Model Probe, DR Snapshot, up-eco-lightfix). Check EACH job's Last run / Dispatch — one can be "late" (1h6m) and one GAGAL exit 1 while others run fine.
- MC health: HTTP 000 + LaunchAgent absent = down. ALSO verify `start.sh` runs `npx next start` from a directory that HAS package.json — MC app lives in `apex-ui/`; root has none, so the LaunchAgent path fails structurally.
- Timestamps/PIDs/message counts drift minute-to-minute — always fresh `date`; a PID captured in one session is not the running PID later.
- `.env` can contain a key twice (AUXILIARY_VISION_API_KEY duplicate) — check `grep -oE '^[A-Z_]+=' ~/.hermes/.env | sort | uniq -d`.
- When a docs folder recurs, expect it to hide diff collisions: skills/... names exist in BOTH `~/Desktop/Niumination/skills/` and `~/.hermes/skills/`, so `skill_view(name)` can be ambiguous. Prefer absolute paths, and if a tool refuses to guess, read the BANK copy directly at `~/Desktop/Niumination/skills/...`.

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
