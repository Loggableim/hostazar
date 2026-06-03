#!/usr/bin/env python3
"""Generiert 25 neue hostazar.com SEO-Artikel über OpenRouter Free Models (parallel)"""
import json, os, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = '/c/HermesPortable/home/scripts/blog-automation/hostazar'
API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
if not API_KEY:
    with open('/c/HermesPortable/home/.env') as f:
        for line in f:
            if 'OPENROUTER_API_KEY' in line:
                API_KEY = line.strip().split('=', 1)[1].strip('\'"')
                break
MODEL = 'google/gemma-4-26b-a4b-it:free'

TOPICS = [
    {"slug":"the-forest-server-hosting","cat":"gaming","title":"The Forest Server hosten \u2013 Koop-Guide 2026","tags":"The Forest Server, Koop Survival Hosting, Forest Dedicated Server, The Forest mieten"},
    {"slug":"conan-exiles-server-hosten","cat":"gaming","title":"Conan Exiles Server mieten \u2013 Setup & Kosten 2026","tags":"Conan Exiles Server, Conan Exiles mieten, Conan Hosting, Survival Server Setup"},
    {"slug":"space-engineers-server","cat":"gaming","title":"Space Engineers Server mieten oder selbst hosten 2026","tags":"Space Engineers Server, Space Engineers Hosting, SE Server, Space Engineers mieten"},
    {"slug":"scum-server-mieten","cat":"gaming","title":"SCUM Server mieten \u2013 Anbieter, Kosten & Setup 2026","tags":"SCUM Server mieten, SCUM Hosting, SCUM Server Kosten, SCUM Dedicated Server"},
    {"slug":"icarus-server-hosting","cat":"gaming","title":"Icarus Server hosten \u2013 Dedicated Server f\u00fcr Koop 2026","tags":"Icarus Server, Icarus Hosting, Icarus Dedicated Server, Icarus Koop Server"},
    {"slug":"grounded-server-hosting","cat":"gaming","title":"Grounded Server hosten \u2013 Kosten, Setup & Anbieter 2026","tags":"Grounded Server, Grounded Hosting, Grounded Koop, Grounded Server mieten"},
    {"slug":"smalland-server-hosting","cat":"gaming","title":"Smalland Server mieten \u2013 Guide f\u00fcr den Koop-Server 2026","tags":"Smalland Server, Smalland Hosting, Smalland mieten, Smalland Koop Guide"},
    {"slug":"nightingale-server-hosting","cat":"gaming","title":"Nightingale Server hosten \u2013 Realm-Hosting-Guide 2026","tags":"Nightingale Server, Nightingale Hosting, Nightingale Realm, Nightingale mieten"},
    {"slug":"sons-of-the-forest-server","cat":"gaming","title":"Sons of the Forest Server hosten \u2013 Setup-Guide 2026","tags":"Sons of the Forest Server, SOTF Hosting, Sons of the Forest Dedicated Server"},
    {"slug":"cloudflare-tunnel-einrichten","cat":"webhosting","title":"Cloudflare Tunnel einrichten \u2013 Kostenloser Reverse Proxy 2026","tags":"Cloudflare Tunnel, Cloudflare Reverse Proxy, Tunnel einrichten, kostenloser Proxy"},
    {"slug":"plesk-vs-cpanel-vergleich","cat":"webhosting","title":"Plesk vs. cPanel \u2013 Der gro\u00dfe Hosting-Panel-Vergleich 2026","tags":"Plesk, cPanel, Hosting Panel, Server Verwaltung, Webhosting Vergleich"},
    {"slug":"mysql-mariadb-optimierung","cat":"webhosting","title":"MySQL & MariaDB optimieren \u2013 Performance-Guide 2026","tags":"MySQL Optimierung, MariaDB Tuning, Datenbank Performance, Query Optimierung"},
    {"slug":"nextcloud-server-einrichten","cat":"webhosting","title":"Nextcloud Server einrichten \u2013 Cloud-Speicher selbst hosten 2026","tags":"Nextcloud Server, Nextcloud einrichten, Cloud Speicher, Nextcloud Hosting"},
    {"slug":"webseite-sicherheit-2026","cat":"webhosting","title":"Webseite sichern \u2013 Security-Checkliste f\u00fcr deine Website 2026","tags":"Webseite Sicherheit, Website sch\u00fctzen, Hacking Schutz, Security Checkliste"},
    {"slug":"docker-wordpress-hosten","cat":"webhosting","title":"WordPress mit Docker hosten \u2013 Modernes Setup 2026","tags":"WordPress Docker, Docker Hosting, WordPress Container, Docker Compose WordPress"},
    {"slug":"cloud-hosting-vs-shared-hosting","cat":"webhosting","title":"Cloud Hosting vs. Shared Hosting \u2013 Vergleich 2026","tags":"Cloud Hosting, Shared Hosting, Hosting Vergleich, Cloud Server, Webhosting"},
    {"slug":"ansible-automation-guide","cat":"devops","title":"Ansible Automation \u2013 Grundlagen & Praxis-Guide 2026","tags":"Ansible, Automation, Konfigurationsmanagement, DevOps, Ansible Playbooks"},
    {"slug":"gitops-argocd-einrichten","cat":"devops","title":"GitOps mit ArgoCD \u2013 Kubernetes Deployment Guide 2026","tags":"GitOps, ArgoCD, Kubernetes Deployment, GitOps Workflow, Continuous Delivery"},
    {"slug":"linux-server-harden","cat":"devops","title":"Linux Server h\u00e4rten \u2013 Security-Baseline 2026","tags":"Linux Server h\u00e4rten, Server Security, Hardening Guide, Linux absichern"},
    {"slug":"postgresql-vps-optimierung","cat":"devops","title":"PostgreSQL auf dem VPS optimieren \u2013 Tuning-Guide 2026","tags":"PostgreSQL Tuning, PostgreSQL Optimierung, VPS Datenbank, Postgres Performance"},
    {"slug":"traefik-reverse-proxy","cat":"devops","title":"Traefik Reverse Proxy einrichten \u2013 Moderner Docker-Proxy 2026","tags":"Traefik, Reverse Proxy, Docker Proxy, Lets Encrypt Traefik, Load Balancer"},
    {"slug":"elk-stack-log-management","cat":"devops","title":"ELK Stack \u2013 Log-Management mit Elasticsearch & Kibana 2026","tags":"ELK Stack, Elasticsearch, Kibana, Logstash, Log Management, Server Logs"},
    {"slug":"wireguard-vpn-server","cat":"devops","title":"WireGuard VPN Server einrichten \u2013 Schnell & Sicher 2026","tags":"WireGuard, VPN Server, WireGuard einrichten, VPN Setup, Secure Tunnel"},
    {"slug":"n8n-automation-server","cat":"devops","title":"n8n Automation Server hosten \u2013 Workflow-Automatisierung 2026","tags":"n8n, Workflow Automation, n8n Server, Low Code Automation, Self Hosted n8n"},
]

NAV = '''<nav class="navbar">
  <div class="container">
    <a href="/" class="logo">hosta<span>zar</span></a>
    <ul class="nav-links">
      <li><a href="/">Startseite</a></li>
      <li class="nav-dropdown">
        <a href="/gaming/">Gaming</a>
        <div class="nav-dropdown-menu"><a href="/gaming/">🎮 Alle Gaming-Artikel</a></div>
      </li>
      <li class="nav-dropdown">
        <a href="/webhosting/">Webhosting</a>
        <div class="nav-dropdown-menu"><a href="/webhosting/">🌐 Alle Webhosting-Artikel</a></div>
      </li>
      <li class="nav-dropdown">
        <a href="/devops/">DevOps</a>
        <div class="nav-dropdown-menu"><a href="/devops/">⚙️ Alle DevOps-Artikel</a></div>
      </li>
      <li><a href="/about.html">Über uns</a></li>
      <li><a href="/impressum.html">Impressum</a></li>
    </ul>
  </div>
</nav>'''

FOOTER = '''<footer class="footer">
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

def h(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')

def call_api(prompt, max_tokens=1800):
    """Call OpenRouter free model and return text."""
    data = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Du bist ein deutscher SEO-Content-Autor für hostazar.com. Schreibe hochwertige, praxisnahe Hosting-Guides. Verwende SEO-Keywords natürlich. Antworten nur auf Deutsch."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read())
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content'].strip()
            if 'error' in result:
                err = result['error'].get('message', '')
                if 'rate' in err.lower():
                    time.sleep(10)
                    continue
                raise Exception(f"API error: {err[:200]}")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10)
                continue
            raise
        except urllib.error.URLError as e:
            time.sleep(5)
            continue
    raise Exception("API failed after 3 retries")

def generate_article_html(topic, content_text):
    """Assemble full HTML article from generated content."""
    slug = topic['slug']
    cat = topic['cat']
    title = topic['title']
    tags = topic['tags']
    canonical = f"https://hostazar.com/artikel/{slug}.html"
    description = content_text[:160].replace('\n', ' ').strip()
    if not description.endswith('.'):
        description += '.'
    
    kws = ', '.join([t.strip() for t in tags.split(',')])
    cat_label = {'gaming':'Gaming','webhosting':'Webhosting','devops':'DevOps'}[cat]
    cat_emoji = {'gaming':'🎮','webhosting':'🌐','devops':'⚙️'}[cat]
    
    # Split content into paragraphs
    paragraphs = [p.strip() for p in content_text.split('\n\n') if p.strip()]
    content_html = ''
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('## '):
            content_html += f'      <h2>{h(p[3:])}</h2>\n'
        elif p.startswith('### '):
            content_html += f'      <h3>{h(p[3:])}</h3>\n'
        elif p.startswith('- ') or p.startswith('* '):
            items = re.findall(r'^[-*] (.+)$', p, re.MULTILINE)
            if items:
                content_html += '      <ul>\n'
                for item in items:
                    content_html += f'        <li>{h(item)}</li>\n'
                content_html += '      </ul>\n'
            else:
                content_html += f'      <p>{h(p)}</p>\n'
        else:
            content_html += f'      <p>{h(p)}</p>\n'
    
    word_count = len(content_text.split())
    reading_min = max(3, word_count // 200)
    
    # Amazon affiliate links based on category
    amazon_tag = 'nova079-20'
    if cat == 'gaming':
        amazon_search = 'Gameserver+Hosting+Setup'
        amazon_label = 'Gaming-Zubehör & Server-Hardware'
    elif cat == 'webhosting':
        amazon_search = 'Webhosting+Server+Hardware'
        amazon_label = 'Server-Hardware & Hosting-Zubehör'
    else:
        amazon_search = 'DevOps+Server+Administration'
        amazon_label = 'Server-Administration & IT-Zubehör'
    
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h(title)} | hostazar.com</title>
  <meta name="description" content="{h(description)}">
  <meta name="keywords" content="{h(kws)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{h(canonical)}">
  <link rel="stylesheet" href="/css/style.css">

  <meta property="og:type" content="article">
  <meta property="og:url" content="{h(canonical)}">
  <meta property="og:title" content="{h(title)}">
  <meta property="og:description" content="{h(description)}">
  <meta property="og:image" content="https://hostazar.com/images/{slug}.png">
  <meta property="og:locale" content="de_DE">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{h(title)}">
  <meta name="twitter:description" content="{h(description)}">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{h(title)}",
    "url": "{h(canonical)}",
    "datePublished": "2026-06-15",
    "dateModified": "2026-06-15",
    "author": {{ "@type": "Organization", "name": "hostazar.com" }},
    "publisher": {{ "@type": "Organization", "name": "hostazar.com" }},
    "description": "{h(description)}",
    "image": "https://hostazar.com/images/{slug}.png",
    "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{h(canonical)}" }},
    "wordCount": {word_count},
    "articleSection": "{cat_label}",
    "inLanguage": "de"
  }}
  </script>
  <script src="/data/script.js" defer></script>
</head>
<body>

{NAV}

<main class="container article-page">
  <article>
    <div class="article-header">
      <div class="card-meta">
        <span class="card-tag {cat}">{cat_label}</span>
        <span>15. Juni 2026</span>
        <span>· {reading_min} Min Lesezeit</span>
      </div>
      <h1>{h(title)}</h1>
      <p style="color:var(--text-secondary);font-size:1.1rem">Alles zu Kosten, Setup, Anbietern und der richtigen Wahl f&uuml;r deinen {cat_label}-Server 2026.</p>
    </div>

    <div class="adsense-placeholder">
      <p><strong>&mdash; Anzeige &mdash;</strong></p>
      <p>Google AdSense Platzhalter</p>
    </div>

    <div id="breadcrumbs"></div>

    <div class="article-content">
{content_html}
    </div>

    <div class="affiliate-box">
      <p>{cat_emoji} Empfohlenes Zubeh&ouml;r</p>
      <p><strong>{h(amazon_label)}</strong> &ndash; Finde passende Hardware und Zubeh&ouml;r f&uuml;r dein Server-Projekt.</p>
      <a href="https://www.amazon.de/s?k={amazon_search}&amp;tag={amazon_tag}" target="_blank" rel="nofollow sponsored" class="btn">Auf Amazon entdecken &rarr;</a>
      <p style="margin-top:8px;font-size:0.75rem">* Affiliate-Link. Als Amazon-Partner verdienen wir an qualifizierten Verk&auml;ufen.</p>
    </div>

    <div class="amazon-affiliate" style="margin:30px 0;padding:15px;background:#f3e5f5;border:1px solid #9C27B0;border-radius:8px;text-align:center">
      <p><strong>{cat_emoji} Mehr zum Thema auf Amazon</strong></p>
      <p><a href="https://www.amazon.de/s?k={amazon_search}&amp;tag={amazon_tag}" target="_blank" rel="nofollow sponsored">Zu den Produkten auf Amazon &rarr;</a></p>
    </div>

    <div id="related-articles"></div>

    <div class="adsense-placeholder">
      <p><strong>&mdash; Anzeige &mdash;</strong></p>
      <p>Google AdSense Platzhalter (Ende des Artikels)</p>
    </div>

  </article>
</main>

{FOOTER}

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
        {{ url: '/{cat}/', label: '{cat_label}' }},
        {{ label: '{h(title)}' }}
      ]
    }});
  }}
}});
</script>
</body>
</html>'''
    return html

def generate_one(topic):
    """Generate one article: API call + HTML assembly + file write."""
    slug = topic['slug']
    path = os.path.join(REPO, 'artikel', f'{slug}.html')
    if os.path.exists(path) and os.path.getsize(path) > 3000:
        print(f"  SKIP {slug} (already exists)")
        return slug, True
    
    cat = topic['cat']
    cat_label = {'gaming':'Gaming','webhosting':'Webhosting','devops':'DevOps'}[cat]
    
    prompt = f"""Schreibe einen deutschen SEO-Artikel (ca. 500-700 Wörter) zum Thema "{topic['title']}" für hostazar.com.

Kategorie: {cat_label}
Zielgruppe: Deutsche Spieler/Admins, die einen {cat_label}-Server suchen.
Tone: Praxisnah, informativ, leicht verständlich.

Strukturiere den Artikel mit Überschriften (## und ###):
- Einleitung (warum dieses Thema wichtig ist)
- 3-4 Hauptabschnitte mit praktischen Infos (Kosten, Setup, Anbieter, Tipps)
- Fazit mit Empfehlung

Wichtige Keywords natürlich einbauen: {topic['tags']}

Schreibe nur den Artikeltext mit Markdown-Überschriften (## für H2, ### für H3). Kein HTML, keine Einleitung/Abschluss-Bemerkungen."""
    
    try:
        print(f"  Generating {slug}...")
        content = call_api(prompt)
        if not content or len(content) < 200:
            print(f"  WARNING: {slug} too short ({len(content)} chars), retrying...")
            content = call_api(prompt, 2000)
        
        html = generate_article_html(topic, content)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        words = len(content.split())
        print(f"  OK {slug} - {words} Wörter")
        return slug, True
    except Exception as e:
        print(f"  FAIL {slug}: {e}")
        return slug, False

def generate_all():
    """Generate all articles using parallel workers."""
    total = len(TOPICS)
    print(f"Generiere {total} Artikel mit Modell {MODEL}")
    print(f"Workers: 3 parallel\n")
    
    results = {'ok': 0, 'fail': 0, 'skip': 0}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_one, t): t for t in TOPICS}
        for future in as_completed(futures):
            slug, success = future.result()
            if slug == 'SKIP':
                results['skip'] += 1
            elif success:
                results['ok'] += 1
            else:
                results['fail'] += 1
    
    print(f"\nErgebnis: {results['ok']} OK, {results['fail']} fehlgeschlagen, {results['skip']} übersprungen")
    return results

if __name__ == '__main__':
    generate_all()
