import os, sys, json, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = '/c/HermesPortable/home/scripts/blog-automation/hostazar'
import os; API_KEY = os.environ.get("OPENROUTER_API_KEY","")
with open('/c/HermesPortable/home/.env') as f:
    for line in f:
        if 'OPENROUTER_API_KEY' in line:
            API_KEY = line.strip().split('=', 1)[1].strip('\'"')
if not API_KEY:
    import os; API_KEY = os.environ.get("OPENROUTER_API_KEY","")
    print("NO API KEY")
    sys.exit(1)

MODEL = 'google/gemma-4-26b-a4b-it:free'

TOPICS = [
    {"slug":"the-forest-server-hosting","cat":"gaming","title":"The Forest Server hosten – Koop-Guide 2026","tags":"The Forest Server, Koop Survival Hosting, Forest Dedicated Server, The Forest mieten"},
    {"slug":"conan-exiles-server-hosten","cat":"gaming","title":"Conan Exiles Server mieten – Setup & Kosten 2026","tags":"Conan Exiles Server, Conan Exiles mieten, Conan Hosting, Survival Server Setup"},
    {"slug":"space-engineers-server","cat":"gaming","title":"Space Engineers Server mieten oder selbst hosten 2026","tags":"Space Engineers Server, Space Engineers Hosting, SE Server, Space Engineers mieten"},
    {"slug":"scum-server-mieten","cat":"gaming","title":"SCUM Server mieten – Anbieter, Kosten & Setup 2026","tags":"SCUM Server mieten, SCUM Hosting, SCUM Server Kosten, SCUM Dedicated Server"},
    {"slug":"icarus-server-hosting","cat":"gaming","title":"Icarus Server hosten – Dedicated Server für Koop 2026","tags":"Icarus Server, Icarus Hosting, Icarus Dedicated Server, Icarus Koop Server"},
    {"slug":"grounded-server-hosting","cat":"gaming","title":"Grounded Server hosten – Kosten, Setup & Anbieter 2026","tags":"Grounded Server, Grounded Hosting, Grounded Koop, Grounded Server mieten"},
    {"slug":"smalland-server-hosting","cat":"gaming","title":"Smalland Server mieten – Guide für den Koop-Server 2026","tags":"Smalland Server, Smalland Hosting, Smalland mieten, Smalland Koop Guide"},
    {"slug":"nightingale-server-hosting","cat":"gaming","title":"Nightingale Server hosten – Realm-Hosting-Guide 2026","tags":"Nightingale Server, Nightingale Hosting, Nightingale Realm, Nightingale mieten"},
    {"slug":"sons-of-the-forest-server","cat":"gaming","title":"Sons of the Forest Server hosten – Setup-Guide 2026","tags":"Sons of the Forest Server, SOTF Hosting, Sons of the Forest Dedicated Server"},
    {"slug":"cloudflare-tunnel-einrichten","cat":"webhosting","title":"Cloudflare Tunnel einrichten – Kostenloser Reverse Proxy 2026","tags":"Cloudflare Tunnel, Cloudflare Reverse Proxy, Tunnel einrichten"},
    {"slug":"plesk-vs-cpanel-vergleich","cat":"webhosting","title":"Plesk vs. cPanel – Der große Hosting-Panel-Vergleich 2026","tags":"Plesk, cPanel, Hosting Panel, Server Verwaltung, Webhosting Vergleich"},
    {"slug":"mysql-mariadb-optimierung","cat":"webhosting","title":"MySQL & MariaDB optimieren – Performance-Guide 2026","tags":"MySQL Optimierung, MariaDB Tuning, Datenbank Performance, Query Optimierung"},
    {"slug":"nextcloud-server-einrichten","cat":"webhosting","title":"Nextcloud Server einrichten – Cloud-Speicher selbst hosten 2026","tags":"Nextcloud Server, Nextcloud einrichten, Cloud Speicher, Nextcloud Hosting"},
    {"slug":"webseite-sicherheit-2026","cat":"webhosting","title":"Webseite sichern – Security-Checkliste für deine Website 2026","tags":"Webseite Sicherheit, Website schützen, Hacking Schutz, Security Checkliste"},
    {"slug":"docker-wordpress-hosten","cat":"webhosting","title":"WordPress mit Docker hosten – Modernes Setup 2026","tags":"WordPress Docker, Docker Hosting, WordPress Container, Docker Compose WordPress"},
    {"slug":"cloud-hosting-vs-shared-hosting","cat":"webhosting","title":"Cloud Hosting vs. Shared Hosting – Vergleich 2026","tags":"Cloud Hosting, Shared Hosting, Hosting Vergleich, Cloud Server, Webhosting"},
    {"slug":"ansible-automation-guide","cat":"devops","title":"Ansible Automation – Grundlagen & Praxis-Guide 2026","tags":"Ansible, Automation, Konfigurationsmanagement, DevOps, Ansible Playbooks"},
    {"slug":"gitops-argocd-einrichten","cat":"devops","title":"GitOps mit ArgoCD – Kubernetes Deployment Guide 2026","tags":"GitOps, ArgoCD, Kubernetes Deployment, GitOps Workflow"},
    {"slug":"linux-server-harden","cat":"devops","title":"Linux Server härten – Security-Baseline 2026","tags":"Linux Server härten, Server Security, Hardening Guide, Linux absichern"},
    {"slug":"postgresql-vps-optimierung","cat":"devops","title":"PostgreSQL auf dem VPS optimieren – Tuning-Guide 2026","tags":"PostgreSQL Tuning, PostgreSQL Optimierung, VPS Datenbank, Postgres Performance"},
    {"slug":"traefik-reverse-proxy","cat":"devops","title":"Traefik Reverse Proxy einrichten – Moderner Docker-Proxy 2026","tags":"Traefik, Reverse Proxy, Docker Proxy, Lets Encrypt Traefik"},
    {"slug":"elk-stack-log-management","cat":"devops","title":"ELK Stack – Log-Management mit Elasticsearch & Kibana 2026","tags":"ELK Stack, Elasticsearch, Kibana, Logstash, Log Management"},
    {"slug":"wireguard-vpn-server","cat":"devops","title":"WireGuard VPN Server einrichten – Schnell & Sicher 2026","tags":"WireGuard, VPN Server, WireGuard einrichten, VPN Setup, Secure Tunnel"},
    {"slug":"n8n-automation-server","cat":"devops","title":"n8n Automation Server hosten – Workflow-Automatisierung 2026","tags":"n8n, Workflow Automation, n8n Server, Low Code Automation"}
]

NAV = '<nav class="navbar"><div class="container"><a href="/" class="logo">hosta<span>zar</span></a><ul class="nav-links"><li><a href="/">Startseite</a></li><li class="nav-dropdown"><a href="/gaming/">Gaming</a><div class="nav-dropdown-menu"><a href="/gaming/">🎮 Alle Gaming-Artikel</a></div></li><li class="nav-dropdown"><a href="/webhosting/">Webhosting</a><div class="nav-dropdown-menu"><a href="/webhosting/">🌐 Alle Webhosting-Artikel</a></div></li><li class="nav-dropdown"><a href="/devops/">DevOps</a><div class="nav-dropdown-menu"><a href="/devops/">⚙️ Alle DevOps-Artikel</a></div></li><li><a href="/about.html">Über uns</a></li><li><a href="/impressum.html">Impressum</a></li></ul></div></nav>'

FOOTER = '<footer class="footer"><div class="container"><div class="footer-grid"><div><h4>hosta<span style="color:var(--accent)">zar</span></h4><p style="color:var(--text-muted);font-size:0.9rem">Dein Hosting- &amp; Server-Portal mit Guides, Vergleichen und Tutorials.</p></div><div><h4>Kategorien</h4><ul><li><a href="/gaming/">🎮 Gaming</a></li><li><a href="/webhosting/">🌐 Webhosting</a></li><li><a href="/devops/">⚙️ DevOps</a></li></ul></div><div><h4>Rechtliches</h4><ul><li><a href="/about.html">Über uns</a></li><li><a href="/impressum.html">Impressum</a></li></ul></div></div><div class="footer-bottom"><span>&copy; 2026 hostazar.com &ndash; Alle Rechte vorbehalten.</span><span>Made with &hearts; f&uuml;r die Hosting-Community</span></div><p class="affiliate-note">* Bei den mit Sternchen gekennzeichneten Links handelt es sich um Affiliate-Links. Wenn du &uuml;ber diese Links einkaufst, erhalten wir eine kleine Provision &ndash; f&uuml;r dich entstehen keine Mehrkosten. Als Amazon-Partner verdienen wir an qualifizierten Verk&auml;ufen.</p></div></footer>'

def h(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def call_api(prompt, max_tokens=1800):
    data = json.dumps({"model": MODEL, "messages": [
        {"role": "system", "content": "Du bist ein deutscher SEO-Content-Autor für hostazar.com. Schreibe hochwertige, praxisnahe Hosting-Guides auf Deutsch. Verwende SEO-Keywords natürlich."},
        {"role": "user", "content": prompt}
    ], "max_tokens": max_tokens, "temperature": 0.7}).encode()
    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions", data=data,
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}), timeout=120)
            result = json.loads(resp.read())
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content'].strip()
            if 'error' in result:
                err = result['error'].get('message', '')
                if 'rate' in err.lower(): time.sleep(10); continue
                raise Exception(f"API error: {err[:200]}")
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10); continue
            raise
        except urllib.error.URLError:
            time.sleep(5); continue
    raise Exception("API failed after retries")

def make_html(t, content):
    slug = t['slug']; cat = t['cat']; title = t['title']; tags = t['tags']
    can = f"https://hostazar.com/artikel/{slug}.html"
    desc = content[:160].replace('\n',' ').strip()
    if not desc.endswith('.'): desc += '.'
    cl = {'gaming':'Gaming','webhosting':'Webhosting','devops':'DevOps'}[cat]
    ce = {'gaming':'🎮','webhosting':'🌐','devops':'⚙️'}[cat]
    paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    ch = ''
    for p in paras:
        if p.startswith('## '): ch += f'      <h2>{h(p[3:])}</h2>\n'
        elif p.startswith('### '): ch += f'      <h3>{h(p[3:])}</h3>\n'
        elif p.startswith('- ') or p.startswith('* '):
            items = re.findall(r'^[-*] (.+)$', p, re.MULTILINE)
            if items: ch += '      <ul>\n' + ''.join(f'        <li>{h(i)}</li>\n' for i in items) + '      </ul>\n'
            else: ch += f'      <p>{h(p)}</p>\n'
        else: ch += f'      <p>{h(p)}</p>\n'
    wc = max(300, len(content.split()))
    rm = max(3, wc // 200)
    as_ = 'Gameserver+Hosting+Setup' if cat=='gaming' else ('Webhosting+Server' if cat=='webhosting' else 'DevOps+Server')
    al = 'Gaming-Zubehör & Server-Hardware' if cat=='gaming' else ('Server-Hardware & Hosting-Zubehör' if cat=='webhosting' else 'Server-Administration & IT-Zubehör')
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h(title)} | hostazar.com</title>
  <meta name="description" content="{h(desc)}">
  <meta name="keywords" content="{h(tags)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{can}">
  <link rel="stylesheet" href="/css/style.css">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{can}">
  <meta property="og:title" content="{h(title)}">
  <meta property="og:description" content="{h(desc)}">
  <meta property="og:image" content="https://hostazar.com/images/{slug}.png">
  <meta property="og:locale" content="de_DE">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{h(title)}">
  <meta name="twitter:description" content="{h(desc)}">
  <script type="application/ld+json">{{
    "@context": "https://schema.org", "@type": "BlogPosting",
    "headline": "{h(title)}", "url": "{can}",
    "datePublished": "2026-06-15", "dateModified": "2026-06-15",
    "author": {{"@type":"Organization","name":"hostazar.com"}},
    "publisher": {{"@type":"Organization","name":"hostazar.com"}},
    "description": "{h(desc)}",
    "image": "https://hostazar.com/images/{slug}.png",
    "mainEntityOfPage": {{"@type":"WebPage","@id":"{can}"}},
    "wordCount": {wc}, "articleSection": "{cl}", "inLanguage": "de"
  }}</script>
  <script src="/data/script.js" defer></script>
</head>
<body>
{NAV}
<main class="container article-page">
  <article>
    <div class="article-header">
      <div class="card-meta">
        <span class="card-tag {cat}">{cl}</span>
        <span>15. Juni 2026</span>
        <span>· {rm} Min Lesezeit</span>
      </div>
      <h1>{h(title)}</h1>
      <p style="color:var(--text-secondary);font-size:1.1rem">Alles zu Kosten, Setup, Anbietern und der richtigen Wahl f&uuml;r deinen {cl}-Server 2026.</p>
    </div>
    <div class="adsense-placeholder">
      <p><strong>&mdash; Anzeige &mdash;</strong></p>
      <p>Google AdSense Platzhalter</p>
    </div>
    <div id="breadcrumbs"></div>
    <div class="article-content">
{ch}
    </div>
    <div class="affiliate-box">
      <p>{ce} Empfohlenes Zubeh&ouml;r</p>
      <p><strong>{h(al)}</strong> &ndash; Finde passende Hardware f&uuml;r dein Server-Projekt.</p>
      <a href="https://www.amazon.de/s?k={as_}&amp;tag=nova079-20" target="_blank" rel="nofollow sponsored" class="btn">Auf Amazon entdecken &rarr;</a>
      <p style="margin-top:8px;font-size:0.75rem">* Affiliate-Link. Als Amazon-Partner verdienen wir an qualifizierten Verk&auml;ufen.</p>
    </div>
    <div class="amazon-affiliate" style="margin:30px 0;padding:15px;background:#f3e5f5;border:1px solid #9C27B0;border-radius:8px;text-align:center">
      <p><strong>{ce} Mehr zum Thema auf Amazon</strong></p>
      <p><a href="https://www.amazon.de/s?k={as_}&amp;tag=nova079-20" target="_blank" rel="nofollow sponsored">Zu den Produkten auf Amazon &rarr;</a></p>
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
      relatedConfig: {{containerId:'related-articles',category:'{cat}',excludeSlug:'{slug}',count:3}},
      breadcrumbs: [{{url:'/{cat}/',label:'{cl}'}},{{label:'{h(title)}'}}]
    }});
  }}
}});
</script>
</body>
</html>'''

def gen_one(t):
    slug = t['slug']
    path = os.path.join(REPO, 'artikel', f'{slug}.html')
    if os.path.exists(path) and os.path.getsize(path) > 3000:
        print(f"  SKIP {slug}"); return slug, True
    cl = {'gaming':'Gaming','webhosting':'Webhosting','devops':'DevOps'}[t['cat']]
    prompt = f"""Schreibe einen deutschen SEO-Artikel (ca. 500-700 Wörter) für hostazar.com.
Thema: {t['title']}
Kategorie: {cl}
Strukturiere mit ## und ### Überschriften: Einleitung, 3-4 Hauptabschnitte (Kosten, Setup, Anbieter, Tipps), Fazit.
Keywords: {t['tags']}
Nur Fließtext mit Markdown-Überschriften, kein HTML."""
    try:
        print(f"  → {slug}...")
        content = call_api(prompt)
        if not content or len(content) < 200:
            content = call_api(prompt, 2000)
        html = make_html(t, content)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f: f.write(html)
        words = len(content.split())
        print(f"  ✓ {slug} - {words} Wörter")
        return slug, True
    except Exception as e:
        print(f"  ✗ {slug}: {e}"); return slug, False

def main():
    print(f"Generiere {len(TOPICS)} Artikel mit {MODEL} (3 parallel)")
    ok = fail = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        fs = {ex.submit(gen_one, t): t for t in TOPICS}
        for f in as_completed(fs):
            _, success = f.result()
            if success: ok += 1
            else: fail += 1
    print(f"\nErgebnis: {ok} OK, {fail} FAIL")

if __name__ == '__main__':
    main()
