# Kanban-Sync Format Reference

## BACKLOG.md Parseable Task Format

Every actionable task in BACKLOG.md follows:

```
- [STATUS] **Title** — Description — @project-tag
```

### Components

| Segment | Regex | Example |
|---------|-------|---------|
| Bullet | `^- ` | `- ` |
| Status bracket | `\[[ ox]\]` | `[o]`, `[ ]`, `[x]` |
| Bold title | `\*\*[^*]+\*\*` | `**TEDEO T1**` |
| Separator | ` — ` | ` — ` |
| Description | `.*` | `JWT fallback for expired tokens` |
| Project tag | `@[a-z0-9_-]+` | `@tedeo` |

### Status Mapping

| BACKLOG | Kanban DB `status` | Meaning |
|---------|-------------------|---------|
| `[ ]` | `todo` | Pending, not started |
| `[o]` | `in_progress` | Actively being worked on |
| `[x]` | `done` | Completed |

### Task ID Convention

```bash
task_id="backlog-$(slugify title)-${project}"
```

Where `slugify` = lowercase + replace non-alphanum with hyphens.

Example: `- [x] **Niu-LKH v3.1.1** — — @niu-lkh`
→ `backlog-niu-lkh-v3-1-1-niu-lkh`

### Edge Cases

- **No bold title found**: fallback to the text between status bracket and first `—`
- **No project tag found**: assign to `@unassigned`
- **Multiple `@` tags**: last one wins
- **Em-dash in description**: only the first `—` is the separator

## The Script (kanban-sync.sh)

```bash
#!/bin/sh
# kanban-sync.sh — Parse BACKLOG.md → Sync ke Kanban DB
# Cron: setiap 1 jam (no_agent=true)

LOCKDIR="/tmp/kanban-sync.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ Lock exists"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

BACKLOG="/Users/zaryu/Desktop/Niumination/BACKLOG.md"
DB="/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db"

[ ! -f "$BACKLOG" ] && { echo "❌ BACKLOG.md not found"; exit 1; }
[ ! -f "$DB" ] && { echo "❌ kanban.db not found"; exit 1; }

echo "📋 Kanban Sync — $(date '+%Y-%m-%d %H:%M')"

grep -E '^- \[.\] .*@[a-z0-9_-]+' "$BACKLOG" | while read -r line; do
  status_char=$(echo "$line" | sed -n 's/^- \[\(.\)\].*/\1/p')
  case "$status_char" in
    " ") kanban_status="todo" ;;
    "o") kanban_status="in_progress" ;;
    "x") kanban_status="done" ;;
    *) kanban_status="todo" ;;
  esac

  title=$(echo "$line" | sed -n 's/.*\*\*\([^*]*\)\*\*.*/\1/p')
  [ -z "$title" ] && title=$(echo "$line" | sed 's/^- \[.\] //' | sed 's/ —.*//')

  project=$(echo "$line" | sed -n 's/.*@\([a-z0-9_-]*\).*/\1/p')
  [ -z "$project" ] && project="unassigned"

  desc=$(echo "$line" | sed 's/.*— //' | sed 's/ — @.*//' | sed 's/ @.*//')

  task_id="backlog-$(echo "$title" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9_' '-')-${project}"

  existing=$(sqlite3 "$DB" "SELECT id FROM tasks WHERE id='$task_id'" 2>/dev/null)
  now=$(date +%s)

  if [ -z "$existing" ]; then
    sqlite3 "$DB" "INSERT INTO tasks (id, title, body, status, priority, created_at, workspace_kind) VALUES ('$task_id', '$(echo "$title" | sed "s/'/''/g")', '$(echo "$desc" | sed "s/'/''/g") | @$project', '$kanban_status', 0, $now, 'scratch')" 2>/dev/null
    echo "  ✅ Added: $title (@$project)"
  else
    sqlite3 "$DB" "UPDATE tasks SET title='$(echo "$title" | sed "s/'/''/g")', body='$(echo "$desc" | sed "s/'/''/g") | @$project', status='$kanban_status' WHERE id='$task_id'" 2>/dev/null
  fi
done

echo "✅ Kanban sync complete"
```

## Testing

```bash
bash /Users/zaryu/Desktop/Niumination/scripts/kanban-sync.sh
```

Then verify:
```bash
sqlite3 /Volumes/HermesAgent/HermesAgentUSB/data/kanban.db \
  "SELECT status, COUNT(*) FROM tasks WHERE id LIKE 'backlog-%' GROUP BY status"
```

Expected output: 3 rows (todo, in_progress, done) with 41+ total tasks depending on BACKLOG.md size.
