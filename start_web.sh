#!/bin/bash

echo "========================================"
echo "  Web Interface - macOS"
echo "========================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check dependencies
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting Web Interface on port 5000..."
echo ""
echo "IMPORTANT: Make sure file_server.py is running!"
echo "           (Run ./start_server.sh in another terminal)"
echo ""
echo "Open browser to: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python3 web_interface.py
