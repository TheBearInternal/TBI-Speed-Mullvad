#!/bin/bash
# TBI Speed for Mullvad - Setup Script for Linux/macOS
# Created by TheBearInternal

echo "============================================"
echo "TBI Speed for Mullvad - Setup"
echo "============================================"
echo

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3 using your package manager"
    exit 1
fi
python3 --version
echo "[OK] Python is installed"
echo

echo "Checking Mullvad VPN installation..."
if ! command -v mullvad &> /dev/null; then
    echo "[ERROR] Mullvad VPN CLI is not installed"
    echo "Please install Mullvad VPN from https://mullvad.net/download"
    exit 1
fi
mullvad version
echo "[OK] Mullvad VPN is installed"
echo

echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip --user
python3 -m pip install speedtest-cli --user

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install speedtest-cli"
    exit 1
fi
echo "[OK] speedtest-cli installed successfully"
echo

echo "Making scripts executable..."
chmod +x tbi_speed.sh
chmod +x setup.sh
echo "[OK] Scripts are now executable"
echo

echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo
echo "You can now run: ./tbi_speed.sh"
echo "Or directly: python3 tbi_speed.py"
echo
