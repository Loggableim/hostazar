import re
with open(r'C:\HermesPortable\home\scripts\blog-automation\hostazar\artikel\comfyui-auf-gpu-hosten.html', 'r', encoding='utf-8') as f:
    c = f.read()
start = c.find('class="article-content"')
end = c.find('<!-- Related Articles -->', start)
if start > 0 and end > 0:
    text = c[start:end]
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    words = len(clean.split())
    print(f'Article content word count: {words}')
else:
    print('Could not find section boundaries')
