#!/usr/bin/env bash
# Read-only deploy-state probe for a Vercel project.
#
# Answers in one shot: is Vercel itself incident-free, what state are the recent
# deployments in, what does local git say, WHICH COMMIT is actually serving the
# production domain, where the function executes, and whether public endpoints
# answer.
#
# Usage: bash deploy_state_probe.sh <project> <prod-host> [repo-dir]
#   bash deploy_state_probe.sh sapa-ai sapa-smart-ai.vercel.app \
#     ~/Desktop/Niumination/services/sapa-ai
#
# Needs: authenticated `vercel` CLI + a git repo. Makes NO model calls, so it is
# safe to run when the owner's model quota is tight.
# Trim section 6's endpoint list to the app under test.
set -u

PROJECT=${1:?usage: deploy_state_probe.sh <project> <prod-host> [repo-dir]}
HOST=${2:?usage: deploy_state_probe.sh <project> <prod-host> [repo-dir]}
DIR=${3:-$PWD}
cd "$DIR" || { echo "no such dir: $DIR"; exit 1; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "== 1. platform incidents (0 = Vercel healthy) =="
curl -s --max-time 15 -o "$TMP/incidents.json" \
  https://www.vercel-status.com/api/v2/incidents/unresolved.json
python3 -c "
import json
d = json.load(open('$TMP/incidents.json'))
inc = d.get('incidents', [])
print('  open incidents:', len(inc))
for i in inc[:3]:
    print('   -', i.get('name'), '|', i.get('status'))
" 2>/dev/null || echo "  status page unreachable"

echo "== 2. recent deployments (state + age) =="
timeout 60 vercel ls "$PROJECT" 2>&1 | sed -n '4,8p'

echo "== 3. local git =="
git log --oneline -1 --format='  HEAD %h %s' | cut -c1-95
echo "  dirty files: $(git status --short | wc -l | tr -d ' ')"

echo "== 4. commit serving the production domain (the one that matters) =="
timeout 60 vercel api "/v13/deployments/$HOST" > "$TMP/live.json" 2>/dev/null
python3 -c "
import json, datetime
try:
    d = json.load(open('$TMP/live.json'))
    m = d.get('meta') or {}
    print('  status :', d.get('readyState'), '| target:', d.get('target'),
          '| substate:', d.get('readySubstate'))
    print('  commit :', str(m.get('githubCommitSha'))[:8], '|',
          str(m.get('githubCommitMessage'))[:60])
    built = datetime.datetime.fromtimestamp(
        d.get('createdAt', 0) / 1000, datetime.timezone.utc
    ).strftime('%Y-%m-%d %H:%M UTC')
    print('  built  :', built)
except Exception as e:
    print('  unreadable:', e)
"

echo "== 5. where the function executes (second value) =="
curl -sI --max-time 20 "https://$HOST/api/status" | grep -i 'x-vercel-id' \
  || echo "  no x-vercel-id header"

echo "== 6. public endpoints (code + seconds) =="
for p in / /dashboard /api/kpi /api/stats /api/sapa /api/status; do
  printf '  %-16s %s\n' "$p" \
    "$(curl -s -o /dev/null -w '%{http_code} %{time_total}s' --max-time 30 "https://$HOST$p")"
done

echo
echo "Reminder: Ready + minutes old is NOT proof the fix shipped — compare"
echo "section 4's commit against section 3's HEAD."
