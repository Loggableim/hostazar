#!/bin/bash
# Batch fix: Replace old cookie banner + AdSense in all article HTML files
# Run from repo root: bash scripts/batch_fix_legal.sh

REPO_ROOT="/c/HermesPortable/home/scripts/blog-automation/hostazar"
cd "$REPO_ROOT"

echo "=== Batch Legal Fix: Cookie Consent + AdSense Deferral ==="

# 1. Fix AdSense script: async → data-hz-src in article/*.html and category index pages
echo "Fixing AdSense scripts (async → data-hz-src)..."
find artikel devops gaming webhosting ki-llm -name '*.html' -type f | while read f; do
  # Replace the async script tag with data-hz-src version
  sed -i 's|<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>|<script data-hz-src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-909491618868532" crossorigin="anonymous"></script>|g' "$f"
  
  # Add consent-banner.css if not present
  if ! grep -q 'consent-banner.css' "$f"; then
    sed -i 's|<link rel="icon" type="image/x-icon" href="/favicon.ico">|<link rel="icon" type="image/x-icon" href="/favicon.ico">\n  <link rel="stylesheet" href="/css/consent-banner.css">|' "$f"
  fi

  # Add cookie-einstellungen link in footer if not present
  if ! grep -q 'Cookie-Einstellungen' "$f"; then
    sed -i 's|<a href="/datenschutz.html">Datenschutz</a>|<a href="/datenschutz.html">Datenschutz</a> &middot;\n        <a href="#" onclick="window.hzReopenBanner();return false;">Cookie-Einstellungen</a>|g' "$f"
  fi

  # Remove old cookie-banner HTML
  sed -i '/<div class="cookie-banner" id="cookieBanner">/,/<\/div>/d' "$f"
  
  # Add consent-manager.js script after data/script.js
  sed -i 's|<script src="/data/script.js" defer></script>|<script src="/data/script.js" defer></script>\n<script src="/js/consent-manager.js" defer></script>|g' "$f"
done

echo ""
echo "=== Done! ==="
echo "Fixed files in: artikel/, devops/, gaming/, webhosting/, ki-llm/"
