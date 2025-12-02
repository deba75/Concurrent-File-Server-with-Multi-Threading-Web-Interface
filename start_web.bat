@echo off
echo ========================================
echo   Concurrent File Server - Web UI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Dependencies OK!
echo.
echo ========================================
echo   Starting Web Interface...
echo ========================================
echo.
echo Web interface will start on http://localhost:5000
echo.
echo IMPORTANT: Make sure the file server is running first!
echo           (Run start_server.bat in another window)
echo.
echo Press Ctrl+C to stop the web interface
echo.

timeout /t 2 >nul
python web_interface.py

pause
