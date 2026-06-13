#!/usr/bin/env python3
"""Content regen via MiniMax-M3 OpenAI endpoint - robust parsing."""
import json, urllib.request, time, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIKEL_DIR = os.path.join(REPO, "artikel")

with open("C:/sidekick/home/.env") as f:
    KEY = re.search(r"MINIMAX_API_KEY=(\S+)", f.read()).group(1)

all_slugs = sorted(f.replace(".html","") for f in os.listdir(ARTIKEL_DIR) if f.endswith(".html"))
EMPTY = []
for slug in all_slugs:
    with open(os.path.join(ARTIKEL_DIR, f"{slug}.html")) as f:
        c = f.read()
    h2s = len(re.findall(r"<h2[^>]*>", c))
    ps = len([p for p in re.findall(r"<p>(.*?)</p>", c) if len(p) > 80])
    if h2s >= 3 and ps >= 3:
        continue
    title = ""
    t = re.search(r"<title>(.*?)\s*\|", c)
    if t: title = t.group(1).strip()
    EMPTY.append({"slug":slug,"title":title})

print(f"EMPTY: {len(EMPTY)}", flush=True)
DONE = 0

for bi in range(0, len(EMPTY), 4):  # 4 per batch für bessere Qualität
    batch = EMPTY[bi:bi+4]
    idx = bi//4 + 1
    total = (len(EMPTY)+3)//4
    
    prompt = "Generiere deutschen SEO-Content für folgende Artikel. Pro Artikel: 8-12 H2-Überschriften, 3-5 Absätze pro H2, Tabellen, Code-Blöcke.\n"
    prompt += "Antworte NUR mit HTML, KEINE Denkprozesse, keine Markdown-Codeblöcke.\n"
    prompt += "Jeder Artikel beginnt mit <!--SLUG:xxx--> und hat direkt <h2>...</h2>.\n\n"
    
    for a in batch:
        prompt += f'<!--SLUG:{a["slug"]}-->\n'
    
    data = json.dumps({"model":"MiniMax-M3","messages":[
        {"role":"system","content":"Du bist ein deutscher SEO-Content-Autor für hostazar.com. Antworte NUR mit dem HTML-Content. Keine Erklärungen, kein <think>, kein ```html."},
        {"role":"user","content":prompt}
    ],"max_tokens":8192,"temperature":0.7}).encode()
    
    req = urllib.request.Request("https://api.minimax.io/v1/chat/completions", data=data,
        headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
    
    t0 = time.time()
    written = 0
    
    for attempt in range(5):
        try:
            resp = json.loads(urllib.request.urlopen(req, timeout=300).read())
            if "choices" in resp and resp["choices"]:
                reply = resp["choices"][0].get("message", {}).get("content", "")
                
                # Strip <think> tags and ```html blocks
                reply = re.sub(r'<think>.*?</think>', '', reply, flags=re.DOTALL)
                reply = re.sub(r'```html\n?|```', '', reply)
                reply = reply.strip()
                
                # Split by SLUG markers
                parts = re.split(r'<!--SLUG:([a-z0-9][a-z0-9-]+)-->', reply)
                
                if len(parts) < 3:
                    print(f"[{idx}/{total}] ⚠️ keine Slugs gefunden, versuche Regex... ({len(parts)} parts)", flush=True)
                    # Fallback: search for H2 and use first batch slug
                    h2s = re.findall(r'<h2[^>]*>', reply)
                    if len(h2s) >= 3 and batch:
                        fp = os.path.join(ARTIKEL_DIR, f"{batch[0]['slug']}.html")
                        with open(fp) as f: shell = f.read()
                        new = re.sub(r"(<h1[^>]*>.*?</h1>)", r"\1\n"+reply, shell, count=1, flags=re.DOTALL)
                        with open(fp, "w") as f: f.write(new)
                        written += 1
                        print(f"[{idx}/{total}] ✅ 1 (Fallback) ({time.time()-t0:.0f}s)", flush=True)
                        DONE += 1
                        break
                    print(f"[{idx}/{total}] ⚠️ kein H2 gefunden ({len(h2s)})", flush=True)
                    break
                
                for pi, slug in enumerate(parts):
                    if pi % 2 == 1 and pi+1 < len(parts):
                        content = parts[pi+1].strip()
                        # Extract first real content (skip think if any remained)
                        h2_start = content.find('<h2')
                        if h2_start > 0:
                            content = content[h2_start:]
                        content = re.sub(r'```html\n?|```', '', content).strip()
                        
                        if len(content) > 300:
                            fp = os.path.join(ARTIKEL_DIR, f"{slug}.html")
                            if os.path.exists(fp):
                                with open(fp) as f: shell = f.read()
                                new = re.sub(r"(<h1[^>]*>.*?</h1>)", r"\1\n"+content, shell, count=1, flags=re.DOTALL)
                                with open(fp, "w") as f: f.write(new)
                                written += 1
                
                DONE += written
                print(f"[{idx}/{total}] ✅ {written} ({time.time()-t0:.0f}s)", flush=True)
                break
            else:
                print(f"[{idx}/{total}] ⚠️ unerwartete Response", flush=True)
                time.sleep(10)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"[{idx}/{total}] ⏳ 429, warte 90s...", flush=True)
                time.sleep(90)
            else:
                print(f"[{idx}/{total}] ❌ HTTP {e.code}", flush=True)
                break
        except Exception as e:
            print(f"[{idx}/{total}] ❌ {e}", flush=True)
            break
    
    if idx < total:
        time.sleep(max(1, 65 - (time.time()-t0)))

ok = 0
for a in EMPTY:
    with open(os.path.join(ARTIKEL_DIR, f"{a['slug']}.html")) as f:
        c = f.read()
    if len(re.findall(r"<h2[^>]*>", c)) >= 3:
        ok += 1

print(f"\n=== FERTIG: {DONE} Artikel | OK: {ok}/{len(EMPTY)} ===", flush=True)
