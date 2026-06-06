import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# Check obj 0 and obj 1 boundaries
# Obj 0: 5 to 525, has "hostazar.com"}}
# Then `,\n   {` for obj 1
# So between obj 0 and obj 1, we have: "hostazar.com"}},\n   {"
# That is: } (close author) + } (close BlogPosting) + } (extra?) + , + \n + { (open obj 1)
# Wait no, let me count
# "hostazar.com" } } } , { 
# Author close + BlogPosting close + ??? (extra)
# So there's an extra } somewhere
# Let me look at it char by char
obj0_end = block.find('"author"', 5)
print(f'author starts at: {obj0_end}')
# Find the author object close
# The author obj is `{"@type": "Organization", "name": "hostazar.com"}` 
# So after `hostazar.com"` we have `}` (close author)
# Then the outer BlogPosting obj should have `}` (close)
# Then `,` for next obj
# We see: "hostazar.com"}} — that's 2 closing braces
# After that there's `,\n` which is the array separator
# So the structure is: } (author) + } (BlogPosting) = 2, that's CORRECT
# Then , separates to next array element
# So "hostazar.com"}}, is: } (close author) + } (close BlogPosting) + , (array separator) = 3 chars
# Looking at the dump: "hostazar.com"}}, <- we have "hostazar.com"}}},
# Let me count the braces
sample = block[510:530]
print(f'sample bytes: {[c for c in sample]!r}')
