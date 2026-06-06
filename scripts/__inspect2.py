import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
# Find the second application/ld+json block (BlogPosting array)
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
print(f'Found {len(matches)} JSON-LD blocks')
if len(matches) >= 2:
    start = matches[1].end()
    end = content.find('</script>', start)
    block = content[start:end].strip()
    print(f'Block length: {len(block)}')
    # Try to fix
    # 1) Remove leading line breaks
    # 2) The pattern `}},[{"` should be `},{` to keep one array
    # 3) Make sure the block starts with `[` and ends with `]`
    print('---START (first 200)---')
    print(block[:200])
    print('---END (last 200)---')
    print(block[-200:])
