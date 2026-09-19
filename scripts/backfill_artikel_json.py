#!/usr/bin/env python3
"""Backfill data/artikel.json with articles that exist as HTML but are missing
from the catalog. Also converts missing PNG hero images to WebP.

Why: 34 articles (generated June/July 2026) were never added to artikel.json,
so they don't appear in category pages (JS-driven from artikel.json) or the
index. This script adds them with metadata extracted from the HTML.

Run: python scripts/backfill_artikel_json.py
"""
import json, os, re, sys
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, 'artikel')
IMG_DIR = os.path.join(REPO, 'images')
JSON_PATH = os.path.join(REPO, 'data', 'artikel.json')

# Manual category assignment for the 34 orphaned articles
CATEGORIES = {
    'best-vps-hosting-guide-2026': 'devops',
    'borgbackup-vs-restic-for-vps-which-one-actually-saves-your-bacon-in-2026': 'devops',
    'cloudflare-pages-vs-vercel-2026': 'devops',
    'cloudflare-r2-vps-backup-2026': 'webhosting',
    'cutting-docker-image-bloat-real-world-wins-from-multi-stage-builds-in-2026': 'devops',
    'docker-compose-produktion-2026': 'devops',
    'docker-container-tutorial-beginners': 'devops',
    'docker-swarm-vs-kubernetes-2026': 'devops',
    'ebpf-for-vps-observability-in-2026-tracing-without-the-agent-bloat': 'devops',
    'enshrouded-dedicated-server-2026': 'gaming',
    'gameserver-ddos-schutz-cloudflare-2026': 'gaming',
    'hardening-linux-vps-in-2026-practical-steps-beyond-default-firewalls': 'devops',
    'ipv6-only-vps-in-2026-breaking-free-from-legacy-ipv4-without-losing-reach': 'devops',
    'kubernetes-cost-optimization-in-2026-cutting-cluster-waste-without-sacrificing-u': 'devops',
    'migrating-from-docker-compose-to-kubernetes-in-2026-when-its-worth-the-pain-and-': 'devops',
    'minecraft-server-hosting-2026-comparison': 'gaming',
    'minecraft-server-performance-2026': 'gaming',
    'nextcloud-s3-speicher-2026': 'webhosting',
    'nginx-reverse-proxy-setup-guide': 'webhosting',
    'palworld-performance-optimierung-2026': 'gaming',
    'postgresql-connection-poolers-in-2026-pgbouncer-vs-pgpool-ii-on-a-single-vps': 'devops',
    'postgresql-on-a-5-vps-tuning-shared-buffers-and-workmem-for-real-workloads-in-20': 'devops',
    'self-hosted-game-servers-in-2026-why-bare-metal-still-beats-cloud-for-latency': 'gaming',
    'soulmask-server-hosting-2026': 'gaming',
    'spotting-a-hacked-vps-in-2026-forensic-checks-before-its-too-late': 'devops',
    'vps-docker-registry-eigenen-2026': 'devops',
    'vps-kubernetes-einsteiger-2026': 'devops',
    'vps-kubernetes-monitoring-2026': 'devops',
    'vps-monitoring-alerting-2026': 'devops',
    'vps-nginx-tuning-2026': 'webhosting',
    'vps-postgresql-replikation-2026': 'devops',
    'vps-wordpress-sicherheit-2026': 'webhosting',
    'wireguard-mesh-for-vps-clusters-in-2026-ditching-the-central-vpn-headache': 'devops',
    'zero-trust-networking-for-small-vps-fleets-a-pragmatic-setup-guide-for-2026': 'devops',
}


def extract_meta(slug):
    """Extract title, description, date, word count from article HTML."""
    path = os.path.join(ARTIKEL_DIR, slug + '.html')
    raw = open(path, encoding='utf-8').read()

    title = slug.replace('-', ' ').title()
    m = re.search(r'<title>(.*?)(?:\s*\|\s*hostazar\.com)?</title>', raw, re.DOTALL)
    if m:
        title = m.group(1).strip()

    desc = ''
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', raw, re.DOTALL)
    if m:
        desc = m.group(1).strip()
    if not desc:
        m = re.search(r'<meta\s+property="og:description"\s+content="(.*?)"', raw, re.DOTALL)
        if m:
            desc = m.group(1).strip()
    desc = re.sub(r'\s+', ' ', desc)[:160]

    date = ''
    m = re.search(r'article:published_time"\s+content="(\d{4}-\d{2}-\d{2})', raw)
    if m:
        date = m.group(1)
    if not date:
        m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', raw)
        if m:
            date = m.group(1)
    if not date:
        # fallback: file mtime
        import datetime
        date = datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()

    # word count from body text
    body = re.sub(r'<script.*?</script>', ' ', raw, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<[^>]+>', ' ', body)
    words = len(body.split())
    reading_time = str(max(1, round(words / 280)))

    # tags from meta keywords if present
    tags = []
    m = re.search(r'<meta\s+name="keywords"\s+content="(.*?)"', raw, re.DOTALL)
    if m:
        tags = [t.strip() for t in m.group(1).split(',') if t.strip()][:6]

    return {
        'slug': slug,
        'title': title,
        'category': CATEGORIES.get(slug, 'devops'),
        'tags': tags,
        'excerpt': desc,
        'date': date,
        'readingTime': reading_time,
        'image': slug + '.webp',
    }


def convert_missing_webp(slugs):
    """Convert PNG→WebP for slugs that only have PNG."""
    converted = []
    for slug in slugs:
        png = os.path.join(IMG_DIR, slug + '.png')
        webp = os.path.join(IMG_DIR, slug + '.webp')
        if os.path.exists(png) and not os.path.exists(webp):
            img = Image.open(png)
            if img.mode == 'RGBA':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            img.save(webp, 'WEBP', quality=92, method=6)
            converted.append(slug)
    return converted


def main():
    data = json.load(open(JSON_PATH, encoding='utf-8'))
    json_slugs = set(a['slug'] for a in data)
    html_slugs = set(f[:-5] for f in os.listdir(ARTIKEL_DIR) if f.endswith('.html'))
    missing = sorted(html_slugs - json_slugs)

    print(f'Artikel in JSON: {len(json_slugs)}, HTML: {len(html_slugs)}, fehlend: {len(missing)}')

    if not missing:
        print('Nichts zu tun.')
        return

    # 1. Convert missing WebP images
    converted = convert_missing_webp(missing)
    if converted:
        print(f'WebP konvertiert: {len(converted)}')
        for s in converted:
            print(f'  + {s}.webp')

    # 2. Extract metadata + append
    added = []
    for slug in missing:
        entry = extract_meta(slug)
        # verify image exists (webp preferred, png fallback)
        if not os.path.exists(os.path.join(IMG_DIR, entry['image'])):
            if os.path.exists(os.path.join(IMG_DIR, slug + '.png')):
                entry['image'] = slug + '.png'
            else:
                print(f'  ! Kein Bild für {slug}')
        data.append(entry)
        added.append(entry)
        print(f"  + {slug} [{entry['category']}] {entry['date']} ({entry['readingTime']} Min)")

    # 3. Write back (sorted by date desc for tidiness)
    data.sort(key=lambda a: a.get('date', '') or '', reverse=True)
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'\n✅ {len(added)} Artikel hinzugefügt. JSON jetzt: {len(data)} Artikel.')


if __name__ == '__main__':
    main()
