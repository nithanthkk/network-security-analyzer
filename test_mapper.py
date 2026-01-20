from network_mapper import map_network

data = map_network()

if not data:
    print("No active network detected")
else:
    print("Interface:", data["interface"])
    print("Local IP:", data["local_ip"])
    print("Gateway:", data["gateway"])
    print("Subnet:", data["subnet"])
    print("\nConnected Devices:")
    for d in data["devices"]:
        print(d)
