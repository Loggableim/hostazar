import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
print(f'Block length: {len(block)}')
# Print area around char 3094
print('---around 3094---')
print(block[3070:3150])
# Try to parse
import json
try:
    data = json.loads(block)
    print(f'OK: {len(data)} entries')
except json.JSONDecodeError as e:
    print(f'Error: {e}')
    print(f'Position char {e.pos}: ...{block[max(0,e.pos-30):e.pos+30]}...')
