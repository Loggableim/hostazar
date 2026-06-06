import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# Try parsing with json5 or with a permissive parser
# First, let me check what's at position 3098 (the error point)
# That should be the START of the 7th object (positions[6] = 3098)
# But positions[5] = 2569 is the start of the 6th object
# So obj 6 spans 3098-3617
# Print obj 6
print('---OBJ 6 (start 3098)---')
print(block[3098:3617])
print()
# Print the transition from obj 5 to obj 6
print('---TRANSITION 5->6 (2569 to 3120)---')
print(block[2569:3120])
