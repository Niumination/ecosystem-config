#!/bin/sh
# gitleaks-weekly.sh — Scan semua repo Niumination dengan gitleaks
# Cron: setiap Minggu jam 06:00 (no_agent=true)
# Config: ~/.gitleaks.toml (global custom rules)
# Falls back to built-in rules jika config tidak ada

LOCKDIR="/tmp/gitleaks-weekly.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ Lock exists"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

NIUMINATION="/Users/zaryu/Desktop/Niumination"
# Try multiple locations for custom config
CONFIG=""
for try_path in "$HOME/.gitleaks.toml" "/Users/zaryu/.gitleaks.toml"; do
  [ -f "$try_path" ] && { CONFIG="$try_path"; break; }
done
REPORT_DIR="$NIUMINATION/brain/logs"

echo "🔐 Gitleaks Weekly Scan — $(date '+%Y-%m-%d %H:%M')"
echo ""

issues=0
scanned=0
CONFIG_FLAG=""
[ -n "$CONFIG" ] && CONFIG_FLAG="--config=$CONFIG" && echo "📋 Using custom rules: $CONFIG"
[ -z "$CONFIG" ] && echo "📋 Using built-in rules (no custom config found)"
echo ""

find "$NIUMINATION" -name ".git" -type d -maxdepth 4 | while read -r gitdir; do
  repo=$(dirname "$gitdir")
  scanned=$((scanned + 1))
  relpath="${repo#$NIUMINATION/}"
  [ -z "$relpath" ] && relpath="(root)"
  
  result=$(gitleaks detect --source="$repo" $CONFIG_FLAG --no-git --report-path "$REPORT_DIR/gitleaks-$(basename $repo).json" 2>&1)
  
  if echo "$result" | grep -qi "leaks found"; then
    echo "  ⚠️ $relpath: LEAKS FOUND"
    issues=$((issues + 1))
  elif echo "$result" | grep -qi "error\|no config"; then
    echo "  ⚠️ $relpath: scan error (check logs)"
    issues=$((issues + 1))
  else
    echo "  ✅ $relpath: clean"
  fi
done

echo ""
echo "📊 Summary: $scanned repos scanned, $issues with issues"
[ "$issues" -gt 0 ] && echo "⚠️ Review reports in $REPORT_DIR/"
echo "✅ Gitleaks scan complete"
