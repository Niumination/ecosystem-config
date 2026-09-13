---
name: macos-launchd-services
description: Keep macOS always-on services alive; recover launchd plists.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [macos, launchd, launchagent, caffeinate, nosleep, persistent-service, 9router, hermes-gateway, mission-control, insiden-recovery]
    related_skills: [niu-9router-maintain, env-doctor, dotfiles-maintenance]
---

# macOS Launchd Persistent Services

The Niumination workstation runs several always-on services that MUST stay up or Telegram routing / dashboards break. This skill covers verifying them, writing correct LaunchAgents, and recovering after a config-wipe incident (e.g. the 27-Agu-2026 jcode wrong-dir wipe that deleted `~/Library/LaunchAgents/*.plist`).

## When to Use
- "Mac ku kok bisa sleep / tidur?" → caffeinate/no-sleep LaunchAgent hilang
- "9router mati", "Mission Control mati", "gateway Hermes mati"
- After ANY bulk-delete / jcode wrong-directory incident — user-scoped LaunchAgents in `~/Library/LaunchAgents` are NOT in any git repo and get wiped silently
- "cek service lokal" / "cek ekosistem"

## Known Services (inventory)
Full table + exact health commands in `references/services-inventory.md`.

| Service | Port | Plist | Critical? |
|---|---|---|---|
| Hermes Gateway | ephemeral | `ai.hermes.gateway.plist` | ✅ `KeepAlive` — auto-restarts |
| 9router (model router) | 20128 | `com.9router.autostart.plist` | ✅ Telegram channels depend on it; auto-restart |
| 9router cache-watch | — | `com.niumination.9router-watch.plist` | ⚪ NON-CRITICAL, can be dead |
| Mission Control UI | 5200 | `com.niumination.missioncontrol.plist` | ⚠️ UI-only; FastAPI backend is a separate process |
| No-sleep (caffeinate) | — | `com.niumination.nosleep.plist` | ✅ PREVENTS MAC SLEEP |

## Health-Check Recipe (read-only, run first)
```bash
# is a port listening?
lsof -iTCP:20128 -sTCP:LISTEN -P -n
# is a launchd service loaded/alive?
launchctl list | grep -iE "9router|missioncontrol|nosleep|hermes"
# is the process there?
pgrep -fl caffeinate
pgrep -fl "hermes_cli.main gateway"
# does the service actually respond?
curl -s -o /dev/null -w "%{http_code}" -m 8 http://localhost:20128/v1/models
```

## Creating a LaunchAgent (correct pattern)
Every always-on service plist MUST have BOTH:
```xml
<key>RunAtLoad</key>
<true/>
<key>KeepAlive</key>
<true/>
```
Without `KeepAlive` the service won't restart if it crashes; without `RunAtLoad` it won't start at boot.

Load / restart:
```bash
# first load (fails if already loaded):
launchctl load ~/Library/LaunchAgents/com.niumination.nosleep.plist
# restart an already-loaded service (preferred over load):
launchctl kickstart -k gui/$(id -u)/com.niumination.nosleep
# verify:
launchctl list | grep nosleep
pgrep -fl caffeinate
```

## The No-Sleep / Caffeinate Case (most common loss)
After a config-wipe the no-sleep LaunchAgent disappears and `pmset sleep` reverts to `1` → Mac sleeps and kills everything (gateway, 9router, MC).
Recovery: deploy `templates/nosleep.plist` (caffeinate `-s -d -i -m`) and load it.
Verify the assertion is actually held:
```bash
pmset -g assertions | grep -i "PreventUserIdleSystemSleep"
# expect: pid <X>(caffeinate): ... PreventUserIdleSystemSleep named: "caffeinate command-line tool"
pmset -g | grep sleep   # shows "sleep prevented by caffeinate"
```
Flags: `-s` AC-powered, `-d` display, `-i` idle, `-m` disk.

## 9router Sync Notification Spam Fix
The `9router-sync.sh` script (hybrid watcher) fires `osascript display notification` on EVERY model-list delta. When the 9router model catalog flip-flops (e.g., 517↔521 every ~60s due to provider connection churn), this floods the macOS notification center.

**Fix (apply to `scripts/9router-sync.sh`):**
1. **Remove the `osascript` notification block entirely** — log-only is sufficient. The notification was a UX regression, not a feature.
2. **Add debounce window (120s):** record the first change timestamp to `~/.cache/niumination/9router-models.stable`. Only commit the change if the hash stays stable for the full window. Flip-flops within the window are discarded.
3. **Raise curl timeout 10s→30s** — the catalog is large post-update (`model-catalog-raw.json` 528K+), and 10s times out silently.
4. **Remove redundant `com.niumination.9router-watch.plist`** (StartInterval 60s, too aggressive) — `com.niumination.9router-sync.plist` (300s + WatchPaths) is sufficient. Two pollers racing on the same hash file cause duplicate notifications.

Verify fix: run the script twice within 30s — the second run should print "change pending" and exit without committing.

**Post-fix launchctl state:**
- `com.9router.autostart` → running (server)
- `com.niumination.9router-sync` → running (single watcher)
- `com.niumination.9router-watch` → removed

## Pitfalls
- **`launchctl load` fails with I/O error** if the agent is already loaded/collides → use `launchctl kickstart -k gui/$(id -u)/<label>` instead.
- **Do NOT edit `~/.hermes/config.yaml` via patch/write_file** — agent is blocked (security). Use `hermes config set <key> <value>`.
- **Mission Control `/api/*` → 404 is normal** if only the Next.js UI (`apex-ui`) runs and the FastAPI backend process is not up — that's a separate process, not a routing failure.
- **9router provider management** belongs in `niu-9router-maintain`, not here.
- User-scoped LaunchAgents are NOT in any git repo → back the plist files up (e.g. copy to `~/Desktop/Niumination/dotfiles/` or a timestamped archive) so a future incident can't wipe them silently. The 27-Agu insiden proved this.
- **`KeepAlive:false` = SILENT DEATH (most dangerous mistake).** Unlike `KeepAlive` missing, a plist with `KeepAlive:false` LOADS FINE and the process shows up in `launchctl list` — but when the server child exits (common in tray-mode apps without a TTY), launchd does NOT restart it. Symptom: `launchctl list` shows the PID, yet `curl → 000` and `lsof -iTCP:PORT -sTCP:LISTEN` is EMPTY. 29-Agu: `com.9router.autostart` had `KeepAlive:false` → 9router died every few minutes, Telegram routing broke, and it looked "alive" in launchctl. Fix: set `KeepAlive` to `<true/>` (not just present — must be boolean true), unload+load, then verify with `lsof` (must show LISTEN), not just `launchctl list`.
- **Network dependency at boot/login:** if a service needs outbound network/DNS immediately after `RunAtLoad`, it can fail before the macOS network stack is ready. Symptom: launchd runs the service at login, then the service logs DNS/network errors and exits; `KeepAlive` restarts it, but the first message may already be missed. This happened with Hermes Gateway: Telegram notification delivery failed on the first startup after boot because DNS was not yet available. Fix: add a small network-wait wrapper before the real service command, with a bounded timeout so boot does not hang indefinitely.
- **Race condition on startup:** after `load`/`kickstart`, a server may take ~10s before it binds the port. `curl → 000` in the first seconds is NOT a crash — retry 3-5× with 2s gaps before concluding it's dead.

## Hybrid Watcher Pattern (WatchPaths + StartInterval)
For poller/notifier services that should run on a schedule AND instantly when a watched file changes, use BOTH keys (don't pick just one):
```xml
<key>StartInterval</key>
<integer>300</integer>            <!-- poll every 5 min -->
<key>WatchPaths</key>
<array>
  <string>/Users/zaryu/.9router/db/data.sqlite</string>   <!-- trigger instantly on change -->
</array>
```
Used by `com.niumination.9router-sync.plist` (see `templates/9router-sync.plist`): polls `/v1/models` every 5 min AND fires the moment `providerConnections` changes in the 9router DB, then hashes model IDs and posts a macOS notification only on delta. Backup copy lives in `~/Desktop/Niumination/scripts/com.niumination.9router-sync.plist`.

## Portable backup convention
Any LaunchAgent plist that is modified for a network-wait or recovery fix should be backed up into the portable Hermes repo:
`~/Desktop/Niumination/apps/JHermUSB-portable/config/launchd/<label>.plist`
This keeps the local `~/Library/LaunchAgents/` file and a git-tracked copy aligned.

## Skill-sync conflict pattern
When `sync-to-agents.sh` reports a target skill newer than bank, do **not** assume the target is always the source of truth.
1. Inspect whether the target edit is a local runtime mutation or a real content improvement.
2. If it is a real improvement, backport target → bank (`cp`) then regenerate manifest and re-sync.
3. If it is only a local artifact, overwrite target with bank.

## References
- `references/services-inventory.md` — full service table + exact health commands
- `templates/nosleep.plist` — ready-to-deploy caffeinate LaunchAgent
- `templates/9router-sync.plist` — hybrid WatchPaths+StartInterval notifier (realtime model-change alerts)
- `references/gateway-network-wait-fix-2026-08-30.md` — Hermes Gateway DNS-at-boot incident and wrapper fix
- `references/browser-capture-waf-bypass.md` — Playwright browser capture on laptop for WAF-blocked endpoints (Jalur G2)
