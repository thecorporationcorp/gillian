#!/bin/bash
# ============================================================================
# GILLIAN AI - STOP SCRIPT
# ============================================================================

echo "Stopping Gillian AI server..."

# Find and kill process on port 8770
PID=$(lsof -ti:8770)

if [ -z "$PID" ]; then
    echo "✅ No server running"
else
    kill -9 $PID
    echo "✅ Server stopped (PID: $PID)"
fi
