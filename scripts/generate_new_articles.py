#!/usr/bin/env python3
"""
Batch-Artikel-Generierung für 5 neue Gaming-Artikel
Erstellt HTML-Dateien im hostazar-Stil und aktualisiert artikel.json
"""
import json, os, re, datetime

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARTIKEL_JSON = os.path.join(BASE, 'data', 'artikel.json')
ARTIKEL_DIR = os.path.join(BASE, 'artikel')
IMAGES_DIR = os.path.join(BASE, 'images')
SITE_URL = 'https://hostazar.com'

TODAY = datetime.date.today().isoformat()

# ── Artikel-Definitionen ─────────────────────────────────────────────────────

ARTICLES = [
    {
        "slug": "pubg-server-mieten-2026",
        "title": "PUBG Server mieten 2026 – Preise, Slots & Anbieter im Vergleich",
        "category": "gaming",
        "tags": ["PUBG Server mieten", "PUBG Server Preise", "Battle Royale Server", "PUBG Anbieter", "PUBG Server Slots"],
        "excerpt": "PUBG Server mieten 2026: Anbieter-Vergleich mit Preisen, Slot-Anzahl, Anti-Cheat und Performance. Welcher Anbieter ist der beste für Battle Royale?",
        "image": "pubg-server-mieten-2026.png",
        "readingTime": "12",
        "content": """
<h1>PUBG Server mieten 2026 – Preise, Slots & Anbieter im Vergleich</h1>

<p>PlayerUnknown's Battlegrounds hat die Battle-Royale-Geprägt. Obwohl Fortnite und Apex Legends die Aufmerksamkeit auf sich zogen, hat PUBG eine treue Community — und viele Spieler wollen ihren eigenen Server hosten. Egal ob für Custom Matches, Turniere oder private Runden mit Freunden: Ein eigener PUBG Server gibt dir volle Kontrolle über Spielregeln, Maps und Slots.</p>

<div class="highlight-box">
<p><strong>Warum einen PUBG Server mieten?</strong> Custom Matches mit Freunden, Turniere mit eigenen Regeln, Anti-Cheat-Kontrolle, eigene Map-Rotation, niedrige Latenz durch Standort-Wahl.</p>
</div>

<h2>Die besten PUBG Server Anbieter 2026</h2>

<h3>1. Nitrado – Der Allrounder</h3>
<p>Nitrado ist einer der bekanntesten Gameserver-Anbieter in Europa. PUBG-Server ab 10 Slots verfügbar, DDoS-Schutz inklusive, Server-Standorte in Frankfurt, London und Chicago. Preise starten bei ca. 15€/Monat für 30 Slots.</p>
<p><strong>Vorteile:</strong> Webinterface, App-Support, automatische Backups, gute Performance<br>
<strong>Nachteile:</strong> Kein Root-Zugang, begrenzte Konfigurationsmöglichkeiten</p>

<h3>2. G-Portal – Flexibel und günstig</h3>
<p>G-Portal bietet PUBG-Server mit Root-Zugang, voller Konfiguration und Anti-Cheat-Integration. Ab 12€/Monat für 20 Slots. Server in Frankfurt, Amsterdam und New York.</p>
<p><strong>Vorteile:</strong> Root-Zugang, volle Config-Kontrolle, gute Preise<br>
<strong>Nachteile:</strong> Support kann langsam sein</p>

<h3>3. Host Havoc – Premium-Performance</h3>
<p>Host Havoc setzt auf High-Performance-Hardware mit NVMe-SSDs und modernen CPUs. PUBG-Server ab 20€/Monat für 30 Slots. Standorte in Frankfurt, London, New York, Sydney.</p>
<p><strong>Vorteile:</strong> Top-Hardware, exzellenter Support, 99.9% Uptime<br>
<strong>Nachteile:</strong> Teurer als Konkurrenz</p>

<h3>4. GameServers.com – Der Klassiker</h3>
<p>GameServers.com bietet seit Jahren PUBG-Server mit großer Flexibilität. Ab 18€/Monat für 30 Slots. Große Standort-Auswahl weltweit.</p>

<h2>PUBG Server Preise im Vergleich</h3>
<table style="width:100%;border-collapse:collapse;margin:20px 0">
<tr style="background:#222;color:#e0e0e0">
<th style="padding:10px;text-align:left">Anbieter</th>
<th style="padding:10px;text-align:left">Slots</th>
<th style="padding:10px;text-align:left">Preis/Monat</th>
<th style="padding:10px;text-align:left">Standorte</th>
</tr>
<tr style="border-bottom:1px solid #333">
<td style="padding:10px">Nitrado</td><td style="padding:10px">30</td><td style="padding:10px">~15€</td><td style="padding:10px">EU, US</td>
</tr>
<tr style="border-bottom:1px solid #333">
<td style="padding:10px">G-Portal</td><td style="padding:10px">20</td><td style="padding:10px">~12€</td><td style="padding:10px">EU, US</td>
</tr>
<tr style="border-bottom:1px solid #333">
<td style="padding:10px">Host Havoc</td><td style="padding:10px">30</td><td style="padding:10px">~20€</td><td style="padding:10px">EU, US, AU</td>
</tr>
<tr style="border-bottom:1px solid #333">
<td style="padding:10px">GameServers.com</td><td style="padding:10px">30</td><td style="padding:10px">~18€</td><td style="padding:10px">Weltweit</td>
</tr>
</table>

<h2>PUBG Server selbst hosten vs. mieten</h2>
<p>Für technisch versierte Spieler kann es sinnvoll sein, einen PUBG-Server auf einem eigenen VPS zu hosten. Die Vorteile: volle Kontrolle, keine Slot-Begrenzung, günstiger bei vielen Spielern. Die Nachteile: eigene Wartung, DDoS-Schutz selbst einrichten, Updates manuell.</p>

<div class="affiliate-box">
<p><strong>Empfehlung:</strong> Für die meisten Spieler ist ein gemieteter Server die bessere Wahl. Die Kosten sind überschaubar und der Aufwand minimal.</p>
<a href="https://www.g-portal.com/de/games/pubg" class="btn" rel="nofollow noopener" target="_blank">→ G-Portal PUBG Server prüfen</a>
</div>

<h2>Fazit</h2>
<p>PUBG-Server mieten lohnt sich für alle, die Custom Matches, Turniere oder private Runden organisieren wollen. G-Portal bietet das beste Preis-Leistungs-Verhältnis, Host Havoc ist die Premium-Wahl. Für Einsteiger ist Nitrado mit seiner einfachen Bedienung ideal.</p>
"""
    },
    {
        "slug": "lethal-company-server-mieten-2026",
        "title": "Lethal Company Server mieten – Multiplayer Setup Guide 2026",
        "category": "gaming",
        "tags": ["Lethal Company Server", "Lethal Company Multiplayer", "Horror Coop Server", "Lethal Company Setup"],
        "excerpt": "Lethal Company Server mieten oder selbst hosten: Multiplayer Setup-Guide mit Anbieter-Vergleich, Mods und Performance-Tipps für Horror-Coop.",
        "image": "lethal-company-server-mieten-2026.png",
        "readingTime": "10",
        "content": """
<h1>Lethal Company Server mieten – Multiplayer Setup Guide 2026</h1>

<p>Lethal Company hat den Horror-Coop-Markt aufgemischt. Das indie-Game mit seinem einzigartigen Mix aus Horror, Humor und Teamwork ist ein riesiger Erfolg auf Steam. Aber was wenn ihr mehr als 4 Spieler auf einem Server haben wollt? Oder Mods nutzen? Dann braucht ihr einen eigenen Server.</p>

<div class="highlight-box">
<p><strong>Wichtig:</strong> Lethal Company unterstützt offiziell bis zu 4 Spieler. Für mehr Spieler und Mods braucht ihr Community-Lösungen wie LC API oder andere Mods.</p>
</div>

<h2>Lethal Company Server Optionen</h2>

<h3>1. Gemieteter Gameserver</h3>
<p>Anbieter wie G-Portal und Nitrado bieten Lethal Company Server an. Die Einrichtung ist über das Webinterface möglich, Root-Zugang ist aber oft limitiert. Preise: ca. 8-12€/Monat für 4-10 Slots.</p>

<h3>2. Eigener VPS</h3>
<p>Die flexibelste Option. Auf einem eigenen VPS (z.B. Hetzner CX21 ab 5€/Monat) könnt ihr Lethal Company mit Mods und erhöhter Spielerzahl betreiben. Benötigt: Windows Server oder Linux mit Wine/Proton.</p>

<h3>3. Selbst hosten (Lokal)</h3>
<p>Der einfachste Weg für kleine Gruppen. Einer der Spieler hostet den Server lokal. Vorteil: Kostenlos. Nachteile: Host muss online sein, begrenzte Performance, keine 24/7-Verfügbarkeit.</p>

<h2>Mod-Support für Lethal Company</h2>
<p>Die Lethal Company Modding-Community ist extrem aktiv. Beliebte Mods:</p>
<ul>
<li><strong>LC API</strong> – Basis-Mod für erweiterte Spielerzahl und Server-Konfiguration</li>
<li><strong>MoreCompany</strong> – Erhöht die Spielerzahl auf bis zu 20</li>
<li><strong>LateCompany</strong> – Spieler können später dem Spiel beitreten</li>
<li><strong>SkinWalkers</strong> – Neue Monster-Typen für mehr Horror</li>
<li><strong>Helmet_Cameras</strong> – Helmkameras für immersive Perspektive</li>
</ul>

<h2>Server-Performance optimieren</h2>
<p>Lethal Company ist nicht besonders ressourcenhungrig, aber für einen stabilen Server mit Mods sollte man mindestens 2 vCPUs und 4 GB RAM einplanen. SSD-Speicher ist empfehlenswert für schnelle Ladezeiten.</p>

<div class="affiliate-box">
<p><strong>Tipp:</strong> Für Lethal Company mit Mods empfehlen wir einen eigenen VPS bei Hetzner oder Contabo. Flexibler und günstiger als ein Gameserver.</p>
<a href="https://www.hetzner.com/cloud" class="btn" rel="nofollow noopener" target="_blank">→ Hetzner VPS prüfen</a>
</div>

<h2>Fazit</h2>
<p>Lethal Company mit eigenen Server macht besonders dann Sinn, wenn ihr Mods nutzen oder mehr als 4 Spieler auf einem Server haben wollt. Für kleine Gruppen reicht ein lokaler Server, für 24/7-Verfügbarkeit und Mods ist ein VPS die beste Wahl.</p>
"""
    },
    {
        "slug": "helldivers-2-server-hosten-2026",
        "title": "Helldivers 2 Server hosten – Kooperative Missions-Pläne 2026",
        "category": "gaming",
        "tags": ["Helldivers 2 Server", "Helldivers 2 Coop", "Shooter Server", "Helldivers 2 Multiplayer", "Arrowhead Server"],
        "excerpt": "Helldivers 2 Server-Status, Coop-Multiplayer und Community-Server: Alles über die Server-Infrastruktur von Arrowhead's Hit-Shooter.",
        "image": "helldivers-2-server-hosten-2026.png",
        "readingTime": "11",
        "content": """
<h1>Helldivers 2 Server hosten – Kooperative Missions-Pläne 2026</h1>

<p>Helldivers 2 von Arrowhead Game Studios ist einer der größten Multiplayer-Hits des Jahres. Das kooperative Shooter-Erlebnis für bis zu 4 Spieler hat Millionen von Spielern begeistert. Aber wie sieht es mit eigenen Servern aus? Und was ist mit der Server-Infrastruktur?</p>

<div class="highlight-box">
<p><strong>Hinweis:</strong> Helldivers 2 nutzt dedizierte Server von Arrowhead. Private Server sind offiziell nicht verfügbar. Dieser Artikel erklärt die Server-Infrastruktur und was die Community plant.</p>
</div>

<h2>Helldivers 2 Server-Infrastruktur</h2>
<p>Arrowhead betreibt die Helldivers 2 Server auf eigener Infrastruktur. Die Server stehen in verschiedenen Regionen:</p>
<ul>
<li><strong>Europa:</strong> Frankfurt, Amsterdam, London</li>
<li><strong>Nordamerika:</strong> New York, Chicago, Los Angeles</li>
<li><strong>Asien:</strong> Tokyo, Singapore</li>
<li><strong>Ozeanien:</strong> Sydney</li>
</ul>

<h2>Server-Probleme und Lösungen</h2>
<p>Bei Launch hatte Helldivers 2 massive Server-Probleme. Millionen Spieler wollten gleichzeitig spielen, und die Infrastruktur war nicht vorbereitet. Arrowhead hat seitdem:</p>
<ul>
<li>Server-Kapazität mehrfach erhöht</li>
<li>Matchmaking-Optimierungen implementiert</li>
<li>Anti-Cheat-System verbessert</li>
<li>Cross-Play zwischen PS5 und PC ermöglicht</li>
</ul>

<h2>Community-Server und Mods</h2>
<p>Obwohl offizielle private Server nicht verfügbar sind, arbeitet der Community-Modding-Szene an Lösungen. Erwartet werden:</p>
<ul>
<li>Custom Missions mit eigenen Parametern</li>
<li>Modifizierte Schwierigkeitsgrade</li>
<li>Private Lobbies für Clans</li>
<li>Statistik-Tracker und Leaderboards</li>
</ul>

<h2>Performance-Tipps für Helldivers 2</h2>
<p>Um die beste Erfahrung zu haben:</p>
<ol>
<li><strong>Wählt den richtigen Server-Standort:</strong> In den Einstellungen könnt ihr die bevorzugte Region wählen</li>
<li><strong>Verwendet Kabel statt WLAN:</strong> Für einen Shooter ist eine stabile Verbindung essentiell</li>
<li><strong>Schließt Hintergrund-Anwendungen:</strong> Helldivers 2 ist CPU-intensiv</li>
<li><strong>Treibt Grafikeinstellungen hoch:</strong> Das Game sieht besser aus mit höheren Settings</li>
</ol>

<div class="affiliate-box">
<p><strong>Helldivers 2 kaufen:</strong> Das Game ist auf Steam und PS5 verfügbar. Regelmäßige Updates und Seasons halten das Spiel frisch.</p>
<a href="https://store.steampowered.com/app/553850/Helldivers_2/" class="btn" rel="nofollow noopener" target="_blank">→ Helldivers 2 auf Steam</a>
</div>

<h2>Fazit</h2>
<p>Helldivers 2 nutzt dedizierte Server von Arrowhead — private Server sind offiziell nicht möglich. Die Server-Infrastruktur hat sich seit dem Launch deutlich verbessert. Für die beste Erfahrung: Kabelverbindung, richtige Server-Standort-Wahl und aktuelle Treiber.</p>
"""
    },
    {
        "slug": "deep-rock-galactic-server-mieten-2026",
        "title": "Deep Rock Galactic Server mieten – 4-Spieler Koop Guide 2026",
        "category": "gaming",
        "tags": ["Deep Rock Galactic Server", "DRG Server mieten", "Koop Shooter", "Deep Rock Galactic Coop", "Ghost Ship Games"],
        "excerpt": "Deep Rock Galactic Server mieten oder selbst hosten: Anbieter-Vergleich, Setup-Guide und Tipps für den besten Koop-Erlebnis im Bergbau-Shooter.",
        "image": "deep-rock-galactic-server-mieten-2026.png",
        "readingTime": "10",
        "content": """
<h1>Deep Rock Galactic Server mieten – 4-Spieler Koop Guide 2026</h1>

<p>Deep Rock Galactic ist der perfekte Koop-Shooter für alle, die Bergbau, Aliens und Bier lieben. Bis zu 4 Spieler erkunden gemeinsam die Höhlen von Hoxxes IV. Aber was wenn ihr einen permanenten Server wollt, auf dem ihr jederzeit spielen könnt?</p>

<div class="highlight-box">
<p><strong>Rock and Stone!</strong> Deep Rock Galactic unterstützt offiziell Dedicated Server. Die Einrichtung ist einfach und es gibt mehrere Anbieter.</p>
</div>

<h2>Deep Rock Galactic Dedicated Server</h2>
<p>Ghost Ship Games bietet offizielle Dedicated-Server-Software an. Das bedeutet:</p>
<ul>
<li>24/7 Server-Verfügbarkeit</li>
<li>Volle Kontrolle über Schwierigkeit, Missionstyp und Mods</li>
<li>Kein Host-Migration-Problem</li>
<li>Perfekt für Clans und regelmäßige Gruppen</li>
</ul>

<h2>Anbieter-Vergleich</h2>

<h3>1. G-Portal</h3>
<p>G-Portal bietet DRG-Server ab ca. 10€/Monat. Einfache Einrichtung über Webinterface, DDoS-Schutz inklusive. Standorte in Frankfurt, Amsterdam, New York.</p>

<h3>2. Nitrado</h3>
<p>Nitrado ist die bequemste Option. DRG-Server ab 12€/Monat, App-Support, automatische Updates. Perfekt für Einsteiger.</p>

<h3>3. Eigener VPS</h3>
<p>Die günstigste Option für technisch Versierte. Ein Hetzner CX11 VPS (ab 3.50€/Monat) reicht für einen DRG-Server mit 4 Spielern. Benötigt Linux-Kenntnisse.</p>

<h2>Server-Einrichtung</h2>
<p>Die offizielle DRG Dedicated Server Software läuft auf Linux und Windows. Die Einrichtung:</p>
<ol>
<li>SteamCMD installieren</li>
<li>DRG Dedicated Server herunterladen (App-ID: 1361210)</li>
<li>Server-Konfiguration anpassen (Schwierigkeit, Missionen, Mods)</li>
<li>Port 27015 UDP freigeben</li>
<li>Server starten und im Game verbinden</li>
</ol>

<h2>Mods und Customization</h2>
<p>DRG unterstützt Mods über den Mod.io-Integration. Beliebte Mods:</p>
<ul>
<li><strong>Better UI</strong> – Verbesserte Benutzeroberfläche</li>
<li><strong>More Saves</strong> – Mehr Speicherstände</li>
<li><strong>Custom Difficulty</strong> – Eigene Schwierigkeitsgrade</li>
<li><strong>Sandstorm</strong> – Neue Missionstypen</li>
</ul>

<div class="affiliate-box">
<p><strong>Deep Rock Galactic kaufen:</strong> Das Game ist regelmäßig im Sale erhältlich. Mit Season-Pass gibt es monatlich neuen Content.</p>
<a href="https://store.steampowered.com/app/1361210/Deep_Rock_Galactic/" class="btn" rel="nofollow noopener" target="_blank">→ DRG auf Steam</a>
</div>

<h2>Fazit</h2>
<p>Deep Rock Galactic Dedicated Server sind einzurichten und die offizielle Software macht es einfach. Für Einsteiger sind Anbieter wie Nitrado oder G-Portal ideal, für Fortgeschrittene ein eigener VPS die günstigste Option. Rock and Stone!</p>
"""
    },
    {
        "slug": "phasmophobia-server-hosten-2026",
        "title": "Phasmophobia Server hosten – Geisterjagd Multiplayer 2026",
        "category": "gaming",
        "tags": ["Phasmophobia Server", "Phasmophobia Multiplayer", "Horror Coop", "Phasmophobia Geisterjagd", "Kinetic Games"],
        "excerpt": "Phasmophobia Server hosten und Multiplayer-Geisterjagd: Server-Setup, Anbieter-Vergleich und Tipps für den besten Horror-Coop-Erlebnis.",
        "image": "phasmophobia-server-hosten-2026.png",
        "readingTime": "9",
        "content": """
<h1>Phasmophobia Server hosten – Geisterjagd Multiplayer 2026</h1>

<p>Phasmophobia hat den Horror-Gaming-Markt revolutioniert. Als Geisterjäger mit VR-Unterstützung und realistischer Audio-Atmosphäre ist es einer der gruseligsten Multiplayer-Erlebnisse. Aber wie funktionieren die Server? Und kann man einen eigenen hosten?</p>

<div class="highlight-box">
<p><strong>Info:</strong> Phasmophobia nutzt P2P-Verbindung mit einem Host-Spieler. Dedicated Server sind offiziell nicht verfügbar, aber es gibt Community-Lösungen.</p>
</div>

<h2>Phasmophobia Multiplayer – So funktioniert es</h2>
<p>Phasmophobia nutzt ein Host-basiertes System:</p>
<ul>
<li>Ein Spieler ist der Host und hostet den Spiel-Server</li>
<li>Bis zu 4 Spieler können beitreten</li>
<li>Der Host braucht eine gute Upload-Bandbreite</li>
<li>Bei Verlust des Hosts endet das Spiel</li>
</ul>

<h2>Server-Alternativen</h2>

<h3>1. Dedicated Server (Community)</h3>
<p>Die Phasmophobia-Community hat Dedicated-Server-Lösungen entwickelt. Diese erlauben:</p>
<ul>
<li>24/7 Server ohne Host-Spieler</li>
<li>Stabilere Verbindungen</li>
<li>Custom Maps und Mods</li>
<li>Clan-übergreifende Lobbies</li>
</ul>

<h3>2. Gemieteter VPS als Host</h3>
<p>Ein VPS kann als permanenter Host dienen. Empfohlen:</p>
<ul>
<li>Mindestens 2 vCPUs, 4 GB RAM</li>
<li>Windows Server oder Linux mit Wine</li>
<li>Gute Upload-Bandbreite (mindestens 10 Mbit/s)</li>
<li>Standort in der Nähe der Spieler</li>
</ul>

<h3>3. Nitrado / G-Portal</h3>
<p>Einige Anbieter unterstützen Phasmophobia-Server. Die Einrichtung ist ähnlich wie bei anderen Source-basierten Spielen.</p>

<h2>Phasmophobia Performance optimieren</h2>
<p>Für das beste Horror-Erlebnis:</p>
<ol>
<li><strong>VRAM:</strong> Mindestens 4 GB für flüssige VR-Performance</li>
<li><strong>Audio:</strong> Kopfhörer mit Surround-Sound für Geister-Geräusche</li>
<li><strong>Netzwerk:</strong> Kabelverbindung für den Host</li>
<li><strong>Grafik:</strong> Hohe Schatten-Qualität für gruselige Atmosphäre</li>
</ol>

<h2>Mods und Custom Content</h2>
<p>Phasmophobia hat eine aktive Modding-Community:</p>
<ul>
<li><strong>Custom Maps</strong> – Neue Locations wie Schulen, Krankenhäuser, Gefängnisse</li>
<li><strong>More Ghosts</strong> – Zusätzliche Geister-Typen mit einzigartigen Verhalten</li>
<li><strong>VR Improvements</strong> – Verbesserte VR-Interaktion</li>
<li><strong>Voice Recognition</strong> – Sprachbefehle für Geister</li>
</ul>

<div class="affiliate-box">
<p><strong>Phasmophobia kaufen:</strong> Das Game ist auf Steam erhältlich und regelmäßig im Sale. VR-Unterstützung inklusive.</p>
<a href="https://store.steampowered.com/app/739630/Phasmophobia/" class="btn" rel="nofollow noopener" target="_blank">→ Phasmophobia auf Steam</a>
</div>

<h2>Fazit</h2>
<p>Phasmophobia nutzt ein Host-basiertes System, aber Community-Dedicated-Server und VPS-Lösungen bieten mehr Stabilität. Für das beste Horror-Erlebnis: Kopfhörer, Kabelverbindung und eine gruselige Umgebung. Happy Hunting!</p>
"""
    }
]

# ── HTML Template ────────────────────────────────────────────────────────────

def make_html(title, slug, desc, cat, image, date, reading_time, content, tags):
    cat_info = {
        'gaming': ('Gaming', '#4CAF50', 'rgba(76,175,80,0.2)', '#66bb6a'),
        'webhosting': ('Webhosting', '#2196F3', 'rgba(33,150,243,0.2)', '#64b5f6'),
        'devops': ('DevOps', '#FF9800', 'rgba(255,152,0,0.2)', '#ffb74d'),
        'ki-llm': ('KI & LLM', '#9C27B0', 'rgba(156,39,176,0.2)', '#ce93d8'),
    }
    cat_name, color, tag_bg, tag_color = cat_info.get(cat, ('Artikel', '#9C27B0', 'rgba(156,39,176,0.2)', '#ce93d8'))
    
    tag_list = ''.join(f'<span class="tag-pill">{t}</span>' for t in tags[:5])
    
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | hostazar.com</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{SITE_URL}/artikel/{slug}.html">
  <link rel="stylesheet" href="/css/style.css">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE_URL}/artikel/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{SITE_URL}/images/{image}">
  <meta property="og:locale" content="de_DE">
  <meta property="og:site_name" content="Hostazar — VPS &amp; DevOps Portal">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE_URL}/images/{image}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "url": "{SITE_URL}/artikel/{slug}.html",
    "datePublished": "{date}",
    "dateModified": "{date}",
    "author": {{"@type": "Organization", "name": "hostazar.com"}},
    "publisher": {{"@type": "Organization", "name": "hostazar.com"}},
    "description": "{desc}",
    "image": "{SITE_URL}/images/{image}",
    "inLanguage": "de"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Startseite", "item": "{SITE_URL}/"}},
      {{"@type": "ListItem", "position": 2, "name": "{cat_name}", "item": "{SITE_URL}/{cat}/"}},
      {{"@type": "ListItem", "position": 3, "name": "{title}", "item": "{SITE_URL}/artikel/{slug}.html"}}
    ]
  }}
  </script>
</head>
<body>
<nav class="navbar">
  <div class="container">
    <a href="/" class="logo">hosta<span>zar</span></a>
    <button class="nav-toggle" aria-label="Menü öffnen">&#9776;</button>
    <ul class="nav-links">
      <li><a href="/">Startseite</a></li>
      <li><a href="/gaming/">Gaming</a></li>
      <li><a href="/webhosting/">Webhosting</a></li>
      <li><a href="/devops/">DevOps</a></li>
      <li><a href="/ki-llm/">KI &amp; LLM</a></li>
    </ul>
  </div>
</nav>
<nav class="breadcrumbs"><a href="{SITE_URL}/">hostazar</a><span class="sep"> › </span><a href="{SITE_URL}/{cat}/">{cat_name}</a><span class="sep"> › </span><span class="current">{title}</span></nav>
<main class="article-page">
  <div class="container">
    <div class="article-meta-top">
      <span class="card-tag {cat}">{cat_name}</span>
      <span>{reading_time} Min Lesezeit</span>
      <span>{date}</span>
    </div>
    <article class="article-content">
      <figure class="article-hero-img" style="margin:0 0 24px">
        <img src="/images/{image}" alt="{title}" loading="lazy" width="800" height="400" style="width:100%;height:auto;border-radius:12px">
      </figure>
      {content}
    </article>
    <div class="article-tags" style="margin:30px 0;padding-top:20px;border-top:1px solid #333">
      <h4 style="color:var(--text-secondary);font-size:0.9rem;margin-bottom:10px">Tags:</h4>
      <div class="tag-cloud">{tag_list}</div>
    </div>
  </div>
</main>
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div><h4>hostazar.com</h4><p style="color:var(--text-muted);font-size:.85rem">Unabhängige Hosting-Reviews, Gameserver-Guides und DevOps-Tutorials.</p></div>
    </div>
    <div class="footer-bottom"><span>© 2026 hostazar.com</span><span><a href="/impressum.html">Impressum</a> · <a href="/datenschutz.html">Datenschutz</a></span></div>
    <div class="affiliate-note">* Affiliate-Links: Wir erhalten ggf. eine Provision. Das kostet dich keinen Cent mehr.</div>
  </div>
</footer>
<div class="cookie-banner" id="cookieBanner"><div class="cookie-inner"><p>Wir nutzen Cookies für Analyse und AdSense. <a href="/datenschutz.html">Mehr erfahren</a></p><button class="cookie-btn" id="cookieBtn">Akzeptieren</button></div></div>
<script src="/data/script.js" defer></script>
</body>
</html>'''


# ── Generierung ──────────────────────────────────────────────────────────────

os.makedirs(ARTIKEL_DIR, exist_ok=True)

# Lade bestehende artikel.json
with open(ARTIKEL_JSON, encoding='utf-8') as f:
    artikel_list = json.load(f)

existing_slugs = {a['slug'] for a in artikel_list}
added = 0

for art in ARTICLES:
    if art['slug'] in existing_slugs:
        print(f"  SKIP (exists): {art['slug']}")
        continue
    
    # HTML schreiben
    html = make_html(
        title=art['title'],
        slug=art['slug'],
        desc=art['excerpt'],
        cat=art['category'],
        image=art['image'],
        date=TODAY,
        reading_time=art['readingTime'],
        content=art['content'],
        tags=art['tags'],
    )
    
    filepath = os.path.join(ARTIKEL_DIR, f"{art['slug']}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # artikel.json Eintrag
    entry = {
        "slug": art['slug'],
        "title": art['title'],
        "category": art['category'],
        "tags": art['tags'],
        "excerpt": art['excerpt'],
        "date": TODAY,
        "readingTime": art['readingTime'],
        "image": art['image'],
    }
    artikel_list.append(entry)
    existing_slugs.add(art['slug'])
    added += 1
    print(f"  OK: {art['slug']}")

# artikel.json speichern
artikel_list.sort(key=lambda a: a.get('date', ''), reverse=True)
with open(ARTIKEL_JSON, 'w', encoding='utf-8') as f:
    json.dump(artikel_list, f, ensure_ascii=False, indent=2)

print(f"\n=== {added} neue Artikel generiert, {len(artikel_list)} total ===")
