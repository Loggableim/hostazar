#!/usr/bin/env python3
"""Publish one or more articles to hostazar.com — additive, surgical pipeline.

What it does per article:
  1. Generate hero image via local Gen Queue (port 8283, brand style) → PNG + WebP
  2. Render full article HTML in the current site format (nav/footer from skeleton)
  3. Update data/artikel.json (catalog)
  4. Update index.html (card at top of category grid, trim to 6, stats + counts)
  5. Update sitemap.xml (new URL, drop stale /tmp/ URLs)
  6. Regenerate feed.xml
  7. git add/commit/push → GitHub Actions deploys to Cloudflare Pages

Usage:
  python scripts/publish_article.py --spec spec.json          # single article
  python scripts/publish_article.py --specs specs.json        # list of articles
  python scripts/publish_article.py --spec spec.json --no-push

Spec format (JSON):
  {
    "slug": "my-article-2026",
    "title": "Mein Artikel – Titel 2026",
    "category": "devops",              # gaming | webhosting | devops | ki-llm
    "tags": ["Docker", "VPS"],
    "excerpt": "Meta description, max 160 chars.",
    "content_file": "tmp/body.html",   # path to body HTML (h2/p/table/...)
    "image_subject": "anthropomorphic fox devops engineer, kubernetes cluster",  # optional
    "date": "2026-09-19"               # optional, default today
  }
"""
import argparse, datetime, json, os, re, subprocess, sys, time, urllib.request
from io import BytesIO

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, 'artikel')
IMG_DIR = os.path.join(REPO, 'images')
JSON_PATH = os.path.join(REPO, 'data', 'artikel.json')
INDEX_PATH = os.path.join(REPO, 'index.html')
SITEMAP_PATH = os.path.join(REPO, 'sitemap.xml')
SKELETON = os.path.join(ARTIKEL_DIR, '7-days-to-die-server-hosten-2026.html')

SITE = 'https://hostazar.com'
QUEUE = 'http://127.0.0.1:8283'
VENV_PY = r'C:\HermesPortable\venv\Scripts\python.exe'
QUEUE_SCRIPT = r'C:\HermesPortable\home\scripts\local_gen_queue.py'

BRAND_STYLE = (
    'furry editorial illustration, anthropomorphic animal characters, '
    'black and white ink illustration with selective orange color accents on clothing and equipment, '
    'bold black ink outlines, '
    'high contrast monochrome shading, clean vector illustration, graphic novel aesthetics, '
    'editorial magazine artwork, dynamic composition, expressive characters, '
    'professional commercial illustration, crisp linework, halftone textures'
)
NEGATIVE = (
    'photorealistic, painting, oil paint, watercolor, 3d render, photograph, '
    'realistic lighting, soft shading, gradient blur, signature, watermark, text, '
    'low quality, ugly, deformed, blurry, fully grayscale, no color'
)

CAT_META = {
    'gaming':     {'label': 'Gaming',     'bg': 'rgba(76,175,80,0.2)',  'fg': '#66bb6a', 'color': '#4CAF50', 'emoji': '🎮'},
    'webhosting': {'label': 'Webhosting', 'bg': 'rgba(33,150,243,0.2)', 'fg': '#64b5f6', 'color': '#2196F3', 'emoji': '🌐'},
    'devops':     {'label': 'DevOps',     'bg': 'rgba(255,152,0,0.2)',  'fg': '#ffb74d', 'color': '#FF9800', 'emoji': '⚙️'},
    'ki-llm':     {'label': 'KI & LLM',   'bg': 'rgba(156,39,176,0.2)', 'fg': '#ce93d8', 'color': '#9C27B0', 'emoji': '🤖'},
}

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))


def log(msg):
    print(msg, flush=True)


# ── Gen Queue ────────────────────────────────────────────────────────────────

def ensure_queue():
    """Return True if the local gen queue responds; start it detached if not."""
    try:
        urllib.request.urlopen(f'{QUEUE}/health', timeout=5)
        return True
    except Exception:
        pass
    log('  Gen Queue nicht erreichbar — starte sie...')
    try:
        DETACHED = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        subprocess.Popen(
            [VENV_PY, QUEUE_SCRIPT],
            cwd=os.path.dirname(QUEUE_SCRIPT),
            creationflags=DETACHED,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        log(f'  ! Queue-Start fehlgeschlagen: {e}')
        return False
    for _ in range(30):
        time.sleep(2)
        try:
            urllib.request.urlopen(f'{QUEUE}/health', timeout=5)
            log('  Queue gestartet.')
            return True
        except Exception:
            continue
    log('  ! Queue kam nicht hoch.')
    return False


def generate_hero_image(slug, subject, timeout=600):
    """Generate hero image via gen queue → images/{slug}.png + .webp. Returns bool."""
    prompt = f'{subject}, {BRAND_STYLE}'
    payload = json.dumps({
        'model': 'sdxl-realvis',
        'prompt': prompt,
        'negative': NEGATIVE,
        'steps': 25, 'cfg': 7.0,
        'width': 1216, 'height': 832,
    }).encode()
    req = urllib.request.Request(f'{QUEUE}/generate', data=payload,
                                 headers={'Content-Type': 'application/json'})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        job_id = resp.get('job_id')
    except Exception as e:
        log(f'  ! Bild-Submit fehlgeschlagen: {e}')
        return False
    if not job_id:
        log(f'  ! Kein job_id: {resp}')
        return False

    out_path = None
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(5)
        try:
            st = json.loads(urllib.request.urlopen(f'{QUEUE}/status/{job_id}', timeout=10).read())
        except Exception:
            continue
        status = st.get('status')
        if status == 'done' and st.get('output_path'):
            out_path = st['output_path']
            break
        if status == 'failed':
            log(f'  ! Bild-Job fehlgeschlagen: {st.get("error")}')
            return False
    if not out_path or not os.path.exists(out_path):
        log('  ! Bild-Timeout.')
        return False

    img = Image.open(out_path)
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img = img.convert('RGB').resize((1216, 832), Image.LANCZOS)
    img.save(os.path.join(IMG_DIR, f'{slug}.png'), 'PNG', optimize=True)
    img.save(os.path.join(IMG_DIR, f'{slug}.webp'), 'WEBP', quality=92, method=6)
    return True


# ── Rendering ────────────────────────────────────────────────────────────────

def _extract_skeleton_parts():
    raw = open(SKELETON, encoding='utf-8').read()
    nav = re.search(r'<nav class="navbar">.*?</nav>', raw, re.DOTALL).group(0)
    footer = re.search(r'<footer class="footer">.*?</footer>', raw, re.DOTALL).group(0)
    return nav, footer


def extract_faq(content_html):
    """Extract FAQ Q&A pairs from a FAQ section (h3 question + p answer)."""
    m = re.search(r'<h2[^>]*>\s*(?:FAQ|Häufige Fragen|Häufig gestellte Fragen)\s*</h2>(.*)$',
                  content_html, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    tail = m.group(1)
    pairs = []
    for qm in re.finditer(r'<h3[^>]*>(.*?)</h3>\s*<p>(.*?)</p>', tail, re.DOTALL):
        q = re.sub(r'<[^>]+>', '', qm.group(1)).strip()
        a = re.sub(r'<[^>]+>', '', qm.group(2)).strip()
        if q and a:
            pairs.append((q, a))
    return pairs[:6]


def render_article_html(spec):
    """Render full article HTML matching the current site format."""
    slug = spec['slug']
    title = spec['title']
    cat = spec['category']
    cm = CAT_META[cat]
    desc = spec['excerpt']
    date = spec.get('date') or datetime.date.today().isoformat()
    content = spec['content_html']
    image = f'{slug}.webp'
    img_url = f'{SITE}/images/{image}'
    url = f'{SITE}/artikel/{slug}.html'

    words = len(re.sub(r'<[^>]+>', ' ', content).split())
    rt = max(1, round(words / 280))

    nav, footer = _extract_skeleton_parts()

    # FAQ schema
    faq_pairs = extract_faq(content)
    faq_block = ''
    if faq_pairs:
        entities = []
        for q, a in faq_pairs:
            entities.append({
                '@type': 'Question', 'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': a},
            })
        faq_block = (
            '  <script type="application/ld+json">\n'
            + json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage',
                          'mainEntity': entities}, ensure_ascii=False, indent=2)
            + '\n  </script>\n'
        )

    article_schema = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': f'{title} | hostazar.com',
        'url': url,
        'description': desc,
        'inLanguage': 'de',
        'isPartOf': {'@type': 'WebSite', 'name': 'hostazar.com', 'url': SITE},
        'datePublished': date,
        'dateModified': date,
        'image': img_url,
        'author': {'@type': 'Organization', 'name': 'hostazar.com'},
        'publisher': {'@type': 'Organization', 'name': 'hostazar.com'},
        'wordCount': words,
    }
    breadcrumb_schema = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Startseite', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url},
        ],
    }

    # Related articles: 6 newest from same category, excluding self
    catalog = json.load(open(JSON_PATH, encoding='utf-8'))
    rel = [a for a in catalog
           if a.get('category') == cat and a['slug'] != slug]
    rel.sort(key=lambda a: a.get('date', '') or '', reverse=True)
    rel = rel[:6]
    rel_cards = []
    for a in rel:
        rcm = CAT_META.get(a.get('category', 'devops'), CAT_META['devops'])
        rdate = a.get('date', '')
        try:
            d = datetime.date.fromisoformat(rdate)
            date_str = f'{d.day:02d}. {MONTHS[d.month - 1]} {d.year}'
        except Exception:
            date_str = rdate
        rel_cards.append(f'''<article class="blog-card">
  <a href="/artikel/{a['slug']}.html" class="card-img-link">
    <div class="card-img"><img src="/images/{a.get('image', '')}" alt="{esc(a['title'])}" loading="lazy" width="400" height="200"></div>
  </a>
  <div class="card-body">
    <div class="card-meta">
      <span class="card-tag {a.get('category', 'devops')}" style="background:{rcm['color']}22;color:{rcm['color']}">{rcm['label']}</span>
      <span>{date_str}</span>
      <span>{a.get('readingTime', '?')} Min</span>
    </div>
    <h3><a href="/artikel/{a['slug']}.html">{esc(a['title'])}</a></h3>
    <p class="card-excerpt">{esc(a.get('excerpt', ''))}</p>
    <div class="card-footer">
      <a href="/artikel/{a['slug']}.html" class="read-more">Weiterlesen &rarr;</a>
    </div>
  </div>
</article>''')
    related_html = ''
    if rel_cards:
        related_html = (
            '\n\n<section class="related-section">\n'
            '  <h4 class="related-heading">&#128214; &#196;hnliche Artikel</h4>\n'
            '  <div class="related-grid">\n    '
            + '\n'.join(rel_cards)
            + '\n  </div>\n</section>'
        )

    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} | hostazar.com</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{url}">
  <link rel="stylesheet" href="/css/style.css">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{esc(title)} | hostazar.com">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:image" content="{img_url}">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Hostazar &mdash; VPS &amp; DevOps Portal">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)} | hostazar.com">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{img_url}">
  <script data-hz-src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="stylesheet" href="/css/consent-banner.css">

  <script type="application/ld+json">
{json.dumps(article_schema, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(breadcrumb_schema, ensure_ascii=False, indent=2)}
  </script>
{faq_block}</head>
<body>
{nav}
<main class="article-page">
  <div class="container">
    <div class="article-meta-top">
      <span class="card-tag {cat}">{cm['label']}</span>
      <span>{rt} Min Lesezeit</span>
    </div>
    <h1>{esc(title)}</h1>
{content}{related_html}
  </div>
</main>

{footer}
<script src="/data/script.js" defer></script>
<script src="/js/consent-manager.js" defer></script>
<script>
document.addEventListener('DOMContentLoaded', function () {{
  if (typeof hostazarApp !== 'undefined') {{
    hostazarApp.init({{
      gridId: 'related-articles',
      relatedConfig: {{
        containerId: 'related-articles',
        category: '{cat}',
        excludeSlug: '{slug}',
        count: 3
      }},
      breadcrumbs: [
        {{ url: '/{cat}/', label: '{cm['label']}' }},
        {{ label: '{esc(title)}' }}
      ]
    }});
  }}
}});
</script>
</body>
</html>'''
    return html


# ── Catalog / Index / Sitemap / Feed ─────────────────────────────────────────

def update_catalog(spec):
    data = json.load(open(JSON_PATH, encoding='utf-8'))
    if any(a['slug'] == spec['slug'] for a in data):
        log(f'  = {spec["slug"]} schon im Katalog')
        return
    words = len(re.sub(r'<[^>]+>', ' ', spec['content_html']).split())
    entry = {
        'slug': spec['slug'],
        'title': spec['title'],
        'category': spec['category'],
        'tags': spec.get('tags', []),
        'excerpt': spec['excerpt'],
        'date': spec.get('date') or datetime.date.today().isoformat(),
        'readingTime': str(max(1, round(words / 280))),
        'image': f'{spec["slug"]}.webp',
    }
    data.append(entry)
    data.sort(key=lambda a: a.get('date', '') or '', reverse=True)
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log(f'  + Katalog: {spec["slug"]} ({len(data)} Artikel)')


def _index_card(spec):
    cm = CAT_META[spec['category']]
    words = len(re.sub(r'<[^>]+>', ' ', spec['content_html']).split())
    rt = max(1, round(words / 280))
    date = spec.get('date') or datetime.date.today().isoformat()
    return f'''    <article class="blog-card">
      <a href="/artikel/{spec['slug']}.html" class="card-img-link">
        <div class="card-img">
          <img src="/images/{spec['slug']}.webp" alt="{esc(spec['title'])}" loading="lazy" onerror="this.parentElement.innerHTML='<span class=\\'placeholder-icon\\'>{cm['emoji']}</span>'">
        </div>
      </a>
      <div class="card-body">
        <div class="card-meta">
          <span class="card-tag {spec['category']}" style="background:{cm['bg']};color:{cm['fg']}">{cm['label']}</span>
          <span>{date}</span>
          <span>· {rt} Min</span>
        </div>
        <h3><a href="/artikel/{spec['slug']}.html">{esc(spec['title'])}</a></h3>
        <p class="card-excerpt">{esc(spec['excerpt'])}</p>
        <div class="card-footer">
          <span class="read-more"><a href="/artikel/{spec['slug']}.html">Weiterlesen →</a></span>
        </div>
      </div>
    </article>
'''


def update_index(specs):
    """Rebuild category grids with newest 6 from catalog; refresh stats/counts."""
    html = open(INDEX_PATH, encoding='utf-8').read()
    catalog = json.load(open(JSON_PATH, encoding='utf-8'))

    for spec in specs:
        log(f'  + Index: {spec["slug"]} → {spec["category"]}')

    # rebuild each category grid with the newest 6 catalog entries
    for cat in CAT_META:
        sec_marker = f'<section class="cat-section" id="{cat}">'
        sec_start = html.find(sec_marker)
        if sec_start < 0:
            log(f'  ! Sektion {cat} nicht gefunden')
            continue
        grid_marker = '<div class="blog-grid">'
        grid_pos = html.find(grid_marker, sec_start)
        if grid_pos < 0:
            log(f'  ! blog-grid in {cat} nicht gefunden')
            continue
        # grid closes at the </div> after the last </article> in this section
        sec_end = html.find('</section>', sec_start)
        last_article = html.rfind('</article>', grid_pos, sec_end)
        grid_end = html.find('</div>', last_article)
        arts = [a for a in catalog if a.get('category') == cat]
        arts.sort(key=lambda a: a.get('date', '') or '', reverse=True)
        arts = arts[:6]
        cards = '\n'.join(_index_card_from_entry(a) for a in arts)
        new_grid = grid_marker + '\n' + cards + '\n      '
        html = html[:grid_pos] + new_grid + html[grid_end:]

    # refresh counts
    total = len(catalog)
    per_cat = {}
    for a in catalog:
        per_cat[a.get('category', 'devops')] = per_cat.get(a.get('category', 'devops'), 0) + 1

    html = re.sub(r'(<div class="stat-num">)\d+(</div><div class="stat-label">Artikel</div>)',
                  rf'\g<1>{total}\g<2>', html)
    html = re.sub(r'mit \d+ Guides', f'mit {total} Guides', html)
    for cat, cm in CAT_META.items():
        n = per_cat.get(cat, 0)
        # cat-more-link (regular hyphen)
        html = re.sub(rf'(→ Alle )\d+( {re.escape(cm["label"])}-Artikel anzeigen)',
                      rf'\g<1>{n}\g<2>', html)
        # mega-nav view-all (non-breaking hyphen U+2011)
        html = re.sub(rf'(→ Alle )\d+( {re.escape(cm["label"])}\u2011Artikel anzeigen)',
                      rf'\g<1>{n}\g<2>', html)

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(html)
    log(f'  + Index aktualisiert (total={total}, {per_cat})')


def _index_card_from_entry(a):
    """Render an index card from a catalog entry."""
    cm = CAT_META.get(a.get('category', 'devops'), CAT_META['devops'])
    return f'''    <article class="blog-card">
      <a href="/artikel/{a['slug']}.html" class="card-img-link">
        <div class="card-img">
          <img src="/images/{a.get('image', '')}" alt="{esc(a['title'])}" loading="lazy" onerror="this.parentElement.innerHTML='<span class=\\'placeholder-icon\\'>{cm['emoji']}</span>'">
        </div>
      </a>
      <div class="card-body">
        <div class="card-meta">
          <span class="card-tag {a.get('category', 'devops')}" style="background:{cm['bg']};color:{cm['fg']}">{cm['label']}</span>
          <span>{a.get('date', '')}</span>
          <span>· {a.get('readingTime', '?')} Min</span>
        </div>
        <h3><a href="/artikel/{a['slug']}.html">{esc(a['title'])}</a></h3>
        <p class="card-excerpt">{esc(a.get('excerpt', ''))}</p>
        <div class="card-footer">
          <span class="read-more"><a href="/artikel/{a['slug']}.html">Weiterlesen →</a></span>
        </div>
      </div>
    </article>'''


def update_sitemap(specs):
    xml = open(SITEMAP_PATH, encoding='utf-8').read()
    # drop stale /tmp/ URLs
    xml = re.sub(r'\s*<url>\s*<loc>[^<]*/tmp/[^<]*</loc>.*?</url>', '', xml, flags=re.DOTALL)
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    for spec in specs:
        loc = f'{SITE}/artikel/{spec["slug"]}/'
        if loc in xml:
            continue
        block = (f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{now}</lastmod>\n'
                 f'    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n')
        xml = xml.replace('</urlset>', block + '</urlset>')
        log(f'  + Sitemap: {spec["slug"]}')
    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(xml)


def regenerate_feed():
    r = subprocess.run([sys.executable, os.path.join(REPO, 'scripts', 'generate_rss.py')],
                       cwd=REPO, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        log(f'  ! RSS-Feed: {r.stderr[-300:]}')
    else:
        log('  + feed.xml regeneriert')


def git_commit_push(message):
    def run(*args):
        return subprocess.run(['git'] + list(args), cwd=REPO,
                              capture_output=True, text=True, timeout=120)
    run('add', '-A')
    r = run('commit', '-m', message)
    if r.returncode != 0 and 'nothing to commit' not in (r.stdout + r.stderr):
        log(f'  ! git commit: {r.stdout[-200:]}{r.stderr[-200:]}')
        return False
    r = run('push')
    if r.returncode != 0:
        log(f'  ! git push: {r.stderr[-300:]}')
        return False
    log('  + committed & pushed → GitHub Actions deployt')
    return True


# ── Orchestration ────────────────────────────────────────────────────────────

def publish(specs, push=True):
    """Publish a list of specs. Returns dict with per-step results."""
    results = {'published': [], 'failed': []}
    if not specs:
        return results

    if not ensure_queue():
        log('! Gen Queue nicht verfügbar — Abbruch.')
        results['failed'] = [s['slug'] for s in specs]
        return results

    for spec in specs:
        slug = spec['slug']
        log(f'[{slug}] Publishing...')
        if os.path.exists(os.path.join(ARTIKEL_DIR, slug + '.html')):
            log(f'  ! Artikel existiert bereits — skip')
            results['failed'].append(slug)
            continue

        # 1. image
        subject = spec.get('image_subject') or f'anthropomorphic animal character, {spec["title"]}'
        if not generate_hero_image(slug, subject):
            log(f'  ! Bild fehlgeschlagen — Artikel wird übersprungen (kein Broken-Image)')
            results['failed'].append(slug)
            continue
        log('  + Hero-Bild (PNG+WebP)')

        # 2. render + write article
        html = render_article_html(spec)
        with open(os.path.join(ARTIKEL_DIR, slug + '.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        log('  + Artikel-HTML')

        # 3. catalog
        update_catalog(spec)
        results['published'].append(slug)

    # 4-6. catalog surfaces
    update_index([s for s in specs if s['slug'] in results['published']])
    update_sitemap([s for s in specs if s['slug'] in results['published']])
    regenerate_feed()

    # 7. deploy
    if push and results['published']:
        names = ', '.join(results['published'])
        git_commit_push(f'Content: {names}')

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', help='Path to single spec JSON')
    ap.add_argument('--specs', help='Path to specs JSON array')
    ap.add_argument('--no-push', action='store_true', help='Skip git commit/push')
    args = ap.parse_args()

    if args.spec:
        spec = json.load(open(args.spec, encoding='utf-8'))
        specs = [spec]
    elif args.specs:
        specs = json.load(open(args.specs, encoding='utf-8'))
    else:
        ap.error('--spec or --specs required')

    # resolve content_file relative to repo
    for s in specs:
        cf = s.get('content_file', '')
        if cf and not os.path.isabs(cf):
            s['content_file'] = os.path.join(REPO, cf)
        s['content_html'] = open(s['content_file'], encoding='utf-8').read()

    res = publish(specs, push=not args.no_push)
    log(f'\nFERTIG: {len(res["published"])} publiziert, {len(res["failed"])} fehlgeschlagen')
    if res['failed']:
        log(f'Fehlgeschlagen: {res["failed"]}')
        sys.exit(1)


if __name__ == '__main__':
    main()
