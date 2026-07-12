#!/usr/bin/env python3 

import subprocess
import re
import sys
import random
import argparse
import os
import platform
import time
import threading


def get_os():
    return platform.system()


if get_os() == "Windows":
    import winreg

# --- ASCII Art Banner ---
CODARA_BANNER = r"""
                                   ,__ __    ___ 
              |                   /|  |  |  / (_)
  __   __   __|   __,   ,_    __,  |  |  | |     
 /    /  \_/  |  /  |  /  |  /  |  |  |  | |     
 \___/\__/ \_/|_/\_/|_/   |_/\_/|_/|  |  |_/\___/
                                                 
      MAC Utility CLI (Multi-Platform)
  Codara Software Solutions
----------------------------------------
"""
COMPANY_NAME = "Codara Software Solutions"
APP_NAME = "CodaraMC MAC Utility CLI"
VERSION = "2.0.0" 

LAA_START_BYTE = 0x02

VENDOR_OUIS = {
    "apple": "00:1B:63",
    "cisco": "00:0F:F7",
    "dlink": "00:17:9A",
    "samsung": "00:00:F0",
    "random": None
}

# --- Helper Functions ---
def run_command(command_list, error_message, allow_fail=False):
    try:
        return subprocess.check_output(command_list, stderr=subprocess.PIPE).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        stderr_text = ""
        if e.stderr:
            try:
                stderr_text = e.stderr.decode('utf-8').strip()
            except AttributeError:
                stderr_text = str(e.stderr).strip()

        if not allow_fail:
            print(f"❌ ERROR: {error_message or 'Command failed.'}")
            if stderr_text:
                print(f"   stderr: {stderr_text}")
            print(f"   command: {' '.join(command_list)}")
            sys.exit(1)
        return ""
    except FileNotFoundError:
        if not allow_fail:
            print(f"❌ ERROR: System command '{command_list[0]}' not found.")
            sys.exit(1)
        return ""


def print_macos_restriction_notice(interface):
    if get_os() != "Darwin":
        return

    normalized_interface = interface.lower()
    if any(marker in normalized_interface for marker in ["wifi", "wi-fi", "airport", "en0", "en1", "en2", "awdl"]):
        print("ℹ️  INFO: On recent macOS versions, changing the MAC address of built-in Wi-Fi interfaces is often restricted by the operating system.")
        print("   If the change fails, try a different interface or a supported external adapter.")

def get_current_mac(interface):
    os_type = get_os()
    if os_type == "Linux":
        output = run_command(["ip", "link", "show", interface], "", allow_fail=True)
        mac_search = re.search(r"link/ether\s+([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})", output)
        return mac_search.group(1).lower() if mac_search else None
    elif os_type == "Darwin":
        output = run_command(["ifconfig", interface], "", allow_fail=True)
        mac_search = re.search(r"ether\s+([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})", output)
        return mac_search.group(1).lower() if mac_search else None
    elif os_type == "Windows":
        output = run_command(["getmac", "/v", "/fo", "csv"], "", allow_fail=True)
        for line in output.splitlines():
            if interface.lower() in line.lower():
                mac_search = re.search(r"([0-9a-fA-F]{2}(-[0-9a-fA-F]{2}){5})", line)
                return mac_search.group(1).replace("-", ":").lower() if mac_search else None
    return "OS Not Supported"

def generate_mac(vendor=None):
    if vendor and vendor.lower() in VENDOR_OUIS and VENDOR_OUIS[vendor.lower()]:
        oui = VENDOR_OUIS[vendor.lower()].split(':')
        mac_bytes = [int(x, 16) for x in oui]
    else:
        mac_bytes = [LAA_START_BYTE]
        
    while len(mac_bytes) < 6:
        mac_bytes.append(random.randint(0x00, 0xff))
            
    return ':'.join(map(lambda x: "%02x" % x, mac_bytes))

def is_valid_mac(mac_address):
    mac_regex = r"^([0-9a-fA-F]{2}[:\-]){5}([0-9a-fA-F]{2})$"
    return re.match(mac_regex, mac_address) is not None

def change_hostname(new_hostname):
    os_type = get_os()
    print(f"🕵️  Stealth Mode: Changing Hostname to {new_hostname}...")
    if os_type == "Linux":
        run_command(["hostnamectl", "set-hostname", new_hostname], "", allow_fail=True)
    elif os_type == "Darwin":
        run_command(["scutil", "--set", "HostName", new_hostname], "", allow_fail=True)
    elif os_type == "Windows":
        run_command(["wmic", "computersystem", "where", f"name='%computername%'", "call", "rename", f"name='{new_hostname}'"], "", allow_fail=True)

# --- Windows Specific Functions (Bulletproof WMI Method) ---
def get_windows_registry_subkey(interface):
    """Windows වලින් කෙලින්ම අදාළ Registry Folder එක අංකය අසා දැනගැනීම"""
   
    output = run_command(["wmic", "nic", "where", f"NetConnectionID='{interface}'", "get", "Index", "/value"], "", allow_fail=True)
    match = re.search(r"Index=(\d+)", output)
    if match:
        return f"{int(match.group(1)):04d}"
    
   
    cmd = ["powershell", "-NoProfile", "-Command", f"(Get-CimInstance -ClassName Win32_NetworkAdapter -Filter \"NetConnectionID='{interface}'\").DeviceID"]
    output = run_command(cmd, "", allow_fail=True)
    try:
        return f"{int(output.strip()):04d}"
    except:
        return None

def change_mac_windows(interface, new_mac):
    mac_no_colon = new_mac.replace(":", "").replace("-", "")
    

    subkey = get_windows_registry_subkey(interface)
    
    if not subkey:
        print(f"❌ ERROR: Could not locate adapter '{interface}' in the System. Check the exact name (e.g., 'Wi-Fi').")
        return False

    reg_path = f"SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{subkey}"
    
    try:
       
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "NetworkAddress", 0, winreg.REG_SZ, mac_no_colon)
        winreg.CloseKey(reg_key)
        
        print("🔄 Restarting Network Adapter to apply changes (Please wait 5-10s)...")
        run_command(["netsh", "interface", "set", "interface", f"name={interface}", "admin=disable"], "", allow_fail=True)
        time.sleep(3)
        run_command(["netsh", "interface", "set", "interface", f"name={interface}", "admin=enable"], "", allow_fail=True)
        time.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Windows Error: Requires Administrator privileges. Right-click and 'Run as Administrator'. ({e})")
        return False

def reset_mac_windows(interface):
    subkey = get_windows_registry_subkey(interface)
    
    if not subkey:
        print(f"❌ ERROR: Could not locate adapter '{interface}' to reset.")
        return False

    reg_path = f"SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{subkey}"
    
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE)
        try:
            winreg.DeleteValue(reg_key, "NetworkAddress")
        except OSError:
            pass # Already default
        winreg.CloseKey(reg_key)
        
        print("🔄 Restarting Network Adapter...")
        run_command(["netsh", "interface", "set", "interface", f"name={interface}", "admin=disable"], "", allow_fail=True)
        time.sleep(3)
        run_command(["netsh", "interface", "set", "interface", f"name={interface}", "admin=enable"], "", allow_fail=True)
        time.sleep(3)
        return True
    except Exception as e:
        print(f"❌ Windows Error: Run as Administrator. ({e})")
        return False

# --- Main Feature Functions ---
def change_mac(interface, new_mac, timer=None, stealth=False):
    os_type = get_os()
    
    if os_type in ["Linux", "Darwin"] and subprocess.call(["id", "-u"]) != 0:
        print("❌ ERROR: You must run this tool with root privileges (sudo).")
        return

    print(f"\n[{COMPANY_NAME}] Platform: {os_type}")
    print(f"Attempting to change MAC address for {interface} to {new_mac}...")
    
    if stealth:
        random_host = f"User-{random.randint(1000,9999)}"
        change_hostname(random_host)

    success = True
    if os_type == "Linux":
        run_command(["ip", "link", "set", interface, "down"], f"Failed to bring down {interface}.")
        run_command(["ip", "link", "set", interface, "address", new_mac], f"Failed to set MAC address.")
        run_command(["ip", "link", "set", interface, "up"], f"Failed to bring up {interface}.")
        
    elif os_type == "Darwin":
        print_macos_restriction_notice(interface)
        run_command(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-z"], "", allow_fail=True)
        run_command(["ifconfig", interface, "ether", new_mac], f"Failed to set MAC address.")
        
    elif os_type == "Windows":
        success = change_mac_windows(interface, new_mac)

    if not success:
        return

    print(f"✅ SUCCESS! {interface} new MAC sequence executed.")

    if timer:
        print(f"⏳ Timer set for {timer} seconds. The MAC will revert automatically...")
        def revert_task():
            time.sleep(timer)
            print(f"\n⏰ Timer expired! Reverting {interface} to original MAC...")
            reset_to_permanent(interface)
        
        t = threading.Thread(target=revert_task)
        t.start()

def reset_to_permanent(interface):
    os_type = get_os()
    if os_type in ["Linux", "Darwin"] and subprocess.call(["id", "-u"]) != 0:
        return

    print(f"\n[{COMPANY_NAME}] Resetting MAC address for {interface} to permanent hardware address...")
   
    if os_type == "Linux":
        run_command(["macchanger", "-p", interface], "", allow_fail=True)
        print(f"✅ SUCCESS! {interface} reset to original hardware MAC.")
    elif os_type == "Darwin":
        run_command(["ifconfig", interface, "down"], "", allow_fail=True)
        run_command(["ifconfig", interface, "up"], "", allow_fail=True)
        print(f"✅ SUCCESS! {interface} reset to original hardware MAC.")
    elif os_type == "Windows":
        success = reset_mac_windows(interface)
        if success:
            print(f"✅ SUCCESS! {interface} reset to original hardware MAC.")

# --- CLI Setup ---
def main():
    print(CODARA_BANNER) 

    parser = argparse.ArgumentParser(description=f"{APP_NAME} | {VERSION}")
    parser.add_argument("-i", "--interface", required=True, help="Network interface (e.g., eth0, en0, 'Wi-Fi')")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("status", help="Show current MAC status.")

    parser_random = subparsers.add_parser("random", help="Change to a random MAC address.")
    parser_random.add_argument("-v", "--vendor", choices=VENDOR_OUIS.keys(), default="random")
    parser_random.add_argument("-t", "--timer", type=int, help="Auto-revert time in seconds.")
    parser_random.add_argument("--stealth", action="store_true", help="Randomize hostname.")

    parser_set = subparsers.add_parser("set", help="Change to a specific MAC address.")
    parser_set.add_argument("mac_address", help="New MAC address")
    parser_set.add_argument("-t", "--timer", type=int)
    parser_set.add_argument("--stealth", action="store_true")
    
    subparsers.add_parser("reset", help="Reset MAC address")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()

    if args.command == "status":
        print(f"Current Interface MAC: {get_current_mac(args.interface)}")
    elif args.command == "random":
        new_mac = generate_mac(args.vendor)
        change_mac(args.interface, new_mac, getattr(args, 'timer', None), getattr(args, 'stealth', False))
    elif args.command == "set":
        if not is_valid_mac(args.mac_address):
            print("❌ ERROR: Invalid MAC format.")
            sys.exit(1)
        change_mac(args.interface, args.mac_address, getattr(args, 'timer', None), getattr(args, 'stealth', False))
    elif args.command == "reset":
        reset_to_permanent(args.interface)

if __name__ == "__main__":
    main()
