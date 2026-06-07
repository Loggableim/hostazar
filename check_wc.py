#!/usr/bin/env python3
import re, sys

with open(r'C:\HermesPortable\home\scripts\blog-automation\hostazar\artikel\nvidia-jetson-ki-am-edge-llm-embedded-2026.html', 'r') as f:
    html = f.read()

match = re.search(r'<div class="article-content">(.*?)</div>\s*<div class="affiliate-box"', html, re.DOTALL)
if match:
    content = match.group(1)
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'&amp;|&lt;|&gt;|&mdash;|&nbsp;|&#8211;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = len(text.split())
    chars = len(text)
    print(f'Content words: {words}')
    print(f'Content chars: {chars}')
else:
    print('Pattern not found')
    # Find article-content positions
    for m in re.finditer(r'article-content', html):
        ctx = html[max(0,m.start()-50):m.start()+100]
        print(f'Found at {m.start()}: ...{ctx}...')
