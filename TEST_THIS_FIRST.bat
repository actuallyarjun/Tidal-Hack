@echo off
echo ========================================
echo TESTING LIVE STREAM
echo ========================================
echo.

REM Force use of the correct Python
set PYTHON_PATH=C:\Users\asvat\AppData\Local\Programs\Python\Python313\python.exe

echo Testing Python and packages...
%PYTHON_PATH% -c "import av; print('av version:', av.__version__)"
if errorlevel 1 (
    echo.
    echo ERROR: av package not found!
    echo Installing now...
    %PYTHON_PATH% -m pip install av streamlit-webrtc
    echo.
)

echo.
echo Starting live stream test...
echo.
%PYTHON_PATH% -m streamlit run test_livestream.py

pause
