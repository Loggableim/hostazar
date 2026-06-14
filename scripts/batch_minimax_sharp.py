#!/usr/bin/env python3
"""Regenerate ALL SDXL blurry images via MiniMax image-01 with 65s RPM wait."""
import json, urllib.request, time, os, re, sys
from io import BytesIO
from PIL import Image

with open("C:/sidekick/home/.env") as f:
    KEY = re.search(r"MINIMAX_API_KEY=(\S+)", f.read()).group(1)

STYLE = "furry editorial illustration, anthropomorphic animal characters, black and white artwork with a single accent color, bold black ink outlines, high contrast monochrome shading, clean vector illustration, graphic novel aesthetics"

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(REPO, "images")

all_slugs = sorted(f.replace(".html","") for f in os.listdir(os.path.join(REPO, "artikel")) if f.endswith(".html"))

# Alle PNGs älter als 12h = SDXL blurry
now = time.time()
sdxl = [s for s in all_slugs if os.path.exists(os.path.join(IMG_DIR, f"{s}.png")) and (now - os.path.getmtime(os.path.join(IMG_DIR, f"{s}.png"))) / 3600 > 12]

# Subject prompts laden
exec(compile(open(os.path.join(REPO, "scripts", "batch_brand_images.py")).read().split("# === MAIN")[0], "brand", "exec"))

print(f"MiniMax Sharp Batch: {len(sdxl)} SDXL-Bilder", flush=True)
DONE = 0

for i, slug in enumerate(sdxl, 1):
    subject = SUBJECT_PROMPTS.get(slug, f"anthropomorphic {slug.replace('-',' ')} scene")
    prompt = f"{subject}, {STYLE}"
    data = json.dumps({"model":"image-01","prompt":prompt,"aspect_ratio":"16:9","n":1}).encode()
    req = urllib.request.Request("https://api.minimax.io/v1/image_generation", data=data,
        headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
    
    sys.stdout.write(f"[{i}/{len(sdxl)}] {slug}... ")
    sys.stdout.flush()
    t0 = time.time()
    
    for attempt in range(5):
        try:
            resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
            code = resp.get("base_resp",{}).get("status_code")
            if code == 0:
                url = resp.get("data",{}).get("image_urls",[None])[0]
                if url:
                    img = Image.open(BytesIO(urllib.request.urlopen(url, timeout=60).read()))
                    if img.mode == "RGBA":
                        bg = Image.new("RGB", img.size, (255,255,255))
                        bg.paste(img, mask=img.split()[3])
                        img = bg
                    img = img.resize((1216, 832), Image.LANCZOS)
                    img.save(os.path.join(IMG_DIR, f"{slug}.png"), "PNG", optimize=True)
                    img.save(os.path.join(IMG_DIR, f"{slug}.webp"), "WEBP", quality=92, method=6)
                    DONE += 1
                    elapsed = time.time() - t0
                    print(f"✅ {elapsed:.0f}s", flush=True)
                    break
                print(f"❌ no URL", flush=True)
                break
            elif code == 1002:
                if attempt < 3:
                    time.sleep(65)
                else:
                    print(f"❌ RPM exhausted", flush=True)
                    break
            else:
                print(f"❌ API {code}", flush=True)
                break
        except Exception as e:
            print(f"❌ {type(e).__name__}", flush=True)
            break
    
    if i < len(sdxl):
        wait = max(1, 65 - (time.time()-t0))
        time.sleep(wait)

print(f"\n=== FERTIG: {DONE}/{len(sdxl)} ===", flush=True)
