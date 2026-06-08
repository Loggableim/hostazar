#!/usr/bin/env python3
"""Regenerate broken KI/LLM hero images — high quality Pillow art, 1200x630."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')
os.makedirs(OUTPUT, exist_ok=True)
W, H = 1200, 630

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1, c2))

def draw_base_gradient(draw, c1, c2):
    for y in range(H):
        t = y / H
        draw.line([(0,y),(W,y)], fill=lerp(c1, c2, t))

def draw_grid(draw, color, spacing=60, alpha=20):
    c = (color[0]//6, color[1]//6, color[2]//6, alpha)
    for x in range(0, W, spacing):
        draw.line([(x,0),(x,H)], fill=c, width=1)
    for y in range(0, H, spacing):
        draw.line([(0,y),(W,y)], fill=c, width=1)

def draw_glow_circle(draw, cx, cy, r, color, intensity=1.0):
    for i in range(r*3, 0, -2):
        t = i / (r*3)
        a = int(120 * intensity * (1-t)**2)
        if a < 1: continue
        c = tuple(min(255, int(cc * (1-t) + 15 * t)) for cc in color)
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c + (a,))

def draw_neural_net(draw, accent):
    random.seed(42)
    # Nodes in layers
    layers = [(150, [200, 280, 360, 440]), (300, [180, 260, 340, 420, 500]),
              (500, [160, 230, 300, 370, 440, 510]), (700, [200, 280, 360, 440]),
              (850, [250, 330, 410])]
    all_nodes = []
    for lx, lys in layers:
        layer_nodes = []
        for ly in lys:
            r = random.randint(5, 12)
            layer_nodes.append((lx, ly, r))
            # Glow
            draw_glow_circle(draw, lx, ly, r, accent, 0.4)
            draw.ellipse([lx-r, ly-r, lx+r, ly+r], fill=accent + (160,))
        all_nodes.append(layer_nodes)
    # Connections
    for li in range(len(all_nodes)-1):
        for x1, y1, r1 in all_nodes[li]:
            for x2, y2, r2 in all_nodes[li+1][:3]:
                draw.line([(x1,y1),(x2,y2)], fill=(accent[0]//3, accent[1]//3, accent[2]//3, 30), width=1)

def draw_server_rack(draw, x, y, w, h, accent):
    # Rack body
    draw.rectangle([x, y, x+w, y+h], fill=(15,15,35), outline=accent+(80,), width=2)
    # Server units
    for i in range(6):
        sy = y + 15 + i * (h-30) // 6
        draw.rectangle([x+8, sy, x+w-8, sy+18], fill=(25,25,50), outline=accent+(40,), width=1)
        # LEDs
        for j in range(4):
            led_colors = [(0,200,100), (0,150,255), (255,200,0), (255,80,80)]
            lc = led_colors[j] if random.random() > 0.2 else (50,50,50)
            draw.ellipse([x+w-30+j*10, sy+5, x+w-26+j*10, sy+13], fill=lc + (200,))
    # Glow from rack
    draw_glow_circle(draw, x+w//2, y+h//2, w, accent, 0.3)

def draw_gpu_cluster(draw, accent):
    random.seed(123)
    for i in range(7):
        gx = 150 + i * 150
        gy = 200 + (i % 3) * 100
        gw, gh = 110, 55
        # GPU body with gradient
        for dx in range(gw):
            t = dx / gw
            c = lerp((20,20,45), accent, t * 0.15)
            draw.line([(gx-gw//2+dx, gy-gh//2), (gx-gw//2+dx, gy+gh//2)], fill=c)
        draw.rectangle([gx-gw//2, gy-gh//2, gx+gw//2, gy+gh//2], outline=accent+(120,), width=2)
        # Fan blades
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = gx + int(15 * math.cos(rad))
            y1 = gy + int(15 * math.sin(rad))
            x2 = gx + int(25 * math.cos(rad))
            y2 = gy + int(25 * math.sin(rad))
            draw.line([(x1,y1),(x2,y2)], fill=accent+(80,), width=2)
        # Circuit traces
        for t in range(5):
            ty = gy - gh//2 + 8 + t * 10
            draw.line([(gx-gw//2+8, ty), (gx+gw//2-8, ty)], fill=(accent[0]//3, accent[1]//3, accent[2]//3, 50), width=1)
        # PCIe connector
        draw.rectangle([gx-10, gy+gh//2, gx+10, gy+gh//2+18], fill=(200,180,50,140))
        # Glow
        draw_glow_circle(draw, gx, gy, 30, accent, 0.5)
    # Connection bus at bottom
    for y in [320, 420]:
        draw.line([(100, y), (1100, y)], fill=accent+(40,), width=2)

def draw_ai_chip(draw, cx, cy, accent):
    # Main chip body — large detailed processor
    for r in range(130, 0, -2):
        t = r / 130
        c = lerp((15,15,40), accent, t * 0.25)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c + (15,))
    # Outer ring
    draw.ellipse([cx-120, cy-120, cx+120, cy+120], fill=(20,20,50), outline=accent+(150,), width=3)
    # Inner rings
    for r in [90, 60, 30]:
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=accent+(50 + r,), width=1)
    # Circuit traces radiating out
    for angle in range(0, 360, 8):
        rad = math.radians(angle)
        x1, y1 = cx + int(125*math.cos(rad)), cy + int(125*math.sin(rad))
        x2, y2 = cx + int(200*math.cos(rad)), cy + int(200*math.sin(rad))
        draw.line([(x1,y1),(x2,y2)], fill=accent+(40 + int(20*math.sin(angle*3)),), width=1)
    # Corner markers
    for dx, dy in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        mx, my = cx + dx*100, cy + dy*100
        draw.rectangle([mx-8, my-8, mx+8, my+8], fill=accent+(100,), outline=accent+(150,), width=2)
    # Center glow
    draw_glow_circle(draw, cx, cy, 50, accent, 0.7)
    # Data flow animation dots
    random.seed(42)
    for _ in range(30):
        angle = random.uniform(0, 2*math.pi)
        dist = random.randint(40, 100)
        x = cx + int(dist * math.cos(angle))
        y = cy + int(dist * math.sin(angle))
        draw.ellipse([x-3, y-3, x+3, y+3], fill=accent+(150,))

def draw_cloud_server(draw, accent):
    # Cloud shapes
    for cx, cy, r in [(350, 180, 70), (410, 160, 50), (470, 180, 60)]:
        draw_glow_circle(draw, cx, cy, r, accent, 0.3)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(25,25,55), outline=accent+(80,), width=2)
    # Server below
    draw_server_rack(draw, 500, 280, 160, 200, accent)
    # Connection lines
    for i in range(4):
        y = 240 + i * 30
        draw.line([(440, y), (500, y)], fill=accent+(60,), width=2)

def draw_particles(draw, accent, count=200):
    random.seed(999)
    for _ in range(count):
        x, y = random.randint(0, W), random.randint(0, H)
        s = random.randint(1, 3)
        a = random.randint(15, 60)
        c = (accent[0]//3, accent[1]//3, accent[2]//3, a)
        draw.ellipse([x, y, x+s, y+s], fill=c)

def draw_bottom_fade(draw):
    for i in range(80):
        t = i / 80
        y = H - 80 + i
        draw.line([(0,y),(W,y)], fill=(8,8,24,int(200*t)), width=1)

def make_hero(filename, accent_hex, icon_type):
    random.seed(hash(filename) % 2**32)
    accent = hex_to_rgb(accent_hex)
    
    canvas = Image.new('RGB', (W, H), (8, 8, 24))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    
    # Background gradient
    draw_base_gradient(draw, (8, 8, 28), (12, 10, 45))
    
    # Grid
    draw_grid(draw, accent, 80, 15)
    
    # Icon based on type
    if icon_type == 'neural':
        draw_neural_net(draw, accent)
    elif icon_type == 'server':
        draw_server_rack(draw, 350, 100, 200, 300, accent)
    elif icon_type == 'gpu':
        draw_gpu_cluster(draw, accent)
    elif icon_type == 'chip':
        draw_ai_chip(draw, W//2, H//2 - 30, accent)
    elif icon_type == 'cloud':
        draw_cloud_server(draw, accent)
    
    # Particles
    draw_particles(draw, accent, 150)
    
    # Bottom fade
    draw_bottom_fade(draw)
    
    # Save as high-quality PNG
    canvas = canvas.convert('RGB')
    path = os.path.join(OUTPUT, filename)
    canvas.save(path, 'PNG', optimize=True)
    sz = os.path.getsize(path)
    return sz

# All broken KI/LLM images
targets = [
    ('llm-lokal-hosten-2026.png', '#9C27B0', 'neural'),
    ('llama-cpp-cpu-vs-gpu-performance-2026.png', '#9C27B0', 'gpu'),
    ('comfyui-auf-gpu-hosten.png', '#9C27B0', 'gpu'),
    ('ki-server-sicherheit-llm-api-absichern-2026.png', '#FF9800', 'server'),
    ('runpod-serverless-vs-dedicated-gpu-2026.png', '#9C27B0', 'cloud'),
    ('vast-ai-gpu-mieten-2026.png', '#9C27B0', 'cloud'),
    ('ai-agent-frameworks-2026.png', '#9C27B0', 'neural'),
    ('mistral-modelle-lokal-hosten-2026.png', '#9C27B0', 'chip'),
    ('cloud-gpu-kosten-vergleich-2026.png', '#2196F3', 'cloud'),
    ('cuda-rocam-vulkan-lokale-llm-gpu-backend-vergleich-2026.png', '#9C27B0', 'gpu'),
    ('deepseek-r1-v3-lokal-hosten-2026.png', '#9C27B0', 'chip'),
    ('docker-llm-inference-container.png', '#2196F3', 'server'),
    ('gpu-fuer-ki-modelle-mieten-2026.png', '#9C27B0', 'gpu'),
    ('gpu-ram-manager-2026.png', '#9C27B0', 'chip'),
    ('llama-3-3-4-lokal-hosten-2026.png', '#9C27B0', 'chip'),
    ('llm-fine-tuning-runpod-vastai-2026.png', '#9C27B0', 'neural'),
    ('llm-frontends-vergleich-2026.png', '#9C27B0', 'neural'),
    ('nvidia-jetson-ki-am-edge-llm-embedded-2026.png', '#9C27B0', 'chip'),
    ('ollama-vs-vllm-vs-lm-studio-2026.png', '#9C27B0', 'server'),
    ('open-webui-ollama-betreiben-2026.png', '#9C27B0', 'neural'),
    ('tabbyapi-aphrodite-sglang-llm-server-2026.png', '#9C27B0', 'server'),
    ('vllm-auf-eigener-gpu-aufsetzen.png', '#9C27B0', 'gpu'),
    ('vllm-multi-model-server-2026.png', '#9C27B0', 'server'),
    ('ki-im-devops-einsatz-2026.png', '#FF9800', 'neural'),
    ('llm-sicherheit-prompt-injection-schutz-2026.png', '#FF9800', 'server'),
    ('ki-gestuetzte-code-reviews-praxis-2026.png', '#9C27B0', 'neural'),
    ('openrouter-api-vs-eigene-gpu-kostenvergleich-2026.png', '#9C27B0', 'cloud'),
]

print(f"=== Regenerating {len(targets)} KI/LLM images ===\n")
total_sz = 0
for filename, color, icon in targets:
    sz = make_hero(filename, color, icon)
    total_sz += sz
    print(f"  {filename[:50]:50s} {sz//1024:3d} KB")

print(f"\nTotal: {len(targets)} images, {total_sz//1024} KB")
