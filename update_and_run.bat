@echo off
REM Social Media Engine - Update and Run Dashboard
REM This script downloads the latest code and starts the dashboard

echo.
echo ========================================
echo   Social Media Engine - Update & Run
echo ========================================
echo.

REM Get the directory where this script is located
setlocal enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

echo Downloading latest code from GitHub...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "try { ^
        $ProgressPreference = 'SilentlyContinue'; ^
        Invoke-WebRequest -Uri 'https://github.com/sevenball842/social_media_engine/archive/refs/heads/claude/social-media-engine-6zcvkb.zip' -OutFile 'update.zip'; ^
        Add-Type -AssemblyName System.IO.Compression.FileSystem; ^
        [System.IO.Compression.ZipFile]::ExtractToDirectory('update.zip', '.'); ^
        Get-ChildItem -Path 'social_media_engine-*' -Directory | ForEach-Object { ^
            Get-ChildItem -Path $_.FullName | Move-Item -Destination '.' -Force; ^
        }; ^
        Remove-Item 'social_media_engine-*' -Recurse -Force; ^
        Remove-Item 'update.zip' -Force; ^
        Write-Host 'Download and extract complete!' ^
    } catch { ^
        Write-Host 'Error downloading: ' $_.Exception.Message; ^
        exit 1; ^
    }"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to download latest code
    echo Make sure you have internet connection
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
python -m pip install -q flask flask-cors

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Dashboard...
echo ========================================
echo.
echo Open your browser and go to:
echo   http://localhost:5000
echo.
echo To stop: Press Ctrl+C
echo ========================================
echo.

python src/dashboard/app.py

pause
