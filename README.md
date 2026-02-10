 Network Security Analyzer

Wired & Wireless Reconnaissance Tool**



📌 Overview

Network Security Analyzer** is a Python-based cybersecurity reconnaissance tool designed to perform **ethical wired and wireless network analysis** through a unified graphical interface.

The project integrates real-world security tools such as Nmap, airodump-ng, and **ARP-based network mapping, following correct networking principles and ethical boundaries.

This project focuses on **learning by building**, not automation of attacks.



⚙️ Features

Wired Reconnaissance (Nmap)

- TCP connect scanning (`sT`)
- IPv4 and CIDR subnet support
- Open port and service enumeration
- Basic service risk classification

Wireless Reconnaissance (Passive)

- Nearby Wi-Fi network discovery
- SSID, BSSID, channel, encryption, and signal power detection
- Passive scanning only (no injection or attacks)

Network Mapping

- Gateway detection
- Subnet identification
- Connected device discovery via ARP
- IP, MAC, and device state enumeration

 User Interface

- Dark-themed GUI
- Separate wired and wireless workflows
- Real-time terminal-style output
- Clear scan controls

---

 🔌 Hardware Requirement (Important)

⚠️ **Wireless scanning requires an external Wi-Fi adapter that supports monitor mode.**

- Internal laptop Wi-Fi cards usually **do not support monitor mode**
- Tools like `airodump-ng` require a compatible external adapter
- Example: USB Wi-Fi adapters with monitor-mode support (e.g., Alfa adapters)

Without a compatible external adapter:

- Wired scanning and network mapping will still work
- Wireless scanning will **not function**



 🧠 Architecture


Network_scanner/
│
├── gui.py                # User Interface
├── scanner_engine.py     # Wired Nmap scanning
├── wireless_engine.py    # Wireless reconnaissance
├── network_mapper.py     # Internal network mapping



Each module is independent and easy to extend.



 ▶ Usage

bash
sudo ./venv/bin/python gui.py



 Wired Scan

1. Enter IP address or subnet
2. Click **Start Wired Scan**

 Wireless Scan

1. Connect external Wi-Fi adapter
2. Enable monitor mode
3. Click **Start Wireless Scan**

Network Mapping

1. Connect to a network manually
2. Click **Map Current Network**



 ⚠️ Ethical Use Notice

This tool is intended for:

- Educational use
- Authorized security testing
- Network auditing with permission

Unauthorized scanning or monitoring is illegal.



 📌 Project Status

Version 1.0 – Stable (Foundational Project)

