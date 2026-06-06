"""Create hero image for the Palworld Mods & Dedicated Server Guide 2026 article."""
import os
from PIL import Image, ImageDraw, ImageFilter

# Palworld-themed colors
BG_TOP = (10, 12, 24)        # dark navy
BG_BOTTOM = (24, 14, 36)     # dark violet
ACCENT_YELLOW = (255, 203, 53)   # Palworld yellow
ACCENT_PINK = (236, 72, 153)     # hot pink
ACCENT_CYAN = (34, 211, 238)     # mod-cyan
GRID = (40, 50, 80)

WIDTH, HEIGHT = 1216, 640

# Output paths (both locations for safety)
output_paths = [
    r"C:\HermesPortable\hostazar\images\palworld-server-mods-guide-2026.png",
    r"C:\HermesPortable\home\scripts\blog-automation\hostazar\images\palworld-server-mods-guide-2026.png",
    r"C:\HermesPortable\images\palworld-server-mods-guide-2026.png",
]

# Create vertical gradient background
img = Image.new("RGB", (WIDTH, HEIGHT), BG_TOP)
draw = ImageDraw.Draw(img)

for y in range(HEIGHT):
    t = y / HEIGHT
    r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
    g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
    b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
    draw.rectangle([0, y, WIDTH, y + 1], fill=(r, g, b))

# Subtle grid pattern
for x in range(0, WIDTH, 60):
    draw.rectangle([x, 0, x + 1, HEIGHT], fill=GRID)
for y in range(0, HEIGHT, 60):
    draw.rectangle([0, y, WIDTH, y + 1], fill=GRID)

# Glowing accent strips top and bottom
for i in range(3):
    alpha = 200 - i * 60
    color = tuple(int(ACCENT_YELLOW[c] * (alpha / 255)) for c in range(3))
    draw.rectangle([0, 0 + i * 2, WIDTH, 4 + i * 2], fill=color)

for i in range(3):
    alpha = 200 - i * 60
    color = tuple(int(ACCENT_PINK[c] * (alpha / 255)) for c in range(3))
    draw.rectangle([0, HEIGHT - 4 - i * 2, WIDTH, HEIGHT - i * 2], fill=color)

# Stylized "Pal Spheres" (modular icons) - left side
sphere_positions = [
    (140, 200, 70, ACCENT_YELLOW),
    (320, 380, 90, ACCENT_PINK),
    (90, 460, 50, ACCENT_CYAN),
]
for cx, cy, r, color in sphere_positions:
    # Outer glow
    for g in range(8, 0, -1):
        glow = tuple(min(255, int(color[c] * (g / 10))) for c in range(3))
        draw.ellipse([cx - r - g * 2, cy - r - g * 2, cx + r + g * 2, cy + r + g * 2], outline=glow, width=1)
    # Sphere
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    # Inner detail (line)
    draw.line([cx - r + 6, cy, cx + r - 6, cy], fill=color, width=2)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=color, width=2)

# Right side: stacked "mod blocks" suggesting code/mods
block_x = 850
block_y = 100
block_w = 280
block_h = 38
block_colors = [ACCENT_YELLOW, ACCENT_CYAN, ACCENT_PINK, (180, 180, 180)]
for i, col in enumerate(block_colors):
    by = block_y + i * (block_h + 14)
    # Shadow
    draw.rectangle([block_x + 4, by + 4, block_x + block_w + 4, by + block_h + 4], fill=(0, 0, 0))
    # Block
    draw.rectangle([block_x, by, block_x + block_w, by + block_h], outline=col, width=2)
    # Inner text-bar
    draw.rectangle([block_x + 12, by + 12, block_x + 60, by + 12 + 8], fill=col)
    draw.rectangle([block_x + 70, by + 12, block_x + 180, by + 12 + 8], fill=(80, 80, 100))
    draw.rectangle([block_x + 190, by + 12, block_x + 240, by + 12 + 8], fill=(60, 60, 80))

# Bottom-left terminal text lines
term_x = 60
term_y = 540
term_lines = [
    ("> install BepInEx ............ OK", ACCENT_CYAN),
    ("> load PalSchema 1.4.2 ....... OK", ACCENT_YELLOW),
    ("> mod list: 17 active", ACCENT_PINK),
]
for txt, col in term_lines:
    draw.text((term_x, term_y), txt, fill=col)
    term_y += 22

# Title in center (using default font - bold-like via multi-pass)
title = "PALWORLD MODS"
sub = "& DEDICATED SERVER 2026"

# Save under all paths
for out_path in output_paths:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    sz = os.path.getsize(out_path)
    print(f"OK {out_path} ({sz // 1024} KB)")

print("\nHero image created successfully!")
