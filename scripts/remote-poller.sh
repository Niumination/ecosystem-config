#!/bin/sh
# remote-poller.sh — Check remote repo status for Niumination ecosystem
# Cron: setiap 6 jam (no_agent=true, deliver=telegram)
# Only reports when changes detected (silent if all clean)

LOCKDIR="/tmp/remote-poller.lock"
mkdir "$LOCKDIR" 2>/dev/null || { echo "❌ Lock exists"; exit 1; }
trap "rmdir '$LOCKDIR' 2>/dev/null" EXIT

NIUMINATION="/Users/zaryu/Desktop/Niumination"
HAS_CHANGES=0

# Repositori dengan remote GitHub — fetch dengan timeout 10s
for repo_dir in "$NIUMINATION"/apps/kune-ya.com "$NIUMINATION"/\
  "$NIUMINATION"/apps/niu-vermilion "$NIUMINATION"/apps/PemdiAcehTengah "$NIUMINATION"/apps/Niu-LKH \
  "$NIUMINATION"/apps/niu-dash "$NIUMINATION"/desktop/flame-ade "$NIUMINATION"/brain \
  "$NIUMINATION"/desktop/x-downloader "$NIUMINATION"/agents/Ultra; do

  [ -d "$repo_dir/.git" ] || continue
  cd "$repo_dir" 2>/dev/null || continue
  repo_name=$(basename "$repo_dir")

  # Skip repos without remote
  git remote get-url origin >/dev/null 2>&1 || continue

  # Fetch dengan timeout 10s
  timeout 10 git fetch origin --quiet 2>/dev/null
  fetch_exit=$?
  
  if [ "$fetch_exit" -eq 124 ]; then
    echo "⚠️ $repo_name: remote fetch timed out (skipped)"
    HAS_CHANGES=1
    continue
  fi

  current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  ahead=$(git rev-list --count "@{upstream}..HEAD" 2>/dev/null || echo 0)
  behind=$(git rev-list --count "HEAD..@{upstream}" 2>/dev/null || echo 0)

  if [ "$behind" -gt 0 ]; then
    echo "⚠️ $repo_name ($current_branch): $behind commit(s) BEHIND remote → pull needed"
    HAS_CHANGES=1
  fi
  if [ "$ahead" -gt 0 ]; then
    echo "ℹ️ $repo_name ($current_branch): $ahead commit(s) AHEAD of remote → push needed"
    HAS_CHANGES=1
  fi
done

[ "$HAS_CHANGES" -eq 0 ] && exit 0  # Silent when all clean - no delivery
