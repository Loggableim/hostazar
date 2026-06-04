#!/usr/bin/env python3
"""Generate hero images for 3 new hostazar articles using Pillow."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT = "C:/HermesPortable/home/spaces/hostazar/images"
os.makedirs(OUTPUT, exist_ok=True)
W, H = 1200, 630

def lerp_color(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1, c2))

def add_glow(draw, cx, cy, r, color):
    for i in range(r, 0, -3):
        t = i / r
        alpha = int(120 * (1-t))
        c = tuple(int(cc * t + 255 * (1-t)) for cc in color)
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c + (alpha,))

def make_contabo():
    canvas = Image.new('RGB', (W, H), (10, 10, 35))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    for y in range(H):
        t = y / H
        c = lerp_color((15, 15, 50), (30, 20, 60), t)
        draw.line([(0, y), (W, y)], fill=c)
    for _ in range(15):
        cx = random.randint(0, W)
        cy = random.randint(100, 400)
        for r in range(0, 120, 5):
            t = r / 120
            col = (50 + int(100*(1-t)), 100 + int(100*(1-t)), 255, int(30*(1-t)))
            draw.ellipse([cx-r, cy-r//2, cx+r, cy+r//2], fill=col)
    for _ in range(20):
        x = random.randint(0, W)
        for y in range(H):
            t = y / H
            w = int(60 * (1-t))
            if w > 0:
                c = (100, 150, 255, int(15 * (1-t)))
                draw.line([(x-w, y), (x+w, y)], fill=c)
    for _ in range(150):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 3)
        c = (100, 180, 255, random.randint(20, 80))
        draw.ellipse([x, y, x+s, y+s], fill=c)
    return canvas.convert('RGB')

def make_jenkins():
    canvas = Image.new('RGB', (W, H), (12, 8, 10))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    for y in range(H):
        t = y / H
        c = lerp_color((20, 10, 15), (40, 15, 20), t)
        draw.line([(0, y), (W, y)], fill=c)
    for _ in range(12):
        points = []
        x = random.randint(0, W)
        y = random.randint(0, H)
        points.append((x, y))
        for _ in range(random.randint(3, 6)):
            x += random.randint(-100, 100)
            y += random.randint(-60, 60)
            points.append((x, y))
        for i in range(len(points)-1):
            col = (255, 100 + random.randint(0, 100), 50, random.randint(10, 30))
            draw.line([points[i], points[i+1]], fill=col, width=random.randint(2, 8))
    for _ in range(6):
        cx = random.randint(100, W-100)
        cy = random.randint(100, H-100)
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        add_glow(gd, cx, cy, 50, (255, 150, 50))
        canvas = Image.alpha_composite(canvas.convert('RGBA'), glow)
        draw = ImageDraw.Draw(canvas, 'RGBA')
        draw.ellipse([cx-15, cy-15, cx+15, cy+15], fill=(255, 180, 50, 200))
    for _ in range(100):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 4)
        c = (255, 150, 50, random.randint(20, 80))
        draw.ellipse([x, y, x+s, y+s], fill=c)
    return canvas.convert('RGB')

def make_gitea():
    canvas = Image.new('RGB', (W, H), (8, 12, 10))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    for y in range(H):
        t = y / H
        c = lerp_color((10, 20, 15), (15, 40, 20), t)
        draw.line([(0, y), (W, y)], fill=c)
    for _ in range(5):
        start_x = random.randint(50, 200)
        start_y = random.randint(50, H-50)
        points = [(start_x, start_y)]
        cx, cy = start_x, start_y
        for _ in range(random.randint(4, 8)):
            cx += random.randint(50, 150)
            cy += random.randint(-80, 80)
            cy = max(30, min(H-30, cy))
            points.append((cx, cy))
        for i in range(len(points)-1):
            col = (50, 255, 100, random.randint(20, 50))
            draw.line([points[i], points[i+1]], fill=col, width=3)
            draw.ellipse([points[i][0]-8, points[i][1]-8, points[i][0]+8, points[i][1]+8],
                        fill=(80, 255, 120, 150))
    for _ in range(20):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.randint(10, 40)
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        add_glow(gd, x, y, r*2, (50, 255, 100))
        canvas = Image.alpha_composite(canvas.convert('RGBA'), glow)
    draw = ImageDraw.Draw(canvas, 'RGBA')
    for _ in range(120):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 3)
        c = (100, 255, 150, random.randint(20, 80))
        draw.ellipse([x, y, x+s, y+s], fill=c)
    return canvas.convert('RGB')

def add_atmosphere(img, blur_radius=2):
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.2)
    return img

random.seed(42)
images = [
    ("contabo-vps-erfahrungen-2026", make_contabo, "Contabo VPS"),
    ("jenkins-ci-cd-pipeline-vps-2026", make_jenkins, "Jenkins CI/CD"),
    ("gitea-git-server-vps-2026", make_gitea, "Gitea Git"),
]
for name, maker, label in images:
    print(f"Generating {label}...")
    img = maker()
    img = add_atmosphere(img, blur_radius=2)
    path = os.path.join(OUTPUT, f"{name}.png")
    img.save(path, "PNG", quality=92)
    size = os.path.getsize(path)
    print(f"  Saved: {name}.png - {size/1024:.0f} KB")
print("\n3 Hero-Bilder erstellt!")
