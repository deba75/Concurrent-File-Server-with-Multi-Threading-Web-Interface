#!/bin/bash

echo "========================================"
echo "  Concurrent File Server - macOS"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install from: https://www.python.org/downloads/mac-osx/"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Dependencies OK!"
echo ""
echo "========================================"
echo "  Starting Servers..."
echo "========================================"
echo ""

# Start file server in background
echo "Starting File Server on port 9999..."
python3 file_server.py &
SERVER_PID=$!
echo "File Server PID: $SERVER_PID"
echo ""

# Wait a moment for server to start
sleep 2

# Start web interface
echo "Starting Web Interface on port 5000..."
echo ""
echo "========================================"
echo "  Servers Running!"
echo "========================================"
echo ""
echo "Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Start web interface (will run in foreground)
python3 web_interface.py

# When web interface stops, kill the file server
kill $SERVER_PID 2>/dev/null
echo ""
echo "Servers stopped."
