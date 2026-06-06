import re, json
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# Try to parse
try:
    data = json.loads(block)
    print(f'OK: {len(data)} entries')
    for d in data:
        print(f"  - {d.get('headline','')[:60]}")
except json.JSONDecodeError as e:
    print(f'Error at line {e.lineno} col {e.colno} pos {e.pos}')
    # Show context
    s = max(0, e.pos - 50)
    print(f'Context: ...{block[s:e.pos+50]!r}...')
