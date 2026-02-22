import json

with open(r'practice_4/json/sample-data.json', 'r') as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 50 + " " + "-" * 20 + " " + "-" * 7 + " " + "-" * 6)


interfaces = data.get("imdata", [])


for item in interfaces:
    attr = item.get("l1PhysIf", {}).get("attributes", {})
    
    dn = attr.get("dn", "")
    descr = attr.get("descr", "")
    speed = attr.get("speed", "")
    mtu = attr.get("mtu", "")
    
    print(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<6}")