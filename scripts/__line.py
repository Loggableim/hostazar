import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# I see the issue. The first object ends with "name": "hostazar.com"}
# Then there's ,{"@context":... for the second object
# But the second object has "VPS mieten 2026" which is the OLD entry
# Wait - the error said position 3098 expecting property name
# That means the parser found a } before position 3098 that closed a containing object
# And the next char at 3098 was { but it's not a property name
# Actually maybe my fix script broke a different thing
# Let me check the original commit to see if my insertion broke it
# First, find which is the 3098 area
print(f'len: {len(block)}')
# Try incremental parsing
import json
# Replace any unescaped newlines that might be in strings
# Check line numbers
line = 1
col = 1
for i, c in enumerate(block):
    if c == '\n':
        line += 1
        col = 1
    else:
        col += 1
    if i == 3098:
        print(f'Pos 3098: line {line} col {col}: char before: {block[i-5:i+5]!r}')
        break
