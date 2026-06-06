import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
# The original pattern is: "hostazar.com"}}],[{"@context"
# That's: }} (close author+BlogPosting) ,[ (start new array) {"@context"
# To fix: just remove the [ so it becomes: "hostazar.com"}},{"@context"
fixed = re.sub(r'(hostazar\.com"\})\},\[\{(?="@context")', r'\1},{"', content)
# Verify the change
print(f'Made change: {fixed != content}')
with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed)
# Validate
import json
m = list(re.finditer(r'<script type="application/ld\+json">', content))
start = m[1].end()
end = content.find('</script>', start)
block = content[start:end]
print(f'Original block parse test...')
try:
    data = json.loads(block)
    print(f'OK: {len(data)} entries')
except json.JSONDecodeError as e:
    print(f'Original error: {e}')
# Re-validate the FIXED file
with open(path, 'r', encoding='utf-8') as f:
    new_content = f.read()
m = list(re.finditer(r'<script type="application/ld\+json">', new_content))
start = m[1].end()
end = new_content.find('</script>', start)
block = new_content[start:end]
try:
    data = json.loads(block)
    print(f'FIXED OK: {len(data)} entries')
except json.JSONDecodeError as e:
    print(f'FIXED error: {e}')
    print(f'Context: ...{block[max(0,e.pos-30):e.pos+30]!r}...')
