#!/usr/bin/env python3
"""
Test script for build_megapage_v2.py fixes.
Verifies:
1. build_legal_pages() produces clean output (no navigation duplication)
2. Content extraction regex in build_all_articles() preserves H1+H2+Ps
"""
import os, sys, re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def test_legal_pages():
    """Test that legal pages have exactly ONE nav and ONE footer."""
    print('=' * 60)
    print('TEST 1: Legal pages — no navigation duplication')
    print('=' * 60)
    
    for fname in ('impressum.html', 'datenschutz.html', 'about.html'):
        path = os.path.join(BASE, fname)
        if not os.path.exists(path):
            print(f'  SKIP: {fname} not found')
            continue
        
        size = os.path.getsize(path)
        with open(path, encoding='utf-8') as f:
            content = f.read()
        
        nav_count = content.count('</nav>')
        footer_count = content.count('</footer>')
        main_count = content.count('<main')
        html_count = content.count('<html')
        
        # Expected: 1 navbar (<nav class="navbar">) + 1 breadcrumb (<nav class="breadcrumbs">) = 2
        # The old bug duplicated both, producing 15-30 navs per file.
        navbar_count = content.count('class="navbar"')
        breadcrumb_count = content.count('class="breadcrumbs"')
        footer_count = content.count('</footer>')
        main_count = content.count('<main')
        html_count = content.count('<html')
        
        is_full_html = html_count > 0
        
        if is_full_html:
            # Full page: should have exactly 1 navbar, 1 breadcrumb, 1 footer
            has_duplication = navbar_count != 1 or footer_count != 1
            status = '✗ FAIL (duplication!)' if has_duplication else '✓ OK'
            extra = f'{navbar_count} navbars, {breadcrumb_count} breadcrumbs, {footer_count} footers'
        else:
            # Pre-build: inner content only, no nav/footer
            has_extra = navbar_count > 0 or footer_count > 0
            status = '✗ FAIL (extra content)' if has_extra else '✓ OK (pre-build)'
            extra = f'inner content only'
        
        print(f'  {status} {fname}: {size:>7,} bytes, {extra}, '
              f'{main_count} <main>, {html_count} <html>')
    
    print()


def test_content_extraction():
    """Test that article content extraction preserves key HTML elements."""
    print('=' * 60)
    print('TEST 2: Content extraction regex — preserves H1+H2+Ps')
    print('=' * 60)
    
    # Find a sample article
    artikel_dir = os.path.join(BASE, 'artikel')
    if not os.path.exists(artikel_dir):
        print('  SKIP: artikel/ directory not found')
        return
    
    articles = [f for f in os.listdir(artikel_dir) if f.endswith('.html')]
    if not articles:
        print('  SKIP: No article files found')
        return
    
    sample = articles[0]
    sample_path = os.path.join(artikel_dir, sample)
    print(f'  Sample article: {sample}')
    
    with open(sample_path, encoding='utf-8') as f:
        raw = f.read()
    
    orig_size = len(raw)
    
    # Apply the FIXED regexes (same logic as in build_megapage_v2.py)
    # Priority 1: <main> tag
    content_match = re.search(
        r'<main[^>]*>(.*)</main>',
        raw, re.DOTALL | re.IGNORECASE
    )
    if not content_match:
        # Priority 2: <article> tag
        content_match = re.search(
            r'<article[^>]*>(.*?)</article>',
            raw, re.DOTALL | re.IGNORECASE
        )
    if not content_match:
        # Priority 3: div with article-content class
        content_match = re.search(
            r'<div[^>]*class="[^"]*article-content[^"]*"[^>]*>(.*)</div>',
            raw, re.DOTALL | re.IGNORECASE
        )
    
    if not content_match:
        print('  ✗ FAIL: No content match found!')
        return
    
    article_inner = content_match.group(1)
    extracted_size = len(article_inner)
    
    # Count preserved elements
    h1_count = article_inner.count('<h1')
    h2_count = article_inner.count('<h2')
    p_count = article_inner.count('<p')
    img_count = article_inner.count('<img')
    a_count = article_inner.count('<a ')
    
    # Check that H1+H2+Ps are present (meaningful content)
    status = '✓ OK' if (h1_count + h2_count) >= 1 and p_count >= 1 else '✗ FAIL'
    print(f'  {status} Extracted content: {orig_size:,} → {extracted_size:,} bytes')
    print(f'      H1: {h1_count}, H2: {h2_count}, <p>: {p_count}, <img>: {img_count}, <a>: {a_count}')
    
    # Verify no duplicate navs in extracted content
    nav_count = article_inner.count('</nav>')
    if nav_count > 0:
        print(f'  ⚠ WARN: Extracted content contains {nav_count} nav(s)')
    print()


def test_regex_old_vs_new():
    """Show how the old buggy regex fails vs the fixed regex."""
    print('=' * 60)
    print('TEST 3: Old regex vs new regex on sample HTML')
    print('=' * 60)
    
    sample_html = '''<!DOCTYPE html>
<html>
<body>
<nav>Nav content</nav>
<main class="article-page">
  <div class="container">
    <div class="article-meta-top"><span>Category</span><span>5 Min</span></div>
    <h1>Test Article Title</h1>
    <p>This is the first paragraph of the article content that should be extracted.</p>
    <h2>Section One</h2>
    <p>More content in section one with <a href="#">a link</a>.</p>
    <div class="code-block">some code</div>
    <h2>Section Two</h2>
    <p>Final paragraph content.</p>
  </div>
</main>
<section class="related-section"><h4>Related</h4></section>
<footer>Footer content</footer>
</body>
</html>'''
    
    # OLD buggy regex
    old_match = re.search(
        r'<(?:main|div[^>]*class=\"?article-content\"?[^>]*)>(.*?)</(?:main|div)>',
        sample_html, re.DOTALL | re.IGNORECASE
    )
    old_result = old_match.group(1) if old_match else 'NO MATCH'
    
    # NEW fixed regex
    new_match = re.search(
        r'<main[^>]*>(.*)</main>',
        sample_html, re.DOTALL | re.IGNORECASE
    )
    new_result = new_match.group(1) if new_match else 'NO MATCH'
    
    print(f'  Old regex extract length: {len(old_result)} chars')
    print(f'  New regex extract length: {len(new_result)} chars')
    print(f'  Old regex (first 100 chars): {old_result[:100]}')
    print(f'  New regex (first 100 chars): {new_result[:100]}')
    
    # Verify old regex was truncated (lazy match on first </div>)
    # The old regex with lazy (.*?) matching <main...>(.*?)</(?:main|div)>
    # would match up to the first </div> in the sample (</div> after article-meta-top)
    if '<h1>' not in old_result:
        print('  ✓ Old regex correctly identified as buggy (truncated content)')
    else:
        print('  ⚠ Old regex extracted full content (test HTML too simple)')
    
    if '<h1>Test Article Title</h1>' in new_result:
        print('  ✓ New regex preserves H1 heading')
    if '<p>This is the first paragraph' in new_result:
        print('  ✓ New regex preserves paragraphs')
    if '<div class="code-block">' in new_result:
        print('  ✓ New regex preserves inner divs')
    if '<section class="related-section">' not in new_result:
        print('  ✓ New regex correctly stops at </main> (excludes content after)')
    
    print()


if __name__ == '__main__':
    test_legal_pages()
    test_content_extraction()
    test_regex_old_vs_new()
    print('All tests completed.')
