import socket
import ipaddress
from datetime import datetime
import sys

# ==============================
# USER INPUT
# ==============================
target_input = input("Enter target IP or Hostname: ").strip()

# ==============================
# VALIDATE IP / HOSTNAME
# ==============================
try:
    # If it's a valid IP
    ipaddress.ip_address(target_input)
    target_ip = target_input
except ValueError:
    # Try resolving hostname
    try:
        target_ip = socket.gethostbyname(target_input)
        print(f"[i] Resolved {target_input} → {target_ip}")
    except socket.gaierror:
        print("❌ Invalid IP address or hostname")
        sys.exit()

# Common ports to scan
ports = [21, 22, 23, 80, 443, 8080]

# Port to service mapping
services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    80: "HTTP",
    443: "HTTPS",
    8080: "HTTP-Alt"
}

# Risk levels for services
risks = {
    "FTP": "HIGH",
    "Telnet": "HIGH",
    "SSH": "MEDIUM",
    "HTTP": "MEDIUM",
    "HTTPS": "LOW",
    "HTTP-Alt": "MEDIUM",
    "Unknown Service": "UNKNOWN"
}

print(f"\nStarting scan on {target_ip}\n")

open_ports = []

# ==============================
# PORT SCANNING
# ==============================
for port in ports:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target_ip, port))

        if result == 0:
            service = services.get(port, "Unknown Service")
            risk = risks.get(service, "UNKNOWN")
            print(f"[+] Port {port} OPEN → {service} | Risk: {risk}")
            open_ports.append((port, service, risk))
        else:
            print(f"[-] Port {port} CLOSED")

        s.close()

    except KeyboardInterrupt:
        print("\n❌ Scan interrupted by user")
        sys.exit()

    except socket.error:
        print(f"[!] Error scanning port {port}")

print("\nScan Completed")

# ==============================
# REPORT GENERATION
# ==============================
with open("report.txt", "w") as file:
    file.write("Network Scanner & Security Analyzer Report\n")
    file.write("==========================================\n")
    file.write(f"Target       : {target_input}\n")
    file.write(f"Resolved IP  : {target_ip}\n")
    file.write(f"Scan Time    : {datetime.now()}\n\n")

    if open_ports:
        file.write("Open Ports & Security Analysis:\n")
        file.write("--------------------------------\n")
        for port, service, risk in open_ports:
            file.write(f"Port {port} → {service} | Risk Level: {risk}\n")
    else:
        file.write("No open ports detected.\n")

print("📄 Report saved as report.txt")
