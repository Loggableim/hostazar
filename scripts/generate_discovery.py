#!/usr/bin/env python3
"""Deterministic sitemap and complete RSS from the article registry."""
import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.etree import ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://hostazar.com'
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

def generate(root):
    articles = json.loads((root / 'data/artikel.json').read_text(encoding='utf-8'))
    slugs = [a['slug'] for a in articles]
    if len(slugs) != len(set(slugs)) or not slugs:
        raise ValueError('Empty registry or duplicate slugs')
    for slug in slugs:
        if not re.fullmatch(r'[a-z0-9-]+', slug) or not (root / 'artikel' / (slug + '.html')).is_file():
            raise ValueError('Invalid slug or missing article: ' + slug)
    E.register_namespace('', NS)
    sitemap = E.Element('{' + NS + '}urlset')
    urls = set()
    for path in root.glob('*.html'):
        urls.add(BASE + ('/' if path.name == 'index.html' else '/' + path.name))
    for path in (root / name / 'index.html' for name in ('gaming', 'webhosting', 'ki-llm', 'devops')):
        if not path.is_file():
            continue
        urls.add(BASE + '/' + path.relative_to(root).as_posix())
    urls.discard(BASE + '/404.html')
    urls.update(BASE + '/artikel/' + s + '.html' for s in slugs)
    for url in sorted(urls):
        E.SubElement(E.SubElement(sitemap, '{' + NS + '}url'), '{' + NS + '}loc').text = url
    rss = E.Element('rss', version='2.0')
    ch = E.SubElement(rss, 'channel')
    for tag, value in [('title', 'Hostazar'), ('link', BASE + '/'), ('description', 'Hosting, Gaming und DevOps'), ('language', 'de')]:
        E.SubElement(ch, tag).text = value
    for a in sorted(articles, key=lambda a: (a['date'], a['slug']), reverse=True):
        date = datetime.fromisoformat(a['date']).replace(tzinfo=timezone.utc)
        item = E.SubElement(ch, 'item')
        url = BASE + '/artikel/' + a['slug'] + '.html'
        for tag, value in [('title', a['title']), ('link', url), ('description', a.get('excerpt', '')), ('pubDate', format_datetime(date))]:
            E.SubElement(item, tag).text = value
        E.SubElement(item, 'guid', isPermaLink='true').text = url
    result = {}
    for name, tree in [('sitemap.xml', sitemap), ('feed.xml', rss)]:
        E.indent(tree, space='  ')
        result[name] = E.tostring(tree, encoding='utf-8', xml_declaration=True) + b'\n'
    return result, len(slugs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result, count = generate(ROOT)
    stale = []
    for name, content in result.items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_bytes() != content:
                stale.append(name)
        else:
            path.write_bytes(content)
    print(f'Registry articles: {count}; sitemap article URLs: {count}; RSS items: {count}')
    if stale:
        raise SystemExit('Stale discovery files: ' + ', '.join(stale))
