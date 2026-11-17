#!/usr/bin/env python3
"""Strict HTML quality gates; Python standard library only."""
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.opens, self.closes = Counter(), Counter()
        self.title, self.description, self.links = [], [], []
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.opens[tag] += 1
        if tag == 'title':
            self.in_title = True
        if tag == 'meta' and a.get('name', '').lower() == 'description':
            self.description.append(a.get('content', '').strip())
        if tag == 'a':
            self.links.append((a.get('href', ''), set(a.get('rel', '').lower().split())))
    def handle_endtag(self, tag):
        self.closes[tag] += 1
        if tag == 'title':
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)

def audit(root):
    errors = []
    articles = sorted((root / 'artikel').glob('*.html'))
    if not articles:
        errors.append('No article HTML files')
    for path in sorted(root.glob('*.html')) + articles:
        p = Page()
        p.feed(path.read_text(encoding='utf-8'))
        issues = []
        for tag in ('main', 'h1'):
            if p.opens[tag] != p.closes[tag]:
                issues.append(f'{tag} unbalanced: {p.opens[tag]}/{p.closes[tag]}')
        if path in articles:
            if p.opens['h1'] != 1:
                issues.append(f'H1 count {p.opens["h1"]}')
            title = ' '.join(''.join(p.title).split())
            if p.opens['title'] != 1 or not 50 <= len(title) <= 60:
                issues.append(f'Title length {len(title)} (required 50–60)')
            if len(p.description) != 1 or not 120 <= len(p.description[0]) <= 155:
                issues.append('Description missing/duplicate or outside 120–155')
            targets = set()
            for href, rel in p.links:
                u = urlsplit(urljoin('https://hostazar.com/artikel/' + path.name, href))
                host = (u.hostname or '').lower()
                if (host == 'amzn.to' or host.endswith('.amzn.to') or
                    host == 'amazon.de' or host.endswith('.amazon.de') or
                    host == 'amazon.com' or host.endswith('.amazon.com')):
                    if not {'sponsored', 'nofollow'} <= rel:
                        issues.append('Amazon link missing sponsored nofollow')
                if host == 'hostazar.com' and u.path.startswith('/artikel/') and u.path.endswith('.html'):
                    target = root / u.path.lstrip('/')
                    if target.is_file() and target.resolve() != path.resolve():
                        targets.add(u.path)
            if len(targets) < 2:
                issues.append(f'Only {len(targets)} distinct existing internal article links')
        errors.extend(f'{path.relative_to(root)}: {issue}' for issue in issues)
    for error in errors:
        print('ERROR ' + error)
    print(f'Articles: {len(articles)}; violations: {len(errors)}; exitcode: {int(bool(errors))}')
    return int(bool(errors))

if __name__ == '__main__':
    sys.exit(audit(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT))
