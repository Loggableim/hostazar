#!/usr/bin/env python3
"""
Auto internal linking for hostazar — kontextuelle Links zwischen Artikeln.
Läuft nach jedem Content-Update (manuell oder via Cron).
"""
import os, re, json, html as html_mod

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, "artikel")
SITE = "https://hostazar.com"
MAX_LINKS_PER_ARTICLE = 4
MAX_LINKS_PER_H2 = 1

# ── Topic → Interne Link-Ziele ──────────────────────────
# Jedes Keyword matched auf andere Artikel
TOPIC_MAP = {
    "gameserver": [
        ("/artikel/gameserver-mieten-guide.html", "Gameserver mieten – Guide"),
        ("/artikel/minecraft-server-vergleich-2026.html", "Minecraft Server Vergleich"),
    ],
    "minecraft": [
        ("/artikel/minecraft-server-vergleich-2026.html", "Minecraft Server mieten Vergleich"),
        ("/artikel/minecraft-server-mods-plugins-guide-2026.html", "Minecraft Modding-Guide"),
    ],
    "valheim": [
        ("/artikel/valheim-server-vps-mieten-2026.html", "Valheim Server Guide"),
    ],
    "7 days to die": [
        ("/artikel/7-days-to-die-server-hosten-2026.html", "7 Days to Die Server Guide"),
    ],
    "ark": [
        ("/artikel/ark-survival-ascended-server-hosten-2026.html", "ARK Server Guide"),
    ],
    "cs2": [
        ("/artikel/cs2-server-mieten-guide-2026.html", "CS2 Server Guide"),
    ],
    "dayz": [
        ("/artikel/dayz-server-mieten-2026.html", "DayZ Server Guide"),
    ],
    "rust": [
        ("/artikel/rust-server-mieten-guide-2026.html", "Rust Server Guide"),
    ],
    "palworld": [
        ("/artikel/palworld-server-hosting-guide-2026.html", "Palworld Server Guide"),
    ],
    "satisfactory": [
        ("/artikel/satisfactory-server-mieten-oder-selbst-hosten-2026.html", "Satisfactory Server Guide"),
    ],
    "terraria": [
        ("/artikel/terraria-server-hosten-2026.html", "Terraria Server Guide"),
    ],
    "phasmophobia": [
        ("/artikel/phasmophobia-server-hosten-2026.html", "Phasmophobia Server Guide"),
        ("/artikel/phasmophobia-server-mieten-2026.html", "Phasmophobia Server mieten"),
    ],
    "factorio": [
        ("/artikel/factorio-server-hosting-2026.html", "Factorio Server Guide"),
    ],
    "fivem": [
        ("/artikel/fivem-server-mieten-2026.html", "FiveM Server Guide"),
    ],
    "project zomboid": [
        ("/artikel/project-zomboid-server-hosting-2026.html", "Project Zomboid Server Guide"),
    ],
    "v rising": [
        ("/artikel/v-rising-server-mieten-2026.html", "V Rising Server Guide"),
    ],
    "enshrouded": [
        ("/artikel/enshrouded-server-hosting-2026.html", "Enshrouded Server Guide"),
    ],
    "lethal company": [
        ("/artikel/lethal-company-server-mieten-2026.html", "Lethal Company Server Guide"),
    ],
    "docker": [
        ("/artikel/docker-compose-vps-guide.html", "Docker Compose Guide"),
        ("/artikel/docker-vs-podman-vergleich-2026.html", "Docker vs Podman"),
    ],
    "nginx": [
        ("/artikel/nginx-reverse-proxy-einrichten-2026.html", "Nginx Reverse Proxy Guide"),
        ("/artikel/nginx-vs-apache-webserver-vergleich-2026.html", "Nginx vs Apache"),
    ],
    "postgresql": [
        ("/artikel/postgresql-vps-optimierung.html", "PostgreSQL Optimierung"),
        ("/artikel/postgresql-vs-mysql-vergleich-2026.html", "PostgreSQL vs MySQL"),
    ],
    "mysql": [
        ("/artikel/mysql-mariadb-optimierung.html", "MySQL Optimierung"),
        ("/artikel/postgresql-vs-mysql-vergleich-2026.html", "MySQL vs PostgreSQL"),
    ],
    "kubernetes": [
        ("/artikel/k3s-kubernetes-vps-2026.html", "K3s Kubernetes auf VPS"),
        ("/artikel/helm-charts-kubernetes-guide-2026.html", "Helm Charts Guide"),
    ],
    "terraform": [
        ("/artikel/terraform-infrastructure-as-code-2026.html", "Terraform IaC Guide"),
    ],
    "ansible": [
        ("/artikel/ansible-automation-guide.html", "Ansible Automation Guide"),
    ],
    "prometheus": [
        ("/artikel/prometheus-grafana-monitoring-2026.html", "Prometheus Monitoring"),
    ],
    "grafana": [
        ("/artikel/prometheus-grafana-monitoring-2026.html", "Grafana Dashboard"),
    ],
    "cloudflare": [
        ("/artikel/cloudflare-tunnel-einrichten.html", "Cloudflare Tunnel Setup"),
        ("/artikel/cloudflare-waf-einrichten-2026.html", "Cloudflare WAF Guide"),
    ],
    "backup": [
        ("/artikel/backup-strategien-vps-server-2026.html", "VPS Backup Strategien"),
    ],
    "vps": [
        ("/artikel/vps-mieten-vergleich-2026.html", "VPS mieten Vergleich"),
        ("/artikel/dedizierter-server-vs-vps-2026.html", "VPS vs Dediziert"),
    ],
    "hostinger": [
        ("/artikel/hostinger-review-2026.html", "Hostinger Review"),
    ],
    "hetzner": [
        ("/artikel/hetzner-cloud-vs-dediziert-vergleich-2026.html", "Hetzner Vergleich"),
    ],
    "netcup": [
        ("/artikel/netcup-vps-erfahrungen-2026.html", "Netcup VPS Erfahrungen"),
    ],
    "contabo": [
        ("/artikel/contabo-vps-erfahrungen-2026.html", "Contabo VPS Erfahrungen"),
    ],
    "llm": [
        ("/artikel/llm-lokal-hosten-2026.html", "LLM lokal hosten"),
        ("/artikel/ollama-llm-server-vps-2026.html", "Ollama LLM Server"),
    ],
    "ollama": [
        ("/artikel/ollama-llm-server-vps-2026.html", "Ollama Server"),
        ("/artikel/open-webui-ollama-betreiben-2026.html", "Open WebUI Guide"),
    ],
    "wireguard": [
        ("/artikel/wireguard-vpn-server.html", "WireGuard VPN Setup"),
    ],
    "wordpress": [
        ("/artikel/docker-wordpress-hosten.html", "WordPress mit Docker"),
        ("/artikel/wordpress-hosting-vergleich-2026.html", "WordPress Hosting Vergleich"),
    ],
    "nextcloud": [
        ("/artikel/nextcloud-server-einrichten.html", "Nextcloud Setup"),
    ],
    "linux": [
        ("/artikel/linux-server-harden.html", "Linux Server Härten"),
    ],
    "ssl": [
        ("/artikel/ssl-zertifikat-lets-encrypt-2026.html", "Let's Encrypt SSL"),
    ],
    "github actions": [
        ("/artikel/github-actions-ci-cd-pipeline-2026.html", "GitHub Actions CI/CD"),
    ],
    "gitlab": [
        ("/artikel/gitlab-ci-cd-pipeline-guide-2026.html", "GitLab CI/CD Guide"),
    ],
    "argocd": [
        ("/artikel/gitops-argocd-einrichten.html", "ArgoCD GitOps Guide"),
    ],
    "minio": [
        ("/artikel/minio-object-storage-selbst-hosten-2026.html", "MinIO Object Storage"),
    ],
    "n8n": [
        ("/artikel/n8n-automation-server.html", "n8n Automation"),
    ],
    "portainer": [
        ("/artikel/portainer-docker-management-vps-2026.html", "Portainer Docker Management"),
    ],
    "proxmox": [
        ("/artikel/proxmox-heimserver-einrichten-2026.html", "Proxmox Home Server"),
    ],
    "pterodactyl": [
        ("/artikel/pterodactyl-panel-installieren-2026.html", "Pterodactyl Panel"),
    ],
    "teamspeak": [
        ("/artikel/teamspeak-server-mieten-2026.html", "TeamSpeak Server"),
    ],
    "vaultwarden": [
        ("/artikel/vaultwarden-passwort-manager-selbst-hosten-2026.html", "Vaultwarden Passwort-Manager"),
    ],
}


def add_links(html):
    """Füge kontextuelle interne Links zu <p>-Absätzen hinzu."""
    # Nur innerhalb von <p>-Tags arbeiten (nicht in Nav, Footer, Code)
    paragraphs = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
    linked_count = 0
    
    for para_text in paragraphs:
        if linked_count >= MAX_LINKS_PER_ARTICLE:
            break
        
        # Skip already linked paragraphs
        if '<a href' in para_text:
            continue
        
        lower = para_text.lower()
        for keyword, links in TOPIC_MAP.items():
            if linked_count >= MAX_LINKS_PER_ARTICLE:
                break
            if keyword.lower() in lower:
                # Find first occurrence in text
                idx = lower.find(keyword.lower())
                if idx < 0:
                    continue
                
                # Pick link (cycle through if multiple)
                link_idx = 0
                for li, (url, title) in enumerate(links):
                    # Check if this URL is not this article itself
                    link_slug = url.replace('/artikel/', '').replace('.html', '')
                    if link_slug not in html:  # crude check, works for slugs
                        link_idx = li
                        break
                
                link_url, link_title = links[link_idx]
                
                # Build anchor
                original_word = para_text[idx:idx+len(keyword)]
                anchor = f'<a href="{link_url}" title="{link_title}">{original_word}</a>'
                
                # Replace in paragraph
                old = para_text
                para_text = para_text[:idx] + anchor + para_text[idx+len(keyword):]
                lower = para_text.lower()
                linked_count += 1
        
        # Replace paragraph in html
        if 'old' in dir() and para_text != old:
            html = html.replace(f'<p>{old}</p>', f'<p>{para_text}</p>', 1)
    
    return html, linked_count


# ── Main ──────────────────────────────────────────
total_links = 0
linked_articles = 0
for f in sorted(os.listdir(ARTIKEL_DIR)):
    if not f.endswith('.html'):
        continue
    fp = os.path.join(ARTIKEL_DIR, f)
    with open(fp, 'r') as fh:
        c = fh.read()
    
    new_c, count = add_links(c)
    if count > 0:
        with open(fp, 'w') as fh:
            fh.write(new_c)
        linked_articles += 1
        total_links += count
        if linked_articles <= 5:
            print(f'✅ {f}: {count} Links', flush=True)

print(f'\n✅ {linked_articles} Artikel mit {total_links} neuen internen Links', flush=True)
