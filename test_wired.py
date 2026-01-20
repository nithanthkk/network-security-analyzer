from scanner_engine import run_nmap_scan, analyze_risk

results = run_nmap_scan("127.0.0.1")

print("Results:")
for r in results:
    print(r, analyze_risk(r["service"]))
