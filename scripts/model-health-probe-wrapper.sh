#!/bin/bash
# Wrapper script for model health probe
# Sources .env and runs probe, outputs JSON result

set -a
source ~/.hermes/.env 2>/dev/null
set +a

# Run probe and capture output
OUTPUT=$(python3 ~/Desktop/Niumination/scripts/model-health-probe.py 2>&1)
EXIT_CODE=$?

echo "$OUTPUT"

# Find the newest probe result
NEWEST=$(ls -t ~/.hermes/cron/output/model-probe-*.json 2>/dev/null | head -1)

if [ -n "$NEWEST" ] && [ -f "$NEWEST" ]; then
    echo ""
    echo "=== RESULTS ==="
    python3 -c "
import json
with open('$NEWEST') as f:
    data = json.load(f)

ok = data['ok']
failed = data['failed']
total = data['total']

# Sort successful by latency
results = data['results']
ok_results = [r for r in results if r['status'] == 'ok']
ok_sorted = sorted(ok_results, key=lambda x: x['latency_ms'])

# Categorize failures
failed_results = [r for r in results if r['status'] != 'ok']
capacity = len([r for r in failed_results if '503' in r['status']])
auth = len([r for r in failed_results if '401' in r['status'] or '403' in r['status']])
timeout = len([r for r in failed_results if r['latency_ms'] > 29000])
parse = len([r for r in failed_results if 'Extra data' in r.get('error', '')])
other = len(failed_results) - capacity - auth - timeout - parse

print(f'Total: {total} | OK: {ok} | Failed: {failed}')
print()
if ok_sorted:
    print('TOP 5 TERCEPAT:')
    for i, r in enumerate(ok_sorted[:5], 1):
        print(f'  {i}. {r[\"model\"]:<45} {r[\"latency_ms\"]:>6.0f}ms  {r[\"tps\"]:.0f} tps')
    print()
print(f'FAILURE BREAKDOWN:')
print(f'  503 (capacity): {capacity}')
print(f'  401/403 (auth): {auth}')
print(f'  Timeout (>30s): {timeout}')
print(f'  Parse error:    {parse}')
print(f'  Other:          {other}')
"
fi

exit $EXIT_CODE
