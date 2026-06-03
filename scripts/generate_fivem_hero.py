#!/usr/bin/env python3
"""Generate FiveM/GTA V Roleplay hero image — neon cyberpunk gaming style."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont

OUTPUT = os.path.dirname(os.path.abspath(__file__)) + "/../images"
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

def make_fivem_hero():
    """FiveM/GTA V neon cyberpunk style with green/black color scheme."""
    canvas = Image.new('RGB', (W, H), (5, 5, 12))
    draw = ImageDraw.Draw(canvas, 'RGBA')

    # Dark base gradient (deep green/black)
    for y in range(H):
        t = y / H
        c = lerp_color((5, 10, 5), (10, 5, 20), t)
        draw.line([(0, y), (W, y)], fill=c)

    # City skyline silhouettes (abstract)
    for base_x in range(0, W, 60):
        h = random.randint(60, 200)
        w = random.randint(30, 80)
        x = base_x + random.randint(-10, 10)
        for i in range(h):
            y_pos = H - 80 - i
            alpha = int(40 * (1 - i/h))
            draw.line([(x-w//2, y_pos), (x+w//2, y_pos)], fill=(0, 255, 100, alpha))

    # Glowing neon orbs (green)
    for _ in range(40):
        x = random.randint(0, W)
        y = random.randint(100, H-100)
        r = random.randint(10, 50)
        col = (0, 255, random.randint(80, 200))
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        add_glow(gd, x, y, r*3, col)
        canvas = Image.alpha_composite(canvas.convert('RGBA'), glow)
        draw = ImageDraw.Draw(canvas, 'RGBA')
        draw.ellipse([x-r, y-r, x+r, y+r], fill=col + (180,))

    # Neon particles (floating dust)
    for _ in range(300):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 5)
        c = (0, 255, random.randint(50, 200), random.randint(30, 150))
        draw.ellipse([x, y, x+s, y+s], fill=c)

    # Horizon glow
    for i in range(100, 0, -2):
        t = i / 100
        y = H - i
        c = (0, 255, 80, int(25 * t))
        draw.line([(0, y), (W, y)], fill=c)

    # "FIVEM" big text outline glow
    try:
        # Try to use a bold font if available
        font_large = ImageFont.truetype("arial.ttf", 120)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw a glowing text effect manually
    text_str = "FiveM"
    text_str2 = "Roleplay Server Guide 2026"
    
    # Draw glow behind text
    # We approximate by drawing circles
    for _ in range(30):
        x = random.randint(300, 900)
        y = random.randint(150, 350)
        r = random.randint(5, 20)
        add_glow(draw, x, y, r*2, (0, 255, 100))

    # Horizontal scan lines
    for y in range(0, H, 3):
        alpha = random.randint(1, 6)
        draw.line([(0, y), (W, y)], fill=(0, 255, 100, alpha))

    # Grid lines (subtle)
    for x in range(0, W, 50):
        draw.line([(x, 0), (x, H)], fill=(0, 255, 100, 6))
    for y in range(0, H, 50):
        draw.line([(0, y), (W, y)], fill=(0, 255, 100, 6))

    # Vignette effect (darker edges)
    for i in range(200, 0, -5):
        t = i / 200
        alpha = int(40 * (1-t))
        # top
        draw.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))
        # bottom
        draw.line([(0, H-i), (W, H-i)], fill=(0, 0, 0, alpha))
    for i in range(200, 0, -5):
        t = i / 200
        alpha = int(40 * (1-t))
        draw.line([(i, 0), (i, H)], fill=(0, 0, 0, alpha))
        draw.line([(W-i, 0), (W-i, H)], fill=(0, 0, 0, alpha))

    return canvas.convert('RGB')

def add_atmosphere(img, blur_radius=2):
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.2)
    return img

if __name__ == "__main__":
    random.seed(42)
    print("Generating FiveM Hero Image (Neon Cyberpunk)...")
    img = make_fivem_hero()
    img = add_atmosphere(img, blur_radius=1.5)
    path = os.path.join(OUTPUT, "fivem-server-mieten-2026.png")
    img.save(path, "PNG", quality=92)
    size = os.path.getsize(path)
    print(f"  Saved: fivem-server-mieten-2026.png - {size/1024:.0f} KB")
    print("Done!")
