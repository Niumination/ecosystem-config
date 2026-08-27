# Handoff Narrative — Credential Broker Plan (HOLD for active sessions)

_For: Hermes Agent (and any agent picking up this work) · 2026-08-27_

## TL;DR
A central credential broker (`scripts/keys.sh`, macOS Keychain-backed) is
**scaffolded and tested** but its migration phase (**Phase B**) is **ON HOLD**.
Do NOT repoint any tool configs to the broker until the currently-active jcode
sessions have finished. This note exists so the plan is not lost and so no
agent accidentally executes Phase B early.

## Why this note exists
The user is running **2 active jcode sessions** that are mid-task:
- PID 22342 — `_jcode-bin`, 75% CPU, 54m47s elapsed (actively working)
- PID 1028  — `_jcode-bin`, 23% CPU, 1h24m elapsed (actively working)
- (PID 16648 — `_jcode-bin`, ~3% CPU, near-idle — third session)

Migrating live credentials (editing `~/.jcode/config.json`, `opencode.jsonc`,
`~/.hermes/.env`, etc.) while these sessions hold open connections/auth state
would break in-flight requests and could corrupt their context. Therefore:
**Phase B is blocked until those sessions exit cleanly.**

## The plan (context for Hermes)
Full design: `docs/references/credential-broker-design.md`.

- **Tier 1 (broker):** flat AI-API keys → single source in macOS Keychain via
  `scripts/keys.sh`. 17 canonicals already mapped (opencode_zen, openrouter,
  gemini, github, fal, telegram, agentrouter, juan, nine_router, huancheng,
  aerolink, tavily, anthropic, vercel, discord, bing, nvidia_nim).
- **Tier 2 (stays put):** 9router's own upstream key store (broker only
  manages its local `sk-...` token); OAuth tokens stay in native stores.
- **Phase A (DONE):** broker script + roundtrip test; `vault/` perms 755→700;
  this design doc. Committed.
- **Phase B (PENDING — blocked):** per-canonical `keys set` + repoint consumers.
- **Phase C (future):** `keys env` into shell profile + launchd plists; `keys audit`.

## Gate to proceed with Phase B
Only start Phase B after ALL of these are true:
1. `pgrep -f "_jcode-bin" | grep -v menubar` shows **no actively-working**
   sessions (or the user explicitly says "lanjut").
2. No opencode session is mid-request against a key about to be moved.

Safe check: `ps -Ao pid,etime,%cpu,command | grep _jcode-bin | grep -v menubar`

## If you are Hermes and find this mid-flight
- Do NOT edit any credential file.
- Do NOT run `keys set` against live keys yet.
- If the active sessions have clearly finished (per gate above) AND the user has
  approved, proceed with Phase B starting from the lowest-risk canonical
  (`bing`/`tavily`) as a pilot, then the critical ones.
- Rollback is trivial: broker never deletes the source store until the consumer
  is confirmed working against the broker; keep old plaintext as backup until
  verified.

## Status
Phase A committed (scripts/keys.sh + design doc + vault/ 700). Phase B blocked
on active sessions. Waiting for user "lanjut" or session completion.
