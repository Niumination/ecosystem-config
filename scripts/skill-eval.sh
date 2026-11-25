#!/bin/bash
# Local skill-eval gate wrapper (plugin-eval, MIT — see scripts/plugin-eval/ATTRIBUTION.md)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec node "$ROOT/scripts/plugin-eval/scripts/plugin-eval.js" "$@"
