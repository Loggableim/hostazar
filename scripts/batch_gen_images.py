#!/usr/bin/env python3
"""Generate missing hero images for hostazar via local gen queue (port 8283)."""
import json, urllib.request, time, os, sys, re
from PIL import Image

QUEUE = "http://127.0.0.1:8283"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = os.path.join(REPO, "images")
LOG_FILE = os.path.join(IMG_DIR, "_gen_batch_log.txt")

os.makedirs(IMG_DIR, exist_ok=True)

# Article prompts for the 22 missing/small images
PROMPTS = {
    "nginx-vs-apache-webserver-vergleich-2026": "Nginx vs Apache web server comparison, two server logos facing each other, configuration files, speed graph comparison, data center background",
    "postgresql-vs-mysql-vergleich-2026": "PostgreSQL vs MySQL database comparison, elephant vs dolphin logo, database cylinders, SQL query, performance benchmark chart",
    "raspberry-pi-homelab-server-2026": "Raspberry Pi homelab server setup, multiple Pi boards stacked, LED blinking, ethernet cables, mini data center on desk",
    "remote-work-tirol": "Remote work in Tirol Austria, laptop with mountain view, Alps landscape, home office setup, cow and laptop, digital nomad",
    "text-generation-webui-oobabooga-einrichten-2026": "Oobabooga Text Generation WebUI, LLM chat interface, model loading screen, GPU usage graph, terminal with Python",
    "phasmophobia-server-hosten-2026": "Phasmophobia ghost hunting server, ghost detector EMF reader, UV light, abandoned asylum corridor, spirit box equipment",
    "gaming-pc-selbst-bauen-2026": "Gaming PC build guide 2026, custom water cooling, RGB components, GPU graphics card, motherboard with CPU, PC building tools",
    "cloud-vs-dedicated-server-2026": "Cloud vs dedicated server comparison, cloud nodes vs physical server rack, scalability arrows, cost comparison graph",
    "steam-deck-vs-asus-rog-ally-vs-lenovo-legion-go-2026": "Steam Deck vs ASUS ROG Ally vs Lenovo Legion Go comparison, three handheld gaming devices side by side, gaming performance",
    "baldurs-gate-3-server-mieten-2026": "Baldur's Gate 3 server hosting, D&D dice, fantasy castle, mind flayer silhouette, campfire with party, RPG adventure",
    "hostinger-review-2026": "Hostinger web hosting review 2026, hPanel dashboard, hosting plans comparison, speed test results, website builder interface",
    "istio-service-mesh-2026": "Istio service mesh on Kubernetes, service graph, envoy sidecar proxies, traffic routing arrows, security shield, cloud native",
    "lethal-company-server-mieten-2026": "Lethal Company co-op server, abandoned industrial moon, scrap metal, monster silhouettes, spaceship interior, horror sci-fi",
    "beste-gaming-monitore-2026": "Best gaming monitors 2026 comparison, 144Hz 240Hz OLED displays side by side, esports setup, RGB lighting, screen specs",
    "deep-rock-galactic-server-mieten-2026": "Deep Rock Galactic server hosting, dwarf miner with pickaxe, glowing crystals, space rig, dark cave tunnels, co-op mining",
    "escape-from-tarkov-server-hosten-2026": "Escape from Tarkov server hosting, tactical military gear, Tarkov city ruins, weapon modding, loot stash, armored vest",
    "webhosting-sicherheit-ddos-schutz-waf-2026": "Web hosting security DDoS protection WAF, firewall shield, attack graph blocked, secure server rack, padlock on globe",
    "helldivers-2-server-hosten-2026": "Helldivers 2 server hosting, super destroyer spaceship, orbital strike, bug alien swarm, helldiver trooper, galactic war map",
    "quantisierte-modelle-gguf-awq-gptq-exl2-bitsandbytes-2026": "Quantized LLM models comparison GGUF AWQ GPTQ ExLlama, compression graph, model size vs quality tradeoff, robot brain",
    "managed-wordpress-hosting-vergleich-2026": "Managed WordPress hosting comparison 2026, WP logo, speed rocket, dashboard interfaces, caching plugins, CDN globe",
    "pubg-server-mieten-2026": "PUBG Battle Royale server hosting, parachute over island, weapon crate, military gear, battleground map, chicken dinner trophy",
    "phasmophobia-server-mieten-2026": "Phasmophobia ghost hunting server hosting, paranormal investigation equipment, ghost silhouette, EMF reader, asylum hallway, UV light",
}

STYLE = "clean digital illustration, flat design, bold colors, game art style, modern vector graphics, dramatic lighting, high contrast, epic composition"
NEG = "photorealistic, sketch, charcoal, black and white, monochrome, pencil drawing, watercolor, signature, text, watermark, blurry, low quality, ugly, deformed"


def submit(slug):
    prompt = PROMPTS[slug]
    full_prompt = f"{prompt}, {STYLE}"
    data = json.dumps({
        "model": "sdxl-lightning",
        "prompt": full_prompt,
        "negative": NEG,
        "steps": 8,
        "cfg": 2.0,
        "width": 1216,
        "height": 832,
        "seed": -1,
    }).encode()
    req = urllib.request.Request(f"{QUEUE}/generate", data=data,
        headers={"Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        jid = resp.get("job_id")
        print(f"  Submitted {slug} -> job {jid}")
        return jid
    except Exception as e:
        print(f"  FAILED submit {slug}: {e}")
        return None


def wait_for(job_id, slug, timeout=300):
    for i in range(timeout // 3):
        time.sleep(3)
        try:
            resp = json.loads(
                urllib.request.urlopen(f"{QUEUE}/status/{job_id}", timeout=10).read())
            st = resp.get("status")
            if st == "done" and resp.get("output_path"):
                src = resp["output_path"]
                if os.path.exists(src):
                    dst = os.path.join(IMG_DIR, f"{slug}.png")
                    process_image(src, dst)
                    print(f"  DONE {slug} -> {dst} ({os.path.getsize(dst)//1024}KB)")
                    return True
            elif st == "failed":
                print(f"  FAILED {slug}: {resp.get('error', 'unknown')}")
                return False
        except Exception as e:
            pass
    print(f"  TIMEOUT {slug}")
    return False


def process_image(src, dst):
    img = Image.open(src)
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img = img.resize((1216, 832), Image.LANCZOS)
    img.save(dst, "PNG", optimize=True)
    # Also update OG image in article if needed
    return dst


print("=== HOSTAZAR BATCH IMAGE GENERATION ===")
print(f"Queue: {QUEUE}")
print(f"Images dir: {IMG_DIR}")
print()

# Check queue health
try:
    h = json.loads(urllib.request.urlopen(f"{QUEUE}/health", timeout=10).read())
    print(f"Queue: pending={h['pending']} vram={h['vram_mb']}MB")
except Exception as e:
    print(f"Queue offline: {e}")
    sys.exit(1)

# Process only the 22 missing/small images
slugs = sorted(PROMPTS.keys())
print(f"Zu generieren: {len(slugs)} Bilder\n")

# Submit all jobs
jobs = []
for slug in slugs:
    jid = submit(slug)
    if jid:
        jobs.append((slug, jid))
    time.sleep(0.5)

print(f"\n{len(jobs)} Jobs submitted. Warte auf Ergebnisse...\n")

# Wait for all
success = []
failed = []
for slug, jid in jobs:
    if wait_for(jid, slug):
        success.append(slug)
    else:
        failed.append(slug)

print(f"\n=== ERGEBNIS ===")
print(f"Erfolgreich: {len(success)}")
print(f"Fehlgeschlagen: {len(failed)}")
if failed:
    print(f"Fehler: {', '.join(failed)}")

# Log
with open(LOG_FILE, "w") as f:
    f.write(f"Batch gen {time.strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Success: {len(success)}, Failed: {len(failed)}\n")
    f.write(f"Success: {', '.join(success)}\n")
    if failed:
        f.write(f"Failed: {', '.join(failed)}\n")
