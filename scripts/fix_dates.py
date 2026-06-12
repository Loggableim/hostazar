#!/usr/bin/env python3
"""Fix all future dates in artikel.json and HTML files to not exceed 2026-06-11."""
import json, os, re, glob

REPO = r'C:\HermesPortable\home\scripts\blog-automation\hostazar'
ARTIKEL_JSON = os.path.join(REPO, 'data', 'artikel.json')
ARTIKEL_DIR = os.path.join(REPO, 'artikel')
MAX_DATE = '2026-06-11'

# 1. Fix artikel.json
with open(ARTIKEL_JSON, encoding='utf-8') as f:
    data = json.load(f)

fixed_count = 0
for a in data:
    d = a.get('date', '')
    if d > MAX_DATE:
        print(f"  FIX artikel.json: {a['slug']}: {d} -> {MAX_DATE}")
        a['date'] = MAX_DATE
        fixed_count += 1

with open(ARTIKEL_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"Fixed {fixed_count} dates in artikel.json")

# 2. Fix HTML files
html_fixed = 0
for path in glob.glob(os.path.join(ARTIKEL_DIR, '*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    
    # Fix datePublished and dateModified in JSON-LD
    # Pattern: "datePublished": "2026-06-15"
    def fix_date_field(m):
        field = m.group(1)
        date_val = m.group(2)
        if date_val > MAX_DATE:
            return f'"{field}": "{MAX_DATE}"'
        return m.group(0)
    
    content = re.sub(
        r'"(datePublished|dateModified|date)":\s*"(\d{4}-\d{2}-\d{2})"',
        fix_date_field,
        content
    )
    
    # Fix dates in meta content attributes: content="2026-06-15"
    def fix_meta_date(m):
        date_val = m.group(1)
        if date_val > MAX_DATE:
            return f'content="{MAX_DATE}"'
        return m.group(0)
    
    content = re.sub(
        r'content="(\d{4}-\d{2}-\d{2})"',
        fix_meta_date,
        content
    )
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        html_fixed += 1
        slug = os.path.splitext(os.path.basename(path))[0]
        print(f"  FIX HTML: {slug}")

print(f"Fixed {html_fixed} HTML files")
print("Done!")
