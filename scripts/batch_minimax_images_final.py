#!/usr/bin/env python3
"""Regenerate ALL 154 hero images via MiniMax image-01 API."""
import json, urllib.request, time, os, re, sys
from io import BytesIO
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(REPO, "images")
KEY = re.search(r"MINIMAX_API_KEY=(\S+)", open("C:/sidekick/home/.env").read()).group(1)

STYLE = (
    "furry editorial illustration, anthropomorphic animal characters, "
    "black and white artwork with a single accent color, bold black ink outlines, "
    "high contrast monochrome shading, clean vector illustration, graphic novel aesthetics, "
    "editorial magazine artwork, dynamic composition, expressive characters, "
    "selective color highlights, professional commercial illustration, crisp linework, "
    "halftone textures"
)

# Load subjects from brand script
exec(compile(open(os.path.join(REPO, "scripts", "batch_brand_images.py")).read().split("# === MAIN")[0], "brand", "exec"))
SUBJECT = SUBJECT_PROMPTS

artikel_dir = os.path.join(REPO, "artikel")
all_slugs = sorted(f.replace(".html", "") for f in os.listdir(artikel_dir) if f.endswith(".html"))
for slug in all_slugs:
    if slug not in SUBJECT:
        base = slug.replace("-", " ").replace(" 20", " ")
        base = re.sub(r"20\d{2}$", "", base).strip()
        SUBJECT[slug] = f"anthropomorphic {base}, technology concept, editorial style"

TOTAL = len(all_slugs)
print(f"=== MINIMAX BATCH: {TOTAL} Bilder ===", flush=True)
print(f"Est. ~{TOTAL * 17 // 60} min", flush=True)

DONE = 0
FAIL = 0

for i, slug in enumerate(all_slugs, 1):
    subject = SUBJECT.get(slug, f"anthropomorphic {slug.replace('-',' ')} scene")
    prompt = f"{subject}, {STYLE}"
    
    data = json.dumps({"model": "image-01", "prompt": prompt, "aspect_ratio": "16:9", "n": 1}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation",
        data=data,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    )
    
    sys.stdout.write(f"[{i}/{TOTAL}] {slug}... ")
    sys.stdout.flush()
    t0 = time.time()
    
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
        code = resp.get("base_resp", {}).get("status_code")
        if code != 0:
            print(f"❌ Code {code} ({time.time()-t0:.0f}s)", flush=True)
            FAIL += 1
            time.sleep(5)
            continue
        
        url = resp.get("data", {}).get("image_urls", [None])[0]
        if not url:
            print(f"❌ no URL ({time.time()-t0:.0f}s)", flush=True)
            FAIL += 1
            continue
        
        img = Image.open(BytesIO(urllib.request.urlopen(url, timeout=60).read()))
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        
        png_path = os.path.join(IMG_DIR, f"{slug}.png")
        webp_path = os.path.join(IMG_DIR, f"{slug}.webp")
        
        img.save(png_path, "PNG", optimize=True)
        img.save(webp_path, "WEBP", quality=98, method=4)
        
        png_kb = os.path.getsize(png_path) // 1024
        elapsed = time.time() - t0
        print(f"✅ {png_kb}KB ({elapsed:.0f}s)", flush=True)
        DONE += 1
    except Exception as e:
        print(f"❌ {e} ({time.time()-t0:.0f}s)", flush=True)
        FAIL += 1
    
    # Rate limit: image-01 seems faster than text, ~3s per image
    time.sleep(3)

print(f"\n=== FERTIG: ✅ {DONE} | ❌ {FAIL} ===", flush=True)
