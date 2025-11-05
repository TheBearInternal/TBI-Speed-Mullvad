@echo off
REM TBI Speed for Mullvad - Setup Script for Windows
REM Created by TheBearInternal

echo ============================================
echo TBI Speed for Mullvad - Setup
echo ============================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python is installed
echo.

echo Checking Mullvad VPN installation...
mullvad version
if errorlevel 1 (
    echo [ERROR] Mullvad VPN CLI is not installed or not in PATH
    echo Please install Mullvad VPN from https://mullvad.net/download
    pause
    exit /b 1
)
echo [OK] Mullvad VPN is installed
echo.

echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install speedtest-cli
if errorlevel 1 (
    echo [ERROR] Failed to install speedtest-cli
    pause
    exit /b 1
)
echo [OK] speedtest-cli installed successfully
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo You can now run: tbi_speed.bat
echo.
pause
