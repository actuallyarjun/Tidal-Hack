@echo off
cls
echo ============================================================
echo DEBUG MODE - Vision Navigation Assistant
echo ============================================================
echo.

set PYTHON_PATH=C:\Users\asvat\AppData\Local\Programs\Python\Python313\python.exe

echo [1] Killing any existing Streamlit processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501') do (
    echo Killing process %%a on port 8501...
    taskkill /F /PID %%a >nul 2>&1
)
echo Port 8501 cleared!
echo.

echo [2] Testing imports...
echo.
%PYTHON_PATH% test_imports.py
echo.

echo ============================================================
echo [3] Starting Streamlit app...
echo ============================================================
echo Look for [OK] WebRTC messages in the output below
echo.
echo Opening browser at http://localhost:8501
echo.

start "" "http://localhost:8501"
%PYTHON_PATH% -m streamlit run src\ui\app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

pause

