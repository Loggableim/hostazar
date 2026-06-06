#!/usr/bin/env python3
"""Generate hero image (1200x630) for a single hostazar blog article.

Uses Pillow to produce a dark-theme gradient with neon accent, matching
the existing article-hero style (see scripts/generate_hero_ai_style.py).

Usage:
    python generate_blog_image.py <slug> "<topic>"

Output: images/<slug>.png
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__)))
OUT = os.path.join(REPO, "images")
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 630

# Per-category palettes (dark-theme neon)
PALETTES = {
    "gaming":     {"bg1": (12, 8, 32),  "bg2": (40, 10, 60),  "accent": (76, 175, 80),  "accent2": (0, 255, 180)},
    "webhosting": {"bg1": (8, 12, 32),  "bg2": (20, 30, 80),  "accent": (33, 150, 243), "accent2": (100, 200, 255)},
    "devops":     {"bg1": (24, 12, 4),  "bg2": (60, 28, 10),  "accent": (255, 152, 0),  "accent2": (255, 200, 80)},
    "default":    {"bg1": (10, 10, 24), "bg2": (30, 20, 50),  "accent": (156, 39, 176), "accent2": (200, 100, 255)},
}


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def gradient_bg(cat):
    p = PALETTES.get(cat, PALETTES["default"])
    img = Image.new("RGB", (W, H), p["bg1"])
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=lerp(p["bg1"], p["bg2"], t))
    return img, p


def add_glows(img, p, count=35):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(count):
        cx = random.randint(0, W)
        cy = random.randint(0, H)
        r = random.randint(20, 110)
        color = random.choice([p["accent"], p["accent2"]])
        for i in range(r, 0, -6):
            t = i / r
            alpha = int(40 * t)
            d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=18))
    img.paste(layer, (0, 0), layer)


def add_grid(img, p):
    """Subtle dark grid lines for the 'server / hosting' tech look."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=p["accent"] + (18,))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=p["accent"] + (12,))
    img.paste(overlay, (0, 0), overlay)


def add_title_strip(img, p, title):
    """Add a small dark gradient at the bottom for the title strip."""
    overlay = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(200):
        a = int(180 * (y / 200))
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img.paste(overlay, (0, H - 200), overlay)


def main():
    if len(sys.argv) < 3:
        print("usage: generate_blog_image.py <slug> <category> [topic]")
        sys.exit(1)
    slug = sys.argv[1]
    cat = sys.argv[2]
    topic = sys.argv[3] if len(sys.argv) > 3 else slug
    random.seed(slug)  # deterministic per article
    img, p = gradient_bg(cat)
    add_grid(img, p)
    add_glows(img, p)
    add_title_strip(img, p, topic)
    # slight vignette
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    for i in range(0, 200, 4):
        vd.rectangle([i, i, W - i, H - i], outline=int(255 * (1 - i / 200)))
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=80))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(img, black, vignette)
    out_path = os.path.join(OUT, f"{slug}.png")
    img.save(out_path, "PNG", optimize=True)
    print(f"OK {out_path}")


if __name__ == "__main__":
    main()
