#!/usr/bin/env python3
"""
Inject Amazon affiliate links (tag=nova079-20) into hostazar.com articles.
Only articles without existing links get injected.
Injects an affiliate-box before </main> with category-relevant product links.
"""
import os, re, glob

ARTIKEL_DIR = r"C:\HermesPortable\home\scripts\blog-automation\hostazar\artikel"

# Category-based Amazon keyword mappings
# For each category, define the search term and display text
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
    },
    "hosting-comparison": {
        "kw": "Server+Hosting+Netzwerk+Hardware",
        "title": "Server-Hardware-Vergleich & Empfehlungen 2026",
        "cta": "Server-Equipment & Hardware auf Amazon vergleichen"
    }
}

def categorize_article(slug):
    """Determine article category from filename slug."""
    gaming_keywords = [
        "server-hosten", "server-mieten", "mieten-guide", "server-hosting",
        "server-mods", "gameserver", "-server-", "gaming",
        "7-days-to-die", "ark-survival", "conan-exiles", "cs2-server", "dayz",
        "deep-rock", "dont-starve", "enshrouded", "escape-from-tarkov",
        "factorio", "farming-simulator", "fivem", "grounded", "helldivers",
        "icarus", "lethal-company", "minecraft", "nightingale", "palworld",
        "phasmophobia", "project-zomboid", "pubg", "raft-server", "rust-server",
        "satisfactory", "scum", "smalland", "sons-of-the-forest", "space-engineers",
        "terraria", "the-forest", "valheim", "v-rising", "gaming-pc", "gaming-monitore",
        "steam-deck", "beste-gaming"
    ]
    devops_keywords = [
        "ansible", "terraform", "docker", "kubernetes", "k3s", "helm",
        "gitops", "argocd", "jenkins", "github-actions", "gitlab-ci",
        "prometheus", "grafana", "elk-stack", "elastic", "loki",
        "caddy", "traefik", "nginx", "reverse-proxy", "cloudflare",
        "wireguard", "openvpn", "linux-server-harden", "vps-absichern",
        "backup-strategien", "minio", "portainer", "cloud-gpu",
        "devops-tools", "gitops", "mysql", "mariadb", "postgresql",
        "redis", "uptime-kuma"
    ]
    webhosting_keywords = [
        "webhosting", "hosting-vergleich", "wordpress-hosting",
        "managed-wordpress", "plesk", "cpanel", "domain-kaufen",
        "email-server", "ghost-cms", "website-online",
        "webseite-sicherheit", "webseite-geschwindigkeit",
        "lamp-stack", "lemp-stack", "ssl-zertifikat",
        "cloudflare-pages", "netlify", "vercel"
    ]
    ki_keywords = [
        "llm", "gpu", "cuda", "rocam", "vulkan", "ollama", "vllm",
        "künstliche-intelligenz", "ki-server", "ki-modelle",
        "comfyui", "deepseek", "llama", "mistral", "open-webui",
        "quantisierte-modelle", "gguf", "text-generation-webui",
        "openrouter", "runpod", "vast-ai", "nvidia-jetson",
        "tabbyapi", "free-llm", "llm-sicherheit", "ki-gestuetzte",
        "ki-im-devops", "llm-fine-tuning", "llm-frontends"
    ]
    vps_keywords = [
        "vps-mieten", "vps-anbieter", "contabo-vps", "netcup-vps",
        "hetzner", "cloud-hosting", "cloud-vs-dedicated",
        "dedizierter-server", "webhosting-vserver"
    ]

    for kw in gaming_keywords:
        if kw in slug:
            return "gaming-server"
    for kw in ki_keywords:
        if kw in slug:
            return "ki-llm"
    for kw in devops_keywords:
        if kw in slug:
            return "devops"
    for kw in webhosting_keywords:
        if kw in slug:
            return "webhosting"
    for kw in vps_keywords:
        if kw in slug:
            return "vps"
    return "tools"  # fallback

def extract_title(html):
    """Extract the article title from the HTML."""
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        # Remove site name suffix
        title = re.sub(r'\s*[|–-]\s*hostazar\.com.*$', '', title).strip()
        return title
    return None

def extract_h1(html):
    """Extract the first h1 tag content."""
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    # Try to find text after <!-- article content starts -->
    m = re.search(r'class="[^"]*article-content[^"]*"[^>]*>(.*?)(?:<h2|<section|<div class=")', html, re.IGNORECASE | re.DOTALL)
    return None

def get_slug_from_title(title):
    """Create an Amazon-friendly search keyword from the title."""
    if not title:
        return None
    # Remove HTML entities
    title = re.sub(r'&[a-z]+;', ' ', title)
    # Keep meaningful keywords (remove year numbers and filler words)
    title = re.sub(r'\b20\d{2}\b', '', title)  # remove years
    # Remove common suffixes
    title = re.sub(r'\s*[|–-].*$', '', title)
    # Remove special chars but keep spaces
    title = re.sub(r'[^\w\s]', ' ', title)
    # Limit to first ~4 meaningful words
    words = [w for w in title.split() if len(w) > 2][:4]
    if not words:
        return None
    return "+".join(words)

def build_affiliate_block(amazon_kw, category_key):
    """Build the affiliate HTML block."""
    cat = CATEGORY_PRODUCTS.get(category_key, CATEGORY_PRODUCTS["tools"])
    
    if amazon_kw:
        full_kw = amazon_kw
    else:
        full_kw = cat["kw"]
    
    url = f"https://www.amazon.de/s?k={full_kw}&amp;tag=nova079-20"
    
    return f'''
<div class="affiliate-box" style="margin:30px 0;padding:20px;background:linear-gradient(135deg,#667eea22,#764ba222);border:1px solid #667eea44;border-radius:12px;text-align:center">
<p><strong>🔧 {cat["title"]}</strong></p>
<p style="margin:10px 0;font-size:.95rem">Du möchtest dein Setup optimieren? Hier findest du passende Hardware, Zubehör und Equipment:</p>
<a href="{url}" class="btn" rel="sponsored noopener noreferrer" target="_blank" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border-radius:8px;text-decoration:none;font-weight:600">👉 {cat["cta"]}</a>
</div>
'''

def inject_amazon(filepath):
    """Inject Amazon affiliate link into an article if missing."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Skip if already has links
    if 'tag=nova079-20' in content:
        return False
    
    # Extract slug from filename
    slug = os.path.splitext(os.path.basename(filepath))[0]
    
    # Categorize
    category = categorize_article(slug)
    
    # Get title for keyword generation
    title = extract_title(content)
    if title:
        amazon_kw = get_slug_from_title(title)
    else:
        amazon_kw = slug.replace('-', '+')
    
    # Build affiliate block
    block = build_affiliate_block(amazon_kw, category)
    
    # Inject before </main>
    replacement = block + '\n\n</main>'
    new_content = content.replace('</main>', replacement, 1)
    
    if new_content == content:
        # Try alternative: before <footer
        replacement = block + '\n\n<footer'
        new_content = content.replace('<footer', replacement, 1)
    
    if new_content == content:
        return False  # Could not inject
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    files = sorted(glob.glob(os.path.join(ARTIKEL_DIR, "*.html")))
    total = len(files)
    injected = 0
    skipped = 0
    failed = 0
    
    for fp in files:
        # Skip word_count.py if it somehow ended up here
        if 'word_count' in fp:
            continue
        try:
            if inject_amazon(fp):
                injected += 1
                print(f"  ✅ {os.path.basename(fp)}")
            else:
                skipped += 1
        except Exception as e:
            failed += 1
            print(f"  ❌ {os.path.basename(fp)}: {e}")
    
    print(f"\n📊 Ergebnis: {injected} injiziert, {skipped} übersprungen (bereits vorhanden oder fehlgeschlagen), {failed} Fehler")
    print(f"   Neue Gesamtanzahl mit Amazon-Links: {injected + 4} / {total}")

if __name__ == "__main__":
    main()
