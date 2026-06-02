#!/usr/bin/env python3
"""
Pop-Tech Kacheln Batch Generator für hostazar.com
Generiert alle Artikel-Bilder im Pop-Tech Kacheln Stil via ComfyUI SDXL + Pillow-Textoverlay.
Vollständige Liste aller 34 Artikel.
"""
import json, urllib.request, time, os, sys
from PIL import Image, ImageDraw, ImageFont

COMFY_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

ALL_ARTICLES = [
    # EXISTING (9)
    {"slug": "vps-absichern-2026", "title": "VPS absichern 2026", "category": "devops", "color": "#FF9800"},
    {"slug": "docker-compose-vps-guide", "title": "Docker Compose auf dem VPS", "category": "devops", "color": "#FF9800"},
    {"slug": "valheim-server-vps-mieten-2026", "title": "Valheim Server mieten", "category": "gaming", "color": "#4CAF50"},
    {"slug": "webhosting-anbieter-vergleich-2026", "title": "Webhosting-Anbieter 2026", "category": "webhosting", "color": "#2196F3"},
    {"slug": "minecraft-server-vergleich-2026", "title": "Minecraft Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "gameserver-mieten-guide", "title": "Gameserver mieten", "category": "gaming", "color": "#4CAF50"},
    {"slug": "webhosting-vserver-vergleich", "title": "Webhosting vs VServer", "category": "webhosting", "color": "#2196F3"},
    {"slug": "devops-tools-2024", "title": "DevOps Tools 2024", "category": "devops", "color": "#FF9800"},
    {"slug": "palworld-server-hosting-guide-2026", "title": "Palworld Server Hosting", "category": "gaming", "color": "#4CAF50"},
    # NEW GAMING (11)
    {"slug": "cs2-server-mieten-guide-2026", "title": "CS2 Server mieten", "category": "gaming", "color": "#4CAF50"},
    {"slug": "ark-survival-ascended-server-hosten-2026", "title": "ARK Survival Hosting", "category": "gaming", "color": "#4CAF50"},
    {"slug": "satisfactory-server-mieten-oder-selbst-hosten-2026", "title": "Satisfactory Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "rust-server-mieten-guide-2026", "title": "Rust Server mieten", "category": "gaming", "color": "#4CAF50"},
    {"slug": "7-days-to-die-server-hosten-2026", "title": "7 Days to Die Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "farming-simulator-25-server-mieten-2026", "title": "Farming Sim 25 Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "project-zomboid-server-hosting-2026", "title": "Project Zomboid Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "v-rising-server-mieten-2026", "title": "V Rising Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "terraria-server-hosten-2026", "title": "Terraria Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "enshrouded-server-hosting-2026", "title": "Enshrouded Server", "category": "gaming", "color": "#4CAF50"},
    {"slug": "dayz-server-mieten-2026", "title": "DayZ Server", "category": "gaming", "color": "#4CAF50"},
    # NEW WEBHOSTING (7)
    {"slug": "netcup-vps-erfahrungen-2026", "title": "Netcup VPS", "category": "webhosting", "color": "#2196F3"},
    {"slug": "hetzner-cloud-vs-dediziert-vergleich-2026", "title": "Hetzner Cloud vs Dediziert", "category": "webhosting", "color": "#2196F3"},
    {"slug": "domain-kaufen-einrichten-2026", "title": "Domain kaufen", "category": "webhosting", "color": "#2196F3"},
    {"slug": "ssl-zertifikat-lets-encrypt-2026", "title": "SSL Let's Encrypt", "category": "webhosting", "color": "#2196F3"},
    {"slug": "wordpress-hosting-vergleich-2026", "title": "WordPress Hosting", "category": "webhosting", "color": "#2196F3"},
    {"slug": "website-online-bringen-guide-2026", "title": "Website online bringen", "category": "webhosting", "color": "#2196F3"},
    {"slug": "email-server-selbst-hosten-2026", "title": "E-Mail Server", "category": "webhosting", "color": "#2196F3"},
    # NEW DEVOPS (7)
    {"slug": "docker-vs-podman-vergleich-2026", "title": "Docker vs Podman", "category": "devops", "color": "#FF9800"},
    {"slug": "github-actions-ci-cd-pipeline-2026", "title": "GitHub Actions", "category": "devops", "color": "#FF9800"},
    {"slug": "nginx-reverse-proxy-einrichten-2026", "title": "Nginx Reverse Proxy", "category": "devops", "color": "#FF9800"},
    {"slug": "k3s-kubernetes-vps-2026", "title": "K3s Kubernetes", "category": "devops", "color": "#FF9800"},
    {"slug": "prometheus-grafana-monitoring-2026", "title": "Prometheus & Grafana", "category": "devops", "color": "#FF9800"},
    {"slug": "backup-strategien-vps-server-2026", "title": "Backup Strategien", "category": "devops", "color": "#FF9800"},
    {"slug": "terraform-infrastructure-as-code-2026", "title": "Terraform IaC", "category": "devops", "color": "#FF9800"},
]

CATEGORY_COLORS = {
    "gaming": ("#4CAF50", "#81C784"),
    "webhosting": ("#2196F3", "#64B5F6"),
    "devops": ("#FF9800", "#FFB74D"),
}

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def compose_poptech_basic(title_text, output_path, category):
    """Compose Pop-Tech image with category color background and text overlay."""
    W, H = 1200, 630
    if category in CATEGORY_COLORS:
        left_color_hex, _ = CATEGORY_COLORS[category]
    else:
        left_color_hex = "#9C27B0"
    purple = "#9C27B0"
    left_rgb = hex_to_rgb(left_color_hex)
    purple_rgb = hex_to_rgb(purple)

    canvas = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([(0, 0), (W // 2, H)], fill=left_rgb)
    draw.rectangle([(W // 2, 0), (W, H)], fill=purple_rgb)
    for x_offset in range(-2, 3):
        draw.line([(W // 2 + x_offset, 0), (W // 2 + x_offset, H)], fill=(255, 255, 255), width=1)

    font_paths = [
        "C:/Windows/Fonts/seguiemj.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 36)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()

    # Draw text centered
    lines = []
    words = title_text.split()
    if len(words) <= 3:
        lines = [title_text]
    else:
        mid = len(words) // 2
        lines = [' '.join(words[:mid]), ' '.join(words[mid:])]
    
    text_lines = lines if lines else [title_text]
    for li, line in enumerate(text_lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        tx = (W - tw) // 2
        ty = (H // 2) - 40 + li * 50
        draw.text((tx + 1, ty + 1), line, fill=(0, 0, 0, 100), font=font)
        draw.text((tx, ty), line, fill=(255, 255, 255), font=font)

    # Category badge
    badge_text = category.upper()
    bbox2 = draw.textbbox((0, 0), badge_text, font=font)
    bw = bbox2[2] - bbox2[0]
    draw.rectangle((20, 20, 30 + bw, 46), fill=left_rgb)
    draw.text((25, 23), badge_text, fill=(255, 255, 255), font=font)

    canvas.save(output_path, "PNG", quality=95)
    print(f"  Composed: {os.path.basename(output_path)}")
    return output_path

def main():
    print(f"=== Pop-Tech Batch Generator ({len(ALL_ARTICLES)} articles) ===\n")
    
    # Use existing icon if available, otherwise compose minimal
    for art in ALL_ARTICLES:
        slug = art["slug"]
        output_path = os.path.join(OUTPUT_DIR, f"{slug}.png")
        icon_path = os.path.join(OUTPUT_DIR, f"icon_{slug}.png")
        
        # If final image already exists and is large enough, skip
        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            print(f"  [SKIP] {slug} — already exists")
            continue
        
        # Simple deterministic icon if no SDXL available
        if not (os.path.exists(icon_path) and os.path.getsize(icon_path) > 1000):
            # Generate a simple geometric icon
            S = 512
            icon = Image.new('RGB', (S, S), '#222222')
            di = ImageDraw.Draw(icon)
            white = (255, 255, 255)
            cx, cy = S // 2, S // 2
            # Draw a simple shape based on category
            if art['category'] == 'gaming':
                # Gamepad shape
                di.rounded_rectangle([cx-120, cy-80, cx+120, cy+80], radius=40, outline=white, width=24)
                di.rectangle([cx-60, cy-110, cx-20, cy+110], fill=white)
                di.rectangle([cx+20, cy-110, cx+60, cy+110], fill=white)
                di.ellipse([cx-100, cy-100, cx+100, cy+100], outline=white, width=12)
            elif art['category'] == 'webhosting':
                # Globe
                di.ellipse([cx-100, cy-100, cx+100, cy+100], outline=white, width=20)
                di.arc([cx-60, cy-100, cx+60, cy+100], 0, 360, fill=white, width=12)
                di.line([cx, cy-100, cx, cy+100], fill=white, width=12)
                di.line([cx-100, cy, cx+100, cy], fill=white, width=12)
            else:
                # Gear for devops
                di.ellipse([cx-80, cy-80, cx+80, cy+80], outline=white, width=20)
                for angle in range(0, 360, 45):
                    import math
                    a = math.radians(angle)
                    ex = cx + 95 * math.cos(a)
                    ey = cy + 95 * math.sin(a)
                    di.ellipse([int(ex-16), int(ey-16), int(ex+16), int(ey+16)], fill=white)
                di.ellipse([cx-30, cy-30, cx+30, cy+30], fill='#222222')
            icon.save(icon_path)
            print(f"  Icon generated: icon_{slug}.png")
        
        # Compose final image with Pillow text overlay
        compose_poptech_basic(art["title"], output_path, art["category"])
    
    print(f"\n=== Done. Generated/verified {len(ALL_ARTICLES)} images ===")

if __name__ == "__main__":
    main()
