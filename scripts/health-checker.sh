#!/bin/sh
# health-checker.sh — Niumination Ecosystem Health Checker
# Cron: tiap 2 jam
# Mengecek: disk usage, git remote status, deploy endpoint health (10 Tier 1)
# Output: stdout → deliver ke Telegram

LOCKDIR="/tmp/health-checker.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ Lock exists — another run in progress"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

NIUMINATION="/Users/zaryu/Desktop/Niumination"

echo "🔍 Niumination Health Check — $(date '+%Y-%m-%d %H:%M')"
echo ""

# 1. Disk usage
echo "## 💾 Disk"
df -h / | tail -1 | awk '{printf "  Used: %s / %s (%s)\n", $3, $2, $5}'

# 2. Git status — check uncommitted changes in key repos
echo ""
echo "## 📦 Git Status (dirty = uncommitted changes)"
dirty=0
for repo in apps/kune-ya.com apps/niu-vermilion apps/PemdiAcehTengah apps/niu-dash desktop/flame-ade services/niu-cast apps/Niu-LKH brain sites/TEDEO-Kanban desktop/x-downloader agents/Ultra labs/niumination-workspace; do
  d="$NIUMINATION/$repo"
  if [ -d "$d/.git" ]; then
    cd "$d" 2>/dev/null
    if ! git diff --quiet HEAD 2>/dev/null; then
      echo "  ⚠️ $repo: dirty"
      dirty=$((dirty + 1))
    fi
  fi
done
[ "$dirty" -eq 0 ] && echo "  ✅ All clean"

# 3. Deploy health — quick HTTP check all 10 Tier 1 projects
echo ""
echo "## 🌐 Deploy Status (Tier 1)"
# Format: label|url|expected_code
checks="
PemdiAcehTengah|https://pemdi-aceh-tengah.vercel.app|200
Niu-LKH|https://niumination.github.io/Niu-LKH|200
kune-ya-com|https://kune-ya-com.vercel.app|200
niu-dash|https://niumination.github.io/niu-dash|200
TEDEO-web|https://tedeo-web.vercel.app|200
Pemdi-Alt|https://pemdi-aceh-tengah.vercel.app/|200
AuditTI-AT|https://niumination.github.io/AuditTI-AT|200
Maze-3D|https://niumination.github.io/Maze-3D-Game---Web-Based|200
kune-ya-preview|https://kune-ya-pxqyveoo4-archk4lis-projects.vercel.app|200
"
up=0
down=0
echo "$checks" | grep -v '^$' | while IFS='|' read -r label url expected; do
  [ -z "$url" ] && continue
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null || echo "000")
  case "$status" in
    200|301|302) echo "  ✅ $label → $status" ;;
    *) echo "  ❌ $label → $status" ;;
  esac
done

echo ""
echo "✅ Health check complete"
