import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# pos 3098 is: "hostazar.com"  }  ,  {  "  @  c
# 3098 in the array means position 3098 of the block
# The block is: [obj1, obj2, obj3, ...]
# Position 0 is [
# So pos 3098 is inside the array
# We see "},{" at 3098-3101 area
# But "},{" IS valid! Let me check if maybe the `{"@type": "Organization", "name": "hostazar.com"}` has missing closing brace before next object's {
# Looking at the context, after "name": "hostazar.com"} we have ,{"@context"
# That's: },{" — close obj, comma, open obj → VALID
# So error must be IN the next object
# Let me extract the next object starting at pos 3100
s = 3100
print(f'Next 400 chars: {block[s:s+400]!r}')
