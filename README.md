# 🛡️ CodaraMC: Multi-Platform MAC Utility CLI

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-success.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**CodaraMC** is a robust, production-ready Command Line Interface (CLI) utility developed by Codara Software Solutions. It allows security professionals, penetration testers, and developers to easily manage, spoof, and randomize network MAC addresses across multiple operating systems.

## ✨ Features (v2.0.0 Major Update)
*   **🌍 Multi-Platform Support:** Fully compatible with **Windows**, **Linux**, and **macOS**. 
*   **🕵️ Stealth Mode:** Randomize both your MAC address and Computer Hostname simultaneously for maximum anonymity.
*   **⏳ Auto-Revert Timer:** Set a time bomb! Spoof your MAC temporarily and let the tool automatically revert to your original hardware MAC after a given number of seconds.
*   **🏭 Vendor Specific OUI:** Generate realistic MAC addresses mimicking popular vendors (Apple, Cisco, Samsung, D-Link, etc.).
*   **🛡️ Smart Hardware Detection:** Uses advanced WMI (Windows) and Registry scanning to accurately locate and modify adapter settings without triggering security blocks.

## 🚀 Installation

Ensure you have Python 3 installed. Clone this repository and install it globally using pip:

```bash
git clone [https://github.com/MadhushaMG/codara-mc.git](https://github.com/MadhushaMG/codara-mc.git)
cd codara-mc
pip install .




(Note: On Windows, ensure you run your terminal as Administrator)

💻 Usage & Examples
Check current adapter status:

```bash
codaramac status -i "Wi-Fi"   # Windows
sudo codaramac status -i eth0 # Linux/macOS
Stealth Mode with Timer (The Ultimate OSINT Feature):
Change MAC and Hostname to a random value, and revert back after 60 seconds:

```bash
codaramac random -i "Wi-Fi" --stealth -t 60
Reset to Original Hardware MAC:

```bash
codaramac reset -i "Wi-Fi"


## 🛠️ Troubleshooting

If you encounter issues while installing or using CodaraMC, try the solutions below.

### 1. Permission Denied

**Problem**

```
Permission denied
```

**Solution**

Run the command with elevated privileges.

```bash
sudo codaramac status -i eth0
```

On Windows, open Command Prompt or PowerShell as **Administrator**.

---

### 2. Interface Not Found

**Problem**

```
Interface not found
```

**Solution**

List available network interfaces and use the correct interface name.

Linux:

```bash
ip link show
```

Windows:

```powershell
netsh interface show interface
```

macOS:

```bash
ifconfig
```

---

### 3. Missing Dependencies

**Problem**

Required commands such as `ip`, `dhclient`, or `macchanger` are missing.

**Solution**

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install iproute2 isc-dhcp-client macchanger
```

Fedora:

```bash
sudo dnf install iproute dhclient macchanger
```

---

### 4. Invalid MAC Address

**Problem**

```
Invalid MAC address format
```

**Solution**

Use a valid MAC address in the format:

```text
00:11:22:33:44:55
```

---

### 5. Network Not Reconnecting

**Problem**

The network connection does not return after changing the MAC address.

**Solution**

Restart the network interface.

Linux:

```bash
sudo dhclient
```

or

```bash
sudo systemctl restart NetworkManager
```

Windows:

Disable and re-enable the adapter from Network Connections.

---

### 6. Reset Does Not Restore Original MAC

Some network drivers do not fully restore the hardware MAC until the adapter or system is restarted.

**Solution**

Restart the network adapter or reboot your computer.

---

### 7. pip install Fails

Upgrade pip before installing.

```bash
python -m pip install --upgrade pip
pip install .
```

If using multiple Python versions:

```bash
python3 -m pip install .
```

---

### 8. Verify Installation

Check that the CLI is installed correctly.

```bash
codaramac --help
```

or

```bash
codaramac --version
```

If the command is not found, ensure your Python Scripts directory is included in your PATH.


🤝 Contributing

Contributions, issues, and feature requests are welcome!
If you are participating in open-source programs, please check our open issues.




