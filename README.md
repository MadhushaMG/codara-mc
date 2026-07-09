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
```


(Note: On Windows, ensure you run your terminal as Administrator)

💻 Usage & Examples
Check current adapter status:

```bash
codaramac status -i "Wi-Fi"   # Windows
sudo codaramac status -i eth0 # Linux/macOS
Stealth Mode with Timer (The Ultimate OSINT Feature):
Change MAC and Hostname to a random value, and revert back after 60 seconds:
```

```bash
codaramac random -i "Wi-Fi" --stealth -t 60
Reset to Original Hardware MAC:
```

```bash
codaramac reset -i "Wi-Fi"
```


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
If you are participating in open-source programs, please check our open issues.


## 🛡️ Code of Conduct

To help us maintain a welcoming, inclusive, and respectful community, all contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

By participating in this project, you agree to abide by its guidelines and help foster a positive environment for everyone.
