#!/bin/bash

echo "=================================="
echo "  TBI Speed for Mullvad - Setup"
echo "  by TheBearInternal"
echo "=================================="
echo ""

OS_TYPE=$(uname -s 2>/dev/null || echo "Windows")
PYTHON_CMD=""

if [[ "$OS_TYPE" == "Darwin" ]]; then
    OS="macOS"
elif [[ "$OS_TYPE" == "Linux" ]]; then
    OS="Linux"
else
    OS="Windows"
fi

echo "Detected OS: $OS"
echo ""

echo "[1/3] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✓ Python3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✓ Python found: $(python --version)"
else
    echo "✗ Python not installed"
    echo ""
    echo "Please install Python 3 from:"
    echo "https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "[2/3] Checking Mullvad..."
if command -v mullvad &> /dev/null; then
    echo "✓ Mullvad CLI found: $(mullvad version 2>&1 | head -n1)"
else
    echo "✗ Mullvad not found"
    echo ""
    echo "Please install from:"
    echo "https://mullvad.net/download"
    exit 1
fi

echo ""
echo "[3/3] Installing dependencies..."
$PYTHON_CMD -m pip install speedtest-cli 2>/dev/null || pip install speedtest-cli 2>/dev/null || pip3 install speedtest-cli

chmod +x tbi_speed.sh 2>/dev/null

echo ""
echo "=================================="
echo "  Setup Complete!"
echo "=================================="
echo ""
echo "Run TBI Speed for Mullvad:"
echo "  ./tbi_speed.sh"
echo ""
echo "Or directly:"
echo "  $PYTHON_CMD tbi_speed.py"
echo ""
