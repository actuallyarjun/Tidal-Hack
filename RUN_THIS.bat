@echo off
cls
echo ========================================
echo    LIVE NAVIGATION MVP
echo ========================================
echo.

REM Force use of the correct Python
set PYTHON_PATH=C:\Users\asvat\AppData\Local\Programs\Python\Python313\python.exe

echo Checking packages...
%PYTHON_PATH% -c "import av, streamlit_webrtc; print('Packages OK')" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    %PYTHON_PATH% -m pip install av streamlit-webrtc ultralytics
    echo.
)

echo Starting application...
echo.
%PYTHON_PATH% -m streamlit run livestream_simple.py

pause
