@echo off
REM TBI Speed for Mullvad - Windows Launcher
REM Created by TheBearInternal

echo Starting TBI Speed for Mullvad...
echo.

REM Run the Python script
python tbi_speed.py

REM Check if Python script failed
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to run the speed test.
    echo Make sure Python and Mullvad VPN are installed.
    echo.
    pause
    exit /b 1
)

echo.
pause
