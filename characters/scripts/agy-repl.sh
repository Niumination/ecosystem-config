#!/bin/bash
# agy-repl.sh — REPL untuk agy (antigravity-cli)
# Bekerja dengan herdr agent send: kirim prompt, akhiri dengan ---PROCESS---
# Contoh:
#   herdr agent send arsitek "Analyze this"
#   herdr agent send arsitek "---PROCESS---"

set -e
MODEL="${1:-}"

if [ -n "$MODEL" ]; then
  MODEL_ARG="--model $MODEL"
else
  MODEL_ARG=""
fi

echo "🧠 AGY READY — Claude Opus 4.6" >&2

while true; do
  buf=""
  while IFS= read -r line; do
    if [ "$line" = "---PROCESS---" ]; then
      break
    fi
    buf="${buf}${line}"$'\n'
  done
  
  if [ -n "$buf" ]; then
    # Hapus trailing newline
    buf="${buf%$'\n'}"
    
    # Panggil agy dengan print mode
    # shellcheck disable=SC2086
    agy $MODEL_ARG --dangerously-skip-permissions --print "$buf" 2>&1 || true
    echo ""
    echo "=== END ==="
  fi
done
