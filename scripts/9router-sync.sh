#!/bin/bash
# 9router-sync.sh — Hybrid watcher: polling + DB WatchPaths
# Fetches http://localhost:20128/v1/models, hashes sorted IDs,
# compares with ~/.cache/niumination/9router.hash, updates cache & notifies.
set -u
MODELS_URL="http://127.0.0.1:20128/v1"
CACHE_DIR="$HOME/.cache/niumination"
CACHE_FILE="$CACHE_DIR/9router-models.json"
HASH_FILE="$CACHE_DIR/9router-models.hash"
STATE_FILE="$HOME/Desktop/Niumination/.9router-state.json"
LOG_FILE="$CACHE_DIR/9router-sync.log"

mkdir -p "$CACHE_DIR"

# Fetch models (no auth needed; 9router allows without for /v1/models)
MODELS_JSON=$(curl -s -m 10 "$MODELS_URL/v1/models" 2>/dev/null)
if [ -z "$MODELS_JSON" ] || ! echo "$MODELS_JSON" | python3 -c "import sys,json; json.load(sys.stdin)" >/dev/null 2>&1; then
  echo "$(date -Iseconds) fetch failed" >> "$LOG_FILE"
  exit 0
fi

# Sorted model IDs + hash
IDS=$(echo "$MODELS_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print('\n'.join(sorted(m['id'] for m in d.get('data',[]))))")
COUNT=$(echo "$IDS" | grep -c . || true)
HASH=$(echo "$IDS" | sha256sum 2>/dev/null | cut -d' ' -f1 || shasum -a 256 <<< "$IDS" | cut -d' ' -f1)

PREV_HASH=""
[ -f "$HASH_FILE" ] && PREV_HASH=$(cat "$HASH_FILE" 2>/dev/null | tr -d ' \n')

if [ "$HASH" = "$PREV_HASH" ]; then
  exit 0
fi

# First run or change detected
echo "$HASH" > "$HASH_FILE"
echo "$MODELS_JSON" | python3 -m json.tool > "$CACHE_FILE" 2>/dev/null || echo "$MODELS_JSON" > "$CACHE_FILE"

# Also dump providerConnections summary for state
CONNS=$(sqlite3 ~/.9router/db/data.sqlite "SELECT provider||'/'||name||'('||CASE WHEN isActive=1 THEN 'on' ELSE 'off' END||')' FROM providerConnections;" 2>/dev/null | tr '\n' ',' | sed 's/,$//')

python3 <<PYEOF 2>/dev/null >> "$LOG_FILE"
import json, pathlib, datetime
state = {
  "updated_at": datetime.datetime.now().isoformat(),
  "hash": "$HASH",
  "model_count": $COUNT,
  "providers": "$CONNS".split(",") if "$CONNS" else [],
  "models": """$(echo "$IDS" | python3 -c "import sys,json; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))" 2>/dev/null | head -c 4000)"""
}
pathlib.Path("$STATE_FILE").write_text(json.dumps(state, indent=2))
print(f"{state['updated_at']} sync: {state['model_count']} models hash {state['hash'][:8]}")
PYEOF

echo "$(date -Iseconds) change: $COUNT models hash ${HASH:0:8} -> updated" >> "$LOG_FILE"
# macOS notification (silent if not available)
if command -v osascript >/dev/null 2>&1; then
  osascript -e "display notification \"$COUNT models (hash ${HASH:0:8})\" with title \"9router sync\" subtitle \"Model list changed\"" 2>/dev/null || true
fi
exit 0
