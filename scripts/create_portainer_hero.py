"""Create hero image for Portainer article."""
import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "/c/HermesPortable/hostazar/images"
os.makedirs(output_dir, exist_ok=True)

img = Image.new('RGB', (1216, 640), '#1a1a2e')
draw = ImageDraw.Draw(img)

# DevOps orange accent
accent = (255, 152, 0)  # #FF9800

# Draw accent strips (orange tones)
for i in range(6):
    bar_color = tuple(min(c + 30 * i, 255) for c in accent)
    draw.rectangle([0, 140 + i*6, 1216, 146 + i*6], fill=bar_color)

# Draw simple grid pattern
for x in range(0, 1216, 60):
    draw.rectangle([x, 0, x+1, 640], fill='#222244')
for y in range(0, 640, 60):
    draw.rectangle([0, y, 1216, y+1], fill='#222244')

# Draw circle accent
draw.ellipse([458, 120, 758, 420], fill=None, outline=accent, width=4)
draw.ellipse([488, 150, 728, 390], fill=accent + (40,), outline=None)

# Draw container/box icons inside circle
# Container box 1
box_color = (255, 152, 0)
draw.rectangle([535, 220, 585, 270], fill=None, outline=box_color, width=2)
draw.rectangle([585, 240, 635, 290], fill=None, outline=box_color, width=2)
draw.rectangle([635, 260, 685, 310], fill=None, outline=box_color, width=2)
# Stacked look

# Draw some decorative dots
for x in range(530, 690, 30):
    for y in range(220, 320, 30):
        draw.ellipse([x+12, y+12, x+14, y+14], fill=(255, 200, 80, 80))

# Draw anchor text "Portainer" in a placeholder style
# We'll use a simple text drawing
try:
    # Try to find a font
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/c/Windows/Fonts/arial.ttf",
    ]
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, 48)
            break
    if font is None:
        font = ImageFont.load_default()
    
    # Draw title
    draw.text((100, 45), "Portainer", fill=accent, font=font)
    
    # Subtitle
    try:
        font_small = ImageFont.truetype(font_paths[1] if os.path.exists(font_paths[1]) else font_paths[0], 24)
    except:
        font_small = ImageFont.load_default()
    draw.text((100, 100), "Docker Management UI auf VPS 2026", fill='#cccccc', font=font_small)
    
    # Tech tags
    try:
        font_tag = ImageFont.truetype(font_paths[1] if os.path.exists(font_paths[1]) else font_paths[0], 16)
    except:
        font_tag = ImageFont.load_default()
    draw.text((100, 530), "Docker  •  Container  •  Web-UI  •  DevOps", fill='#888888', font=font_tag)
except:
    pass

path = os.path.join(output_dir, "portainer-docker-management-vps-2026.png")
img.save(path, 'PNG')
sz = os.path.getsize(path)
print(f"✓ portainer-docker-management-vps-2026.png ({sz//1024} KB)")