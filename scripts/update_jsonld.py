"""Add 3 new articles to JSON-LD in index.html"""
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.rfind('}]')
if idx > 0:
    new_entries = ', {"@context": "https://schema.org", "@type": "BlogPosting", "headline": "TeamSpeak 3 Server mieten 2026 \u2013 Sprachserver f\u00fcr Gamer", "url": "https://hostazar.com/artikel/teamspeak-server-mieten-2026.html", "datePublished": "2026-06-05", "dateModified": "2026-06-05", "description": "TeamSpeak 3 Server mieten 2026: Anbieter-Vergleich, Kosten, Setup-Guide f\u00fcr deinen Gaming-Sprachserver.", "author": {"@type": "Organization", "name": "hostazar.com"}}, {"@context": "https://schema.org", "@type": "BlogPosting", "headline": "Grafana Loki Log-Aggregation auf VPS 2026 \u2013 Installations-Guide", "url": "https://hostazar.com/artikel/grafana-loki-log-aggregation-vps-2026.html", "datePublished": "2026-06-05", "dateModified": "2026-06-05", "description": "Grafana Loki auf VPS installieren: Log-Aggregation mit Loki, Promtail und Grafana. Docker-Compose-Setup und LogQL-Abfragen.", "author": {"@type": "Organization", "name": "hostazar.com"}}, {"@context": "https://schema.org", "@type": "BlogPosting", "headline": "Ghost CMS Hosting auf VPS 2026 \u2013 Blog-Software installieren und betreiben", "url": "https://hostazar.com/artikel/ghost-cms-hosting-vps-2026.html", "datePublished": "2026-06-05", "dateModified": "2026-06-05", "description": "Ghost CMS auf VPS hosten 2026: Node.js-Blog-Software mit Ghost-CLI oder Docker installieren. Nginx, MySQL und SSL-Setup.", "author": {"@type": "Organization", "name": "hostazar.com"}}'
    content = content[:idx] + new_entries + content[idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('JSON-LD updated successfully!')
else:
    print('ERROR: Could not find JSON-LD closing bracket')
