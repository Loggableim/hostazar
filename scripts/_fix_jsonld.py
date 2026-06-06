import re
path = r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
matches = list(re.finditer(r'<script type="application/ld\+json">', content))
start = matches[1].end()
end = content.find('</script>', start)
block = content[start:end]
# Find the broken `}},[{` pattern
broken = block.find('}},[{')
print(f'broken pattern at offset: {broken}')
print(f'context: ...{block[broken-30:broken+50]}...')
# Find all broken patterns
all_broken = [m.start() for m in re.finditer(r'\}\},\[\{', block)]
print(f'All broken patterns: {all_broken}')
# Try to fix
fixed = re.sub(r'\}\},\[\{', '},{', block)
# Re-write the file
new_content = content[:start] + fixed + content[end:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Fixed and saved')
