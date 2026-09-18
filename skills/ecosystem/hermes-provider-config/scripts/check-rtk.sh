#!/usr/bin/env bash
set -euo pipefail

printf 'RTK binary: '; if command -v rtk >/dev/null 2>&1; then
  rtk --version
else
  echo 'MISSING'
  exit 1
fi

printf 'Rewrite probe: '; probe=$((echo 'echo halo') | rtk rewrite 2>&1 || true)
if printf '%s' "$probe" | grep -qi 'No hook installed'; then
  echo 'NOT INITIALIZED — run: rtk init -g'
  exit 2
fi

printf 'Hermes plugin: '
if [ -d "${HERMES_HOME:-$HOME/.hermes}/plugins/rtk-rewrite" ]; then
  echo 'PRESENT'
else
  echo 'MISSING'
  exit 3
fi

echo 'OK: RTK active (Hermes internal)'