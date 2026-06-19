#!/usr/bin/env python3
"""
MiniMax-M3 Cron: Generate 4 new hostazar articles + hero images.
Runs from cron, commits + pushes to GitHub → auto-deploy via CF Pages.
"""
import json, urllib.request, time, os, re, sys, datetime
from io import BytesIO
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, "artikel")
IMG_DIR = os.path.join(REPO, "images")
SITE = "https://hostazar.com"
TODAY = datetime.date.today().isoformat()

KEY = re.search(r"MINIMAX_API_KEY=(\S+)", open("C:/sidekick/home/.env").read()).group(1)

STYLE_IMG = "furry editorial illustration, anthropomorphic animal characters, black and white artwork with a single accent color, bold black ink outlines, high contrast monochrome shading, clean vector illustration, graphic novel aesthetics"

# ── Article Topics ──────────────────────────────────────────
# Rotating pool — pick 4 each run, avoid duplicates with existing slugs
TOPIC_POOL = [
    ("soulmask-server-hosting-2026", "Soulmask Server hosten – Dedicated Server Guide 2026", "gaming"),
    ("enshrouded-dedicated-server-2026", "Enshrouded Dedicated Server – Setup & Hosting 2026", "gaming"),
    ("palworld-performance-optimierung-2026", "Palworld Server Performance optimieren – Tuning-Guide 2026", "gaming"),
    ("vps-kubernetes-einsteiger-2026", "Kubernetes auf VPS für Einsteiger – Cluster-Setup 2026", "devops"),
    ("docker-swarm-vs-kubernetes-2026", "Docker Swarm vs Kubernetes – Orchestrierung im Vergleich 2026", "devops"),
    ("vps-monitoring-alerting-2026", "VPS Monitoring & Alerting – Das richtige Setup 2026", "devops"),
    ("cloudflare-r2-vps-backup-2026", "Cloudflare R2 als VPS-Backup – Storage-Guide 2026", "webhosting"),
    ("vps-nginx-tuning-2026", "Nginx auf dem VPS optimieren – Performance-Tuning 2026", "webhosting"),
    ("vps-wordpress-sicherheit-2026", "WordPress auf VPS absichern – Security-Guide 2026", "webhosting"),
    ("gameserver-ddos-schutz-cloudflare-2026", "Gameserver DDoS-Schutz mit Cloudflare – Setup 2026", "gaming"),
    ("vps-postgresql-replikation-2026", "PostgreSQL Replikation auf VPS – Master-Slave Setup 2026", "devops"),
    ("docker-compose-produktion-2026", "Docker Compose für Produktion – Best Practices 2026", "devops"),
    ("minecraft-server-performance-2026", "Minecraft Server Performance optimieren – Guide 2026", "gaming"),
    ("vps-kubernetes-monitoring-2026", "Kubernetes Monitoring auf VPS – Prometheus & Grafana 2026", "devops"),
    ("nextcloud-s3-speicher-2026", "Nextcloud mit S3-Speicher nutzen – Cloud-Integration 2026", "webhosting"),
    ("vps-docker-registry-eigenen-2026", "Eigene Docker Registry auf VPS betreiben – Guide 2026", "devops"),
]

def call_minimax(prompt):
    data = json.dumps({"model": "MiniMax-M3", "messages": [
        {"role": "system", "content": "Du bist ein deutscher SEO-Content-Autor für hostazar.com. Schreibe detaillierte, praxisnahe Guides mit konkreten Zahlen, Befehlen und Vergleichen."},
        {"role": "user", "content": prompt}
    ], "max_tokens": 8192, "temperature": 0.7}).encode()
    req = urllib.request.Request("https://api.minimax.io/v1/chat/completions", data=data,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=300).read())
    return resp["choices"][0]["message"]["content"]

def call_minimax_img(slug):
    """Generate hero image via MiniMax image-01."""
    prompt = f"anthropomorphic {slug.replace('-',' ')} scene, server hosting, technology concept, {STYLE_IMG}"
    data = json.dumps({"model": "image-01", "prompt": prompt, "aspect_ratio": "16:9", "n": 1}).encode()
    req = urllib.request.Request("https://api.minimax.io/v1/image_generation", data=data,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
    url = resp["data"]["image_urls"][0]
    img = Image.open(BytesIO(urllib.request.urlopen(url, timeout=60).read()))
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255,255,255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img = img.resize((1216, 832), Image.LANCZOS)
    img.save(os.path.join(IMG_DIR, f"{slug}.png"), "PNG", optimize=True)
    img.save(os.path.join(IMG_DIR, f"{slug}.webp"), "WEBP", quality=92, method=6)

def build_html(slug, title, category, content_html, desc):
    """Wrap content in full HTML shell with nav, footer, schema."""
    img = f"{SITE}/images/{slug}.webp"
    
    # Load existing shell from another article for nav/footer
    existing = [f for f in os.listdir(ARTIKEL_DIR) if f.endswith(".html")]
    if existing:
        with open(os.path.join(ARTIKEL_DIR, existing[0])) as f:
            shell = f.read()
        nav = ""
        n = re.search(r"(<nav class=\"navbar\">.*?</nav>)", shell, re.DOTALL)
        if n: nav = n.group(1)
        footer = ""
        f = re.search(r"(<footer class=\"footer\">.*?</footer>)", shell, re.DOTALL)
        if f: footer = f.group(1)
    else:
        nav = '<nav class="navbar"><div class="container"><a href="/" class="logo">hosta<span>zar</span></a></div></nav>'
        footer = '<footer class="footer"><div class="container"><p>&copy; 2026 hostazar.com</p></div></footer>'
    
    cat_upper = category.title()
    
    full = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | hostazar.com</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE}/artikel/{slug}.html">
  <link rel="stylesheet" href="/css/style.css">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/artikel/{slug}.html">
  <meta property="og:title" content="{title} | hostazar.com">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Hostazar &mdash; VPS &amp; DevOps Portal">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | hostazar.com">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{img}">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "url": "{SITE}/artikel/{slug}.html",
    "description": "{desc}",
    "inLanguage": "de",
    "datePublished": "{TODAY}",
    "dateModified": "{TODAY}",
    "image": "{img}",
    "author": {{ "@type": "Organization", "name": "hostazar.com" }},
    "publisher": {{ "@type": "Organization", "name": "hostazar.com" }}
  }}
  </script>
</head>
<body>
{nav}
<main class="article-page">
  <div class="container">
    <div class="article-meta-top">
      <span class="card-tag {category}" style="background:var(--accent-dim);color:var(--accent)">{cat_upper}</span>
      <span>12 Min Lesezeit</span>
    </div>
    <h1>{title}</h1>
    <div class="article-body">
{content_html}
    </div>
  </div>
</main>
{footer}
</body>
</html>"""
    return full


# ── MAIN ──────────────────────────────────────────────────
# Pick 4 topics that don't exist yet
existing_slugs = set(f.replace(".html", "") for f in os.listdir(ARTIKEL_DIR) if f.endswith(".html"))
available = [t for t in TOPIC_POOL if t[0] not in existing_slugs]
selected = available[:4]

if len(selected) < 4:
    print(f"⚠️ Nur {len(selected)} neue Topics verfügbar", flush=True)
    if len(selected) == 0:
        print("❌ Keine neuen Topics — TOPIC_POOL erweitern!", flush=True)
        sys.exit(0)

print(f"Generiere {len(selected)} neue Artikel:", flush=True)

for slug, title, category in selected:
    print(f"\n  [{slug}] {title}", flush=True)
    
    # Step 1: Content via MiniMax-M3
    prompt = f"""Schreibe einen detaillierten deutschen SEO-Guide für: {title}
    
Anforderungen:
- 8-12 H2-Überschriften mit je 3-5 Absätzen
- Konkrete Zahlen, Befehle, Preisangaben
- Tabellen wo Vergleiche, Code-Blöcke wo technisch
- Nutze <h2>, <p>, <table>, <ul>, <pre><code> Tags
- Max 3000 Wörter
- NUR Article-Body HTML, kein <h1>, keine Navigation"""
    
    t0 = time.time()
    content = call_minimax(prompt)
    content = re.sub(r"<think>.*?</think>|```html\s*|```", "", content, flags=re.DOTALL).strip()
    h2_start = content.find("<h2")
    if h2_start > 0:
        content = content[h2_start:]
    print(f"    ✅ Content ({len(content)} chars, {time.time()-t0:.0f}s)", flush=True)
    
    # Step 2: Extract description
    desc = title
    first_p = re.search(r"<p>(.*?)</p>", content)
    if first_p:
        desc = re.sub(r"<[^>]+>", "", first_p.group(1))[:160]
    
    # Step 3: Build HTML
    html = build_html(slug, title, category, content, desc)
    with open(os.path.join(ARTIKEL_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    
    # Step 4: Generate hero image (separate RPM window)
    time.sleep(30)  # avoid image-01 RPM
    try:
        call_minimax_img(slug)
        print(f"    ✅ Hero-Image", flush=True)
    except Exception as e:
        print(f"    ⚠️ Image failed: {e}", flush=True)

print(f"\n✅ {len(selected)} Artikel generiert!", flush=True)
