#!/usr/bin/env python3
"""
Hostazar image batch watcher.
Waits for remaining 10 images in queue, copies to hostazar/images/,
resizes to 1216x640, creates WebP, then git commit + push.
"""
import json, urllib.request, os, re, shutil, time
from PIL import Image

STATUS_URL = "http://127.0.0.1:8283/status/"
IMG_DIR = "C:/HermesPortable/home/scripts/blog-automation/hostazar/images"
TARGET_W, TARGET_H = 1216, 640

# Second batch: job_id -> target filename (no extension)
jobs = {
    "gen_eded30d62852": "plausible-analytics-vps-2026",
    "gen_80f470f8f68f": "portainer-docker-management-vps-2026",
    "gen_fd21e2d2e1e7": "raft-server-mieten-2026",
    "gen_957b39daac32": "server-kosten-investor-guide",
    "gen_1ed53a647b77": "gaming-pc-finanzieren",
    "gen_287199482fdf": "ghost-cms-hosting-vps-2026",
    "gen_af4cb4fbf7f1": "grafana-loki-log-aggregation-vps-2026",
    "gen_17221e4e46cc": "lemp-stack-vps-einrichten-2026",
    "gen_434c5aa50ed7": "teamspeak-server-mieten-2026",
    "gen_91ce18a2678f": "vps-mieten-vergleich-2026",
}

def get_output_path(jid):
    try:
        resp = json.loads(urllib.request.urlopen(STATUS_URL + jid, timeout=10).read())
        st = resp.get("status")
        path = None
        if st == "done" and resp.get("output_path"):
            path = resp["output_path"].replace("\\\\", "/")
        elif st == "failed":
            err = str(resp.get("error", ""))
            m = re.search(r'"output_path": "([^"]+)"', err)
            if m:
                path = m.group(1).replace("\\\\", "/")
        return st, path
    except:
        return "error", None

def resize_and_save(src, dst_png):
    img = Image.open(src)
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    w, h = img.size
    if w != TARGET_W or h != TARGET_H:
        scale = max(TARGET_W / w, TARGET_H / h)
        new_w, new_h = int(w * scale), int(h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - TARGET_W) // 2
        top = (new_h - TARGET_H) // 2
        img = img.crop((left, top, left + TARGET_W, top + TARGET_H))
    img.save(dst_png, 'PNG')
    dst_webp = dst_png.replace('.png', '.webp')
    img.save(dst_webp, 'WEBP', quality=85)
    return os.path.getsize(dst_png)

print("Hostazar image watcher: waiting for 10 images...")
completed = {}
MAX_WAIT = 7200  # 2 hours max
start = time.time()

while len(completed) < len(jobs) and (time.time() - start) < MAX_WAIT:
    for jid, name in jobs.items():
        if jid in completed:
            continue
        st, src = get_output_path(jid)
        if src and os.path.exists(src):
            dst = os.path.join(IMG_DIR, f"{name}.png")
            size = resize_and_save(src, dst)
            print(f"[OK] {name}.png -> {size:,} bytes")
            completed[jid] = True
    if len(completed) < len(jobs):
        time.sleep(15)
    else:
        break

# Also remove old placeholder PNGs that are now replaced
old_placeholders = [
    "cloudflare-waf-einrichten-2026.png", "ddos-schutz-gameserver-2026.png",
    "dedizierter-server-vs-vps-2026.png", "discord-bot-vps-hosten-2026.png",
    "hugo-astro-static-site-vergleich-2026.png", "jitsi-meet-server-vps-2026.png",
    "minecraft-bedrock-vs-java-server-2026.png", "minio-object-storage-selbst-hosten-2026.png",
    "ollama-llm-server-vps-2026.png", "palworld-server-mods-guide-2026.png",
]

print(f"\nCompleted: {len(completed)}/{len(jobs)}")
if completed:
    # Git commit
    os.chdir("C:/HermesPortable/home/scripts/blog-automation/hostazar")
    os.system('git add images/*.png images/*.webp')
    os.system('git commit -m "Fix: 20 Artikelbilder neu generiert (Pop-Art-Comic-Stil) - Platzhalter durch echte AI-Bilder ersetzt"')
    os.system('git push')
    print("Git commit + push done.")
else:
    print("No images completed. Will need manual check later.")