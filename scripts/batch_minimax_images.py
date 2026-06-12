#!/usr/bin/env python3
"""
MASSIVE MiniMax Batch — generiert ALLE 147 hostazar Hero-Bilder NEU
mit dem neuen Brand-Style: furry editorial illustration, B&W + accent color

Usage:  python scripts/batch_minimax_images.py
Env:    MINIMAX_API_KEY in C:\sidekick\home\.env
"""
import json, urllib.request, time, os, re, sys
from io import BytesIO
from PIL import Image

# --- Config ---
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = os.path.join(REPO, "images")
LOG_FILE = os.path.join(IMG_DIR, "_minimax_batch_log.txt")
os.makedirs(IMG_DIR, exist_ok=True)

# MiniMax Setup
with open('C:/sidekick/home/.env', 'r') as f:
    env_content = f.read()
m = re.search(r'MINIMAX_API_KEY=(\S+)', env_content)
API_KEY = m.group(1)
API_URL = "https://api.minimax.io/v1/image_generation"

# === BRAND STYLE (IMMER IDENTISCH) ===
BRAND_STYLE = (
    "furry editorial illustration, anthropomorphic animal characters, "
    "black and white artwork with a single accent color, bold black ink outlines, "
    "high contrast monochrome shading, clean vector illustration, graphic novel aesthetics, "
    "editorial magazine artwork, dynamic composition, expressive characters, "
    "selective color highlights, professional commercial illustration, crisp linework, halftone textures"
)

NEGATIVE = (
    "photorealistic, painting, oil paint, watercolor, 3d render, photograph, "
    "realistic lighting, soft shading, gradient blur, signature, watermark, text, "
    "low quality, ugly, deformed, blurry"
)

# === PER-ARTICLE SUBJECT PROMPTS ===
SUBJECT_PROMPTS = {
    # ----- GAMESERVER (A-Z) -----
    "7-days-to-die-server-hosten-2026": "anthropomorphic zombie wolf survivor, fortified base with turrets, blood moon rising, wasteland landscape",
    "ark-survival-ascended-server-hosten-2026": "anthropomorphic raptor tamer with tek gear, floating obelisk, dinosaur silhouettes at sunset",
    "baldurs-gate-3-server-mieten-2026": "anthropomorphic tiefling wizard with magic staff, D&D dice tower, mind flayer silhouette, campfire glow",
    "conan-exiles-server-hosten": "anthropomorphic barbarian warrior with greatsword, desert temple ruins, giant snake, sandstorm approaching",
    "cs2-server-mieten-guide-2026": "anthropomorphic counter-terrorist fox, tactical gear, bomb defuse kit, dust2 reference, weapon silhouettes",
    "dayz-server-mieten-2026": "anthropomorphic survivor wolf in military gear, abandoned chernarus town, zombie horde distant",
    "deep-rock-galactic-server-mieten-2026": "anthropomorphic dwarf miner with pickaxe and beer, glowing crystals, space rig, dark caves",
    "dont-starve-together-server-hosten-2026": "anthropomorphic Maxwell shadow demon, campfire in dark forest, Chester companion, nightmare fuel",
    "enshrouded-server-hosting-2026": "anthropomorphic flame warden with magic shield, shrouded mist, fantasy ruins, glowing lumen tree",
    "escape-from-tarkov-server-hosten-2026": "anthropomorphic bear operator with tactical vest, tarkov city ruins, weapon modding bench",
    "factorio-server-hosting-2026": "anthropomorphic engineer rabbit with wrench, conveyor belts, space elevator, industrial factory complex",
    "farming-simulator-25-server-mieten-2026": "anthropomorphic farmer pig with straw hat, tractor, harvester, wheat field, barn with silo",
    "fivem-server-mieten-2026": "anthropomorphic police dog with radio, sports car, los santos skyline, neon signs reflection",
    "gameserver-mieten-guide": "anthropomorphic gaming raccoon, multiple game server racks, neon controllers floating, RGB cables",
    "gaming-pc-finanzieren": "anthropomorphic finance badger with glasses, gaming PC parts, euro coins, investment growth chart",
    "grounded-server-hosting": "anthropomorphic ant soldier with acorn helmet, giant grass blades, spider web, lab equipment in backyard",
    "helldivers-2-server-hosten-2026": "anthropomorphic helldiver eagle with cape, super destroyer orbital strike, bug swarm, galactic map",
    "icarus-server-hosting": "anthropomorphic space explorer otter with exosuit, crashed escape pod, alien planet, terraforming equipment",
    "lethal-company-server-mieten-2026": "anthropomorphic scavenger cat with scrap metal, abandoned industrial moon, monster silhouette, spaceship",
    "minecraft-bedrock-vs-java-server-2026": "anthropomorphic creeper and enderman debating, pixelated blocks, nether portal glow, redstone contraptions",
    "minecraft-server-mods-plugins-guide-2026": "anthropomorphic villager librarian with enchanted book, modded weapons, plugin config, crafting table",
    "minecraft-server-vergleich-2026": "anthropomorphic enderman with purple glow, server comparison chart, grass and netherrack blocks",
    "nightingale-server-hosting": "anthropomorphic realmwalker fox with victorian coat, magical portal, estate building, antique lamp, fae realm",
    "palworld-server-hosting-guide-2026": "anthropomorphic pal tamer with sphere orbs, pals creatures, fantasy island, survival base building",
    "phasmophobia-server-hosten-2026": "anthropomorphic ghost hunter cat with EMF reader, asylum corridor, UV light, ghost orb floating",
    "phasmophobia-server-mieten-2026": "anthropomorphic paranormal investigator dog, spirit box, crucifix, haunted mansion, ghost silhouette",
    "project-zomboid-server-hosting-2026": "anthropomorphic survivor crow, isometric zombie apocalypse, boarded house, helicopter flyover, knox county",
    "pterodactyl-panel-installieren-2026": "anthropomorphic pterodactyl tech bird, game panel dashboard, server management, wingspan servers",
    "pubg-server-mieten-2026": "anthropomorphic battle royale wolf with parachute, military gear, erangel map, chicken dinner trophy",
    "raft-server-mieten-2026": "anthropomorphic survival otter on raft, shark fin in water, floating debris, hook and rope, island in distance",
    "rust-server-mieten-guide-2026": "anthropomorphic rust survivor bear, scrap metal base, AK-47, radiation zone, loot crate, burning barrel",
    "satisfactory-server-mieten-oder-selbst-hosten-2026": "anthropomorphic FICSIT engineer rabbit, conveyor belts, space elevator, factory complex, hypertubes",
    "scum-server-mieten": "anthropomorphic prisoner wolf, prison island, mech robot, loot crate, toxic zone, survival gear",
    "smalland-server-hosting": "anthropomorphic tiny fox on giant mushroom, insect mount, fantasy forest, miniature camp, firefly lantern",
    "sons-of-the-forest-server": "anthropomorphic survivor fox with tactical gear, crashed helicopter, cave entrance, kelvin robot, mutants",
    "space-engineers-server": "anthropomorphic engineer otter in spacesuit, asteroid mining ship, space station, welding tool, planets",
    "terraria-server-hosten-2026": "anthropomorphic guide cat with guide voodoo doll, eye of cthulhu, underground cavern, pickaxe, npc houses",
    "the-forest-server-hosting": "anthropomorphic plane crash survivor wolf, cannibal effigy, cave entrance, tree house, mutants, fire",
    "valheim-server-vps-mieten-2026": "anthropomorphic viking bear with helmet and shield, yggdrasil tree, mead hall, norse runes, longship",
    "v-rising-server-mieten-2026": "anthropomorphic vampire bat lord, gothic castle, blood altar, dark throne, bat swarm, full moon",
    # ----- WEBHOSTING -----
    "caddy-web-server-einrichten-2026": "anthropomorphic caddy deer with HTTPS shield, reverse proxy diagram, automatic SSL, configuration file",
    "cloud-hosting-vs-shared-hosting": "anthropomorphic cloud cat vs groundhog, scalability graph, shared vs distributed servers, cloud nodes",
    "cloudflare-tunnel-einrichten": "anthropomorphic cloudflare fox with orange shield, tunnel visualization, global network, proxy flow arrows",
    "cloudflare-pages-vercel-netlify-vergleich-2026": "anthropomorphic deployment bear comparing three server options, CI/CD pipeline, static hosting logos",
    "cloudflare-waf-einrichten-2026": "anthropomorphic security wolf with WAF shield, bot filter, DDoS protection, firewall rules, orange cloud",
    "cloud-vs-dedicated-server-2026": "anthropomorphic cloud bird vs dedicated bull, server rack comparison, cost graph, performance chart",
    "dedizierter-server-vs-vps-2026": "anthropomorphic dedicated dragon vs VPS rabbit, server tiers comparison, resource allocation diagram",
    "docker-wordpress-hosten": "anthropomorphic whale captain with WordPress logo, container ship, compose YAML, sailing on data ocean",
    "domain-kaufen-einrichten-2026": "anthropomorphic domain registrar cat with globe, DNS settings chain, registrar dashboard, domain search",
    "email-server-selbst-hosten-2026": "anthropomorphic postmaster owl, postfix dovecot envelopes, encryption lock, mail server rack, spam filter",
    "ghost-cms-hosting-vps-2026": "anthropomorphic ghost editor cat, publishing platform, blog dashboard, newsletter, membership setup",
    "hetzner-cloud-vs-dediziert-vergleich-2026": "anthropomorphic german engineer bear, hetzner data center, server comparison, price tags, cloud vs dedicated",
    "hostinger-review-2026": "anthropomorphic hostinger reviewer fox, hPanel dashboard, hosting plans, speed test results, website builder",
    "lemp-stack-vps-einrichten-2026": "anthropomorphic linux penguin with LEMP stack tools, nginx server, database, PHP, terminal commands",
    "lamp-stack-vs-lemp-stack-vergleich-2026": "anthropomorphic lamp sheep vs lemp fox, apache vs nginx, database comparison, web stack architecture",
    "managed-wordpress-hosting-vergleich-2026": "anthropomorphic WP expert cat, wordpress logos comparison, managed hosting tiers, caching plugins, CDN globe",
    "mysql-mariadb-optimierung": "anthropomorphic database dolphin vs seahorse, database cylinders, query optimization, indexing gears, performance graph",
    "netcup-vps-erfahrungen-2026": "anthropomorphic netcup reviewer raccoon, VPS dashboard, german hosting control panel, server stats",
    "nextcloud-server-einrichten": "anthropomorphic cloud fox with folder icon, sync arrows, collaboration interface, self-hosted cloud server",
    "nginx-reverse-proxy-einrichten-2026": "anthropomorphic nginx deer with proxy diagram, load balancer, upstream servers, SSL termination, traffic flow",
    "nginx-vs-apache-webserver-vergleich-2026": "anthropomorphic nginx cheetah vs apache buffalo, web server comparison, speed race, configuration battle",
    "plesk-vs-cpanel-vergleich": "anthropomorphic plesk owl vs cpanel eagle, control panel comparison, server admin interface, hosting management",
    "postgresql-vs-mysql-vergleich-2026": "anthropomorphic postgresql elephant vs mysql dolphin, database comparison, SQL query, performance benchmark",
    "postgresql-vps-optimierung": "anthropomorphic postgresql elephant with tuning tools, VPS optimization, query planner, performance dashboard",
    "ssl-zertifikat-lets-encrypt-2026": "anthropomorphic SSL shield cat, HTTPS padlock, certificate chain, let's encrypt, secure connection",
    "webhosting-anbieter-vergleich-2026": "anthropomorphic hosting reviewer owl, provider comparison ranking, server tiers, data center racks, globe network",
    "webhosting-sicherheit-ddos-schutz-waf-2026": "anthropomorphic security fox with WAF shield, DDoS protection, firewall, malware guard, safe server",
    "webhosting-vserver-vergleich": "anthropomorphic hosting comparison bear, shared vs VPS vs dedicated tiers, pyramid of power, control panels",
    "webseite-geschwindigkeit-optimieren-2026": "anthropomorphic speed cheetah with optimization tools, loading speed graph, CDN, cache, performance rocket",
    "webseite-sicherheit-2026": "anthropomorphic security badger with checklist, firewall shield, hacker protection, safe browsing, SSL lock",
    "website-online-bringen-guide-2026": "anthropomorphic rocket scientist fox, rocket lifting globe, HTML code, browser window, hosting server launch",
    "wordpress-hosting-vergleich-2026": "anthropomorphic WP expert cat, WordPress logos comparison, themes and plugins, dashboard, hosting tiers",
    # ----- DEVOPS -----
    "ansible-automation-guide": "anthropomorphic ansible robot fox, playbook YAML, automation diagram, control node, managed hosts, infrastructure gears",
    "backup-strategien-vps-server-2026": "anthropomorphic backup badger with 3-2-1 rule, hard drives shield, cloud backup, restore process, data protection",
    "docker-compose-vps-guide": "anthropomorphic docker whale captain with compose YAML, multi-container ship, reverse proxy, database, web server",
    "docker-container-security-best-practices-2026": "anthropomorphic docker security cat, container shield, image scanning, secrets management, secured containers",
    "docker-vs-podman-vergleich-2026": "anthropomorphic docker whale vs podman pony, container engines side by side, daemonless vs daemon architecture",
    "elk-stack-log-management": "anthropomorphic elk trio: elasticsearch elephant, kibana owl, logstash fox, log analysis dashboard, server monitoring",
    "github-actions-ci-cd-pipeline-2026": "anthropomorphic github actions cat, YAML workflow pipeline, test automation, deploy arrows, runner bot, CI/CD flow",
    "gitlab-ci-cd-pipeline-guide-2026": "anthropomorphic gitlab fox with CI/CD pipeline, merge request, test stages, deployment environments",
    "gitops-argocd-einrichten": "anthropomorphic argocd deer with git repository, kubernetes cluster, sync arrows, continuous delivery pipeline",
    "grafana-loki-log-aggregation-vps-2026": "anthropomorphic grafana bear with loki fox, log aggregation dashboard, server metrics, monitoring panels",
    "jenkins-ci-cd-pipeline-vps-2026": "anthropomorphic jenkins robot with pipeline, build stages, test automation, deployment, blue ocean interface",
    "k3s-kubernetes-vps-2026": "anthropomorphic k3s cat with tiny kubernetes logo, cluster nodes on VPS, container orchestration, lightweight K8s",
    "linux-server-harden": "anthropomorphic linux penguin with security tools, terminal commands, security audit, firewall, ssh key shield",
    "minio-object-storage-selbst-hosten-2026": "anthropomorphic minio storage deer, S3-compatible cloud, object storage buckets, data replication, hosted on VPS",
    "n8n-automation-server": "anthropomorphic n8n workflow cat, node connections, automation triggers, workflow diagram, self-hosted server",
    "prometheus-grafana-monitoring-2026": "anthropomorphic prometheus bear with grafana owl, monitoring dashboard, alert metrics, server health graphs",
    "terraform-infrastructure-as-code-2026": "anthropomorphic terraform rhino, infrastructure as code, HCL config, cloud resources, plan apply workflow",
    "traefik-reverse-proxy": "anthropomorphic traefik fox with proxy logo, automatic HTTPS, docker service discovery, middleware chain diagram",
    "uptime-kuma-monitoring-einrichten-2026": "anthropomorphic kuma bear with monitoring dashboard, uptime status, server health, notification alerts",
    "vps-absichern-2026": "anthropomorphic security wolf with locked server, SSH key shield, firewall, fail2ban, protection layers, encrypted lock",
    "vps-anbieter-vergleich-2026": "anthropomorphic VPS comparison owl, server tiers ranking, price comparison, performance chart, data centers",
    "vps-mieten-vergleich-2026": "anthropomorphic VPS shopping cat, server plans comparison, budget vs premium tiers, cloud providers logos",
    "wireguard-vpn-server": "anthropomorphic wireguard penguin with fast tunnel, key exchange, secure connection, global network nodes, VPN shield",
    # ----- KI & LLM -----
    "ai-agent-frameworks-2026": "anthropomorphic AI agent fox with multiple robot assistants, langchain crewai autogen, neural network connections",
    "cloud-gpu-kosten-vergleich-2026": "anthropomorphic cloud GPU racoon, GPU server comparison, A100 H100 RTX4090, price per hour chart, cloud providers",
    "comfyui-auf-gpu-hosten": "anthropomorphic comfyui artist cat with GPU server, workflow nodes, stable diffusion generation, canvas interface",
    "cuda-rocam-vulkan-lokale-llm-gpu-backend-vergleich-2026": "anthropomorphic GPU backend owl, CUDA nvidia, ROCm amd, Vulkan comparison, GPU architecture diagram",
    "deepseek-r1-v3-lokal-hosten-2026": "anthropomorphic deepseek dragon with MoE architecture, GPU server, model quantization, local LLM hosting",
    "devops-tools-2024": "anthropomorphic devops octopus with multiple tools: docker, kubernetes, terraform, ansible, CI/CD pipeline tools",
    "discord-bot-vps-hosten-2026": "anthropomorphic discord bot cat with VPS server, discord logo, bot commands, moderation tools, voice channels",
    "docker-llm-inference-container": "anthropomorphic docker whale with LLM container, GPU passthrough, ollama in container, inference pipeline",
    "free-llm-benchmark-2026": "anthropomorphic benchmarking owl with LLM models comparison, performance chart, speed test, quality metrics",
    "gaestebeitrag-finanz-junkie-server-kosten-investor-guide": "anthropomorphic investor fox with server costs, financial graphs, hosting investment, money growth chart",
    "gitea-git-server-vps-2026": "anthropomorphic gitea gopher with git server, repository management, pull requests, VPS hosted, development tools",
    "gpu-fuer-ki-modelle-mieten-2026": "anthropomorphic GPU rental cat, cloud GPU comparison, A100 H100 L40S, hourly pricing, deep learning setup",
    "gpu-ram-manager-2026": "anthropomorphic VRAM manager rabbit, GPU memory allocation graph, model loading, CUDA memory, optimization tools",
    "helm-charts-kubernetes-guide-2026": "anthropomorphic helm ship captain with kubernetes charts, package management, deployment templates, cluster on sea",
    "hugo-astro-static-site-vergleich-2026": "anthropomorphic static site builder fox, hugo vs astro comparison, SSG speed, markdown workflow, deployment",
    "istio-service-mesh-2026": "anthropomorphic istio service mesh cat, envoy sidecar proxies, traffic routing, security shield, kubernetes service graph",
    "jitsi-meet-server-vps-2026": "anthropomorphic jitsi deer with video conference, VPS hosted, multiple participants, screen sharing, chat bubbles",
    "ki-gestuetzte-code-reviews-praxis-2026": "anthropomorphic AI code reviewer owl, code analysis, PR review, robot assistant with glasses, github integration",
    "ki-im-devops-einsatz-2026": "anthropomorphic AI devops bear, automated incident response, monitoring AI, chatops, LLM integrated pipeline",
    "ki-server-sicherheit-llm-api-absichern-2026": "anthropomorphic LLM security wolf, API shield, prompt injection protection, model firewall, safe AI server",
    "llama-3-3-4-lokal-hosten-2026": "anthropomorphic llama with 70B model, GPU server rack, local LLM hosting, quantization, inference speed",
    "llama-cpp-cpu-vs-gpu-performance-2026": "anthropomorphic llama engineer, CPU vs GPU performance chart, benchmark comparison, GGUF models, speed test",
    "llm-fine-tuning-runpod-vastai-2026": "anthropomorphic fine-tuning fox with GPU cloud, runpod vastai comparison, training dashboard, model customization",
    "llm-frontends-vergleich-2026": "anthropomorphic LLM interface cat, open-webui vs text-gen-webui vs ollama comparison, chat interfaces",
    "llm-lokal-hosten-2026": "anthropomorphic local LLM bear with GPU server, ollama llama model, self-hosted AI, private inference",
    "llm-sicherheit-prompt-injection-schutz-2026": "anthropomorphic AI security fox with LLM shield, prompt injection filter, safe prompts, model guardrails",
    "mistral-modelle-lokal-hosten-2026": "anthropomorphic mistral fox with MoE architecture, quantized models, local hosting, GPU requirements chart",
    "nvidia-jetson-ki-am-edge-llm-embedded-2026": "anthropomorphic jetson penguin with edge AI, embedded GPU, robotics, LLM on device, IoT machine learning",
    "ollama-llm-server-vps-2026": "anthropomorphic ollama moose with llama model, VPS server, local LLM API, model management, terminal interface",
    "ollama-vs-vllm-vs-lm-studio-2026": "anthropomorphic LLM server comparison: ollama moose vs vllm fox vs lmstudio cat, inference performance",
    "open-webui-ollama-betreiben-2026": "anthropomorphic web UI cat with ollama backend, chat interface, model selection, RAG settings, conversation",
    "openrouter-api-vs-eigene-gpu-kostenvergleich-2026": "anthropomorphic api vs GPU cost comparison fox, openrouter pricing, self-hosted vs cloud inference cost chart",
    "openvpn-server-vps-einrichten-2026": "anthropomorphic openvpn badger with tunnel, VPN server on VPS, encryption keys, secure connection, global access",
    "palworld-server-mods-guide-2026": "anthropomorphic palworld modder cat with bepinex plugins, server ini config, admin tools, mod installation",
    "portainer-docker-management-vps-2026": "anthropomorphic portainer beaver with docker dashboard, container management, VPS server, stack deployment",
    "proxmox-heimserver-einrichten-2026": "anthropomorphic proxmox owl with virtualization, home server, VM management, hypervisor, lab setup",
    "quantisierte-modelle-gguf-awq-gptq-exl2-bitsandbytes-2026": "anthropomorphic quantization fox, GGUF AWQ GPTQ comparison, model compression, quality vs size chart, robot brain",
    "raspberry-pi-homelab-server-2026": "anthropomorphic raspberry pi cat with multiple Pi boards, homelab setup, ethernet cables, mini data center on desk",
    "redis-cache-vps-einrichten-2026": "anthropomorphic redis deer with cache server, lightning bolt speed, data caching, VPS optimization, memory storage",
    "remote-work-tirol": "anthropomorphic remote worker fox with laptop, tyrolean mountain view, home office with cow, digital nomad life",
    "runpod-serverless-vs-dedicated-gpu-2026": "anthropomorphic runpod cat, serverless vs dedicated GPU comparison, cost efficiency, scaling, AI cloud options",
    "steam-deck-vs-asus-rog-ally-vs-lenovo-legion-go-2026": "anthropomorphic handheld gamers: fox deck vs cat ally vs dog legion, three devices comparison, gaming performance",
    "tabbyapi-aphrodite-sglang-llm-server-2026": "anthropomorphic LLM server fox with tabbyapi aphrodite sglang, model hosting, inference API, GPU utilization",
    "teamspeak-server-mieten-2026": "anthropomorphic teamspeak deer with voice server, microphone, voice channels, gamer communication, VPS hosted",
    "text-generation-webui-oobabooga-einrichten-2026": "anthropomorphic oobabooga cat with Text Gen WebUI, model loading screen, GPU usage, chat interface, parameters tuning",
    "vaultwarden-passwort-manager-selbst-hosten-2026": "anthropomorphic vaultwarden badger with password vault, self-hosted bitwarden, encrypted lock, keychain",
    "vast-ai-gpu-mieten-2026": "anthropomorphic vast ai cat with GPU marketplace, rentable GPUs, cloud compute, deep learning comparison",
    "vllm-auf-eigener-gpu-aufsetzen": "anthropomorphic vllm fox with GPU server, inference engine, model deployment, API endpoint, serving setup",
    "vllm-multi-model-server-2026": "anthropomorphic vllm multi-model fox, multiple LLMs serving, GPU sharing, inference management, model routing",
    # ----- TECHNIK-VERGLEICHE -----
    "beste-gaming-monitore-2026": "anthropomorphic gamer cat with multiple monitors, 144Hz 240Hz OLED comparison, esports setup, RGB lighting",
    "gaming-pc-selbst-bauen-2026": "anthropomorphic PC builder dog with components, custom water cooling, GPU graphics card, RGB, build tools",
    # ----- SPEZIAL -----
    "contabo-vps-erfahrungen-2026": "anthropomorphic contabo customer fox, VPS experience review, german hosting, dashboard, price-performance chart",
    "docker-registry-selbst-hosten-2026": "anthropomorphic docker registry whale with storage server, container images, private registry, harbor interface",
    "jitsi-meet-server-vps-2026": "anthropomorphic jitsi deer with video conference, VPS hosted, multiple participants, screen sharing, chat bubbles",
    "plausible-analytics-vps-2026": "anthropomorphic plausible analytics owl, privacy-first analytics dashboard, visitor stats, self-hosted on VPS",
    "vps-mieten-vergleich-2026": "anthropomorphic VPS comparison racoon, server plans comparison, price-performance chart, hosting providers comparison",
}

print(f"=== MINIMAX BATCH: Alle 147 Hero-Bilder neu generieren ===")
print(f"Style: {BRAND_STYLE[:60]}...")
print(f"Artikel mit eigenen Prompts: {len(SUBJECT_PROMPTS)}")

# Get all article slugs
artikel_files = sorted([f.replace('.html', '') for f in os.listdir(os.path.join(REPO, 'artikel')) if f.endswith('.html')])
missing_prompts = [s for s in artikel_files if s not in SUBJECT_PROMPTS]

if missing_prompts:
    print(f"\n⚠️  Kein Prompt für {len(missing_prompts)} Artikel — generiere automatisch:")
    # Auto-generate from slug
    for slug in missing_prompts:
        # Clean slug to readable text
        readable = slug.replace('-', ' ').replace('.html', '')
        # Remove year numbers for cleaner prompt
        base = re.sub(r'\s20\d{2}$', '', readable)
        base = re.sub(r'^20\d{2}\s', '', base)
        SUBJECT_PROMPTS[slug] = f"anthropomorphic {base.replace(' ', ' ')} scene, technology concept artwork, server and computer elements, editorial style"
        print(f"  ✏️  {slug}")
    print(f"   → {len(missing_prompts)} auto-generierte Prompts")

print(f"\nPrompts insgesamt: {len(SUBJECT_PROMPTS)}")

def generate_image(slug):
    """Generate a single image via MiniMax API."""
    subject = SUBJECT_PROMPTS.get(slug, f"anthropomorphic {slug.replace('-', ' ')} scene")
    full_prompt = f"{subject}, {BRAND_STYLE}"
    
    payload = json.dumps({
        "model": "image-01",
        "prompt": full_prompt,
        "aspect_ratio": "16:9",
        "n": 1,  # Single image per call (rate limit safety)
    }).encode()
    
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
        base = resp.get("base_resp", {})
        code = base.get("status_code")
        if code != 0:
            print(f"  ❌ API Error {code}: {base.get('status_msg', '?')}")
            return None
        urls = resp.get("data", {}).get("image_urls", [])
        if urls:
            return urls
        print(f"  ❌ No image_urls in response: {list(resp.get('data', {}).keys())}")
        return None
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"  ❌ HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {e}")
        return None


def download_and_save(url, slug):
    """Download image from URL and save to images/ as PNG."""
    try:
        img_resp = urllib.request.urlopen(url, timeout=60)
        img_data = img_resp.read()
        img = Image.open(BytesIO(img_data))
        
        # Convert RGBA to RGB if needed
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        
        # Resize to 1216x832
        img = img.resize((1216, 832), Image.LANCZOS)
        
        # Save as PNG
        dst = os.path.join(IMG_DIR, f"{slug}.png")
        img.save(dst, "PNG", optimize=True)
        return os.path.getsize(dst)
    except Exception as e:
        print(f"  ❌ Download error: {e}")
        return None


# === MAIN BATCH ===
results = {"success": 0, "failed": 0, "skipped": 0}
log_entries = []

for i, slug in enumerate(artikel_files):
    print(f"\n[{i+1}/{len(artikel_files)}] {slug}")
    
    urls = generate_image(slug)
    if not urls:
        print(f"  ❌ No image returned")
        results["failed"] += 1
        log_entries.append(f"FAIL {slug}: no image returned")
        continue
    
    # Try first URL, if fails try second
    saved = False
    for url in urls:
        size = download_and_save(url, slug)
        if size and size > 10000:  # min 10KB
            print(f"  ✅ {size//1024}KB")
            results["success"] += 1
            log_entries.append(f"OK {slug}: {size//1024}KB")
            saved = True
            break
        elif size:
            print(f"  ⚠️  Too small ({size//1024}KB), trying next...")
    
    if not saved:
        print(f"  ❌ All URLs failed or too small")
        results["failed"] += 1
        log_entries.append(f"FAIL {slug}: all urls bad")
    
    # Rate limit safety: wait between requests
    if i < len(artikel_files) - 1:
        time.sleep(3.0)

# Summary
print(f"\n{'='*50}")
print(f"BATCH COMPLETE")
print(f"Success: {results['success']}")
print(f"Failed: {results['failed']}")
print(f"{'='*50}")

# Log
with open(LOG_FILE, 'w') as f:
    f.write(f"MiniMax Batch - {time.strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Total: {len(artikel_files)}, Success: {results['success']}, Failed: {results['failed']}\n")
    for entry in log_entries:
        f.write(f"{entry}\n")
