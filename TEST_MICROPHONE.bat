@echo off
cls
echo ========================================
echo      MICROPHONE TEST
echo ========================================
echo.
echo This will test if your microphone works
echo before running the full app.
echo.
echo When prompted, say something LOUD and CLEAR
echo Example: "What do you see?"
echo.
pause
echo.

set PYTHON_PATH=C:\Users\asvat\AppData\Local\Programs\Python\Python313\python.exe

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Running microphone test...
echo.

%PYTHON_PATH% test_microphone.py

echo.
echo ========================================
echo      TEST COMPLETE
echo ========================================
echo.
echo If all tests passed: Your mic works!
echo If any failed: Check the error messages
echo.
pause

