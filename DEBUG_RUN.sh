#!/bin/bash

clear
echo "============================================================"
echo "DEBUG MODE - Vision Navigation Assistant"
echo "============================================================"
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

echo "[1] Killing any existing Streamlit processes..."
lsof -ti:8501 | xargs kill -9 2>/dev/null
echo "Port 8501 cleared!"
echo ""

echo "[2] Testing imports..."
echo ""
$PYTHON_PATH test_imports.py
echo ""

echo "============================================================"
echo "[3] Starting Streamlit app..."
echo "============================================================"
echo "Look for [OK] WebRTC messages in the output below"
echo ""
echo "Opening browser at http://localhost:8501"
echo ""

# Open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "http://localhost:8501" &
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "http://localhost:8501" &
fi

$PYTHON_PATH -m streamlit run src/ui/app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

echo ""
echo "Press any key to exit..."
read -n 1

