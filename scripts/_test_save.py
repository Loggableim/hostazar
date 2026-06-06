"""Test if PIL save works at the path."""
import os
from PIL import Image

paths = [
    r"C:\HermesPortable\hostazar\images\cloudflare-waf-einrichten-2026.png",
    r"C:\HermesPortable\images\discord-bot-vps-hosten-2026.png",
]
for p in paths:
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img = Image.new('RGB', (1216, 640), '#0a0e27')
        img.save(p, 'PNG')
        print(f"OK: {p} ({os.path.getsize(p)} bytes)")
    except Exception as e:
        print(f"FAIL {p}: {e}")
