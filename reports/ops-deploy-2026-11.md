# Betriebsprüfung 2026-11-04

Basis: main 720ba994c8834a7412dee45854c95550fce60bb9. Kein Content-Branch übernommen.

## Ergebnis
227 Einträge in data/artikel.json, nicht 228. Sitemap und RSS werden deterministisch daraus generiert, jeweils 227 Artikel-URLs/Items. Fehlende Dateien, doppelte oder unsichere Slugs brechen die Generierung ab. Statische Seiten und Kategorien bleiben in der Sitemap, 404 wird ausgeschlossen.

Die strikten Gates melden auf main 363 Verstöße, Exitcode 1 (siehe ops-gates.log). Keine grüne Gesamtabnahme. Inhaltskorrekturen gehören in den Content-Pass. Titel/Description werden anhand geparster HTML-Texte und numerischer Längen geprüft. Interne Links müssen auf mindestens zwei verschiedene existierende andere Artikel zeigen.

Zwei Regressionstests erfolgreich: gültige Fixtures sowie isolierte Verstöße für H1, Title, Description, Affiliate-Links, interne Links, Tag-Balance und leeres Artikelverzeichnis. Siehe ops-tests.log. Python 3.13 in isoliertem Container; keine Python-Pakete erforderlich. Shell-Einstieg POSIX, Python 3 Voraussetzung.

## Änderungen
- scripts/analyze_articles.sh + .py: gemeinsame strikte Gates, ROOT relativ zur Skriptdatei.
- analyze_articles.sh: kompatibler Einstieg statt Windows-Pfaden.
- deploy.sh: reine Prüfung, kein automatisches git add/Commit/Push.
- scripts/generate_discovery.py: reproduzierbare XML-Generierung; --check erkennt veraltete Dateien.
- sitemap.xml/feed.xml: neu generiert, RSS ohne zufällige Laufzeitstempel.
- Workflow: Fehler nicht mehr verschluckt, Tests vor Gates, Branch/PR nur Qualität; Produktion nur main nach erfolgreicher Qualität. Feste Wrangler-Version; nur öffentliche Dateien werden veröffentlicht.
- 404.html, _redirects: Fehlerseite und kanonische Redirect-Regeln vorbereitet.
- _headers: kurze Cachezeiten für veränderliche Assets, Revalidierung für HTML.
- tests/test_ops.py und Prüfprotokolle.

## Offene Betriebsprüfung
ads.txt fehlt. Keine verifizierte Publisher-ID gefunden; keine ID erfunden. AdSense bleibt offen. Vorhandene CSP erlaubt nur eigene Scripts und blockiert externe Anzeigen; erst mit tatsächlicher Anzeigenintegration gezielt konfigurieren.

GitHub-Actions-Lauf, Cloudflare-Zugang, production-Umgebungsschutz sowie echte HTTP/HTTPS-Redirects und Live-404 wurden nicht verifiziert. Redirect-Dateien können zonenseitige HTTPS-Einstellungen nicht beweisen. Kein Merge, kein Live-Deploy. Vor Freigabe Content-Verstöße beseitigen und CI auf dem integrierten Stand grün prüfen. Für Freigabe vor jedem Produktionslauf sollte die production-Umgebung in GitHub erforderliche Reviewer haben; dies ist keine durch YAML allein garantierte Sperre.
