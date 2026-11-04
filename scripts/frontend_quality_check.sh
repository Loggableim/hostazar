#!/usr/bin/env bash
# Frontend quality audit for hostazar.com (POSIX, repo-root relative).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

issues=0
warn=0

note() { echo "$*"; }
fail() { note "FAIL: $*"; issues=$((issues + 1)); }
warn_line() { note "WARN: $*"; warn=$((warn + 1)); }

note "=== hostazar frontend quality check ==="
note "Root: $ROOT"
note ""

# 1) Render-blocking AdSense (should use data-hz-src)
rb=$(grep -rl 'async src=.*pagead2.googlesyndication.com' . \
  --include='*.html' 2>/dev/null | grep -v node_modules || true)
if [ -n "$rb" ]; then
  while IFS= read -r f; do
    fail "render-blocking AdSense in $f"
  done <<< "$rb"
else
  note "OK: no async AdSense loader in HTML"
fi

# 2) Articles: exactly one H1
for f in artikel/*.html; do
  [ -f "$f" ] || continue
  c=$(grep -oi '<h1[^>]*>' "$f" | wc -l)
  if [ "$c" -ne 1 ]; then
    fail "$f has $c H1 tags (expected 1)"
  fi
done
note "OK: H1 count scan finished"

# 3) Articles: main landmark
missing_main=0
for f in artikel/*.html; do
  if ! grep -q '<main' "$f"; then
    warn_line "no <main> in $f"
    missing_main=$((missing_main + 1))
  fi
done
note "Articles without <main>: $missing_main"

# 4) Template generators reference shared ad fragments
for s in scripts/build_megapage_v2.py scripts/publish_article.py scripts/site_template.py; do
  if [ ! -f "$s" ]; then
    fail "missing $s"
  fi
done
if grep -q 'site_template' scripts/build_megapage_v2.py && grep -q 'ad-slot--responsive' css/style.css; then
  note "OK: shared template + CLS ad-slot CSS present"
else
  fail "template/CSS ad-slot wiring incomplete"
fi

# 5) CSS size (performance baseline)
css_kb=$(($(wc -c < css/style.css) / 1024))
note "style.css size: ${css_kb} KiB"
if [ "$css_kb" -gt 120 ]; then
  warn_line "style.css > 120 KiB (${css_kb} KiB)"
fi

# 6) Viewport on key pages
for f in index.html team.html artikel/minecraft-server-vergleich-2026.html; do
  if ! grep -q 'name="viewport"' "$f"; then
    fail "missing viewport in $f"
  fi
done
note "OK: viewport on sample pages"

# 7) Internal artikel links spot-check (sample)
sample="$ROOT/artikel/minecraft-server-vergleich-2026.html"
links=$(grep -oE 'href="/artikel/[^"]+\.html"' "$sample" | sed 's/href="//;s/"//' | sort -u)
broken=0
while IFS= read -r href; do
  [ -z "$href" ] && continue
  path="${href#/}"
  if [ ! -f "$path" ]; then
    fail "broken link in sample: $href"
    broken=$((broken + 1))
  fi
done <<< "$links"
note "Sample internal links broken: $broken"

# 8) Images without alt in nav mega-menu (sample article)
empty_alt=$(grep -c 'alt=""' "$sample" || true)
note "Sample page img alt=\"\" count: $empty_alt (nav thumbs OK if decorative)"

note ""
note "=== Summary: $issues failure(s), $warn warning(s) ==="
exit $([ "$issues" -eq 0 ] && echo 0 || echo 1)
