"""Create simple placeholder hero images for new articles."""
import os
from PIL import Image, ImageDraw

output_dir = "/c/HermesPortable/hostazar/images"
os.makedirs(output_dir, exist_ok=True)

images = {
    "teamspeak-server-mieten-2026.png": ("TeamSpeak 3", "Sprachserver für Gamer 2026", (76, 175, 80)),
    "grafana-loki-log-aggregation-vps-2026.png": ("Grafana Loki", "Log-Aggregation auf VPS", (255, 152, 0)),
    "ghost-cms-hosting-vps-2026.png": ("Ghost CMS", "Blog-Software auf VPS hosten", (33, 150, 243)),
}

for filename, (title, subtitle, accent) in images.items():
    img = Image.new('RGB', (1216, 640), '#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Draw accent strips
    for i in range(6):
        bar_color = tuple(min(c + 30 * i, 255) for c in accent)
        draw.rectangle([0, 120 + i*5, 1216, 125 + i*5], fill=bar_color)
    
    # Draw simple grid pattern
    for x in range(0, 1216, 60):
        draw.rectangle([x, 0, x+1, 640], fill='#222244')
    for y in range(0, 640, 60):
        draw.rectangle([0, y, 1216, y+1], fill='#222244')
    
    # Draw circle
    draw.ellipse([508, 200, 708, 400], fill=accent + (60,), outline=accent, width=3)
    
    path = os.path.join(output_dir, filename)
    img.save(path, 'PNG')
    sz = os.path.getsize(path)
    print(f"✓ {filename} ({sz//1024} KB)")

print("\nAll 3 images created successfully!")
