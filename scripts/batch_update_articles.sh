#!/bin/bash
# hostazar.com — Batch-Legal-Fix für alle HTML-Dateien
# Entfernt alte Cookie-Banner, ersetzt AdSense durch Consent-gesteuertes Laden
# Führt Datenschutz-Links und Cookie-Einstellungen im Footer ein
# Verwendung: bash scripts/batch_update_articles.sh

BASE="/c/HermesPortable/home/scripts/blog-automation/hostazar"
cd "$BASE"

echo "=== Batch Legal Fix: Cookie Consent + AdSense Deferral ==="
echo ""

TOTAL=0
UPDATED=0

find artikel devops gaming webhosting ki-llm -name '*.html' -type f | while read f; do
  TOTAL=$((TOTAL + 1))
  modified=0

  # 1. Add consent-banner.css after style.css or favicon
  if ! grep -q 'consent-banner.css' "$f"; then
    sed -i 's|<link rel="icon" type="image/x-icon" href="/favicon.ico">|<link rel="icon" type="image/x-icon" href="/favicon.ico">\n  <link rel="stylesheet" href="/css/consent-banner.css">|' "$f"
    modified=1
  fi

  # 2. Replace async AdSense script with data-hz-src version (no async since JS handles it)
  if grep -q '<script async src="https://pagead2.googlesyndication.com' "$f"; then
    sed -i 's|<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>|<script data-hz-src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>|' "$f"
    modified=1
  fi

  # 3. Ensure consent-manager.js is loaded (after data/script.js)
  if ! grep -q 'consent-manager.js' "$f"; then
    sed -i 's|<script src="/data/script.js" defer></script>|<script src="/data/script.js" defer></script>\n<script src="/js/consent-manager.js" defer></script>|' "$f"
    modified=1
  fi

  # 4. Add Cookie-Einstellungen link in footer (after Datenschutz link)
  if grep -q 'href="/datenschutz.html">Datenschutz</a>' "$f" && ! grep -q 'Cookie-Einstellungen' "$f"; then
    sed -i 's|href="/datenschutz.html">Datenschutz</a>|href="/datenschutz.html">Datenschutz</a> &middot;\n        <a href="#" onclick="window.hzReopenBanner();return false;">Cookie-Einstellungen</a>|' "$f"
    modified=1
  fi

  # 5. Remove old cookie-banner HTML block
  if grep -q 'class="cookie-banner" id="cookieBanner"' "$f"; then
    sed -i '/<div class="cookie-banner" id="cookieBanner">/,/<\/div>/d' "$f"
    modified=1
  fi

  if [ $modified -eq 1 ]; then
    UPDATED=$((UPDATED + 1))
    echo "Updated: $(basename "$f")"
  fi
done

echo ""
echo "Done. $UPDATED of $TOTAL files updated."
