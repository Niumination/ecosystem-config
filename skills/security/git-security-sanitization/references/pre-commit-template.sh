#!/usr/bin/env bash
set -euo pipefail
echo "[pre-commit] typecheck ..."
rm -rf .next
npx tsc --noEmit >/tmp/tsc-$$.log 2>&1 || { echo "[typecheck] FAIL:"; cat /tmp/tsc_$$.log; rm -f /tmp/tsc_$$.log; exit 1; }
echo "[typecheck] OK"
rm -f /tmp/tsc_$$.log
echo "[pre-commit] PII gate ..."
bash scripts/pii-gate.sh .
