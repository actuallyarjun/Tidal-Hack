@echo off
cls
echo ========================================
echo    LIVE NAVIGATION MVP - NETWORK MODE
echo ========================================
echo.

REM Force use of the correct Python
set PYTHON_PATH=C:\Users\asvat\AppData\Local\Programs\Python\Python313\python.exe

echo Cleaning up port 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo Checking packages...
%PYTHON_PATH% -c "import av, streamlit_webrtc; print('Packages OK')" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    %PYTHON_PATH% -m pip install av streamlit-webrtc ultralytics
    echo.
)

echo.
echo Getting local IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found
)
:found
echo.
echo ========================================
echo NETWORK ACCESS ENABLED
echo ========================================
echo Access from THIS device:
echo   http://localhost:8501
echo.
echo Access from OTHER devices (phone/tablet):
echo   http://%IP%:8501
echo.
echo Make sure all devices are on the SAME WiFi!
echo ========================================
echo.
echo Starting application...
echo.

REM Run with network access enabled (using proper modular architecture)
start "" "http://localhost:8501"
%PYTHON_PATH% -m streamlit run src\ui\app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

pause
