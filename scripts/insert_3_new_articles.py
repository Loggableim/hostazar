#!/usr/bin/env python3
"""Insert 3 new article cards into hostazar.com index.html + update JSON / sitemap / JSON-LD."""
import os, json, re, html, datetime

REPO = r"C:\HermesPortable\home\scripts\blog-automation\hostazar"
ARTIKEL_JSON = os.path.join(REPO, "data", "artikel.json")
INDEX_HTML = os.path.join(REPO, "index.html")
SITEMAP = os.path.join(REPO, "sitemap.xml")

NOW = datetime.datetime(2026, 6, 6, 20, 30, 0)
LASTMOD = NOW.strftime("%Y-%m-%dT%H:%M:%S+00:00")

NEW_ARTICLES = [
    {
        "slug": "raft-server-mieten-2026",
        "title": "Raft Server mieten – Dedicated Server Guide & Kosten 2026",
        "category": "gaming",
        "tags": ["Raft Server mieten", "Raft Dedicated Server", "Raft Multiplayer", "Raft Server Hosting 2026", "Survival Gameserver"],
        "excerpt": "Raft Server mieten oder selbst hosten? ✓ Anbieter-Vergleich, Kosten, Setup-Anleitung & Mods. Alles für deinen eigenen Raft-Dedicated-Server 2026.",
        "date": "2026-06-06",
        "readingTime": "12",
        "image": "raft-server-mieten-2026.png",
    },
    {
        "slug": "helm-charts-kubernetes-guide-2026",
        "title": "Helm Charts – Kubernetes Package Manager Einführung & Praxis 2026",
        "category": "devops",
        "tags": ["Helm Charts", "Kubernetes Package Manager", "K8s Helm", "Helm Installieren", "Helm Chart erstellen"],
        "excerpt": "Helm Charts für Kubernetes: ✓ Installation, Charts suchen, deployen, eigene Charts erstellen & Praxis-Beispiele. Der komplette Helm-Guide 2026.",
        "date": "2026-06-06",
        "readingTime": "13",
        "image": "helm-charts-kubernetes-guide-2026.png",
    },
    {
        "slug": "hugo-astro-static-site-vergleich-2026",
        "title": "Hugo vs. Astro – Static Site Generator Hosting Vergleich 2026",
        "category": "webhosting",
        "tags": ["Hugo vs Astro", "Static Site Generator", "SSG Vergleich", "Webhosting SSG", "Hugo Astro Hosting"],
        "excerpt": "Hugo vs. Astro: Der große Static-Site-Generator-Vergleich 2026 ✓ Performance, Hosting, Lernkurve, Deployment & Use Cases. Welcher SSG passt zu dir?",
        "date": "2026-06-06",
        "readingTime": "14",
        "image": "hugo-astro-static-site-vergleich-2026.png",
    },
]

def h(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
              .replace('"', "&quot;").replace("'", "&#39;"))

def card_html(a, cat_label, tag_color_bg, tag_color_fg):
    slug = a["slug"]
    title = a["title"]
    excerpt = a["excerpt"]
    date = a["date"]
    rt = a["readingTime"]
    img = a["image"]
    return f'''    <article class="blog-card">
      <a href="/artikel/{slug}.html" class="card-img-link">
        <div class="card-img">
          <img src="/images/{img}" alt="{h(title)}" loading="lazy" onerror="this.parentElement.innerHTML='<span class=\\'placeholder-icon\\'>{cat_label.split()[0]}</span>'">
        </div>
      </a>
      <div class="card-body">
        <div class="card-meta">
          <span class="card-tag {a["category"]}" style="background:{tag_color_bg};color:{tag_color_fg}">{cat_label}</span>
          <span>{date}</span>
          <span>· {rt} Min</span>
        </div>
        <h3><a href="/artikel/{slug}.html">{h(title)}</a></h3>
        <p class="card-excerpt">{h(excerpt)}</p>
        <div class="card-footer">
          <span class="read-more"><a href="/artikel/{slug}.html">Weiterlesen →</a></span>
        </div>
      </div>
    </article>
'''

CATEGORY_STYLES = {
    "gaming":     ("Gaming",     "rgba(76,175,80,0.2)",  "#66bb6a"),
    "webhosting": ("Webhosting", "rgba(33,150,243,0.2)", "#64b5f6"),
    "devops":     ("DevOps",     "rgba(255,152,0,0.2)",  "#ffb74d"),
}

def insert_cards_into_index(articles):
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        text = f.read()
    for art in articles:
        cat = art["category"]
        cat_label, bg, fg = CATEGORY_STYLES[cat]
        sec_marker = f'<section class="cat-section" id="{cat}">'
        sec_start = text.find(sec_marker)
        if sec_start < 0:
            print(f"  ! section id={cat} not found")
            continue
        grid_marker = '<div class="blog-grid">'
        grid_pos = text.find(grid_marker, sec_start)
        if grid_pos < 0:
            print(f"  ! blog-grid not found inside {cat}")
            continue
        insert_at = grid_pos + len(grid_marker)
        card = card_html(art, cat_label, bg, fg)
        text = text[:insert_at] + "\n" + card + text[insert_at:]
        print(f"  + inserted card for {art['slug']} into {cat}")
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(text)

def update_artikel_json(articles):
    with open(ARTIKEL_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    existing_slugs = {a["slug"] for a in data}
    added = 0
    for a in articles:
        if a["slug"] in existing_slugs:
            print(f"  = skip {a['slug']} (already in json)")
            continue
        data.append(a)
        added += 1
        print(f"  + added {a['slug']} to artikel.json")
    with open(ARTIKEL_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return added

def update_sitemap(articles):
    with open(SITEMAP, "r", encoding="utf-8") as f:
        text = f.read()
    added = 0
    for a in articles:
        loc = f"https://hostazar.com/artikel/{a['slug']}.html"
        if loc in text:
            print(f"  = {loc} already in sitemap")
            continue
        block = (
            f"  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{LASTMOD}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.7</priority>\n"
            f"  </url>\n"
        )
        text = text.replace("</urlset>", block + "</urlset>")
        added += 1
        print(f"  + added {loc} to sitemap")
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(text)
    return added

def update_index_jsonld(articles):
    """Append BlogPosting JSON-LD entries to the existing JSON-LD array in index.html."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        text = f.read()
    # Find the closing </script> of the JSON-LD block (the one with BlogPosting array)
    # Look for the pattern: [`{"@context": "https://schema.org", "@type": "BlogPosting", ...}]
    # There are two JSON-LD blocks: 1st is WebSite, 2nd is the array of BlogPosting.
    # Find the second one.
    first_script_end = text.find("</script>")
    if first_script_end < 0:
        print("  ! no first </script> found")
        return 0
    second_script_start = text.find("<script", first_script_end)
    if second_script_start < 0:
        print("  ! no second <script> found")
        return 0
    second_inner_start = text.find(">", second_script_start) + 1
    second_inner_end = text.find("</script>", second_inner_start)
    if second_inner_end < 0:
        print("  ! no second </script> found")
        return 0
    
    inner = text[second_inner_start:second_inner_end].strip()
    # Try to parse as JSON - it's either an array or object
    # Existing content starts with [ or {...
    # Let's strip outer [ ] or just find the last entry
    
    # Extract the BlogPosting entries - they are in an array like:
    # [{"@context":..., "@type":"BlogPosting",...}, {...}]
    # We need to add new entries inside the array
    
    # Strategy: find the last } before the closing ] and add a comma + new entry
    # The inner script is like: [{"@context":..., ...}, {"@context":..., ...}]
    
    # Let's just append before the closing ]
    new_entries = []
    for a in articles:
        slug = a["slug"]
        title = a["title"]
        desc = a["excerpt"]
        entry = json.dumps({
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "url": f"https://hostazar.com/artikel/{slug}.html",
            "datePublished": a["date"],
            "dateModified": a["date"],
            "description": desc,
            "author": {"@type": "Organization", "name": "hostazar.com"}
        }, ensure_ascii=False)
        new_entries.append(entry)
    
    # Insert before the closing ]
    last_bracket = inner.rfind("]")
    if last_bracket < 0:
        print("  ! no closing bracket in JSON-LD")
        return 0
    
    # Add a comma before each new entry
    prefix = "," if inner[last_bracket-1] != "[" else ""
    insertion = prefix + ",".join(new_entries)
    new_inner = inner[:last_bracket] + insertion + inner[last_bracket:]
    
    text = text[:second_inner_start] + "\n  " + new_inner + "\n  " + text[second_inner_end:]
    
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"  + updated JSON-LD with {len(articles)} new entries")
    return len(articles)

def update_stat_bar():
    """Update the stat-bar article count."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        text = f.read()
    # Find current count and increase by 3
    # Pattern: <div class="stat-num">58</div>
    import re
    match = re.search(r'<div class="stat-num">(\d+)</div>', text)
    if match:
        current = int(match.group(1))
        new_count = current + 3
        text = text.replace(
            f'<div class="stat-num">{current}</div>',
            f'<div class="stat-num">{new_count}</div>',
            1  # only first occurrence
        )
        print(f"  + updated stat count from {current} to {new_count}")
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    print("=== Updating index.html (cards) ===")
    insert_cards_into_index(NEW_ARTICLES)
    print("\n=== Updating data/artikel.json ===")
    n1 = update_artikel_json(NEW_ARTICLES)
    print("\n=== Updating sitemap.xml ===")
    n2 = update_sitemap(NEW_ARTICLES)
    print("\n=== Updating JSON-LD in index.html ===")
    n3 = update_index_jsonld(NEW_ARTICLES)
    print("\n=== Updating stat count ===")
    update_stat_bar()
    print(f"\nDone. {n1} json + {n2} sitemap + {n3} JSON-LD entries added.")

if __name__ == "__main__":
    main()
