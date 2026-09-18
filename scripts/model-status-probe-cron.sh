#!/bin/bash
# Wrapper script for model status probe cron job
# Runs the probe + report generator and outputs the report
# Designed for no_agent cron (no LLM needed)

set -a
source ~/.hermes/.env 2>/dev/null
set +a

# Run probe
python3 ~/Desktop/Niumination/scripts/model_status_checker.py 2>&1

# Generate short report
python3 ~/Desktop/Niumination/scripts/model_status_report.py 2>&1
