#!/usr/bin/env python3
"""Generate 3 AI hero images for hostazar.com via local ComfyUI API (SDXL RealVisXL)."""
import json, urllib.request, time, os, sys
from PIL import Image, ImageDraw, ImageFont

COMFY_URL = "http://127.0.0.1:8189"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def submit_prompt(workflow):
    data = json.dumps({"prompt": workflow, "client_id": "hostazar-hero-gen"}).encode()
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp["prompt_id"]

def poll_history(pid, timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        try:
            req = urllib.request.Request(f"{COMFY_URL}/history/{pid}")
            hist = json.loads(urllib.request.urlopen(req).read())
            if pid in hist:
                entry = hist[pid]
                status = entry.get("status", {})
                if status.get("completed") or status.get("status_str") == "success":
                    return entry
                if status.get("status_str") == "error":
                    msgs = status.get("messages", [])
                    for mt, m in msgs:
                        if mt == "execution_error":
                            print(f"  ERROR: {m.get('exception_message', 'unknown')}")
                    return None
        except Exception:
            pass
        time.sleep(2)
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

def add_text_overlay(image_path, title_text, category):
    """Add category-colored text overlay in Pop-Tech style."""
    W, H = 1200, 630
    img = Image.open(image_path).convert("RGB").resize((W, H), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    
    # Semi-transparent bottom bar
    draw.rectangle([(0, H-90), (W, H)], fill=(0, 0, 0, 180))
    
    # Category color accent
    cat_colors = {"gaming": "#4CAF50", "webhosting": "#2196F3", "devops": "#FF9800"}
    color = cat_colors.get(category, "#9C27B0")
    draw.rectangle([(0, H-90), (8, H)], fill=color)
    
    # Find font
    font_paths = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 28)
                break
            except:
                pass
    if font is None:
        font = ImageFont.load_default()
    
    # Draw text
    draw.text((24, H-70), title_text, fill=(255, 255, 255), font=font)
    
    # hostazar.com watermark
    font_small = ImageFont.truetype(font_paths[0], 14) if os.path.exists(font_paths[0]) and font else font
    draw.text((W-180, H-30), "hostazar.com", fill=(255, 255, 255, 120), font=font_small)
    
    img.save(image_path, "PNG", quality=92)

# Build SDXL workflows
def make_workflow_style(prompt, neg_prompt="text, watermark, blurry, low quality, distorted"):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "RealVisXL_V4.0.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg_prompt, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1216, "height": 640, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": 42, "control_after_generate": "randomize",
            "steps": 25, "cfg": 7.0, "sampler_name": "dpmpp_2m", "scheduler": "karras",
            "denoise": 1.0, "model": ["1", 0], "positive": ["2", 0],
            "negative": ["3", 0], "latent_image": ["4", 0]
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "hero_output", "images": ["6", 0]}}
    }

PROMPTS = [
    {
        "name": "hero-ai-gaming",
        "category": "gaming",
        "title": "Gameserver Hosting Guide 2026",
        "prompt": "Epic cinematic wide shot of a neon-lit server room with glowing game controllers and holographic game world projections, cyberpunk style, dark purple and green atmosphere, volumetric lighting, ray tracing, highly detailed, 8k, concept art, wide angle 16:9, realistic textures, mist, glowing elements, blade runner aesthetic, game server infrastructure",
        "neg": "text, watermark, signature, blurry, low quality, distorted, ugly, deformed, photorealistic, grainy, noisy, oversaturated, cartoon"
    },
    {
        "name": "hero-ai-webhosting",
        "category": "webhosting",
        "title": "Webhosting & Cloud Portal 2026",
        "prompt": "Ethereal cinematic wide shot of floating glowing servers connected by light beams in a vast cloud-filled digital space, blue and purple aurora lighting, volumetric clouds, data streams flowing like rivers of light, hyperrealistic, 8k, wide angle 16:9, dreamy atmosphere, glowing network connections, floating data particles, global network visualization, soft lighting",
        "neg": "text, watermark, signature, blurry, low quality, distorted, ugly, deformed, cartoon, oversaturated, grainy"
    },
    {
        "name": "hero-ai-devops",
        "category": "devops",
        "title": "DevOps & Server Automation 2026",
        "prompt": "Cinematic shot of a futuristic data center with holographic terminal screens showing code, pipeline diagrams and server metrics floating in orange and amber light, warm dark atmosphere, technical aesthetic, volumetric fog, glowing elements, hexagonal data patterns, wide angle 16:9, hyperrealistic, 8k, blade runner inspired, industrial tech, cables and server racks fading into darkness",
        "neg": "text, watermark, signature, blurry, low quality, distorted, ugly, deformed, cartoon, oversaturated, cartoonish"
    }
]

if __name__ == "__main__":
    for p in PROMPTS:
        print(f"Generating {p['name']}...")
        workflow = make_workflow_style(p["prompt"], p["neg"])
        
        try:
            pid = submit_prompt(workflow)
            print(f"  Prompt: {pid}")
            
            hist = poll_history(pid, timeout=180)
            if hist:
                fn, sub = get_latest_output(hist)
                if fn:
                    output_path = os.path.join(OUTPUT_DIR, f"{p['name']}.png")
                    downloaded = download_image(fn, sub, output_path)
                    add_text_overlay(downloaded, p["title"], p["category"])
                    size = os.path.getsize(downloaded)
                    print(f"  OK: {downloaded} ({size/1024:.0f} KB)")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\nDone! 3 AI Hero-Bilder generiert.")
