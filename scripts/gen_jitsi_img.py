from PIL import Image, ImageDraw
import os

img = Image.new('RGB', (1216, 640), (26, 26, 46))
draw = ImageDraw.Draw(img)

accent = (33, 150, 243)

for i in range(6):
    bar_color = tuple(min(c + 30 * i, 255) for c in accent)
    draw.rectangle([0, 100 + i * 7, 1216, 105 + i * 7], fill=bar_color)

for x in range(0, 1216, 60):
    draw.rectangle([x, 0, x + 1, 640], fill=(34, 34, 68))
for y in range(0, 640, 60):
    draw.rectangle([0, y, 1216, y + 1], fill=(34, 34, 68))

draw.ellipse([458, 170, 758, 470], fill=accent + (60,), outline=accent, width=4)
draw.ellipse([508, 220, 708, 420], outline=(100, 180, 255), width=2)

save_path = "C:\\HermesPortable\\hostazar\\images\\jitsi-meet-server-vps-2026.png"
img.save(save_path, 'PNG')
sz = os.path.getsize(save_path)
print(f"OK: {save_path} ({sz} bytes)")