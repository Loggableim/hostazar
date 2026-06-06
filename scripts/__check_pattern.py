import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# The original `}},[{` became `},{` after first fix, but the comma is in wrong place
# Should be `}},{"` but my fix produced `},{` (correct for inside array) which is right
# But the file has `},{` "},{` which is "name": "..."},{  (good), then "{..." (missing comma in between? no, the comma is the {)
# Actually the right format is `}},{"` (close then open with comma)
# Let me check what it looks like now
print('---PATTERN 1:  }},{ ---')
idx = block.find('}},{"')
if idx > 0:
    print(f'Found at {idx}: ...{block[idx-20:idx+30]}...')
# Actually my earlier fix turned `}},[{` into `},{` (replaced `}},[{` with `},{`)
# But that should have made: "name": "hostazar.com"}},[{... -> "name": "hostazar.com"},{...  ← missing one `,` and one `}`
# Let me see
print('---')
print(block[3080:3120])
