#!/usr/bin/env python3
"""Count words in article - more robust version."""
import re, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    html = f.read()
# Count all text between body tags, removing HTML tags
body_match = re.search(r'<div class="article-content">(.*?)</div>\s*<!-- Related Articles -->', html, re.DOTALL)
if not body_match:
    body_match = re.search(r'<div class="article-content">(.*?)</div>', html, re.DOTALL)
if body_match:
    content = body_match.group(1)
    # Remove code blocks
    content = re.sub(r'<pre[^>]*>.*?</pre>', ' ', content, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', content)
    words = len([w for w in text.split() if any(c.isalpha() for c in w)])
    print(f"Article word count: {words}")
else:
    print("ERROR: Could not find article-content div")
    # Debug: show what comes after "article-content"
    idx = html.find('article-content')
    if idx > 0:
        print(f"Found 'article-content' at position {idx}")
        print(f"Context: ...{html[idx-50:idx+200]}...")
    else:
        print("'article-content' not found in HTML!")
