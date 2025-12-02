@echo off
echo ========================================
echo   Concurrent File Server - Startup
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
echo   Starting File Server...
echo ========================================
echo.
echo Server will start on localhost:9999
echo Press Ctrl+C to stop the server
echo.

python file_server.py

pause
