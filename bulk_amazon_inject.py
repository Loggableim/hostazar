#!/usr/bin/env python3
"""Bulk-inject Amazon affiliate links (tag=nova079-20) into hostazar.com articles."""
import os, re, glob

ARTIKEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'artikel')

CATEGORY_PRODUCTS = {
    "gaming-server": {
        "kw": "Gaming+Server+Hardware+2026",
        "title": "Gaming-Server-Hardware & Zubehör 2026",
        "cta": "Server-Hardware & Gaming-Equipment auf Amazon entdecken"
    },
    "devops": {
        "kw": "DevOps+Server+Infrastructure+Hardware",
        "title": "DevOps-Server-Hardware & Netzwerk-Equipment 2026",
        "cta": "Server-Equipment & Netzwerk-Hardware auf Amazon entdecken"
    },
    "webhosting": {
        "kw": "Server+Webhosting+Hardware+Equipment",
        "title": "Server-Hardware & Webhosting-Zubehör 2026",
        "cta": "Server-Equipment & Zubehör auf Amazon entdecken"
    },
    "ki-llm": {
        "kw": "NVIDIA+GPU+Künstliche+Intelligenz+Server",
        "title": "KI-Server-Hardware & GPUs 2026",
        "cta": "GPUs & KI-Hardware auf Amazon entdecken"
    },
    "vps": {
        "kw": "Server+Netzwerk+Hardware+HomeLab",
        "title": "VPS-Server-Hardware & Netzwerk-Equipment 2026",
        "cta": "Server-Equipment & Netzwerk-Hardware auf Amazon entdecken"
    },
    "tools": {
        "kw": "HomeLab+Server+Zubehör+Netzwerk",
        "title": "HomeLab-Server-Equipment & Tools 2026",
        "cta": "Server-Zubehör & Netzwerk-Tools auf Amazon entdecken"
    }
}

def categorize(slug):
    gaming = ['server-hosten','server-mieten','mieten-guide','server-hosting','server-mods','gameserver','-server-','gaming','7-days-to-die','ark-survival','conan-exiles','cs2-server','dayz','deep-rock','dont-starve','enshrouded','escape-from-tarkov','factorio','farming-simulator','fivem','grounded','helldivers','icarus','lethal-company','minecraft','nightingale','palworld','phasmophobia','project-zomboid','pubg','raft-server','rust-server','satisfactory','scum','smalland','sons-of-the-forest','space-engineers','terraria','the-forest','valheim','v-rising','gaming-pc','gaming-monitore','steam-deck','beste-gaming']
    devops = ['ansible','terraform','docker','kubernetes','k3s','helm','gitops','argocd','jenkins','github-actions','gitlab-ci','prometheus','grafana','elk-stack','elastic','loki','caddy','traefik','nginx','reverse-proxy','cloudflare','wireguard','openvpn','linux-server-harden','vps-absichern','backup-strategien','minio','portainer','cloud-gpu','devops-tools','mysql','mariadb','postgresql','redis','uptime-kuma']
    webhosting = ['webhosting','hosting-vergleich','wordpress-hosting','managed-wordpress','plesk','cpanel','domain-kaufen','email-server','ghost-cms','website-online','webseite-sicherheit','webseite-geschwindigkeit','lamp-stack','lemp-stack','ssl-zertifikat','cloudflare-pages','netlify','vercel']
    ki = ['llm','gpu','cuda','rocam','vulkan','ollama','vllm','künstliche-intelligenz','ki-server','ki-modelle','comfyui','deepseek','llama','mistral','open-webui','quantisierte-modelle','gguf','text-generation-webui','openrouter','runpod','vast-ai','nvidia-jetson','tabbyapi','free-llm','llm-sicherheit','ki-gestuetzte','ki-im-devops','llm-fine-tuning','llm-frontends']
    vps = ['vps-mieten','vps-anbieter','contabo-vps','netcup-vps','hetzner','cloud-hosting','cloud-vs-dedicated','dedizierter-server','webhosting-vserver']
    for kw in gaming:
        if kw in slug: return 'gaming-server'
    for kw in ki:
        if kw in slug: return 'ki-llm'
    for kw in devops:
        if kw in slug: return 'devops'
    for kw in webhosting:
        if kw in slug: return 'webhosting'
    for kw in vps:
        if kw in slug: return 'vps'
    return 'tools'

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        t = m.group(1).strip()
        t = re.sub(r'\s*[|–-]\s*hostazar\.com.*$', '', t).strip()
        return t
    return None

def build_kw(title):
    if not title: return None
    title = re.sub(r'&[a-z]+;', ' ', title)
    title = re.sub(r'\b20\d{2}\b', '', title)
    title = re.sub(r'\s*[|–-].*$', '', title)
    title = re.sub(r'[^\w\s]', ' ', title)
    words = [w for w in title.split() if len(w) > 2][:4]
    return '+'.join(words) if words else None

def build_block(amazon_kw, cat_key):
    cat = CATEGORY_PRODUCTS.get(cat_key, CATEGORY_PRODUCTS['tools'])
    kw = amazon_kw if amazon_kw else cat['kw']
    url = f'https://www.amazon.de/s?k={kw}&amp;tag=nova079-20'
    return f'''
<div class="affiliate-box" style="margin:30px 0;padding:20px;background:linear-gradient(135deg,#667eea22,#764ba222);border:1px solid #667eea44;border-radius:12px;text-align:center">
<p><strong>🔧 {cat["title"]}</strong></p>
<p style="margin:10px 0;font-size:.95rem">Du möchtest dein Setup optimieren? Hier findest du passende Hardware, Zubehör und Equipment:</p>
<a href="{url}" class="btn" rel="nofollow noopener" target="_blank" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border-radius:8px;text-decoration:none;font-weight:600">👉 {cat["cta"]}</a>
</div>
'''

files = sorted(glob.glob(os.path.join(ARTIKEL_DIR, '*.html')))
injected = 0
failed = 0

for fp in files:
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if 'tag=nova079-20' in content:
        continue
    slug = os.path.splitext(os.path.basename(fp))[0]
    cat = categorize(slug)
    title = extract_title(content)
    kw = build_kw(title) if title else slug.replace('-','+')
    block = build_block(kw, cat)
    
    new_content = content.replace('</main>', block + '\n\n</main>', 1)
    if new_content == content:
        new_content = content.replace('<footer', block + '\n\n<footer', 1)
    if new_content == content:
        print(f'  ⚠️ SKIPPED: {slug}')
        failed += 1
        continue
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
    injected += 1
    print(f'  ✅ {slug} [{cat}]')

print(f'\n📊 ERGEBNIS: {injected} injiziert, {failed} übersprungen/fehlgeschlagen')
