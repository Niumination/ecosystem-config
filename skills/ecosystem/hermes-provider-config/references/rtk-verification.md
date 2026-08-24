# RTK Verification Recipe (verified 18 Ags 2026)

User asks "periksa apakah rtk benar diterapkan" — verify with these direct probes, then report in ≤5 lines. Do NOT write history recaps or fix anything unasked.

## Quick probes

```bash
# 1. Binary version
rtk --version            # → rtk 0.45.0

# 2. Plugin enabled in active config
grep -A3 "plugins:" /Volumes/HermesAgent/HermesAgentUSB/data/config.yaml
# → enabled: [rtk-rewrite]

# 3. Rewrite actually fires (exit code semantics)
rtk rewrite "git status" ; echo "exit: $?"
# → prints rewritten command "rtk git status", exit 3 = REWRITTEN
rtk rewrite "npm install" ; echo "exit: $?"
# → exit 1 = pass-through (no RTK equivalent)

# 4. Savings stats (global scope)
rtk gain
# → Total commands, tokens saved %, top commands
```

## Exit code semantics (critical)
- `3` = command rewritten to RTK version
- `1` = pass-through (no equivalent)
- `0` = normal command result

## Interpretation (18 Ags 2026 snapshot)
- Binary: `rtk 0.45.0` (Homebrew)
- Plugin `rtk-rewrite`: enabled in config → intercepts Hermes `terminal()` calls
- Savings: 68.6% (2,265 commands, 6.3M tokens, avg 2.1s/cmd)
- Top: `rtk grep` 323×, `rtk read` 166×

## Pitfalls
- Config write protection: `patch`/`write_file` to config.yaml is REFUSED by Hermes — always `hermes config set ...`
- Plugins physically present in `data/plugins/` ≠ enabled in config `plugins.enabled` — check both
- `~/.claude/settings.json` (Claude Code hooks) is a SEPARATE thing from the Hermes plugin — user does NOT use Claude Code; do not touch it
