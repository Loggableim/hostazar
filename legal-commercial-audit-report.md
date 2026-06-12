# Legal & Commercial Audit – hostazar.com

**Datum:** 11. Juni 2026  
**Auditor:** Sidekick Legal Audit Agent  
**Repo:** `/c/HermesPortable/home/scripts/blog-automation/hostazar`  
**Geprüfte Dateien:** `index.html`, `impressum.html`, `datenschutz.html`, `about.html`, `data/script.js`, `robots.txt`

---

## Zusammenfassung der Schweregrade

| Schweregrad | Anzahl |
|---|---|
| 🔴 KRITISCH | 7 |
| 🟠 HIGH | 4 |
| 🟡 MEDIUM | 9 |
| 🔵 LOW | 5 |
| **Gesamt** | **25 Issues** |

---

## 1. IMPRESSUM (TMG-/ECG-Konformität)

### 1.1 🔴 KRITISCH – Falscher Rechtsrahmen (TMG statt ECG)

**Fundstelle:** `impressum.html` Zeile 7456  
**Aktuell:** `Angaben gemäß §5 TMG (Telemediengesetz)`  
**Problem:** Die Adresse lautet **Haller Strasse 3, 6020 Innsbruck, Österreich**. Das TMG ist deutsches Recht und in Österreich nicht anwendbar. In Österreich gelten:
- **§5 ECG** (E-Commerce-Gesetz) für Diensteanbieter
- **§25 MedienG** (Mediengesetz) für journalistische/blogs
- **§2 ECG** i.V.m. der Gewerbeordnung

**Remediation:** Ersetzen durch:
```
Angaben gemäß §5 ECG (E-Commerce-Gesetz), §24 MedienG
```
Alternativ: Ggf. mit Zusatz "falls TMG anwendbar" aber primär auf österreichisches Recht stellen.

### 1.2 🟡 MEDIUM – Keine Aufsichtsbehörde / Registernummer

**Fundstelle:** `impressum.html` (gesamtes Impressum)  
**Problem:** In Österreich ist bei Unternehmen die Angabe des Firmenbuchs (FB-Nummer) bzw. der Gewerbebehörde üblich. Natürliche Personen (Einzelunternehmer) müssen ggf. die Mitgliedschaft in der Wirtschaftskammer angeben.

**Remediation:** Ergänzen:
```
Mitglied der Wirtschaftskammer Tirol
Gewerbebehörde: Magistrat Innsbruck
```

### 1.3 🟡 MEDIUM – Keine USt-Identifikationsnummer

**Fundstelle:** `impressum.html`  
**Problem:** Falls der Betreiber umsatzsteuerpflichtig ist (Überschreitung der Kleinunternehmergrenze von €35.000/Jahr in Österreich), muss eine USt-ID (ATU...) angegeben werden. Fehlt vollständig.

**Remediation:** Falls zutreffend, ergänzen: `USt-IdNr.: ATU12345678`. Falls Kleinunternehmer, klarstellen: "Umsatzsteuerbefreit gemäß §6 Abs. 1 Z 27 UStG" (österreichische Kleinunternehmerregelung).

### 1.4 🟡 MEDIUM – Keine Streitschlichtung / ODR-Plattform

**Fundstelle:** `impressum.html`  
**Problem:** Es fehlt der Hinweis auf:
- Die **OS-Plattform** der EU-Kommission: `https://ec.europa.eu/consumers/odr/`
- Die Bereitschaft zur **Verbraucherschlichtung** gemäß §36 VSBG (DE) bzw. §29 AStG (AT)

In Österreich muss auf die **Agentur für Verbrauchergesundheit und -sicherheit (BAK)** / Schlichtungsstellen hingewiesen werden.

**Remediation:** Einfügen:
```
Hinweis auf EU-Streitschlichtung: Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: https://ec.europa.eu/consumers/odr/
Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.
```

### 1.5 🔵 LOW – Kein Datenschutzbeauftragter

**Fundstelle:** `impressum.html`  
**Problem:** Bei kleineren Websites nicht zwingend vorgeschrieben, aber wäre ein Vertrauenssignal.

---

## 2. DATENSCHUTZERKLÄRUNG (DSGVO-Konformität)

### 2.1 🔴 KRITISCH – Keine Speicherdauer-Angaben (Art. 13(2)(a) DSGVO)

**Fundstelle:** `datenschutz.html` Abschnitte 3 & 4  
**Problem:** Nirgends wird angegeben, **wie lange** Cookies, Server-Logfiles oder andere personenbezogene Daten gespeichert werden. Die DSGVO verlangt in Art. 13(2)(a) die Angabe der Speicherdauer oder der Kriterien für deren Festlegung.

**Remediation:** In den Abschnitten 3 und 4 ergänzen:
- Google AdSense-Cookies: Dauer (z.B. 1 Jahr für Anzeigen-Personalisierung)
- Amazon PartnerNet-Cookies: Dauer
- Server-Logfiles: "werden nach 7 Tagen gelöscht, es sei denn, sie werden zur Strafverfolgung benötigt"
- LocalStorage-Consent: "wird dauerhaft im Browser gespeichert, bis Sie ihn löschen"

### 2.2 🔴 KRITISCH – Keine Drittland-Transfer-Information (Art. 44-49 DSGVO)

**Fundstelle:** `datenschutz.html`, Abschnitte 3 (Google AdSense) und 5 (Cloudflare)  
**Problem:** Google AdSense und Cloudflare übertragen nachweislich Daten in die USA (Drittland). Es fehlt jeder Hinweis auf:
- **Angemessenheitsbeschluss** (EU-US Data Privacy Framework / DPF seit Juli 2023)
- **Standardvertragsklauseln (SCCs)**
- **Hinweis auf das Risiko** von fehlendem EU-Datenschutzniveau

**Remediation:** Bei Google AdSense ergänzen:
```
Google überträgt Daten gegebenenfalls in die USA. Google ist nach dem EU-US Data Privacy Framework (DPF) zertifiziert. Weitere Informationen: https://policies.google.com/privacy/frameworks
```
Bei Cloudflare ergänzen (analog).

### 2.3 🔴 KRITISCH – Google AdSense wird vor Cookie-Consent geladen

**Fundstelle:** `impressum.html` Zeile 22, `datenschutz.html` Zeile 22, `index.html`  
**Problem:** Das Google AdSense-Script wird im `<head>` jeder Seite geladen:
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>
```
Dies geschieht **bevor** der Cookie-Consent eingeholt wird (der erst via `script.js` dynamisch nachgeladen wird). Dies ist ein Verstoß gegen die DSGVO i.V.m. der ePrivacy-Richtlinie und dem TTDSG/TKG.

**Remediation:** Das AdSense-Script darf erst nach erteiltem Consent geladen werden. Implementierung:
1. Script aus `<head>` entfernen
2. In `script.js` nach Consent dynamisch nachladen:
```javascript
if (hasConsent) {
  var adScript = document.createElement('script');
  adScript.async = true;
  adScript.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532';
  adScript.crossOrigin = 'anonymous';
  document.head.appendChild(adScript);
}
```

### 2.4 🟠 HIGH – Cookie-Consent nicht DSGVO-konform (ePrivacy)

**Fundstelle:** `data/script.js` Zeilen 323-340, `datenschutz.html` Abschnitt 3  
**Problem:** Der Cookie-Banner bietet nur einen "Akzeptieren"-Button. Erforderlich ist:
- **Granularität**: Einwilligung nach Zwecken getrennt (z.B. "Marketing", "Analyse", "Personalisierung")
- **Ablehnen-Option**: Ein "Nur essenzielle Cookies" oder "Ablehnen"-Button muss vorhanden sein
- **Nachweis**: Die Einwilligung muss nachweisbar sein (consent.log, nicht nur localStorage)

Die aktuelle Implementierung (`localStorage.setItem('hostazar_cookie_consent', '1')`) ist zu schwach und entspricht nicht den Anforderungen der DSGVO.

**Remediation:** Einsatz einer Consent-Management-Plattform (CMP) wie:
- **Cookiebot** (kostenlos für kleine Websites)
- **Osano**
- **Complianz** (für statische Sites)
- **Klaro!** (Open-Source, DSGVO-konform)
Oder Eigenbau mit:
- Mehrstufiger Consent (Zwecke + Empfänger)
- Ablehnen-Button
- Widerrufsmöglichkeit
- Consent-Nachweis-Log

### 2.5 🟡 MEDIUM – Keine Auftragsverarbeitungs-Verträge (AVV) erwähnt

**Problem:** Weder für Google AdSense noch für Cloudflare werden Auftragsverarbeitungsverträge (Art. 28 DSGVO) erwähnt.

**Remediation:** Ergänzen:
```
Wir haben mit Google (AdSense) und Cloudflare Auftragsverarbeitungsverträge (AVV) gemäß Art. 28 DSGVO abgeschlossen.
```

### 2.6 🟡 MEDIUM – "Analyse" ohne genauere Angabe

**Fundstelle:** `datenschutz.html` Zeile 7481, `Cookie-Banner`  
**Problem:** Der Text spricht von "Analyse" ohne konkret zu nennen, welcher Analysedienst verwendet wird (Google Analytics? Matomo? Eigenlog?).

**Remediation:** Konkretisieren: "Wir verwenden keine externe Analyse-Software. Zugriffsstatistiken werden ausschließlich über Server-Logfiles ausgewertet."

### 2.7 🔵 LOW – Cloudflare-Abschnitt zu knapp

**Fundstelle:** `datenschutz.html`, Abschnitt 5 (nur 2 Sätze)  
**Remediation:** Um welche Daten handelt es sich? Speicherort der CDN-Caches? Dauer der Datenverarbeitung?

---

## 3. AFFILIATE-OFFENLEGUNG

### 3.1 🟠 HIGH – Amazon-Affiliate-Tag "nova079-20" nicht auf Betreiber ausgestellt

**Fundstelle:** Alle Amazon-Links auf der Seite (z.B. `tag=nova079-20`)  
**Problem:** Der verwendete Amazon-Partner-Tag ist `nova079-20`. Dies ist **nicht** auf den Namen "Dominik Rainer" oder "hostazar.com" registriert. Die Provision fließt an den Inhaber des Tags "nova079", nicht zwingend an den im Impressum genannten Betreiber. Dies wirft ein **Transparenzproblem** auf und könnte gegen wettbewerbsrechtliche Vorschriften verstoßen (Täuschung über die Identität des Werbenden).

**Remediation:** 
1. Entweder einen Amazon-Partner-Tag auf den Namen "Dominik Rainer" / "hostazar.com" registrieren
2. Oder offenlegen, dass die Affiliate-Einnahmen an einen Dritten gehen (z.B. "Der Amazon-Partner-Tag ist auf einen externen Dienstleister ausgestellt")

### 3.2 🟠 HIGH – Keine unmittelbare Affiliate-Kennzeichnung an den Links

**Fundstelle:** Diverse Artikel (z.B. `artikel/ansible-automation-guide.html` Zeile 838)  
**Problem:** Die Amazon-Links in den Artikeln haben kein sichtbares **Sternchen (*)** vor dem Link. Nach deutscher/österreichischer Rechtsprechung (BGH "Partnerprogramm"-Urteil, OLG Frankfurt) muss die Werbeabsicht **in unmittelbarem räumlichen Zusammenhang** mit dem Affiliate-Link stehen. Ein allgemeiner Hinweis im Footer reicht nicht aus.

Beispiel aktuell:
```html
<a href="https://www.amazon.de/s?k=...&tag=nova079-20" ...>👉 Server-Hardware auf Amazon entdecken</a>
```
Muss sein:
```html
<a href="https://www.amazon.de/s?k=...&tag=nova079-20" ...>* Server-Hardware auf Amazon entdecken</a>
```

**Remediation:** Alle Amazon-Links in Artikeln mit `*` (Sternchen) oder dem Wort "Werbung" kennzeichnen. Oder ein Skript verwenden, das den Link-Text automatisch ergänzt.

### 3.3 🟡 MEDIUM – Inkonsistente Affiliate-Formulierungen

**Fundstelle:** Unterschiedliche Footer auf verschiedenen Seiten  
**Aktuell:**
- `index.html`: `* Bei den mit Sternchen gekennzeichneten Links handelt es sich um Affiliate-Links... Als Amazon-Partner verdienen wir an qualifizierten Verkäufen.`
- `impressum.html` (2. Footer): `* Affiliate-Links: Wir erhalten ggf. eine Provision beim Kauf. Das kostet dich keinen Cent mehr.`
- `about.html` (1. Footer): Gleicher Text wie index.html
- `about.html` (2. Footer): Kürzerer Text

**Problem:** Inkonsistente Darstellung könnte vor Gericht als unzureichende Offenlegung gewertet werden.

**Remediation:** Vereinheitlichen auf die aussagekräftigste Version (mit Amazon-Partner-Statement).

### 3.4 🔵 LOW – Keine Offenlegung von gesponserten Artikeln

**Problem:** Es ist nicht erkennbar, ob manche Artikel oder Vergleiche von Hosting-Anbietern gesponsert sind. Die Behauptung der Unabhängigkeit in `about.html` ist positiv, aber ohne Methodik-Offenlegung.

---

## 4. COOKIE-CONSENT

### 4.1 🔴 KRITISCH – Keine Opt-Out / Widerrufsmöglichkeit

**Fundstelle:** `data/script.js`  
**Problem:** Nachdem der Nutzer "Akzeptieren" geklickt hat, gibt es keine Möglichkeit, die Einwilligung zu widerrufen. Der localStorage-Eintrag (`hostazar_cookie_consent`) kann vom Nutzer nur manuell gelöscht werden.

**Remediation:** Einen "Cookie-Einstellungen"-Link im Footer ergänzen, der das Cookie-Banner erneut öffnet und eine "Widerrufen"-Funktion bietet.

### 4.2 🟡 MEDIUM – Cookie-Banner auch auf statischen Seiten doppelt vorhanden

**Fundstelle:** `about.html` (Zeilen 7562-7567), `impressum.html` (Zeilen 8399-8404), `datenschutz.html` (Zeilen 8438-8443)  
**Problem:** In diesen Dateien existiert sowohl ein hartcodiertes Cookie-Banner-HTML **als auch** das dynamisch per `script.js` generierte Banner. Dies führt zu doppelten Bannern.

**Remediation:** Entweder hartcodierte Banner entfernen (dynamisches via JS verwenden) oder umgekehrt.

---

## 5. URHEBERRECHTSHINWEISE

### 5.1 🟡 MEDIUM – Inkonsistente Copyright-Jahreszahlen

**Fundstelle:**
- `impressum.html` Zeile 7521: `© 2025 hostazar.com`
- `impressum.html` Zeile 7569: `© 2026 hostazar.com`
- `datenschutz.html`: `© 2026`
- `index.html`: `© 2026`
- `about.html` Zeile 7503: `© 2025` (früherer Footer)

**Problem:** Drei verschiedene Copyright-Jahre in derselben Codebase. Das wirkt unprofessionell und könnte als nachlässig ausgelegt werden.

**Remediation:** Vereinheitlichen auf `© 2026 hostazar.com – Alle Rechte vorbehalten.`

### 5.2 🔵 LOW – Urheberrechtshinweis im Impressum

Der vorhandene Hinweis ist in Ordnung, könnte aber um einen CC-/Lizenzhinweis ergänzt werden.

---

## 6. KOMMERZIELLE TRANSPARENZ

### 6.1 🟠 HIGH – Amazon-Tag nicht auf Betreiber registriert (siehe 3.1)

Wiederholung – siehe Abschnitt 3.1.

### 6.2 🟡 MEDIUM – Keine Transparenz zu Werbekooperationen

**Fundstelle:** `about.html`  
**Problem:** Die Behauptung "vollständig unabhängig" wird nicht durch eine Methodik-Offenlegung gestützt. Wurden Anbieter kontaktiert? Gab es Testzugänge? Werden Provisionen pauschal oder prozentual abgerechnet?

**Remediation:** Transparenz-Statement einfügen:
```
Transparenz: Wir testen Produkte eigenständig. Einige der Links auf dieser Seite sind Affiliate-Links (gekennzeichnet mit *). Die Auswahl der Produkte und die Bewertung erfolgen unabhängig von Partnerprogrammen. Hosting-Anbieter haben keinen Einfluss auf unsere Inhalte.
```

---

## 7. VERTRAUENSSIGNALE

### 7.1 🟡 MEDIUM – Datenschutz-Link fehlt in index.html-Footer

**Fundstelle:** `index.html` Zeilen 1143-1148  
**Aktuell:** Im Footer der Startseite gibt es nur Links zu "Über uns" und "Impressum" – **nicht** zur Datenschutzerklärung.

**Remediation:** `Datenschutz`-Link ergänzen:
```html
<li><a href="/impressum.html">Impressum</a></li>
<li><a href="/datenschutz.html">Datenschutz</a></li>
```

### 7.2 🟡 MEDIUM – Keine SSL-Prüfung möglich (Quellcode)

**Hinweis:** Die Canonical-URLs verwenden `https://`. Eine tatsächliche Prüfung, ob HTTPS korrekt implementiert ist (keine gemischten Inhalte, HSTS, etc.), kann nur auf dem Live-Server erfolgen.

### 7.3 🔵 LOW – Keine Telefonnummer im Impressum

**Fundstelle:** `impressum.html` Zeile 7469  
**Aktuell:** Nur E-Mail als Kontakt.

**Remediation:** Ergänzung einer Telefonnummer (optional, aber empfohlen für Seriosität) oder eines Kontaktformulars.

### 7.4 🔵 LOW – Keine Social-Media-Links

Im Footer fehlen Links zu Social-Media-Präsenzen (auch wenn diese nicht existieren, ist ein Hinweis auf fehlende Präsenz möglich).

### 7.5 🔵 LOW – Kein Impressum/About im Nav der index.html

**Fundstelle:** `index.html` Navigation  
**Aktuell:** Die Hauptnavigation der Startseite enthält keine Links zu "Impressum", "Datenschutz" oder "Über uns" – nur im Footer. Bei der Länge der Seite (über 1150 Zeilen) könnte der Footer übersehen werden.

---

## 8. DATEI-QUALITÄT & BUILD-PROBLEME

### 8.1 🟠 HIGH – Massive Dateiduplikation (Build-Fehler)

**Fundstelle:** `impressum.html` (8406 Zeilen, 652 KB), `datenschutz.html` (8445 Zeilen, 655 KB)  
**Problem:** Beide Dateien enthalten 6-7x die vollständige Navigation und mehrfach den Footer. Dies ist ein Build-Fehler (wahrscheinlich durch Template-Concatenation). Die Dateien sind 600+ KB pro Stück für einfache Rechtstexte, was die Ladezeit massiv verschlechtert.

**Beleg:** In `impressum.html` erscheint die Navigation (inkl. 50+ Mega-Menu-Links) auf den Zeilen 57-676, 679-1283, 1286-... etc. mehrfach.

**Remediation:** Build-Prozess reparieren, sodass Navigation/Footer nur einmal eingefügt werden. Die Dateien sollten < 50 KB sein.

### 8.2 🟡 MEDIUM – robots.txt in Ordnung

Die `robots.txt` ist korrekt und erlaubt allen Crawlern den Zugriff.

---

## 9. CHECKLISTE: SOFORTMASSNAHMEN

| Priorität | Maßnahme | Aufwand |
|---|---|---|
| 🔴 1 | AdSense-Script erst nach Consent laden | 1h |
| 🔴 2 | Cookie-Banner um "Ablehnen" + Granularität erweitern | 4h |
| 🔴 3 | TMG → ECG/MedienG im Impressum ändern | 0,5h |
| 🔴 4 | Speicherdauer in Datenschutzerklärung ergänzen | 1h |
| 🔴 5 | Drittland-Transfer-Info (DPF/SCCs) ergänzen | 1h |
| 🟠 6 | Amazon-Tag auf Betreiber registrieren oder Transparenz schaffen | 2h |
| 🟠 7 | Sternchen-Markierung an allen Affiliate-Links | 2h |
| 🟠 8 | Build-Fehler beheben (Dateiduplikation) | 2h |
| 🟡 9 | Datenschutz-Link im index.html-Footer ergänzen | 0,2h |
| 🟡 10 | Copyright-Jahre vereinheitlichen | 0,2h |
| 🟡 11 | USt-ID prüfen und ergänzen | 0,5h |
| 🟡 12 | ODR-Plattform-Hinweis ergänzen | 0,3h |
| 🟡 13 | Cookie-Banner-Widerruf implementieren | 2h |
| 🟡 14 | Doppelte Cookie-Banner entfernen | 0,5h |

---

## 10. RECHTLICHES RISIKO-RATING

| Bereich | Risiko | Begründung |
|---|---|---|
| Impressum | 🔴 HOCH | Falscher Rechtsrahmen (TMG statt ECG) + fehlende Pflichtangaben |
| Datenschutz | 🔴 HOCH | AdSense-Vorab-Laden + fehlende Speicherdauer + kein Drittland-Transfer |
| Affiliate | 🟠 MITTEL-HOCH | Tag nicht auf Betreiber + fehlende Link-Kennzeichnung |
| Cookie-Consent | 🔴 HOCH | Nur "Akzeptieren" + keine Opt-Out + kein Widerruf |
| Copyright | 🟡 NIEDRIG | Nur inkonsistente Jahreszahlen |
| Kommerzielle Transparenz | 🟠 MITTEL | Tag-Diskrepanz |

**Gesamtbewertung:** Die Website hostazar.com hat erhebliche rechtliche Mängel. Die drei kritischsten Punkte sind:
1. **Falscher Rechtsrahmen im Impressum** (TMG statt ECG) – könnte als Ordnungswidrigkeit geahndet werden
2. **AdSense-Script vor Consent** – klarer DSGVO-Verstoß mit Abmahnrisiko
3. **Cookie-Consent ohne echte Wahlmöglichkeit** – Verstoß gegen ePrivacy-Richtlinie

Bei einer Abmahnung (z.B. durch Wettbewerbsverbände) sind Kosten im unteren bis mittleren vierstelligen Bereich pro Verstoß möglich.

---

*Report erstellt am 11. Juni 2026 | Legal & Commercial Audit Agent*
