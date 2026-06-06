"""Create hero image for Jitsi Meet Server article."""
import os
from PIL import Image, ImageDraw

output_dir = "/c/HermesPortable/hostazar/images"
os.makedirs(output_dir, exist_ok=True)

filename = "jitsi-meet-server-vps-2026.png"
accent = (33, 150, 243)  # Blue = Webhosting category

img = Image.new('RGB', (1216, 640), '#1a1a2e')
draw = ImageDraw.Draw(img)

# Draw accent strips in blue tones
for i in range(6):
    bar_color = tuple(min(c + 30 * i, 255) for c in accent)
    draw.rectangle([0, 100 + i * 7, 1216, 105 + i * 7], fill=bar_color)

# Draw simple grid pattern
for x in range(0, 1216, 60):
    draw.rectangle([x, 0, x + 1, 640], fill='#222244')
for y in range(0, 640, 60):
    draw.rectangle([0, y, 1216, y + 1], fill='#222244')

# Draw accent circle
draw.ellipse([458, 170, 758, 470], fill=accent + (60,), outline=accent, width=4)

# Draw a smaller inner circle
draw.ellipse([508, 220, 708, 420], outline=(100, 180, 255), width=2)

path = os.path.join(output_dir, filename)
img.save(path, 'PNG')
sz = os.path.getsize(path)
print(f"✓ {filename} ({sz // 1024} KB)")
print("Hero image created successfully!")