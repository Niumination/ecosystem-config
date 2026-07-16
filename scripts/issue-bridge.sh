#!/bin/sh
# issue-bridge.sh — Niumination BACKLOG → GitHub Issues sync
# Cron: setiap 6 jam (no_agent=true)
# Map @project tag → GitHub repo untuk semua task di BACKLOG

LOCKDIR="/tmp/issue-bridge.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ issue-bridge: Lock exists — already running"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

NIUMINATION="/Users/zaryu/Desktop/Niumination"
BACKLOG="$NIUMINATION/BACKLOG.md"
LOG="$NIUMINATION/brain/logs"
mkdir -p "$LOG"

echo "📡 issue-bridge — $(date '+%Y-%m-%d %H:%M WIB')"
echo ""

# Map @project → GitHub repo
map_repo() {
  case "$1" in
    tedeo)              echo "Niumination/TEDEO" ;;
    kune-ya)            echo "Niumination/kune-ya.com" ;;
    pemdi-aceh-tengah)  echo "Niumination/PemdiAcehTengah" ;;
    niu-flow)           echo "Niumination/Niu-Flow" ;;
    niu-vermilion)      echo "Niumination/Niu-Vermilion" ;;
    niu-dash)           echo "Niumination/niu-dash" ;;
    niu-cast)           echo "Niumination/niu-cast" ;;
    flame-ade)          echo "Niumination/Flame-ADE" ;;
    niu-lkh)            echo "Niumination/Niu-LKH" ;;
    brain)              echo "Niumination/brain" ;;
    tedeo-kanban)       echo "Niumination/TEDEO-Kanban" ;;
    niu-studio)         echo "Niumination/niu-studio" ;;
    maze-3d)            echo "Niumination/maze-3d" ;;
    niude)              echo "Niumination/niude" ;;
    niuterm)            echo "Niumination/niuterm" ;;
    *)                  echo "" ;;
  esac
}

# Write tasks to temp file, one per line: priority|status|title|desc|tag
TMPFILE=$(mktemp /tmp/issue-bridge-XXXXXX)
trap "rm -f '$TMPFILE'; rmdir '$LOCKDIR' 2>/dev/null" EXIT

CURRENT_SECTION=""
grep -n '' "$BACKLOG" | while IFS=':' read -r linenum line; do
  # Detect section header (P1/P2/P3)
  case "$line" in
    *"P1"*"Critical"*) CURRENT_SECTION="P1" ;;
    *"P2"*"Active"*)   CURRENT_SECTION="P2" ;;
    *"P3"*"Minor"*)    CURRENT_SECTION="P3" ;;
  esac

  # Match parseable task line
  task=$(echo "$line" | grep -oE '^- \[[ x~-]\] \*\*(.+?)\*\* — .+ — @[a-z0-9_.-]+' 2>/dev/null)
  [ -z "$task" ] && continue

  title=$(echo "$task" | sed -n 's/^- \[.\] \*\*\(.*\)\*\* — .* — @.*/\1/p')
  desc=$(echo "$task" | sed -n 's/^- \[.\] \*\*.*\*\* — \(.*\) — @.*/\1/p')
  tag=$(echo "$task" | sed -n 's/.*@\(.*\)/\1/p' | tr -d '[:space:]')
  status=$(echo "$task" | sed -n 's/^- \[\(.\)\].*/\1/p')

  [ -z "$tag" ] || [ -z "$title" ] && continue

  echo "$CURRENT_SECTION|$status|$title|$desc|$tag" >> "$TMPFILE"
done

CREATED=0; CLOSED=0; SKIPPED=0; ERRORS=0; COUNT=0
MAX_TASKS=20
LOG_FILE="$LOG/issue-bridge-$(date '+%Y%m%d').log"

# Read temp file line by line (no subshell!)
while IFS='|' read -r priority status title desc tag; do
  [ -z "$tag" ] && continue
  [ -z "$title" ] && continue
  [ -z "$priority" ] && priority="P3"

  [ "$COUNT" -ge "$MAX_TASKS" ] && break
  COUNT=$((COUNT+1))

  # Only process P1-P2 for issue creation
  case "$priority" in
    P1|P2) ;;
    *) SKIPPED=$((SKIPPED+1)); continue ;;
  esac

  repo=$(map_repo "$tag")
  [ -z "$repo" ] && continue

  issue_title="[Ecosystem] $title"

  # Map status
  case "$status" in
    "x"|"-") target_state="closed" ;;
    *)       target_state="open" ;;
  esac

  # Search existing issues
  existing=$(gh issue list -R "$repo" --search "\"$issue_title\"" --state all --json number,state --jq '.[0]' 2>/dev/null)

  if [ "$existing" = "null" ] || [ -z "$existing" ]; then
    # Create new issue
    body="**Source:** BACKLOG.md — @$tag\n**Description:** $desc\n**Priority:** $priority\n---\nAuto-synced from Niumination ecosystem."
    result=$(gh issue create -R "$repo" --title "$issue_title" --label "ecosystem,tier-1" --body "$body" 2>&1)
    case "$result" in
      *"github.com"*)
        CREATED=$((CREATED+1))
        num=$(echo "$result" | grep -oE 'issues/[0-9]+' | head -1)
        echo "  ✅ [$tag] $title → $num"
        echo "$(date '+%H:%M') CREATE [$tag] $title $num" >> "$LOG_FILE"
        ;;
      *)
        ERRORS=$((ERRORS+1))
        echo "  ❌ [$tag] $title — $(echo "$result" | head -1)"
        ;;
    esac
  else
    # Issue exists — check state
    current_state=$(echo "$existing" | grep -o '"state":"[^"]*"' | sed 's/"state":"//;s/"//' | tr '[:upper:]' '[:lower:]')
    if [ "$current_state" != "$target_state" ]; then
      if [ "$target_state" = "closed" ]; then
        num=$(echo "$existing" | grep -o '"number":[0-9]*' | grep -o '[0-9]*')
        gh issue close "$num" -R "$repo" --comment "Auto-closed per BACKLOG status" >/dev/null 2>&1
        CLOSED=$((CLOSED+1))
        echo "  🔒 [$tag] $title → closed (#$num)"
        echo "$(date '+%H:%M') CLOSE [$tag] $title #$num" >> "$LOG_FILE"
      else
        num=$(echo "$existing" | grep -o '"number":[0-9]*' | grep -o '[0-9]*')
        gh issue reopen "$num" -R "$repo" >/dev/null 2>&1
        echo "  🔓 [$tag] $title → reopened (#$num)"
      fi
    else
      SKIPPED=$((SKIPPED+1))
    fi
  fi

  sleep 0.3
done < "$TMPFILE"

rm -f "$TMPFILE"

echo ""
echo "--- Ringkasan: +$CREATED created | 🔒 $CLOSED closed | -$SKIPPED unchanged | ❌ $ERRORS errors ---"
echo "$(date '+%H:%M') SUMMARY created=$CREATED closed=$CLOSED skipped=$SKIPPED errors=$ERRORS" >> "$LOG_FILE"
