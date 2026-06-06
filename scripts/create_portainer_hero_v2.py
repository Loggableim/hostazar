"""Create hero image for Portainer article - standalone version."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

# Use POSIX path for cross-compatibility on git-bash
output_dir = "/c/HermesPortable/hostazar/images"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "portainer-docker-management-vps-2026.png")

img = Image.new('RGB', (1216, 640), '#1a1a2e')
draw = ImageDraw.Draw(img)

accent = (255, 152, 0)  # DevOps Orange #FF9800

# Accent strips at bottom
for i in range(6):
    bar_color = tuple(min(c + 30 * i, 255) for c in accent)
    draw.rectangle([0, 570 + i*5, 1216, 575 + i*5], fill=bar_color)

# Grid pattern
for x in range(0, 1216, 60):
    draw.rectangle([x, 0, x+1, 640], fill='#222244')
for y in range(0, 640, 60):
    draw.rectangle([0, y, 1216, y+1], fill='#222244')

# Accent circle
draw.ellipse([458, 120, 758, 420], fill=None, outline=accent, width=4)
draw.ellipse([488, 150, 728, 390], fill=accent + (40,), outline=None)

# Stacked container boxes
box_color = accent
draw.rectangle([535, 200, 585, 250], fill=None, outline=box_color, width=2)
draw.rectangle([555, 240, 605, 290], fill=None, outline=box_color, width=2)
draw.rectangle([575, 280, 625, 330], fill=None, outline=box_color, width=2)

# Decorative dots around circle
for x in range(500, 720, 30):
    for y in range(200, 360, 30):
        draw.ellipse([x+12, y+12, x+14, y+14], fill=(255, 200, 80, 60))

# Text labels
try:
    # Try common font paths
    font = None
    for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
               "/c/Windows/Fonts/arial.ttf"]:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, 48)
            break
    if font is None:
        font = ImageFont.load_default()

    draw.text((70, 60), "Portainer", fill=accent, font=font)

    font_small = ImageFont.load_default()
    try:
        for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                   "/c/Windows/Fonts/arial.ttf"]:
            if os.path.exists(fp):
                font_small = ImageFont.truetype(fp, 26)
                break
    except:
        pass

    draw.text((70, 115), "Docker Management UI", fill='#ffffff', font=font_small)
    draw.text((70, 148), "auf VPS einrichten 2026", fill='#cccccc', font=font_small)

    font_tag = ImageFont.load_default()
    draw.text((70, 510), "Docker  ·  Container  ·  Web-UI  ·  DevOps", fill='#888888', font=font_tag)
except Exception as e:
    print(f"Font note: {e}")

img.save(output_path, 'PNG')
sz = os.path.getsize(output_path)
print(f"OK: {output_path} ({sz//1024} KB)")