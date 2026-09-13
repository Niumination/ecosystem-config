#!/bin/bash
# Wait for network/DNS before starting a network-dependent service.
# Usage: this script is the LaunchAgent Program; put the real service command
# in WAITER_TARGET_CMD or WAITER_TARGET_PLIST.

set -euo pipefail

MAX_WAIT="${MAX_WAIT:-120}"
SLEEP_SECONDS="${SLEEP_SECONDS:-2}"

check_network() {
  # Require both basic IP connectivity and DNS resolution.
  if ping -q -t 1 -c 1 8.8.8.8 >/dev/null 2>&1 \
     && ping -q -t 1 -c 1 1.1.1.1 >/dev/null 2>&1 \
     && getent hosts api.telegram.org >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

elapsed=0
while [ "$elapsed" -lt "$MAX_WAIT" ]; do
  if check_network; then
    echo "[wait-for-network] network ready after ${elapsed}s"
    exit 0
  fi
  sleep "$SLEEP_SECONDS"
  elapsed=$((elapsed + SLEEP_SECONDS))
done

echo "[wait-for-network] timeout after ${MAX_WAIT}s; continuing anyway" >&2
exit 0
