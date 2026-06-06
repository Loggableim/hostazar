#!/usr/bin/env python3
"""Generate Docker Registry hero image for hostazar.com using DevOps/Cybernetic style."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT = os.path.dirname(os.path.abspath(__file__)) + "/../images"
os.makedirs(OUTPUT, exist_ok=True)
W, H = 1200, 630

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp_color(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1, c2))

def add_glow(draw, cx, cy, r, color):
    for i in range(r, 0, -3):
        t = i / r
        alpha = int(120 * (1-t))
        c = tuple(int(cc * t + 255 * (1-t)) for cc in color)
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c + (alpha,))

def make_docker_registry_hero():
    """Style: Cybernetic/Techno with Docker-Container Registry theme."""
    canvas = Image.new('RGB', (W, H), (12, 8, 10))
    draw = ImageDraw.Draw(canvas, 'RGBA')

    # Base gradient — dark red-orange (devops style)
    for y in range(H):
        t = y / H
        c = lerp_color((20, 10, 15), (40, 15, 20), t)
        draw.line([(0, y), (W, y)], fill=c)

    # Hex grid (DevOps signature)
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

    # Docker container stack pillars — vertical glowing columns like stacked containers
    pillars = [(180, 250, 45), (420, 220, 40), (660, 260, 50), (900, 230, 42), (1080, 270, 38)]
    for px, py, width in pillars:
        # Pillar glow
        for w in range(width, 0, -4):
            t = w / width
            a = int(25 * (1-t))
            draw.rectangle([px-w, py-100, px+w, py+100], fill=(255, 130, 50, a))
        # Container-like rectangles (stacked)
        for stack_y in range(py-90, py+80, 30):
            draw.rectangle([px-width//2, stack_y-2, px+width//2, stack_y+10],
                           fill=(255, 160, 60, random.randint(40, 80)))
            draw.rectangle([px-width//2+2, stack_y-2, px+width//2-2, stack_y+10],
                           fill=(200, 100, 30, random.randint(20, 40)))

    # Glowing data cables (horizontal connections between pillars)
    cable_colors = [(255, 140, 50), (255, 100, 40), (200, 120, 60)]
    for i in range(len(pillars)-1):
        x1, y1, _ = pillars[i]
        x2, y2, _ = pillars[i+1]
        cx1, cx2 = x1 + 60, x2 - 60
        for _ in range(2):
            col = random.choice(cable_colors)
            # Bezier-style multi-segment line
            points = [(x1, y1-40), ((x1+x2)//2, y1-80), ((x1+x2)//2, y2-80), (x2, y2-40)]
            for j in range(len(points)-1):
                draw.line([points[j], points[j+1]], fill=col + (random.randint(15, 35),), width=random.randint(2, 5))

    # Terminal particles (glowing dots)
    for _ in range(150):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 4)
        c = (255, 150, 50, random.randint(20, 80))
        draw.ellipse([x, y, x+s, y+s], fill=c)

    # Bottom horizon glow
    for i in range(50, 0, -2):
        t = i / 50
        y = H - i
        c = (255, 100, 50, int(25 * t))
        draw.line([(0, y), (W, y)], fill=c)

    # Central Docker Registry logo glow (circular)
    cx, cy = W//2, H//2
    for r in range(220, 0, -8):
        t = r / 220
        a = int(18 * (1-t))
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(255, 140, 50, a))

    # Inner container registry icon (simplified)
    box_size = 80
    draw.rectangle([cx-box_size, cy-box_size//2, cx+box_size, cy+box_size//2],
                   fill=(255, 180, 70, 100))
    draw.rectangle([cx-box_size+8, cy-box_size//2-8, cx+box_size-8, cy-box_size//2+8],
                   fill=(200, 100, 30, 80))
    draw.rectangle([cx-box_size+8, cy+box_size//2-8, cx+box_size-8, cy+box_size//2+8],
                   fill=(200, 100, 30, 80))
    # Registry text lines
    for i, ty in enumerate([cy-box_size//2-25, cy-box_size//2-15, cy+box_size//2+15, cy+box_size//2+25]):
        draw.text((cx-30, ty), "REG" if i < 2 else "IST", fill=(255, 200, 100, 60))

    return canvas.convert('RGB')

def add_atmosphere(img, blur_radius=2):
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Color(img).enhance(1.2)
    return img

if __name__ == "__main__":
    random.seed(42)
    random.seed(42)
    print("Generating Docker Registry Hero (Cybernetic Techno — DevOps)...")
    img = make_docker_registry_hero()
    img = add_atmosphere(img, blur_radius=2)
    path = os.path.join(OUTPUT, "docker-registry-selbst-hosten-2026.png")
    img.save(path, "PNG", quality=92)
    size = os.path.getsize(path)
    print(f"  Saved: docker-registry-selbst-hosten-2026.png - {size/1024:.0f} KB")
    print("Done!")
