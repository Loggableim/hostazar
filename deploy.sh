#!/bin/bash
# Auto-Deploy Script — Blog Automation Framework
# Führt Qualitätsprüfung vor dem Deploy durch

cd "$(dirname "$0")"

echo "=== Qualitätsprüfung vor Deploy ==="

# 1. Artikel-Analyse
echo "--- Analyze Articles ---"
bash analyze_articles.sh
ANALYZE_EXIT=$?
if [ $ANALYZE_EXIT -ne 0 ]; then
  echo "❌ analyze_articles.sh fehlgeschlagen"
  exit 1
fi

# 2. H1-Tag-Prüfung
echo "--- H1-Tag Check ---"
missing_h1=0
for f in artikel/*.html; do
  if ! grep -q '<h1>' "$f"; then
    echo "MISSING H1: $f"
    missing_h1=$((missing_h1+1))
  fi
done
if [ "$missing_h1" -gt 0 ]; then
  echo "❌ $missing_h1 Artikel ohne H1-Tag gefunden"
  exit 1
fi
echo "✅ Alle Artikel haben H1-Tags"

# 3. HTML-Grundvalidierung
echo "--- HTML Validation ---"
errors=0
for f in *.html artikel/*.html; do
  if [ -f "$f" ]; then
    main_open=$(grep -c '<main' "$f" 2>/dev/null || echo 0)
    main_close=$(grep -c '</main>' "$f" 2>/dev/null || echo 0)
    if [ "$main_open" -ne "$main_close" ]; then
      echo "❌ Unclosed <main> in $f"
      errors=$((errors+1))
    fi
    h1_open=$(grep -c '<h1' "$f" 2>/dev/null || echo 0)
    h1_close=$(grep -c '</h1>' "$f" 2>/dev/null || echo 0)
    if [ "$h1_open" -ne "$h1_close" ]; then
      echo "❌ Unclosed <h1> in $f"
      errors=$((errors+1))
    fi
  fi
done
if [ "$errors" -gt 0 ]; then
  echo "❌ $errors HTML-Fehler gefunden"
  exit 1
fi
echo "✅ HTML-Grundprüfung bestanden"

# 4. Prüfung auf rel="sponsored" bei Amazon-Links
echo "--- Amazon Affiliate Links Check ---"
missing_sponsored=0
for f in artikel/*.html; do
  if grep -q 'amazon.de' "$f"; then
    if ! grep -q 'rel="sponsored' "$f"; then
      echo "MISSING sponsored: $f"
      missing_sponsored=$((missing_sponsored+1))
    fi
  fi
done
if [ "$missing_sponsored" -gt 0 ]; then
  echo "❌ $missing_sponsored Artikel ohne rel=sponsored auf Amazon-Links"
  exit 1
fi
echo "✅ Alle Amazon-Links haben rel=sponsored"

echo ""
echo "=== ✅ Alle Qualitätsprüfungen bestanden ==="
echo ""

# Nur bei Erfolg commiten und pushen
git add -A
git commit -m "Auto: Blog-Framework Update $(date +%Y-%m-%d)"
git push
echo "--- DEPLOYED ---"
