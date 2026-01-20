import subprocess
import re


def run_cmd(command):
    """
    Run a shell command and return output safely
    """
    try:
        return subprocess.check_output(command, stderr=subprocess.DEVNULL).decode()
    except Exception:
        return ""


def get_default_interface():
    """
    Get active network interface
    """
    output = run_cmd(["ip", "route"])
    for line in output.splitlines():
        if line.startswith("default"):
            return line.split()[4]
    return None


def get_local_ip(interface):
    """
    Get local IP address of interface
    """
    output = run_cmd(["ip", "addr", "show", interface])
    match = re.search(r"inet (\d+\.\d+\.\d+\.\d+/\d+)", output)
    return match.group(1) if match else None


def get_gateway():
    """
    Get default gateway IP
    """
    output = run_cmd(["ip", "route"])
    for line in output.splitlines():
        if line.startswith("default"):
            return line.split()[2]
    return None


def get_subnet():
    """
    Get subnet CIDR
    """
    output = run_cmd(["ip", "route"])
    for line in output.splitlines():
        if "proto kernel" in line:
            return line.split()[0]
    return None


def arp_scan(subnet):
    """
    Discover devices using ARP scan
    """
    devices = []

    output = run_cmd(["ip", "neigh"])
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[0].count(".") == 3:
            devices.append({
                "ip": parts[0],
                "mac": parts[4],
                "state": parts[5] if len(parts) > 5 else "UNKNOWN"
            })

    return devices


def map_network():
    """
    Main network mapping function
    """
    interface = get_default_interface()
    if not interface:
        return None

    return {
        "interface": interface,
        "local_ip": get_local_ip(interface),
        "gateway": get_gateway(),
        "subnet": get_subnet(),
        "devices": arp_scan(get_subnet())
    }
