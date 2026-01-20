import nmap


def analyze_risk(service):
    service = service.lower()
    if service in ["ftp", "telnet"]:
        return "HIGH"
    elif service in ["ssh", "http"]:
        return "MEDIUM"
    return "LOW"


def run_nmap_scan(target):
    """
    Runs a basic TCP connect scan using nmap.
    Works on localhost, IPv4, and subnets.
    """

    nm = nmap.PortScanner()

    # -sT = TCP connect scan (safe, works without raw sockets)
    # -Pn = skip host discovery (important for localhost)
    # --top-ports 100 = fast but useful
    scan_args = "-sT -Pn --top-ports 100"

    try:
        nm.scan(hosts=target, arguments=scan_args)
    except Exception as e:
        raise RuntimeError(f"Nmap scan failed: {e}")

    results = []

    for host in nm.all_hosts():
        if "tcp" not in nm[host]:
            continue

        for port, port_data in nm[host]["tcp"].items():
            if port_data["state"] == "open":
                results.append({
                    "host": host,
                    "port": port,
                    "service": port_data.get("name", "unknown"),
                    "version": port_data.get("version", "")
                })

    return results
