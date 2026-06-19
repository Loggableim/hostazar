#!/usr/bin/env python3
"""Generate RSS 2.0 feed.xml for hostazar.com from artikel/*.html"""
import os, re, datetime, html as html_mod

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, "artikel")
SITE = "https://hostazar.com"
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

items = []
for f in sorted(os.listdir(ARTIKEL_DIR), reverse=True):
    if not f.endswith(".html"): continue
    fp = os.path.join(ARTIKEL_DIR, f)
    with open(fp, "r", encoding="utf-8") as fh:
        c = fh.read()

    title = ""
    t = re.search(r"<title>(.*?)\s*\| hostazar", c)
    if t: title = t.group(1).strip()

    desc = ""
    d = re.search(r'name="description"\s*content="([^"]+)"', c)
    if d: desc = d.group(1)

    pubdate = NOW
    p = re.search(r'"datePublished":\s*"([^"]+)"', c)
    if p:
        d = p.group(1)
        try:
            dt = datetime.datetime.strptime(d, "%Y-%m-%d")
            pubdate = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except: pass

    slug = f.replace(".html", "")
    url = f"{SITE}/artikel/{slug}.html"
    og_img = f"{SITE}/images/{slug}.webp"

    # First 30 words of desc as excerpt
    excerpt = " ".join(desc.split()[:30]) + "…" if desc else title

    # Get H2s for content overview in feed
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", c)
    h2_stripped = []
    for h in h2s[:3]:
        h2_stripped.append(re.sub(r"<[^>]+>", "", h).strip())
    cat_match = re.search(r'class="card-tag[^"]*"[^>]*>(\w+)', c)
    cat = cat_match.group(1) if cat_match else "Hosting"
    escaped_cat = html_mod.escape(cat)

    item = f"""  <item>
    <title>{html_mod.escape(title)}</title>
    <link>{url}</link>
    <guid isPermaLink="true">{url}</guid>
    <description>{html_mod.escape(excerpt)}</description>
    <pubDate>{pubdate}</pubDate>
    <source url="{SITE}/feed.xml">hostazar.com</source>
    <category>{escaped_cat}</category>
    <enclosure url="{og_img}" type="image/webp" length="0"/>
  </item>"""
    items.append(item)

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>hostazar.com — Hosting &amp; Server Portal</title>
    <link>{SITE}</link>
    <description>Unabhängige Hosting-Reviews, Gameserver-Guides und DevOps-Tutorials. Transparent, testbench-basiert.</description>
    <language>de</language>
    <lastBuildDate>{NOW}</lastBuildDate>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>{SITE}/favicon.ico</url>
      <title>hostazar.com</title>
      <link>{SITE}</link>
    </image>
{chr(10).join(items)}
  </channel>
</rss>"""

with open(os.path.join(REPO, "feed.xml"), "w", encoding="utf-8") as f:
    f.write(feed)

count = len(items)
print(f"✅ feed.xml generiert — {count} Artikel", flush=True)
