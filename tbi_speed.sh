#!/bin/bash
# TBI Speed for Mullvad - Unix Launcher
# Created by TheBearInternal

echo "Starting TBI Speed for Mullvad..."
echo

# Run the Python script
python3 tbi_speed.py

# Check exit code
if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Failed to run the speed test."
    echo "Make sure Python 3 and Mullvad VPN are installed."
    echo
    exit 1
fi

echo
read -p "Press Enter to exit..."
