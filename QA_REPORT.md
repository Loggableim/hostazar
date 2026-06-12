# QA Report — hostazar.com

**Datum:** 2026-06-11 | **Tester:** Subagent (Verifikation)  
**Projekt:** hostazar.com Blog Automation  
**Build:** `build_megapage_v2.py` (letzter Durchlauf: 2026-06-11)

---

## Test 1: Artikelzählung & Wortzahl

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| Artikel gesamt | ✅ 149 | 149 HTML-Dateien in `artikel/` |
| Artikel mit >800 Wörtern | ✅ 149 (100%) | Alle Artikel erfüllen Mindestwortzahl |
| Durchschnittliche Wortzahl | ⚠️ Nicht geprüft | Keine Aggregatberechnung durchgeführt |

## Test 2: H1-Tags

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| Artikel mit H1 | ❌ 14/149 (9.4%) | Nur 14 von 149 haben `<h1>`-Tag |
| Artikel ohne H1 | 135/149 (90.6%) | Massives SEO-Problem |
| Verlorene H1 durch Build | 5 Tags | ai-agent-frameworks, baldurs-gate-3, hostinger-review, istio-service-mesh, phasmophobia-server-mieten |

**Bewertung:** ❌ NICHT BESTANDEN — H1 ist kritisches SEO-Element

## Test 3: Zukunftsdaten

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| Daten nach 2026-06-11 | ✅ 0 | Keine Datumsangaben nach heute |
| Heutige Daten (2026-06-11) | ⚠️ Normal | Viele Artikel auf heute datiert |
| Daten in 2025 | ⚠️ 3 Artikel | devops-tools-2024 (2025-05-12), gameserver-mieten-guide (2025-05-28), webhosting-vserver-vergleich (2025-05-20) |

**Bewertung:** ✅ BESTANDEN

## Test 4: Sitemap-Validität

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| Sitemap-URLs gesamt | 157 | Nach v2-Build |
| URLs im .html-Format | ✅ 157/157 | Korrekte URLs |
| URLs → existierende Dateien | ✅ 157/157 | Alle URLs zeigen auf gültige Dateien |
| Category-URLs (/gaming/, /devops/, etc.) | ✅ 4/4 | Existieren als `*/index.html` |

**Bewertung:** ✅ BESTANDEN

## Test 5: robots.txt

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| robots.txt vorhanden | ✅ | `User-agent: *` + `Disallow:` |
| Sitemap-URL | ✅ | `https://hostazar.com/sitemap.xml` |
| Crawl-Delay | ❌ Fehlt | SEO-Agent behauptete "mit Crawl-Delay", aber nicht vorhanden |

**Bewertung:** ⚠️ BESTANDEN MIT EINSCHRÄNKUNG

## Test 6: Trust-Seiten

| Seite | Existiert | Größe | Status |
|-------|-----------|-------|--------|
| about.html | ✅ | 709.041 Bytes | ⚠️ Enthält alte Megapage-Inhalte |
| methodik.html | ❌ | — | Nicht erstellt |
| finanzierung.html | ❌ | — | Nicht erstellt |
| team.html | ❌ | — | Nicht erstellt |

**Bewertung:** ❌ NICHT BESTANDEN — 3 von 4 Trust-Seiten fehlen/fehlerhaft

## Test 7: Indizierungssignale

| Signal | Ergebnis | Details |
|--------|----------|---------|
| Canonical URLs | ✅ Alle | Auf allen Seiten vorhanden |
| meta robots | ✅ Alle | `index, follow` auf allen Seiten |
| Schema.org BreadcrumbList | ✅ 149/149 | Auf allen Artikelseiten |
| Schema.org Article | ✅ 149/149 | BlogPosting/Article Schema |
| OG:title | ✅ Alle | Auf allen Seiten |
| OG:description | ✅ Alle | Auf allen Seiten |
| OG:image (Artikel) | ✅ 149/149 | Hero-Bilder referenziert |
| OG:image (Legal) | ❌ 0/2 | impressum, datenschutz ohne OG:image |
| Twitter Cards | ✅ Alle | Konsistent mit OG-Tags |

**Bewertung:** ⚠️ BESTANDEN MIT EINSCHRÄNKUNG

## Test 8: Content Health

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| Mindestwortzahl (>800) | ✅ 149/149 | Alle bestehen |
| H1-Tag | ❌ 14/149 | 135 Artikel ohne H1 |
| main-Tag | ✅ 149/149 | Alle haben `<main>` |
| article-Tag | ✅ 135/149 | 14 ohne `<article>` |
| BreadcrumbList | ✅ 149/149 | Alle Artikel |
| Navigation | ✅ 149/149 | Mega-Navigation intakt |
| Footer | ✅ 149/149 | Mit allen 4 Kategorien |
| Cookie-Banner | ✅ 149/149 | Consent-Banner vorhanden |

**Bewertung:** ⚠️ BESTANDEN MIT EINSCHRÄNKUNGEN

## Test 9: Affiliate & Werbung

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| rel="sponsored" Attribute | ❌ 0/149 | Alle nach Build verloren |
| "werbefrei" statt "finanziert durch Affiliate" | ❌ 149/149 | QA-Fix überschrieben |
| "testbench-basiert" noch vorhanden | ❌ 149/149 | Trust-Fix überschrieben |
| AdSense Script | ✅ 149/149 | Auf allen Seiten |

**Bewertung:** ❌ NICHT BESTANDEN

## Test 10: Kategorie-Struktur

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| 4 Kategorien | ✅ | Gaming (45), Webhosting (24), DevOps (53), KI & LLM (27) |
| Category Hubs | ✅ 4/4 | gaming/, webhosting/, devops/, ki-llm/ |
| Index-Seite | ✅ | 149 Artikel gelistet |

**Bewertung:** ✅ BESTANDEN

## Test 11: Build-Prozess

| Kriterium | Ergebnis | Details |
|-----------|----------|---------|
| build_megapage_v2.py | ✅ Erfolgreich | Keine Fehler |
| Alle Seiten generiert | ✅ | index, 4 hubs, 149 artikel, 3 legal |
| Sitemap generiert | ✅ | 157 URLs |
| Laufzeit | ✅ ~5 Sekunden | Schnell |

**Bewertung:** ✅ BESTANDEN

---

## Gesamtbewertung

| Bereich | Score | Status |
|---------|-------|--------|
| Artikelerstellung | ⭐⭐⭐⭐⭐ 10/10 | ✅ |
| Datumskorrekturen | ⭐⭐⭐⭐⭐ 10/10 | ✅ |
| Sitemap | ⭐⭐⭐⭐⭐ 10/10 | ✅ |
| Kategorie-Struktur | ⭐⭐⭐⭐⭐ 10/10 | ✅ |
| Schema.org | ⭐⭐⭐⭐ 8/10 | ⚠️ (Author: Organization) |
| Indizierungssignale | ⭐⭐⭐⭐ 8/10 | ⚠️ (OG:image Legal fehlt) |
| Build-Prozess | ⭐⭐⭐⭐⭐ 10/10 | ✅ |
| Content Health | ⭐⭐ 4/10 | ❌ (H1, article-Tag) |
| Trust-Seiten | ⭐ 2/10 | ❌ (methodik/finanzierung/team fehlen) |
| Affiliate/Werbung | ⭐ 1/10 | ❌ (Alles überschrieben) |

**Gesamt:** ⭐⭐⭐ 60/100 — **BESTANDEN MIT VORBEHALT**

---

## Kritische Issues (MUSS behoben werden)

| # | Issue | Schwere | Betroffene Dateien |
|---|-------|---------|-------------------|
| 1 | H1-Tags fehlen | 🔴 Kritisch | 135 Artikel |
| 2 | about.html überdimensioniert | 🔴 Kritisch | about.html |
| 3 | "werbefrei" statt "finanziert durch Affiliate" | 🔴 Kritisch | 149 Artikel |
| 4 | methodik/finanzierung/team.html fehlen | 🟡 Hoch | 3 Dateien |
| 5 | Affiliate rel="sponsored" fehlt | 🟡 Hoch | 149 Artikel |
| 6 | Author Schema falsch | 🟡 Mittel | 149 Artikel + Schema |
| 7 | OG:image auf Legal-Seiten | 🟢 Niedrig | impressum.html, datenschutz.html |

---

## Detail-Ergebnisse

### Artikel mit H1 (14/149)
```
beste-gaming-monitore-2026.html
cloud-vs-dedicated-server-2026.html
deep-rock-galactic-server-mieten-2026.html
gaming-pc-selbst-bauen-2026.html
helldivers-2-server-hosten-2026.html
ki-gestuetzte-code-reviews-praxis-2026.html
ki-im-devops-einsatz-2026.html
lethal-company-server-mieten-2026.html
llm-sicherheit-prompt-injection-schutz-2026.html
managed-wordpress-hosting-vergleich-2026.html
phasmophobia-server-hosten-2026.html
pubg-server-mieten-2026.html
steam-deck-vs-asus-rog-ally-vs-lenovo-legion-go-2026.html
webhosting-sicherheit-ddos-schutz-waf-2026.html
```

### Artikel OHNE article-Tag (14/149)
```
ai-agent-frameworks-2026.html
baldurs-gate-3-server-mieten-2026.html
cloud-gpu-kosten-vergleich-2026.html
cloud-hosting-vs-shared-hosting.html
cloudflare-tunnel-einrichten.html
docker-llm-inference-container.html
elk-stack-log-management.html
gaming-pc-finanzieren.html
hostinger-review-2026.html
lamp-stack-vs-lemp-stack-vergleich-2026.html
llm-lokal-hosten-2026.html
nginx-reverse-proxy-einrichten-2026.html
postgresql-vps-optimierung.html
redis-cache-vps-einrichten-2026.html
```

---

## Empfehlungen

1. **H1-Fix-Script schreiben** — Aus dem Titel in artikel.json + Kategorie-Präfix automatisch H1 generieren und in alle 135 Artikel ohne H1 einfügen
2. **about.html neu schreiben** — Echte About-Seite erstellen (max 5KB), alte Megapage-Reste entfernen
3. **Global Replace "werbefrei"** → `"finanziert durch Affiliate"` in allen 149 Artikeln
4. **Trust-Seiten generieren** — methodik, finanzierung, team aus Templates
5. **Build-Script erweitern** — H1 aus artikel.json generieren, Author auf Person setzen, rel-Attribute erhalten
6. **OG:image für Legal-Seiten** — Standard-Bild setzen
