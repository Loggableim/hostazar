#!/usr/bin/env python3
"""Final pass: regenerate remaining 42 empty articles with individual calls."""
import json, urllib.request, time, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, "artikel")
KEY = re.search(r"MINIMAX_API_KEY=(\S+)", open("C:/sidekick/home/.env").read()).group(1)

SLUGS = "cloud-gpu-kosten-vergleich-2026 cloud-hosting-vs-shared-hosting contabo-vps-erfahrungen-2026 cuda-rocam-vulkan-lokale-llm-gpu-backend-vergleich-2026 deep-rock-galactic-server-mieten-2026 discord-bot-vps-hosten-2026 docker-compose-vps-guide domain-kaufen-einrichten-2026 enshrouded-server-hosting-2026 escape-from-tarkov-server-hosten-2026 gaming-pc-selbst-bauen-2026 github-actions-ci-cd-pipeline-2026 gitops-argocd-einrichten grounded-server-hosting helldivers-2-server-hosten-2026 helm-charts-kubernetes-guide-2026 hetzner-cloud-vs-dediziert-vergleich-2026 hugo-astro-static-site-vergleich-2026 k3s-kubernetes-vps-2026 lemp-stack-vps-einrichten-2026 llama-cpp-cpu-vs-gpu-performance-2026 llm-fine-tuning-runpod-vastai-2026 llm-sicherheit-prompt-injection-schutz-2026 managed-wordpress-hosting-vergleich-2026 minio-object-storage-selbst-hosten-2026 n8n-automation-server netcup-vps-erfahrungen-2026 nightingale-server-hosting nvidia-jetson-ki-am-edge-llm-embedded-2026 openrouter-api-vs-eigene-gpu-kostenvergleich-2026 plausible-analytics-vps-2026 project-zomboid-server-hosting-2026 runpod-serverless-vs-dedicated-gpu-2026 scum-server-mieten smalland-server-hosting sons-of-the-forest-server text-generation-webui-oobabooga-einrichten-2026 uptime-kuma-monitoring-einrichten-2026 vaultwarden-passwort-manager-selbst-hosten-2026 vps-anbieter-vergleich-2026 webseite-geschwindigkeit-optimieren-2026 wireguard-vpn-server".split()

TITLES = {}
for slug in SLUGS:
    fp = os.path.join(ARTIKEL_DIR, f"{slug}.html")
    if os.path.exists(fp):
        with open(fp) as f:
            t = re.search(r"<title>(.*?)\s*\|", f.read())
            TITLES[slug] = t.group(1).strip() if t else slug

print(f"Remaining: {len(SLUGS)}", flush=True)
DONE = 0

for i, slug in enumerate(SLUGS, 1):
    title = TITLES.get(slug, slug)
    prompt = f"Schreibe deutschen SEO-Content für: {title}. 8-12 H2, 3-5 Absätze pro H2, Tabellen, Code. NUR HTML."
    
    data = json.dumps({"model":"MiniMax-M3","messages":[
        {"role":"system","content":"Du bist SEO-Content-Autor für hostazar.com. NUR HTML, KEINE Erklärungen."},
        {"role":"user","content":prompt}
    ],"max_tokens":4096,"temperature":0.7}).encode()
    
    req = urllib.request.Request("https://api.minimax.io/v1/chat/completions", data=data,
        headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
    
    sys.stdout.write(f"[{i}/{len(SLUGS)}] {slug}... ")
    sys.stdout.flush()
    t0 = time.time()
    
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=300).read())
        reply = resp.get("choices",[{}])[0].get("message",{}).get("content","")
        reply = re.sub(r"<think>.*?</think>|```html\n?|```", "", reply, flags=re.DOTALL).strip()
        
        h2_start = reply.find("<h2")
        if h2_start >= 0:
            content = reply[h2_start:]
            if len(content) > 300:
                with open(os.path.join(ARTIKEL_DIR, f"{slug}.html")) as f: shell = f.read()
                new = re.sub(r"(<h1[^>]*>.*?</h1>)", r"\1\n"+content, shell, count=1, flags=re.DOTALL)
                with open(os.path.join(ARTIKEL_DIR, f"{slug}.html"), "w") as f: f.write(new)
                DONE += 1
                print(f"✅ ({time.time()-t0:.0f}s)", flush=True)
                time.sleep(max(1, 65 - (time.time()-t0)))
                continue
        print(f"⚠️ zu kurz ({time.time()-t0:.0f}s)", flush=True)
    except Exception as e:
        print(f"❌ {e} ({time.time()-t0:.0f}s)", flush=True)
    
    time.sleep(65)

ok = 0
for slug in SLUGS:
    with open(os.path.join(ARTIKEL_DIR, f"{slug}.html")) as f:
        c = f.read()
    if len(re.findall(r"<h2[^>]*>", c)) >= 3:
        ok += 1

print(f"\n=== FINAL PASS: {DONE} regeneriert | OK: {ok}/{len(SLUGS)} ===", flush=True)
