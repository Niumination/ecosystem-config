# Local Patch Preservation During Hermes Update

**Date:** 2026-09-09
**Verified by:** Afrizal Munthe (Niumination)

## The Problem

When updating Hermes via `hermes update` or `git pull upstream main`, local patches that modify upstream-tracked files cause merge conflicts. The update can stall, timeout, or fail silently.

**Example (9 Sep 2026):**
- Local patch: commit `05ef3d7518` adds `_wait_for_send_paths_healthy()`, `_lifecycle_status_block()`, `_send_home_channel_startup_notifications()` to `gateway/run.py`
- Upstream `gateway/run.py` has been completely restructured (modularization in v0.21.x)
- Result: merge conflict → `temp-merge-test` branch created and abandoned → update failed

## Detection — Check for Local Patches Before Updating

```bash
cd /Users/zaryu/src/hermes-agent

# Count commits ahead of upstream
git rev-list --count upstream/main..HEAD

# List local-only commits
git log --oneline upstream/main..HEAD

# Check which files local commits touch
git diff --name-only upstream/main..HEAD
```

If `git rev-list --count upstream/main..HEAD` > 0, you have local patches that need preservation.

## Preservation Workflow

### Step 1: Export Local Patches

```bash
cd /Users/zaryu/src/hermes-agent

# Create a diff of all local changes vs upstream
git diff upstream/main..HEAD > /tmp/hermes-local-patches-$(date +%Y%m%d).diff

# Also save individual commit diffs
mkdir -p /tmp/hermes-patches
git log --oneline upstream/main..HEAD | while read hash msg; do
    git show "$hash" > /tmp/hermes-patches/${hash}.patch
done
```

### Step 2: Analyze Patch Survivability

For each local patch, determine:
1. **Function addition** (e.g., new method in a class) → May need re-insertion at new location
2. **Bug fix** → Check if upstream already fixed it
3. **Config change** → Re-apply via `hermes config set` after update

### Step 3: Hard Reset to Upstream

```bash
cd /Users/zaryu/src/hermes-agent

# Backup current state
cp -r . ../hermes-agent-backup-$(date +%Y%m%d)

# Reset to upstream
git fetch upstream main
git reset --hard upstream/main
```

### Step 4: Re-apply Patches

For function additions:
1. Locate the new file/section where the function should live
2. Insert the function at the appropriate location
3. Verify it doesn't conflict with upstream changes

For config changes:
```bash
hermes config set <path> <value>
```

### Step 5: Verify

```bash
hermes --version
hermes config show
hermes status
# Verify local functions still exist in source (notif helpers moved to run_notifications.py pasca-modularisasi v0.21.x)
grep -n "_wait_for_send_paths_healthy\|_lifecycle_status_block" gateway/run_notifications.py
```

## Current Local Patches (Niumination, as of 2026-09-10)

Local HEAD is 3 commits ahead of upstream/main (plus 100+ upstream commits behind — see update plan). Verify anytime with `git log --oneline upstream/main..HEAD`.

| Commit | File | Description | Status |
|--------|------|-------------|--------|
| `0da89439d3` | `gateway/run_notifications.py` | Notif gateway Bahasa Indonesia + status block + bounded-wait (restore dari `05ef3d7518` ke struktur baru pasca-modularisasi v0.21.x) | Active — wajib export sebelum update, upstream menimpa file ini |
| `e1b7e2e6d1` | `gateway/run_turn.py` | Suppress normal final send saat stale finalize dengan `_final_response_sent` (duplicate-send fix) | Active — cek apakah upstream sudah menyerap saat update |
| `c6b22d0edc` | `gateway/stream_consumer.py` | Cegah duplicate final send saat stream consumer sudah push konten (duplicate-send fix) | Active — cek apakah upstream sudah menyerap saat update |
| `05ef3d7518` | `gateway/run.py` (struktur lama) | Patch notif asli era pre-modularisasi | Superseded oleh `0da89439d3` — commit masih ada di reflog bila teks lama dibutuhkan lagi |
| `0224447274` | `gateway/run.py` | Merge resolution | Obsolete |

## Pitfall: `hermes update` Timeout

`hermes update` often times out because:
1. Gateway restart takes longer than the tool timeout
2. Merge conflicts block the automatic pull
3. Network latency during large pulls (7,935+ commits)

**Workaround:** If `hermes update` times out, check actual state:
```bash
ps aux | grep hermes | grep -v grep
git log --oneline -1
hermes --version
```

If the process is still running but the tool timed out, the update may actually be in progress. Wait and check again in 2-3 minutes.

## Post-Update Local Patch Re-apply Checklist

After updating to a new upstream version:

1. [ ] Run `hermes --version` to confirm new version
2. [ ] Check if local patches are still needed (upstream may have absorbed them)
3. [ ] For each needed patch, find the new insertion point
4. [ ] Apply patch manually at the new location
5. [ ] Verify with `grep -n "function_name" <file>`
6. [ ] Restart gateway: `launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway`
7. [ ] Verify gateway starts cleanly: `tail -f ~/.hermes/logs/gateway.error.log`
