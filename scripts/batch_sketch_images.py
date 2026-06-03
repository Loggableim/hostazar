#!/usr/bin/env python3
"""Batch generate sketch-style hero images for ALL 58 hostazar articles via ComfyUI."""
import json, urllib.request, time, os, sys

COMFY_URL = "http://127.0.0.1:8189"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = os.path.join(REPO, "images")
LOG_FILE = os.path.join(IMG_DIR, "_sketch_batch_log.txt")

os.makedirs(IMG_DIR, exist_ok=True)

# Load article catalog
with open(os.path.join(REPO, "data", "artikel.json"), encoding="utf-8") as f:
    CATALOG = json.load(f)

# Per-article subject prompts
ARTICLE_PROMPTS = {
    "minecraft-server-vergleich-2026": "Minecraft server computer glowing purple, pixelated grass block, creeper face shadow, Ender pearl floating",
    "palworld-server-hosting-guide-2026": "Palworld game server, Pals creatures silhouettes, sphere orbs floating, fantasy survival server, lush island",
    "valheim-server-vps-mieten-2026": "Valheim viking server, Viking helmet, Yggdrasil tree, mead hall, Norse runes, dark forest",
    "cs2-server-mieten-guide-2026": "CS2 Counter-Strike server, tactical gear, bomb defuse kit, dust2 references, weapon silhouettes",
    "7-days-to-die-server-hosten-2026": "7 Days to Die zombie survival server, blood moon horde, fortified base, zombie silhouettes, wasteland",
    "ark-survival-ascended-server-hosten-2026": "ARK Survival Evolved server, dinosaur silhouette, Tek gear, obelisk, floating island",
    "dayz-server-mieten-2026": "DayZ survival server, Chernarus map, military bunker, zombie apocalypse, abandoned town",
    "enshrouded-server-hosting-2026": "Enshrouded game server, flame altar, shrouded fog, fantasy ruins, glowing lumen",
    "farming-simulator-25-server-mieten-2026": "Farming Simulator 25 server, tractor, harvester, wheat field, barn, farm equipment",
    "gameserver-mieten-guide": "generic game server rack, multiple game icons floating, neon glowing controllers",
    "grounded-server-hosting": "Grounded backyard server, giant insect silhouettes, grass blades towering, ant hill, lab equipment",
    "icarus-server-hosting": "Icarus survival server, space pod crash, alien planet, terraforming equipment, exosuit",
    "nightingale-server-hosting": "Nightingale realm server, Victorian fae realm, magical portals, estate building, antique lamp",
    "project-zomboid-server-hosting-2026": "Project Zomboid server, isometric zombie apocalypse, survival house, helicopter, Knox County",
    "rust-server-mieten-guide-2026": "Rust survival server, scrap metal base, AK-47 silhouette, radiation zone, loot crate",
    "satisfactory-server-mieten-oder-selbst-hosten-2026": "Satisfactory factory server, conveyor belts, space elevator, industrial complex, FICSIT equipment",
    "scum-server-mieten": "SCUM survival server, prison island, mech robot silhouette, loot crate, toxic zone",
    "smalland-server-hosting": "Smalland survival server, tiny character on giant mushroom, insect mount, fantasy forest",
    "sons-of-the-forest-server": "Sons of the Forest server, mutant cannibal silhouette, crashed helicopter, cave entrance, Kelvin robot",
    "space-engineers-server": "Space Engineers server, asteroid mining ship, space station, welding tool, planetary base",
    "terraria-server-hosten-2026": "Terraria server, Eye of Cthulhu, pickaxe, underground cavern, NPC houses, guide voodoo doll",
    "the-forest-server-hosting": "The Forest survival server, plane crash, cannibal effigy, cave entrance, mutants, tree house",
    "v-rising-server-mieten-2026": "V Rising vampire server, gothic castle, blood altar, bat swarm, dark throne, vampiric powers",
    # Webhosting
    "webhosting-anbieter-vergleich-2026": "web hosting provider comparison ranking, server tiers, globe network, data center racks, SSL shield",
    "webhosting-vserver-vergleich": "web hosting vs VPS comparison, shared server vs dedicated, pyramid of power, control panel screens",
    "hetzner-cloud-vs-dediziert-vergleich-2026": "Hetzner cloud vs dedicated server, German data center, server rack comparison, price tags",
    "netcup-vps-erfahrungen-2026": "Netcup VPS server, virtual machines, control panel, German hosting, server dashboard",
    "domain-kaufen-einrichten-2026": "domain registration purchase, DNS settings, globe with domain chains, registrar dashboard",
    "email-server-selbst-hosten-2026": "self-hosted email server, Postfix Dovecot, mail envelopes, encryption lock, mailbox rack",
    "ssl-zertifikat-lets-encrypt-2026": "SSL certificate Lets Encrypt, HTTPS padlock, certificate chain, secure connection shield",
    "website-online-bringen-guide-2026": "launch website online guide, rocket lifting globe, HTML code, browser window, hosting server",
    "wordpress-hosting-vergleich-2026": "WordPress hosting comparison, WP logo, themes and plugins, dashboard, blog setup",
    "cloudflare-tunnel-einrichten": "Cloudflare tunnel setup, orange cloud shield, tunnel visualization, global network, proxy flow",
    "plesk-vs-cpanel-vergleich": "Plesk vs cPanel hosting panel comparison, two control panels side by side, server admin interface",
    "mysql-mariadb-optimierung": "MySQL MariaDB database optimization, database cylinder, query performance graph, indexing gears",
    "nextcloud-server-einrichten": "Nextcloud self-hosted cloud server, cloud with folder icon, sync arrows, collaboration interface",
    "webseite-sicherheit-2026": "website security checklist 2026, firewall shield, lock icon, hacker protection, safe browsing",
    "docker-wordpress-hosten": "Docker WordPress hosting, container ship with WP logo, whale with WordPress, compose YAML",
    "cloud-hosting-vs-shared-hosting": "cloud hosting vs shared hosting comparison, scalability graph, shared vs distributed servers",
    # DevOps
    "devops-tools-2024": "devops tools collection, Docker, Kubernetes, Terraform, Ansible logos, CI/CD pipeline flow",
    "vps-absichern-2026": "VPS security hardening, SSH key, firewall shield, fail2ban, locked server rack, protection layers",
    "docker-compose-vps-guide": "Docker Compose on VPS, multi-container ship, reverse proxy Nginx, database container, web server",
    "docker-vs-podman-vergleich-2026": "Docker vs Podman comparison, container engines side by side, daemonless vs daemon architecture",
    "github-actions-ci-cd-pipeline-2026": "GitHub Actions CI/CD pipeline, YAML workflow, automated test, deploy arrows, runner bot",
    "k3s-kubernetes-vps-2026": "K3s lightweight Kubernetes on VPS, tiny K8s logo, cluster nodes, container orchestration",
    "nginx-reverse-proxy-einrichten-2026": "Nginx reverse proxy configuration, load balancer, upstream servers, SSL termination, traffic flow",
    "prometheus-grafana-monitoring-2026": "Prometheus Grafana monitoring, dashboard graphs, alert metrics, server health, visualization panels",
    "terraform-infrastructure-as-code-2026": "Terraform Infrastructure as Code, HCL configuration, cloud resources, plan apply workflow",
    "backup-strategien-vps-server-2026": "VPS backup strategy, 3-2-1 rule, hard drives, cloud backup, restore process, data protection",
    "gitops-argocd-einrichten": "GitOps ArgoCD deployment, git repository sync, Kubernetes cluster, continuous delivery pipeline",
    "linux-server-harden": "Linux server hardening, terminal command lines, security audit, kernel lock, root shield",
    "postgresql-vps-optimierung": "PostgreSQL VPS optimization, elephant logo, performance tuning, query optimization, database server",
    "traefik-reverse-proxy": "Traefik reverse proxy, modern proxy logo, automatic HTTPS, Docker service discovery, middleware chain",
    "elk-stack-log-management": "ELK Stack Elasticsearch Kibana Logstash, log analysis dashboard, data pipeline, server monitoring",
    "wireguard-vpn-server": "WireGuard VPN server setup, fast tunnel, key exchange, secure connection, global network nodes",
    "n8n-automation-server": "n8n workflow automation server, node connections, workflow diagram, automation triggers, self-hosted",
    "ansible-automation-guide": "Ansible automation guide, playbook YAML, infrastructure automation, control node, managed hosts",
}

SKETCH_STYLE = "sketch style, black and white charcoal pencil drawing, rough hand-drawn lines, crosshatching, unfinished concept art sketch, monochrome, minimalist linework, paper texture background, artistic sketching technique, no shading"
NEG = "color, photograph, painting, render, 3d, realistic, detailed textures, soft shading, gradient, blur, watermark, text, signature, vibrant, oil paint, watercolor, digital art"

def submit_prompt(prompt_text):
    workflow = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "RealVisXL_V4.0.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": f"{prompt_text}, {SKETCH_STYLE}", "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1216, "height": 640, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": 42, "control_after_generate": "randomize",
            "steps": 22, "cfg": 6.5, "sampler_name": "dpmpp_sde", "scheduler": "karras",
            "denoise": 1.0, "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "sketch_out", "images": ["6", 0]}}
    }
    data = json.dumps({"prompt": workflow, "client_id": "hostazar-sketch-batch"}).encode()
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp["prompt_id"]

def poll_history(pid, timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = json.loads(urllib.request.urlopen(urllib.request.Request(f"{COMFY_URL}/history/{pid}")).read())
            if pid in resp:
                entry = resp[pid]
                status = entry.get("status", {})
                if status.get("completed") or status.get("status_str") == "success":
                    return entry
                if status.get("status_str") == "error":
                    for mt, m in status.get("messages", []):
                        if mt == "execution_error": print(f"  ERROR: {m.get('exception_message','?')[:100]}")
                    return None
        except: pass
        time.sleep(2)
    return None

def download_image(filename, subfolder=""):
    url = f"{COMFY_URL}/view?{urllib.parse.urlencode({'filename':filename,'subfolder':subfolder,'type':'output'})}"
    urllib.request.urlretrieve(url, os.path.join(IMG_DIR, filename))
    return os.path.join(IMG_DIR, filename)

def get_latest_output(hist):
    for node_out in hist.get("outputs", {}).values():
        images = node_out.get("images", [])
        if images: return images[0]["filename"], images[0].get("subfolder", "")
    return None, None

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    print(msg)

if __name__ == "__main__":
    total = len(CATALOG)
    existing = [a['slug'] for a in CATALOG]
    
    log(f"Sketch-Batch: {total} Bilder")
    
    done = 0
    fail = 0
    skip = 0
    
    for idx, article in enumerate(CATALOG):
        slug = article['slug']
        title = article['title']
        target = os.path.join(IMG_DIR, f"{slug}.png")
        
        # Skip if already generated (check >50KB)
        if os.path.exists(target) and os.path.getsize(target) > 50000:
            skip += 1
            if idx % 5 == 0:
                log(f"  [{idx+1}/{total}] SKIP {slug} (exists)")
            continue
        
        # Get subject prompt
        subject = ARTICLE_PROMPTS.get(slug, f"{article['category']} server technology, technical equipment, data center")
        prompt = f"{subject}, detailed line art drawing"
        
        try:
            pid = submit_prompt(prompt)
            log(f"  [{idx+1}/{total}] → {slug}...")
            
            hist = poll_history(pid, timeout=180)
            if hist:
                fn, sub = get_latest_output(hist)
                if fn:
                    dl = download_image(fn, sub)
                    # Rename to slug.png
                    os.replace(dl, target)
                    done += 1
                    log(f"    ✓ {slug} ({os.path.getsize(target)/1024:.0f} KB)")
                else:
                    fail += 1
                    log(f"    ✗ {slug} no output")
            else:
                fail += 1
                log(f"    ✗ {slug} timeout/error")
        except Exception as e:
            fail += 1
            log(f"    ✗ {slug}: {str(e)[:100]}")
    
    log(f"=== FERTIG: {done} OK, {fail} FAIL, {skip} skipped ===")
