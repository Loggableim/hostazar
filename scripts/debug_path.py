"""Debug: check where file was saved"""
import os

paths = [
    "/c/HermesPortable/hostazar/images/jitsi-meet-server-vps-2026.png",
    "C:\\HermesPortable\\hostazar\\images\\jitsi-meet-server-vps-2026.png",
    os.path.join(os.getcwd(), "images", "jitsi-meet-server-vps-2026.png") if os.getcwd() else "",
]

for p in paths:
    if not p:
        continue
    print(f"Path: {p}")
    print(f"  Exists: {os.path.exists(p)}")
    if os.path.exists(p):
        print(f"  Size: {os.path.getsize(p)}")
    print()

# Also search
print("Current dir:", os.getcwd())
for root, dirs, files in os.walk("/c/HermesPortable/hostazar/images"):
    for f in files:
        if "jitsi" in f.lower():
            print(f"FOUND: {os.path.join(root, f)}")