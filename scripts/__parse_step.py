import re, json
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# The error was at char 3098: "name": "hostazar.com"  },{"@context"
# That's:  "}  then ",{"" -- valid
# BUT the JSON parser might be confused by the structure of the array element after
# Let me parse step by step
# Find each BlogPosting object via regex
posts = re.findall(r'\{\\"@context\\":\s*\\"https://schema.org\\".*?\\"author\\":\s*\{\\"@type\\":\s*\\"Organization\\",\s*\\"name\\":\s*\\"hostazar.com\\"\\}\}', block)
print(f'Found {len(posts)} posts via regex')
# Try to split the array manually
import re
stripped = block.strip()
# Strip outer [ and ]
if stripped.startswith('[') and stripped.endswith(']'):
    inner = stripped[1:-1]
    print(f'Inner length: {len(inner)}')
    # Split on `}, {` and `},{`
    parts = re.split(r'\},\s*\{', inner)
    print(f'Parts: {len(parts)}')
    for i, p in enumerate(parts):
        wrapped = '{' + p + '}'
        if not p.startswith('{'):
            wrapped = '{' + p
        if not p.endswith('}'):
            wrapped = p + '}'
        wrapped = '{' + p.strip().lstrip('{').rstrip('}') + '}'
        try:
            obj = json.loads(wrapped)
            print(f'  Part {i}: OK - {obj.get("headline", "")[:50]}')
        except json.JSONDecodeError as e:
            print(f'  Part {i}: FAIL at {e.pos}: ...{wrapped[max(0,e.pos-30):e.pos+30]}...')
            break
