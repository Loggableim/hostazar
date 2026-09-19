#!/usr/bin/env python3
"""Light build: rebuild index.html, category pages and sitemap.xml from
data/artikel.json — WITHOUT re-rendering article pages.

Why light: the full build_megapage_v2.py re-renders every article and
regresses post-build patches (FAQ/HowTo JSON-LD, .webp image refs,
wordCount). Articles are maintained additively; only the catalog surfaces
(index, category pages, sitemap) are regenerated here.

Run: python scripts/light_build.py
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_megapage_v2 as bm  # noqa: E402  (reads data/artikel.json at import)

def main():
    print(f'Light build — {len(bm.ARTIKEL)} Artikel im Katalog', file=sys.stderr)
    bm.build_index()
    for cat in bm.KATEGORIEN:
        bm.build_category(cat)
    bm.build_sitemap()
    print('Light build fertig.', file=sys.stderr)

if __name__ == '__main__':
    main()
