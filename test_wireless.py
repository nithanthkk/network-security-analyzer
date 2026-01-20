from wireless_engine import run_wireless_scan

results = run_wireless_scan()

for net in results:
    print(net)
