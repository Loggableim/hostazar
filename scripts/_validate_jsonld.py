"""Validate the JSON-LD array in index.html parses correctly."""
import re, os, json
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
# Find the BlogPosting array
m = re.search(r'<script type="application/ld\+json">\s*(\[.*?\])\s*</script>', content, re.DOTALL)
if not m:
    print("FAIL: No JSON-LD array found")
    raise SystemExit(1)
raw = m.group(1)
# Try to parse
try:
    data = json.loads(raw)
    print(f"OK: JSON-LD array has {len(data)} entries")
    # Check for our 3 new ones
    urls = [e.get('url','') for e in data]
    for slug in ['cloudflare-waf-einrichten-2026.html', 'discord-bot-vps-hosten-2026.html', 'palworld-server-mods-guide-2026.html']:
        found = any(slug in u for u in urls)
        print(f"  {'OK' if found else 'MISS'}: {slug}")
except Exception as e:
    print(f"FAIL parse: {e}")
    print(f"First 200 chars: {raw[:200]}")
