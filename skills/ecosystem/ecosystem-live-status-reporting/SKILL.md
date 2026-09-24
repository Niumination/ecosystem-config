---
name: ecosystem-live-status-reporting
description: Use when producing live verified ecosystem status reports.
tags: [ecosystem, status, audit, verification, niumination]
---

# Ecosystem Live Status Reporting

Produce a report of the Niumination ecosystem that matches CURRENT live conditions. The owner asks variants of "laporan status lengkap" / "pastikan sesuai kondisi aktual" / "tidak ada yang terlewat" — the deliverable must be re-verified against the machine right before handoff, never copied from docs or an earlier snapshot.

## Procedure

1. **Probe live state first, in one batch.** Run the parallel probes (below) in a single turn — they are independent.
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
4. **Compare config vs runtime and call out drift.** `~/.hermes/config.yaml` channel_overrides often differ from what state.db shows as the active per-thread model — report the gap explicitly; do not normalize the number to match either source.
5. **Document vs filesystem drift is a finding, not an error.** When AGENTS.md lists projects/services that are missing (e.g. cc-acehtengah hiatus) or filesystem has projects not in AGENTS.md (abstract-studio, kopi-aceh-app-android, mata-aihackfest-2026), list them as findings.
6. **Write the report to `docs/reports/`** (never new subfolders; never `docs/reference/`). Keep a numbered Recommendations section, honest pros/cons, and a `## Bukti` block with the exact commands + exit codes.
7. **Before handoff, re-verify.** If user asks "pastikan / periksa lagi", re-run the probe set and diff every number you cited; update the file in place.

## Always-on rules

- Verification-first: do not claim success from docs, transcripts, or memory — only from commands you just ran, with evidence attached.
- Stale numbers are the #1 failure. Every count must have a capture timestamp.
- Report the truth even when it is uncomfortable (server down, idle threads, failed cron). Owner values honest status over optimistic gloss.
- When you find a doc that contradicts the machine, the MACHINE wins; note the drift, never "fix" the doc silently.

## Pitfalls (condensed)

- 9router catalog count: parse JSON with python3 and count `data[]` — `grep -o '"id"'` counts nested ids and inflates (718 vs real 252).
- Skill counts: THREE distinct numbers exist — manifest `skillCount` (~178), live SKILL.md count minus `.archive` (~180), Hermes target `~/.hermes/skills` (~232 incl bundled). Never report AGENTS.md's stale 121.
- Cron jobs: `hermes cron list` shows up to FIVE (Tab Stash, Brain Top-10, Model Probe, DR Snapshot, up-eco-lightfix). Check EACH job's Last run / Dispatch — one can be "late" (1h6m) and one GAGAL exit 1 while others run fine.
- MC health: HTTP 000 + LaunchAgent absent = down. ALSO verify `start.sh` runs `npx next start` from a directory that HAS package.json — MC app lives in `apex-ui/`; root has none, so the LaunchAgent path fails structurally.
- Timestamps/PIDs/message counts drift minute-to-minute — always fresh `date`; a PID captured in one session is not the running PID later.
- `.env` can contain a key twice (AUXILIARY_VISION_API_KEY duplicate) — check `grep -oE '^[A-Z_]+=' ~/.hermes/.env | sort | uniq -d`.
- When a docs folder recurs, expect it to hide diff collisions: skills/... names exist in BOTH `~/Desktop/Niumination/skills/` and `~/.hermes/skills/`, so `skill_view(name)` can be ambiguous. Prefer absolute paths, and if a tool refuses to guess, read the BANK copy directly at `~/Desktop/Niumination/skills/...`.

## References

- `references/ecosystem-verification-pitfalls.md` — full pitfall list with commands.
