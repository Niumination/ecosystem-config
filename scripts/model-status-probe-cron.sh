#!/bin/bash
# Wrapper script for model status probe cron job
# Runs the probe + report generator and outputs the report
# Designed for no_agent cron (no LLM needed)
# FIX: Now properly surfaces probe failures instead of masking them

set -a
source ~/.hermes/.env 2>/dev/null
set +a

# Run probe (real model calls)
PROBE_OUTPUT=$(python3 ~/Desktop/Niumination/scripts/model_status_checker.py 2>&1)
echo "$PROBE_OUTPUT"

# Check if probe found failures
if echo "$PROBE_OUTPUT" | grep -q "Critical Failed: [1-9]"; then
    echo ""
    echo "⚠️ ALERT: Model probe detected failures. Do NOT trust OK status from this job."
    exit 1
fi

# Generate short report (only if no failures)
python3 ~/Desktop/Niumination/scripts/model_status_report.py 2>&1
