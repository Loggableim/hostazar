"""Create hero image for Plausible Analytics article."""
import os
from PIL import Image, ImageDraw

output_dir = "C:\\HermesPortable\\hostazar\\images"
os.makedirs(output_dir, exist_ok=True)

filename = "plausible-analytics-vps-2026.png"
accent = (33, 150, 243)  # Blue #2196F3 = Webhosting

img = Image.new('RGB', (1216, 640), '#1a1a2e')
draw = ImageDraw.Draw(img)

# Draw accent strips in blue tones
for i in range(6):
    bar_color = tuple(min(c + 20 * i, 255) for c in accent)
    draw.rectangle([0, 100 + i * 6, 1216, 105 + i * 6], fill=bar_color)

# Draw simple grid pattern
for x in range(0, 1216, 60):
    draw.rectangle([x, 0, x + 1, 640], fill='#222244')
for y in range(0, 640, 60):
    draw.rectangle([0, y, 1216, y + 1], fill='#222244')

# Draw circle in blue
draw.ellipse([508, 180, 708, 380], fill=accent + (50,), outline=accent, width=3)

# Draw a smaller inner circle
draw.ellipse([558, 230, 658, 330], fill=(255, 255, 255, 20), outline=(100, 180, 255), width=2)

# Draw chart-like bars (graph icon effect)
bar_colors = [(33, 150, 243), (66, 165, 245), (100, 181, 246), (130, 177, 255)]
bar_positions = [(440, 380), (480, 350), (520, 370), (560, 310)]
for i, (bx, by) in enumerate(bar_positions):
    draw.rectangle([bx, by, bx + 20, 400], fill=bar_colors[i] + (180,))

# Draw a diamond shape
draw.polygon([(608, 150), (628, 170), (608, 190), (588, 170)], fill=(255, 255, 255, 30), outline=(150, 200, 255))

path = os.path.join(output_dir, filename)
img.save(path, 'PNG')
sz = os.path.getsize(path)
print(f"✓ {filename} ({sz//1024} KB)")
print("Image created successfully!")