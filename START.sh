#!/bin/bash
# ============================================================================
# GILLIAN AI - PRODUCTION START SCRIPT
# ============================================================================

cd "$(dirname "$0")"

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║              Starting Gillian AI Production Server...             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if already running
if lsof -Pi :8770 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Server already running on port 8770"
    echo ""
    echo "To stop: ./STOP.sh"
    echo "Or visit: http://localhost:8770"
    echo ""
    exit 0
fi

# Start server
cd gillian_server
python3 gillian_advanced.py
