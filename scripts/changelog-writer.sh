#!/bin/sh
# changelog-writer.sh — Update ecosystem-changelog.md dengan snapshot harian
# Cron: setiap hari jam 20:00 (no_agent=true, deliver=local)

LOCKDIR="/tmp/changelog-writer.lock"
mkdir "$LOCKDIR" 2>/dev/null || exit 1
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

NIUMINATION="/Users/zaryu/Desktop/Niumination"
CLOG="$NIUMINATION/brain/docs/ecosystem-changelog.md"
BACKLOG="$NIUMINATION/BACKLOG.md"

total=$(grep -cE '^- \[.\]' "$BACKLOG" 2>/dev/null || echo 0)
done_t=$(grep -cE '^- \[x\]' "$BACKLOG" 2>/dev/null || echo 0)
active=$(grep -cE '^- \[~\]' "$BACKLOG" 2>/dev/null || echo 0)
cancelled=$(grep -cE '^- \[-\]' "$BACKLOG" 2>/dev/null || echo 0)
pending=$((total - done_t - active - cancelled))

dirty=0
for repo in projects/TEDEO Production/kune-ya.com projects/Niu-Flow Production/niu-vermilion Production/PemdiAcehTengah Production/niu-dash projects/flame-ade projects/niu-cast Production/Niu-LKH brain projects/TEDEO-Kanban projects/x-downloader; do
  d="$NIUMINATION/$repo"
  [ -d "$d/.git" ] || continue
  (cd "$d" 2>/dev/null && git diff --quiet HEAD 2>/dev/null) || dirty=$((dirty + 1))
done

DATE=$(date '+%Y-%m-%d %H:%M WIB')
echo "" >> "$CLOG"
echo "## $DATE — Auto-snapshot" >> "$CLOG"
echo "" >> "$CLOG"
echo "### Stat Snapshot" >> "$CLOG"
echo "- Tasks: $total total ($done_t ✅ / $active 🔄 / $pending ⏳ / $cancelled ⏸)" >> "$CLOG"
echo "- Dirty repos: $dirty" >> "$CLOG"
echo "" >> "$CLOG"

echo "✅ Changelog updated"
