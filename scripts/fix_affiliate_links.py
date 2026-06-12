#!/usr/bin/env python3
"""Add rel='sponsored' to affiliate links (Amazon tag=nova079-20)."""
import glob, os, re

REPO = r'C:\HermesPortable\home\scripts\blog-automation\hostazar'
ARTIKEL_DIR = os.path.join(REPO, 'artikel')

fixed = 0
for path in glob.glob(os.path.join(ARTIKEL_DIR, '*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    
    # Fix 1: rel="nofollow noopener" -> rel="nofollow noopener sponsored"
    content = content.replace(
        'rel="nofollow noopener"',
        'rel="nofollow noopener sponsored"'
    )
    
    # Fix 2: rel="nofollow noopener sponsored" (already has sponsored, skip)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1

print(f"Fixed affiliate links in {fixed} HTML files")
