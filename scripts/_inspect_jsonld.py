import re
with open(r'C:\HermesPortable\home\scripts\blog-automation\hostazar\index.html', 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'<script type="application/ld\+json">', content)
start = m.end()
end = content.find('</script>', start)
print(f'JSON-LD length: {end - start} chars')
print('---FIRST 500---')
print(content[start:start+500])
print('---LAST 500---')
print(content[end-500:end])
