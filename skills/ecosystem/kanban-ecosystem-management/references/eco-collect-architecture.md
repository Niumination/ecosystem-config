# Ecosystem State Collector Architecture

## Overview

`eco-collect.py` is a zero-cost filesystem scanner that discovers all projects in the Niumination ecosystem (git repos + non-git directories) and detects changes since the last run. It replaces hardcoded project lists with **auto-discovery** to prevent staleness when directories are moved or added.

## Source Code

Location: `/Users/zaryu/Desktop/Niumination/scripts/eco-collect.py`

## Architecture Flow

```
                    ┌──────────────────────────┐
                    │  eco-collect.py          │
                    │  (Python collector)       │
                    └──────────┬───────────────┘
                               ```
                                                   ┌──────────▼───────────────┐
                                                   │  Auto-discover:          │
                                                   │  · root/*/               │
                                                   │  · projects/*/           │
                                                   │  · Production/*/         │
                                                   └──────────┬───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │  Compare vs state file   │
                    │  brain/logs/             │
                    │  eco-manifest.json       │
                    └──────┬──────────┬────────┘
                           │          │
                    ┌──────▼──┐  ┌────▼─────────┐
                    │ NO      │  │ CHANGED      │
                    │ CHANGES │  │ → full       │
                    │ exit 0  │  │   manifest   │
                    └─────────┘  │   JSON       │
                                 └──────┬───────┘
                                        │
                          ┌─────────────▼──────────┐
                          │ LLM agent (Hermes cron)│
                          │ decides if manifest    │
                          │ needs patching         │
                          └────────────────────────┘
```

## Dual Scheduling Strategy

### 1. Hermes Cron — `ecosystem-auto-sync` (every 15m)

```bash
# Created via:
cronjob action=create \
  schedule="every 15m" \
  name="ecosystem-auto-sync" \
  script="eco-collect.py" \
  deliver="local" \
  workdir="/Users/zaryu/Desktop/Niumination" \
  enabled_toolsets=["terminal","file"]
```

- Runs the collector script → stdout injected into agent prompt
- If `NO_CHANGES`: agent sees short output, skips processing (~200 tokens)
- If full manifest: agent compares with state, patches manifest if needed (~6K tokens)
- `deliver=local` means output stays in session log, not pushed to Telegram

### 2. Launchd — `com.niumination.eco-collect` (every 30min + RunAtLoad)

```xml
<!-- ~/Library/LaunchAgents/com.niumination.eco-collect.plist -->
<key>ProgramArguments</key>
<array>
  <string>/usr/bin/python3</string>
  <string>/Users/zaryu/Desktop/Niumination/scripts/eco-collect.py</string>
  <string>--save</string>
</array>
<key>StartInterval</key>
<integer>1800</integer>  <!-- 30 minutes -->
<key>RunAtLoad</key>
<true/>
```

- Runs silently with `--save` flag (no stdout, updates state file in place)
- Keeps the state file warm even when Hermes cron hasn't fired
- Zero cost — no LLM involved, pure mechanical file write

## State File Format

File: `brain/logs/eco-manifest.json`

```json
{
  "version": 2,
  "timestamp": "2026-06-22T15:39:06+07:00",
  "git_repos": {
    "brain": "/Users/zaryu/Desktop/Niumination/brain",
    "TEDEO": "/Users/zaryu/Desktop/Niumination/projects/TEDEO",
    "kune-ya.com": "/Users/zaryu/Desktop/Niumination/projects/kune-ya.com",
    ...
  },
  "non_git": {
    "scripts": "/Users/zaryu/Desktop/Niumination/scripts",
    "Ultra": "/Users/zaryu/Desktop/Niumination/projects/Ultra",
    ...
  },
  "summary": {
    "git_count": 18,
    "non_git_count": 12,
    "total": 30
  }
}
```

The state file is the **single source of truth** for change detection. On each run:
1. Auto-discover current filesystem state
2. Read saved manifest
3. Compare `git_repos` keys + `non_git` keys
4. If identical → `NO_CHANGES`; otherwise → emit new manifest JSON

## Auto-Discovery Logic

Three-level scan: root level (= brain, scripts, docs/) + `projects/` subdirectory + `Production/` subdirectory.

```python
def auto_discover_git_repos(root):
    """Find all .git directories at root level, inside projects/, AND inside Production/"""
    git_repos = {}
    # Level 1: root-level dirs (brain, etc.)
    for item in sorted(os.listdir(root)):
        full = os.path.join(root, item)
        if os.path.isdir(os.path.join(full, '.git')):
            git_repos[item] = full
    # Level 2: inside projects/
    projects_dir = os.path.join(root, 'projects')
    if os.path.isdir(projects_dir):
        for item in sorted(os.listdir(projects_dir)):
            full = os.path.join(projects_dir, item)
            if os.path.isdir(os.path.join(full, '.git')):
                git_repos[item] = full
    # Level 3: inside Production/
    production_dir = os.path.join(root, 'Production')
    if os.path.isdir(production_dir):
        for item in sorted(os.listdir(production_dir)):
            full = os.path.join(production_dir, item)
            if os.path.isdir(os.path.join(full, '.git')):
                git_repos[item] = full
    return git_repos

def auto_discover_non_git(root):
    """Find non-git directories at all three levels"""
    items = {}
    for level in ['', 'projects/', 'Production/']:
        target = os.path.join(root, level)
        if not os.path.isdir(target):
            continue
        for item in sorted(os.listdir(target)):
            full = os.path.join(target, item)
            if not os.path.isdir(full) or item.startswith('.'):
                continue
            if not os.path.isdir(os.path.join(full, '.git')):
                items[item] = full
    return items
```

## Key Design Constraints

1. **brain/ is itself a git repo** — scanned at root level as a git repo, not as a non-git directory
2. **Root Niumination is NOT a git repo** — it contains sub-repos but has no `.git` itself
3. **`projects/` and `Production/`** are the canonical subdirectories — moved projects live in one or the other
4. **No `.`-prefixed dirs** — `.git`, `.trash`, `.hermes` are excluded by `startswith('.')` check
5. **Sorted output** — `sorted(os.listdir(...))` ensures deterministic comparison
6. **`Production/` entry in `NON_GIT_DIRS`** — the dir itself is not a repo, but its sub-git-repos are discovered via the explicit `Production/*` scan level. Do NOT remove `"Production"` from `NON_GIT_DIRS`.

## Cost Analysis

| Scenario | Tokens | Est. Cost (big-pickle) | Frequency | Monthly Cost |
|----------|--------|----------------------|-----------|-------------|
| NO_CHANGES | ~200 | ~$0.0004 | 2880 runs/mo (15m) | ~$1.15 |
| Full manifest (change) | ~6,000 | ~$0.013 | ~5-10 changes/mo | ~$0.13 |
| **Total worst-case** | | | | **~$1.28/mo** |
| **Total typical** | | | | **~$1.20/mo** |

The NO_CHANGES guard saves ~97% of token cost vs running the LLM every tick.

## Pitfalls / Lessons Learned

- **Hardcoded lists WILL go stale** — The original eco-collect.py had a fixed list of 26 projects. When user moved 3 repos to `projects/` and added 4 new items, the script silently reported NO_CHANGES while the ecosystem had actually changed. Auto-discovery is the fix.
- **brain/ as git repo is easy to miss** — The brain vault appears as a regular directory, but has `.git`. Always check for `.git` rather than assuming from the directory name.
- **State file path matters** — Must survive `/tmp` cleanup (use `brain/logs/` not `/tmp/`). Must be writable by both cron and launchd. Must be in version control or ignored via `.gitignore`.
- **Launchd vs cron path differences** — Launchd runs with a minimal PATH. The script uses `/usr/bin/python3` (absolute path) and doesn't depend on project-local binaries. Cron runs through Hermes which inherits the user's PATH.
- **--save flag is essential for launchd** — Without it, launchd would send empty stdout notifications. `--save` suppresses stdout entirely and only writes the state file.
- **Production/ moves require a scan-level update** — When moving repos from `projects/` to `Production/`, the auto-discovery must include `Production/*` scanning. Without this, moved repos disappear from the eco-manifest count (they were counted under `projects/` but aren't detected under `Production/`). Add `scan_dirs += sorted(NIUMINATION.glob("Production/*"))` to the script's `auto_discover_git_repos()` function.
- **`NON_GIT_DIRS` has `"Production"` — this is intentional** — The `Production/` directory itself is not a git repo (it's a container of sub-repos). The list entry prevents it from being listed as a non-git item. Its sub-repos are discovered via the separate `Production/*` scan level.
