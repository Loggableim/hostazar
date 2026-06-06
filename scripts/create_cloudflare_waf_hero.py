"""Create hero image for Cloudflare WAF article."""
import os
from PIL import Image, ImageDraw, ImageFont

output_dir = r"C:\HermesPortable\hostazar\images"
os.makedirs(output_dir, exist_ok=True)

# Dark navy background
W, H = 1216, 640
img = Image.new('RGB', (W, H), '#0a0e27')
draw = ImageDraw.Draw(img)

# Cloudflare orange accent
accent = (243, 128, 32)  # #F38020
accent_dark = (200, 95, 15)
accent_glow = (255, 165, 60)

# Subtle gradient background (vertical)
for y in range(H):
    # Lerp between two dark navy tones
    t = y / H
    r = int(0x0a + (0x12 - 0x0a) * t)
    g = int(0x0e + (0x16 - 0x0e) * t)
    b = int(0x27 + (0x3a - 0x27) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Draw a subtle grid pattern (security/network feel)
for x in range(0, W, 48):
    draw.line([(x, 0), (x, H)], fill='#161a3a', width=1)
for y in range(0, H, 48):
    draw.line([(0, y), (W, y)], fill='#161a3a', width=1)

# Draw Cloudflare-style orange shield/wall on the right
# Big shield outline
shield_x, shield_y, shield_w, shield_h = 760, 130, 320, 380
# Shield shape using polygon
shield_points = [
    (shield_x + shield_w/2, shield_y),                # top center
    (shield_x + shield_w, shield_y + 60),              # top right
    (shield_x + shield_w, shield_y + shield_h*0.55),   # right
    (shield_x + shield_w/2, shield_y + shield_h),      # bottom point
    (shield_x, shield_y + shield_h*0.55),              # left
    (shield_x, shield_y + 60),                          # top left
]
# Glow behind shield
for i in range(8, 0, -1):
    glow_color = (243, 128, 32, 25 + i*5)
    draw.polygon([
        (shield_x - i*3 + shield_w/2, shield_y - i*2),
        (shield_x + shield_w + i*3, shield_y + 60),
        (shield_x + shield_w + i*3, shield_y + shield_h*0.55),
        (shield_x + shield_w/2, shield_y + shield_h + i*2),
        (shield_x - i*3, shield_y + shield_h*0.55),
        (shield_x - i*3, shield_y + 60),
    ], outline=(243, 128, 32), width=1)

# Shield body (semi-transparent fill effect by drawing nested polygons)
draw.polygon(shield_points, fill=(28, 22, 50), outline=accent, width=4)

# Inner shield detail lines
draw.line([
    (shield_x + 30, shield_y + 100),
    (shield_x + shield_w/2, shield_y + 30),
    (shield_x + shield_w - 30, shield_y + 100)
], fill=accent_dark, width=2)

# Draw firewall blocks / WAF bricks inside the shield
brick_x, brick_y = shield_x + 70, shield_y + 140
brick_w, brick_h = 180, 40
# Row 1
for i in range(3):
    bx = brick_x + (i % 2) * 30
    draw.rectangle([bx, brick_y, bx + brick_w, brick_y + brick_h],
                   outline=accent, width=2)
# Row 2 offset
for i in range(3):
    bx = brick_x - 30 + (i % 2) * 30 + 30
    draw.rectangle([bx, brick_y + 50, bx + brick_w, brick_y + 90],
                   outline=accent_glow, width=2)
# Row 3
for i in range(2):
    bx = brick_x + 30 + (i % 2) * 30
    draw.rectangle([bx, brick_y + 100, bx + brick_w, brick_y + 140],
                   outline=accent_dark, width=2)

# Top accent bar
draw.rectangle([0, 0, W, 6], fill=accent)
# Bottom accent bar (thinner)
draw.rectangle([0, H-4, W, H], fill=accent_dark)

# Small decorative dots (network nodes) on the left side
nodes = [(120, 80), (200, 540), (90, 320), (240, 200), (160, 460), (280, 380)]
for nx, ny in nodes:
    draw.ellipse([nx-4, ny-4, nx+4, ny+4], fill=accent_glow)
    # Connection line to a "central" point
    draw.line([(nx, ny), (320, 320)], fill=(243, 128, 32, 60), width=1)

# Central node
draw.ellipse([308, 308, 332, 332], fill=accent, outline=accent_glow, width=2)
draw.ellipse([300, 300, 340, 340], outline=accent, width=1)

# Font paths
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/c/Windows/Fonts/arialbd.ttf",
    "/c/Windows/Fonts/arial.ttf",
]

def get_font(size, bold=True):
    candidates = font_paths if bold else [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/c/Windows/Fonts/arial.ttf",
    ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    return ImageFont.load_default()

# Big title
try:
    font_title = get_font(60, bold=True)
    font_sub = get_font(28, bold=False)
    font_tag = get_font(18, bold=False)
    font_small = get_font(16, bold=False)

    # Title
    draw.text((60, 60), "Cloudflare WAF", fill=accent, font=font_title)
    # Subtitle
    draw.text((60, 140), "DDoS-Schutz & Bot-Filter 2026",
              fill='#e0e0e0', font=font_sub)
    draw.text((60, 180), "Web Application Firewall Schritt-f\u00fcr-Schritt einrichten",
              fill='#9aa3c7', font=font_sub)

    # Left side info block
    draw.text((60, 280), "Managed Rules  \u2022  Rate Limiting",
              fill='#cdd3ee', font=font_tag)
    draw.text((60, 310), "Bot Management  \u2022  Custom Rules",
              fill='#cdd3ee', font=font_tag)
    draw.text((60, 340), "DDoS L3/L7  \u2022  Magic Transit",
              fill='#cdd3ee', font=font_tag)
    draw.text((60, 370), "Zero Trust  \u2022  Cloudflare Tunnel",
              fill='#cdd3ee', font=font_tag)

    # Tech tags footer
    draw.text((60, 555), "OWASP  \u2022  SQLi  \u2022  XSS  \u2022  WAF  \u2022  DevSecOps  \u2022  2026",
              fill='#5a6290', font=font_tag)

    # Author/brand mark bottom-right
    draw.text((W - 230, 595), "hostazar.com", fill='#5a6290', font=font_small)
except Exception as e:
    print(f"Font rendering fallback: {e}")

path = os.path.join(output_dir, "cloudflare-waf-einrichten-2026.png")
img.save(path, 'PNG')
sz = os.path.getsize(path)
print(f"\u2713 cloudflare-waf-einrichten-2026.png ({sz//1024} KB)")
print(f"  Pfad: {path}")
