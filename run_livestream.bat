@echo off
echo ========================================
echo Vision Navigation Assistant
echo LIVE STREAM MODE
echo ========================================
echo.

REM Force use of the correct Python
set PYTHON_PATH=C:\Users\asvat\AppData\Local\Programs\Python\Python313\python.exe

REM Verify packages are installed
echo Checking packages...
%PYTHON_PATH% -c "import av; import streamlit_webrtc; print('Live stream packages OK')" 2>nul
if errorlevel 1 (
    echo [ERROR] Live stream packages not found!
    echo Installing now...
    %PYTHON_PATH% -m pip install streamlit-webrtc av ultralytics
    echo.
)

REM Run the application
echo.
echo ========================================
echo Starting Live Stream Application...
echo ========================================
echo.
echo The app will open in your browser.
echo Select "Live Webcam Stream" in the sidebar.
echo Click START to begin real-time detection.
echo.
echo Press Ctrl+C to stop the server.
echo.

%PYTHON_PATH% -m streamlit run src\ui\app.py

pause
