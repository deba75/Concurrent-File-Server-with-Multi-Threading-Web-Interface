@echo off
echo ========================================
echo   Concurrent File Server - Full Stack
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
echo   Starting Both Servers...
echo ========================================
echo.

REM Start file server in a new window
echo Starting File Server on localhost:9999...
start "File Server" cmd /k "python file_server.py"

REM Wait a moment for the server to start
timeout /t 3 >nul

REM Start web interface in a new window
echo Starting Web Interface on http://localhost:5000...
start "Web Interface" cmd /k "python web_interface.py"

REM Wait a moment for the web server to start
timeout /t 3 >nul

REM Open web browser
echo Opening web browser...
start http://localhost:5000

echo.
echo ========================================
echo   Both servers are now running!
echo ========================================
echo.
echo File Server:     localhost:9999
echo Web Interface:   http://localhost:5000
echo.
echo Close the server windows to stop the application.
echo.
pause
