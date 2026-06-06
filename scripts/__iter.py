import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# Try regex-extracting objects one at a time
# Find each object starting with {"@context"
positions = [m.start() for m in re.finditer(r'\{"@context"', block)]
print(f'Object starts: {positions}')
# How many objects?
print(f'Number of objects: {len(positions)}')
# For each pair, try to parse the object
import json
# Find author close - the object ends with `"name": "hostazar.com"}` (within the author object)
# Then maybe has more text until `},{` or `}]`
for i, p in enumerate(positions):
    if i + 1 < len(positions):
        next_p = positions[i+1]
    else:
        next_p = len(block) - 1
    # The end of this object should be at the last `}` before the next `,` or before the final `]`
    # Find the next `}}` after position p
    end_search = block.find('"}]}', p)  # author + object close + array close
    if end_search > 0 and end_search < next_p:
        end_pos = end_search + 4
    else:
        # find `}},{"` or `}]` or `}}` + comma
        end_pos = block.find('},{', p) + 3
        if end_pos <= 2:
            end_pos = block.find('}]', p) + 2
    obj_str = block[p:end_pos]
    try:
        obj = json.loads(obj_str)
        print(f'  Obj {i}: OK ({len(obj_str)} chars) - {obj.get("headline","")[:50]}')
    except json.JSONDecodeError as e:
        print(f'  Obj {i}: FAIL at {e.pos}: {obj_str[max(0,e.pos-30):e.pos+30]!r}')
        break
