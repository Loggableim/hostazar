#!/usr/bin/env python3
"""Regenerate broken KI/LLM hero images (10-15KB placeholders) with proper AI-style art."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images')
os.makedirs(OUTPUT, exist_ok=True)
W, H = 1200, 630

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp_color(c1, c2, t):
    return tuple(int(a + (b-a)*t) for a,b in zip(c1, c2))

def add_glow(draw, cx, cy, r, color, alpha_base=80):
    for i in range(r, 0, -2):
        t = i / r
        a = int(alpha_base * (1-t))
        if a < 1: continue
        c = tuple(min(255, int(cc * t + 40 * (1-t))) for cc in color)
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=c + (a,))

def draw_neural_network(draw, nodes, connections, base_color):
    """Draw neural network nodes and connections."""
    for (x1, y1), (x2, y2) in connections:
        draw.line([(x1,y1),(x2,y2)], fill=base_color + (40,), width=1)
    for (x, y), r in nodes:
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        add_glow(gd, x, y, r*4, base_color, 60)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=base_color + (180,))

def draw_server_rack(draw, x, y, w, h, color):
    """Draw server rack silhouette."""
    draw.rectangle([x, y, x+w, y+h], fill=(20, 20, 40), outline=color + (100,), width=2)
    for i in range(5):
        sy = y + 10 + i * (h-20) // 5
        draw.rectangle([x+5, sy, x+w-5, sy+8], fill=color + (60,))
        # LED dots
        for j in range(3):
            led_c = (0, 255, 100) if random.random() > 0.3 else (255, 100, 0)
            draw.ellipse([x+w-15+j*8, sy+2, x+w-11+j*8, sy+6], fill=led_c + (200,))

def draw_gpu_chip(draw, cx, cy, w, h, color):
    """Draw GPU chip silhouette."""
    draw.rectangle([cx-w//2, cy-h//2, cx+w//2, cy+h//2], fill=(30,30,50), outline=color+(120,), width=2)
    # Circuit traces
    for i in range(4):
        ty = cy - h//2 + 10 + i * (h-20) // 4
        draw.line([(cx-w//2+5, ty), (cx+w//2-5, ty)], fill=color+(40,), width=1)

def make_ai_hero(filename, title, accent_color, icon_type='neural'):
    """Generate a hero image for KI/LLM articles."""
    random.seed(hash(filename) % 2**32)
    
    # Dark gradient background
    canvas = Image.new('RGB', (W, H), (8, 8, 24))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    
    # Base gradient
    bg_dark = (8, 8, 30)
    bg_mid = (15, 10, 50)
    for y in range(H):
        t = y / H
        c = lerp_color(bg_dark, bg_mid, t)
        draw.line([(0, y), (W, y)], fill=c)
    
    # Grid pattern (subtle)
    grid_color = (accent_color[0]//8, accent_color[1]//8, accent_color[2]//8, 15)
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=grid_color, width=1)
    
    if icon_type == 'neural':
        # Neural network visualization
        nodes = []
        connections = []
        layers = [4, 6, 8, 6, 4]
        layer_x = [200, 350, 500, 650, 800]
        for li, (lx, ncount) in enumerate(zip(layer_x, layers)):
            for ni in range(ncount):
                ly = 150 + ni * (H-300) // max(ncount-1, 1)
                r = random.randint(6, 14)
                nodes.append(((lx, ly), r))
                # Connect to previous layer
                if li > 0:
                    prev_nodes = nodes[-ncount-li:-ncount] if li > 0 else []
                    for (px, py), _ in prev_nodes[-3:]:
                        connections.append(((px, py), (lx, ly)))
        draw_neural_network(draw, nodes, connections, accent_color)
        
    elif icon_type == 'server':
        # Server rack with GPU
        draw_server_rack(draw, 350, 120, 200, 350, accent_color)
        draw_gpu_chip(draw, 650, 250, 120, 80, accent_color)
        # Glowing connections
        for i in range(5):
            y = 180 + i * 50
            draw.line([(550, y), (580, y)], fill=accent_color + (100,), width=2)
            
    elif icon_type == 'gpu':
        # Multiple GPUs
        for i, gx in enumerate([250, 450, 650, 850]):
            gy = 200 + (i % 2) * 100
            draw_gpu_chip(draw, gx, gy, 100, 60, accent_color)
            # PCIe connector
            draw.rectangle([gx-10, gy+30, gx+10, gy+50], fill=(200, 180, 50, 150))
    
    elif icon_type == 'cloud':
        # Cloud + server hybrid
        # Cloud shape
        for cx, cy, r in [(400, 200, 80), (460, 180, 60), (520, 200, 70)]:
            glow = Image.new('RGBA', (W, H), (0,0,0,0))
            gd = ImageDraw.Draw(glow)
            add_glow(gd, cx, cy, r*2, accent_color, 40)
            canvas.paste(Image.alpha_composite(canvas.convert('RGBA'), glow).convert('RGB'))
            draw = ImageDraw.Draw(canvas, 'RGBA')
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(30,30,60), outline=accent_color+(100,), width=2)
        # Server below
        draw_server_rack(draw, 500, 320, 180, 200, accent_color)
    
    elif icon_type == 'chip':
        # AI chip / processor
        cx, cy = W//2, H//2
        # Main chip body
        for r in range(120, 0, -5):
            t = r / 120
            c = lerp_color((20,20,50), accent_color, t*0.3)
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c + (30,))
        draw.ellipse([cx-100, cy-100, cx+100, cy+100], fill=(25,25,55), outline=accent_color+(150,), width=3)
        # Circuit traces radiating out
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            x1 = cx + int(110 * math.cos(rad))
            y1 = cy + int(110 * math.sin(rad))
            x2 = cx + int(160 * math.cos(rad))
            y2 = cy + int(160 * math.sin(rad))
            draw.line([(x1,y1),(x2,y2)], fill=accent_color+(80,), width=1)
        # Inner glow
        glow = Image.new('RGBA', (W, H), (0,0,0,0))
        gd = ImageDraw.Draw(glow)
        add_glow(gd, cx, cy, 80, accent_color, 50)
        canvas = Image.alpha_composite(canvas.convert('RGBA'), glow)
        draw = ImageDraw.Draw(canvas, 'RGBA')
    
    # Floating particles
    for _ in range(150):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 3)
        a = random.randint(20, 80)
        c = (accent_color[0]//2, accent_color[1]//2, accent_color[2]//2, a)
        draw.ellipse([x, y, x+s, y+s], fill=c)
    
    # Bottom gradient fade
    for i in range(100):
        t = i / 100
        y = H - 100 + i
        c = (8, 8, 24, int(255 * t))
        draw.line([(0, y), (W, y)], fill=c)
    
    # Title text area (dark bar at bottom)
    draw.rectangle([0, H-80, W, H], fill=(8, 8, 24, 200))
    
    # Save
    canvas = canvas.convert('RGB')
    path = os.path.join(OUTPUT, filename)
    canvas.save(path, 'PNG', quality=95)
    sz = os.path.getsize(path)
    print(f"  OK {filename} ({sz//1024}KB)")

# KI/LLM articles with broken images
targets = [
    # filename, title, accent_color, icon_type
    ('llm-lokal-hosten-2026.png', 'LLM lokal hosten', (156, 39, 176), 'neural'),
    ('llama-cpp-cpu-vs-gpu-performance-2026.png', 'llama.cpp Performance', (156, 39, 176), 'gpu'),
    ('comfyui-auf-gpu-hosten.png', 'ComfyUI GPU', (156, 39, 176), 'gpu'),
    ('ki-server-sicherheit-llm-api-absichern-2026.png', 'KI Server Sicherheit', (255, 152, 0), 'server'),
    ('runpod-serverless-vs-dedicated-gpu-2026.png', 'RunPod Serverless', (156, 39, 176), 'cloud'),
    ('vast-ai-gpu-mieten-2026.png', 'Vast.ai GPU', (156, 39, 176), 'cloud'),
    ('ai-agent-frameworks-2026.png', 'AI Agent Frameworks', (156, 39, 176), 'neural'),
    ('mistral-modelle-lokal-hosten-2026.png', 'Mistral lokal hosten', (156, 39, 176), 'chip'),
    ('cloud-gpu-kosten-vergleich-2026.png', 'Cloud GPU Kosten', (33, 150, 243), 'cloud'),
    ('cuda-rocam-vulkan-lokale-llm-gpu-backend-vergleich-2026.png', 'CUDA ROCm Vulkan', (156, 39, 176), 'gpu'),
    ('deepseek-r1-v3-lokal-hosten-2026.png', 'DeepSeek R1 V3', (156, 39, 176), 'chip'),
    ('docker-llm-inference-container.png', 'Docker LLM Inference', (33, 150, 243), 'server'),
    ('gpu-fuer-ki-modelle-mieten-2026.png', 'GPU KI Modelle mieten', (156, 39, 176), 'gpu'),
    ('gpu-ram-manager-2026.png', 'GPU RAM Manager', (156, 39, 176), 'chip'),
    ('llama-3-3-4-lokal-hosten-2026.png', 'Llama 33 4 lokal', (156, 39, 176), 'chip'),
    ('llm-fine-tuning-runpod-vastai-2026.png', 'LLM Fine Tuning', (156, 39, 176), 'neural'),
    ('llm-frontends-vergleich-2026.png', 'LLM Frontends', (156, 39, 176), 'neural'),
    ('nvidia-jetson-ki-am-edge-llm-embedded-2026.png', 'NVIDIA Jetson Edge', (156, 39, 176), 'chip'),
    ('ollama-vs-vllm-vs-lm-studio-2026.png', 'Ollama vLLM LM Studio', (156, 39, 176), 'server'),
    ('open-webui-ollama-betreiben-2026.png', 'Open WebUI Ollama', (156, 39, 176), 'neural'),
    ('tabbyapi-aphrodite-sglang-llm-server-2026.png', 'TabbyAPI Aphrodite', (156, 39, 176), 'server'),
    ('vllm-auf-eigener-gpu-aufsetzen.png', 'vLLM GPU Setup', (156, 39, 176), 'gpu'),
    ('vllm-multi-model-server-2026.png', 'vLLM Multi Model', (156, 39, 176), 'server'),
    ('ki-im-devops-einsatz-2026.png', 'KI im DevOps', (255, 152, 0), 'neural'),
    ('llm-sicherheit-prompt-injection-schutz-2026.png', 'LLM Sicherheit', (255, 152, 0), 'server'),
    ('ki-gestuetzte-code-reviews-praxis-2026.png', 'KI Code Reviews', (156, 39, 176), 'neural'),
    # Also fix openrouter
    ('openrouter-api-vs-eigene-gpu-kostenvergleich-2026.png', 'OpenRouter vs GPU', (156, 39, 176), 'cloud'),
]

print(f"=== Regenerating {len(targets)} KI/LLM hero images ===\n")
for filename, title, color, icon in targets:
    make_ai_hero(filename, title, color, icon)

print(f"\n=== DONE: {len(targets)} images regenerated ===")
