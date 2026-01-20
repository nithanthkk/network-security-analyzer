import subprocess
import csv
import time
import os

CSV_FILE = "wireless_scan-01.csv"
INTERFACE = "wlan0"
MON_INTERFACE = "wlan0"


def enable_monitor_mode():
    subprocess.run(
        ["sudo", "airmon-ng", "start", INTERFACE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def disable_monitor_mode():
    subprocess.run(
        ["sudo", "airmon-ng", "stop", MON_INTERFACE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def run_wireless_scan(duration=10):
    """
    Automatically enables monitor mode,
    runs airodump-ng, then disables monitor mode.
    """

    enable_monitor_mode()
    time.sleep(2)

    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)

    command = [
        "sudo", "airodump-ng",
        "--output-format", "csv",
        "--write", "wireless_scan",
        MON_INTERFACE
    ]

    process = subprocess.Popen(command)
    time.sleep(duration)
    process.terminate()

    networks = parse_csv()

    disable_monitor_mode()

    return networks


def parse_csv():
    networks = []

    if not os.path.exists(CSV_FILE):
        return networks

    with open(CSV_FILE, newline="", encoding="utf-8", errors="ignore") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) < 14:
                continue
            if row[0].strip() in ("BSSID", ""):
                continue

            networks.append({
                "bssid": row[0].strip(),
                "channel": row[3].strip(),
                "power": row[8].strip(),
                "encryption": row[5].strip(),
                "ssid": row[13].strip()
            })

    return networks
