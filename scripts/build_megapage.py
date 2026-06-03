#!/usr/bin/env python3
"""hostazar.com Megapage Builder
Generates category pages, rebuilds index, patches articles.
Run from repo root: python scripts/build_megapage.py
"""
import json, os, re, sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with open(os.path.join(BASE, 'data', 'artikel.json'), encoding='utf-8') as f:
    ARTIKEL = json.load(f)
with open(os.path.join(BASE, 'data', 'kategorien.json'), encoding='utf-8') as f:
    KATEGORIEN = json.load(f)

print(f"BASE: {BASE}", file=sys.stderr)

CAT_SLUGS = sorted(ARTIKEL, key=lambda a: a['date'] or '', reverse=True)
CAT_GROUPS = {k: [a for a in ARTIKEL if a['category'] == k] for k in KATEGORIEN}
for k in CAT_GROUPS:
    CAT_GROUPS[k].sort(key=lambda a: a['date'] or '', reverse=True)

def h(s):
    d = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return ''.join(d.get(c, c) for c in s)

def build_mega_nav():
    """Generate mega navigation with all articles in dropdowns."""
    cats_order = ['gaming', 'webhosting', 'devops']
    cat_labels = {'gaming': '🎮 Gaming', 'webhosting': '🌐 Webhosting', 'devops': '⚙️ DevOps'}
    cat_colors = {'gaming': '#4CAF50', 'webhosting': '#2196F3', 'devops': '#FF9800'}
    
    nav = '''<nav class="navbar">
  <div class="container">
    <a href="/" class="logo">hosta<span>zar</span></a>
    <ul class="nav-links">
      <li><a href="/">Startseite</a></li>'''

    for cat in cats_order:
        articles = CAT_GROUPS.get(cat, [])
        color = cat_colors.get(cat, '#9C27B0')
        nav += f'''
      <li class="nav-dropdown">
        <a href="/{cat}/">{cat_labels.get(cat, cat)}</a>
        <div class="nav-dropdown-menu">
          <div class="mega-grid">'''
        
        # Split articles into 4 columns
        per_col = max(1, (len(articles) + 3) // 4)
        cols = [articles[i:i+per_col] for i in range(0, len(articles), per_col)]
        col_labels = ['Beliebt', 'Anleitungen', 'Vergleiche', 'Setup']
        
        for ci, col_articles in enumerate(cols):
            nav += f'''
            <div class="mega-column">
              <h4><span style="color:{color}">◆</span> {col_labels[ci] if ci < len(col_labels) else 'Mehr'}</h4>'''
            for a in col_articles:
                img = f"/images/{a['slug']}.png"
                title_raw = a['title'].replace('&amp;','&').replace('&','&amp;').replace(' — ',' – ')
                title_short = title_raw[:62]
                nav += f'''
              <a href="/artikel/{a['slug']}.html" class="mega-item">
                <img src="{img}" alt="" loading="lazy">
                <span class="mega-title">{title_short}</span>
              </a>'''
            nav += '''
            </div>'''
        
        nav += f'''
            <div class="mega-view-all">
              <a href="/{cat}/">→ Alle {len(articles)} {cat_labels.get(cat, cat).split()[1]}‑Artikel anzeigen</a>
            </div>
          </div>
        </div>
      </li>'''

    nav += '''
      <li><a href="/about.html">Über uns</a></li>
      <li><a href="/impressum.html">Impressum</a></li>
    </ul>
  </div>
</nav>'''
    return nav

NAV_HTML = build_mega_nav()

FOOTER_HTML = '''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>hosta<span style="color:var(--accent)">zar</span></h4>
        <p style="color:var(--text-muted);font-size:0.9rem">Dein Hosting- &amp; Server-Portal mit Guides, Vergleichen und Tutorials.</p>
      </div>
      <div>
        <h4>Kategorien</h4>
        <ul>
          <li><a href="/gaming/">🎮 Gaming</a></li>
          <li><a href="/webhosting/">🌐 Webhosting</a></li>
          <li><a href="/devops/">⚙️ DevOps</a></li>
        </ul>
      </div>
      <div>
        <h4>Rechtliches</h4>
        <ul>
          <li><a href="/about.html">Über uns</a></li>
          <li><a href="/impressum.html">Impressum</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 hostazar.com &ndash; Alle Rechte vorbehalten.</span>
      <span>Made with &hearts; f&uuml;r die Hosting-Community</span>
    </div>
    <p class="affiliate-note">* Bei den mit Sternchen gekennzeichneten Links handelt es sich um Affiliate-Links. Wenn du &uuml;ber diese Links einkaufst, erhalten wir eine kleine Provision &ndash; f&uuml;r dich entstehen keine Mehrkosten. Als Amazon-Partner verdienen wir an qualifizierten Verk&auml;ufen.</p>
  </div>
</footer>'''

def page_head(title, desc, canonical, cat_filter=''):
    blog_entries = json.dumps([
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": a['title'],
            "url": f"https://hostazar.com/artikel/{a['slug']}.html",
            "datePublished": a.get('date', '2026-06-15'),
            "dateModified": a.get('date', '2026-06-15'),
            "description": a.get('excerpt', '')[:200],
            "author": {"@type": "Organization", "name": "hostazar.com"}
        }
        for a in CAT_SLUGS[:12]
    ], ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h(title)} | hostazar.com</title>
  <meta name="description" content="{h(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{h(canonical)}">
  <link rel="stylesheet" href="/css/style.css">

  <meta property="og:type" content="website">
  <meta property="og:url" content="{h(canonical)}">
  <meta property="og:title" content="{h(title)}">
  <meta property="og:description" content="{h(desc)}">
  <meta property="og:image" content="https://hostazar.com/images/minecraft-server-vergleich-2026.png">
  <meta property="og:locale" content="de_DE">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{h(title)}">
  <meta name="twitter:description" content="{h(desc)}">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "{h(title)}",
    "url": "{h(canonical)}",
    "description": "{h(desc)}",
    "isPartOf": {{ "@type": "WebSite", "name": "hostazar.com", "url": "https://hostazar.com/" }}
  }}
  </script>

  <script type="application/ld+json">
  {blog_entries}
  </script>

  <script src="/data/script.js" defer></script>
</head>
<body>
{NAV_HTML}'''


def build_category_page(cat_key):
    cat = KATEGORIEN[cat_key]
    name = cat['name']
    emoji = cat['emoji']
    color = cat['color']
    desc = cat['desc']
    slug = cat_key

    articles = CAT_GROUPS.get(cat_key, [])
    count = len(articles)

    head = page_head(
        f'{emoji} {name} – Server Hosting & Guides',
        f'{name} Guides und Tutorials: {desc} {count} Artikel zu Gameserver-Hosting, Setup, Kosten und Vergleichen.',
        f'https://hostazar.com/{slug}/'
    )

    html = f'''{head}

<main>
  <section class="cat-hero" style="border-bottom:3px solid {color}">
    <div class="container">
      <h1>{emoji} {name}</h1>
      <p>{h(desc)}</p>
    </div>
  </section>

  <div class="container">
    <div class="search-section">
      <div class="search-bar">
        <input type="text" id="cat-search" placeholder="In {count} Artikeln suchen …" aria-label="Artikel suchen">
        <button class="search-reset-btn" id="search-reset">×</button>
      </div>
    </div>

    <div class="cat-filter-pills" id="cat-filter">
      <a href="#" class="cat-pill active" data-cat="all">Alle</a>
      <a href="#" class="cat-pill" data-cat="gaming">🎮 Gaming</a>
      <a href="#" class="cat-pill" data-cat="webhosting">🌐 Webhosting</a>
      <a href="#" class="cat-pill" data-cat="devops">⚙️ DevOps</a>
    </div>

    <div id="tag-cloud-container"></div>

    <div id="article-count"></div>

    <section class="blog-grid" id="article-grid"></section>

    <div id="pagination"></div>
  </div>
</main>

{FOOTER_HTML}

<script>
document.addEventListener('DOMContentLoaded', function () {{
  if (typeof hostazarApp !== 'undefined') {{
    hostazarApp.init({{
      gridId: 'article-grid',
      searchId: 'cat-search',
      filterId: 'cat-filter',
      paginationId: 'pagination',
      articleCountId: 'article-count',
      tagCloudId: 'tag-cloud-container',
      defaultCategory: '{slug}'
    }});
  }}
}});
</script>
</body>
</html>'''

    return html


def build_index():
    """New index page: hero + stats + category sections + streamlined footer."""
    total = len(ARTIKEL)
    gaming_count = len(CAT_GROUPS.get('gaming', []))
    webhosting_count = len(CAT_GROUPS.get('webhosting', []))
    devops_count = len(CAT_GROUPS.get('devops', []))

    # Build category sections (6 cards each)
    sections = []
    for cat_key, cat_data in KATEGORIEN.items():
        articles = CAT_GROUPS.get(cat_key, [])[:6]
        cards = []
        for a in articles:
            c = KATEGORIEN[a['category']]
            cards.append(f'''    <article class="blog-card">
      <a href="/artikel/{h(a['slug'])}.html" class="card-img-link">
        <div class="card-img">
          <img src="/images/{h(a['image'])}" alt="{h(a['title'])}" loading="lazy" onerror="this.parentElement.innerHTML='<span class=\\'placeholder-icon\\'>{c['emoji']}</span>'">
        </div>
      </a>
      <div class="card-body">
        <div class="card-meta">
          <span class="card-tag {cat_key}" style="background:{cat_data.get('tag_bg','rgba(76,175,80,0.2)')};color:{cat_data.get('tag_color','#66bb6a')}">{cat_data['name']}</span>
          <span>{a.get('date','2026')}</span>
          {f"<span>· {a['readingTime']} Min</span>" if a.get('readingTime') else ''}
        </div>
        <h3><a href="/artikel/{h(a['slug'])}.html">{h(a['title'])}</a></h3>
        <p class="card-excerpt">{h(a.get('excerpt','')[:150])}{'…' if len(a.get('excerpt','')) > 150 else ''}</p>
        <div class="card-footer">
          <span class="read-more"><a href="/artikel/{h(a['slug'])}.html">Weiterlesen →</a></span>
        </div>
      </div>
    </article>''')

        sections.append(f'''  <section class="cat-section" id="{cat_key}">
    <div class="container">
      <h2>{cat_data['emoji']} <a href="/{cat_key}/">{cat_data['name']}</a></h2>
      <div class="blog-grid">
{chr(10).join(cards)}
      </div>
      <div class="cat-more-link"><a href="/{cat_key}/">→ Alle {len(CAT_GROUPS[cat_key])} {cat_data['name']}-Artikel anzeigen</a></div>
    </div>
  </section>''')

    # Latest articles JSON-LD (top 12)
    latest_json = json.dumps([
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": a['title'],
            "url": f"https://hostazar.com/artikel/{a['slug']}.html",
            "datePublished": a.get('date', '2026-06-15'),
            "dateModified": a.get('date', '2026-06-15'),
            "description": a.get('excerpt', '')[:200],
            "author": {"@type": "Organization", "name": "hostazar.com"}
        }
        for a in ARTIKEL[:12]
    ], ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>hostazar.com – Hosting & Server Portal | Gaming, Webhosting & DevOps</title>
  <meta name="description" content="Hosting- und Server-Blog mit {total} Guides zu Gameserver-Miete, Webhosting, VPS und DevOps-Tools. Produktvergleiche und Tutorials auf Deutsch.">
  <meta name="keywords" content="Hosting, Server, Gameserver, Webhosting, VPS, DevOps, Cloud, Rootserver">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://hostazar.com/">
  <link rel="stylesheet" href="/css/style.css">

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://hostazar.com/">
  <meta property="og:title" content="hostazar.com – Hosting & Server Portal">
  <meta property="og:description" content="Hosting- und Server-Blog mit {total} Guides zu Gameserver-Miete, Webhosting, VPS und DevOps-Tools.">
  <meta property="og:image" content="https://hostazar.com/images/minecraft-server-vergleich-2026.png">
  <meta property="og:locale" content="de_DE">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="hostazar.com – Hosting & Server Portal">
  <meta name="twitter:description" content="Hosting- und Server-Blog mit {total} Guides zu Gameserver-Miete, Webhosting, VPS und DevOps-Tools.">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "hostazar.com",
    "url": "https://hostazar.com/",
    "description": "Hosting & Server Portal – Guides, Vergleiche und Tutorials zu Gameserver-Miete, Webhosting, VPS und DevOps-Tools.",
    "inLanguage": "de",
    "publisher": {{ "@type": "Organization", "name": "hostazar.com" }}
  }}
  </script>

  <script type="application/ld+json">
  {latest_json}
  </script>

  <script src="/data/script.js" defer></script>
</head>
<body>
{NAV_HTML}

<section class="hero">
  <div class="container">
    <h1>Server-Wissen <span>für Einsteiger &amp; Profis</span></h1>
    <p>Dein deutschsprachiges Portal rund um Gameserver, Webhosting, VPS und DevOps-Tools. Praxisnahe Guides, Vergleiche und Tutorials &ndash; unabh&auml;ngig, transparent, aktuell.</p>
    <div class="badge-row">
      <span class="badge">🎮 {gaming_count} Gaming-Guides</span>
      <span class="badge">🌐 {webhosting_count} Webhosting-Guides</span>
      <span class="badge">⚙️ {devops_count} DevOps-Guides</span>
    </div>
  </div>
</section>

<div class="container">
  <div class="site-stats">
    <div class="stat-item"><div class="stat-num">{total}</div><div class="stat-label">Artikel</div></div>
    <div class="stat-item"><div class="stat-num">3</div><div class="stat-label">Kategorien</div></div>
    <div class="stat-item"><div class="stat-num">5+</div><div class="stat-label">Gameserver-Guides</div></div>
    <div class="stat-item"><div class="stat-num">100%</div><div class="stat-label">Deutsch</div></div>
  </div>
</div>

{chr(10).join(sections)}

<div class="container">
  <div class="adsense-placeholder">
    <p><strong>— Anzeige —</strong></p>
    <p>Google AdSense Platzhalter. Hier erscheint nach Integration eine kontextbezogene Anzeige.</p>
  </div>
</div>

{FOOTER_HTML}

</body>
</html>'''
    return html


def patch_articles():
    """Patch all 34 articles: nav, breadcrumbs, related articles, script include."""
    total = 0
    for a in ARTIKEL:
        slug = a['slug']
        path = os.path.join(BASE, 'artikel', f'{slug}.html')
        if not os.path.exists(path):
            print(f"  MISSING: {path}")
            continue

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Add script.js include before </head>
        if '/data/script.js' not in content:
            content = content.replace('</head>', '  <script src="/data/script.js" defer></script>\n</head>')
            changed = True

        # 2. Replace nav - check if it lacks mega-grid
        old_nav = re.search(r'<nav class="navbar">.*?</nav>', content, re.DOTALL)
        if old_nav and 'mega-grid' not in old_nav.group():
            content = content.replace(old_nav.group(), NAV_HTML)
            changed = True

        # 3. Add breadcrumbs after article-header div close, before <div class="article-content">
        breadcrumb_html = '    <div id="breadcrumbs"></div>\n'
        if '<div id="breadcrumbs">' not in content:
            # Put breadcrumbs right after article-header closing div but before article-content
            content = content.replace(
                '    <div class="article-content">',
                breadcrumb_html + '    <div class="article-content">',
                1
            )
            changed = True

        # 4. Add related articles div before the last adsense/affiliate block in the article
        related_html = '    <div id="related-articles"></div>\n'
        if '<div id="related-articles">' not in content:
            # Find the last adsense or amazon block
            for marker in ['<!-- AdSense Platzhalter unten', '<!-- Amazon Affiliate Puffer', '<!-- AdSense Placeholder -->']:
                pos = content.find(marker)
                if pos != -1:
                    # Insert before this marker
                    content = content[:pos] + related_html + content[pos:]
                    changed = True
                    break

        # 5. Add inline init script before </body>
        cat_name = KATEGORIEN.get(a['category'], {}).get('name', a['category'])
        init_script = f"""<script>
document.addEventListener('DOMContentLoaded', function () {{
  if (typeof hostazarApp !== 'undefined') {{
    hostazarApp.init({{
      gridId: 'related-articles',
      relatedConfig: {{
        containerId: 'related-articles',
        category: '{a["category"]}',
        excludeSlug: '{slug}',
        count: 3
      }},
      breadcrumbs: [
        {{ url: '/{a["category"]}/', label: '{cat_name}' }},
        {{ label: '{a["title"]}' }}
      ]
    }});
  }}
}});
</script>"""
        if 'hostazarApp' not in content:
            content = content.replace('</body>', init_script + '\n</body>', 1)
            changed = True

        if changed:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            total += 1

    print(f"  ✅ {total} Artikel gepatcht")
    return total


def update_sitemap():
    """Add new category URLs to sitemap."""
    path = os.path.join(BASE, 'sitemap.xml')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_entries = ''
    for slug in KATEGORIEN:
        url = f'https://hostazar.com/{slug}/'
        if url not in content:
            new_entries += f'''
  <url>
    <loc>{url}</loc>
    <lastmod>2026-06-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>'''

    if new_entries:
        content = content.replace('  <url>\n    <loc>https://hostazar.com/</loc>', f'  <url>\n    <loc>https://hostazar.com/</loc>{new_entries}')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ Sitemap aktualisiert")
    else:
        print("  ℹ️ Sitemap bereits aktuell")

    return content


def write_category_pages():
    """Write all category landing pages."""
    created = 0
    for cat_key in KATEGORIEN:
        slug = cat_key
        dir_path = os.path.join(BASE, slug)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, 'index.html')
        html = build_category_page(cat_key)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        created += 1
        print(f"  ✅ /{slug}/index.html")
    return created


if __name__ == '__main__':
    print("=== hostazar.com Megapage Builder ===")
    print()
    print("Kategorie-Seiten:")
    write_category_pages()
    print()
    print("Index-Seite:")
    idx_html = build_index()
    with open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(idx_html)
    print("  ✅ index.html")
    print()
    print("Artikel patchen:")
    patch_articles()
    print()
    print("Sitemap:")
    update_sitemap()
    print()
    print("=== Fertig ===")
