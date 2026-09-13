# Hermes Update Procedure & Version Pitfalls

**Date:** 2026-09-09
**Verified by:** Afrizal Munthe (Niumination)

## The "Up to date" Trap

`hermes --version` reports "Up to date" when the local install matches the **installed package version**, NOT when it matches `upstream/main`. This is misleading.

**Example (9 Sep 2026):**
- `hermes --version` → "Up to date" 
- Actual: `v0.20.5` (2026.8.19) — commit `02244472`
- Upstream: `v2026.9.7` (v0.21.1) — released 2026-09-07
- **7,935 commits behind upstream**

## Correct Update Check

```bash
cd /Users/zaryu/src/hermes-agent
git fetch upstream main --quiet 2>&1
git rev-list --count HEAD..upstream/main 2>&1  # actual behind count
git log --oneline HEAD..upstream/main 2>&1 | head -10
```

## Update Methods

### Method 1: `hermes update` (Recommended)
- Approved but often times out
- Gateway restarts automatically
- If it fails: check `ps aux | grep hermes` for running processes

### Method 2: Manual git pull
```bash
cd /Users/zaryu/src/hermes-agent
git pull upstream main
# Then restart gateway:
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

### Method 3: If update stalls
```bash
# Check gateway status
ps aux | grep hermes | grep -v grep

# Force restart
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

## Post-Update Verification

```bash
hermes --version 2>&1
git log --oneline -1 2>&1
# Both should show new version/commit
```

## OpenCode `x-opencode-session` Header Issue

**Problem:** OpenCode Go relay requires `x-opencode-session` header on every request. Starting 09/06/2026, requests without it will error.

**Fix:** PR #101864 (https://github.com/NousResearch/hermes-agent/pull/101864)

**Status (9 Sep 2026):**
- NOT in local Hermes (v0.20.5, commit `02244472`)
- ZERO references to `x-opencode-session` in codebase
- PR #101864 not found in `git log --all --grep="101864"`
- Provider plugins don't include session header logic

**Affected:** `opencode-free`, `opencode-zen`, `opencode-go` providers
**NOT affected:** Nous Portal provider (`inclusionai/ling-3.0-flash-fin:free`)

**Workaround:** Patch `plugins/model-providers/opencode-*.py` to add `x-opencode-session` header from `session_id` in `build_api_kwargs_extras()`, or wait for upstream merge.

## Config Drift Detection

When `hermes status` shows different model/provider than `hermes config show`:

```bash
hermes config show 2>&1 | grep -A4 "Model:"
hermes status 2>&1 | grep -A2 "Model:"
```

If they differ → drift exists. Fix by syncing config.yaml to match runtime via `hermes config set`.
