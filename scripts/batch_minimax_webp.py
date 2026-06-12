#!/usr/bin/env python3
"""MiniMax batch (Resume ab 59) + sofortige WEBP-Konvertierung."""
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

TOTAL = len(all_slugs)

def generate(slug):
    prompt = f"{SUBJECT.get(slug, 'anthropomorphic '+slug.replace('-',' ')+' scene')}, {STYLE}"
    data = json.dumps({"model": "image-01", "prompt": prompt, "aspect_ratio": "16:9", "n": 1}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation", data=data,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    )
    for attempt in range(3):
        resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
        code = resp.get("base_resp", {}).get("status_code")
        if code == 1002:
            if attempt < 2:
                time.sleep(65)
                continue
            return None, "RPM exhausted"
        if code != 0:
            return None, f"API error {code}"
        urls = resp.get("data", {}).get("image_urls", [])
        if urls:
            return urls[0], None
        return None, "no URLs"
    return None, "max retries"

def save_as_webp(url, slug):
    """Download PNG + save as WEBP (und PNG als Source behalten)."""
    img = Image.open(BytesIO(urllib.request.urlopen(url, timeout=60).read()))
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    img = img.resize((1216, 832), Image.LANCZOS)
    # Save PNG (source)
    png_path = os.path.join(IMG_DIR, f"{slug}.png")
    img.save(png_path, "PNG", optimize=True)
    # Save WEBP (fürs Web)
    webp_path = os.path.join(IMG_DIR, f"{slug}.webp")
    img.save(webp_path, "WEBP", quality=90, method=6)
    return os.path.getsize(png_path) // 1024, os.path.getsize(webp_path) // 1024

def convert_existing_to_webp():
    """Convert ALL existing PNG hero images to WEBP (for ones already done)."""
    count = 0
    for slug in all_slugs:
        png_path = os.path.join(IMG_DIR, f"{slug}.png")
        webp_path = os.path.join(IMG_DIR, f"{slug}.webp")
        if os.path.exists(png_path) and not os.path.exists(webp_path):
            try:
                img = Image.open(png_path)
                if img.mode == "RGBA":
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                img = img.resize((1216, 832), Image.LANCZOS)
                img.save(webp_path, "WEBP", quality=90, method=6)
                count += 1
            except:
                pass
    return count

# Step 1: Convert bereits vorhandene PNGs zu WEBP
print("=== Step 1: WEBP-Konvertierung bestehender PNGs ===")
converted = convert_existing_to_webp()
print(f"  {converted} PNGs → WEBP konvertiert\n")

# Step 2: Resume MiniMax Batch ab 58
START = 58
remaining = all_slugs[START:]
print(f"=== Step 2: MiniMax Resume ({len(remaining)} Bilder, ab {START+1}/{TOTAL}) ===")
print(f"Est. time: {len(remaining) * 62 // 60} min\n")

DONE = 0
FAIL = 0
LOG = []

for i, slug in enumerate(remaining, START + 1):
    sys.stdout.write(f"[{i}/{TOTAL}] {slug}... ")
    sys.stdout.flush()
    t0 = time.time()
    url, err = generate(slug)
    if url:
        png_kb, webp_kb = save_as_webp(url, slug)
        DONE += 1
        elapsed = time.time() - t0
        print(f"✅ PNG={png_kb}KB WEBP={webp_kb}KB ({elapsed:.0f}s)")
        LOG.append(f"OK {slug} {png_kb}KB/{webp_kb}KB")
    else:
        FAIL += 1
        print(f"❌ {err}")
        LOG.append(f"FAIL {slug}: {err}")
    if i < TOTAL:
        wait = 62 - (time.time() - t0)
        if wait > 0:
            print(f"   wait {wait:.0f}s...")
            time.sleep(wait)

print(f"\n=== FERTIG: ✅ {DONE} | ❌ {FAIL} ===")
with open(os.path.join(IMG_DIR, "_minimax_webp_log.txt"), "w") as f:
    f.write(f"MiniMax + WEBP {time.strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"OK: {DONE} FAIL: {FAIL}\n")
    for l in LOG:
        f.write(f"{l}\n")
