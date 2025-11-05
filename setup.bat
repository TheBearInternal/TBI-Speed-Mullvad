@echo off
title TBI Speed for Mullvad - Setup

echo ==================================
echo   TBI Speed for Mullvad - Setup
echo   by TheBearInternal
echo ==================================
echo.

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not installed
    echo.
    echo Please install Python 3 from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)
python --version
echo.

echo [2/3] Checking Mullvad...
mullvad version >nul 2>&1
if errorlevel 1 (
    echo X Mullvad CLI not found
    echo.
    echo Please install from:
    echo https://mullvad.net/download
    pause
    exit /b 1
)
mullvad version
echo.

echo [3/3] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install speedtest-cli
echo.

echo ==================================
echo   Setup Complete!
echo ==================================
echo.
echo Run TBI Speed for Mullvad:
echo   tbi_speed.bat
echo.
pause
