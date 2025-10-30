#!/usr/bin/env python3
"""
██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██║     
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║     
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗╚██████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝

Advanced Cybersecurity Education & Research Suite
Professional toolkit for authorized security testing and education
"""

import os
import sys
import socket
import subprocess
import threading
import time
import json
import random
import requests
from datetime import datetime
import ipaddress
import concurrent.futures
from urllib.parse import urljoin, urlparse
import hashlib
import re

try:
    import nmap
    import scapy.all as scapy
    import dns.resolver
    import whois
    ADVANCED_MODULES = True
except ImportError:
    ADVANCED_MODULES = False
    print("Some advanced modules not available. Install with: pip install python-nmap scapy dnspython python-whois")

# Color definitions for the aesthetic
class Colors:
    # Matrix/Hacker style colors
    GREEN = '\033[32m'
    BRIGHT_GREEN = '\033[92m'
    CYAN = '\033[36m'
    BRIGHT_CYAN = '\033[96m'
    BLUE = '\033[34m'
    BRIGHT_BLUE = '\033[94m'
    RED = '\033[31m'
    BRIGHT_RED = '\033[91m'
    YELLOW = '\033[33m'
    BRIGHT_YELLOW = '\033[93m'
    MAGENTA = '\033[35m'
    BRIGHT_MAGENTA = '\033[95m'
    WHITE = '\033[37m'
    BRIGHT_WHITE = '\033[97m'
    BLACK = '\033[30m'
    GRAY = '\033[90m'
    
    # Special effects
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    RESET = '\033[0m'

class CyberSecFramework:
    def __init__(self):
        self.version = "3.0.0"
        self.session_data = {}
        self.authorized_targets = set()
        self.scan_results = {}
        self.current_target = None
        
    def print_banner(self):
        """Display hacker-style banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        banner = f"""
{Colors.BRIGHT_GREEN}
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ {Colors.BRIGHT_CYAN}███████╗███████╗ ██████╗
{Colors.BRIGHT_GREEN}██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗{Colors.BRIGHT_CYAN}██╔════╝██╔════╝██╔════╝
{Colors.BRIGHT_GREEN}██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝{Colors.BRIGHT_CYAN}███████╗█████╗  ██║     
{Colors.BRIGHT_GREEN}██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗{Colors.BRIGHT_CYAN}╚════██║██╔══╝  ██║     
{Colors.BRIGHT_GREEN}╚██████╗   ██║   ██████╔╝███████╗██║  ██║{Colors.BRIGHT_CYAN}███████║███████╗╚██████╗
{Colors.BRIGHT_GREEN} ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝{Colors.BRIGHT_CYAN}╚══════╝╚══════╝ ╚═════╝
{Colors.RESET}
{Colors.GREEN}[{Colors.WHITE} Made by Advanced Security Research Team {Colors.GREEN}]{Colors.RESET}

{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}ReaperNet |=| Administrator |{Colors.RESET}
{Colors.RED}═══════════ {Colors.WHITE}Help{Colors.RESET}

{Colors.RED}╔════ {Colors.WHITE}[Command]{Colors.RED} ═══════════════════════════════════════════ {Colors.WHITE}[Description]{Colors.RED} ═══════════╗
{Colors.RED}║{Colors.CYAN}  nmap            {Colors.WHITE}Network reconnaissance and port scanning         {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  attack          {Colors.WHITE}Educational attack simulations (SYN, Slowloris) {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  traffic         {Colors.WHITE}Network traffic analysis and monitoring         {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  vuln            {Colors.WHITE}Vulnerability scanning and web testing          {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  intel           {Colors.WHITE}IP/Domain intelligence and WHOIS lookup         {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  defense         {Colors.WHITE}IDS/IPS simulation and firewall testing         {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  report          {Colors.WHITE}Generate professional security reports          {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  help            {Colors.WHITE}Display this help menu                          {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  banner          {Colors.WHITE}Display the banner                              {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  clear           {Colors.WHITE}Clear the screen                                {Colors.RED}║
{Colors.RED}║{Colors.CYAN}  exit            {Colors.WHITE}Exit the framework                              {Colors.RED}║
{Colors.RED}╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.YELLOW}[{Colors.WHITE}⚠{Colors.YELLOW}] {Colors.WHITE}LEGAL WARNING: Use only on authorized systems with explicit permission{Colors.RESET}
{Colors.YELLOW}[{Colors.WHITE}⚠{Colors.YELLOW}] {Colors.WHITE}Educational and research purposes only - Users assume full legal responsibility{Colors.RESET}
"""
        print(banner)

    def legal_check(self):
        """Quick legal acknowledgment"""
        print(f"\n{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Legal Authorization Required{Colors.RESET}")
        response = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Do you have authorization for target systems? (y/N): {Colors.RESET}")
        if response.lower() != 'y':
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Exiting - Use only with proper authorization{Colors.RESET}")
            sys.exit(1)
        print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Authorization acknowledged{Colors.RESET}")

    def command_prompt(self):
        """Main command interface"""
        while True:
            try:
                # Display current target if set
                target_info = f" | Target: {self.current_target}" if self.current_target else ""
                prompt = f"{Colors.RED}┌──({Colors.WHITE}ReaperNet{Colors.RED}㉿{Colors.WHITE}root{Colors.RED})-[{Colors.WHITE}~{Colors.RED}]{target_info}\n└─{Colors.WHITE}$ {Colors.RESET}"
                
                command = input(prompt).strip().lower()
                
                if command == 'help' or command == '':
                    self.show_help()
                elif command == 'banner':
                    self.print_banner()
                elif command == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                elif command == 'nmap':
                    self.nmap_module()
                elif command == 'attack':
                    self.attack_module()
                elif command == 'traffic':
                    self.traffic_module()
                elif command == 'vuln':
                    self.vuln_module()
                elif command == 'intel':
                    self.intel_module()
                elif command == 'defense':
                    self.defense_module()
                elif command == 'report':
                    self.report_module()
                elif command == 'exit':
                    print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Goodbye! Use your skills ethically.{Colors.RESET}")
                    break
                else:
                    print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Unknown command: {command}{Colors.RESET}")
                    print(f"{Colors.YELLOW}[{Colors.WHITE}?{Colors.YELLOW}] {Colors.WHITE}Type 'help' for available commands{Colors.RESET}")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[{Colors.WHITE}!{Colors.YELLOW}] {Colors.WHITE}Interrupted by user{Colors.RESET}")
                break
            except Exception as e:
                print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Error: {e}{Colors.RESET}")

    def show_help(self):
        """Display help menu"""
        help_menu = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
{Colors.CYAN}║                                    {Colors.WHITE}CYBERSEC FRAMEWORK HELP{Colors.CYAN}                                    ║
{Colors.CYAN}╠═══════════════════════════════════════════════════════════════════════════════════════════════════╣
{Colors.CYAN}║                                                                                                   ║
{Colors.CYAN}║  {Colors.GREEN}RECONNAISSANCE MODULES{Colors.CYAN}                                                                     ║
{Colors.CYAN}║  {Colors.WHITE}nmap{Colors.CYAN}                - Network mapping, port scanning, service detection                   ║
{Colors.CYAN}║  {Colors.WHITE}intel{Colors.CYAN}               - IP/Domain intelligence, WHOIS, DNS enumeration                    ║
{Colors.CYAN}║                                                                                                   ║
{Colors.CYAN}║  {Colors.GREEN}OFFENSIVE MODULES{Colors.CYAN}                                                                          ║
{Colors.CYAN}║  {Colors.WHITE}attack{Colors.CYAN}              - Educational attack simulations (DoS, Flood)                       ║
{Colors.CYAN}║  {Colors.WHITE}vuln{Colors.CYAN}                - Vulnerability scanning, web testing, exploitation                  ║
{Colors.CYAN}║                                                                                                   ║
{Colors.CYAN}║  {Colors.GREEN}DEFENSIVE MODULES{Colors.CYAN}                                                                          ║
{Colors.CYAN}║  {Colors.WHITE}traffic{Colors.CYAN}             - Network traffic analysis and monitoring                            ║
{Colors.CYAN}║  {Colors.WHITE}defense{Colors.CYAN}             - IDS/IPS simulation, firewall testing                              ║
{Colors.CYAN}║                                                                                                   ║
{Colors.CYAN}║  {Colors.GREEN}UTILITY MODULES{Colors.CYAN}                                                                            ║
{Colors.CYAN}║  {Colors.WHITE}report{Colors.CYAN}              - Generate comprehensive security reports                            ║
{Colors.CYAN}║  {Colors.WHITE}help{Colors.CYAN}                - Display this help menu                                             ║
{Colors.CYAN}║  {Colors.WHITE}banner{Colors.CYAN}              - Display the main banner                                            ║
{Colors.CYAN}║  {Colors.WHITE}clear{Colors.CYAN}               - Clear the terminal screen                                          ║
{Colors.CYAN}║  {Colors.WHITE}exit{Colors.CYAN}                - Exit the framework                                                 ║
{Colors.CYAN}║                                                                                                   ║
{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(help_menu)

    def verify_target(self, target):
        """Verify target authorization"""
        try:
            # Check if target is local/private
            if target in ['localhost', '127.0.0.1', '::1']:
                print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Localhost target authorized{Colors.RESET}")
                self.current_target = target
                return True
                
            # Check for private IP ranges
            try:
                ip = ipaddress.ip_address(target)
                if ip.is_private or ip.is_loopback:
                    print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Private IP authorized: {target}{Colors.RESET}")
                    self.current_target = target
                    return True
            except ValueError:
                pass
                
            # Manual authorization for external targets
            print(f"{Colors.YELLOW}[{Colors.WHITE}!{Colors.YELLOW}] {Colors.WHITE}External target detected: {target}{Colors.RESET}")
            auth = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Do you have written authorization? (y/N): {Colors.RESET}")
            if auth.lower() == 'y':
                self.authorized_targets.add(target)
                self.current_target = target
                print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Authorization confirmed{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Authorization denied{Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Error verifying target: {e}{Colors.RESET}")
            return False

    def nmap_module(self):
        """Network reconnaissance module"""
        print(f"\n{Colors.CYAN}[{Colors.WHITE}*{Colors.CYAN}] {Colors.WHITE}NMAP - Network Reconnaissance Module{Colors.RESET}")
        
        if not ADVANCED_MODULES:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Nmap module not available. Install: pip install python-nmap{Colors.RESET}")
            return
            
        target = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Enter target (IP/hostname/range): {Colors.RESET}")
        
        if not self.verify_target(target):
            return
            
        scan_options = {
            '1': ('Quick Scan', '-T4 -F'),
            '2': ('Comprehensive Scan', '-T4 -A -v'),
            '3': ('Stealth Scan', '-sS -T2'),
            '4': ('UDP Scan', '-sU --top-ports 100'),
            '5': ('Service Detection', '-sV'),
            '6': ('OS Detection', '-O'),
            '7': ('Script Scan', '--script=default'),
            '8': ('Custom Scan', 'custom')
        }
        
        print(f"\n{Colors.YELLOW}[{Colors.WHITE}+{Colors.YELLOW}] {Colors.WHITE}Available Scan Types:{Colors.RESET}")
        for key, (name, _) in scan_options.items():
            print(f"{Colors.GREEN}[{key}] {Colors.WHITE}{name}{Colors.RESET}")
            
        choice = input(f"\n{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Select scan type: {Colors.RESET}")
        
        if choice in scan_options:
            scan_name, args = scan_options[choice]
            
            if args == 'custom':
                args = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Enter custom Nmap arguments: {Colors.RESET}")
                
            print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Starting {scan_name} on {target}...{Colors.RESET}")
            
            try:
                nm = nmap.PortScanner()
                result = nm.scan(target, arguments=args)
                
                print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Scan completed{Colors.RESET}")
                
                for host in nm.all_hosts():
                    state = nm[host].state()
                    print(f"\n{Colors.BRIGHT_CYAN}[{Colors.WHITE}+{Colors.BRIGHT_CYAN}] {Colors.WHITE}Host: {host} ({state}){Colors.RESET}")
                    
                    if 'tcp' in nm[host]:
                        tcp_ports = nm[host]['tcp'].keys()
                        for port in sorted(tcp_ports):
                            port_state = nm[host]['tcp'][port]['state']
                            service = nm[host]['tcp'][port].get('name', 'unknown')
                            version = nm[host]['tcp'][port].get('version', '')
                            
                            color = Colors.GREEN if port_state == 'open' else Colors.RED
                            print(f"  {color}[{port_state.upper()}]{Colors.WHITE} {port}/tcp {service} {version}{Colors.RESET}")
                            
                # Store results
                self.scan_results[target] = result
                
            except Exception as e:
                print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Scan failed: {e}{Colors.RESET}")

    def attack_module(self):
        """Educational attack simulation module"""
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}] {Colors.WHITE}ATTACK - Educational Simulation Module{Colors.RESET}")
        print(f"{Colors.YELLOW}[{Colors.WHITE}!{Colors.YELLOW}] {Colors.WHITE}For educational purposes only - Use responsibly{Colors.RESET}")
        
        target = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Enter target for simulation: {Colors.RESET}")
        
        if not self.verify_target(target):
            return
            
        attacks = {
            '1': 'TCP SYN Flood Simulation',
            '2': 'Slowloris HTTP Attack',
            '3': 'UDP Flood Simulation', 
            '4': 'ICMP Ping Flood',
            '5': 'HTTP GET Flood',
            '6': 'Port Scan Detection Test'
        }
        
        print(f"\n{Colors.YELLOW}[{Colors.WHITE}+{Colors.YELLOW}] {Colors.WHITE}Available Attack Simulations:{Colors.RESET}")
        for key, name in attacks.items():
            print(f"{Colors.RED}[{key}] {Colors.WHITE}{name}{Colors.RESET}")
            
        choice = input(f"\n{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Select attack type: {Colors.RESET}")
        
        if choice == '1':
            self.syn_flood_sim(target)
        elif choice == '2':
            self.slowloris_sim(target)
        elif choice == '3':
            self.udp_flood_sim(target)
        elif choice == '4':
            self.icmp_flood_sim(target)
        elif choice == '5':
            self.http_flood_sim(target)
        elif choice == '6':
            self.portscan_detection_test(target)

    def syn_flood_sim(self, target):
        """TCP SYN flood simulation"""
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}] {Colors.WHITE}TCP SYN Flood Simulation{Colors.RESET}")
        
        port = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Target port (default 80): {Colors.RESET}") or "80"
        duration = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Duration in seconds (max 30): {Colors.RESET}") or "10"
        
        try:
            port = int(port)
            duration = min(int(duration), 30)
            
            print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Starting SYN flood simulation for {duration}s...{Colors.RESET}")
            
            start_time = time.time()
            packet_count = 0
            
            while time.time() - start_time < duration:
                # Simulate SYN packets (educational demonstration)
                src_ip = f"192.168.1.{random.randint(1, 254)}"
                packet_count += 1
                
                if packet_count % 100 == 0:
                    print(f"{Colors.GREEN}[{Colors.WHITE}+{Colors.GREEN}] {Colors.WHITE}Packets simulated: {packet_count}{Colors.RESET}")
                    
                time.sleep(0.01)
                
            print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Simulation complete. Total packets: {packet_count}{Colors.RESET}")
            print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}In real attack, this would overwhelm connection table{Colors.RESET}")
            
        except ValueError:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Invalid input. Use numeric values.{Colors.RESET}")

    def slowloris_sim(self, target):
        """Slowloris attack simulation"""
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}] {Colors.WHITE}Slowloris HTTP Attack Simulation{Colors.RESET}")
        
        port = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Target port (default 80): {Colors.RESET}") or "80"
        connections = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Number of connections (max 10): {Colors.RESET}") or "5"
        
        try:
            port = int(port)
            connections = min(int(connections), 10)
            
            print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Starting Slowloris with {connections} connections...{Colors.RESET}")
            
            sockets = []
            
            # Create partial HTTP connections
            for i in range(connections):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((target, port))
                    sock.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
                    sockets.append(sock)
                    print(f"{Colors.GREEN}[{Colors.WHITE}+{Colors.GREEN}] {Colors.WHITE}Connection {i+1} established{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Connection {i+1} failed: {e}{Colors.RESET}")
                    
            # Keep connections alive
            for round in range(3):
                print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Sending keep-alive headers (round {round+1})...{Colors.RESET}")
                for sock in sockets[:]:
                    try:
                        sock.send(f"X-Keep-Alive: {random.randint(1, 1000)}\r\n".encode())
                    except:
                        sockets.remove(sock)
                time.sleep(2)
                
            # Clean up
            for sock in sockets:
                sock.close()
                
            print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Slowloris simulation complete{Colors.RESET}")
            
        except ValueError:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Invalid input{Colors.RESET}")

    def traffic_module(self):
        """Network traffic analysis module"""
        print(f"\n{Colors.CYAN}[{Colors.WHITE}*{Colors.CYAN}] {Colors.WHITE}TRAFFIC - Network Analysis Module{Colors.RESET}")
        
        options = {
            '1': 'Live Packet Capture',
            '2': 'Traffic Pattern Analysis',
            '3': 'Protocol Statistics',
            '4': 'Bandwidth Monitor',
            '5': 'Anomaly Detection'
        }
        
        print(f"\n{Colors.YELLOW}[{Colors.WHITE}+{Colors.YELLOW}] {Colors.WHITE}Traffic Analysis Options:{Colors.RESET}")
        for key, name in options.items():
            print(f"{Colors.CYAN}[{key}] {Colors.WHITE}{name}{Colors.RESET}")
            
        choice = input(f"\n{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Select option: {Colors.RESET}")
        
        if choice == '1':
            self.packet_capture()
        elif choice == '2':
            self.traffic_patterns()
        elif choice == '3':
            self.protocol_stats()

    def packet_capture(self):
        """Live packet capture simulation"""
        print(f"\n{Colors.CYAN}[{Colors.WHITE}*{Colors.CYAN}] {Colors.WHITE}Live Packet Capture{Colors.RESET}")
        
        duration = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Capture duration (seconds): {Colors.RESET}") or "10"
        
        try:
            duration = int(duration)
            print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Starting packet capture for {duration}s...{Colors.RESET}")
            
            # Simulate packet capture
            protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'DNS']
            packet_count = 0
            
            start_time = time.time()
            while time.time() - start_time < duration:
                protocol = random.choice(protocols)
                src_ip = f"192.168.1.{random.randint(1, 254)}"
                dst_ip = f"10.0.0.{random.randint(1, 254)}"
                size = random.randint(64, 1500)
                
                packet_count += 1
                
                if packet_count % 50 == 0:
                    print(f"{Colors.GREEN}[{Colors.WHITE}+{Colors.GREEN}] {Colors.WHITE}Packet {packet_count}: {src_ip} -> {dst_ip} [{protocol}] {size} bytes{Colors.RESET}")
                    
                time.sleep(0.1)
                
            print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Capture complete. Total packets: {packet_count}{Colors.RESET}")
            
        except ValueError:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Invalid duration{Colors.RESET}")

    def vuln_module(self):
        """Vulnerability scanning module"""
        print(f"\n{Colors.MAGENTA}[{Colors.WHITE}*{Colors.MAGENTA}] {Colors.WHITE}VULN - Vulnerability Scanner{Colors.RESET}")
        
        target = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Enter target URL/IP: {Colors.RESET}")
        
        if not self.verify_target(target):
            return
            
        vulns = {
            '1': 'Directory Brute Force',
            '2': 'SQL Injection Test',
            '3': 'XSS Scanner',
            '4': 'SSL/TLS Analysis',
            '5': 'HTTP Header Analysis',
            '6': 'Port Vulnerability Check'
        }
        
        print(f"\n{Colors.YELLOW}[{Colors.WHITE}+{Colors.YELLOW}] {Colors.WHITE}Vulnerability Tests:{Colors.RESET}")
        for key, name in vulns.items():
            print(f"{Colors.MAGENTA}[{key}] {Colors.WHITE}{name}{Colors.RESET}")
            
        choice = input(f"\n{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Select test: {Colors.RESET}")
        
        if choice == '1':
            self.directory_bruteforce(target)
        elif choice == '2':
            self.sql_injection_test(target)
        elif choice == '5':
            self.http_header_analysis(target)

    def directory_bruteforce(self, target):
        """Directory brute force scanner"""
        print(f"\n{Colors.MAGENTA}[{Colors.WHITE}*{Colors.MAGENTA}] {Colors.WHITE}Directory Brute Force Scanner{Colors.RESET}")
        
        common_dirs = [
            'admin', 'administrator', 'login', 'backup', 'config', 'database',
            'uploads', 'images', 'css', 'js', 'api', 'test', 'dev', 'beta',
            'private', 'secret', 'hidden', 'files', 'docs', 'data'
        ]
        
        print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Testing {len(common_dirs)} directories...{Colors.RESET}")
        
        found = []
        
        for directory in common_dirs:
            try:
                if not target.startswith('http'):
                    url = f"http://{target}/{directory}"
                else:
                    url = f"{target}/{directory}"
                    
                response = requests.get(url, timeout=3, allow_redirects=False)
                
                if response.status_code in [200, 301, 302, 403]:
                    found.append((directory, response.status_code))
                    color = Colors.GREEN if response.status_code == 200 else Colors.YELLOW
                    print(f"  {color}[{response.status_code}] {Colors.WHITE}/{directory}{Colors.RESET}")
                    
            except requests.exceptions.RequestException:
                pass
                
        if found:
            print(f"\n{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Found {len(found)} accessible directories{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}No directories found{Colors.RESET}")

    def http_header_analysis(self, target):
        """HTTP security header analysis"""
        print(f"\n{Colors.MAGENTA}[{Colors.WHITE}*{Colors.MAGENTA}] {Colors.WHITE}HTTP Security Header Analysis{Colors.RESET}")
        
        try:
            if not target.startswith('http'):
                url = f"http://{target}"
            else:
                url = target
                
            response = requests.get(url, timeout=10)
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME type sniffing protection',
                'X-XSS-Protection': 'XSS filter',
                'Strict-Transport-Security': 'HTTPS enforcement',
                'Content-Security-Policy': 'Content injection protection',
                'Referrer-Policy': 'Referrer information control'
            }
            
            print(f"{Colors.CYAN}[{Colors.WHITE}+{Colors.CYAN}] {Colors.WHITE}Security Header Analysis:{Colors.RESET}")
            
            for header, description in security_headers.items():
                if header in headers:
                    print(f"  {Colors.GREEN}[✓] {Colors.WHITE}{header}: {headers[header]}{Colors.RESET}")
                else:
                    print(f"  {Colors.RED}[✗] {Colors.WHITE}{header}: Missing ({description}){Colors.RESET}")
                    
            print(f"\n{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Server: {headers.get('Server', 'Unknown')}{Colors.RESET}")
            print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Response Code: {response.status_code}{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Analysis failed: {e}{Colors.RESET}")

    def intel_module(self):
        """Intelligence gathering module"""
        print(f"\n{Colors.BRIGHT_BLUE}[{Colors.WHITE}*{Colors.BRIGHT_BLUE}] {Colors.WHITE}INTEL - Intelligence Gathering{Colors.RESET}")
        
        target = input(f"{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Enter domain/IP: {Colors.RESET}")
        
        intel_options = {
            '1': 'WHOIS Lookup',
            '2': 'DNS Enumeration',
            '3': 'Subdomain Discovery',
            '4': 'IP Geolocation',
            '5': 'Reverse DNS',
            '6': 'Certificate Analysis'
        }
        
        print(f"\n{Colors.YELLOW}[{Colors.WHITE}+{Colors.YELLOW}] {Colors.WHITE}Intelligence Options:{Colors.RESET}")
        for key, name in intel_options.items():
            print(f"{Colors.BRIGHT_BLUE}[{key}] {Colors.WHITE}{name}{Colors.RESET}")
            
        choice = input(f"\n{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Select option: {Colors.RESET}")
        
        if choice == '1':
            self.whois_lookup(target)
        elif choice == '2':
            self.dns_enumeration(target)
        elif choice == '4':
            self.ip_geolocation(target)

    def whois_lookup(self, domain):
        """WHOIS information lookup"""
        print(f"\n{Colors.BRIGHT_BLUE}[{Colors.WHITE}*{Colors.BRIGHT_BLUE}] {Colors.WHITE}WHOIS Lookup for {domain}{Colors.RESET}")
        
        if not ADVANCED_MODULES:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}WHOIS module not available{Colors.RESET}")
            return
            
        try:
            w = whois.whois(domain)
            
            print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}WHOIS Information:{Colors.RESET}")
            print(f"  {Colors.CYAN}Domain:{Colors.WHITE} {w.domain_name}{Colors.RESET}")
            print(f"  {Colors.CYAN}Registrar:{Colors.WHITE} {w.registrar}{Colors.RESET}")
            print(f"  {Colors.CYAN}Creation Date:{Colors.WHITE} {w.creation_date}{Colors.RESET}")
            print(f"  {Colors.CYAN}Expiration Date:{Colors.WHITE} {w.expiration_date}{Colors.RESET}")
            
            if w.name_servers:
                print(f"  {Colors.CYAN}Name Servers:{Colors.WHITE} {', '.join(w.name_servers)}{Colors.RESET}")
                
        except Exception as e:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}WHOIS lookup failed: {e}{Colors.RESET}")

    def report_module(self):
        """Generate security reports"""
        print(f"\n{Colors.GREEN}[{Colors.WHITE}*{Colors.GREEN}] {Colors.WHITE}REPORT - Security Report Generator{Colors.RESET}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cybersec_report_{timestamp}.txt"
        
        report_content = f"""
═══════════════════════════════════════════════════════════════════════════════
                      CYBERSECURITY ASSESSMENT REPORT
═══════════════════════════════════════════════════════════════════════════════

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Framework: Advanced Cybersecurity Education & Research Suite v{self.version}
Operator: Authorized Security Researcher

EXECUTIVE SUMMARY
═════════════════
This report contains the results of authorized security testing conducted
using the CyberSec Framework for educational and research purposes.

SCOPE AND TARGETS
════════════════
Authorized Targets: {list(self.authorized_targets) if self.authorized_targets else ['localhost', '127.0.0.1']}
Current Target: {self.current_target or 'None set'}

SCAN RESULTS
════════════
Total Scans Performed: {len(self.scan_results)}

"""
        
        for target, results in self.scan_results.items():
            report_content += f"\nTarget: {target}\n"
            report_content += f"Results: {str(results)[:500]}...\n"
            report_content += "-" * 50 + "\n"
            
        report_content += f"""

RECOMMENDATIONS
══════════════
1. Ensure all identified vulnerabilities are properly remediated
2. Implement security controls for any exposed services
3. Regular security assessments should be conducted
4. Monitor network traffic for suspicious activities
5. Maintain up-to-date security patches and configurations

DISCLAIMER
══════════
This assessment was conducted for educational and authorized testing purposes only.
All activities were performed with proper authorization and in compliance with
applicable laws and regulations.

Report generated by CyberSec Framework v{self.version}
═══════════════════════════════════════════════════════════════════════════════
"""
        
        try:
            with open(filename, 'w') as f:
                f.write(report_content)
                
            print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}Report generated: {filename}{Colors.RESET}")
            print(f"{Colors.CYAN}[{Colors.WHITE}*{Colors.CYAN}] {Colors.WHITE}Report saved to current directory{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Report generation failed: {e}{Colors.RESET}")

    def defense_module(self):
        """Defense and monitoring module"""
        print(f"\n{Colors.GREEN}[{Colors.WHITE}*{Colors.GREEN}] {Colors.WHITE}DEFENSE - Security Monitoring{Colors.RESET}")
        
        defense_options = {
            '1': 'IDS/IPS Simulation',
            '2': 'Firewall Rule Test',
            '3': 'Log Analysis Demo',
            '4': 'Honeypot Simulation',
            '5': 'Intrusion Detection'
        }
        
        print(f"\n{Colors.YELLOW}[{Colors.WHITE}+{Colors.YELLOW}] {Colors.WHITE}Defense Options:{Colors.RESET}")
        for key, name in defense_options.items():
            print(f"{Colors.GREEN}[{key}] {Colors.WHITE}{name}{Colors.RESET}")
            
        choice = input(f"\n{Colors.CYAN}[{Colors.WHITE}?{Colors.CYAN}] {Colors.WHITE}Select option: {Colors.RESET}")
        
        if choice == '1':
            self.ids_simulation()
        elif choice == '3':
            self.log_analysis_demo()

    def ids_simulation(self):
        """Intrusion Detection System simulation"""
        print(f"\n{Colors.GREEN}[{Colors.WHITE}*{Colors.GREEN}] {Colors.WHITE}IDS/IPS Simulation{Colors.RESET}")
        
        print(f"{Colors.YELLOW}[{Colors.WHITE}*{Colors.YELLOW}] {Colors.WHITE}Monitoring network for suspicious activity...{Colors.RESET}")
        
        # Simulate IDS alerts
        alerts = [
            "Port scan detected from 192.168.1.100",
            "Suspicious HTTP requests to /admin",
            "Multiple failed SSH login attempts",
            "Unusual DNS queries detected",
            "Potential DDoS attack pattern",
            "Malware signature detected in traffic"
        ]
        
        for i in range(10):
            time.sleep(1)
            if random.random() < 0.3:  # 30% chance of alert
                alert = random.choice(alerts)
                severity = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
                color = {
                    "LOW": Colors.GREEN,
                    "MEDIUM": Colors.YELLOW, 
                    "HIGH": Colors.RED,
                    "CRITICAL": Colors.BRIGHT_RED
                }[severity]
                
                print(f"{color}[{severity}] {Colors.WHITE}{alert}{Colors.RESET}")
            else:
                print(f"{Colors.GREEN}[INFO] {Colors.WHITE}Network traffic normal{Colors.RESET}")
                
        print(f"{Colors.GREEN}[{Colors.WHITE}✓{Colors.GREEN}] {Colors.WHITE}IDS monitoring simulation complete{Colors.RESET}")


def main():
    """Main function"""
    try:
        framework = CyberSecFramework()
        framework.print_banner()
        framework.legal_check()
        framework.command_prompt()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[{Colors.WHITE}!{Colors.YELLOW}] {Colors.WHITE}Framework terminated by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[{Colors.WHITE}!{Colors.RED}] {Colors.WHITE}Critical error: {e}{Colors.RESET}")


if __name__ == "__main__":
    main()
