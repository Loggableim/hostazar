#!/bin/bash
# Analyze all article HTML files for hero images and H1 titles

ARTIKEL_DIR="/c/HermesPortable/home/scripts/blog-automation/hostazar/artikel"
IMAGES_DIR="/c/HermesPortable/home/scripts/blog-automation/hostazar/images"

echo "=== IMAGES IN IMAGES DIR ==="
ls -1 "$IMAGES_DIR" | sort

echo ""
echo "=== ARTICLES ANALYSIS ==="
total=0
missing=0

for f in "$ARTIKEL_DIR"/*.html; do
  filename=$(basename "$f")
  slug="${filename%.html}"
  total=$((total+1))
  
  # Read the file content
  content=$(cat "$f")
  
  # Check for hero-image class or images/ in img tags
  has_hero=$(echo "$content" | grep -i -c 'class="*hero-image"')
  has_images_in_img=$(echo "$content" | grep -c 'images/')
  
  # Extract H1 title (first <h1> tag content)
  h1=$(echo "$content" | grep -oP '<h1[^>]*>\K[^<]+' | head -1)
  
  # Extract <title> tag content as fallback
  title=$(echo "$content" | grep -oP '<title[^>]*>\K[^<]+' | head -1)
  
  if [ "$has_hero" -eq 0 ] && [ "$has_images_in_img" -eq 0 ]; then
    echo "MISSING|$filename|$slug|$h1|$title"
    missing=$((missing+1))
  else
    echo "OK|$filename|$slug|$h1|$title"
  fi
done

echo ""
echo "Total articles: $total"
echo "Missing hero image: $missing"
