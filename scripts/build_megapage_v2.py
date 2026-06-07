#!/usr/bin/env python3
"""
hostazar.com — Mega Portal Static Site Generator v2
=====================================================
Rendert alle Seiten aus Templates + artikel.json

Features:
  - JSON-LD BlogPosting pro Artikel
  - BreadcrumbList Schema auf jeder Seite
  - Article-Schema mit wordCount, dateModified, image
  - Responsive images mit loading="lazy"
  - Canonical URLs konsistent
  - lastmod in sitemap.xml wird auf Artikel-Datum gesetzt
  - Touch-freundliches Mega Menu
  - Cookie Consent Banner
  - AdSense Platzhalter

Usage:
  cd hostazar.com && python scripts/build_megapage_v2.py
"""
import json, os, re, sys, datetime, html as html_mod

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE_URL = 'https://hostazar.com'
SITE_NAME = 'hostazar.com'
SITE_DESC = 'Hosting- und Server-Blog mit Guides zu Gameserver-Miete, Webhosting, VPS und DevOps-Tools. Produktvergleiche und Tutorials auf Deutsch.'

with open(os.path.join(BASE, 'data', 'artikel.json'), encoding='utf-8') as f:
    ARTIKEL = json.load(f)
with open(os.path.join(BASE, 'data', 'kategorien.json'), encoding='utf-8') as f:
    KATEGORIEN = json.load(f)

# ── Helpers ──────────────────────────────────────────────────────────────────

def h(s):
    t = str(s)
    # First unescape any existing entities, then re-escape
    t = t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&ndash;', '–').replace('&mdash;', '—')
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def article_url(slug):
    return SITE_URL + '/artikel/' + slug + '.html'

def article_path(slug):
    return os.path.join(BASE, 'artikel', slug + '.html')

def cat_url(cat):
    return SITE_URL + '/' + cat + '/'

def make_cat_groups():
    groups = {}
    for a in ARTIKEL:
        cat = a.get('category', 'devops')
        groups.setdefault(cat, []).append(a)
    for k in groups:
        groups[k].sort(key=lambda a: a.get('date', '') or '', reverse=True)
    return groups

CAT_GROUPS = make_cat_groups()

# ── Base page shell ──────────────────────────────────────────────────────────

def page_shell(title, desc, canonical, body_html,
               og_type='website', og_image=None,
               page_type='other', jsonld_blocks=None,
               extra_head='', article_html=None, article_meta=None):
    """Build a full HTML page from a standardized scaffold."""

    if og_image is None:
        og_image = SITE_URL + '/images/ollama-llm-server-vps-2026.png'

    jsonld = []

    # 1) Main schema
    if page_type == 'article':
        schema_obj = {
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': title,
            'url': canonical,
            'description': desc,
            'inLanguage': 'de',
            'isPartOf': {'@type': 'WebSite', 'name': SITE_NAME, 'url': SITE_URL},
        }
        if article_meta:
            am = article_meta
            if am.get('date'):
                schema_obj['datePublished'] = am['date']
                schema_obj['dateModified'] = am.get('date', am['date'])
            if am.get('image'):
                schema_obj['image'] = SITE_URL + '/images/' + am['image']
            if am.get('excerpt'):
                schema_obj['description'] = am['excerpt']
        schema_obj['author'] = {'@type': 'Organization', 'name': SITE_NAME}
        schema_obj['publisher'] = {'@type': 'Organization', 'name': SITE_NAME}
        if article_html:
            text = re.sub(r'<[^>]+>', ' ', article_html)
            schema_obj['wordCount'] = len(text.split())
        jsonld.append(('application/ld+json', schema_obj))
    elif page_type == 'legal':
        jsonld.append(('application/ld+json', {
            '@context': 'https://schema.org',
            '@type': 'WebPage',
            'name': title,
            'url': canonical,
            'description': desc,
            'inLanguage': 'de',
        }))
    else:
        jsonld.append(('application/ld+json', {
            '@context': 'https://schema.org',
            '@type': 'WebSite',
            'name': SITE_NAME,
            'url': SITE_URL,
            'description': SITE_DESC,
            'inLanguage': 'de',
            'publisher': {'@type': 'Organization', 'name': SITE_NAME},
        }))

    # 2) BreadcrumbList
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': SITE_URL + '/'}]
    if page_type == 'article' and article_meta and article_meta.get('category'):
        cat_key = article_meta['category']
        cat_info = KATEGORIEN.get(cat_key, {})
        cat_name = cat_info.get('name', cat_key.title())
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': cat_name, 'item': SITE_URL + '/' + cat_key + '/'})
        crumbs.append({'@type': 'ListItem', 'position': 3, 'name': title, 'item': canonical})
    elif page_type == 'category' and article_meta and article_meta.get('cat'):
        cat_key = article_meta['cat']
        cat_info = KATEGORIEN.get(cat_key, {})
        cat_name = cat_info.get('name', cat_key.title())
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': cat_name, 'item': canonical})
    elif page_type in ('legal', 'static'):
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': title, 'item': canonical})

    jsonld.append(('application/ld+json', {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': crumbs,
    }))

    if jsonld_blocks:
        for blk in jsonld_blocks:
            jsonld.append(('application/ld+json', blk))

    jsonld_tags = '\n'.join(
        '  <script type="' + t + '">\n  ' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n  </script>'
        for t, obj in jsonld
    )

    # Breadcrumb HTML
    crumb_items = ['<a href="' + SITE_URL + '/">hostazar</a>']
    if page_type == 'article' and article_meta and article_meta.get('category'):
        cat_key = article_meta['category']
        cat_info = KATEGORIEN.get(cat_key, {})
        cat_name = cat_info.get('name', cat_key.title())
        crumb_items.append('<a href="' + SITE_URL + '/' + cat_key + '/">' + h(cat_name) + '</a>')
        crumb_items.append('<span class="current">' + h(title) + '</span>')
    elif page_type == 'category' and article_meta and article_meta.get('cat'):
        cat_key = article_meta['cat']
        cat_info = KATEGORIEN.get(cat_key, {})
        cat_name = cat_info.get('name', cat_key.title())
        crumb_items.append('<span class="current">' + h(cat_name) + '</span>')
    elif page_type in ('legal', 'static'):
        crumb_items.append('<span class="current">' + h(title) + '</span>')

    breadcrumb_html = '  <nav class="breadcrumbs">' + '<span class="sep"> &rsaquo; </span>'.join(crumb_items) + '</nav>\n'

    nav_html = build_mega_nav_html()
    footer_html = build_footer()

    return '''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>''' + h(title) + '''</title>
  <meta name="description" content="''' + h(desc) + '''">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="''' + canonical + '''">
  <link rel="stylesheet" href="/css/style.css">
  <meta property="og:type" content="''' + og_type + '''">
  <meta property="og:url" content="''' + canonical + '''">
  <meta property="og:title" content="''' + h(title) + '''">
  <meta property="og:description" content="''' + h(desc) + '''">
  <meta property="og:image" content="''' + og_image + '''">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Hostazar &mdash; VPS &amp; DevOps Portal">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="''' + h(title) + '''">
  <meta name="twitter:description" content="''' + h(desc) + '''">
  <meta name="twitter:image" content="''' + og_image + '''">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
''' + extra_head + '''
''' + jsonld_tags + '''
</head>
<body>
''' + nav_html + '''
''' + breadcrumb_html + body_html + '''
''' + footer_html + '''
<script src="/data/script.js" defer></script>
</body>
</html>'''


# ── Navigation ───────────────────────────────────────────────────────────────

def build_mega_nav_html():
    cats_order = ['gaming', 'webhosting', 'devops', 'ki-llm']
    cat_colors = {'gaming': '#4CAF50', 'webhosting': '#2196F3', 'devops': '#FF9800', 'ki-llm': '#9C27B0'}

    lines = [
        '<nav class="navbar">',
        '  <div class="container">',
        '    <a href="/" class="logo">hosta<span>zar</span></a>',
        '    <button class="nav-toggle" aria-label="Men&#252; &#246;ffnen">&#9776;</button>',
        '    <ul class="nav-links">',
        '      <li><a href="/">Startseite</a></li>',
    ]

    for cat in cats_order:
        cat_info = KATEGORIEN.get(cat, {})
        emoji = cat_info.get('emoji', '')
        color = cat_info.get('color', cat_colors.get(cat, '#9C27B0'))
        name = cat_info.get('name', cat.title())
        arts = CAT_GROUPS.get(cat, [])
        half = (len(arts) + 1) // 2
        col1 = arts[:half]
        col2 = arts[half:]

        lines.append('      <li class="nav-dropdown">')
        lines.append('        <a href="/' + cat + '/">' + h(emoji) + ' ' + h(name) + '</a>')
        lines.append('        <div class="nav-dropdown-menu"><div class="mega-grid">')
        lines.append('          <div class="mega-column">')
        lines.append('            <h4><span style="color:' + color + '">&#9670;</span> A-Z</h4>')
        for a in col1:
            slug = a['slug']
            img = a.get('image', '')
            atitle = h(a['title'])
            lines.append('            <a href="/artikel/' + slug + '.html" class="mega-item">')
            if img:
                lines.append('              <img src="/images/' + img + '" alt="" loading="lazy" width="36" height="36">')
            lines.append('              <span class="mega-title">' + atitle + '</span>')
            lines.append('            </a>')
        lines.append('          </div>')
        lines.append('          <div class="mega-column">')
        lines.append('            <h4><span style="color:' + color + '">&#9670;</span> Neueste</h4>')
        for a in col2:
            slug = a['slug']
            img = a.get('image', '')
            atitle = h(a['title'])
            lines.append('            <a href="/artikel/' + slug + '.html" class="mega-item">')
            if img:
                lines.append('              <img src="/images/' + img + '" alt="" loading="lazy" width="36" height="36">')
            lines.append('              <span class="mega-title">' + atitle + '</span>')
            lines.append('            </a>')
        lines.append('          </div>')
        lines.append('          <div class="mega-view-all"><a href="/' + cat + '/">Alle ' + h(name) + '-Artikel</a></div>')
        lines.append('        </div></div>')
        lines.append('      </li>')

    lines += [
        '      <li><a href="/about.html">&#220;ber</a></li>',
        '    </ul>',
        '  </div>',
        '</nav>',
    ]
    return '\n'.join(lines)


# ── Footer ───────────────────────────────────────────────────────────────────

def build_footer():
    year = datetime.date.today().year
    cats_html = ''
    for cat_key, info in KATEGORIEN.items():
        name = info.get('name', cat_key)
        arts = CAT_GROUPS.get(cat_key, [])[:5]
        cats_html += '      <div class="footer-links-columns"><h5>' + h(name) + '</h5>\n'
        for a in arts:
            cats_html += '        <a href="/artikel/' + a['slug'] + '.html">' + h(a['title']) + '</a>\n'
        cats_html += '        <a href="/' + cat_key + '/" style="color:var(--accent)">Alle &rarr;</a>\n      </div>\n'

    return '''
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>hostazar.com</h4>
        <p style="color:var(--text-muted);font-size:.85rem;max-width:300px">
          Unabh&#228;ngige Hosting-Reviews, Gameserver-Guides und DevOps-Tutorials. Transparent, testbench-basiert, werbefrei.
        </p>
      </div>
''' + cats_html + '''    </div>
    <div class="footer-bottom">
      <span>&copy; ''' + str(year) + ''' hostazar.com</span>
      <span>
        <a href="/impressum.html">Impressum</a> &middot;
        <a href="/datenschutz.html">Datenschutz</a>
      </span>
    </div>
    <div class="affiliate-note">
      * Affiliate-Links: Wir erhalten ggf. eine Provision beim Kauf. Das kostet dich keinen Cent mehr.
    </div>
  </div>
</footer>
<div class="cookie-banner" id="cookieBanner">
  <div class="cookie-inner">
    <p>Wir nutzen Cookies f&#252;r Analyse und AdSense. <a href="/datenschutz.html">Mehr erfahren</a></p>
    <button class="cookie-btn" id="cookieBtn">Akzeptieren</button>
  </div>
</div>'''


# ── Blog Card ────────────────────────────────────────────────────────────────

def render_blog_card(a, color_map=None):
    if color_map is None:
        color_map = {'gaming': '#4CAF50', 'webhosting': '#2196F3', 'devops': '#FF9800'}
    cat = a.get('category', 'devops')
    cat_info = KATEGORIEN.get(cat, {})
    cat_name = cat_info.get('name', cat.title())
    color = color_map.get(cat, '#9C27B0')
    image = a.get('image', '')
    date_display = ''
    if a.get('date'):
        try:
            dt = datetime.date.fromisoformat(a['date'])
            date_display = dt.strftime('%d. %B %Y')
        except Exception:
            date_display = a['date']

    if image:
        img_html = '<img src="/images/' + image + '" alt="' + h(a['title']) + '" loading="lazy" width="400" height="200">'
    else:
        img_html = '<span class="placeholder-icon">&#128196;</span>'

    return '''<article class="blog-card">
  <a href="/artikel/''' + a['slug'] + '''.html" class="card-img-link">
    <div class="card-img">''' + img_html + '''</div>
  </a>
  <div class="card-body">
    <div class="card-meta">
      <span class="card-tag ''' + cat + '''" style="background:''' + color + '''22;color:''' + color + '''">''' + h(cat_name) + '''</span>
      <span>''' + date_display + '''</span>
      <span>''' + a.get('readingTime', '?') + ''' Min</span>
    </div>
    <h3><a href="/artikel/''' + a['slug'] + '''.html">''' + h(a['title']) + '''</a></h3>
    <p class="card-excerpt">''' + h(a.get('excerpt', '')) + '''</p>
    <div class="card-footer">
      <a href="/artikel/''' + a['slug'] + '''.html" class="read-more">Weiterlesen &rarr;</a>
    </div>
  </div>
</article>'''


# ── Related Articles ─────────────────────────────────────────────────────────

def render_related(current_slug, category, n=6):
    """Find related articles: same category first, then cross-category by tag overlap."""
    current = next((a for a in ARTIKEL if a['slug'] == current_slug), None)
    current_tags = set(t.lower() for t in (current.get('tags') or []))
    
    # Score all other articles
    scored = []
    for a in ARTIKEL:
        if a['slug'] == current_slug:
            continue
        score = 0
        # Same category bonus
        if a.get('category') == category:
            score += 3
        # Tag overlap
        a_tags = set(t.lower() for t in (a.get('tags') or []))
        overlap = current_tags & a_tags
        score += len(overlap) * 2
        # Prefer newer articles
        if a.get('date', '') > '2026-06-01':
            score += 1
        scored.append((score, a))
    
    scored.sort(key=lambda x: (-x[0], x[1].get('date', '')), reverse=False)
    pool = [a for _, a in scored[:n]]
    
    if not pool:
        return ''
    cards = '\n'.join(render_blog_card(a) for a in pool)
    return '''
<section class="related-section">
  <h4 class="related-heading">&#128214; &#196;hnliche Artikel</h4>
  <div class="related-grid">
    ''' + cards + '''
  </div>
</section>'''


# ── Build: Index Page ────────────────────────────────────────────────────────

def build_index():
    all_sorted = sorted(ARTIKEL, key=lambda a: a.get('date', '') or '', reverse=True)
    total = len(all_sorted)

    cat_counts = {}
    for a in ARTIKEL:
        cat_counts[a.get('category', 'devops')] = cat_counts.get(a.get('category', 'devops'), 0) + 1

    stats_inner = '        <div class="stat-item"><div class="stat-num">' + str(total) + '</div><div class="stat-label">Artikel gesamt</div></div>\n'
    cat_labels = {'gaming': 'Gaming', 'webhosting': 'Webhosting', 'devops': 'DevOps', 'ki-llm': 'KI & LLM'}
    for cat in ['gaming', 'webhosting', 'devops', 'ki-llm']:
        count = cat_counts.get(cat, 0)
        label = cat_labels.get(cat, cat)
        stats_inner += '        <div class="stat-item"><div class="stat-num">' + str(count) + '</div><div class="stat-label">' + label + '</div></div>\n'

    hero = '''
<section class="hero">
  <div class="container">
    <h1>Hosting &amp; Server <span>Blog</span></h1>
    <p>''' + SITE_DESC + '''</p>
    <div class="badge-row">
      <span class="badge">&#10003; 100% Unabh&#228;ngig</span>
      <span class="badge">&#10003; Benchmark-getestet</span>
      <span class="badge">&#10003; auf Deutsch</span>
    </div>
  </div>
</section>'''

    stats_html = '''
<section class="site-stats">
  <div class="container">
''' + stats_inner + '''  </div>
</section>'''

    cat_sections = ''
    cat_colors = {'gaming': '#4CAF50', 'webhosting': '#2196F3', 'devops': '#FF9800', 'ki-llm': '#9C27B0'}
    for cat in ['gaming', 'webhosting', 'devops', 'ki-llm']:
        arts = CAT_GROUPS.get(cat, [])
        if not arts:
            continue
        cat_info = KATEGORIEN.get(cat, {})
        cat_name = cat_info.get('name', cat.title())
        emoji = cat_info.get('emoji', '')
        color = cat_info.get('color', cat_colors.get(cat, '#9C27B0'))
        recent = arts[:6]
        grid = '\n'.join(render_blog_card(a) for a in recent)
        line1 = '<section class="cat-section">'
        line2 = '  <div class="container">'
        line3 = '    <h2 id="' + cat + '"><a href="/' + cat + '/" style="color:' + color + '">' + h(emoji) + ' ' + h(cat_name) + '</a></h2>'
        line4 = '    <div class="blog-grid">'
        line5 = '      ' + grid
        line6 = '    </div>'
        line7 = '    <div class="cat-more-link">'
        line8 = '      <a href="/' + cat + '/">Alle ' + h(cat_name) + '-Artikel (' + str(len(arts)) + ') &rarr;</a>'
        line9 = '    </div>'
        line10 = '  </div>'
        line11 = '</section>'
        cat_sections += '\n' + line1 + '\n' + line2 + '\n' + line3 + '\n' + line4 + '\n' + line5 + '\n' + line6 + '\n' + line7 + '\n' + line8 + '\n' + line9 + '\n' + line10 + '\n' + line11

    body = hero + stats_html + cat_sections

    page = page_shell(
        title=SITE_NAME + ' &ndash; Hosting &amp; Server Portal | Gaming, Webhosting &amp; DevOps',
        desc=SITE_DESC,
        canonical=SITE_URL + '/',
        body_html=body,
        og_type='website',
        page_type='index',
    )
    out = os.path.join(BASE, 'index.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    print('OK index.html (' + str(total) + ' Artikel)', file=sys.stderr)


# ── Build: Category Pages ────────────────────────────────────────────────────

def build_category(cat_key):
    cat_info = KATEGORIEN.get(cat_key, {})
    cat_name = cat_info.get('name', cat_key.title())
    cat_desc = cat_info.get('desc', '')
    cat_emoji = cat_info.get('emoji', '')
    arts = CAT_GROUPS.get(cat_key, [])
    if not arts:
        print('  WARN: Keine Artikel fuer Kategorie ' + cat_key, file=sys.stderr)
        return

    grid = '\n'.join(render_blog_card(a) for a in arts)

    body = '''
<section class="cat-hero">
  <div class="container">
    <h1>''' + h(cat_emoji) + ' ' + h(cat_name) + '''</h1>
    <p>''' + h(cat_desc) + ' <strong>' + str(len(arts)) + ''' Artikel</strong></p>
  </div>
</section>
<section><div class="container">
  <div class="blog-grid">
    ''' + grid + '''
  </div>
</div></section>'''

    # JSON-LD BlogPosting list
    bplist = []
    for a in arts:
        entry = {
            '@context': 'https://schema.org',
            '@type': 'BlogPosting',
            'headline': a['title'],
            'url': article_url(a['slug']),
            'datePublished': a.get('date', ''),
            'dateModified': a.get('date', ''),
            'description': a.get('excerpt', ''),
            'author': {'@type': 'Organization', 'name': SITE_NAME},
        }
        if a.get('image'):
            entry['image'] = SITE_URL + '/images/' + a['image']
        bplist.append(entry)

    extra_head = '  <script type="application/ld+json">\n' + json.dumps(bplist, ensure_ascii=False, indent=2) + '\n  </script>'

    page = page_shell(
        title=h(cat_emoji) + ' ' + h(cat_name) + ' &ndash; Artikel &amp; Guides | ' + SITE_NAME,
        desc=h(cat_desc) + ' ' + str(len(arts)) + ' Artikel zu ' + h(cat_name) + ' auf ' + SITE_NAME + '.',
        canonical=cat_url(cat_key),
        body_html=body,
        og_type='website',
        page_type='category',
        extra_head=extra_head,
        article_meta={'cat': cat_key},
    )

    cat_dir = os.path.join(BASE, cat_key)
    os.makedirs(cat_dir, exist_ok=True)
    out = os.path.join(cat_dir, 'index.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page)
    print('OK ' + cat_key + '/index.html (' + str(len(arts)) + ' Artikel)', file=sys.stderr)


# ── Build: Article Pages ─────────────────────────────────────────────────────

def build_all_articles():
    patched = 0
    for a in ARTIKEL:
        ap = article_path(a['slug'])
        if not os.path.exists(ap):
            continue
        with open(ap, encoding='utf-8') as f:
            raw = f.read()

        cat = a.get('category', 'devops')
        cat_info = KATEGORIEN.get(cat, {})
        cat_name = cat_info.get('name', cat.title())
        image = a.get('image', '')
        if image:
            og_image = SITE_URL + '/images/' + image
        else:
            og_image = SITE_URL + '/images/ollama-llm-server-vps-2026.png'

        # Extract article content
        content_match = re.search(
            r'<(?:main|div[^>]*class="?article-content"?[^>]*)>(.*?)</(?:main|div)>',
            raw, re.DOTALL | re.IGNORECASE
        )
        if not content_match:
            content_match = re.search(
                r'<article[^>]*>(.*?)</article>',
                raw, re.DOTALL | re.IGNORECASE
            )

        if content_match:
            article_inner = content_match.group(1)
        else:
            bm = re.search(r'<body[^>]*>(.*?)</body>', raw, re.DOTALL | re.IGNORECASE)
            article_inner = bm.group(1) if bm else raw

        rel = render_related(a['slug'], cat)
        reading_time = a.get('readingTime', '?')

        article_body_html = (
            '<main class="article-page">\n'
            '  <div class="container">\n'
            '    <div class="article-meta-top">\n'
            '      <span class="card-tag ' + cat + '">' + h(cat_name) + '</span>\n'
            '      <span>' + reading_time + ' Min Lesezeit</span>\n'
            '    </div>\n'
            + article_inner + '\n' +
            rel + '\n'
            '  </div>\n'
            '</main>'
        )

        page = page_shell(
            title=a['title'] + ' | ' + SITE_NAME,
            desc=a.get('excerpt', SITE_DESC),
            canonical=article_url(a['slug']),
            body_html=article_body_html,
            og_type='article',
            og_image=og_image,
            page_type='article',
            article_html=raw,
            article_meta={
                'date': a.get('date', ''),
                'image': image,
                'excerpt': a.get('excerpt', ''),
                'category': cat,
            },
        )

        with open(ap, 'w', encoding='utf-8') as f:
            f.write(page)
        patched += 1

    print('OK ' + str(patched) + ' Artikel-Seiten gerendert', file=sys.stderr)


# ── Build: Static Legal Pages ────────────────────────────────────────────────

def build_legal_page(filename, title, desc, body_inner):
    body = '<main class="static-page"><div class="container">' + body_inner + '</div></main>'
    canonical = SITE_URL + '/' + filename
    page = page_shell(
        title=title + ' | ' + SITE_NAME,
        desc=desc,
        canonical=canonical,
        body_html=body,
        page_type='legal',
    )
    with open(os.path.join(BASE, filename), 'w', encoding='utf-8') as f:
        f.write(page)


def build_legal_pages():
    for fname, title, desc in [
        ('impressum.html', 'Impressum', 'Impressum und Angaben nach &sect; 5 TMG f&#252;r hostazar.com.'),
        ('datenschutz.html', 'Datenschutzerkl&#228;rung', 'Datenschutzerkl&#228;rung f&#252;r hostazar.com gem&#228;&szlig; DSGVO.'),
        ('about.html', '&#220;ber hostazar.com', '&#220;ber uns: hostazar.com &ndash; unabh&#228;ngige Hosting-Reviews und Server-Guides.'),
    ]:
        with open(os.path.join(BASE, fname), encoding='utf-8') as f:
            existing = f.read()
        m = re.search(r'<body[^>]*>(.*?)</body>', existing, re.DOTALL)
        body_inner = m.group(1) if m else existing
        build_legal_page(fname, title, desc, body_inner)
    print('OK Legal pages (impressum, datenschutz, about)', file=sys.stderr)


# ── Build: Sitemap ───────────────────────────────────────────────────────────

def build_sitemap():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    def add_url(loc, lastmod=None, changefreq='monthly', priority='0.7'):
        lines.append('  <url>')
        lines.append('    <loc>' + loc + '</loc>')
        if lastmod:
            lines.append('    <lastmod>' + lastmod + '</lastmod>')
        lines.append('    <changefreq>' + changefreq + '</changefreq>')
        lines.append('    <priority>' + priority + '</priority>')
        lines.append('  </url>')

    add_url(SITE_URL + '/', changefreq='daily', priority='1.0')
    add_url(SITE_URL + '/about.html', changefreq='monthly', priority='0.5')
    add_url(SITE_URL + '/impressum.html', changefreq='yearly', priority='0.3')
    add_url(SITE_URL + '/datenschutz.html', changefreq='yearly', priority='0.3')

    for cat in KATEGORIEN:
        latest = CAT_GROUPS.get(cat, [])
        lastmod = latest[0].get('date', '') if latest else ''
        add_url(SITE_URL + '/' + cat + '/', lastmod=lastmod, changefreq='daily', priority='0.8')

    for a in ARTIKEL:
        slug = a['slug']
        date = a.get('date', '')
        add_url(article_url(slug), lastmod=date, changefreq='monthly', priority='0.7')

    lines.append('</urlset>')

    out = os.path.join(BASE, 'sitemap.xml')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print('OK sitemap.xml (' + str(len(ARTIKEL)) + ' Artikel-URLs)', file=sys.stderr)


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('=' * 50, file=sys.stderr)
    print(' hostazar.com Mega Portal Build v2', file=sys.stderr)
    print('=' * 50, file=sys.stderr)

    build_index()
    for cat in KATEGORIEN:
        build_category(cat)
    build_all_articles()
    build_legal_pages()
    build_sitemap()

    print('-' * 50, file=sys.stderr)
    print(' FERTIG: ' + str(len(ARTIKEL)) + ' Artikel, ' + str(len(KATEGORIEN)) + ' Kategorien', file=sys.stderr)
    print('-' * 50, file=sys.stderr)
