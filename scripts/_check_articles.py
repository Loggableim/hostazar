import re, os
files = ['artikel/cloudflare-waf-einrichten-2026.html', 'artikel/discord-bot-vps-hosten-2026.html', 'artikel/palworld-server-mods-guide-2026.html']
base = r'C:\HermesPortable\home\scripts\blog-automation\hostazar'
for f in files:
    path = os.path.join(base, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text)
    words = len(text.split())
    has_affiliate = 'nova079-20' in content
    has_h2 = content.count('<h2>')
    has_hero = 'hero-image' in content
    has_jsonld = 'application/ld+json' in content
    print(f'{f}: {words} words, {has_h2} H2, affiliate={has_affiliate}, hero={has_hero}, JSON-LD={has_jsonld}')
