#!/bin/sh
# kanban-sync.sh — Parse BACKLOG.md → Sync ke Kanban DB
# Cron: setiap 1 jam (no_agent=true)
# Format input: `- [STATUS] **Title** — Desc — @project`
# STATUS: ' '=todo, '~'=in_progress, 'x'=done, '-'=cancelled

LOCKDIR="/tmp/kanban-sync.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ Lock exists"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

BACKLOG="/Users/zaryu/Desktop/Niumination/BACKLOG.md"
DB="/Volumes/HermesAgent/HermesAgentUSB/data/kanban.db"

[ ! -f "$BACKLOG" ] && { echo "❌ BACKLOG.md not found"; exit 1; }
[ ! -f "$DB" ] && { echo "❌ kanban.db not found"; exit 1; }

# Parse BACKLOG.md — extract task lines
echo "📋 Kanban Sync — $(date '+%Y-%m-%d %H:%M')"
echo ""

added=0
updated=0
skipped=0

# Temp files untuk subshell-safe counters
ADD_TMP=$(mktemp /tmp/kanban-added.XXXXXX)
UPD_TMP=$(mktemp /tmp/kanban-updated.XXXXXX)
SKIP_TMP=$(mktemp /tmp/kanban-skipped.XXXXXX)
echo "0" > "$ADD_TMP"
echo "0" > "$UPD_TMP"
echo "0" > "$SKIP_TMP"

# Read task lines: - [ ], - [~], - [x], or - [-] with @project
grep -E '^- \[.\] .*@[a-z0-9_-]+' "$BACKLOG" | while read -r line; do
  # Extract status
  status_char=$(echo "$line" | sed -n 's/^- \[\(.\)\].*/\1/p')
  case "$status_char" in
    " ") kanban_status="todo" ;;
    "~") kanban_status="in_progress" ;;
    "x") kanban_status="done" ;;
    "-") kanban_status="cancelled" ;;
    *) kanban_status="todo" ;;
  esac

  # Extract title (bold text between ** **)
  title=$(echo "$line" | sed -n 's/.*\*\*\([^*]*\)\*\*.*/\1/p')
  [ -z "$title" ] && title=$(echo "$line" | sed 's/^- \[.\] //' | sed 's/ —.*//')

  # Extract project tag
  project=$(echo "$line" | sed -n 's/.*@\([a-z0-9_-]*\).*/\1/p')
  [ -z "$project" ] && project="unassigned"

  # Extract description (text between — and @)
  desc=$(echo "$line" | sed 's/.*— //' | sed 's/ — @.*//' | sed 's/ @.*//')

  # Generate task ID
  task_id="backlog-$(echo "$title" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9_' '-')-${project}"

  # Check if task exists
  existing=$(sqlite3 "$DB" "SELECT id FROM tasks WHERE id='$task_id'" 2>/dev/null)
  
  now=$(date +%s)
  
  if [ -z "$existing" ]; then
    sqlite3 "$DB" "INSERT INTO tasks (id, title, body, status, priority, created_at, workspace_kind) VALUES ('$task_id', '$(echo "$title" | sed "s/'/''/g")', '$(echo "$desc" | sed "s/'/''/g") | @$project', '$kanban_status', 0, $now, 'scratch')" 2>/dev/null
    echo "  ✅ Added: $title (@$project)"
    echo $(( $(cat "$ADD_TMP") + 1 )) > "$ADD_TMP"
  else
    sqlite3 "$DB" "UPDATE tasks SET title='$(echo "$title" | sed "s/'/''/g")', body='$(echo "$desc" | sed "s/'/''/g") | @$project', status='$kanban_status' WHERE id='$task_id'" 2>/dev/null
    echo $(( $(cat "$UPD_TMP") + 1 )) > "$UPD_TMP"
  fi
done

# Read counters from temp files
added=$(cat "$ADD_TMP")
updated=$(cat "$UPD_TMP")
skipped=$(cat "$SKIP_TMP")
rm -f "$ADD_TMP" "$UPD_TMP" "$SKIP_TMP"

echo ""
echo "📊 Summary: +$added added, $updated updated, $skipped skipped"
echo "✅ Kanban sync complete"

# === Divergence Detection ===
echo ""
echo "🔍 Divergence Check:"

NIUMINATION="/Users/zaryu/Desktop/Niumination"
LOG_DIR="$NIUMINATION/brain/logs"
mkdir -p "$LOG_DIR"

diverged=0
DIVERGE_TMP=$(mktemp /tmp/kanban-diverge.XXXXXX)
echo "0" > "$DIVERGE_TMP"
LOG_TMP=$(mktemp /tmp/kanban-log.XXXXXX)
echo "" > "$LOG_TMP"

# 1. Detect @project tags with no matching filesystem directory
grep -oE '@[a-z0-9_-]+' "$BACKLOG" | sort -u | sed 's/@//' | while read -r tag; do
  # Map common tags to directory names
  dir_name="$tag"
  case "$tag" in
    tedeo) dir_name="TEDEO" ;;
    niu-lkh) dir_name="Niu-LKH" ;;
    niu-flow) dir_name="Niu-Flow" ;;
    niu-vermilion) dir_name="niu-vermilion" ;;
    niu-dash) dir_name="projects/niu-dash" ;;
    niu-kanban-dash) dir_name="projects/niu-kanban-dash" ;;
    niu-studio) dir_name="projects/niu-studio" ;;
    niude) dir_name="projects/niude" ;;
    niuterm) dir_name="projects/niuterm" ;;
    niutui) dir_name="projects/niutui" ;;
    orchestrator) dir_name="projects/orchestrator" ;;
    terax-ai) dir_name="projects/terax-ai" ;;
    maze-3d) dir_name="projects/maze-3d" ;;
    zen) dir_name="projects/zen" ;;
    pemdi-aceh-tengah) dir_name="PemdiAcehTengah" ;;
    flame-ade) dir_name="projects/flame-ade" ;;
    kune-ya) dir_name="kune-ya.com" ;;
    niu-cast) dir_name="niu-cast" ;;
    tedeo-kanban) dir_name="TEDEO-Kanban" ;;
    brain) dir_name="brain" ;;
    audit) dir_name="AuditTI-AT" ;;
    jhermusb) dir_name="JHermUSB-portable" ;;
    dotfiles) dir_name="dotfiles" ;;
    labs) dir_name="labs" ;;
    pi) dir_name="PI" ;;
    aistudio) dir_name="aistudio-google" ;;
    archive) dir_name="archive" ;;
    audit-ti) dir_name="AuditTI-AT" ;;
    jhcode) dir_name="JHcode" ;;
    mac-web-dashboard) dir_name="Production/mac-web-dashboard" ;;
    arch-web-dashboard) dir_name="Production/arch-web-dashboard" ;;
    ai-first-os) dir_name="Production/ai-first-os" ;;
    # Remote-only repos — skip (no local dir expected)
    agent-router|automata|continue-agent|db-diskominfo|devs-niu|diskominfo-at) continue ;;
    diskominfo-web|dnd-kit|flame-code|forks|free-vps|hermes-v) continue ;;
    kms-spbe|niu-dash-docs|niu-homepage|niu-private|niu-speedtest|niu-startpage) continue ;;
    niu-cyber-search|prakom-surgawi|rekap-spbe|spbe-devops-academy) continue ;;
    virtual-assistance|zaryu-startpage|project|diskominfoweb|diskominfo) continue ;;
  esac
  if [ ! -d "$NIUMINATION/$dir_name" ]; then
    echo "  ⚠️ Orphaned @$tag — no directory for \"$dir_name\""
    echo "1" > "$DIVERGE_TMP"
    echo "- @${tag}: no directory \"$dir_name\"" >> "$LOG_TMP"
  fi
done

diverged=$(cat "$DIVERGE_TMP")
log_entries=$(cat "$LOG_TMP")
rm -f "$DIVERGE_TMP" "$LOG_TMP"

# 2. Detect git repos with no @project in BACKLOG
for repo_dir in "$NIUMINATION"/projects/TEDEO "$NIUMINATION"/Production/kune-ya.com "$NIUMINATION"/projects/Niu-Flow \
  "$NIUMINATION"/Production/niu-vermilion "$NIUMINATION"/Production/PemdiAcehTengah "$NIUMINATION"/Production/Niu-LKH \
  "$NIUMINATION"/Production/niu-dash "$NIUMINATION"/projects/flame-ade "$NIUMINATION"/brain \
  "$NIUMINATION"/projects/niu-cast "$NIUMINATION"/projects/TEDEO-Kanban \
  "$NIUMINATION"/projects/niutui "$NIUMINATION"/Production/arch-web-dashboard \
  "$NIUMINATION"/Production/mac-web-dashboard "$NIUMINATION"/Production/ai-first-os; do
  [ -d "$repo_dir/.git" ] || continue
  repo_name=$(basename "$repo_dir")
  # Check if repo appears in BACKLOG
  if ! grep -qi "$repo_name" "$BACKLOG" 2>/dev/null; then
    echo "  ⚠️ Unregistered repo: $repo_name (has .git but no BACKLOG entry)"
    log_entries="${log_entries}- ${repo_name}: no BACKLOG entry\\n"
    diverged=1
  fi
done

# 3. Log divergence if found
if [ "$diverged" -eq 1 ]; then
  DATE=$(date '+%Y-%m-%d %H:%M')
  {
    echo "=== Divergence Log: $DATE ==="
    echo "$log_entries"
    echo ""
  } >> "$LOG_DIR/divergence-$(date '+%Y%m%d').log"
  echo "  📝 Divergence logged to brain/logs/"
else
  echo "  ✅ No divergence detected"
fi
