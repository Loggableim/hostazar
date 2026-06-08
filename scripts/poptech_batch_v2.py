#!/usr/bin/env python3
"""
Pop-Tech Kacheln Batch Generator v2 — für KI/LLM + restliche Fehlende Artikel.
"""
import json, urllib.request, time, os, sys
from PIL import Image, ImageDraw, ImageFont

COMFY_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

CATEGORY_COLORS = {
    "gaming": ("#4CAF50", "#81C784"),
    "webhosting": ("#2196F3", "#64B5F6"),
    "devops": ("#FF9800", "#FFB74D"),
    "ki-llm": ("#9C27B0", "#CE93D8"),
}

# Alle fehlenden Artikel mit ihren Kategorien und Icon-Prompts
ARTICLES = [
    # KI & LLM (Purple)
    {"slug": "comfyui-auf-gpu-hosten", "title": "ComfyUI auf GPU hosten", "category": "ki-llm", "icon": "a GPU graphics card with a paint palette, flat bold vector icon, white silhouette, minimalist, centered, no details"},
    {"slug": "cuda-rocam-vulkan-lokale-llm-gpu-backend-vergleich-2026", "title": "CUDA, ROCm, Vulkan GPU-Vergleich", "category": "ki-llm", "icon": "three interconnected gear chips, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "deepseek-r1-v3-lokal-hosten-2026", "title": "DeepSeek R1/V3 lokal hosten", "category": "ki-llm", "icon": "a brain with a server chip inside, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "docker-llm-inference-container", "title": "Docker LLM Inference Container", "category": "ki-llm", "icon": "a whale with a neural network node, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "gpu-fuer-ki-modelle-mieten-2026", "title": "GPU für KI-Modelle mieten", "category": "ki-llm", "icon": "a stack of GPU cards with dollar sign, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "gpu-ram-manager-2026", "title": "GPU-RAM-Manager 2026", "category": "ki-llm", "icon": "a memory chip with a gauge meter, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "ki-gestuetzte-code-reviews-praxis-2026", "title": "KI Code-Reviews in der Praxis", "category": "ki-llm", "icon": "a code bracket with a magnifying glass, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "ki-im-devops-einsatz-2026", "title": "KI im DevOps-Einsatz", "category": "ki-llm", "icon": "a DevOps infinity loop with a brain, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "llama-3-3-4-lokal-hosten-2026", "title": "Llama 3.3 & Llama 4 lokal", "category": "ki-llm", "icon": "a llama silhouette inside a server rack, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "llama-cpp-cpu-vs-gpu-performance-2026", "title": "llama.cpp CPU vs GPU", "category": "ki-llm", "icon": "a processor chip split in half, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "llm-fine-tuning-runpod-vastai-2026", "title": "LLM Fine-Tuning auf GPUs", "category": "ki-llm", "icon": "a tuning dial with AI nodes, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "llm-frontends-vergleich-2026", "title": "LLM-Frontends im Vergleich", "category": "ki-llm", "icon": "a monitor with chat bubbles, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "llm-lokal-hosten-2026", "title": "LLM lokal hosten 2026", "category": "ki-llm", "icon": "a server tower with AI brain, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "llm-sicherheit-prompt-injection-schutz-2026", "title": "LLM Sicherheit", "category": "ki-llm", "icon": "a shield with a brain inside, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "mistral-modelle-lokal-hosten-2026", "title": "Mistral Modelle lokal hosten", "category": "ki-llm", "icon": "a mist or cloud with AI nodes, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "nvidia-jetson-ki-am-edge-llm-embedded-2026", "title": "NVIDIA Jetson KI am Edge", "category": "ki-llm", "icon": "a small embedded chip with AI symbol, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "ollama-vs-vllm-vs-lm-studio-2026", "title": "Ollama vs vLLM vs LM Studio", "category": "ki-llm", "icon": "three server towers side by side, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "open-webui-ollama-betreiben-2026", "title": "Open WebUI mit Ollama", "category": "ki-llm", "icon": "a web browser with a chat AI interface, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "openrouter-api-vs-eigene-gpu-kostenvergleich-2026", "title": "OpenRouter vs eigene GPU", "category": "devops", "icon": "a balance scale with API and GPU, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "runpod-serverless-vs-dedicated-gpu-2026", "title": "RunPod Serverless vs GPU", "category": "ki-llm", "icon": "a cloud with a GPU card inside, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "tabbyapi-aphrodite-sglang-llm-server-2026", "title": "LLM-Server Vergleich", "category": "ki-llm", "icon": "three API server nodes connected, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "text-generation-webui-oobabooga-einrichten-2026", "title": "Text Generation WebUI", "category": "ki-llm", "icon": "a web interface with text generation, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "vast-ai-gpu-mieten-2026", "title": "Vast.ai GPU mieten", "category": "ki-llm", "icon": "a world globe with GPU cards, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "vllm-auf-eigener-gpu-aufsetzen", "title": "vLLM auf eigener GPU", "category": "ki-llm", "icon": "a GPU with a speed rocket, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "vllm-multi-model-server-2026", "title": "Multi-Model Server", "category": "ki-llm", "icon": "multiple model layers stacked, flat bold vector icon, white silhouette, minimalist, no details"},
    # Nicht KI/LLM aber auch fehlend:
    {"slug": "beste-gaming-monitore-2026", "title": "Beste Gaming-Monitore 2026", "category": "gaming", "icon": "a monitor screen with gamepad, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "cloud-vs-dedicated-server-2026", "title": "Cloud vs Dedicated Server", "category": "webhosting", "icon": "two server racks compared side by side, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "deep-rock-galactic-server-mieten-2026", "title": "Deep Rock Galactic Server", "category": "gaming", "icon": "a dwarf miner pickaxe crossed with laser, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "escape-from-tarkov-server-hosten-2026", "title": "Escape from Tarkov Server", "category": "gaming", "icon": "a tactical helmet with night vision, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "factorio-server-hosting-2026", "title": "Factorio Server hosten", "category": "gaming", "icon": "a factory gear with conveyor belt, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "gaestebeitrag-finanz-junkie-server-kosten-investor-guide", "title": "Serverkosten Investor-Guide", "category": "devops", "icon": "a chart arrow going up with server, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "gaming-pc-selbst-bauen-2026", "title": "Gaming-PC selbst bauen", "category": "gaming", "icon": "a PC tower with tools crossed, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "helldivers-2-server-hosten-2026", "title": "Helldivers 2 Server", "category": "gaming", "icon": "a helldiver helmet arrow, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "lethal-company-server-mieten-2026", "title": "Lethal Company Server", "category": "gaming", "icon": "a scarecrow or hazard symbol, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "managed-wordpress-hosting-vergleich-2026", "title": "Managed WordPress 2026", "category": "webhosting", "icon": "a WordPress logo circle simplified, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "phasmophobia-server-hosten-2026", "title": "Phasmophobia Server", "category": "gaming", "icon": "a ghost silhouette with EMF reader, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "pubg-server-mieten-2026", "title": "PUBG Server mieten", "category": "gaming", "icon": "a pan crossed with a rifle, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "quantisierte-modelle-gguf-awq-gptq-exl2-bitsandbytes-2026", "title": "Quantisierte Modelle 2026", "category": "devops", "icon": "a compression icon with bars, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "redis-cache-vps-einrichten-2026", "title": "Redis Cache auf VPS", "category": "devops", "icon": "a lightning bolt inside a database cylinder, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "remote-work-tirol", "title": "Remote Work Tirol", "category": "webhosting", "icon": "a mountain peak with WiFi signal, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "steam-deck-vs-asus-rog-ally-vs-lenovo-legion-go-2026", "title": "Handheld-Vergleich 2026", "category": "gaming", "icon": "three handheld consoles side by side, flat bold vector icon, white silhouette, minimalist, no details"},
    {"slug": "webhosting-sicherheit-ddos-schutz-waf-2026", "title": "Webhosting-Sicherheit", "category": "webhosting", "icon": "a shield with globe and lock, flat bold vector icon, white silhouette, minimalist, no details"},
]

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def generate_icon_sdxl(icon_prompt, seed=None):
    """Generate icon as white silhouette on dark bg using SDXL."""
    prompt = f"flat vector silhouette icon of {icon_prompt}, solid white shape on solid dark grey background #222222, no details inside the shape, bold clean outline, minimalist icon design, no text, no gradient, high contrast, centered composition"
    neg = "text, watermark, signature, blurry, low quality, photorealistic, 3d, gradient, complex details, multiple objects, realistic, shadow"
    
    workflow = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": seed if seed else 42,
            "control_after_generate": "randomize",
            "steps": 25, "cfg": 7.0, "sampler_name": "dpmpp_2m", "scheduler": "karras",
            "denoise": 1.0, "model": ["1", 0], "positive": ["2", 0],
            "negative": ["3", 0], "latent_image": ["4", 0]
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "icon_batch", "images": ["6", 0]}}
    }
    
    payload = json.dumps({"prompt": workflow, "client_id": "hostazar-icons-v2"}).encode()
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=payload, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp["prompt_id"]

def poll_history(prompt_id, timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"{COMFY_URL}/history/{prompt_id}")
            hist = json.loads(urllib.request.urlopen(req).read())
            if prompt_id in hist:
                entry = hist[prompt_id]
                status = entry.get("status", {})
                if status.get("completed") or status.get("status_str") == "success":
                    return entry
                if status.get("status_str") == "error":
                    msgs = status.get("messages", [])
                    for mt, m in msgs:
                        if mt == "execution_error":
                            print(f"  ERROR: {m.get('exception_message', 'unknown')}")
                    return None
        except:
            pass
        time.sleep(3)
    print(f"  TIMEOUT after {timeout}s")
    return None

def download_image(filename, subfolder="", output_path=None):
    params = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": "output"})
    url = f"{COMFY_URL}/view?{params}"
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, filename)
    urllib.request.urlretrieve(url, output_path)
    return output_path

def get_latest_output(history_entry):
    outputs = history_entry.get("outputs", {})
    for node_id, node_out in outputs.items():
        images = node_out.get("images", [])
        if images:
            img = images[0]
            return img["filename"], img.get("subfolder", "")
    return None, None

def compose_poptech(icon_path, output_path, title_text, category):
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

    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        icon_size = 280
        icon.thumbnail((icon_size, icon_size), Image.LANCZOS)
        gray = icon.convert("L")
        mask = gray.point(lambda x: 255 if x > 100 else 0)
        white_shape = Image.new("RGBA", icon.size, (255, 255, 255, 0))
        white_shape.putalpha(mask)
        icon_x = (W - icon.size[0]) // 2
        icon_y = (H - icon.size[1]) // 2 - 40
        canvas.paste(white_shape, (icon_x, icon_y), white_shape)

    font = None
    for fp in ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arialbd.ttf"]:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 30)
                break
            except:
                continue
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), title_text, font=font)
    tw = bbox[2] - bbox[0]
    ty = (H // 2) + 130
    tx = (W - tw) // 2
    draw.text((tx + 1, ty + 1), title_text, fill=(0, 0, 0, 100), font=font)
    draw.text((tx, ty), title_text, fill=(255, 255, 255), font=font)

    canvas.save(output_path, "PNG", quality=95)
    print(f"  Composed: {os.path.basename(output_path)}")

def main():
    logpath = os.path.join(os.path.dirname(__file__), "..", "poptech_batch_v2.log")
    log = open(logpath, "a", encoding="utf-8")
    
    total = len(ARTICLES)
    done = 0
    skipped = 0
    
    for i, art in enumerate(ARTICLES):
        slug = art["slug"]
        final_path = os.path.join(OUTPUT_DIR, f"{slug}.png")
        icon_path = os.path.join(OUTPUT_DIR, f"icon_{slug}.png")
        
        # Skip if final image already exists
        if os.path.exists(final_path) and os.path.getsize(final_path) > 5000:
            log.write(f"[SKIP] {slug} — already exists\n")
            skipped += 1
            continue
        
        # Generate icon
        if not (os.path.exists(icon_path) and os.path.getsize(icon_path) > 5000):
            print(f"\n[{i+1}/{total}] ICON {slug}...")
            log.write(f"[ICON] {slug}\n")
            pid = generate_icon_sdxl(art["icon"])
            hist = poll_history(pid)
            if hist:
                fn, sub = get_latest_output(hist)
                if fn:
                    download_image(fn, sub, icon_path)
                    print(f"  Saved icon: {os.path.basename(icon_path)}")
                    log.write(f"  Icon OK: {slug}\n")
        else:
            print(f"\n[{i+1}/{total}] ICON {slug} — cached")
        
        # Compose
        if os.path.exists(icon_path) and os.path.getsize(icon_path) > 5000:
            print(f"[COMPOSE] {slug} — {art['title']}")
            log.write(f"[COMPOSE] {slug}\n")
            compose_poptech(icon_path, final_path, art["title"], art["category"])
            done += 1
        else:
            print(f"[FAIL] {slug} — no icon")
            log.write(f"[FAIL] {slug} — no icon\n")
    
    log.write(f"\n=== DONE: {done} generated, {skipped} skipped, {total} total ===\n")
    log.close()
    print(f"\n=== DONE: {done} generated, {skipped} skipped, {total} total ===")

if __name__ == "__main__":
    main()
