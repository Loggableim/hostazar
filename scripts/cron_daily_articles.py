#!/usr/bin/env python3
"""Daily content generator for hostazar.com.

Generates N new articles (default 4) via Ollama (deepseek-v4.1-flash),
then publishes them through publish_article.py (hero image, catalog,
index, sitemap, RSS, git push → Cloudflare Pages).

Topic selection: static pool first; when exhausted, asks the LLM for
fresh topic ideas based on existing slugs.

Run: python scripts/cron_daily_articles.py [--count 4] [--no-push]
"""
import argparse, datetime, json, os, re, subprocess, sys, time, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, 'artikel')
TMP_DIR = os.path.join(REPO, 'tmp')
LOG_FILE = os.path.join(REPO, 'tmp', 'daily_content.log')

OLLAMA_URL = 'https://ollama.com/v1/chat/completions'
OLLAMA_MODEL = 'deepseek-v4.1-flash'
ENV_PATH = 'C:/sidekick/home/.env'

SYSTEM_PROMPT = (
    'Du bist ein deutscher SEO-Content-Autor für hostazar.com — ein Hosting- und '
    'Server-Portal für Gameserver, Webhosting, DevOps und KI/LLM-Themen. '
    'Du schreibst detaillierte, praxisnahe Guides mit konkreten Zahlen, Befehlen, '
    'Preisangaben und Vergleichen. Zielgruppe: Server-Admins, DevOps-Engineers, Gamer.'
)

# Static topic pool: (slug, title, category)
TOPIC_POOL = [
    ('docker-compose-vs-kubernetes-2026', 'Docker Compose vs. Kubernetes 2026 – Wann sich was lohnt', 'devops'),
    ('github-actions-self-hosted-runner-2026', 'GitHub Actions Self-Hosted Runner auf VPS betreiben 2026', 'devops'),
    ('traefik-vs-nginx-reverse-proxy-2026', 'Traefik vs. Nginx als Reverse Proxy 2026 – Vergleich', 'devops'),
    ('ansible-vs-terraform-2026', 'Ansible vs. Terraform 2026 – Wann welches Tool?', 'devops'),
    ('docker-security-hardening-2026', 'Docker Security Hardening 2026 – Container absichern', 'devops'),
    ('linux-server-haertung-checkliste-2026', 'Linux Server Härtung 2026 – Die komplette Checkliste', 'devops'),
    ('vps-backup-strategie-2026', 'VPS Backup-Strategie 2026 – 3-2-1-Regel richtig umsetzen', 'devops'),
    ('container-registry-harbor-2026', 'Harbor Container Registry selbst hosten 2026', 'devops'),
    ('webhosting-vs-vps-2026', 'Webhosting vs. VPS 2026 – Der große Vergleich', 'webhosting'),
    ('letsencrypt-ssl-zertifikate-2026', 'Let\'s Encrypt SSL-Zertifikate 2026 – Automatisierung mit Certbot', 'webhosting'),
    ('email-server-mailcow-2026', 'Mailcow E-Mail-Server selbst hosten 2026', 'webhosting'),
    ('wordpress-caching-optimierung-2026', 'WordPress Caching optimieren 2026 – Redis, OPcache & CDN', 'webhosting'),
    ('cdn-fuer-websites-2026', 'CDN für Websites 2026 – Cloudflare, BunnyCDN & Fastly im Vergleich', 'webhosting'),
    ('domain-dns-einrichten-2026', 'Domain & DNS richtig einrichten 2026 – A, CNAME, MX erklärt', 'webhosting'),
    ('nginx-fastcgi-cache-2026', 'Nginx FastCGI Cache einrichten 2026 – Performance-Guide', 'webhosting'),
    ('website-migration-server-2026', 'Website auf neuen Server migrieren 2026 – Schritt für Schritt', 'webhosting'),
    ('rag-system-selbst-hosten-2026', 'RAG-System selbst hosten 2026 – Vektordatenbank + LLM', 'ki-llm'),
    ('llm-finetuning-einsteiger-2026', 'LLM Fine-Tuning für Einsteiger 2026 – LoRA & QLoRA', 'ki-llm'),
    ('whisper-spracherkennung-server-2026', 'Whisper Spracherkennung auf Server betreiben 2026', 'ki-llm'),
    ('stable-diffusion-server-hosten-2026', 'Stable Diffusion auf Server hosten 2026 – GPU-Setup', 'ki-llm'),
    ('vector-datenbanken-vergleich-2026', 'Vektordatenbanken im Vergleich 2026 – Qdrant, Milvus, Chroma', 'ki-llm'),
    ('lokale-llm-quantisierung-2026', 'LLM-Quantisierung erklärt 2026 – GGUF, GPTQ, AWQ', 'ki-llm'),
    ('ai-agenten-selbst-hosten-2026', 'AI-Agenten selbst hosten 2026 – Frameworks & Setup', 'ki-llm'),
    ('gpu-server-mieten-2026', 'GPU-Server mieten 2026 – Anbieter, Preise & Use Cases', 'ki-llm'),
    ('minecraft-plugin-server-optimierung-2026', 'Minecraft Plugin-Server optimieren 2026 – Paper & Spigot Tuning', 'gaming'),
    ('cs2-server-tuning-2026', 'CS2 Server Tuning 2026 – Tickrate, Config & Performance', 'gaming'),
    ('valheim-mods-server-2026', 'Valheim Mods auf dem Server installieren 2026', 'gaming'),
    ('palworld-server-update-2026', 'Palworld Server Update & Wipe-Management 2026', 'gaming'),
    ('kubernetes-helm-charts-2026', 'Kubernetes Helm Charts 2026 – Praxis-Guide für Einsteiger', 'devops'),
    ('prometheus-alerting-regeln-2026', 'Prometheus Alerting-Regeln schreiben 2026 – Praxis-Guide', 'devops'),
    ('grafana-dashboards-vps-2026', 'Grafana Dashboards für VPS-Monitoring 2026', 'devops'),
    ('linux-firewall-nftables-2026', 'Linux Firewall mit nftables 2026 – Modernes Setup', 'devops'),
    ('ssh-sicherheit-absichern-2026', 'SSH absichern 2026 – Keys, 2FA & Port-Knocking', 'devops'),
    ('fail2ban-konfiguration-2026', 'Fail2ban richtig konfigurieren 2026 – Schutz vor Brute-Force', 'devops'),
    ('docker-logging-monitoring-2026', 'Docker Logging & Monitoring 2026 – Loki, Promtail & Grafana', 'devops'),
    ('postgresql-backup-restore-2026', 'PostgreSQL Backup & Restore 2026 – pg_dump, WAL & PITR', 'devops'),
    ('redis-caching-vps-2026', 'Redis als Cache auf dem VPS 2026 – Setup & Tuning', 'devops'),
    ('nginx-http3-quic-2026', 'Nginx mit HTTP/3 & QUIC betreiben 2026', 'webhosting'),
    ('wireguard-vpn-einrichten-2026', 'WireGuard VPN einrichten 2026 – Kompletter Guide', 'devops'),
    ('tailscale-vs-wireguard-2026', 'Tailscale vs. Wireguard 2026 – Mesh-VPN im Vergleich', 'devops'),
]


def log(msg):
    line = f'[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}'
    print(line, flush=True)
    os.makedirs(TMP_DIR, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def ollama_key():
    env = open(ENV_PATH, encoding='utf-8').read()
    m = re.search(r'OLLAMA_API_KEY=(\S+)', env)
    if not m:
        raise RuntimeError('OLLAMA_API_KEY nicht in ' + ENV_PATH)
    return m.group(1)


def call_ollama(prompt, max_tokens=16384, temperature=0.7, timeout=300):
    key = ollama_key()
    data = json.dumps({
        'model': OLLAMA_MODEL,
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt},
        ],
        'max_tokens': max_tokens,
        'temperature': temperature,
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=data, headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
    })
    resp = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    msg = resp['choices'][0]['message']
    content = msg.get('content') or ''
    # strip any think blocks / code fences
    content = re.sub(r'```html\s*|```', '', content)
    return content.strip()


def pick_topics(count):
    existing = set(f[:-5] for f in os.listdir(ARTIKEL_DIR) if f.endswith('.html'))
    available = [t for t in TOPIC_POOL if t[0] not in existing]
    if len(available) >= count:
        return available[:count]

    # Pool exhausted → ask LLM for fresh topics
    log(f'Topic-Pool fast leer ({len(available)} übrig) — frage LLM um neue Themen...')
    recent = sorted(existing)[-80:]
    prompt = (
        'Hier sind bestehende Artikel-Slugs von hostazar.com:\n'
        + '\n'.join(recent) +
        '\n\nSchlage 8 NEUE Artikel-Themen vor, die noch NICHT existieren. '
        'Bereiche: Gameserver, Webhosting, DevOps, VPS, KI/LLM, Server-Hardware, Sicherheit. '
        'Antworte NUR mit JSON-Array: [{"slug": "kurzer-slug-2026", "title": "Deutscher Titel 2026", "category": "gaming|webhosting|devops|ki-llm"}, ...]'
    )
    try:
        raw = call_ollama(prompt, max_tokens=2000, temperature=0.9)
        m = re.search(r'\[.*\]', raw, re.DOTALL)
        ideas = json.loads(m.group(0)) if m else []
    except Exception as e:
        log(f'  ! LLM-Topic-Vorschlag fehlgeschlagen: {e}')
        ideas = []
    fresh = [(i['slug'], i['title'], i['category']) for i in ideas
             if i.get('slug') and i.get('title') and i.get('category')
             and i['slug'] not in existing]
    combined = available + fresh
    log(f'  → {len(fresh)} neue LLM-Topics, insgesamt {len(combined)} verfügbar')
    return combined[:count]


def generate_article(slug, title, category):
    """Generate one article. Returns spec dict or None."""
    prompt = f'''Schreibe einen detaillierten deutschen SEO-Guide für hostazar.com:

TITEL: {title}
KATEGORIE: {category}
SLUG: {slug}

Antworte in GENAU diesem Format (die Marker exakt so):

===EXCERPT===
[Meta-Description, 140-160 Zeichen, mit Hauptkeyword]

===TAGS===
[4-6 Tags, komma-getrennt]

===IMAGE===
[Englischer Bild-Prompt für ein anthropomorphes Tier im Server/Tech-Kontext, z.B. "anthropomorphic fox system administrator, server rack, terminal screens, network cables". NUR die Subjekt-Beschreibung, kein Style.]

===CONTENT===
[NUR Body-HTML: 8-12 <h2>-Abschnitte mit je 3-5 Absätzen. Nutze <h2>, <h3>, <p>, <ul>, <ol>, <table>, <pre><code>, <strong>. Konkrete Zahlen, Befehle, Preisangaben. Am Ende ein FAQ-Abschnitt: <h2>FAQ</h2> mit 3-5 <h3>Frage</h3><p>Antwort</p>. KEIN <h1>, keine Navigation, kein Markdown. 1500-2500 Wörter.]'''

    t0 = time.time()
    raw = call_ollama(prompt, max_tokens=16384)
    log(f'  [{slug}] Content generiert ({len(raw)} chars, {time.time()-t0:.0f}s)')

    def section(name):
        m = re.search(rf'==={name}===\s*(.*?)(?=\n===[A-Z]+===|\Z)', raw, re.DOTALL)
        return m.group(1).strip() if m else ''

    excerpt = section('EXCERPT')
    tags_raw = section('TAGS')
    image_subject = section('IMAGE')
    content = section('CONTENT')

    # cleanup content
    content = re.sub(r'^```html\s*|```\s*$', '', content).strip()
    h2 = content.find('<h2')
    if h2 > 0:
        content = content[h2:]
    if not content or len(content) < 2000:
        log(f'  ! [{slug}] Content zu kurz ({len(content)} chars) — skip')
        return None

    tags = [t.strip() for t in tags_raw.split(',') if t.strip()][:6]
    if not excerpt:
        first_p = re.search(r'<p>(.*?)</p>', content, re.DOTALL)
        excerpt = re.sub(r'<[^>]+>', '', first_p.group(1))[:160] if first_p else title

    words = len(re.sub(r'<[^>]+>', ' ', content).split())
    log(f'  [{slug}] {words} Wörter, {content.count("<h2")} H2s, {len(tags)} Tags')

    return {
        'slug': slug,
        'title': title,
        'category': category,
        'tags': tags,
        'excerpt': excerpt[:160],
        'image_subject': image_subject or f'anthropomorphic animal character, {title}',
        'date': datetime.date.today().isoformat(),
        'content_html': content,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--count', type=int, default=4)
    ap.add_argument('--no-push', action='store_true')
    args = ap.parse_args()

    log(f'=== Daily Content Run: {args.count} Artikel ===')

    topics = pick_topics(args.count)
    if not topics:
        log('Keine Topics verfügbar — Abbruch.')
        return

    specs = []
    for slug, title, category in topics:
        try:
            spec = generate_article(slug, title, category)
            if spec:
                specs.append(spec)
        except Exception as e:
            log(f'  ! [{slug}] Fehler: {e}')

    if not specs:
        log('Keine Artikel generiert — Abbruch.')
        sys.exit(1)

    # write specs + content files for the publisher
    os.makedirs(TMP_DIR, exist_ok=True)
    for spec in specs:
        body_path = os.path.join(TMP_DIR, f'{spec["slug"]}_body.html')
        with open(body_path, 'w', encoding='utf-8') as f:
            f.write(spec['content_html'])
        spec['content_file'] = body_path

    specs_path = os.path.join(TMP_DIR, 'daily_specs.json')
    with open(specs_path, 'w', encoding='utf-8') as f:
        json.dump(specs, f, ensure_ascii=False, indent=2)

    log(f'{len(specs)} Artikel generiert → publish_article.py')
    cmd = [sys.executable, os.path.join(REPO, 'scripts', 'publish_article.py'),
           '--specs', specs_path]
    if args.no_push:
        cmd.append('--no-push')
    r = subprocess.run(cmd, cwd=REPO, timeout=2400)
    log(f'publish_article.py exit={r.returncode}')
    sys.exit(r.returncode)


if __name__ == '__main__':
    main()
