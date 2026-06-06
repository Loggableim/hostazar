#!/usr/bin/env python3
"""Generate hero image for Hugo vs Astro article."""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(REPO, "images")
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 630

# Webhosting palette with darkorange/wine/purple accent
palette = {
    "bg1": (28, 12, 36),   # dark purple-black
    "bg2": (60, 18, 30),   # wine/dark red
    "accent": (200, 80, 40),  # darkorange
    "accent2": (156, 39, 176),  # purple
    "accent3": (255, 120, 50),  # bright orange
}

def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def gradient_bg():
    img = Image.new("RGB", (W, H), palette["bg1"])
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=lerp(palette["bg1"], palette["bg2"], t))
    return img

def add_glows(img, count=40):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(count):
        cx = random.randint(0, W)
        cy = random.randint(0, H)
        r = random.randint(20, 120)
        color = random.choice([palette["accent"], palette["accent2"], palette["accent3"]])
        for i in range(r, 0, -6):
            t = i / r
            alpha = int(45 * t)
            d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=20))
    img.paste(layer, (0, 0), layer)

def add_grid(img):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=palette["accent2"] + (15,))
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=palette["accent2"] + (10,))
    img.paste(overlay, (0, 0), overlay)

def add_code_snippets(img):
    """Add abstract code-line decorations."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    lines = [
        (80, 120, "hugo new site blog && cd blog"),
        (100, 165, "npm create astro@latest -- --template basics"),
        (120, 210, "hugo server -D  # Live-Reload on :1313"),
        (90, 255, "astro build && astro deploy"),
        (140, 300, "git push origin main  # Auto-deploy"),
    ]
    for x, y, txt in lines:
        for i, c in enumerate(txt):
            cx = x + i * 11
            cy = y
            alpha = random.randint(20, 70)
            color = random.choice([palette["accent"], palette["accent2"], palette["accent3"]])
            d.text((cx, cy), c, fill=color + (alpha,))
    img.paste(overlay, (0, 0), overlay)

def add_vignette(img):
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    for i in range(0, 180, 4):
        vd.rectangle([i, i, W - i, H - i], outline=int(255 * (1 - i / 180)))
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=70))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(img, black, vignette)

def add_title_strip(img):
    overlay = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for y in range(220):
        a = int(180 * (y / 220))
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    img.paste(overlay, (0, H - 220), overlay)

def main():
    slug = "hugo-astro-static-site-vergleich-2026"
    random.seed(slug)
    img = gradient_bg()
    add_grid(img)
    add_glows(img)
    add_code_snippets(img)
    add_title_strip(img)
    img = add_vignette(img)
    out_path = os.path.join(OUT, f"{slug}.png")
    img.save(out_path, "PNG", optimize=True)
    print(f"OK {out_path}")

if __name__ == "__main__":
    main()
