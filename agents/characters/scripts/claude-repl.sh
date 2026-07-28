#!/bin/bash
# claude-repl.sh — REPL untuk claude-code
# Bekerja dengan herdr agent send: kirim prompt, akhiri dengan ---PROCESS---
# Contoh:
#   herdr agent send penjaga "Check service status"
#   herdr agent send penjaga "---PROCESS---"

set -e

echo "🛡️ CLAUDE READY — Claude Sonnet" >&2

while true; do
  buf=""
  while IFS= read -r line; do
    if [ "$line" = "---PROCESS---" ]; then
      break
    fi
    buf="${buf}${line}"$'\n'
  done
  
  if [ -n "$buf" ]; then
    buf="${buf%$'\n'}"
    
    # Panggil claude dengan print mode
    claude -p "$buf" --print --dangerously-skip-permissions 2>&1 || true
    echo ""
    echo "=== END ==="
  fi
done
