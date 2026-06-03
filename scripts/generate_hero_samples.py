#!/usr/bin/env python3
"""Generate 3 sample hero images for hostazar.com in Pop-Tech style."""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630

CAT_COLORS = {
    "gaming": ("#4CAF50", "#81C784"),
    "webhosting": ("#2196F3", "#64B5F6"),
    "devops": ("#FF9800", "#FFB74D"),
}
PURPLE = "#9C27B0"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def auto_font(size=36):
    paths = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def draw_icon_rounded_rect(draw, x, y, w, h, r=20, fill=(255,255,255), width=8):
    """Draw a rounded rectangle outline."""
    draw.rounded_rectangle([x, y, x+w, y+h], radius=r, outline=fill, width=width)

def draw_icon_circle(draw, cx, cy, r, fill=(255,255,255), width=None):
    if width:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=fill, width=width)
    else:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)

def draw_icon_line(draw, x1, y1, x2, y2, fill=(255,255,255), width=6):
    draw.line([x1, y1, x2, y2], fill=fill, width=width)

def make_gaming():
    canvas = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(canvas)
    left_rgb = hex_to_rgb(CAT_COLORS["gaming"][0])
    purple_rgb = hex_to_rgb(PURPLE)
    draw.rectangle([(0, 0), (W//2, H)], fill=left_rgb)
    draw.rectangle([(W//2, 0), (W, H)], fill=purple_rgb)
    for xo in range(-2, 3):
        draw.line([(W//2+xo, 0), (W//2+xo, H)], fill=(255,255,255), width=1)
    
    # Game controller icon
    cx, cy = 600, 240
    # Controller body
    draw_icon_rounded_rect(draw, cx-110, cy-50, 220, 130, r=50, width=18)
    # D-pad
    draw.rectangle([cx-70, cy-25, cx-40, cy+25], fill=(255,255,255))
    draw.rectangle([cx-55, cy-40, cx-55, cy+40], fill=(255,255,255))
    # Buttons
    draw_icon_circle(draw, cx+80, cy-30, 14, fill=(255,255,255))
    draw_icon_circle(draw, cx+95, cy-10, 14, fill=(255,255,255))
    draw_icon_circle(draw, cx+80, cy+10, 14, fill=(255,255,255))
    draw_icon_circle(draw, cx+65, cy-10, 14, fill=(255,255,255))
    # Analog sticks
    draw_icon_circle(draw, cx-20, cy-40, 22, width=10)
    draw_icon_circle(draw, cx-20, cy+40, 22, width=10)
    # Server rack below
    draw_icon_rounded_rect(draw, 420, 440, 360, 120, r=20, width=14)
    for sy in [470, 500, 530]:
        draw.line([450, sy, 750, sy], fill=(255,255,255), width=6)
    for sx in [450, 465]:
        draw_icon_circle(draw, sx, 470, 5, fill=(255,255,255))
    
    font = auto_font(28)
    draw.text((400, 590), "GAMING SERVER GUIDE", fill=(255,255,255), font=font)
    return canvas

def make_webhosting():
    canvas = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(canvas)
    left_rgb = hex_to_rgb(CAT_COLORS["webhosting"][0])
    purple_rgb = hex_to_rgb(PURPLE)
    draw.rectangle([(0, 0), (W//2, H)], fill=left_rgb)
    draw.rectangle([(W//2, 0), (W, H)], fill=purple_rgb)
    for xo in range(-2, 3):
        draw.line([(W//2+xo, 0), (W//2+xo, H)], fill=(255,255,255), width=1)
    
    # Globe icon
    cx, cy = 600, 240
    draw_icon_circle(draw, cx, cy, 90, width=14)
    # Globe lines - horizontal
    for angle_deg in [-60, -30, 0, 30, 60]:
        import math
        angle = math.radians(angle_deg)
        w = 90 * math.cos(angle)
        h_e = 90 * math.sin(angle)
        y = cy + h_e
        if y < cy - 85 or y > cy + 85:
            continue
        x_left = cx - w
        x_right = cx + w
        draw.line([x_left, y, x_right, y], fill=(255,255,255), width=5)
    # Globe vertical line
    draw.line([cx, cy-90, cx, cy+90], fill=(255,255,255), width=5)
    # Globe arc
    draw.arc([cx-90, cy-90, cx+90, cy+90], -60, 60, fill=(255,255,255), width=5)
    draw.arc([cx-90, cy-90, cx+90, cy+90], 120, 240, fill=(255,255,255), width=5)
    
    # Server below globe
    cy2 = 470
    draw_icon_rounded_rect(draw, cx-120, cy2-30, 240, 100, r=16, width=12)
    for sy in [cy2, cy2+30]:
        draw.line([cx-95, sy, cx+95, sy], fill=(255,255,255), width=6)
    draw_icon_circle(draw, cx-80, cy2-16, 4, fill=(255,255,255))
    draw_icon_circle(draw, cx-80, cy2+14, 4, fill=(255,255,255))
    
    # Cloud shape above globe
    for cloud_cx, cloud_cy, cloud_r in [(cx-40, cy-130, 35), (cx+10, cy-140, 45), (cx+60, cy-130, 35)]:
        draw_icon_circle(draw, cloud_cx, cloud_cy, cloud_r, fill=(255,255,255))
    draw.rectangle([cx-65, cy-155, cx+85, cy-115], fill=(255,255,255))
    
    font = auto_font(28)
    draw.text((380, 580), "WEBHOSTING GUIDE", fill=(255,255,255), font=font)
    return canvas

def make_devops():
    canvas = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(canvas)
    left_rgb = hex_to_rgb(CAT_COLORS["devops"][0])
    purple_rgb = hex_to_rgb(PURPLE)
    draw.rectangle([(0, 0), (W//2, H)], fill=left_rgb)
    draw.rectangle([(W//2, 0), (W, H)], fill=purple_rgb)
    for xo in range(-2, 3):
        draw.line([(W//2+xo, 0), (W//2+xo, H)], fill=(255,255,255), width=1)
    
    cx, cy = 600, 230
    # Gear/wheel icon
    draw_icon_circle(draw, cx, cy, 75, width=14)
    draw_icon_circle(draw, cx, cy, 35, fill=(255,255,255))
    # Gear teeth
    for i in range(8):
        import math
        angle = math.radians(i * 45)
        rx1 = 75 * math.cos(angle)
        ry1 = 75 * math.sin(angle)
        rx2 = 100 * math.cos(angle)
        ry2 = 100 * math.sin(angle)
        aw = 16
        draw.line([rx1, ry1, rx2, ry2], fill=(255,255,255), width=aw)
    
    # Terminal bracket symbols
    font_large = auto_font(40)
    draw.text((cx-120, cy+80), "</>", fill=(255,255,255), font=font_large)
    
    # Code lines
    for i, y in enumerate([cy+145, cy+165, cy+185]):
        w = 200 - i * 40
        draw.line([cx-100, y, cx-100+w, y], fill=(255,255,255), width=6)
    
    # Pipeline dots
    sx, sy = 680, 380
    for i in range(4):
        draw_icon_circle(draw, sx+i*30, sy, 6, fill=(255,255,255))
        if i < 3:
            draw.line([sx+i*30+8, sy, sx+(i+1)*30-8, sy], fill=(255,255,255), width=4)
    
    font = auto_font(28)
    draw.text((420, 590), "DEVOPS GUIDE", fill=(255,255,255), font=font)
    return canvas

if __name__ == "__main__":
    print("Generating 3 sample hero images...")
    for name, maker in [("hero-gaming", make_gaming), ("hero-webhosting", make_webhosting), ("hero-devops", make_devops)]:
        img = maker()
        path = os.path.join(OUTPUT, f"{name}.png")
        img.save(path, "PNG", quality=95)
        size = os.path.getsize(path)
        print(f"  ✅ {name}.png - {size/1024:.0f} KB - {img.size}")
    print("\n3 Hero-Bilder erstellt im Pop-Tech-Stil!")
