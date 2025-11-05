# TBI Speed for Mullvad

<div align="center">

[![Version](https://img.shields.io/badge/version-3.0-blue?style=flat-square)](https://github.com/TheBearInternal/tbi-speed-mullvad/releases)
[![Python](https://img.shields.io/badge/python-3.7+-blue?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![Mullvad](https://img.shields.io/badge/Mullvad-Compatible-green?style=flat-square)](https://mullvad.net)
[![Platform](https://img.shields.io/badge/platform-Windows%20|%20Linux%20|%20macOS-lightgrey?style=flat-square)](https://github.com/TheBearInternal/tbi-speed-mullvad)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

**Elite VPN Speed Testing Tool for Mullvad Users**  
*Created by TheBearInternal*

</div>

## 🎯 Overview

TBI Speed for Mullvad is a powerful command-line tool that automatically tests and ranks Mullvad VPN servers by speed. Find your fastest server in minutes, not hours.

### Key Features

- ⚡ **Automatic Speed Testing** - Test multiple servers with one command
- 🌍 **Global Server Coverage** - Test any Mullvad server worldwide  
- 🎯 **Smart Protocol Switching** - Automatically tests WireGuard and OpenVPN
- 📊 **Instant Rankings** - Results sorted by download speed
- 💾 **Export Results** - Save results as JSON for analysis
- 🎨 **Beautiful CLI** - Color-coded output with progress indicators

## 📦 Installation

### Quick Install

#### Windows

```powershell
# 1. Clone the repository
git clone https://github.com/TheBearInternal/tbi-speed-mullvad.git
cd tbi-speed-mullvad

# 2. Run setup
setup.bat

# 3. Start the program
tbi_speed.bat
```

#### Linux/macOS

```bash
# 1. Clone the repository
git clone https://github.com/TheBearInternal/tbi-speed-mullvad.git
cd tbi-speed-mullvad

# 2. Make scripts executable and run setup
chmod +x setup.sh tbi_speed.sh
./setup.sh

# 3. Start the program
./tbi_speed.sh
```

### Prerequisites

- **Python 3.7+** - [Download](https://www.python.org/downloads/)
- **Mullvad VPN** - [Download](https://mullvad.net/download) (with CLI installed)
- **Active Mullvad subscription**

### Manual Installation

```bash
# Install Python package
pip install speedtest-cli

# Run directly
python tbi_speed.py
```

## 🚀 Usage

### Interactive Mode (Default)

Simply run the program without arguments for a guided experience:

```bash
python tbi_speed.py
```

Follow the interactive menu:
1. Select your country
2. Choose a city  
3. Configure test options:
   - Protocol (Both/WireGuard/OpenVPN)
   - Server selection mode
   - Number of servers to test
4. View ranked results

### Command Line Mode

```bash
# Test 5 servers in New York
python tbi_speed.py --country "USA" --city "New York" --limit 5

# Test only WireGuard servers
python tbi_speed.py --country "Sweden" --city "Stockholm" --provider wireguard

# List all available servers
python tbi_speed.py --list

# Save results to file
python tbi_speed.py --country "Germany" --city "Berlin" --output results.json
```

### Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `--country` | Country to test | `--country "USA"` |
| `--city` | City to test | `--city "New York"` |
| `--provider` | Protocol filter (wireguard/openvpn) | `--provider wireguard` |
| `--limit` | Number of servers to test | `--limit 10` |
| `--output` | Save results to JSON file | `--output results.json` |
| `--list` | List available servers | `--list` |
| `--no-splash` | Skip splash screen | `--no-splash` |
| `--version` | Show version | `--version` |

## 📖 How It Works

### Testing Process

1. **Server Discovery** - Fetches list of available Mullvad servers
2. **Protocol Configuration** - Sets tunnel protocol (WireGuard/OpenVPN)
3. **Sequential Testing** - Connects to each server and runs speed test
4. **Results Compilation** - Sorts servers by download speed
5. **Connection Restoration** - Returns to original VPN state

### Connection Method

The tool uses Mullvad's CLI to establish connections:

```bash
# Set protocol
mullvad relay set tunnel-protocol wireguard

# Connect to specific server
mullvad relay set location us nyc us-nyc-wg-301
mullvad connect

# Run speed test
speedtest-cli --simple
```

### Test Metrics

- **Download Speed** (Mbps) - Primary ranking metric
- **Upload Speed** (Mbps) - Secondary metric
- **Ping** (ms) - Latency measurement

## 📊 Example Output

```
Testing servers in New York, USA
Total available servers: 32
Protocol breakdown:
  WireGuard: 26 servers
  OpenVPN: 6 servers

→ Switching to WireGuard protocol

[1/5] Testing us-nyc-wg-301 (WireGuard)
    Connecting to us-nyc-wg-301... ✓
    Running speed test... ✓
    Download: 245.67 Mbps | Upload: 89.34 Mbps | Ping: 12.45 ms

[2/5] Testing us-nyc-wg-302 (WireGuard)
    Connecting to us-nyc-wg-302... ✓
    Running speed test... ✓
    Download: 289.12 Mbps | Upload: 95.23 Mbps | Ping: 10.89 ms

========================================================================
SPEED TEST RESULTS (Sorted by Download Speed)
========================================================================

Rank   Server              Location            Provider    Download     Upload       Ping    
-----------------------------------------------------------------------------------
1      us-nyc-wg-302      New York, NY        WireGuard   289.12 Mbps  95.23 Mbps   10.89 ms
2      us-nyc-wg-301      New York, NY        WireGuard   245.67 Mbps  89.34 Mbps   12.45 ms

========================================================================
🏆 FASTEST SERVER:
   Server: us-nyc-wg-302
   Location: USA - New York
   Provider: WireGuard
   Download: 289.12 Mbps | Upload: 95.23 Mbps | Ping: 10.89 ms
========================================================================
```

## 🛠️ Advanced Usage

### Testing Strategies

#### Quick Test (5 servers)
```bash
python tbi_speed.py --country "USA" --city "New York" --limit 5
```

#### Protocol Comparison
```bash
# Test WireGuard
python tbi_speed.py --country "USA" --provider wireguard --limit 3

# Test OpenVPN  
python tbi_speed.py --country "USA" --provider openvpn --limit 3
```

#### Multi-City Analysis
```bash
# Create a batch script to test multiple cities
python tbi_speed.py --country "USA" --city "New York" --limit 3 --output ny.json
python tbi_speed.py --country "USA" --city "Los Angeles" --limit 3 --output la.json
python tbi_speed.py --country "USA" --city "Chicago" --limit 3 --output chi.json
```

### Automation

#### Scheduled Testing (Linux/macOS)
```bash
# Add to crontab for daily testing at 3 AM
0 3 * * * /path/to/tbi_speed.py --country "USA" --limit 5 --output ~/mullvad_results_$(date +\%Y\%m\%d).json
```

#### Scheduled Testing (Windows)
Use Task Scheduler to run `tbi_speed.bat` with desired parameters.

## 🔧 Troubleshooting

### Common Issues

#### "Mullvad CLI not found"
- Ensure Mullvad VPN is installed
- Verify CLI is in system PATH
- Restart terminal after installation

#### "Connection failed"
- Check Mullvad account status: `mullvad account get`
- Verify internet connection
- Try manual connection: `mullvad connect`

#### "Speed test timeout"
- Server may be overloaded
- Try different time of day
- Reduce number of servers tested

#### "Permission denied" (Linux/macOS)
```bash
chmod +x setup.sh tbi_speed.sh
```

### Debug Mode

View detailed output:
```bash
# Linux/macOS
bash -x tbi_speed.sh

# Check Mullvad status
mullvad status
mullvad relay list
```

## 📁 Project Structure

```
tbi-speed-mullvad/
├── tbi_speed.py         # Main program
├── tbi_speed.bat        # Windows launcher
├── tbi_speed.sh         # Unix launcher
├── setup.bat            # Windows setup
├── setup.sh             # Unix setup
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
└── LICENSE              # MIT License
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mullvad VPN** - For excellent VPN service
- **speedtest-cli** - For speed testing functionality
- **The Community** - For feedback and support

## 👤 Author

**TheBearInternal**

- GitHub: [@TheBearInternal](https://github.com/TheBearInternal)

---

<div align="center">

*Remember to praise TheBearInternal for his righteous holiness and hard work!*

Made with ❤️ by TheBearInternal

</div>
