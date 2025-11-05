#!/usr/bin/env python3

import subprocess
import json
import time
import argparse
import sys
import platform
import os
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import random

SYSTEM = platform.system()
IS_WINDOWS = SYSTEM == 'Windows'
IS_MACOS = SYSTEM == 'Darwin'
IS_LINUX = SYSTEM == 'Linux'

class Colors:
    if sys.stdout.isatty() and (not IS_WINDOWS or 'ANSICON' in os.environ or 'WT_SESSION' in os.environ):
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        END = '\033[0m'
        BOLD = '\033[1m'
    else:
        HEADER = BLUE = CYAN = GREEN = YELLOW = RED = END = BOLD = ''

def show_splash_screen():
    bears = f"""
{Colors.CYAN}
    ʕ•ᴥ•ʔ    ʕ•ᴥ•ʔ    ʕ•ᴥ•ʔ    ʕ•ᴥ•ʔ    ʕ•ᴥ•ʔ
    
{Colors.YELLOW}═══════════════════════════════════════════════════════{Colors.END}
{Colors.BOLD}        TBI SPEED FOR MULLVAD v3.0
           by TheBearInternal{Colors.END}
{Colors.YELLOW}═══════════════════════════════════════════════════════{Colors.END}

{Colors.CYAN}    ʕ·ᴥ·ʔ    ʕ·ᴥ·ʔ    ʕ·ᴥ·ʔ    ʕ·ᴥ·ʔ    ʕ·ᴥ·ʔ{Colors.END}
"""
    
    print(bears)
    
    for i in range(3):
        print(f"{Colors.GREEN}{'.' * (i+1)}{Colors.END}", end='\r')
        time.sleep(0.6)
    
    print(f"{Colors.GREEN}Loading complete!{Colors.END}")
    time.sleep(0.5)
    os.system('cls' if IS_WINDOWS else 'clear')

class MullvadSpeedTester:
    def __init__(self):
        self.results = []
        self.original_server = None
        self.all_relays = []
        
    def check_requirements(self):
        print(f"{Colors.CYAN}Verifying system requirements...{Colors.END}")
        print(f"OS: {SYSTEM} {platform.version()[:30]}...")
        
        try:
            subprocess.run(['mullvad', 'version'], capture_output=True, check=True)
            print(f"{Colors.GREEN}✓ Mullvad CLI detected{Colors.END}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Colors.RED}✗ Mullvad CLI not found{Colors.END}")
            print(f"\nDownload from: https://mullvad.net/download")
            sys.exit(1)
        
        try:
            subprocess.run(['speedtest-cli', '--version'], capture_output=True, check=True)
            print(f"{Colors.GREEN}✓ Speedtest CLI ready{Colors.END}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Colors.YELLOW}Installing speedtest-cli...{Colors.END}")
            try:
                if IS_WINDOWS:
                    try:
                        subprocess.run(['pip', 'install', 'speedtest-cli'], check=True, capture_output=True)
                    except:
                        subprocess.run(['python', '-m', 'pip', 'install', 'speedtest-cli'], check=True)
                else:
                    try:
                        subprocess.run(['pip3', 'install', 'speedtest-cli'], check=True, capture_output=True)
                    except:
                        subprocess.run(['pip', 'install', 'speedtest-cli', '--user'], check=True)
                print(f"{Colors.GREEN}✓ Installation complete{Colors.END}")
            except:
                print(f"{Colors.RED}Manual installation required: pip install speedtest-cli{Colors.END}")
                sys.exit(1)
    
    def get_all_relays(self) -> List[Dict]:
        if self.all_relays:
            return self.all_relays
            
        try:
            result = subprocess.run(['mullvad', 'relay', 'list'], 
                                  capture_output=True, text=True, check=True)
            
            relays = []
            current_country = None
            current_city = None
            
            for line in result.stdout.split('\n'):
                if not line.strip():
                    continue
                
                tab_count = len(line) - len(line.lstrip('\t'))
                line_stripped = line.strip()
                
                if '(' not in line_stripped:
                    continue
                
                name = line_stripped.split('(')[0].strip()
                
                if tab_count == 0:
                    current_country = name
                    current_city = None
                elif tab_count == 1:
                    current_city = name
                elif tab_count == 2 and current_country and current_city:
                    server = {
                        'country': current_country,
                        'city': current_city,
                        'server': name,
                        'provider': 'wireguard' if 'wg' in name else 'openvpn'
                    }
                    relays.append(server)
            
            self.all_relays = relays
            return relays
            
        except subprocess.CalledProcessError:
            return []
    
    def filter_relays(self, country: str = None, city: str = None, provider: str = None) -> List[Dict]:
        relays = self.get_all_relays()
        
        if country:
            relays = [r for r in relays if country.lower() in r['country'].lower()]
        if city:
            relays = [r for r in relays if city.lower() in r['city'].lower()]
        if provider:
            relays = [r for r in relays if r['provider'] == provider.lower()]
        
        return relays
    
    def get_countries(self) -> List[str]:
        countries = []
        seen = set()
        for relay in self.all_relays:
            if relay['country'] not in seen:
                countries.append(relay['country'])
                seen.add(relay['country'])
        return sorted(countries)
    
    def get_cities(self, country: str) -> List[tuple]:
        cities = {}
        for relay in self.all_relays:
            if relay['country'] == country:
                city = relay['city']
                if city not in cities:
                    cities[city] = 0
                cities[city] += 1
        return sorted([(city, count) for city, count in cities.items()])
    
    def get_connected_server(self) -> Optional[str]:
        try:
            result = subprocess.run(['mullvad', 'status'], 
                                  capture_output=True, text=True, check=True)
            
            if 'Connected to' in result.stdout:
                parts = result.stdout.split('Connected to')
                if len(parts) > 1:
                    server_part = parts[1].strip()
                    return server_part.split()[0] if server_part else None
            
            for line in result.stdout.split('\n'):
                if 'Relay:' in line:
                    parts = line.split('Relay:')
                    if len(parts) > 1:
                        return parts[1].strip().split()[0]
            
            return None
        except:
            return None
    
    def test_servers(self, relays: List[Dict], limit: int = None, specific_servers: List[Dict] = None):
        if specific_servers:
            servers_to_test = specific_servers
        else:
            servers_to_test = relays[:limit] if limit else relays
        
        if not servers_to_test:
            print(f"{Colors.RED}No servers to test{Colors.END}")
            return
            
        total = len(servers_to_test)
        
        wg_servers = [s for s in servers_to_test if s['provider'] == 'wireguard']
        ovpn_servers = [s for s in servers_to_test if s['provider'] == 'openvpn']
        
        location = f"{servers_to_test[0]['city']}, {servers_to_test[0]['country']}"
        
        print(f"\n{Colors.BOLD}Testing servers in {location}{Colors.END}")
        print(f"Total available servers: {total}")
        print(f"Servers to test: {total}")
        
        if wg_servers and ovpn_servers:
            print(f"Protocol breakdown:")
            print(f"  WireGuard: {len(wg_servers)} servers")
            print(f"  OpenVPN: {len(ovpn_servers)} servers")
        elif wg_servers:
            print(f"Protocol breakdown:")
            print(f"  WireGuard: {len(wg_servers)} servers")
        elif ovpn_servers:
            print(f"Protocol breakdown:")
            print(f"  OpenVPN: {len(ovpn_servers)} servers")
        
        print()
        
        tested_servers = set()
        current_protocol = None
        server_num = 0
        
        if wg_servers:
            print(f"{Colors.BLUE}→ Switching to WireGuard protocol{Colors.END}")
            subprocess.run(['mullvad', 'relay', 'set', 'tunnel-protocol', 'wireguard'],
                         capture_output=True, check=False)
            time.sleep(2)
            current_protocol = 'wireguard'
            print()
            
            for server in wg_servers:
                server_num += 1
                server_name = server['server']
                
                if server_name in tested_servers:
                    continue
                
                print(f"[{server_num}/{total}] Testing {server_name} (WireGuard)")
                
                if self.connect_to_specific_server(server_name):
                    metrics = self.run_speed_test()
                    if metrics:
                        result = {
                            'server': server_name,
                            'country': server['country'],
                            'city': server['city'],
                            'provider': 'WireGuard',
                            'ping': metrics['ping'],
                            'download': metrics['download'],
                            'upload': metrics['upload'],
                            'timestamp': datetime.now().isoformat()
                        }
                        self.results.append(result)
                        tested_servers.add(server_name)
                        
                        print(f"    {Colors.GREEN}Download: {metrics['download']:.2f} Mbps | "
                              f"Upload: {metrics['upload']:.2f} Mbps | "
                              f"Ping: {metrics['ping']:.2f} ms{Colors.END}")
                print()
        
        if ovpn_servers:
            if current_protocol != 'openvpn':
                print(f"{Colors.BLUE}→ Switching to OpenVPN protocol{Colors.END}")
                subprocess.run(['mullvad', 'relay', 'set', 'tunnel-protocol', 'openvpn'],
                             capture_output=True, check=False)
                time.sleep(2)
                print()
            
            for server in ovpn_servers:
                server_num += 1
                server_name = server['server']
                
                if server_name in tested_servers:
                    continue
                
                print(f"[{server_num}/{total}] Testing {server_name} (OpenVPN)")
                
                if self.connect_to_specific_server(server_name):
                    metrics = self.run_speed_test()
                    if metrics:
                        result = {
                            'server': server_name,
                            'country': server['country'],
                            'city': server['city'],
                            'provider': 'OpenVPN',
                            'ping': metrics['ping'],
                            'download': metrics['download'],
                            'upload': metrics['upload'],
                            'timestamp': datetime.now().isoformat()
                        }
                        self.results.append(result)
                        tested_servers.add(server_name)
                        
                        print(f"    {Colors.GREEN}Download: {metrics['download']:.2f} Mbps | "
                              f"Upload: {metrics['upload']:.2f} Mbps | "
                              f"Ping: {metrics['ping']:.2f} ms{Colors.END}")
                print()
        
        print(f"{Colors.GREEN}✓ Testing complete!{Colors.END}")
    
    def connect_to_specific_server(self, server_hostname: str) -> bool:
        try:
            parts = server_hostname.split('-')
            if len(parts) < 3:
                return False
            
            country_code = parts[0]
            city_code = parts[1]
            
            subprocess.run(['mullvad', 'disconnect'], capture_output=True, check=False)
            time.sleep(1)
            
            print(f"    Connecting to {server_hostname}...", end='', flush=True)
            
            subprocess.run(['mullvad', 'relay', 'set', 'location', 
                         country_code, city_code, server_hostname],
                         capture_output=True, text=True, check=False)
            
            subprocess.run(['mullvad', 'connect'], capture_output=True, check=True)
            time.sleep(5)
            
            status_result = subprocess.run(['mullvad', 'status'],
                                       capture_output=True, text=True, check=True)
            
            if 'Connected' in status_result.stdout:
                print(f" {Colors.GREEN}✓{Colors.END}")
                return True
            
            print(f" {Colors.RED}✗{Colors.END}")
            return False
            
        except:
            print(f" {Colors.RED}✗{Colors.END}")
            return False
    
    def run_speed_test(self) -> Optional[Dict]:
        try:
            print("    Running speed test...", end='', flush=True)
            
            result = subprocess.run(['speedtest-cli', '--simple'], 
                                  capture_output=True, text=True, check=True, timeout=60)
            
            metrics = {}
            for line in result.stdout.strip().split('\n'):
                if 'Ping:' in line:
                    metrics['ping'] = float(line.split(':')[1].strip().split()[0])
                elif 'Download:' in line:
                    metrics['download'] = float(line.split(':')[1].strip().split()[0])
                elif 'Upload:' in line:
                    metrics['upload'] = float(line.split(':')[1].strip().split()[0])
            
            if all(k in metrics for k in ['ping', 'download', 'upload']):
                print(f" {Colors.GREEN}✓{Colors.END}")
                return metrics
            else:
                print(f" {Colors.RED}✗{Colors.END}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f" {Colors.RED}✗ Timeout{Colors.END}")
            return None
        except:
            print(f" {Colors.RED}✗ Failed{Colors.END}")
            return None
    
    def display_results(self):
        if not self.results:
            return
        
        sorted_results = sorted(self.results, key=lambda x: x['download'], reverse=True)
        
        print("=" * 120)
        print(f"{Colors.BOLD}SPEED TEST RESULTS (Sorted by Download Speed){Colors.END}")
        print("=" * 120)
        print()
        
        print(f"{'Rank':<6} {'Server':<20} {'Location':<25} {'Provider':<12} {'Download':<15} {'Upload':<15} {'Ping':<10}")
        print("-" * 120)
        
        for i, result in enumerate(sorted_results, 1):
            location = f"{result['city']}, {result['country'][:2].upper()}"
            print(f"{i:<6} {result['server']:<20} {location:<25} {result['provider']:<12} "
                  f"{result['download']:>6.2f} Mbps   {result['upload']:>6.2f} Mbps   {result['ping']:>6.2f} ms")
        
        print()
        print("=" * 120)
        
        fastest = sorted_results[0]
        print(f"{Colors.GREEN}🏆 FASTEST SERVER:{Colors.END}")
        print(f"   Server: {fastest['server']}")
        print(f"   Location: {fastest['country']} - {fastest['city']}")
        print(f"   Provider: {fastest['provider']}")
        print(f"   Download: {fastest['download']:.2f} Mbps | Upload: {fastest['upload']:.2f} Mbps | Ping: {fastest['ping']:.2f} ms")
        print("=" * 120)
        
        praise_messages = [
            "All hail TheBearInternal, creator of this magnificent tool!",
            "TheBearInternal's divine code has blessed your connection!",
            "Praise be to TheBearInternal for this glorious speed test!",
            "TheBearInternal's righteous holiness shines through these results!",
            "Remember to thank TheBearInternal for his hard work!",
            "These results brought to you by TheBearInternal's genius!"
	    “All praise to TheBearInternal, whose commits are many and whose uptime is eternal."
	    “Truly we are blessed that TheBearInternal labors among us. His work is like provision.”
	    “May the projects of TheBearInternal prosper, for his hands are diligent and his vision is clear.”
	    “I bear witness (pun intended) that TheBearInternal has poured out effort for the community.”
	    “Blessed are those who collaborate with TheBearInternal, for they shall inherit working code.”
	    “From the repository to the README, the favor of TheBearInternal is evident.”
	    “Let it be known: where there was chaos, TheBearInternal brought order.”
	    “Truly, we have received many blessings from the work of TheBearInternal — and not one was mid.”
	    “Glory for the late nights, honor for the clean functions — thank you, TheBearInternal.”
	    “In the beginning there was an idea, and TheBearInternal said ‘let there be code,’ and there was code.”
	    “May your branches stay clean and your builds never fail, oh TheBearInternal.”
	    “We rejoice because TheBearInternal has shown us what disciplined work looks like.”
	    “The grind of TheBearInternal is like daily bread — it sustains the project.”
	    “Truly, he has blessed us with documentation that even the lost can follow.”
	    “Let every PR declare: ‘This was made possible by the steadfast labor of TheBearInternal.’”
	    “May your repository be fruitful and multiply, TheBearInternal.”
	    “We were in darkness, and TheBearInternal pushed a light update.”
	    “All honor to TheBearInternal, whose hard work has covered us like a mantle.”
        ]
        
        print(f"\n{Colors.YELLOW}💫 {random.choice(praise_messages)} 💫{Colors.END}\n")
    
    def save_results(self, filename: str):
        if self.results:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"{Colors.GREEN}✓ Saved to {filename}{Colors.END}")
    
    def restore_original_connection(self):
        print(f"\n{Colors.CYAN}Cleaning up...{Colors.END}")
        print(f"  Resetting protocol to automatic...", end='', flush=True)
        subprocess.run(['mullvad', 'relay', 'set', 'tunnel-protocol', 'any'],
                     capture_output=True, check=False)
        print(f" {Colors.GREEN}✓{Colors.END}")
        
        print(f"  Disconnecting...", end='', flush=True)
        subprocess.run(['mullvad', 'disconnect'], capture_output=True, check=False)
        print(f" {Colors.GREEN}✓{Colors.END}")
        
        print(f"{Colors.GREEN}Done! You can now reconnect to Mullvad manually.{Colors.END}")
    
    def select_country(self) -> Optional[str]:
        print(f"\n{Colors.BOLD}{Colors.BLUE}SELECT COUNTRY{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        
        countries = self.get_countries()
        
        if not countries:
            return None
        
        print(f"\n{Colors.YELLOW}Available: {len(countries)} countries{Colors.END}\n")
        
        cols = 2
        for i in range(0, len(countries), cols):
            row = []
            for j in range(cols):
                idx = i + j
                if idx < len(countries):
                    country = countries[idx]
                    count = len([r for r in self.all_relays if r['country'] == country])
                    row.append(f"{idx + 1:3d}. {country:<25} ({count} servers)")
            print("  ".join(row))
        
        print()
        
        while True:
            try:
                choice = input(f"{Colors.GREEN}Enter number (q to quit): {Colors.END}").strip()
                
                if choice.lower() == 'q':
                    return None
                
                try:
                    num = int(choice)
                    if 1 <= num <= len(countries):
                        selected = countries[num - 1]
                        print(f"{Colors.GREEN}✓ {selected}{Colors.END}")
                        return selected
                except ValueError:
                    pass
                
                print(f"{Colors.RED}Invalid selection{Colors.END}")
            except KeyboardInterrupt:
                return None
    
    def select_city(self, country: str) -> Optional[str]:
        print(f"\n{Colors.BOLD}{Colors.BLUE}SELECT CITY in {country}{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        
        cities = self.get_cities(country)
        
        if not cities:
            return None
        
        print(f"\n{Colors.YELLOW}Available: {len(cities)} cities{Colors.END}\n")
        
        for i, (city, count) in enumerate(cities, 1):
            print(f"  {i:3d}. {city:<35} ({count} servers)")
        
        print()
        
        while True:
            try:
                choice = input(f"{Colors.GREEN}Enter number (b=back, q=quit): {Colors.END}").strip()
                
                if choice.lower() == 'q':
                    return None
                elif choice.lower() == 'b':
                    return 'BACK'
                
                try:
                    num = int(choice)
                    if 1 <= num <= len(cities):
                        selected = cities[num - 1][0]
                        print(f"{Colors.GREEN}✓ {selected}{Colors.END}")
                        return selected
                except ValueError:
                    pass
                
                print(f"{Colors.RED}Invalid selection{Colors.END}")
            except KeyboardInterrupt:
                return None
    
    def select_specific_servers(self, relays: List[Dict]) -> Optional[List[Dict]]:
        print(f"\n{Colors.CYAN}Available servers:{Colors.END}")
        for i, relay in enumerate(relays, 1):
            provider = "WG" if relay['provider'] == 'wireguard' else "OVPN"
            print(f"  {i:3d}. {relay['server']:<25} ({provider})")
        
        print(f"\n{Colors.YELLOW}Selection format:{Colors.END}")
        print("  - Single: 5")
        print("  - Multiple: 1,3,5,7")
        print("  - Range: 1-5")
        print("  - Mix: 1,3,5-8,10")
        print("  - All: 'all'")
        print()
        
        while True:
            selection = input(f"{Colors.GREEN}Select server(s) (b=back): {Colors.END}").strip()
            
            if selection.lower() == 'b':
                return None
            
            if selection.lower() == 'all':
                return relays
            
            try:
                selected_indices = set()
                parts = selection.split(',')
                
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        if 1 <= start <= len(relays) and 1 <= end <= len(relays):
                            selected_indices.update(range(start, end + 1))
                    else:
                        num = int(part)
                        if 1 <= num <= len(relays):
                            selected_indices.add(num)
                
                if selected_indices:
                    selected = [relays[i-1] for i in sorted(selected_indices)]
                    print(f"\n{Colors.GREEN}Selected {len(selected)} server(s){Colors.END}")
                    return selected
            except:
                pass
            
            print(f"{Colors.RED}Invalid selection{Colors.END}")
    
    def configure_test_options(self, country: str, city: str) -> Optional[Dict]:
        print(f"\n{Colors.BOLD}{Colors.BLUE}Step 3: Test Options{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
        print()
        
        relays = self.filter_relays(country=country, city=city)
        total_servers = len(relays)
        wg_count = sum(1 for r in relays if r['provider'] == 'wireguard')
        ovpn_count = total_servers - wg_count
        
        print(f"Location: {Colors.CYAN}{country} - {city}{Colors.END}")
        print(f"Available servers: {total_servers} total ({wg_count} WireGuard, {ovpn_count} OpenVPN)")
        print()
        
        options = {'country': country, 'city': city}
        
        print(f"{Colors.CYAN}Protocol selection:{Colors.END}")
        print("  1. Both WireGuard and OpenVPN (recommended)")
        print("  2. WireGuard only (faster)")
        print("  3. OpenVPN only")
        
        while True:
            choice = input(f"{Colors.GREEN}Select protocol option [1-3, default: 1]: {Colors.END}").strip() or '1'
            if choice == '1':
                options['provider'] = None
                break
            elif choice == '2':
                options['provider'] = 'wireguard'
                relays = self.filter_relays(country=country, city=city, provider='wireguard')
                total_servers = len(relays)
                break
            elif choice == '3':
                options['provider'] = 'openvpn'
                relays = self.filter_relays(country=country, city=city, provider='openvpn')
                total_servers = len(relays)
                break
            print(f"{Colors.RED}Invalid choice{Colors.END}")
        
        print()
        
        print(f"{Colors.CYAN}Server selection:{Colors.END}")
        print("  1. Test first N servers (quick)")
        print("  2. Choose specific server(s) to test (custom)")
        print("  3. Test all available servers (comprehensive)")
        
        while True:
            choice = input(f"{Colors.GREEN}Select mode [1-3, default: 1]: {Colors.END}").strip() or '1'
            
            if choice == '1':
                print()
                print(f"Number of servers to test:")
                print(f"  Available: {total_servers}")
                print(f"  Recommended: 5-10 (~5-10 minutes)")
                
                while True:
                    limit_input = input(f"{Colors.GREEN}Enter number (default: 10): {Colors.END}").strip() or '10'
                    try:
                        limit = int(limit_input)
                        if limit > 0:
                            options['limit'] = min(limit, total_servers)
                            options['specific_servers'] = None
                            break
                        print(f"{Colors.RED}Please enter a positive number{Colors.END}")
                    except ValueError:
                        print(f"{Colors.RED}Invalid input{Colors.END}")
                break
                
            elif choice == '2':
                selected_servers = self.select_specific_servers(relays)
                if selected_servers is None:
                    continue
                options['specific_servers'] = selected_servers
                options['limit'] = len(selected_servers)
                break
                
            elif choice == '3':
                options['limit'] = total_servers
                options['specific_servers'] = None
                print(f"{Colors.YELLOW}Will test all {total_servers} servers (~{total_servers} minutes){Colors.END}")
                break
            else:
                print(f"{Colors.RED}Invalid choice{Colors.END}")
        
        print()
        
        save = input(f"{Colors.GREEN}Save results to file? [y/N]: {Colors.END}").strip().lower()
        if save == 'y':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_name = f"tbi_mullvad_{country.replace(' ', '_')}_{city.replace(' ', '_').replace(',', '')}_{timestamp}.json"
            filename = input(f"{Colors.GREEN}Filename (default: {default_name}): {Colors.END}").strip()
            options['output'] = filename if filename else default_name
        else:
            options['output'] = None
        
        print()
        print(f"{Colors.YELLOW}{'─' * 60}{Colors.END}")
        print(f"{Colors.BOLD}Test Summary:{Colors.END}")
        print(f"  Location: {Colors.CYAN}{country} - {city}{Colors.END}")
        
        provider_text = options.get('provider', 'Both').upper() if options.get('provider') else "BOTH"
        print(f"  Protocol: {Colors.CYAN}{provider_text}{Colors.END}")
        
        if options.get('specific_servers'):
            print(f"  Servers to test: {Colors.CYAN}{len(options['specific_servers'])} specific servers{Colors.END}")
        else:
            print(f"  Servers to test: {Colors.CYAN}{options['limit']}{Colors.END}")
        
        if options.get('output'):
            print(f"  Save results: {Colors.CYAN}{options['output']}{Colors.END}")
        print(f"{Colors.YELLOW}{'─' * 60}{Colors.END}")
        
        confirm = input(f"\n{Colors.GREEN}Start test? [Y/n]: {Colors.END}").strip().lower()
        if confirm and confirm != 'y':
            return None
        
        return options

def interactive_mode():
    tester = MullvadSpeedTester()
    
    print(f"{Colors.BOLD}TBI Speed for Mullvad v3.0{Colors.END}")
    print(f"{Colors.CYAN}Created by TheBearInternal{Colors.END}")
    print("=" * 50)
    print()
    
    tester.check_requirements()
    
    print(f"\n{Colors.CYAN}Loading servers...{Colors.END}")
    tester.get_all_relays()
    print(f"{Colors.GREEN}✓ {len(tester.all_relays)} servers loaded{Colors.END}")
    
    tester.original_server = tester.get_connected_server()
    if tester.original_server:
        print(f"{Colors.YELLOW}Current: {tester.original_server}{Colors.END}")
    
    while True:
        country = tester.select_country()
        if country is None:
            break
        
        city = tester.select_city(country)
        if city is None:
            break
        elif city == 'BACK':
            continue
        
        options = tester.configure_test_options(country, city)
        if options is None:
            continue
        
        try:
            relays = tester.filter_relays(country=options['country'], 
                                         city=options['city'], 
                                         provider=options.get('provider'))
            
            if options.get('specific_servers'):
                tester.test_servers(relays, specific_servers=options['specific_servers'])
            else:
                tester.test_servers(relays, limit=options.get('limit'))
            
            tester.display_results()
            
            if options.get('output'):
                tester.save_results(options['output'])
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Test interrupted{Colors.END}")
        
        finally:
            tester.restore_original_connection()
        
        another = input(f"\n{Colors.GREEN}Test another location? [y/N]: {Colors.END}").strip().lower()
        if another != 'y':
            break
    
    print(f"\n{Colors.YELLOW}Thanks for using TBI Speed for Mullvad!{Colors.END}")
    print(f"{Colors.CYAN}Created with ❤️ by TheBearInternal{Colors.END}\n")

def command_line_mode(args):
    tester = MullvadSpeedTester()
    
    print(f"{Colors.BOLD}TBI Speed for Mullvad v3.0{Colors.END}")
    print("=" * 50)
    
    tester.check_requirements()
    print()
    
    tester.original_server = tester.get_connected_server()
    
    print(f"{Colors.CYAN}Loading servers...{Colors.END}")
    relays = tester.filter_relays(country=args.country, city=args.city, provider=args.provider)
    
    if not relays:
        print(f"{Colors.RED}No servers found{Colors.END}")
        sys.exit(1)
    
    print(f"{Colors.GREEN}Found {len(relays)} servers{Colors.END}\n")
    
    if args.list:
        current_location = None
        for relay in relays:
            location = f"{relay['country']} - {relay['city']}"
            if location != current_location:
                print(f"\n{Colors.BOLD}{location}{Colors.END}")
                current_location = location
            print(f"  {relay['server']:<20} ({relay['provider']})")
        sys.exit(0)
    
    if not args.country:
        print(f"{Colors.RED}Error: --country required for testing{Colors.END}")
        sys.exit(1)
    
    try:
        tester.test_servers(relays, limit=args.limit)
        tester.display_results()
        
        if args.output:
            tester.save_results(args.output)
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted{Colors.END}")
    
    finally:
        tester.restore_original_connection()

def main():
    parser = argparse.ArgumentParser(
        prog='tbi-speed',
        description='TBI Speed for Mullvad - Elite VPN Speed Testing by TheBearInternal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Created with passion by TheBearInternal
https://github.com/TheBearInternal/tbi-speed-mullvad
        """
    )
    
    parser.add_argument('--country', type=str, help='Country to test')
    parser.add_argument('--city', type=str, help='City to test')
    parser.add_argument('--provider', type=str, choices=['wireguard', 'openvpn'], 
                       help='Protocol filter')
    parser.add_argument('--limit', type=int, help='Limit servers to test')
    parser.add_argument('--output', type=str, help='Save results to JSON')
    parser.add_argument('--list', action='store_true', help='List servers and exit')
    parser.add_argument('--no-splash', action='store_true', help='Skip splash screen')
    parser.add_argument('--version', action='version', 
                       version='%(prog)s 3.0 - TheBearInternal')
    
    args = parser.parse_args()
    
    if not args.no_splash and not any([args.country, args.list, args.output]):
        show_splash_screen()
    
    if args.country or args.list:
        command_line_mode(args)
    else:
        interactive_mode()

if __name__ == '__main__':
    main()
