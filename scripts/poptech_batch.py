#!/usr/bin/env python3
"""
Pop-Tech Kacheln Batch Generator für hostazar.com
Generiert alle Artikel-Bilder im Pop-Tech Kacheln Stil via ComfyUI SDXL + Pillow-Textoverlay.
"""
import json, urllib.request, time, os, sys
from PIL import Image, ImageDraw, ImageFont

# Konfiguration
COMFY_URL = "http://127.0.0.1:8188"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Artikel-Definitionen
ARTICLES = [
    {
        "slug": "vps-absichern-2026",
        "title": "VPS absichern 2026",
        "category": "devops",
        "color": "#FF9800",
        "icon_prompt": "a shield with a lock inside, flat bold vector icon, white silhouette, minimalist, centered on dark background, security symbol, no details, clean shape"
    },
    {
        "slug": "docker-compose-vps-guide",
        "title": "Docker Compose auf dem VPS",
        "category": "devops",
        "color": "#FF9800",
        "icon_prompt": "three stacked server boxes or containers, flat bold vector icon, white silhouette, minimalist, centered on dark background, docker style, no details"
    },
    {
        "slug": "valheim-server-vps-mieten-2026",
        "title": "Valheim Server mieten",
        "category": "gaming",
        "color": "#4CAF50",
        "icon_prompt": "a viking helmet with horns, flat bold vector icon, white silhouette, minimalist, centered on dark background, norse symbol, no details"
    },
    {
        "slug": "webhosting-anbieter-vergleich-2026",
        "title": "Webhosting-Anbieter 2026",
        "category": "webhosting",
        "color": "#2196F3",
        "icon_prompt": "a globe or world wide web symbol, flat bold vector icon, white silhouette, minimalist, centered on dark background, internet, clean shape"
    },
    {
        "slug": "minecraft-server-vergleich-2026",
        "title": "Minecraft Server",
        "category": "gaming",
        "color": "#4CAF50",
        "icon_prompt": "a pickaxe crossed with a sword, flat bold vector icon, white silhouette, minimalist, centered on dark background, minecraft style, no details"
    },
    {
        "slug": "gameserver-mieten-guide",
        "title": "Gameserver mieten",
        "category": "gaming",
        "color": "#4CAF50",
        "icon_prompt": "a game controller or gamepad, flat bold vector icon, white silhouette, minimalist, centered on dark background, gaming symbol, no details"
    },
    {
        "slug": "webhosting-vserver-vergleich",
        "title": "Webhosting vs VServer",
        "category": "webhosting",
        "color": "#2196F3",
        "icon_prompt": "a balance scale or two servers side by side, flat bold vector icon, white silhouette, minimalist, centered on dark background, comparison symbol"
    },
    {
        "slug": "devops-tools-2024",
        "title": "DevOps Tools 2024",
        "category": "devops",
        "color": "#FF9800",
        "icon_prompt": "a gear or wrench crossed with a terminal bracket, flat bold vector icon, white silhouette, minimalist, centered on dark background, tools symbol"
    },
]

CATEGORY_COLORS = {
    "gaming": ("#4CAF50", "#81C784"),
    "webhosting": ("#2196F3", "#64B5F6"),
    "devops": ("#FF9800", "#FFB74D"),
}

def parse_hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def hex_to_rgb(h):
    return parse_hex(h)

def submit_sdxl_prompt(prompt_text, width=1216, height=640):
    """Submit SDXL prompt to ComfyUI and return prompt_id."""
    workflow = {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["1", 1]
            }
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "text, watermark, signature, blurry, low quality, distorted, ugly, deformed, photorealistic, gradient, detailed, noisy, complex",
                "clip": ["1", 1]
            }
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            }
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "seed": 42,
                "control_after_generate": "randomize",
                "steps": 25,
                "cfg": 7.0,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0]
            }
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2]
            }
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "poptech_temp",
                "images": ["6", 0]
            }
        }
    }
    payload = json.dumps({"prompt": workflow, "client_id": "hostazar-poptech"}).encode()
    req = urllib.request.Request(
        f"{COMFY_URL}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    pid = resp["prompt_id"]
    print(f"  Prompt submitted: {pid}")
    return pid

def poll_history(prompt_id, timeout=180):
    """Poll ComfyUI history until prompt completes."""
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
        except Exception as e:
            pass  # still running
        time.sleep(3)
    print(f"  TIMEOUT after {timeout}s")
    return None

def download_image(filename, subfolder="", output_path=None):
    """Download a generated image from ComfyUI output."""
    params = urllib.parse.urlencode({
        "filename": filename,
        "subfolder": subfolder,
        "type": "output"
    })
    url = f"{COMFY_URL}/view?{params}"
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, filename)
    urllib.request.urlretrieve(url, output_path)
    return output_path

def get_latest_output(history_entry):
    """Get the output image filename from a history entry."""
    outputs = history_entry.get("outputs", {})
    for node_id, node_out in outputs.items():
        images = node_out.get("images", [])
        if images:
            img = images[0]
            return img["filename"], img.get("subfolder", "")
    return None, None

def compose_poptech(icon_path, output_path, title_text, category):
    """Compose the final Pop-Tech Kacheln image with background, icon, and text."""
    # Size
    W, H = 1200, 630

    # Colors
    if category in CATEGORY_COLORS:
        left_color_hex, left_color_light = CATEGORY_COLORS[category]
    else:
        left_color_hex, left_color_light = "#9C27B0", "#CE93D8"
    purple = "#9C27B0"
    left_rgb = hex_to_rgb(left_color_hex)
    purple_rgb = hex_to_rgb(purple)

    # Create canvas
    canvas = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(canvas)

    # Fill left half with category color
    draw.rectangle([(0, 0), (W // 2, H)], fill=left_rgb)
    # Fill right half with purple
    draw.rectangle([(W // 2, 0), (W, H)], fill=purple_rgb)

    # Add a subtle diagonal overlap / transition line (like a zigzag or angled cut)
    # Simple 5px white/light divider line at the center
    for x_offset in range(-2, 3):
        draw.line([(W // 2 + x_offset, 0), (W // 2 + x_offset, H)], fill=(255, 255, 255), width=1)

    # Load and process icon
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        # Scale icon to fit nicely
        icon_size = 280  # max width/height for icon
        icon.thumbnail((icon_size, icon_size), Image.LANCZOS)

        # Create white silhouette from the icon
        # Convert to grayscale, threshold to get the white shape
        gray = icon.convert("L")
        # Create a mask where white/light pixels become opaque
        mask = gray.point(lambda x: 255 if x > 100 else 0)
        
        # Create a white shape
        white_shape = Image.new("RGBA", icon.size, (255, 255, 255, 0))
        white_shape.putalpha(mask)

        # Paste icon centered
        icon_x = (W - icon.size[0]) // 2
        icon_y = (H - icon.size[1]) // 2 - 40  # offset up to leave room for text
        canvas.paste(white_shape, (icon_x, icon_y), white_shape)

    # Add text - title
    title_text_short = title_text
    # Try to find a font
    font_paths = [
        "C:/Windows/Fonts/seguiemj.ttf",  # Segoe UI Emoji
        "C:/Windows/Fonts/segoeuib.ttf",  # Segoe UI Bold
        "C:/Windows/Fonts/segoeui.ttf",   # Segoe UI
        "C:/Windows/Fonts/arialbd.ttf",   # Arial Bold
        "C:/Windows/Fonts/arial.ttf",     # Arial
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 32)
                break
            except Exception:
                continue
    if font is None:
        font = ImageFont.load_default()

    # Draw text centered below icon
    bbox = draw.textbbox((0, 0), title_text_short, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (W - tw) // 2
    ty = (H // 2) + 120  # below the icon area

    # Text shadow for readability
    draw.text((tx + 1, ty + 1), title_text_short, fill=(0, 0, 0, 100), font=font)
    draw.text((tx, ty), title_text_short, fill=(255, 255, 255), font=font)

    # Add category badge top-left
    badge_text = category.upper()
    bbox2 = draw.textbbox((0, 0), badge_text, font=font)
    bw = bbox2[2] - bbox2[0]
    badge_rect = (20, 20, 30 + bw, 46)
    draw.rectangle(badge_rect, fill=left_rgb)
    draw.text((25, 23), badge_text, fill=(255, 255, 255), font=font)

    # Save
    canvas.save(output_path, "PNG", quality=95)
    print(f"  Composed: {os.path.basename(output_path)}")
    return output_path

def generate_icon_sdxl(icon_prompt, seed=None):
    """Generate just the icon as white silhouette on dark bg using SDXL."""
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
        "7": {"class_type": "SaveImage", "inputs": {"filename_prefix": "icon_temp", "images": ["6", 0]}}
    }
    
    payload = json.dumps({"prompt": workflow, "client_id": "hostazar-icons"}).encode()
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=payload, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req).read())
    pid = resp["prompt_id"]
    print(f"  Icon prompt: {pid}")
    return pid

def main():
    print("=== Pop-Tech Kacheln Batch Generator ===\n")
    
    # Step 1: Generate icons with SDXL
    icon_files = {}
    for art in ARTICLES:
        slug = art["slug"]
        icon_path = os.path.join(OUTPUT_DIR, f"icon_{slug}.png")
        if os.path.exists(icon_path) and os.path.getsize(icon_path) > 1000:
            print(f"  [SKIP] Icon exists for {slug}")
            icon_files[slug] = icon_path
            continue
        
        print(f"\n[ICON] {slug} — {art['icon_prompt'][:60]}...")
        pid = generate_icon_sdxl(art["icon_prompt"])
        hist = poll_history(pid)
        if hist:
            fn, sub = get_latest_output(hist)
            if fn:
                downloaded = download_image(fn, sub, icon_path)
                print(f"  Saved icon: {downloaded}")
                icon_files[slug] = icon_path
        # Small delay between prompts
        time.sleep(2)
    
    # Step 2: Compose final images
    print("\n=== Composing final images ===\n")
    for art in ARTICLES:
        slug = art["slug"]
        output_path = os.path.join(OUTPUT_DIR, f"{slug}.png")
        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            print(f"  [SKIP] Final exists for {slug}")
            continue
        
        icon_path = icon_files.get(slug)
        if icon_path and os.path.exists(icon_path):
            print(f"\n[COMPOSE] {slug} — {art['title']}")
            compose_poptech(icon_path, output_path, art["title"], art["category"])
        else:
            print(f"\n[COMPOSE] {slug} — no icon, generating without it")
            # Generate without icon
            W, H = 1200, 630
            left_rgb = hex_to_rgb(ARTICLES[0]["color"])  # fallback
            for a in ARTICLES:
                if a["slug"] == slug:
                    if a["category"] in CATEGORY_COLORS:
                        left_rgb = hex_to_rgb(CATEGORY_COLORS[a["category"]][0])
                    break
            purple_rgb = hex_to_rgb("#9C27B0")
            canvas = Image.new("RGB", (W, H))
            draw = ImageDraw.Draw(canvas)
            draw.rectangle([(0, 0), (W // 2, H)], fill=left_rgb)
            draw.rectangle([(W // 2, 0), (W, H)], fill=purple_rgb)
            canvas.save(output_path, "PNG", quality=95)
            print(f"  Saved fallback: {os.path.basename(output_path)}")
    
    print("\n=== Done ===")

if __name__ == "__main__":
    main()
