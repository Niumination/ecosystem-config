#!/usr/bin/env bash
# Segel file beku (chmod a-w) agar model lemah tidak "iseng merapikan" konstitusi.
set -euo pipefail
NIU="${NIU:-/Users/zaryu/Desktop/Niumination}"
CORE="${NIU_CORE:-$NIU/core}"

files=(
  "$CORE/CONSTITUTION.md"
  "$CORE/VISION.md"
  "$CORE/SCOPE.md"
  "$CORE/MODEL.policy.yaml"
  "$CORE/FREEZE.list"
  "$CORE/AGENTS.slim.md"
)
if [[ -f "$HOME/.hermes/SOUL.md" ]]; then
  files+=("$HOME/.hermes/SOUL.md")
fi

for f in "${files[@]}"; do
  if [[ -f "$f" ]]; then
    chmod a-w "$f" || true
    echo "sealed $f"
  else
    echo "skip (missing) $f"
  fi
done
echo "untuk mengedit sebagai manusia: chmod u+w <file> && \$EDITOR <file> && chmod a-w <file>"
