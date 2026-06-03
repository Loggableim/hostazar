#!/usr/bin/env python3
"""Generate 3 AI-art-style hero images for hostazar.com using Pillow artistic effects."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

OUTPUT = os.path.dirname(os.path.abspath(__file__)) + "/../images"
os.makedirs(OUTPUT, exist_ok=True)
W, H = 1200, 630

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp_color(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1, c2))

def noise_layer(w, h, scale=10):
    """Create Perlin-esque organic noise."""
    img = Image.new('RGB', (w//scale, h//scale))
    draw = ImageDraw.Draw(img)
    for x in range(0, w//scale):
        for y in range(0, h//scale):
            v = random.randint(0, 255)
            draw.point((x, y), fill=(v, v, v))
    return img.resize((w, h), Image.Resampling.LANCZOS)

def add_glow(draw, cx, cy, r, color):
    """Soft radial glow."""
    for i in range(r, 0, -3):
        t = i / r
        alpha = int(120 * (1-t))
        c = tuple(int(cc * t + 255 * (1-t)) for cc in color)
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c + (alpha,))

def make_style_gaming():
    """Style: Synthetic/Digital Art — neon cyberpunk jungle with glowing Pal-like creatures."""
    canvas = Image.new('RGB', (W, H), (8, 8, 24))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    
    # Base gradient
    for y in range(H):
        t = y / H
        c = lerp_color((8, 8, 40), (20, 8, 50), t)
        draw.line([(0, y), (W, y)], fill=c)
    
    # Glowing neon orbs (organic shapes)
    for _ in range(60):
        x = random.randint(0, W)
        y = random.randint(100, H-100)
        r = random.randint(8, 40)
        colors = [(0,255,100), (100,255,200), (180,0,255), (255,100,200)]
        col = random.choice(colors)
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        add_glow(gd, x, y, r*3, col)
        canvas = Image.alpha_composite(canvas.convert('RGBA'), glow)
        draw = ImageDraw.Draw(canvas, 'RGBA')
        draw.ellipse([x-r, y-r, x+r, y+r], fill=col + (200,))
    
    # Floating particles
    for _ in range(200):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 4)
        c = (100, 255, 150, random.randint(30, 120))
        draw.ellipse([x, y, x+s, y+s], fill=c)
    
    # Ground horizon glow
    for i in range(80, 0, -2):
        t = i / 80
        y = H - i
        c = (30, 200, 100, int(30 * t))
        draw.line([(0, y), (W, y)], fill=c)
    
    # Procedural "creature" silhouettes
    for cx, cy in [(200, 300), (500, 250), (800, 280)]:
        # Body
        for r_scale in range(15, 45, 3):
            r = r_scale + 10 * math.sin(r_scale * 0.3 + cx)
            alpha = max(10, 60 - r_scale)
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(0, 255, 100, alpha))
    
    # Grid lines overlay
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(0, 255, 100, 8))
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(0, 255, 100, 8))
    
    return canvas.convert('RGB')

def make_style_webhosting():
    """Style: Ethereal Cloudscape — soft glowing clouds over data ocean."""
    canvas = Image.new('RGB', (W, H), (10, 10, 35))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    
    # Deep gradient
    for y in range(H):
        t = y / H
        c = lerp_color((15, 15, 50), (30, 20, 60), t)
        draw.line([(0, y), (W, y)], fill=c)
    
    # Glowing cloud clusters
    for _ in range(15):
        cx = random.randint(0, W)
        cy = random.randint(100, 400)
        for r in range(0, 120, 5):
            t = r / 120
            col = (50 + int(100*(1-t)), 100 + int(100*(1-t)), 255, int(30*(1-t)))
            draw.ellipse([cx-r, cy-r/2, cx+r, cy+r/2], fill=col)
    
    # Light rays
    for _ in range(20):
        x = random.randint(0, W)
        for y in range(H):
            t = y / H
            w = int(60 * (1-t))
            if w > 0:
                c = (100, 150, 255, int(15 * (1-t)))
                draw.line([(x-w, y), (x+w, y)], fill=c)
    
    # Data stream particles
    for _ in range(150):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 3)
        c = (100, 180, 255, random.randint(20, 80))
        draw.ellipse([x, y, x+s, y+s], fill=c)
    
    # Horizon glow
    for i in range(60, 0, -2):
        t = i / 60
        y = H - i
        c = (50, 100, 255, int(40 * t))
        draw.line([(0, y), (W, y)], fill=c)
    
    return canvas.convert('RGB')

def make_style_devops():
    """Style: Cybernetic/Techno — data cables, hex grids, glowing terminal."""
    canvas = Image.new('RGB', (W, H), (12, 8, 10))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    
    # Base gradient
    for y in range(H):
        t = y / H
        c = lerp_color((20, 10, 15), (40, 15, 20), t)
        draw.line([(0, y), (W, y)], fill=c)
    
    # Hex grid
    for row in range(0, H+30, 40):
        for col in range(0, W+30, 60):
            x = col + (0 if row % 80 == 0 else 30)
            y = row
            alpha = random.randint(5, 15)
            for i in range(6):
                angle = math.radians(60 * i - 30)
                ax = x + 25 * math.cos(angle)
                ay = y + 25 * math.sin(angle)
                bx = x + 25 * math.cos(angle + math.radians(60))
                by = y + 25 * math.sin(angle + math.radians(60))
                draw.line([(ax, ay), (bx, by)], fill=(255, 120, 50, alpha))
    
    # Glowing data cables
    for _ in range(8):
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
    
    # Terminal glow dots
    for _ in range(100):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 4)
        c = (255, 150, 50, random.randint(20, 80))
        draw.ellipse([x, y, x+s, y+s], fill=c)
    
    # Bottom glow
    for i in range(50, 0, -2):
        t = i / 50
        y = H - i
        c = (255, 100, 50, int(25 * t))
        draw.line([(0, y), (W, y)], fill=c)
    
    return canvas.convert('RGB')

# Add artistic blur/atmosphere
def add_atmosphere(img, blur_radius=3):
    """Apply subtle blur and color grading for painterly effect."""
    # Soft blur
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    # Enhance contrast
    from PIL import ImageEnhance
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.2)
    return img

if __name__ == "__main__":
    random.seed(42)
    styles = [
        ("hero-ai-gaming", make_style_gaming, "Neon Cyberpunk — Gaming"),
        ("hero-ai-webhosting", make_style_webhosting, "Ethereal Cloudscape — Webhosting"),
        ("hero-ai-devops", make_style_devops, "Cybernetic Techno — DevOps"),
    ]
    
    for name, maker, label in styles:
        print(f"Generating {label}...")
        img = maker()
        img = add_atmosphere(img, blur_radius=2)
        path = os.path.join(OUTPUT, f"{name}.png")
        img.save(path, "PNG", quality=92)
        size = os.path.getsize(path)
        print(f"  Saved: {name}.png - {size/1024:.0f} KB")

    print("\n3 AI-Style Hero-Bilder erstellt!")
