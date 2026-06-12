# Release Checklist — hostazar.com

**Datum:** 2026-06-11  
**Ziel:** Deployment hostazar.com → Cloudflare Pages

---

## ⬜ Phase 1: Pre-Flight Checks

- [x] **149 Artikel** vorhanden
- [x] **Alle Artikel mit >800 Wörtern** — ✅ (100%)
- [ ] **H1-Tags auf allen Artikelseiten** — ❌ (Nur 14/149)
- [ ] **H1-Tags nachträglich einfügen** — ⚠️ MUSS VOR DEPLOYMENT GEMACHT WERDEN
- [x] **BreadcrumbList Schema** — ✅ (149/149 Artikel)
- [x] **main-Tag** — ✅ (149/149 Artikel)
- [x] **Sitemap** — ✅ (157 URLs, .html-Format, valid)
- [x] **Sitemap-URLs zeigen auf existierende Dateien** — ✅
- [ ] **robots.txt mit Crawl-Delay** — ❌ (einfaches `Disallow:` ohne Delay)
- [x] **robots.txt grundsätzlich OK** — ✅ (Sitemap-URL vorhanden)
- [x] **Category Hubs (4/4)** — ✅

---

## ⬜ Phase 2: Trust & Legal

- [x] **impressum.html** — ✅ (8.544 Bytes, korrekt)
- [x] **datenschutz.html** — ✅ (12.471 Bytes, DSGVO-konform)
- [ ] **about.html** — ⚠️ Enthält alte Megapage-Inhalte (709KB), sollte bereinigt werden
- [ ] **methodik.html** — ❌ FEHLT
- [ ] **finanzierung.html** — ❌ FEHLT
- [ ] **team.html** — ❌ FEHLT
- [ ] **Author Schema auf Person (Dominik Rainer)** — ❌ Noch `Organization`
- [ ] **OG:image auf impressum.html** — ❌ Fehlt
- [ ] **OG:image auf datenschutz.html** — ❌ Fehlt

---

## ⬜ Phase 3: Content Quality

- [ ] **"werbefrei" → "finanziert durch Affiliate"** — ❌ Noch in 149 Artikeln
- [ ] **"testbench-basiert" entfernen** — ❌ Noch in 149 Artikeln
- [ ] **Affiliate-Link rel-Attribute** — ❌ Alle `rel`-Attribute fehlen
  - Soll: `rel="sponsored noopener noreferrer"`
- [x] **NEKPREIS → NEUKUNDENPREIS** — ✅
- [x] **Keine Zukunftsdaten (>2026-06-11)** — ✅
- [x] **Keine chinesischen Zeichen** — ✅

---

## ⬜ Phase 4: SEO & Indexierung

- [x] **Sitemap aktuell** — ✅ (157 URLs)
- [x] **robots.txt vorhanden** — ✅
- [ ] **robots.txt Crawl-Delay ergänzen** — ⚠️ Empfohlen
- [x] **Canonical URLs** — ✅ (Konsistent)
- [x] **Schema.org BreadcrumbList** — ✅ (Alle Seiten)
- [x] **Schema.org Article/BlogPosting** — ✅ (Alle 149 Artikel)
- [x] **OG:image auf Artikelseiten** — ✅
- [ ] **OG:image auf Legal-Seiten** — ❌ (impressum, datenschutz)
- [x] **index.html (Startseite)** — ✅ (82KB, 149 Artikel)

---

## ⬜ Phase 5: Build Verification

- [x] **build_megapage_v2.py ausgeführt** — ✅ (letzter Durchlauf)
- [x] **Keine Fehler beim Build** — ✅
- [x] **index.html generiert** — ✅
- [x] **Category Hubs generiert** — ✅ (4/4)
- [x] **Alle Artikelseiten generiert** — ✅
- [x] **Legal Pages generiert** — ✅
- [x] **Sitemap generiert** — ✅
- [ ] **Neue untracked Files prüfen** — ⚠️ Siehe git status

---

## ⬜ Phase 6: Deployment

- [ ] **Git Commit** — Noch ausstehend (172 modified files)
- [ ] **Commit Message** — z.B. `feat: Release 2026-06-11 — 149 Artikel, 4 Kategorien, v2 Build`
- [ ] **Push zu GitHub** — `git push origin main`
- [ ] **Cloudflare Pages Build** — Automatisch via GitHub Actions
- [ ] **Health Check nach Deployment** — URL: https://hostazar.com
- [ ] **Sitemap einreichen** — Google Search Console

---

## ⬜ Phase 7: Post-Deployment

- [ ] **Indexierungs-Status prüfen** — Google Search Console
- [ ] **Affiliate-Links testen** — 145+ Links
- [ ] **Schema.org Validierung** — Google Rich Results Test
- [ ] **Mobile-Friendly Test** — Google PageSpeed Insights
- [ ] **Ladezeit prüfen** — Insbesondere about.html (709KB!)
- [ ] **Consent-Banner testen** — Cookie-Einwilligung

---

## 🔴 Kritische Blockers (MUSS vor Deployment)

| # | Issue | Priority | Action Required |
|---|-------|----------|-----------------|
| 1 | **H1-Tags fehlen auf 135 Artikeln** | 🔴 HIGH | Nachträglich per Script einfügen |
| 2 | **about.html überdimensioniert (709KB)** | 🔴 HIGH | Bereinigen, echte About-Seite erstellen |
| 3 | **"werbefrei" statt "finanziert durch Affiliate"** | 🔴 HIGH | Global Replace in allen Artikeln |
| 4 | **methodik/finanzierung/team.html fehlen** | 🟡 MEDIUM | Erstellen (SEO + Trust-Signale) |
| 5 | **Affiliate rel-Attribute verloren** | 🟡 MEDIUM | Wiederherstellen |
| 6 | **Author Schema falsch (Organization)** | 🟡 MEDIUM | Auf Person (Dominik Rainer) ändern |
| 7 | **OG:image auf Legal-Seiten fehlt** | 🟢 LOW | Nachträglich ergänzen |

---

## Zusammenfassung

**Bereit für Deployment:** ❌ NEIN — 7 offene Items, davon 3 kritisch  
**Empfehlung:** Kritische Blockers (#1, #2, #3) vor Deployment beheben  
**Nächster Schritt:** H1-Fix-Script ausführen, about.html bereinigen, werbefrei-Replace
