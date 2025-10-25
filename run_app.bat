@echo off
echo ========================================
echo Vision Navigation Assistant
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check if YOLO model exists
if not exist "src\cv_engine\models\yolov8n.pt" (
    echo Downloading YOLO model...
    python scripts\download_models.py
    echo.
)

REM Run the application
echo Starting Vision Navigation Assistant...
echo.
echo The application will open in your browser.
echo Press Ctrl+C to stop the server.
echo.
streamlit run src\ui\app.py

pause

