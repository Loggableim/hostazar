#!/usr/bin/env python3
"""Generate hero image for Raft Server article."""
import os, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT = "C:/HermesPortable/home/scripts/blog-automation/hostazar/images"
os.makedirs(OUTPUT, exist_ok=True)
W, H = 1200, 630

def lerp_color(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1, c2))

def make_raft():
    canvas = Image.new('RGB', (W, H), (8, 12, 25))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    # Gradient background: dark blue/teal to deep black
    for y in range(H):
        t = y / H
        c = lerp_color((8, 20, 45), (2, 5, 15), t)
        draw.line([(0, y), (W, y)], fill=c)
    # Large glowy circles (ocean/water feel)
    for _ in range(4):
        cx = random.randint(100, W-100)
        cy = random.randint(100, H-100)
        for r in range(0, 160, 8):
            t = r / 160
            alpha = int(25 * (1-t))
            col = (0, 120 + int(80*(1-t)), 180 + int(60*(1-t)), alpha)
            draw.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=col)
    # Horizontal light beams (sun rays through water)
    for _ in range(12):
        y = random.randint(0, H)
        x1 = random.randint(0, W//3)
        x2 = random.randint(2*W//3, W)
        alpha = random.randint(8, 20)
        col = (100, 200, 255, alpha)
        draw.line([(x1, y), (x2, y)], fill=col, width=random.randint(1, 4))
    # Floating particles (bubbles/stars)
    for _ in range(200):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 4)
        alpha = random.randint(15, 70)
        col = (150, 220, 255, alpha)
        draw.ellipse([x, y, x+s, y+s], fill=col)
    # Small glowing orbs
    for _ in range(30):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.randint(3, 12)
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse([x-r, y-r, x+r, y+r], fill=(60, 180, 255, 40))
        gd.ellipse([x-2, y-2, x+2, y+2], fill=(180, 230, 255, 180))
        canvas = Image.alpha_composite(canvas.convert('RGBA'), glow)
        draw = ImageDraw.Draw(canvas, 'RGBA')
    # Lens flare / light source top-left
    cx, cy = 150, 150
    for r in range(80, 0, -4):
        t = r / 80
        alpha = int(60 * (1-t))
        col = (200, 230, 255, alpha)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col)
    # Some horizontal lines (horizon effect)
    for y in range(200, 250):
        t = (y - 200) / 50
        alpha = int(8 * (1 - abs(t-0.5)*2))
        draw.line([(0, y), (W, y)], fill=(50, 150, 255, alpha))
    return canvas.convert('RGB')

def add_atmosphere(img, blur_radius=1.5):
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Color(img).enhance(1.3)
    return img

random.seed(42)
print("Generating Raft Server hero image...")
img = make_raft()
img = add_atmosphere(img, blur_radius=1.5)
path = os.path.join(OUTPUT, "raft-server-mieten-2026.png")
img.save(path, "PNG", quality=95)
size = os.path.getsize(path)
print(f"Saved: raft-server-mieten-2026.png - {size/1024:.0f} KB")
print("Done!")
