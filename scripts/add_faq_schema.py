#!/usr/bin/env python3
"""
Add FAQPage JSON-LD schema to hostazar articles.

Finds articles with FAQ sections or setup guides and injects
FAQPage schema before </head>.
"""

import re
import os
from html import unescape

ARTICLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'artikel')

# Articles with existing FAQ sections (19 articles)
FAQ_ARTICLES = [
    'ai-agent-frameworks-2026.html',
    'baldurs-gate-3-server-mieten-2026.html',
    'best-vps-hosting-guide-2026.html',
    'borgbackup-vs-restic-for-vps-which-one-actually-saves-your-bacon-in-2026.html',
    'cloudflare-pages-vs-vercel-2026.html',
    'cutting-docker-image-bloat-real-world-wins-from-multi-stage-builds-in-2026.html',
    'docker-container-tutorial-beginners.html',
    'hardening-linux-vps-in-2026-practical-steps-beyond-default-firewalls.html',
    'hostinger-review-2026.html',
    'istio-service-mesh-2026.html',
    'kubernetes-cost-optimization-in-2026-cutting-cluster-waste-without-sacrificing-u.html',
    'minecraft-server-hosting-2026-comparison.html',
    'nginx-reverse-proxy-setup-guide.html',
    'phasmophobia-server-mieten-2026.html',
    'postgresql-on-a-5-vps-tuning-shared-buffers-and-workmem-for-real-workloads-in-20.html',
    'rust-server-mieten-guide-2026.html',
    'self-hosted-game-servers-in-2026-why-bare-metal-still-beats-cloud-for-latency.html',
    'spotting-a-hacked-vps-in-2026-forensic-checks-before-its-too-late.html',
    'zero-trust-networking-for-small-vps-fleets-a-pragmatic-setup-guide-for-2026.html',
]

# Additional setup guides (11 articles) - generate FAQ from content
SETUP_ARTICLES = [
    '7-days-to-die-server-hosten-2026.html',
    'ark-survival-ascended-server-hosten-2026.html',
    'cs2-server-mieten-guide-2026.html',
    'domain-kaufen-einrichten-2026.html',
    'email-server-selbst-hosten-2026.html',
    'gameserver-mieten-guide.html',
    'nextcloud-server-einrichten.html',
    'nginx-reverse-proxy-einrichten-2026.html',
    'palworld-server-hosting-guide-2026.html',
    'satisfactory-server-mieten-oder-selbst-hosten-2026.html',
    'valheim-server-vps-mieten-2026.html',
]


def clean_text(text):
    """Clean HTML text content."""
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def strip_html_tags(text):
    """Remove HTML tags from text."""
    return re.sub(r'<[^>]+>', '', text).strip()


def get_faq_section_end(content, start_pos):
    """Find where the FAQ section ends after a given start position."""
    # Look for any of these section-ending markers
    end_patterns = [
        r'<h2[^>]*>',       # Next h2 heading
        r'</article>',       # End of article
        r'<section[^>]*>',   # Next section (related articles)
        r'<hr\s*/?>',        # Horizontal rule
        r'<div[^>]*class="adsense',  # AdSense placeholder
        r'<div[^>]*class="related',   # Related articles
    ]
    
    positions = []
    for pattern in end_patterns:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            if m.start() > start_pos:
                positions.append(m.start())
    
    if positions:
        return min(positions)
    return len(content)


def extract_faq_pairs_generic(content):
    """Extract FAQ pairs from an FAQ section using flexible pattern matching."""
    # Find FAQ section heading
    faq_match = re.search(
        r'<h2[^>]*>(?:FAQ|Häufig)[^<]*</h2>',
        content, re.IGNORECASE
    )
    if not faq_match:
        return []
    
    section_start = faq_match.end()
    section_end = get_faq_section_end(content, section_start)
    faq_section = content[section_start:section_end]
    
    pairs = []
    
    # Pattern 1: <h3>QUESTION</h3> followed by <p>ANSWER</p>
    # (with optional whitespace/newlines between)
    pattern1 = re.compile(
        r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>',
        re.DOTALL | re.IGNORECASE
    )
    for match in pattern1.finditer(faq_section):
        q = clean_text(match.group(1))
        a = clean_text(match.group(2))
        if q and a and len(q) >= 5 and len(a) >= 10:
            pairs.append((q, a))
    
    # Pattern 2: <p><strong>QUESTION</strong><br>ANSWER</p>  (rust style)
    if len(pairs) < 3:
        pattern2 = re.compile(
            r'<p[^>]*><strong>(.*?)</strong>\s*<br\s*/?>(.*?)</p>',
            re.DOTALL | re.IGNORECASE
        )
        for match in pattern2.finditer(faq_section):
            q = clean_text(match.group(1))
            a = clean_text(match.group(2))
            if q and a and len(q) >= 5 and len(a) >= 10:
                pairs.append((q, a))
    
    # Pattern 3: Handle <li> instead of <p> after h3 (phasmophobia style)
    if len(pairs) < 3:
        pattern3 = re.compile(
            r'<h3[^>]*>(.*?)</h3>\s*<li[^>]*>(.*?)</li>',
            re.DOTALL | re.IGNORECASE
        )
        for match in pattern3.finditer(faq_section):
            q = clean_text(match.group(1))
            a = clean_text(match.group(2))
            if q and a and len(q) >= 5 and len(a) >= 10:
                pairs.append((q, a))
    
    return pairs


def extract_troubleshooting_pairs(content):
    """Extract Q&A from Common Pitfalls/Troubleshooting sections."""
    ts_match = re.search(
        r'<h2[^>]*>(?:Common Pitfalls|Troubleshooting)[^<]*</h2>\s*(.*?)(?=<h2[^>]*>|</article>|<section|<hr)',
        content, re.DOTALL | re.IGNORECASE
    )
    if not ts_match:
        return []
    
    section = ts_match.group(1)
    pairs = []
    
    # Look for li strong patterns
    li_pattern = re.compile(
        r'<li[^>]*><strong>(.*?)</strong>(.*?)</li>',
        re.DOTALL
    )
    for match in li_pattern.finditer(section):
        q = clean_text(match.group(1))
        a = clean_text(match.group(2))
        if q and a and len(q) >= 5 and len(a) >= 10:
            pairs.append((q, a))
    
    return pairs


def generate_faq_from_content(content, filename):
    """Generate FAQ pairs from article content for setup guides."""
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = clean_text(title_match.group(1)) if title_match else filename.replace('.html', '').replace('-', ' ')
    
    filename_lower = filename.lower()
    
    # Game server articles with tailored FAQ
    if '7-days-to-die' in filename_lower:
        return [
            ('Welche Anforderungen hat ein 7 Days to Die Server?',
             'Ein 7 Days to Die Server benötigt mindestens 2 vCPU-Kerne, 4 GB RAM und 20 GB Speicher. Für größere Gruppen (8+ Spieler) empfiehlt sich ein VPS mit 4 Kernen und 8 GB RAM. Das Spiel läuft unter Linux und Windows, wobei Linux ressourcenschonender ist.'),
            ('Kann ich 7 Days to Die auf einem VPS hosten?',
             'Ja, ein VPS ist ideal für 7 Days to Die. Du installierst den Dedicated Server via SteamCMD auf einem Linux-VPS. Achte auf eine stabile Anbindung mit mindestens 100 Mbit/s und ausreichend RAM für die Weltgenerierung.'),
            ('Wie viele Spieler passen auf einen 7 Days to Die Server?',
             'Standardmäßig unterstützt 7 Days to Die bis zu 8 Spieler gleichzeitig. Mit leistungsstarker Hardware und optimierten Einstellungen sind auch 16-24 Spieler möglich, sofern die Chunk-Generation nicht überlastet wird.'),
            ('Brauche ich Mods für meinen 7 Days to Die Server?',
             'Mods sind optional, aber beliebt. Overhaul-Mods wie Darkness Falls oder War3UK verändern das Gameplay massiv. Achte darauf, dass alle Spieler die gleichen Mods installiert haben.'),
            ('Wie oft sollte ich meinen 7 Days to Die Server resetten?',
             'Ein regelmäßiger World-Reset alle 1-3 Monate hält das Spiel frisch. Viele Admins resetten bei größeren Updates oder wenn die Weltdatei zu groß wird (uber 1 GB).')
        ]
    elif 'ark-survival' in filename_lower:
        return [
            ('Welche Hardware brauche ich fur einen ARK Server?',
             'ARK: Survival Ascended benotigt einen leistungsstarken Server mit mindestens 4 CPU-Kernen, 8 GB RAM und 50 GB SSD-Speicher. Fur 8-16 Spieler empfehlen sich 6 Kerne und 16 GB RAM.'),
            ('Kann ich ARK auf einem VPS hosten?',
             'Ja, ein VPS mit dedizierten Ressourcen ist optimal fur ARK. Wichtig sind schnelle NVMe-SSDs und eine gute CPU (AMD EPYC oder Intel Xeon). Vermeide geteilte Hosting-Umgebungen.'),
            ('Wie viel RAM braucht ein ARK Server?',
             'Ein ARK Server belegt initial 4-6 GB RAM. Mit mehr Spielern, Mods und groeseren Welten steigt der Bedarf auf 8-16 GB.'),
            ('Welche Mods sind empfehlenswert fur ARK?',
             'Beliebte Mods sind: Structures Plus (S+), Awesome Spyglass, Dino Storage v2 und Super Spyglass. Achte auf Kompatibilitat mit der aktuellen ARK-Version.'),
            ('Wie sichere ich meinen ARK Server?',
             'Regelmaessige Backups der Weltdateien (ShooterGame/Saved/) sind essenziell. Aktiviere BattleEye fur Anti-Cheat und richte automatische Neustarts ein.')
        ]
    elif 'cs2' in filename_lower:
        return [
            ('Welche Anforderungen hat ein CS2 Server?',
             'CS2 (Counter-Strike 2) benoetigt mindestens 2 vCPU-Kerne und 4 GB RAM fuer einen 10-Slots-Server. Fuer 64-Slots oder Wettkampf-Server empfehlen sich 4 Kerne und 8 GB RAM.'),
            ('Wie installiere ich einen CS2 Server?',
             'Installiere den CS2 Dedicated Server ueber SteamCMD mit dem App-ID 740. Nach der Installation konfigurierst du server.cfg und startest den Server mit den gewuenschten Parametern.'),
            ('Welche Plugins brauche ich fuer meinen CS2 Server?',
             'Die wichtigsten Plugins sind: SourceMod (fuer Admin-Befehle), MetaMod (als Plugin-Layer), und Anti-Cheat-Tools. Fuer Wettkampf-Server empfehlen sich zusaetzlich Warmod und Tickrate-Enabler.'),
            ('Wie schuetze ich meinen CS2 Server vor Cheatern?',
             'Aktiviere VAC (Valve Anti-Cheat) und ergaenze durch externe Anti-Cheat-Loesungen. Richte regelmaessige Log-Analysen ein und installiere Plugin-basierte Cheat-Erkennung.'),
            ('Kann ich einen CS2 Server auf einem VPS mieten?',
             'Ja, ein VPS ist ideal fuer CS2. Waehle einen Anbieter mit niedriger Latenz zu deiner Zielregion. Achte auf DDoS-Schutz und mindestens 1 Gbit/s Anbindung.')
        ]
    elif 'domain' in filename_lower:
        return [
            ('Wie kaufe ich eine Domain?',
             'Eine Domain kaufst du bei einem Registrar wie Namecheap, Netcup, IONOS oder Cloudflare. Suche nach der gewuenschten Domain, pruefe die Verfuegbarkeit und schliesse den Kauf ab. Die Kosten liegen zwischen 5 und 20 Euro pro Jahr fuer .de-Domains.'),
            ('Was ist der Unterschied zwischen Domain-Registrar und Hosting?',
             'Der Registrar verwaltet die Domain-Registrierung und DNS-Eintraege. Das Hosting stellt den Speicherplatz und die Server-Ressourcen fuer deine Website bereit. Du kannst beides beim selben Anbieter oder getrennt haben.'),
            ('Wie richte ich DNS-Eintraege fuer meine Domain ein?',
             'DNS-Eintraege konfigurierst du im DNS-Manager deines Registrars. Die wichtigsten Eintraege sind: A-Record (zeigt auf die Server-IP), CNAME (fuer Subdomains), MX (fuer E-Mail) und TXT (fuer Verifizierungen).'),
            ('Brauche ich ein SSL-Zertifikat fuer meine Domain?',
             'Ja, SSL ist heute Pflicht. Kostenlose Zertifikate gibt es via Let\'s Encrypt, die automatisch alle 90 Tage erneuert werden. Viele Hoster bieten kostenlose SSL-Zertifikate im Paket an.'),
            ('Kann ich meine Domain zu einem anderen Anbieter umziehen?',
             'Ja, ein Domain-Transfer ist moeglich. Du benoetigst einen Auth-Code vom aktuellen Registrar, entsperrst die Domain und initiierst den Transfer beim neuen Anbieter. Der Vorgang dauert 5-7 Tage.')
        ]
    elif 'email' in filename_lower:
        return [
            ('Kann ich meinen eigenen E-Mail-Server hosten?',
             'Ja, du kannst einen eigenen E-Mail-Server auf einem VPS hosten. Du benoetigst eine Domain, einen VPS mit statischer IP und Software wie Postfix (SMTP), Dovecot (IMAP) und SpamAssassin.'),
            ('Welche Ports muss ich fuer E-Mail oeffnen?',
             'Fuer E-Mail werden folgende Ports benoetigt: SMTP (25, 587), IMAP (143, 993) und POP3 (110, 995). Viele Hosting-Anbieter blockieren Port 25 standardmaessig.'),
            ('Wie schuetze ich meinen E-Mail-Server vor Spam?',
             'Schuetze deinen Mailserver mit SPF, DKIM und DMARC DNS-Eintraegen. Installiere SpamAssassin oder Rspamd zur Spam-Erkennung und nutze Fail2ban zur Abwehr von Brute-Force-Angriffen.'),
            ('Welche Alternativen gibt es zum Selbsthosten von E-Mail?',
             'Alternativen sind: Managed E-Mail-Hosting (MXroute, Migadu), E-Mail-Provider (Fastmail, ProtonMail) oder der E-Mail-Dienst deines Webhosters.'),
            ('Wie viel kostet ein eigener E-Mail-Server?',
             'Ein eigener E-Mail-Server kostet ca. 5-10 Euro/Monat fuer einen VPS. Hinzu kommt Zeit fuer Einrichtung und Wartung. Die Kosten sind vergleichbar mit Managed E-Mail-Diensten.')
        ]
    elif 'gameserver' in filename_lower and 'mieten' in filename_lower:
        return [
            ('Was ist der Unterschied zwischen Gameserver-Miete und VPS?',
             'Beim Gameserver-Mieten bekommst du einen fertig konfigurierten Server mit Webinterface und Support. Ein VPS gibt dir einen virtuellen Root-Server, auf dem du Gameserver selbst installierst - guenstiger, aber aufwendiger.'),
            ('Wie finde ich den richtigen Gameserver-Anbieter?',
             'Achte auf Serverstandorte in deiner Naehe, DDoS-Schutz, 24/7-Support, einfaches Webinterface, Mod-Unterstuetzung und faire Preise.'),
            ('Welches Spiel passt zu welcher Server-Konfiguration?',
             'Minecraft und Terraria laufen schon auf kleinen Servern (2 Kerne, 2 GB RAM). ARK, Rust und 7 Days to Die brauchen mehr Leistung (4+ Kerne, 8+ GB RAM).'),
            ('Wie wichtig ist DDoS-Schutz fuer Gameserver?',
             'Sehr wichtig. Ohne DDoS-Schutz ist dein Server ein leichtes Ziel fuer Angriffe. Ein guter Anbieter bietet kostenlosen Basisschutz (bis zu 20 Gbit/s).'),
            ('Kann ich meinen Gameserver spaeter upgraden?',
             'Ja, die meisten Anbieter erlauben Upgrades ohne Datenverlust. Achte vor der Buchung auf skalierbare Tarife.')
        ]
    elif 'nextcloud' in filename_lower:
        return [
            ('Welche Hardware brauche ich fuer Nextcloud?',
             'Nextcloud laeuft auf einem VPS mit 2 vCPU-Kernen, 4 GB RAM und 50 GB Speicher. Fuer mehrere Nutzer (5+) empfehlen sich 4 Kerne und 8 GB RAM.'),
            ('Wie installiere ich Nextcloud auf einem VPS?',
             'Die Installation erfolgt per APT, Docker oder dem Nextcloud Snap. Der Docker-Weg ist am einfachsten: Nutze docker-compose mit Nextcloud, MariaDB/PostgreSQL und Redis.'),
            ('Welche Datenbank sollte ich fuer Nextcloud verwenden?',
             'MariaDB oder PostgreSQL sind beide geeignet. PostgreSQL bietet bessere Performance bei vielen Nutzern. SQLite ist nur fuer Testinstallationen geeignet.'),
            ('Wie mache ich regelmaessige Backups von Nextcloud?',
             'Backup der Datenbank (mysqldump/pg_dump) und des Datenverzeichnisses. Automatisiere die Backups per Cronjob und speichere sie extern (S3, Backblaze B2).'),
            ('Wie beschleunige ich meine Nextcloud-Instanz?',
             'Aktiviere Redis-Caching, deaktiviere unnötige Apps, verwende einen OPcache (PHP), optimiere die Datenbank und setze Nextcloud hinter einen Reverse-Proxy mit HTTP/2.')
        ]
    elif 'nginx-reverse-proxy-einrichten' in filename_lower:
        return [
            ('Was ist ein Reverse Proxy und wozu brauche ich ihn?',
             'Ein Reverse Proxy sitzt vor einem oder mehreren Backend-Servern und leitet Client-Anfragen weiter. Er bietet Vorteile wie Lastverteilung, SSL-Terminierung, Caching und Sicherheit.'),
            ('Wie installiere ich NGINX als Reverse Proxy?',
             'Installiere NGINX per apt (sudo apt install nginx), erstelle eine Konfigurationsdatei mit proxy_pass zur Backend-URL, aktiviere die Site und lade NGINX neu.'),
            ('Wie richte ich SSL mit Let\'s Encrypt fuer meinen NGINX Reverse Proxy ein?',
             'Installiere Certbot (sudo apt install certbot python3-certbot-nginx), fuehre sudo certbot --nginx aus und waehle die Domain aus. Die Verlaengerung erfolgt automatisch.'),
            ('Wie leite ich mehrere Dienste mit einem NGINX Reverse Proxy weiter?',
             'Definiere mehrere server-Bloecke oder location-Bloecke mit verschiedenen Domainnamen oder Pfaden. Jeder Block leitet an einen anderen Backend-Dienst weiter.'),
            ('Wie behebe ich einen 502 Bad Gateway Fehler unter NGINX?',
             'Ein 502 Bad Gateway bedeutet, dass der Backend-Dienst nicht erreichbar ist. Pruefe: Laeuft der Dienst? Ist der Port korrekt? Erlaubt die Firewall die Verbindung?')
        ]
    elif 'palworld' in filename_lower:
        return [
            ('Welche Hardware brauche ich fuer einen Palworld Server?',
             'Palworld benoetigt mindestens 4 CPU-Kerne und 8 GB RAM. Fuer 8-16 Spieler empfehlen sich 6 Kerne und 16 GB RAM. Das Spiel ist aktuell nicht optimal optimiert.'),
            ('Wie installiere ich einen Palworld Dedicated Server?',
             'Installiere den Palworld Dedicated Server ueber SteamCMD auf einem Windows- oder Linux-Server. Die Konfiguration erfolgt in der PalWorldSettings.ini.'),
            ('Welche Ports muessen fuer Palworld geoeffnet sein?',
             'Palworld benoetigt Port 8211 (UDP) fuer Spielerverbindungen und Port 27015 (UDP) fuer Steam-Query. Stelle sicher, dass diese Ports in der Firewall freigegeben sind.'),
            ('Wie lade ich Mods auf meinem Palworld Server?',
             'Palworld unterstuetzt Mods ueber UE4SS. Lade die Mod-Dateien herunter, entpacke sie in das Mods-Verzeichnis des Servers und starte den Server neu.'),
            ('Wie optimiere ich die Performance meines Palworld Servers?',
             'Reduziere die Sichtweite in der PalWorldSettings.ini, begrenze die maximale Spielerzahl und starte den Server taeglich neu. Ein schneller NVMe-Speicher verbessert die Ladezeiten deutlich.')
        ]
    elif 'satisfactory' in filename_lower:
        return [
            ('Welche Hardware brauche ich fuer einen Satisfactory Server?',
             'Ein Satisfactory Server benoetigt mindestens 4 CPU-Kerne und 6 GB RAM. Fuer mehrere gleichzeitige Spieler empfehlen sich 6 Kerne und 12 GB RAM.'),
            ('Kann ich Satisfactory auf einem VPS hosten?',
             'Ja, Satisfactory laeuft gut auf einem VPS. Du installierst den Dedicated Server via SteamCMD. Waehle einen VPS mit guter Single-Core-Performance.'),
            ('Wie viele Spieler passen auf einen Satisfactory Server?',
             'Standardmaessig unterstuetzt Satisfactory bis zu 4 Spieler. Mit optimierten Einstellungen und leistungsstarker Hardware sind auch 8 Spieler moeglich.'),
            ('Wie installiere ich Mods auf meinem Satisfactory Server?',
             'Satisfactory unterstuetzt Mods via SML (Satisfactory Mod Loader). Installiere SML auf dem Server und lege die Mod-Dateien im Mods-Ordner ab.'),
            ('Wie mache ich Backups vom Satisfactory Server?',
             'Sichere regelmaessig das Savegame-Verzeichnis des Servers. Automatisiere Backups per Cronjob und speichere sie extern. Besonders vor grossen Updates ist ein Backup wichtig.')
        ]
    elif 'valheim' in filename_lower:
        return [
            ('Welche Hardware brauche ich fuer einen Valheim Server?',
             'Valheim benoetigt mindestens 2 vCPU-Kerne, 4 GB RAM und 10 GB Speicher. Fuer 5-10 Spieler empfehlen sich 4 Kerne und 8 GB RAM. Das Spiel laeuft sehr gut auf Linux.'),
            ('Wie installiere ich einen Valheim Server?',
             'Installiere den Valheim Dedicated Server ueber SteamCMD. Nutze das Valheim-Installationsskript oder richte den Server manuell mit systemd ein.'),
            ('Welche Ports muss ich fuer Valheim oeffnen?',
             'Valheim nutzt Port 2456-2458 (UDP) fuer Spielerverbindungen. Stelle sicher, dass diese Ports in der Firewall freigegeben sind.'),
            ('Wie installiere ich Valheim-Mods auf dem Server?',
             'Valheim-Mods werden ueber BepInEx geladen. Installiere BepInEx auf dem Server und lege die Mod-DLLs im Plugins-Ordner ab. Alle Spieler brauchen die gleichen Mods.'),
            ('Wie sorge ich fuer optimale Performance?',
             'Aktiviere den Valheim Performance-Optimizer, verwende einen Linux-VPS statt Windows, aktualisiere regelmaessig und starte den Server taeglich neu.')
        ]
    else:
        return [
            (f'Was ist {title.split("|")[0].strip()}?',
             f'{title.split("|")[0].strip()} ist ein Setup-Guide, der dir hilft, die richtige Konfiguration fuer dein Projekt zu finden. Der Artikel behandelt die wichtigsten Aspekte wie Anforderungen, Installation und Optimierung.'),
            ('Welche Voraussetzungen brauche ich?',
             'Die genauen Voraussetzungen variieren je nach Projekt. Grundsaetzlich benoetigst du einen VPS oder Root-Server mit Linux (vorzugsweise Ubuntu 22.04/24.04 LTS), Root-Zugriff und grundlegende Kenntnisse in der Kommandozeile.'),
            ('Wie viel kostet die Umsetzung?',
             'Die Kosten haengen von deinen Anforderungen ab. Ein Einsteiger-VPS beginnt bei ca. 5-10 Euro/Monat. Fuer groessere Projekte mit mehr Ressourcenbedarf solltest du 20-50 Euro/Monat einplanen.'),
            ('Welche Sicherheitsmassnahmen sollte ich beachten?',
             'Wichtige Sicherheitsmassnahmen sind: SSH-Zugriff nur mit Schluesseln, Firewall-Konfiguration (UFW/iptables), regelmaessige Sicherheitsupdates, Fail2ban und ein Monitoring-Tool.'),
        ]


def build_faqpage_schema(pairs):
    """Build FAQPage JSON-LD string from question/answer pairs."""
    items = []
    for q, a in pairs:
        q_esc = q.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        a_esc = a.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        items.append(f'    {{\n      "@type": "Question",\n      "name": "{q_esc}",\n      "acceptedAnswer": {{\n        "@type": "Answer",\n        "text": "{a_esc}"\n      }}\n    }}')
    
    items_str = ',\n'.join(items)
    
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{items_str}
    ]
  }}
  </script>'''


def process_article(filepath, filename, generate_faq=False):
    """Process a single article: extract/generate FAQ and inject schema."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if FAQPage already exists
    if 'FAQPage' in content:
        print(f"  \u23ed\ufe0f  FAQPage already exists: {filename}")
        return False
    
    # Try to extract FAQ pairs
    pairs = []
    
    if not generate_faq:
        pairs = extract_faq_pairs_generic(content)
        if not pairs:
            pairs = extract_troubleshooting_pairs(content)
    
    if not pairs and generate_faq:
        pairs = generate_faq_from_content(content, filename)
    
    if not pairs:
        print(f"  \u26a0\ufe0f  No FAQ pairs found: {filename}")
        return False
    
    # Filter and validate pairs
    valid_pairs = []
    for q, a in pairs:
        q_clean = clean_text(q)
        a_clean = clean_text(a)
        if q_clean and a_clean and len(q_clean) >= 5 and len(a_clean) >= 10:
            valid_pairs.append((q_clean, a_clean))
    
    if len(valid_pairs) < 2:
        print(f"  \u26a0\ufe0f  Too few valid FAQ pairs ({len(valid_pairs)}): {filename}")
        return False
    
    # Limit to 5 pairs
    valid_pairs = valid_pairs[:5]
    
    # Build schema
    schema = build_faqpage_schema(valid_pairs)
    
    # Inject before </head>
    head_close = '</head>'
    if head_close in content:
        content = content.replace(head_close, f'\n{schema}\n{head_close}', 1)
    else:
        head_close = '</HEAD>'
        if head_close in content:
            content = content.replace(head_close, f'\n{schema}\n{head_close}', 1)
        else:
            print(f"  \u274c  No </head> found: {filename}")
            return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  \u2705  Added {len(valid_pairs)} FAQ pairs: {filename}")
    return True


def main():
    print("=" * 60)
    print("Adding FAQPage JSON-LD Schema to hostazar Articles")
    print("=" * 60)
    
    # Reset files that were modified in the first run
    for fname in FAQ_ARTICLES + SETUP_ARTICLES:
        filepath = os.path.join(ARTICLES_DIR, fname)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            # Remove FAQPage schema if it was already added
            content = re.sub(
                r'\n  <script type="application/ld\+json">\n  \{\n    "@context": "https://schema.org",\n    "@type": "FAQPage",\n.*?\n  </script>\n</head>',
                '\n</head>',
                content, flags=re.DOTALL
            )
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
    
    success_count = 0
    fail_count = 0
    
    all_articles = [(fname, False) for fname in FAQ_ARTICLES]
    all_articles += [(fname, True) for fname in SETUP_ARTICLES]
    
    print(f"\nProcessing {len(all_articles)} articles...\n")
    
    for fname, generate in all_articles:
        filepath = os.path.join(ARTICLES_DIR, fname)
        if not os.path.exists(filepath):
            print(f"  \u274c  File not found: {fname}")
            fail_count += 1
            continue
        
        try:
            result = process_article(filepath, fname, generate)
            if result:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"  \u274c  Error processing {fname}: {e}")
            fail_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"Summary: {success_count} articles updated, {fail_count} failed/total")
    print(f"{'=' * 60}")


if __name__ == '__main__':
    main()
