#!/bin/bash

echo "========================================"
echo "  File Server - macOS"
echo "========================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "Starting File Server on port 9999..."
echo "Press Ctrl+C to stop"
echo ""

python3 file_server.py
