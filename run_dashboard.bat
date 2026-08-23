@echo off
REM Social Media Engine - Windows Dashboard Launcher
REM Just double-click this file to start the dashboard!

echo.
echo ========================================
echo   Social Media Engine - Dashboard
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Checking Python installation...
python --version

REM Install requirements
echo.
echo Installing dependencies (Flask, etc)...
python -m pip install -q flask flask-cors

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies ready!

REM Start the dashboard
echo.
echo ========================================
echo Starting Dashboard...
echo ========================================
echo.
echo Open your browser and go to:
echo   http://localhost:5000
echo.
echo To stop: Close this window
echo ========================================
echo.

python src/dashboard/app.py

pause
