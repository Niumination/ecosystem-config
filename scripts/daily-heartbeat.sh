#!/bin/sh
# daily-heartbeat.sh — Niumination Daily Ecosystem Digest
# Cron: setiap hari jam 08:00 WIB (deliver=telegram)
# Output: ringkasan ekosistem harian

LOCKDIR="/tmp/daily-heartbeat.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ Lock exists"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

NIUMINATION="/Users/zaryu/Desktop/Niumination"
BACKLOG="$NIUMINATION/BACKLOG.md"
LOG="$NIUMINATION/brain/logs"

echo "🌅 Niumination Daily Digest — $(date '+%Y-%m-%d %H:%M WIB')"
echo ""

# 1. Task overview from BACKLOG
total=$(grep -cE '^- \[.\]' "$BACKLOG" 2>/dev/null || echo 0)
done_tasks=$(grep -cE '^- \[x\]' "$BACKLOG" 2>/dev/null || echo 0)
active=$(grep -cE '^- \[~\]' "$BACKLOG" 2>/dev/null || echo 0)
cancelled=$(grep -cE '^- \[-\]' "$BACKLOG" 2>/dev/null || echo 0)
pending=$((total - done_tasks - active - cancelled))
echo "📋 Tasks: $total total | $done_tasks ✅ | $active 🔄 | $pending ⏳ | $cancelled ⏸"

# 2. Active P1 projects (in_progress)
echo ""
echo "🎯 Active P1:"
grep -E '^- \[~\]' "$BACKLOG" 2>/dev/null | head -5 | while read -r line; do
  # Strip markdown formatting
  clean=$(echo "$line" | sed 's/^- \[.\] \*\*//;s/\*\* —//')
  echo "  • $clean"
done

# 3. Dirty repos
echo ""
echo "📦 Git Status:"
dirty=0
for repo in projects/TEDEO Production/kune-ya.com projects/Niu-Flow Production/niu-vermilion Production/PemdiAcehTengah Production/niu-dash projects/flame-ade projects/niu-cast Production/Niu-LKH brain; do
  d="$NIUMINATION/$repo"
  [ -d "$d/.git" ] || continue
  cd "$d" 2>/dev/null
  git diff --quiet HEAD 2>/dev/null || { echo "  ⚠️ $repo: uncommitted changes"; dirty=$((dirty + 1)); }
done
[ "$dirty" -eq 0 ] && echo "  ✅ All clean"

# 4. Last divergence log entries
echo ""
echo "📜 Recent Logs:"
ls -t "$LOG"/*.log 2>/dev/null | head -3 | while read -r f; do
  echo "  • $(basename "$f"): $(head -1 "$f" 2>/dev/null | cut -c1-80)"
done
[ "$(ls -t "$LOG"/*.log 2>/dev/null | wc -l)" -eq 0 ] && echo "  (no logs yet)"

echo ""
echo "⏰ Next scheduled: kanban-sync (every 1h), health-check (every 2h)"
echo "✅ Digest complete — have a great day!"
