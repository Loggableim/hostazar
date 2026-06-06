#!/usr/bin/env python3
"""Insert 3 new article cards into hostazar.com index.html + update JSON / sitemap."""
import os, json, re, html

REPO = r"C:\HermesPortable\home\scripts\blog-automation\hostazar"
ARTIKEL_JSON = os.path.join(REPO, "data", "artikel.json")
INDEX_HTML = os.path.join(REPO, "index.html")
SITEMAP = os.path.join(REPO, "sitemap.xml")

NEW_ARTICLES = [
    {
        "slug": "dedizierter-server-vs-vps-2026",
        "title": "Dedizierter Server vs. VPS – Der große Vergleich 2026",
        "category": "devops",
        "tags": ["Dedicated Server", "VPS Vergleich", "Root Server", "Server Hosting 2026", "Hetzner", "Contabo"],
        "excerpt": "Dedizierter Server vs. VPS 2026: Ausführlicher Vergleich mit Kosten, Performance, Vor-/Nachteilen und Anbieter-Tabelle. Welcher Server passt zu dir?",
        "date": "2026-06-06",
        "readingTime": "9",
        "image": "dedizierter-server-vs-vps-2026.png",
    },
    {
        "slug": "ddos-schutz-gameserver-2026",
        "title": "DDoS-Schutz für Gameserver – Anbieter & Konfiguration 2026",
        "category": "gaming",
        "tags": ["DDoS Schutz Gameserver", "Game DDoS Protection", "OVH DDoS", "TCPShield", "Minecraft DDoS"],
        "excerpt": "DDoS-Schutz für Gameserver 2026: Anbieter-Vergleich (OVH, Hetzner, G-Portal, TCPShield), Konfiguration mit iptables/nftables und Best Practices gegen Angriffe.",
        "date": "2026-06-06",
        "readingTime": "10",
        "image": "ddos-schutz-gameserver-2026.png",
    },
    {
        "slug": "minecraft-bedrock-vs-java-server-2026",
        "title": "Minecraft Bedrock vs. Java Server – Unterschiede & Hosting 2026",
        "category": "gaming",
        "tags": ["Minecraft Bedrock vs Java", "Minecraft Server Vergleich", "Java Edition Server", "Bedrock Server", "GeyserMC", "Crossplay Minecraft"],
        "excerpt": "Minecraft Bedrock vs. Java Server 2026: Vergleich von Performance, Mods, Crossplay, Hosting-Anforderungen, Server-Software (Spigot, Paper, BDS) und Kosten.",
        "date": "2026-06-06",
        "readingTime": "10",
        "image": "minecraft-bedrock-vs-java-server-2026.png",
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
          <img src="/images/{img}" alt="{h(title)}" loading="lazy" onerror="this.parentElement.innerHTML='<span class=\'placeholder-icon\'>{cat_label.split()[0]}</span>'">
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

    # find the blog-grid opening inside each section by category id
    for art in articles:
        cat = art["category"]
        cat_label, bg, fg = CATEGORY_STYLES[cat]
        # Locate the section start, then find the next <div class="blog-grid"> after it
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
    lastmod = "2026-06-06T15:00:00+00:00"
    added = 0
    for a in articles:
        loc = f"https://hostazar.com/artikel/{a['slug']}.html"
        if loc in text:
            print(f"  = {loc} already in sitemap")
            continue
        block = (
            f"  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.7</priority>\n"
            f"  </url>\n"
        )
        # insert before closing </urlset>
        text = text.replace("</urlset>", block + "</urlset>")
        added += 1
        print(f"  + added {loc} to sitemap")
    with open(SITEMAP, "w", encoding="utf-8") as f:
        f.write(text)
    return added


def main():
    print("=== Updating index.html ===")
    insert_cards_into_index(NEW_ARTICLES)
    print("\n=== Updating data/artikel.json ===")
    n1 = update_artikel_json(NEW_ARTICLES)
    print("\n=== Updating sitemap.xml ===")
    n2 = update_sitemap(NEW_ARTICLES)
    print(f"\nDone. {n1} json + {n2} sitemap entries added.")


if __name__ == "__main__":
    main()
