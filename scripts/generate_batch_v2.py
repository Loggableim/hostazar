#!/usr/bin/env python3
"""Generate 25 SEO articles for hostazar.com via OpenRouter free model (parallel)."""
import os, sys, json, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
if not API_KEY:
    try:
        with open('/c/HermesPortable/home/.env') as f:
            for line in f:
                if 'OPENROUTER_API_KEY' in line:
                    API_KEY = line.strip().split('=', 1)[1].strip('\'"')
                    break
    except:
        pass
if not API_KEY:
    print("NO API KEY found")
    sys.exit(1)

MODEL = 'google/gemma-4-26b-a4b-it:free'
AMAZON_TAG = 'nova079-20'

TOPICS = [
    {"slug":"the-forest-server-hosting","cat":"gaming","title":"The Forest Server hosten \u2013 Koop-Guide 2026"},
    {"slug":"conan-exiles-server-hosten","cat":"gaming","title":"Conan Exiles Server mieten \u2013 Setup & Kosten 2026"},
    {"slug":"space-engineers-server","cat":"gaming","title":"Space Engineers Server mieten oder selbst hosten 2026"},
    {"slug":"scum-server-mieten","cat":"gaming","title":"SCUM Server mieten \u2013 Anbieter, Kosten & Setup 2026"},
    {"slug":"icarus-server-hosting","cat":"gaming","title":"Icarus Server hosten \u2013 Dedicated Server f\u00fcr Koop 2026"},
    {"slug":"grounded-server-hosting","cat":"gaming","title":"Grounded Server hosten \u2013 Kosten, Setup & Anbieter 2026"},
    {"slug":"smalland-server-hosting","cat":"gaming","title":"Smalland Server mieten \u2013 Guide f\u00fcr den Koop-Server 2026"},
    {"slug":"nightingale-server-hosting","cat":"gaming","title":"Nightingale Server hosten \u2013 Realm-Hosting-Guide 2026"},
    {"slug":"sons-of-the-forest-server","cat":"gaming","title":"Sons of the Forest Server hosten \u2013 Setup-Guide 2026"},
    {"slug":"cloudflare-tunnel-einrichten","cat":"webhosting","title":"Cloudflare Tunnel einrichten \u2013 Kostenloser Reverse Proxy 2026"},
    {"slug":"plesk-vs-cpanel-vergleich","cat":"webhosting","title":"Plesk vs. cPanel \u2013 Der gro\u00dfe Hosting-Panel-Vergleich 2026"},
    {"slug":"mysql-mariadb-optimierung","cat":"webhosting","title":"MySQL & MariaDB optimieren \u2013 Performance-Guide 2026"},
    {"slug":"nextcloud-server-einrichten","cat":"webhosting","title":"Nextcloud Server einrichten \u2013 Cloud-Speicher selbst hosten 2026"},
    {"slug":"webseite-sicherheit-2026","cat":"webhosting","title":"Webseite sichern \u2013 Security-Checkliste f\u00fcr deine Website 2026"},
    {"slug":"docker-wordpress-hosten","cat":"webhosting","title":"WordPress mit Docker hosten \u2013 Modernes Setup 2026"},
    {"slug":"cloud-hosting-vs-shared-hosting","cat":"webhosting","title":"Cloud Hosting vs. Shared Hosting \u2013 Vergleich 2026"},
    {"slug":"ansible-automation-guide","cat":"devops","title":"Ansible Automation \u2013 Grundlagen & Praxis-Guide 2026"},
    {"slug":"gitops-argocd-einrichten","cat":"devops","title":"GitOps mit ArgoCD \u2013 Kubernetes Deployment Guide 2026"},
    {"slug":"linux-server-harden","cat":"devops","title":"Linux Server h\u00e4rten \u2013 Security-Baseline 2026"},
    {"slug":"postgresql-vps-optimierung","cat":"devops","title":"PostgreSQL auf dem VPS optimieren \u2013 Tuning-Guide 2026"},
    {"slug":"traefik-reverse-proxy","cat":"devops","title":"Traefik Reverse Proxy einrichten \u2013 Moderner Docker-Proxy 2026"},
    {"slug":"elk-stack-log-management","cat":"devops","title":"ELK Stack \u2013 Log-Management mit Elasticsearch & Kibana 2026"},
    {"slug":"wireguard-vpn-server","cat":"devops","title":"WireGuard VPN Server einrichten \u2013 Schnell & Sicher 2026"},
    {"slug":"n8n-automation-server","cat":"devops","title":"n8n Automation Server hosten \u2013 Workflow-Automatisierung 2026"},
]

NAV = '<nav class="navbar"><div class="container"><a href="/" class="logo">hosta<span>zar</span></a><ul class="nav-links"><li><a href="/">Startseite</a></li><li class="nav-dropdown"><a href="/gaming/">Gaming</a><div class="nav-dropdown-menu"><a href="/gaming/">\U0001f3ae Alle Gaming-Artikel</a></div></li><li class="nav-dropdown"><a href="/webhosting/">Webhosting</a><div class="nav-dropdown-menu"><a href="/webhosting/">\U0001f310 Alle Webhosting-Artikel</a></div></li><li class="nav-dropdown"><a href="/devops/">DevOps</a><div class="nav-dropdown-menu"><a href="/devops/">\u2699\ufe0f Alle DevOps-Artikel</a></div></li><li><a href="/about.html">\u00dcber uns</a></li><li><a href="/impressum.html">Impressum</a></li></ul></div></nav>'

FOOTER = '<footer class="footer"><div class="container"><div class="footer-grid"><div><h4>hosta<span style="color:var(--accent)">zar</span></h4><p style="color:var(--text-muted);font-size:0.9rem">Dein Hosting- &amp; Server-Portal mit Guides.</p></div><div><h4>Kategorien</h4><ul><li><a href="/gaming/">\U0001f3ae Gaming</a></li><li><a href="/webhosting/">\U0001f310 Webhosting</a></li><li><a href="/devops/">\u2699\ufe0f DevOps</a></li></ul></div><div><h4>Rechtliches</h4><ul><li><a href="/about.html">\u00dcber uns</a></li><li><a href="/impressum.html">Impressum</a></li></ul></div></div><div class="footer-bottom"><span>\u00a9 2026 hostazar.com</span></div></div></footer>'

def h(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')

def call_api(prompt):
    for attempt in range(3):
        try:
            data = json.dumps({
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "Du bist ein deutscher SEO-Content-Autor f\u00fcr hostazar.com."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000,
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
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read())
            if 'choices' in result and result['choices']:
                return result['choices'][0]['message']['content'].strip()
            if 'error' in result:
                raise Exception(result['error'].get('message','')[:200])
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(15)
                continue
            raise
        except Exception:
            time.sleep(10)
            continue
    return ""

def gen_one(t):
    slug = t['slug']
    path = os.path.join(REPO, 'artikel', f'{slug}.html')
    if os.path.exists(path) and os.path.getsize(path) > 3000:
        print(f"  SKIP {slug}")
        return True
    
    cl = {'gaming':'Gaming','webhosting':'Webhosting','devops':'DevOps'}[t['cat']]
    kw_hints = {'gaming':'Server mieten, Kosten, Setup, Anbieter, Mods, Performance',
                'webhosting':'Kosten, Setup, Konfiguration, Vergleich, Sicherheit',
                'devops':'Setup, Konfiguration, Best Practices, Sicherheit'}
    kw = kw_hints[t['cat']]
    
    prompt = (
        f"Schreibe einen deutschen SEO-Artikel (500-700 W\u00f6rter) f\u00fcr hostazar.com.\n\n"
        f"Thema: {t['title']}\n"
        f"Kategorie: {cl}\n\n"
        f"Gliederung:\n"
        f"## Einleitung (kurz, mit Keyword)\n"
        f"## [Hauptabschnitt 1 - Kosten oder \u00dcberblick]\n"
        f"## [Hauptabschnitt 2 - Setup oder Anbieter]\n"
        f"## [Hauptabschnitt 3 - Tipps oder Vergleich]\n"
        f"## Fazit\n\n"
        f"Keywords nat\u00fcrlich einbauen: {kw}\n\n"
        f"Schreibe NUR den Flie\u00dftext. \u00dcberschriften mit ## und ### kennzeichnen."
    )
    
    print(f"  \u2192 {slug}...")
    content = call_api(prompt)
    if not content or len(content) < 200:
        print(f"  retry {slug}")
        content = call_api(prompt)
    if not content:
        print(f"  FAIL {slug}")
        return False
    
    wc = max(300, len(content.split()))
    desc = content.replace('\n', ' ').strip()[:160]
    if not desc.endswith('.'):
        desc += '.'
    can = f"https://hostazar.com/artikel/{slug}.html"
    
    paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    body = ''
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if p.startswith('## '):
            body += f'      <h2>{h(p[3:])}</h2>\n'
        elif p.startswith('### '):
            body += f'      <h3>{h(p[3:])}</h3>\n'
        elif any(p.startswith(c) for c in ['- ', '* ']):
            items = re.findall(r'^[-*] (.+)$', p, re.MULTILINE)
            if items:
                body += '      <ul>\n'
                for item in items:
                    body += f'        <li>{h(item)}</li>\n'
                body += '      </ul>\n'
            else:
                body += f'      <p>{h(p)}</p>\n'
        else:
            body += f'      <p>{h(p)}</p>\n'
    
    amz_link = f"https://www.amazon.de/s?k=Server+Hosting+Setup&amp;tag={AMAZON_TAG}"
    
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{h(t["title"])} | hostazar.com</title>
  <meta name="description" content="{h(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{can}">
  <link rel="stylesheet" href="/css/style.css">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{can}">
  <meta property="og:title" content="{h(t["title"])}">
  <meta property="og:description" content="{h(desc)}">
  <meta property="og:image" content="https://hostazar.com/images/{slug}.png">
  <meta property="og:locale" content="de_DE">
  <script type="application/ld+json">{{
    "@context":"https://schema.org","@type":"BlogPosting",
    "headline":"{h(t["title"])}","url":"{can}",
    "datePublished":"2026-06-15","dateModified":"2026-06-15",
    "author":{{"@type":"Organization","name":"hostazar.com"}},
    "description":"{h(desc)}","wordCount":{wc}
  }}</script>
  <script src="/data/script.js" defer></script>
</head>
<body>
{NAV}
<main class="container article-page">
  <article>
    <div class="article-header">
      <div class="card-meta">
        <span class="card-tag {t["cat"]}">{cl}</span>
        <span>15. Juni 2026</span>
        <span>� {max(3,wc//200)} Min Lesezeit</span>
      </div>
      <h1>{h(t["title"])}</h1>
    </div>
    <div class="adsense-placeholder"><p><strong>&mdash; Anzeige &mdash;</strong></p><p>Google AdSense Platzhalter</p></div>
    <div id="breadcrumbs"></div>
    <div class="article-content">
{body}
    </div>
    <div class="affiliate-box">
      <p><strong>Empfohlenes Zubeh&ouml;r</strong></p>
      <a href="{amz_link}" target="_blank" rel="nofollow sponsored" class="btn">Auf Amazon entdecken &rarr;</a>
      <p style="margin-top:8px;font-size:0.75rem">* Affiliate-Link. Als Amazon-Partner verdienen wir an qualifizierten Verk&auml;ufen.</p>
    </div>
    <div id="related-articles"></div>
    <div class="adsense-placeholder"><p><strong>&mdash; Anzeige &mdash;</strong></p><p>Google AdSense Platzhalter (Ende)</p></div>
  </article>
</main>
{FOOTER}
<script>
document.addEventListener('DOMContentLoaded', function(){{
  if(typeof hostazarApp !== 'undefined'){{
    hostazarApp.init({{
      gridId: 'related-articles',
      relatedConfig: {{containerId:'related-articles',category:'{t["cat"]}',excludeSlug:'{slug}',count:3}},
      breadcrumbs: [{{url:'/{t["cat"]}/',label:'{cl}'}},{{label:'{h(t["title"])}'}}]
    }});
  }}
}});
</script>
</body>
</html>'''
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  OK {slug} - {wc} W\u00f6rter")
    return True

def main():
    total = len(TOPICS)
    print(f"Generating {total} articles with {MODEL} (3 parallel workers)")
    
    ok = 0
    fail = 0
    skip = 0
    
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(gen_one, t): t for t in TOPICS}
        for f in as_completed(futures):
            try:
                result = f.result()
                if result is True:
                    ok += 1
                else:
                    fail += 1
            except Exception as e:
                fail += 1
                print(f"  EXCEPTION: {e}")
    
    print(f"\n{'='*40}")
    print(f"Done: {ok} OK, {fail} FAIL, {skip} SKIP")

if __name__ == '__main__':
    main()