#!/usr/bin/env python3
"""Batch ALL hostazar Hero-Images via MiniMax image-01 (1 RPM)."""
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

# --- subject prompts (abbreviated ref to batch_brand_images.py) ---
# Load from brand script
import importlib.util
spec = importlib.util.spec_from_file_location("brand", os.path.join(REPO, "scripts", "batch_brand_images.py"))
mod = importlib.util.module_from_spec(spec)
# We only need SUBJECT_PROMPTS from the file - read it directly
exec(open(os.path.join(REPO, "scripts", "batch_brand_images.py")).read().split("# === MAIN")[0])
SUBJECT = SUBJECT_PROMPTS  # noqa

# Get all article slugs
artikel_dir = os.path.join(REPO, "artikel")
all_slugs = sorted(f.replace(".html", "") for f in os.listdir(artikel_dir) if f.endswith(".html"))

# Ensure every slug has a prompt
for slug in all_slugs:
    if slug not in SUBJECT:
        base = slug.replace("-", " ").replace(" 20", " ")
        base = re.sub(r"20\d{2}$", "", base).strip()
        SUBJECT[slug] = f"anthropomorphic {base}, technology concept, server and computer elements, editorial style"

TOTAL = len(all_slugs)
DONE = 0
FAIL = 0
RPM_WAIT = 62  # seconds between calls (1 RPM limit)

def generate(slug):
    subject = SUBJECT.get(slug, f"anthropomorphic {slug.replace('-', ' ')} scene")
    prompt = f"{subject}, {STYLE}"
    data = json.dumps({"model": "image-01", "prompt": prompt, "aspect_ratio": "16:9", "n": 1}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation",
        data=data,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
    code = resp.get("base_resp", {}).get("status_code")
    if code == 1002:
        print(f"  ⏳ RPM limit, waiting 65s...")
        time.sleep(65)
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        code = resp.get("base_resp", {}).get("status_code")
    if code != 0:
        return None, f"API error {code}: {resp.get('base_resp',{}).get('status_msg','?')}"
    urls = resp.get("data", {}).get("image_urls", [])
    return urls[0] if urls else None, "no URL"

def download(url, slug):
    img = Image.open(BytesIO(urllib.request.urlopen(url, timeout=60).read()))
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img = img.resize((1216, 832), Image.LANCZOS)
    dst = os.path.join(IMG_DIR, f"{slug}.png")
    img.save(dst, "PNG", optimize=True)
    return os.path.getsize(dst) // 1024

print(f"=== MINIMAX BATCH: {TOTAL} Bilder ===")
print(f"RPM wait: {RPM_WAIT}s | Est. time: {TOTAL * RPM_WAIT // 60} min\n")

LOG = []
for i, slug in enumerate(all_slugs, 1):
    sys.stdout.write(f"[{i}/{TOTAL}] {slug}... ")
    sys.stdout.flush()
    t0 = time.time()
    url, err = generate(slug)
    if url:
        kb = download(url, slug)
        DONE += 1
        print(f"✅ {kb}KB ({time.time()-t0:.0f}s)")
        LOG.append(f"OK {slug} {kb}KB")
    else:
        FAIL += 1
        print(f"❌ {err}")
        LOG.append(f"FAIL {slug}: {err}")
    
    if i < TOTAL:
        wait = RPM_WAIT - (time.time() - t0)
        if wait > 0:
            print(f"   waiting {wait:.0f}s...")
            time.sleep(wait)

print(f"\n=== FERTIG ===")
print(f"✅ {DONE} | ❌ {FAIL}")
with open(os.path.join(IMG_DIR, "_minimax_final_log.txt"), "w") as f:
    f.write(f"MiniMax Full Batch {time.strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"OK: {DONE} FAIL: {FAIL}\n")
    for l in LOG:
        f.write(f"{l}\n")
