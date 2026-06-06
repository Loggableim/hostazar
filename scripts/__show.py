import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# Print around char 3094 of the inner content
# Inner: stripped[1:-1]
stripped = block.strip()
inner = stripped[1:-1]
print(f'inner[3080:3120]: {inner[3080:3120]!r}')
# So we have: "hostazar.com"}{ with NO comma in between
# This must have been caused by my fix turning },{ into ,{ (regex ate one char too many)
# Original was: }},[{
# After fix: },{
# Should have been: },{
# But somehow we have: }{
# Let me check the raw bytes
print(f'Bytes around: {[hex(ord(c)) for c in inner[3090:3110]]}')
