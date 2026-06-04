#!/bin/bash
# Cross-reference articles with images

ARTIKEL_DIR="/c/HermesPortable/home/scripts/blog-automation/hostazar/artikel"
IMAGES_DIR="/c/HermesPortable/home/scripts/blog-automation/hostazar/images"

echo "=== ARTICLES WITH NO CORRESPONDING IMAGE FILE ==="
for f in "$ARTIKEL_DIR"/*.html; do
  filename=$(basename "$f")
  slug="${filename%.html}"
  imgfile="$IMAGES_DIR/${slug}.png"
  if [ ! -f "$imgfile" ]; then
    echo "MISSING IMG: $slug"
  fi
done

echo ""
echo "=== IMAGE FILES WITH NO CORRESPONDING ARTICLE ==="
for f in "$IMAGES_DIR"/*.png; do
  filename=$(basename "$f")
  slug="${filename%.png}"
  # Skip non-article images
  if [ "$slug" = "logo" ] || [ "$slug" = "favicon" ] || [[ "$slug" == logo_* ]] || [[ "$slug" == favicon_* ]]; then
    continue
  fi
  article="$ARTIKEL_DIR/${slug}.html"
  if [ ! -f "$article" ]; then
    echo "ORPHAN IMG: $filename"
  fi
done

echo ""
echo "=== DETAILED HERO IMAGE CHECK ==="
echo "Checking each article for a dedicated hero-image img tag in the article BODY..."

for f in "$ARTIKEL_DIR"/*.html; do
  filename=$(basename "$f")
  slug="${filename%.html}"
  
  # Read the body section to check for hero-image usage
  body_content=$(awk '/<body>/,/<\/body>/' "$f")
  
  # Check for img tag with hero-image class
  has_hero_class=$(echo "$body_content" | grep -i -c 'class="hero-image"')
  
  # Check for img tag referencing an image matching the article slug
  has_own_img=$(echo "$body_content" | grep -c "images/$slug")
  
  # Check for any img tag with images/ in body
  has_any_img=$(echo "$body_content" | grep -c 'src="images/')
  
  if [ "$has_own_img" -gt 0 ]; then
    echo "OWN_IMG|$slug"
  elif [ "$has_any_img" -gt 0 ]; then
    echo "HAS_IMG_OTHER|$slug|$has_any_img matches"
  else
    echo "NO_BODY_IMG|$slug"
  fi
done
