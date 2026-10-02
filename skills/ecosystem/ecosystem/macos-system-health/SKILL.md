---
name: macos-system-health
description: "Use when auditing macOS disk, RAM, or service health."
tags: [macos, disk, memory, launchd, health, triage]
last_updated: "2026-10-01"
version: 1.0.0
---

# macOS System Health Audit

Trigger: "periksa seluruh sistem", "why is the Mac slow", "disk penuh", "check memory", "apa yang jalan".

Deliverable: a report that separates **measured state** from **actionable reclaim**, with the command output as proof. Report — do not delete. Every destructive reclaim needs an explicit owner pick.

## Order of inspection

Cheapest and most decisive first; `du` on this user's home runs for minutes, so never start there.

```bash
uptime                                    # load vs core count
df -h / /System/Volumes/Data              # capacity on the Data volume, not just /
sysctl -n hw.memsize; vm_stat; sysctl vm.swapusage
top -l 1 -n 0 | grep -E 'CPU usage|PhysMem'
pmset -g therm                            # thermal throttling changes every other reading
```

Then attribute, don't just count:

```bash
du -sh ~/* 2>/dev/null | sort -rh | head -15
du -sh ~/Library/Caches ~/Library/Application\ Support 2>/dev/null | sort -rh
ps -Ao rss=,comm= | sort -rn | head -15        # per-process RSS, in MB
ps -Ao rss= | awk '{s+=$1} END{printf "%.1f GB\n", s/1048576}'   # compare against physical RAM
```

Then services, and check them against both `launchctl` and the port:

```bash
launchctl list | awk 'NR>1{print $3}'
lsof -ti :<port>                              # empty means NO listener
```

`scripts/disk-holders.sh` runs the whole attribution pass plus the interrupted-pack scan.

## Pitfalls

- **`du` on a top-level dir hides the culprit inside `.git`.** A config repo measuring multi-GB is almost always its object store, not its files. Always `du -sh <dir>/.git/objects/*` before proposing anything — the working tree is usually kilobytes.

- **Interrupted `git gc`/`repack` leaves multi-GB `tmp_pack_*` that `git count-objects` cannot see.** `count-objects` reports loose objects only, so a repo can report a modest size while `.git/objects/pack/` holds gigabytes. Find them by name, then confirm each is orphaned before removing:
  ```bash
  ls -lhS <repo>/.git/objects/pack/ | head
  stat -f '%Sm' -t '%Y-%m-%d %H:%M' <repo>/.git/objects/pack/tmp_pack_*
  file <repo>/.git/objects/pack/tmp_pack_*        # "Git pack, version 2, 1 objects" = truncated write
  pgrep -fl 'git (gc|repack|pack)'                # MUST be empty, and lsof shows no holder
  ```
  Safe to delete only when no `git gc`/`repack` is running, `lsof` shows no holder, and the file is a `tmp_pack_*` (never a real `pack-<sha>.pack`, which is still referenced).

- **A loud repeating log line is not an outage.** Transport-level retried paths (DNS re-walks, sticky-IP failover) can emit hundreds of WARNINGs while delivery stays healthy. Judge by the transport, not the log volume: established sockets plus a message that actually arrived beat any count of warnings. Reporting "Telegram is broken" off warning counts alone is a false alarm.

- **No listener means "never registered", not "crashed".** A port with no process is either a service that was never added to `launchctl` or one that was never meant to run in this context. Check `launchctl list` before calling it a failure, and do not start it unprompted — a missing dashboard port is often deliberate hiatus.

- **Not every cache is reclaimable.** A browser binary inside `~/Library/Caches` may be the *live process* backing a running tool. Check `ps` and `lsof` against the cache path before listing it as free space; deleting it kills the running tool.

- **Browser plugin-containers dominate RSS invisibly.** `ps` shows one line per container, so the top-15 view is really one app. Group by parent (`grep -c plugin-container`) before attributing memory, and report the aggregate — the user needs "Firefox ≈ N GB across M processes", not ten rows.

- **`swap 0` with high RAM usage is not yet a problem.** Report pressure plus swap together; on a lightly-swapped machine the reclaim advice is "close the heavy app", not "restart".

- **Quote the reclaim total honestly.** Sum only paths proven idle. If the biggest safe win is a few GB, say so plainly instead of implying the disk crisis is larger than it is.