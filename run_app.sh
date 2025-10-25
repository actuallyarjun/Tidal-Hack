#!/bin/bash

echo "========================================"
echo "Vision Navigation Assistant"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if dependencies are installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check if YOLO model exists
if [ ! -f "src/cv_engine/models/yolov8n.pt" ]; then
    echo "Downloading YOLO model..."
    python scripts/download_models.py
    echo ""
fi

# Run the application
echo "Starting Vision Navigation Assistant..."
echo ""
echo "The application will open in your browser."
echo "Press Ctrl+C to stop the server."
echo ""
streamlit run src/ui/app.py

