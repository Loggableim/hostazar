#!/usr/bin/env python3
"""Append 3 new articles to the JSON-LD BlogPosting array in index.html,
and update the meta description guide count."""
import os, re

REPO = r"C:\HermesPortable\home\scripts\blog-automation\hostazar"
INDEX_HTML = os.path.join(REPO, "index.html")

NEW = [
    {
        "headline": "Dedizierter Server vs. VPS – Der große Vergleich 2026",
        "url": "https://hostazar.com/artikel/dedizierter-server-vs-vps-2026.html",
        "datePublished": "2026-06-06",
        "dateModified": "2026-06-06",
        "description": "Dedizierter Server vs. VPS 2026: Ausführlicher Vergleich mit Kosten, Performance, Vor-/Nachteilen und Anbieter-Tabelle. Welcher Server passt zu dir?",
    },
    {
        "headline": "DDoS-Schutz für Gameserver – Anbieter & Konfiguration 2026",
        "url": "https://hostazar.com/artikel/ddos-schutz-gameserver-2026.html",
        "datePublished": "2026-06-06",
        "dateModified": "2026-06-06",
        "description": "DDoS-Schutz für Gameserver 2026: Anbieter-Vergleich (OVH, Hetzner, G-Portal, TCPShield), Konfiguration mit iptables/nftables und Best Practices gegen Angriffe.",
    },
    {
        "headline": "Minecraft Bedrock vs. Java Server – Unterschiede & Hosting 2026",
        "url": "https://hostazar.com/artikel/minecraft-bedrock-vs-java-server-2026.html",
        "datePublished": "2026-06-06",
        "dateModified": "2026-06-06",
        "description": "Minecraft Bedrock vs. Java Server 2026: Vergleich von Performance, Mods, Crossplay, Hosting-Anforderungen, Server-Software (Spigot, Paper, BDS) und Kosten.",
    },
]


def json_escape(s):
    return (s.replace("\\", "\\\\").replace('"', '\\"'))


def blogposting_obj(n):
    return (
        '{"@context": "https://schema.org", "@type": "BlogPosting", '
        f'"headline": "{json_escape(n["headline"])}", '
        f'"url": "{n["url"]}", '
        f'"datePublished": "{n["datePublished"]}", '
        f'"dateModified": "{n["dateModified"]}", '
        f'"description": "{json_escape(n["description"])}", '
        '"author": {"@type": "Organization", "name": "hostazar.com"}}'
    )


def main():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        text = f.read()

    # Find the array JSON-LD block: starts with "[{..." inside an application/ld+json script.
    # The array always ends with '}}]' (close last BlogPosting + close array). We use rfind to find
    # the position of the last '}}]' in the JSON-LD script block.
    s = text.find('[{')
    if s < 0:
        print("JSON-LD array block not found")
        return
    end_script = text.find('</script>', s)
    if end_script < 0:
        print("no </script> after [{")
        return
    e = text.rfind('}}]', s, end_script)
    if e < 0:
        print("no closing }}] of array found")
        return
    # The original ends with '}}]'. text[:e] stops BEFORE the first '}' of that '}}]'.
    # We replace that '}}]' with '}}' + ',' + new_obj1 + ',' + new_obj2 + ',' + new_obj3 + ']'
    # so the array remains well-formed.
    text = text[:e] + "}}," + ",".join(blogposting_obj(n) for n in NEW) + "]" + text[e+3:]
    print(f"Appended {len(NEW)} BlogPosting entries to JSON-LD array at position {e}")

    # Update guide count in meta description (and og:description, twitter:description)
    # Find current count
    m = re.search(r'Hosting- und Server-Blog mit (\d+) Guides', text)
    if m:
        old_count = int(m.group(1))
        new_count = 94  # 91 prior + 3 new
        text = re.sub(
            r'Hosting- und Server-Blog mit \d+ Guides',
            f'Hosting- und Server-Blog mit {new_count} Guides',
            text,
        )
        print(f"Updated guide count {old_count} -> {new_count}")
    else:
        print("Guide count pattern not found")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(text)
    print("Done.")


if __name__ == "__main__":
    main()
