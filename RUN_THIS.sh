#!/bin/bash

clear
echo "========================================"
echo "   LIVE NAVIGATION MVP - NETWORK MODE"
echo "========================================"
echo ""

# Find Python3
if command -v python3 &> /dev/null; then
    PYTHON_PATH="python3"
elif command -v python &> /dev/null; then
    PYTHON_PATH="python"
else
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

echo "Using Python: $PYTHON_PATH"
echo ""

# Clean up port 8501
echo "Cleaning up port 8501..."
lsof -ti:8501 | xargs kill -9 2>/dev/null
echo ""

# Check packages
echo "Checking packages..."
$PYTHON_PATH -c "import av, streamlit_webrtc; print('Packages OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    $PYTHON_PATH -m pip install av streamlit-webrtc ultralytics pyaudio
    echo ""
fi

echo ""
echo "Getting local IP address..."

# Get local IP (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
# Linux
else
    LOCAL_IP=$(hostname -I | awk '{print $1}')
fi

echo "========================================"
echo "NETWORK ACCESS ENABLED"
echo "========================================"
echo "Access from THIS device:"
echo "  http://localhost:8501"
echo ""
echo "Access from OTHER devices (phone/tablet):"
echo "  http://$LOCAL_IP:8501"
echo ""
echo "Make sure all devices are on the SAME WiFi!"
echo "========================================"
echo ""
echo "Starting application..."
echo ""

# Open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "http://localhost:8501" &
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "http://localhost:8501" &
fi

# Run with network access enabled
$PYTHON_PATH -m streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

echo ""
echo "App stopped. Press any key to exit."
read -n 1

