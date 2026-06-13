#!/usr/bin/env python3
"""Regenerate ALL SDXL hero images via MiniMax image-01 (1 RPM)."""
import json, urllib.request, time, os, re, sys
from io import BytesIO
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = os.path.join(REPO, "images")

with open("C:/sidekick/home/.env") as f:
    key = re.search(r"MINIMAX_API_KEY=(\S+)", f.read()).group(1)

STYLE = (
    "furry editorial illustration, anthropomorphic animal characters, "
    "black and white artwork with a single accent color, bold black ink outlines, "
    "high contrast monochrome shading, clean vector illustration, graphic novel aesthetics, "
    "editorial magazine artwork, dynamic composition, expressive characters, "
    "selective color highlights, professional commercial illustration, crisp linework, "
    "halftone textures"
)

exec(compile(open(os.path.join(REPO, "scripts", "batch_brand_images.py")).read().split("# === MAIN")[0], "brand", "exec"))
SUBJECT = SUBJECT_PROMPTS

artikel_dir = os.path.join(REPO, "artikel")
all_slugs = sorted(f.replace(".html", "") for f in os.listdir(artikel_dir) if f.endswith(".html"))
for slug in all_slugs:
    if slug not in SUBJECT:
        base = slug.replace("-", " ").replace(" 20", " ")
        base = re.sub(r"20\d{2}$", "", base).strip()
        SUBJECT[slug] = f"anthropomorphic {base}, technology concept, server and computer, editorial style"

# Nur SDXL-Bilder (wo PNG/WEBP nicht <5s auseinander)
SDXL = []
for slug in all_slugs:
    png = os.path.join(IMG_DIR, f"{slug}.png")
    webp = os.path.join(IMG_DIR, f"{slug}.webp")
    if os.path.exists(png) and os.path.exists(webp):
        if abs(os.path.getmtime(webp) - os.path.getmtime(png)) < 5:
            continue  # bereits MiniMax
    SDXL.append(slug)

TOTAL = len(SDXL)
print(f"=== MINIMAX REGEN: {TOTAL} SDXL-Bilder ===")
print(f"Est. time: {TOTAL * 62 // 60} min\n")

def generate(slug):
    prompt = f"{SUBJECT.get(slug, 'anthropomorphic '+slug.replace('-',' ')+' scene')}, {STYLE}"
    data = json.dumps({"model": "image-01", "prompt": prompt, "aspect_ratio": "16:9", "n": 1}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation", data=data,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    for attempt in range(5):
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        code = resp.get("base_resp", {}).get("status_code")
        if code == 1002:
            w = 65
            print(f"     ⏳ RPM limit, waiting {w}s (attempt {attempt+1})...")
            time.sleep(w)
            continue
        if code != 0:
            return None, f"API error {code}"
        urls = resp.get("data", {}).get("image_urls", [])
        if urls:
            return urls[0], None
        return None, "no URLs"
    return None, "max retries exhausted"

def save(slug, url):
    img = Image.open(BytesIO(urllib.request.urlopen(url, timeout=60).read()))
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img = img.resize((1216, 832), Image.LANCZOS)
    img.save(os.path.join(IMG_DIR, f"{slug}.png"), "PNG", optimize=True)
    img.save(os.path.join(IMG_DIR, f"{slug}.webp"), "WEBP", quality=90, method=6)
    return os.path.getsize(os.path.join(IMG_DIR, f"{slug}.png")) // 1024

DONE, FAIL, LOG = 0, 0, []
t_start = time.time()

for i, slug in enumerate(SDXL, 1):
    sys.stdout.write(f"[{i}/{TOTAL}] {slug}... ")
    sys.stdout.flush()
    t0 = time.time()
    url, err = generate(slug)
    if url:
        kb = save(slug, url)
        DONE += 1
        elapsed = time.time() - t0
        remaining = (TOTAL - i) * 62 / 60
        print(f"✅ {kb}KB ({elapsed:.0f}s, ~{remaining:.0f}min left)")
        LOG.append(f"OK {slug} {kb}KB")
    else:
        FAIL += 1
        print(f"❌ {err}")
        LOG.append(f"FAIL {slug}: {err}")

    if i < TOTAL:
        wait = 62 - (time.time() - t0)
        if wait > 0:
            time.sleep(wait)

elapsed = (time.time() - t_start) / 60
print(f"\n=== FERTIG: ✅ {DONE} | ❌ {FAIL} | {elapsed:.0f}min ===")
with open(os.path.join(IMG_DIR, "_minimax_final_log.txt"), "w") as f:
    f.write(f"MiniMax Final Batch {time.strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"OK: {DONE} FAIL: {FAIL}\n")
    for l in LOG:
        f.write(f"{l}\n")
