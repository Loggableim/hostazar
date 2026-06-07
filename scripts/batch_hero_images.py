#!/usr/bin/env python3
"""
Batch-Hero-Bild-Generation für fehlende Artikel-Bilder
Nutzt ComfyUI Queue (Port 8283) pro Artikel.
Format: slug|image_filename|title
"""
import subprocess, json, time, os, sys

COMFY_PORT = 8283
QUEUE_URL = f"http://localhost:{COMFY_PORT}/queue"

MISSING = [
    ("llm-lokal-hosten-2026", "llm-lokal-hosten-2026.png", "LLM lokal hosten 2026"),
    ("llama-cpp-cpu-vs-gpu-performance-2026", "llama-cpp-cpu-vs-gpu-performance-2026.png", "llama.cpp CPU vs GPU Performance 2026"),
    ("openrouter-api-vs-eigene-gpu-kostenvergleich-2026", "openrouter-api-vs-eigene-gpu-kostenvergleich-2026.png", "OpenRouter vs eigene GPU Kostenvergleich"),
    ("comfyui-auf-gpu-hosten", "comfyui-auf-gpu-hosten.png", "ComfyUI auf GPU hosten"),
    ("runpod-serverless-vs-dedicated-gpu-2026", "runpod-serverless-vs-dedicated-gpu-2026.png", "RunPod Serverless vs Dedicated GPU"),
    ("vast-ai-gpu-mieten-2026", "vast-ai-gpu-mieten-2026.png", "Vast.ai GPU mieten 2026"),
    ("mistral-modelle-lokal-hosten-2026", "mistral-modelle-lokal-hosten-2026.png", "Mistral LargeMixtral lokal hosten"),
    ("cuda-rocam-vulkan-lokale-llm-gpu-backend-vergleich-2026", "cuda-rocam-vulkan-lokale-llm-gpu-backend-vergleich-2026.png", "CUDA ROCm Vulkan GPU Backend Vergleich"),
    ("deepseek-r1-v3-lokal-hosten-2026", "deepseek-r1-v3-lokal-hosten-2026.png", "DeepSeek R1 V3 lokal hosten"),
    ("docker-llm-inference-container", "docker-llm-inference-container.png", "Docker Container LLM Inference"),
    ("gpu-fuer-ki-modelle-mieten-2026", "gpu-fuer-ki-modelle-mieten-2026.png", "GPU fuer KI Modelle mieten"),
    ("gpu-ram-manager-2026", "gpu-ram-manager-2026.png", "GPU RAM Manager VRAM Rechner"),
    ("llama-3-3-4-lokal-hosten-2026", "llama-3-3-4-lokal-hosten-2026.png", "Llama 33 4 lokal hosten"),
    ("llm-fine-tuning-runpod-vastai-2026", "llm-fine-tuning-runpod-vastai-2026.png", "LLM Fine Tuning LoRA QLoRA"),
    ("llm-frontends-vergleich-2026", "llm-frontends-vergleich-2026.png", "LLM Frontends Open WebUI Jan LobeChat"),
    ("nvidia-jetson-ki-am-edge-llm-embedded-2026", "nvidia-jetson-ki-am-edge-llm-embedded-2026.png", "NVIDIA Jetson KI am Edge LLM"),
    ("ollama-vs-vllm-vs-lm-studio-2026", "ollama-vs-vllm-vs-lm-studio-2026.png", "Ollama vs vLLM vs LM Studio"),
    ("open-webui-ollama-betreiben-2026", "open-webui-ollama-betreiben-2026.png", "Open WebUI mit Ollama betreiben"),
    ("quantisierte-modelle-gguf-awq-gptq-exl2-bitsandbytes-2026", "quantisierte-modelle-gguf-awq-gptq-exl2-bitsandbytes-2026.png", "Quantisierte Modelle GGUF AWQ GPTQ"),
    ("tabbyapi-aphrodite-sglang-llm-server-2026", "tabbyapi-aphrodite-sglang-llm-server-2026.png", "TabbyAPI Aphrodite SGLang LLM Server"),
    ("text-generation-webui-oobabooga-einrichten-2026", "text-generation-webui-oobabooga-einrichten-2026.png", "Text Generation WebUI oobabooga"),
    ("vllm-auf-eigener-gpu-aufsetzen", "vllm-auf-eigener-gpu-aufsetzen.png", "vLLM eigener GPU Production Ready"),
    ("vllm-multi-model-server-2026", "vllm-multi-model-server-2026.png", "KI Server mehrere Modelle vLLM"),
]

def make_prompt(title):
    """Generate a tech-style hero image prompt."""
    return f"tech blog hero image, {title}, dark background with purple/blue glow, server racks and GPU hardware, circuit board patterns, futuristic clean design, 16:9 aspect ratio, high quality, no text"

def submit_to_comfy(prompt, output_name):
    """Submit prompt to ComfyUI queue."""
    import urllib.request, json as j
    payload = j.dumps({"prompt": prompt, "output": output_name}).encode()
    try:
        req = urllib.request.Request(QUEUE_URL, data=payload, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=10)
        return j.loads(resp.read())
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

total = len(MISSING)
print(f"=== Batch Hero-Bild-Generation: {total} Bilder ===")
print(f"=== ComfyUI Queue: localhost:{COMFY_PORT} ===\n")

for i, (slug, img, title) in enumerate(MISSING, 1):
    prompt = make_prompt(title)
    print(f"[{i:2d}/{total}] {slug[:45]}")
    print(f"       -> {img}")
    result = submit_to_comfy(prompt, img)
    if result:
        print(f"       OK: {result.get('status', 'queued')}")
    time.sleep(0.5)

print(f"\n=== FERTIG: {total} Bilder in Queue ===")
