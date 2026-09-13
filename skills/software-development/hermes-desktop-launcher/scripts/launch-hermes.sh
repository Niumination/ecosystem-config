#!/bin/bash
# Hermes Desktop Launcher Script
# Opens Hermes.app from /Applications

set -e

APP_PATH="/Applications/Hermes.app"

# Check if Hermes.app exists
if [ ! -d "$APP_PATH" ]; then
    echo "❌ Hermes.app not found at $APP_PATH"
    echo ""
    echo "Install options:"
    echo "  1. Copy from source: sudo cp -R ~/src/hermes-agent/apps/desktop/release/mac/Hermes.app /Applications/"
    echo "  2. Build from source: cd ~/src/hermes-agent && npm run install:desktop && cd apps/desktop && npm run dist:mac"
    echo "  3. Download installer: https://hermes-agent.nousresearch.com/desktop"
    exit 1
fi

# Launch the app
echo "🚀 Opening Hermes Desktop..."
open "$APP_PATH"

# Wait and verify process started
sleep 2
if pgrep -f "Hermes.app" > /dev/null; then
    echo "✅ Hermes Desktop is running!"
    echo ""
    echo "Process info:"
    pgrep -f "Hermes.app" | head -3 | xargs -I {} ps -p {} -o pid,ppid,%cpu,%mem,command
else
    echo "⚠️  App may still be starting up. Check manually if needed."
fi
