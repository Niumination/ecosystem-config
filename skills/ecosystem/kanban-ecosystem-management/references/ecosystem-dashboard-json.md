# Ecosystem Dashboard JSON (generate-ecosystem-json)

> **⚠️ DEPRECATED.** This pipeline (`generate-ecosystem-json.py`) no longer exists on the filesystem. The script was removed and `ecosystem-status.json` is now an orphan file (47 bytes, stale). The Niu-Dash ecosystem view now gets data directly from the **Kanban API** (port 5199) via `GET /api/ecosystem`, with a `flatProjects` JS-side fallback. The standalone `ecosystem.html` page uses inline auto-date/stats calculated from its own project array. This reference is preserved for historical understanding of the old pipeline — do NOT attempt to run the `generate-ecosystem-json.py` commands below.

## Overview (Historical)

`generate-ecosystem-json.py` formerly read the current state from BACKLOG.md, AGENTS.md, and the kanban DB to produce `ecosystem-status.json` — the data source for the Niu-Dash ecosystem view (GH Pages dashboard).

Old location: `/Users/zaryu/Desktop/Niumination/scripts/generate-ecosystem-json.py` (REMOVED)

## Data Source

| Input | Purpose |
|-------|---------|
| `BACKLOG.md` | Task counts (total, P1, P2, P3) via `grep -c` |
| `AGENTS.md` | Project tier, priority, and description strings |
| Kanban DB (`kanban.db`) | Task status breakdowns via SQLite query |

## Output

Output path: `Production/niu-dash/public/data/ecosystem-status.json`

**⚠️ CRITICAL PITFALL: The old output path `projects/niu-dash/...` is STALE.** The active Niu-Dash repo and GH Pages deployment live at:
- **Active:** `Production/niu-dash/`
- **Stale:** `projects/niu-dash/` (old location, no longer deployed)

The Python script had this path wrong until Jun 24, 2026. Always verify the OUTPUT variable at the top of the script before regenerating.

## After a Production/ Move

When you move a project from `projects/` to `Production/`, three things can break the ecosystem JSON pipeline:

1. **eco-collect.py misses the repo** — If `auto_discover_git_repos()` doesn't scan `Production/*`, the moved repo drops from the manifest count. Add `Production/*` scan level before running `--force`.
2. **generate-ecosystem-json.py has stale paths** — The PROJECTS dict at the top of the script may reference paths like `projects/xxx/`. Update paths to `Production/xxx/` if the script reads files from the project dir.
3. **Ecosystem count explodes** — If both projects/ AND Production/ versions exist simultaneously (partial move), the manifest double-counts. After a clean move, only one should exist. Run `eco-collect --force` and verify the count matches expectations.

### Quick check after move
```bash
python3 scripts/eco-collect.py --force 2>&1 | grep "Total"
```

## Pipeline

After pushing new Git repos or updating project status:

```bash
cd ~/Desktop/Niumination

# Step 1: Refresh eco-collect manifest
python3 scripts/eco-collect.py --force

# Step 2: Verify manifest is current
python3 -c "
import json
m = json.load(open('brain/logs/eco-manifest.json'))
print(f'Git repos: {m[\"total_git\"]}')
print(f'Non-git items: {m[\"total_non_git\"]}')
print(f'Total: {m[\"total_items\"]}')
"

## JSON Format

```json
{
  "version": 2,
  "generated_at": "2026-06-24T15:00:22+07:00",
  "total_tasks": 55,
  "kanban": {
    "active": N,
    "todo": N,
    "done": N,
    "archived": N
  },
  "backlog": {
    "total": 55,
    "p1": N,
    "p2": N,
    "p3": N
  },
  "projects": [
    {
      "name": "TEDEO",
      "tier": 1,
      "status": "in_progress",
      "priority": "P1",
      "git": "Niumination/TEDEO",
      "dox": true,
      "desc": "..."
    }
  ]
}
```

## Migration History (sh → py)

The original script was `generate-ecosystem-json.sh` — a bash heredoc that produced malformed JSON when `grep -c` output had embedded newlines (`p1: 0\n0` instead of `p1: 0`). Migrated to `generate-ecosystem-json.py` on Jun 24, 2026 using `json.dump()` for reliable output.

Key changes during migration:
- Shell `grep` → Python `re.search()` / `re.findall()`
- Heredoc (`cat > file << EOF`) → `json.dump(data, f, indent=2)`
- Output path fixed from `projects/niu-dash/...` → `Production/niu-dash/...`
- 4 additional projects added to the data source (niumination-workspace, niu-kanban-dash, orchestrator, Ultra)

## Project Data Source

Projects are defined in a Python dictionary at the top of the script. Each entry maps to the AGENTS.md catalog row format:

```python
PROJECTS = {
    "TEDEO": {"tier": 1, "priority": "P1", "status": "in_progress", "git": "Niumination/TEDEO", ...},
    ...
}
```

When adding a new GitHub-pushed project, add its entry here and in `eco-collect.py`'s `NON_GIT_DIRS` (if it was previously non-git).
