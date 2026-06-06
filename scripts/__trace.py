import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# Obj 0 is from pos 5 to pos 525 (start of next obj)
# Let me look at exactly what comes around pos 515
print(f'around 505-525: {block[505:540]!r}')
# Find the pattern in the first object that has an extra }
# The object should end with one } for author, then the outer }, closing the BlogPosting
# But we see }} meaning the closing is double — one is fine, double means extra
# Let me trace structure of first obj
obj0_start = 5  # starts with [{
# Find matching braces
# But first print the actual content
print('---obj0 (pos 5-525)---')
print(block[5:525])
