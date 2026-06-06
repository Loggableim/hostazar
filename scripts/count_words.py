"""Count words in the palworld article."""
import re
import sys

with open(r'C:\HermesPortable\home\scripts\blog-automation\hostazar\artikel\palworld-server-mods-guide-2026.html', 'r', encoding='utf-8') as f:
    html = f.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'&[a-zA-Z]+;', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()
words = text.split()
print(f'WOERTER={len(words)}')
print(f'ZEICHEN={len(text)}')
