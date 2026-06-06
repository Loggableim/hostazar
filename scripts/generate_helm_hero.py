#!/usr/bin/env python3
"""Generate hero image for Helm Charts article using Pillow."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT = "C:/HermesPortable/home/scripts/blog-automation/hostazar/images"
os.makedirs(OUTPUT, exist_ok=True)
W, H = 1200, 630

def lerp_color(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1, c2))

def add_glow(draw, cx, cy, r, color):
    for i in range(r, 0, -3):
        t = i / r
        alpha = int(100 * (1-t))
        c = tuple(int(cc * t + 255 * (1-t)) for cc in color)
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c + (alpha,))

def make_helm():
    canvas = Image.new('RGB', (W, H), (8, 12, 30))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    # Dark gradient background
    for y in range(H):
        t = y / H
        c = lerp_color((10, 15, 45), (20, 40, 70), t)
        draw.line([(0, y), (W, y)], fill=c)

    # Abstract circles / nodes (like a Helm chart)
    nodes = []
    for _ in range(8):
        cx = random.randint(100, W-100)
        cy = random.randint(80, H-80)
        nodes.append((cx, cy))
        for r in range(0, 100, 5):
            t = r / 100
            col = (30 + int(150*(1-t)), 180 + int(60*(1-t)), 255, int(25*(1-t)))
            draw.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=col)

    # Git-like branching lines (representing Helm releases/versions)
    branches = [
        (100, 100, 400, 150),
        (120, 200, 450, 300),
        (150, 350, 500, 450),
        (180, 450, 480, 520),
        (600, 120, 900, 180),
        (650, 250, 950, 350),
        (700, 400, 1000, 480),
        (550, 500, 850, 580),
    ]
    for sx, sy, ex, ey in branches:
        # Branch line
        col = (0, 200, 255, random.randint(30, 60))
        draw.line([(sx, sy), (ex, ey)], fill=col, width=3)
        # Branch nodes
        mx, my = (sx+ex)//2, (sy+ey)//2
        draw.ellipse([mx-6, my-6, mx+6, my+6], fill=(0, 220, 255, 180))
        draw.ellipse([sx-4, sy-4, sx+4, sy+4], fill=(100, 200, 255, 150))
        draw.ellipse([ex-4, ey-4, ex+4, ey+4], fill=(100, 200, 255, 150))

    # Container/Helm icons (abstract boxes)
    for _ in range(6):
        x = random.randint(50, W-50)
        y = random.randint(50, H-50)
        size = random.randint(20, 50)
        col = (0, 200, 255, random.randint(30, 60))
        draw.rectangle([x-size, y-size//2, x+size, y+size//2], outline=col, width=2)
        # inner detail
        col2 = (100, 220, 255, random.randint(20, 40))
        draw.rectangle([x-size//2, y-size//4, x+size//2, y+size//4], outline=col2, width=1)

    # Glowing nodes
    for _ in range(5):
        cx = random.randint(100, W-100)
        cy = random.randint(100, H-100)
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        add_glow(gd, cx, cy, 40, (0, 180, 255))
        canvas = Image.alpha_composite(canvas.convert('RGBA'), glow)
        draw = ImageDraw.Draw(canvas, 'RGBA')
        draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=(0, 200, 255, 200))

    # Tiny stars / particles
    for _ in range(200):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 3)
        c = (150, 220, 255, random.randint(20, 80))
        draw.ellipse([x, y, x+s, y+s], fill=c)

    return canvas.convert('RGB')

def add_atmosphere(img, blur_radius=2):
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.2)
    return img

random.seed(42)
name = "helm-charts-kubernetes-guide-2026"
print(f"Generating Helm Charts hero image...")
img = make_helm()
img = add_atmosphere(img, blur_radius=2)
path = os.path.join(OUTPUT, f"{name}.png")
img.save(path, "PNG", quality=92)
size = os.path.getsize(path)
print(f"  Saved: {name}.png - {size/1024:.0f} KB")
print("Hero-Bild erstellt!")
