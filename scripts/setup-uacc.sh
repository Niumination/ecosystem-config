#!/bin/bash
# UACC MCP setup for Hermes Agent
# Jalankan: bash scripts/setup-uacc.sh

HERMES="/Users/zaryu/.hermes-portable/venv/bin/hermes"
PYTHON="/Users/zaryu/.hermes-portable/venv/bin/python"
UACC_DIR="$HOME/Desktop/Niumination/services/uacc"

echo "=== UACC MCP Setup for Hermes Agent ==="

# [NOTE 28 Jul 2026] Metode hermes mcp add timeout di mesin ini.
# Berhasil via manual edit ~/.hermes/config.yaml:
#   mcp_servers:
#     uacc:
#       command: "/Users/zaryu/.hermes-portable/venv/bin/python"
#       args: ["-m", "uacc.mcp"]

# 1. Add MCP server
echo "[1/3] Adding UACC MCP server to Hermes..."
$HERMES mcp add uacc --command "$PYTHON" --args -m uacc.mcp --connect-timeout 10

# 2. Restart MCP
echo "[2/3] Restarting MCP..."
$HERMES mcp restart

# 3. Verify
echo "[3/3] Verification..."
$HERMES mcp list

echo ""
echo "=== Done! UACC is ready. ==="
echo "Test with: hermes -z \"List my windows using uacc\""
