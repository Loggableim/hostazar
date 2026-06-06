"""Create hero image for Discord Bot VPS article."""
import os
from PIL import Image, ImageDraw, ImageFont

output_dir = r"C:\HermesPortable\images"
os.makedirs(output_dir, exist_ok=True)

# Discord-blurple inspired dark navy background
W, H = 1216, 640
img = Image.new('RGB', (W, H), '#0a0e27')
draw = ImageDraw.Draw(img)

# Discord blurple accent color (#5865F2)
accent = (88, 101, 242)
accent_light = (155, 165, 255)
accent_dark = (54, 60, 140)

# Subtle grid pattern (tech feel)
for x in range(0, W, 60):
    draw.rectangle([x, 0, x+1, H], fill='#121833')
for y in range(0, H, 60):
    draw.rectangle([0, y, W, y+1], fill='#121833')

# Diagonal accent strips (top-left to bottom-right)
for i in range(5):
    alpha = 30 + i * 15
    color = tuple(min(c + i * 12, 255) for c in accent_dark)
    draw.rectangle([0, 80 + i * 8, W, 88 + i * 8], fill=color)

# Glowing orbs (Discord-style)
for cx, cy, r, c in [
    (980, 130, 90, accent),
    (1080, 220, 60, accent_light),
    (160, 480, 80, accent_dark),
    (240, 540, 50, accent),
]:
    # outer glow
    for k in range(8, 0, -1):
        gc = tuple(max(0, v - k * 6) for v in c)
        draw.ellipse([cx - r - k*3, cy - r - k*3, cx + r + k*3, cy + r + k*3], outline=gc, width=1)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

# Stylized Discord/Robot icon (center-right)
# Robot head
hx, hy, hr = 850, 240, 110
draw.rounded_rectangle([hx - hr, hy - hr, hx + hr, hy + hr], radius=24, fill=accent, outline=accent_light, width=3)
# Eyes
draw.ellipse([hx - 55, hy - 25, hx - 25, hy + 5], fill='#0a0e27')
draw.ellipse([hx + 25, hy - 25, hx + 55, hy + 5], fill='#0a0e27')
# Glow inside eyes
draw.ellipse([hx - 48, hy - 18, hx - 32, hy - 2], fill=accent_light)
draw.ellipse([hx + 32, hy - 18, hx + 48, hy - 2], fill=accent_light)
# Smile (rectangle)
draw.rectangle([hx - 30, hy + 35, hx + 30, hy + 50], fill='#0a0e27')
# Antenna
draw.rectangle([hx - 4, hy - hr - 30, hx + 4, hy - hr], fill=accent)
draw.ellipse([hx - 12, hy - hr - 45, hx + 12, hy - hr - 25], fill=accent_light, outline=accent, width=2)
# Body/circuit lines below
draw.line([hx - 60, hy + 130, hx + 60, hy + 130], fill=accent_light, width=3)
for x_off in [-40, 0, 40]:
    draw.rectangle([hx + x_off - 4, hy + 130, hx + x_off + 4, hy + 145], fill=accent_light)

# Code-like decorative lines on the left (like a terminal)
code_x, code_y = 90, 380
lines = [
    ("$ npm install discord.js", accent_light),
    ("$ pm2 start bot.js", accent_light),
    ("✓ Bot online", (80, 220, 120)),
    ("✗ 200ms ping", (255, 152, 100)),
]
try:
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/c/Windows/Fonts/consola.ttf",
        "/c/Windows/Fonts/arial.ttf",
    ]
    font_mono = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_mono = ImageFont.truetype(fp, 22)
            break
    if font_mono is None:
        font_mono = ImageFont.load_default()
    for i, (text, col) in enumerate(lines):
        draw.text((code_x, code_y + i * 30), text, fill=col, font=font_mono)
except Exception:
    pass

# Title and subtitle
try:
    font_paths2 = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/c/Windows/Fonts/arialbd.ttf",
        "/c/Windows/Fonts/arial.ttf",
    ]
    font_big = None
    for fp in font_paths2:
        if os.path.exists(fp):
            font_big = ImageFont.truetype(fp, 52)
            break
    if font_big is None:
        font_big = ImageFont.load_default()

    font_med = None
    for fp in font_paths2:
        if os.path.exists(fp):
            font_med = ImageFont.truetype(fp, 26)
            break
    if font_med is None:
        font_med = ImageFont.load_default()

    font_small = None
    for fp in font_paths2:
        if os.path.exists(fp):
            font_small = ImageFont.truetype(fp, 18)
            break
    if font_small is None:
        font_small = ImageFont.load_default()

    # Title
    draw.text((80, 80), "Discord Bot", fill=accent_light, font=font_big)
    draw.text((80, 145), "auf VPS hosten", fill='#ffffff', font=font_big)
    # Subtitle
    draw.text((80, 220), "Komplettanleitung 2026", fill=accent, font=font_med)
    # Tech tags at bottom
    draw.text((80, 555), "Node.js 22  •  discord.js  •  PM2  •  Docker  •  Prisma  •  Webhooks", fill='#7a8294', font=font_small)
except Exception:
    pass

# Decorative corner brackets
draw.rectangle([20, 20, 60, 22], fill=accent)
draw.rectangle([20, 20, 22, 60], fill=accent)
draw.rectangle([W - 60, 20, W - 20, 22], fill=accent)
draw.rectangle([W - 22, 20, W - 20, 60], fill=accent)
draw.rectangle([20, H - 22, 60, H - 20], fill=accent)
draw.rectangle([20, H - 60, 22, H - 20], fill=accent)
draw.rectangle([W - 60, H - 22, W - 20, H - 20], fill=accent)
draw.rectangle([W - 22, H - 60, W - 20, H - 20], fill=accent)

path = os.path.join(output_dir, "discord-bot-vps-hosten-2026.png")
img.save(path, 'PNG')
sz = os.path.getsize(path)
print(f"✓ discord-bot-vps-hosten-2026.png ({sz//1024} KB) saved at {path}")
