#!/usr/bin/env python3
"""Generate 9 German SEO articles for hostazar.com gaming category."""

import json
import os
import sys
import html as html_mod

# Provider-Helper aus dem Framework laden
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_framework'))
from provider_pool import llm_chat

OUT_DIR = "/c/HermesPortable/home/scripts/blog-automation/hostazar/artikel"

ARTICLES = [
    {
        "slug": "the-forest-server-hosting",
        "title": "The Forest Server hosten – Koop-Guide 2026",
        "tags": "The Forest Server, Koop Server, Survival Server mieten, The Forest Dedicated Server, Sons of the Forest Hosting",
        "category": "gaming",
        "desc": "The Forest Server hosten – Koop-Guide 2026. Kosten, Setup, Anbieter und Tipps für den perfekten Survival-Koop-Server.",
        "h1": "The Forest Server hosten – Koop-Guide 2026",
        "subtitle": "Setup, Kosten & Anbieter – So startest du deinen eigenen The Forest Koop-Server"
    },
    {
        "slug": "conan-exiles-server-hosten",
        "title": "Conan Exiles Server mieten – Setup & Kosten 2026",
        "tags": "Conan Exiles Server, Conan Exiles Hosting, Conan Exiles mieten, Survival Server, Conan Exiles Setup",
        "category": "gaming",
        "desc": "Conan Exiles Server mieten – Setup & Kosten 2026. Schritt-für-Schritt-Anleitung für deinen eigenen Conan Exiles Survival-Server.",
        "h1": "Conan Exiles Server mieten – Setup & Kosten 2026",
        "subtitle": "Vergleich der besten Anbieter, Kostenübersicht und Konfiguration für Conan Exiles"
    },
    {
        "slug": "space-engineers-server",
        "title": "Space Engineers Server mieten oder selbst hosten 2026",
        "tags": "Space Engineers Server, Space Engineers mieten, Space Engineers Hosting, SE Server Setup, Survival Server",
        "category": "gaming",
        "desc": "Space Engineers Server mieten oder selbst hosten 2026. Guide mit Kosten, Setup und Empfehlungen für deine Raumfahrt-Welten.",
        "h1": "Space Engineers Server mieten oder selbst hosten 2026",
        "subtitle": "Kosten, Performance und Setup – Die beste Wahl für deinen SE-Server"
    },
    {
        "slug": "scum-server-mieten",
        "title": "SCUM Server mieten – Anbieter, Kosten & Setup 2026",
        "tags": "SCUM Server mieten, SCUM Hosting, SCUM Server Kosten, Survival Server, SCUM Dedicated Server",
        "category": "gaming",
        "desc": "SCUM Server mieten – Anbieter, Kosten & Setup 2026. Der ultimative Guide für deinen SCUM Dedicated Server.",
        "h1": "SCUM Server mieten – Anbieter, Kosten & Setup 2026",
        "subtitle": "Finde den besten SCUM Server – Inklusive Kostenvergleich und Einrichtungsanleitung"
    },
    {
        "slug": "icarus-server-hosting",
        "title": "Icarus Server hosten – Dedicated Server für Koop 2026",
        "tags": "Icarus Server, Icarus Hosting, Icarus Dedicated Server, Icarus Koop Server, Survival Game Hosting",
        "category": "gaming",
        "desc": "Icarus Server hosten – Dedicated Server für Koop 2026. Setup-Guide und Anbietervergleich für deinen Icarus-Prospektor-Server.",
        "h1": "Icarus Server hosten – Dedicated Server für Koop 2026",
        "subtitle": "Setup, Kosten & beste Anbieter für deinen Icarus-Server"
    },
    {
        "slug": "grounded-server-hosting",
        "title": "Grounded Server hosten – Kosten, Setup & Anbieter 2026",
        "tags": "Grounded Server, Grounded Hosting, Grounded Koop Server, Grounded mieten, Survival Server Hosting",
        "category": "gaming",
        "desc": "Grounded Server hosten – Kosten, Setup & Anbieter 2026. Alles für deinen eigenen Grounded Koop-Server im Garten.",
        "h1": "Grounded Server hosten – Kosten, Setup & Anbieter 2026",
        "subtitle": "So wird dein Garten-Abenteuer zum perfekten Koop-Erlebnis"
    },
    {
        "slug": "smalland-server-hosting",
        "title": "Smalland Server mieten – Guide für den Koop-Server 2026",
        "tags": "Smalland Server, Smalland Hosting, Smalland Koop, Smalland mieten, Survival Server Guide",
        "category": "gaming",
        "desc": "Smalland Server mieten – Guide für den Koop-Server 2026. Alles zu Setup, Kosten und den besten Anbietern.",
        "h1": "Smalland Server mieten – Guide für den Koop-Server 2026",
        "subtitle": "Deine Miniatur-Welt wartet – Der komplette Smalland Hosting-Guide"
    },
    {
        "slug": "nightingale-server-hosting",
        "title": "Nightingale Server hosten – Realm-Hosting-Guide 2026",
        "tags": "Nightingale Server, Nightingale Hosting, Nightingale Realm, Nightingale Koop, Survival Crafting Server",
        "category": "gaming",
        "desc": "Nightingale Server hosten – Realm-Hosting-Guide 2026. Einrichtung, Kosten und Tipps für dein eigenes Nightingale Realm.",
        "h1": "Nightingale Server hosten – Realm-Hosting-Guide 2026",
        "subtitle": "Betrete dein eigenes Realm – Der ultimative Nightingale Hosting-Guide"
    },
    {
        "slug": "sons-of-the-forest-server",
        "title": "Sons of the Forest Server hosten – Vollständiger Setup-Guide 2026",
        "tags": "Sons of the Forest Server, SOTF Hosting, Sons of the Forest Dedicated Server, Koop Hosting, Survival Server Setup",
        "category": "gaming",
        "desc": "Sons of the Forest Server hosten – Vollständiger Setup-Guide 2026. Anleitung für deinen SOTF Dedicated Server mit Freunden.",
        "h1": "Sons of the Forest Server hosten – Vollständiger Setup-Guide 2026",
        "subtitle": "Von der Installation bis zur Konfiguration – Alles für deinen SOTF-Server"
    }
]

# ===== TEMPLATE PARTS =====

HEAD_OPEN = '''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | hostazar.com</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{tags}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://hostazar.com/artikel/{slug}.html">
  <link rel="stylesheet" href="/css/style.css">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://hostazar.com/artikel/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://hostazar.com/images/{slug}.png">
  <meta property="og:locale" content="de_DE">

  <!-- Article JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "url": "https://hostazar.com/artikel/{slug}.html",
    "datePublished": "2026-06-15",
    "dateModified": "2026-06-15",
    "author": {{ "@type": "Organization", "name": "hostazar.com" }},
    "publisher": {{ "@type": "Organization", "name": "hostazar.com" }},
    "description": "{desc}",
    "image": "https://hostazar.com/images/{slug}.png",
    "mainEntityOfPage": {{ "@type": "WebPage", "@id": "https://hostazar.com/artikel/{slug}.html" }},
    "wordCount": {wordcount},
    "inLanguage": "de"
  }}
  </script>
  <script src="/data/script.js" defer></script>
</head>
<body>

<!-- Navigation -->
<nav class="navbar">
  <div class="container">
    <a href="/" class="logo">hosta<span>zar</span></a>
    <ul class="nav-links">
      <li><a href="/">Startseite</a></li>
      <li><a href="/#gaming" class="active">Gaming</a></li>
      <li><a href="/#webhosting">Webhosting</a></li>
      <li><a href="/#devops">DevOps</a></li>
      <li><a href="/about.html">Über uns</a></li>
      <li><a href="/impressum.html">Impressum</a></li>
    </ul>
  </div>
</nav>

<main class="container article-page">
  <article>
    <div class="article-header">
      <div class="card-meta">
        <span class="card-tag gaming">Gaming</span>
        <span>15. Juni 2026</span>
        <span>· {readtime} Min Lesezeit</span>
      </div>
      <h1>{h1}</h1>
      <p style="color:var(--text-secondary);font-size:1.1rem">{subtitle}</p>
    </div>

    <!-- AdSense Placeholder -->
    <div class="adsense-placeholder">
      <p><strong>— Anzeige —</strong></p>
      <p>Google AdSense Platzhalter</p>
    </div>

    <div id="breadcrumbs"></div>

    <div class="article-content">
'''

FOOTER_HTML = '''    </div>

    <!-- Related Articles -->
    <div id="related-articles"></div>

    <!-- Amazon Affiliate Block -->
    <div class="amazon-affiliate" style="margin:30px 0;padding:15px;background:#f3e5f5;border:1px solid #9C27B0;border-radius:8px;text-align:center">
      <p><strong>🎮 {amazon_title}</strong></p>
      <p><a href="{amazon_url}" target="_blank" rel="nofollow">👉 {amazon_cta}</a></p>
    </div>

    <!-- AdSense Platzhalter unten -->
    <div class="adsense-placeholder">
      <p><strong>— Anzeige —</strong></p>
      <p>Google AdSense Platzhalter (Ende des Artikels)</p>
    </div>

  </article>
</main>

<!-- Footer -->
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>hosta<span style="color:var(--accent)">zar</span></h4>
        <p style="color:var(--text-muted);font-size:0.9rem">Dein Hosting- &amp; Server-Portal mit Guides, Vergleichen und Tutorials.</p>
      </div>
      <div>
        <h4>Kategorien</h4>
        <ul>
          <li><a href="/#gaming">🎮 Gaming</a></li>
          <li><a href="/#webhosting">🌐 Webhosting</a></li>
          <li><a href="/#devops">⚙️ DevOps</a></li>
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
      <span>Made with ❤️ f&uuml;r die Hosting-Community</span>
    </div>
    <p class="affiliate-note">* Bei den mit Sternchen gekennzeichneten Links handelt es sich um Affiliate-Links. Wenn du &uuml;ber diese Links einkaufst, erhalten wir eine kleine Provision &ndash; f&uuml;r dich entstehen keine Mehrkosten. Als Amazon-Partner verdienen wir an qualifizierten Verk&auml;ufen.</p>
  </div>
</footer>

<script>
  document.addEventListener('DOMContentLoaded', function () {
    if (typeof hostazarApp !== 'undefined' && hostazarApp.init) {
      hostazarApp.init();
    }
  });
</script>
</body>
</html>'''


def build_article_html(slug, title, tags, desc, h1, subtitle, content, wordcount, readtime):
    """Build the complete HTML article from components."""
    amazon_kw = slug.replace("-", " ").title()
    amazon_title = f"{amazon_kw} Gaming-Zubehör & Server-Hardware"
    amazon_url = f"https://www.amazon.de/s?k={amazon_kw.replace(' ', '+')}+Server+Hardware&amp;tag=nova079-20"
    amazon_cta = f"Alles f&uuml;r deinen {amazon_kw} Server auf Amazon entdecken"

    head = HEAD_OPEN.format(
        title=title,
        desc=desc,
        tags=tags,
        slug=slug,
        h1=h1,
        subtitle=subtitle,
        wordcount=wordcount,
        readtime=readtime
    )

    return head + content.strip() + "\n\n" + FOOTER_HTML.format(
        amazon_title=amazon_title,
        amazon_url=amazon_url,
        amazon_cta=amazon_cta
    )


def call_llm(prompt, system_msg="Du bist ein deutscher SEO-Content-Autor für hostazar.com. Schreibe informativ, detailliert und suchmaschinenoptimiert auf Deutsch."):
    """Call LLM via the Framework Provider-Pool (NVIDIA/Gemini priority)."""
    return llm_chat(
        system_prompt=system_msg,
        user_prompt=prompt,
        provider="content",
        max_tokens=4096,
        temperature=0.7,
    )


def generate_article_content(article):
    """Generate full HTML content for one article via the LLM."""
    slug = article["slug"]
    title = article["title"]
    tags = article["tags"]
    h1 = article["h1"]
    subtitle = article["subtitle"]

    prompt = f"""Schreibe einen deutschen SEO-Artikel für hostazar.com zum Thema: "{title}"

Titel: {title}
Meta-Beschreibung: {article['desc']}
Tags: {tags}
Kategorie: Gaming

Anforderungen:
- Länge: ca. 500-700 Wörter, aber mindestens 4000 Zeichen Inhalt
- Schreibe NUR den Inhalt für <div class="article-content">, keine umschließenden HTML-Tags
- Verwende ausschließlich HTML-Formatierung: <p>, <h2>, <h3>, <ul>/<li>, <ol>/<li>, <table>, <div class="highlight-box">
- Amazon Affiliate-Links mit tag=nova079-20 (als &amp;tag=nova079-20)
- Deutsche Sprache, SEO-optimiert mit den Keywords aus den Tags
- Enthülle KEINE Platzhalter wie "Amazon Affiliate Block" - schreibe nur echten Content
- Verwende <h2> und <h3> Überschriften
- Baue eine Vergleichstabelle (<table>) ein
- Baue mindestens eine highlight-box ein
- Verwende konkrete Anbieter wie Nitrado, G-Portal, Zap-Hosting, 4Netplayers
- Affiliate-Empfehlungen für Gaming-Hardware auf Amazon mit &amp;tag=nova079-20
- Faktenbasiert, hilfreich, direkt

Schreibe jetzt den HTML-Inhalt (NUR den Content für article-content, ohne article-content wrapper):"""

    print(f"  Calling API for '{title}'...")
    content = call_llm(prompt)
    wordcount = len(content.split())
    readtime = max(6, (wordcount // 130) + 1)

    print(f"  Generated {wordcount} words, ~{readtime} min read")

    extra_prompt = f"""Ergänze den folgenden Artikel-Entwurf zu "{title}" mit:
- Einer zusätzlichen checklisten-artigen Vergleichstabelle mit mindestens 6 Kriterien
- Einem Abschnitt "Die besten Anbieter" mit min 4 Anbietern und Preisen
- Einem abschließenden Fazit (2-3 Absätze)
- Gesamt soll der Artikel ca. 700 Wörter haben

Vorhandener Content:
{content}

Schreibe den KOMPLETTEN, erweiterten HTML-Content (nur article-content innerer Bereich) neu - füge alles zusammen:"""

    print(f"  Expanding article...")
    content = call_llm(extra_prompt)
    wordcount = len(content.split())
    readtime = max(6, (wordcount // 130) + 1)
    print(f"  Final: {wordcount} words, ~{readtime} min read")

    return content, wordcount, readtime


def main():
    print(f"=== Generating {len(ARTICLES)} articles for hostazar.com ===\n")
    os.makedirs(OUT_DIR, exist_ok=True)

    for i, article in enumerate(ARTICLES, 1):
        slug = article["slug"]
        filepath = os.path.join(OUT_DIR, f"{slug}.html")

        print(f"\n[{i}/{len(ARTICLES)}] {article['title']}")
        print(f"  Slug: {slug}")

        # Check if already exists
        if os.path.exists(filepath):
            print(f"  File exists, overwriting...")

        try:
            content, wordcount, readtime = generate_article_content(article)

            full_html = build_article_html(
                slug=slug,
                title=article["title"],
                tags=article["tags"],
                desc=article["desc"],
                h1=article["h1"],
                subtitle=article["subtitle"],
                content=content,
                wordcount=wordcount,
                readtime=readtime
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_html)

            size = os.path.getsize(filepath)
            print(f"  ✓ Saved: {filepath} ({size} bytes)")

        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            # Continue with next article

        # Rate limiting delay between articles
        if i < len(ARTICLES):
            print("  Waiting 3s before next article...")
            import time
            time.sleep(3)

    print("\n=== All done! ===")


if __name__ == "__main__":
    main()