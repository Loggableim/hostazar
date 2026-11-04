# Frontend Quality Pass 2026-11 (Branch `frontend/quality-2026-11`)

## Vorher (main, vor diesem Branch)

| Check | Ergebnis |
|-------|----------|
| Render-blocking AdSense (`async src=pagead…`) | 3 statische Seiten: `team.html`, `methodik.html`, `finanzierung.html` |
| Ad-Slot CLS | `.adsense-placeholder` ohne feste Mindesthöhe |
| Generator-Templates | AdSense-Loader und Platzhalter dupliziert, hardcoded `ca-pub-909491618868532` in `build_megapage_v2.py` / `publish_article.py` |
| Consent + AdSense | `page_shell` in `build_megapage_v2.py` ohne `consent-manager.js` |
| Artikel ohne `<main>` | 18 Legacy-HTMLs (engl./MiniMax-Importe) |
| H1 pro Artikel | 227/227 mit genau einer H1 |
| Interne Links (Stichprobe `minecraft-server-vergleich-2026.html`) | 0 kaputt |
| `style.css` | ~23 KiB |

## Nachher (dieser Branch)

| Check | Ergebnis |
|-------|----------|
| Render-blocking AdSense | **0** (Check `scripts/frontend_quality_check.sh` Exit 0) |
| Ad-Slot CLS | `.ad-slot--responsive` + `min-height` auf `.adsense-placeholder`, `contain: layout` |
| Shared Template | `scripts/site_template.py` — Platzhalter `ca-pub-XXXXXXXXXXXXXXXX`, `data-hz-src`-Loader, Ad-Slots mit `<ins class="adsbygoogle">` |
| Consent | `consent-manager.js` lädt AdSense nach Einwilligung inkl. `adsbygoogle.push` |
| Generator angebunden | `build_megapage_v2.py`, `publish_article.py`, `generate_batch.py`, `generate_batch_standalone.py`, `generate_batch_v2.py` |
| Statische Seiten | `team.html`, `methodik.html`, `finanzierung.html`: deferred AdSense + Consent-Banner |
| Artikel ohne `<main>` | weiterhin 18 (Inhalt/Jonas, nicht Template-Rebuild) |

## Geänderte Dateien

- `css/style.css` — Ad-Slot-Styles, CLS-Reserve
- `js/consent-manager.js` — AdSense push nach Script-Load
- `scripts/site_template.py` — **neu**, zentraler HTML-Fragment-Export
- `scripts/build_megapage_v2.py` — Template + Consent-Footer
- `scripts/publish_article.py` — gleiches Muster
- `scripts/generate_batch.py`, `generate_batch_standalone.py`, `generate_batch_v2.py` — Ad-Slots + deferred Loader
- `scripts/frontend_quality_check.sh` — **neu**, Vorher/Nachher-Audit
- `team.html`, `methodik.html`, `finanzierung.html` — Performance/Consent

## Abnahme

```bash
bash scripts/frontend_quality_check.sh   # Exit 0 (18 WARN für fehlendes <main> in Legacy-Artikeln)
```

**Gate-Skripte (`analyze_articles.sh`) nicht geändert** — liegen bei Tarek. Auf `main` melden die Gates weiter rot (363 Verstöße); dieser Branch ändert nur Templates/Shell, nicht alle 227 Artikel-HTMLs.

Kein Merge, kein Deploy.

## Offen

- 18 Legacy-Artikel auf `<main class="article-page">`-Shell migrieren (eigener Content-Pass oder `build_megapage_v2.py --articles` mit Vorsicht).
- Echte Publisher-ID für `ads.txt` / Ersetzen des Platzhalters in `site_template.py` nach Freigabe durch Levin/Cid.
