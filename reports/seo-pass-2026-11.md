# SEO-/Content-Pass vom 4. November 2026

Basis: main, Commit 720ba99. Branch: content/seo-pass-2026-11. Kein Merge und kein Deploy.

## Ergebnis

227 HTML-Artikel geprüft (nicht 228). 20 Artikel vollständig überarbeitet: abgebrochene Anleitungen, unbelegte Messwerte, Preise und erfundene Hostazar-Angebote entfernt. Stattdessen konkrete Entscheidungshilfen, Testabläufe, Kurzantwort und je eine sichtbare FAQ mit passendem Schema. Je zwei manuell gewählte, vorhandene Artikelziele. Metadaten in data/artikel.json synchronisiert. Umfang: 6093 Wörter einschließlich Überschriften, Quellen und Linktexten. Die Texte sind bewusste kompakte Ratgeber, keine vollständigen Installationshandbücher. Keine eigenen Anbieter- oder Hardwaretests behauptet.

## Geänderte Artikel

- artikel/cloud-hosting-vs-shared-hosting.html (298 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/grafana-loki-log-aggregation-vps-2026.html (307 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/baldurs-gate-3-server-mieten-2026.html (309 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/satisfactory-server-mieten-oder-selbst-hosten-2026.html (299 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/deep-rock-galactic-server-mieten-2026.html (298 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/remote-work-tirol.html (301 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/lemp-stack-vps-einrichten-2026.html (304 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/phasmophobia-server-mieten-2026.html (305 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/steam-deck-vs-asus-rog-ally-vs-lenovo-legion-go-2026.html (304 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/docker-wordpress-hosten.html (311 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/devops-tools-2024.html (311 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/openvpn-server-vps-einrichten-2026.html (323 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/hostinger-review-2026.html (301 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/istio-service-mesh-2026.html (302 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/ai-agent-frameworks-2026.html (303 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/hugo-astro-static-site-vergleich-2026.html (305 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/domain-kaufen-einrichten-2026.html (314 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/docker-container-security-best-practices-2026.html (297 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/webhosting-vserver-vergleich.html (302 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.
- artikel/cloudflare-waf-einrichten-2026.html (299 Wörter): vollständiger Text, Title/Description, FAQ-Schema und interne Links.

Zusätzlich nur Affiliate-Kennzeichnung an sämtlichen betroffenen Amazon-Links in:

- artikel/ki-gestuetzte-code-reviews-praxis-2026.html: rel="sponsored nofollow" ergänzt, weitere rel-Werte erhalten.
- artikel/ki-im-devops-einsatz-2026.html: rel="sponsored nofollow" ergänzt, weitere rel-Werte erhalten.
- artikel/nginx-vs-apache-webserver-vergleich-2026.html: rel="sponsored nofollow" ergänzt, weitere rel-Werte erhalten.
- artikel/postgresql-vs-mysql-vergleich-2026.html: rel="sponsored nofollow" ergänzt, weitere rel-Werte erhalten.
- artikel/raspberry-pi-homelab-server-2026.html: rel="sponsored nofollow" ergänzt, weitere rel-Werte erhalten.

Weitere Dateien: data/artikel.json (Titel, Auszug, Lesezeit); scripts/audit_seo.cjs (lesende Bestandsprüfung); reports/seo-*.json und reports/seo-*.log (Befunde und Prüfbelege); dieser Bericht.

## Validierung und offene Abnahme

- Alle 20 Artikel bestehen Title 50–60, Description 120–155, genau eine H1, JSON-Syntax, Article/Breadcrumb vorhanden, sichtbare FAQ passend zum FAQPage-Schema, Tag-Verschachtelung im main sowie zwei vorhandene interne Ziele. Keine Google-Rich-Results-Prüfung oder AdSense-Freigabe erfolgt.
- Gesamter Bestand: keine doppelten Titles, keine JSON-Syntaxfehler, keine fehlenden sponsored/nofollow-Werte an erkannten Amazon-/amzn.to-Links.
- Verbleibend außerhalb des 20er-Passes: {"title-length":197,"meta-length":120,"article-schema":12,"internal-links":40,"breadcrumb-schema":16}. Fehlende FAQ außerhalb des Passes ist nicht pauschal ein Fehler.
- scripts/analyze_articles.sh existiert nicht; angeforderter Aufruf scheitert. Die vorhandene Datei analyze_articles.sh nutzt feste /c/HermesPortable/...-Pfade und untersucht hier nicht die realen Artikel.
- Nur der unveränderte Prüfteil von deploy.sh wurde in einer temporären Datei im Repository ausgeführt, vor git add/commit/push abgeschnitten. Exitcode 0, aber Fehlermeldungen zur alten Analyse und zu numerischen Vergleichen (grep -c plus echo 0). Daher ausdrücklich keine fehlerfreie oder belastbar grüne Deploy-Abnahme. Vollständiges Log liegt bei.
- Deployment-/Workflow-Dateien und bestehende Betriebsskripte bleiben im Zuständigkeitsbereich des Technikteams; keine Infrastrukturänderungen in diesem Branch.
- Externe Dokumentationen für Produktfunktionen geprüft. BSI-Link konnte wegen HTTP 403 nicht inhaltlich geprüft werden; die Tirol-Seite enthält daher keine konkreten Orts-, Verfügbarkeits- oder Preisbehauptungen.
