#!/bin/bash
# Start Gillian-EMRY Hybrid Server

cd "$(dirname "$0")/gillian_server"

echo ""
echo "Starting Gillian server..."
echo "Press Ctrl+C to stop"
echo ""

python3 gillian_server.py
