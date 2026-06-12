#!/bin/bash
# Batch-update category index pages
# gaming/index.html, webhosting/index.html, devops/index.html, ki-llm/index.html

BASE="/c/HermesPortable/home/scripts/blog-automation/hostazar"
PAGES="$BASE/gaming/index.html $BASE/webhosting/index.html $BASE/devops/index.html $BASE/ki-llm/index.html"

for f in $PAGES; do
  [ ! -f "$f" ] && continue
  modified=0

  # 1. Add consent-banner.css
  if grep -q '<link rel="stylesheet" href="/css/style.css">' "$f" && ! grep -q 'consent-banner.css' "$f"; then
    sed -i 's|<link rel="stylesheet" href="/css/style.css">|<link rel="stylesheet" href="/css/style.css">\n  <link rel="stylesheet" href="/css/consent-banner.css">|' "$f"
    modified=1
  fi

  # 2. Add consent-manager.js before </head>
  if ! grep -q 'consent-manager.js' "$f"; then
    sed -i 's|</head>|  <script src="/js/consent-manager.js" defer></script>\n</head>|' "$f"
    modified=1
  fi

  # 3. Add Cookies-Einstellungen in footer
  if grep -q 'href="/impressum.html">Impressum</a>' "$f" && ! grep -q 'Cookies-Einstellungen' "$f"; then
    sed -i 's|href="/impressum.html">Impressum</a>|href="/impressum.html">Impressum</a>\n          <li><a href="/datenschutz.html">Datenschutz</a></li>\n          <li><a href="#" onclick="window.hzWithdrawConsent();return false;">Cookies-Einstellungen</a>|' "$f"
    modified=1
  fi

  echo "$(basename $(dirname $f))/$(basename $f): $([ $modified -eq 1 ] && echo 'Updated' || echo 'Skipped')"
done
