@echo off
echo ========================================
echo   Git Upload to GitHub
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git is installed!
echo.

REM Check if screenshot exists
if not exist "screenshot.png" (
    echo WARNING: screenshot.png not found!
    echo Please save your screenshot as "screenshot.png" in this folder first.
    echo.
    pause
    exit /b 1
)

echo Found screenshot.png
echo.

REM Initialize git if not already initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git remote add origin https://github.com/deba75/Concurrent-File-Server-with-Multi-Threading-Web-Interface.git
) else (
    echo Git repository already initialized
)

echo.
echo ========================================
echo   Adding files to Git...
echo ========================================
git add .

echo.
echo ========================================
echo   Committing changes...
echo ========================================
git commit -m "Initial commit: Multi-threaded Concurrent File Server with Web Interface"

echo.
echo ========================================
echo   Pushing to GitHub...
echo ========================================
git branch -M main
git push -u origin main

echo.
echo ========================================
echo   Upload Complete!
echo ========================================
echo.
echo Visit: https://github.com/deba75/Concurrent-File-Server-with-Multi-Threading-Web-Interface
echo.
pause
