#!/usr/bin/env python3
"""Generate 3 style variants of the SAME Minecraft Server theme: Sketch, Realism, PopArt."""
import json, urllib.request, time, os
from PIL import Image, ImageDraw, ImageFont

COMFY_URL = "http://127.0.0.1:8189"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_PROMPT = "A powerful gaming server computer with glowing purple lights, Minecraft block shadows floating above it, server rack in background, dramatic lighting, cinematic composition, 16:9 wide angle"

def submit_prompt(workflow):
    data = json.dumps({"prompt": workflow, "client_id": "hostazar-hero-gen"}).encode()
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp["prompt_id"]

def poll_history(pid, timeout=180):
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
        except:
            pass
        time.sleep(2)
    print(f"  TIMEOUT")
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

def make_workflow(base_prompt, style_suffix, neg_prompt):
    full_prompt = f"{base_prompt}, {style_suffix}"
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "RealVisXL_V4.0.safetensors"}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": full_prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg_prompt, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1216, "height": 640, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": 42, "control_after_generate": "randomize",
            "steps": 28, "cfg": 7.0, "sampler_name": "dpmpp_2m", "scheduler": "karras",
            "denoise": 1.0, "model": ["1", 0], "positive": ["2", 0],
            "negative": ["3", 0], "latent_image": ["4", 0]
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "style_out", "images": ["6", 0]}}
    }

STYLES = [
    {
        "name": "hero-skizze-minecraft",
        "label": "Skizze",
        "style": "line art sketch, black and white charcoal drawing, rough pencil strokes, unfinished sketch style, hand-drawn, crosshatching, minimalist linework, concept art sketch, monochrome",
        "neg": "color, painting, photorealistic, 3d render, shading, gradient, detailed texture, blur, soft shadows, oil paint, watercolor"
    },
    {
        "name": "hero-realism-minecraft",
        "label": "Realism",
        "style": "photorealistic, hyperrealistic, 8k uhd, detailed texture, subsurface scattering, realistic lighting, sharp focus, depth of field, professional photography, cinema quality, highly detailed, ultra realistic",
        "neg": "painting, sketch, cartoon, anime, illustration, digital art, 3d render, cgi, low quality, blurry, abstract, pop art"
    },
    {
        "name": "hero-popart-minecraft",
        "label": "Pop Art",
        "style": "andy warhol pop art style, bold vibrant colors, high contrast, comic book style, ben-day dots, screen printing aesthetic, bright neon colors, thick black outlines, half-tone patterns, retro pop art, Roy Lichtenstein style",
        "neg": "photorealistic, sketch, black and white, monochrome, soft, muted colors, blurry, gradient, smooth shading, realistic texture"
    }
]

if __name__ == "__main__":
    for s in STYLES:
        print(f"Generating '{s['label']}' -> {s['name']}")
        wf = make_workflow(BASE_PROMPT, s['style'], s['neg'])
        try:
            pid = submit_prompt(wf)
            print(f"  Prompt: {pid}")
            hist = poll_history(pid, timeout=180)
            if hist:
                fn, sub = get_latest_output(hist)
                if fn:
                    out = os.path.join(OUTPUT_DIR, f"{s['name']}.png")
                    download_image(fn, sub, out)
                    print(f"  OK: {out} ({os.path.getsize(out)/1024:.0f} KB)")
        except Exception as e:
            print(f"  FAIL: {e}")
    
    print("\n3 Stilvarianten fertig!")
