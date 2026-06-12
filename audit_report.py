#!/usr/bin/env python3
"""Comprehensive Content & Data Integrity Audit for hostazar.com"""

import os
import re
import subprocess
import json
from datetime import datetime, date
from collections import defaultdict

REPO = r'C:\HermesPortable\home\scripts\blog-automation\hostazar'
ARTICLE_DIR = os.path.join(REPO, 'artikel')
IMAGE_DIR = os.path.join(REPO, 'images')

def get_git_log(article_path):
    """Get git log for a file"""
    try:
        result = subprocess.run(
            ['git', 'log', '--follow', '--format=%ai', '--', article_path],
            capture_output=True, text=True, cwd=REPO, timeout=10
        )
        lines = [l.strip() for l in result.stdout.split('\n') if l.strip()]
        return lines
    except Exception as e:
        return [f"ERROR: {e}"]

def count_words_in_file(filepath):
    """Count actual words in article body (excluding schema/metadata)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Remove script/style tags
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', ' ', content)
        # Remove schema JSON
        content = re.sub(r'\{.*?"@context".*?\}', '', content, flags=re.DOTALL)
        # Decode HTML entities
        content = content.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        # Count words
        words = content.split()
        return len(words)
    except Exception as e:
        return -1

def extract_date_published(filepath):
    """Extract datePublished from schema"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'"datePublished":\s*"([^"]+)"', content)
    return m.group(1) if m else None

def extract_word_count_schema(filepath):
    """Extract wordCount from schema"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'"wordCount":\s*(\d+)', content)
    return int(m.group(1)) if m else None

def extract_image_refs(filepath):
    """Extract image src references from article"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    refs = re.findall(r'src="images/([^"]+)"', content)
    refs += re.findall(r"src='images/([^']+)'", content)
    return list(set(refs))

def extract_internal_links(filepath):
    """Extract internal links to other articles"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'href="(\.\./artikel/[^"]+)"', content)
    links += re.findall(r"href='(\.\./artikel/[^']+)'", content)
    links += re.findall(r'href="(/artikel/[^"]+)"', content)
    links += re.findall(r"href='(/artikel/[^']+)'", content)
    # Normalize: remove leading ../ or /
    normalized = []
    for l in links:
        l = l.replace('../', '').replace('/', '')
        if l.startswith('/artikel/'):
            l = l[1:]  # remove leading /
        normalized.append(l)
    return list(set(normalized))

def check_article_year_consistency(filepath):
    """Check if there's a mismatch between filename year and content mentions"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    filename = os.path.basename(filepath)
    years_in_content = set(re.findall(r'\b(202[0-9])\b', content))
    years_in_filename = set(re.findall(r'(202[0-9])', filename))
    all_years = years_in_content | years_in_filename
    return {
        'years_in_filename': years_in_filename,
        'years_in_content': years_in_content,
        'all_years': all_years
    }

# ============================================================
# MAIN AUDIT
# ============================================================

print("=" * 80)
print("  HOSTAZAR.COM — VOLLSTÄNDIGES CONTENT & DATA INTEGRITY AUDIT")
print(f"  Datum: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 80)

# Collect all article files
articles = sorted([f for f in os.listdir(ARTICLE_DIR) if f.endswith('.html')])
print(f"\n📊 ARTIKEL GEFUNDEN: {len(articles)}")

# Collect all image files from disk
images_on_disk = set(os.listdir(IMAGE_DIR))
print(f"📊 BILDER AUF DISK: {len(images_on_disk)}")

# ============================================================
# 1. DATE ACCURACY AUDIT
# ============================================================
print("\n" + "=" * 80)
print("  🔍 1. DATUMSGENAUIGKEIT (datePublished vs Git-Timestamps)")
print("=" * 80)

date_issues = []
for article in articles:
    filepath = os.path.join(ARTICLE_DIR, article)
    date_pub = extract_date_published(filepath)
    git_dates = get_git_log(filepath)
    first_commit = git_dates[-1] if git_dates else "N/A"
    last_commit = git_dates[0] if git_dates else "N/A"
    
    if date_pub:
        try:
            pub_dt = datetime.strptime(date_pub, '%Y-%m-%d')
            today = datetime.now()
            # Check if in future
            if pub_dt > today:
                date_issues.append({
                    'article': article,
                    'datePublished': date_pub,
                    'last_git_commit': last_commit.split()[0] if last_commit != "N/A" else "N/A",
                    'first_git_commit': first_commit.split()[0] if first_commit != "N/A" else "N/A",
                    'issue': '📅 FUTURE DATE - datePublished liegt in der Zukunft'
                })
            elif first_commit != "N/A":
                fc = first_commit.split()[0]
                if fc != "N/A":
                    fc_dt = datetime.strptime(fc, '%Y-%m-%d')
                    diff = (pub_dt - fc_dt).days
                    if diff > 3:
                        date_issues.append({
                            'article': article,
                            'datePublished': date_pub,
                            'last_git_commit': last_commit.split()[0] if last_commit != "N/A" else "N/A",
                            'first_git_commit': fc,
                            'issue': f'⚠️ datePublished ({date_pub}) ist {diff} Tage NACH erstem Git-Commit ({fc})'
                        })
        except:
            pass

for issue in date_issues:
    sev = "🔴 KRITISCH" if "FUTURE" in issue['issue'] else "🟡 WARNUNG"
    print(f"\n  {sev}: {issue['article']}")
    print(f"    datePublished: {issue['datePublished']}")
    print(f"    Letzter Commit: {issue['last_git_commit']}")
    print(f"    Erster Commit: {issue['first_git_commit']}")
    print(f"    {issue['issue']}")

if not date_issues:
    print("  ✅ Keine Datums-Unstimmigkeiten gefunden.")

# ============================================================
# 2. WORD COUNT ACCURACY
# ============================================================
print("\n" + "=" * 80)
print("  🔍 2. WORDCOUNT GENAUIGKEIT (Schema vs Tatsächlich)")
print("=" * 80)

wc_issues = []
wc_details = []
for article in sorted(articles):
    filepath = os.path.join(ARTICLE_DIR, article)
    schema_wc = extract_word_count_schema(filepath)
    actual_wc = count_words_in_file(filepath)
    if schema_wc and actual_wc > 0:
        diff = abs(schema_wc - actual_wc)
        diff_pct = round(diff / actual_wc * 100, 1) if actual_wc > 0 else 0
        wc_details.append((article, schema_wc, actual_wc, diff, diff_pct))
        if diff > 200:
            wc_issues.append((article, schema_wc, actual_wc, diff, diff_pct))

print(f"\n  {'Artikel':<60} {'Schema':<8} {'Tatsächlich':<12} {'Diff':<8} {'%'}")
print(f"  {'-'*60} {'-'*8} {'-'*12} {'-'*8} {'-'*4}")
for art, swc, awc, diff, pct in wc_details:
    marker = " ⚠️" if diff > 200 else ""
    print(f"  {art:<60} {swc:<8} {awc:<12} {diff:<8} {pct}%{marker}")

print(f"\n  ⚠️  ARTIKEL MIT DIFF >200: {len(wc_issues)}")
for art, swc, awc, diff, pct in wc_issues:
    print(f"    🔴 {art}: Schema={swc}, Tatsächlich={awc}, Diff={diff} ({pct}%)")

# ============================================================
# 3. IMAGE AVAILABILITY
# ============================================================
print("\n" + "=" * 80)
print("  🔍 3. BILDVERFÜGBARKEIT (Referenzierte vs Vorhandene Bilder)")
print("=" * 80)

missing_images = []
all_refs = set()
article_refs = {}
for article in articles:
    filepath = os.path.join(ARTICLE_DIR, article)
    refs = extract_image_refs(filepath)
    article_refs[article] = refs
    all_refs.update(refs)

print(f"\n  Einzigartige Bildreferenzen in Artikeln: {len(all_refs)}")
print(f"  Bilder auf Disk (images/): {len(images_on_disk)}")

# Check for referenced images that don't exist on disk
for ref in sorted(all_refs):
    if ref not in images_on_disk:
        # Find which articles reference this
        articles_with_ref = [a for a, refs in article_refs.items() if ref in refs]
        missing_images.append((ref, articles_with_ref))

print(f"\n  🔴 FEHLENDE BILDER (referenziert aber nicht auf Disk): {len(missing_images)}")
for ref, arts in missing_images:
    print(f"    ❌ {ref}")
    for a in arts[:5]:
        print(f"       → {a}")
    if len(arts) > 5:
        print(f"       ... und {len(arts)-5} weitere")

# Check for images on disk that are NOT referenced by any article
orphan_images = images_on_disk - all_refs
# Normalize: some images might have webp extension vs png
print(f"\n  🟡 VERWAISTE BILDER (auf Disk aber nicht referenziert): {len(orphan_images)}")
for img in sorted(list(orphan_images))[:20]:
    print(f"    💤 {img}")
if len(orphan_images) > 20:
    print(f"    ... und {len(orphan_images)-20} weitere")

# Check for articles with NO image references
no_img_articles = [a for a, refs in article_refs.items() if not refs]
print(f"\n  🟡 ARTIKEL OHNE BILDREFERENZEN: {len(no_img_articles)}")
for a in no_img_articles:
    print(f"    ❓ {a}")

# ============================================================
# 4. INTERNAL LINK CONSISTENCY
# ============================================================
print("\n" + "=" * 80)
print("  🔍 4. INTERNE LINK-KONSISTENZ")
print("=" * 80)

all_articles_set = set(articles)
link_issues = []
total_links = 0
for article in articles:
    filepath = os.path.join(ARTICLE_DIR, article)
    links = extract_internal_links(filepath)
    total_links += len(links)
    for link in links:
        # Normalize link
        link_file = os.path.basename(link)
        if link_file not in all_articles_set and link != article:
            link_issues.append((article, link_file))

print(f"  Interne Links insgesamt: {total_links}")
print(f"  🔴 KAPUTTE INTERNE LINKS: {len(link_issues)}")
for src, tgt in link_issues:
    print(f"    ❌ {src} → {tgt}")

# ============================================================
# 5. YEAR CONSISTENCY (2025 vs 2026)
# ============================================================
print("\n" + "=" * 80)
print("  🔍 5. FAKTENAKTUALITÄT / JAHRESZAHLEN (2025 vs 2026)")
print("=" * 80)

year_issues = []
for article in sorted(articles):
    filepath = os.path.join(ARTICLE_DIR, article)
    info = check_article_year_consistency(filepath)
    fy = info['years_in_filename']
    cy = info['years_in_content']
    
    # Check filename has 2025 but content also has 2026 (mixed signals)
    if '2025' in fy and '2026' in cy:
        year_issues.append((article, 'Filename=2025, Content=2026', info))
    elif '2024' in fy:
        year_issues.append((article, 'Filename=2024 (veraltet)', info))
    
    # Check if article mentions both 2025 and 2026 (dating itself)
    if '2025' in cy and '2026' in cy:
        year_issues.append((article, 'Content mentions BOTH 2025 and 2026', info))

print(f"\n  🟡 JAHRESZAHL-INKONSISTENZEN: {len(year_issues)}")
for art, desc, info in year_issues:
    print(f"    ⚠️  {art}")
    print(f"       {desc}")
    print(f"       Dateiname-Jahre: {info['years_in_filename']}")
    print(f"       Content-Jahre: {info['years_in_content']}")

# Summary of year distributions
year_count = defaultdict(int)
for article in articles:
    filepath = os.path.join(ARTICLE_DIR, article)
    info = check_article_year_consistency(filepath)
    for y in info['all_years']:
        year_count[y] += 1
print(f"\n  Jahreszahlen-Verteilung über alle Artikel:")
for y in sorted(year_count.keys()):
    print(f"    {y}: {year_count[y]}x")

# ============================================================
# 6. DUPLICATE CONTENT CHECK
# ============================================================
print("\n" + "=" * 80)
print("  🔍 6. DUPLICATE CONTENT CHECK (Title-Tag & H1-Duplikate)")
print("=" * 80)

titles = {}
h1s = {}
for article in sorted(articles):
    filepath = os.path.join(ARTICLE_DIR, article)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extract <title>
    t_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = t_match.group(1).strip().lower() if t_match else None
    # Extract <h1>
    h1_match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    h1 = h1_match.group(1).strip().lower() if h1_match else None
    
    if title:
        titles.setdefault(title, []).append(article)
    if h1:
        h1s.setdefault(h1, []).append(article)

dup_titles = {t: a for t, a in titles.items() if len(a) > 1}
dup_h1s = {h: a for h, a in h1s.items() if len(a) > 1}

print(f"\n  Title-Duplikate: {len(dup_titles)}")
for t, arts in dup_titles.items():
    print(f"    ⚠️  '{t[:60]}...' → {arts}")

print(f"\n  H1-Duplikate: {len(dup_h1s)}")
for h, arts in dup_h1s.items():
    print(f"    ⚠️  '{h[:60]}...' → {arts}")

# Check for near-duplicate content (same structure/pattern)
print(f"\n  ⚠️  AI-Generierungsmuster: Prüfe Artikel-Strukturen...")
# Count articles that start with similar introduction patterns
intro_patterns = defaultdict(list)
for article in sorted(articles):
    filepath = os.path.join(ARTICLE_DIR, article)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Get first 150 chars of article body (after the H1)
    h1_end = content.find('</h1>')
    if h1_end > 0:
        first_chars = content[h1_end+5:h1_end+200].strip()[:100]
        intro_patterns[first_chars].append(article)

dup_intros = {k: v for k, v in intro_patterns.items() if len(v) > 1}
print(f"  Artikel mit identischen oder ähnlichen Einleitungen: {len(dup_intros)}")
for intro, arts in list(dup_intros.items())[:5]:
    print(f"    ⚠️  '{intro[:80]}...' → {arts}")

# ============================================================
# 7. INHALTLICHE QUALITÄT (Stichprobe)
# ============================================================
print("\n" + "=" * 80)
print("  🔍 7. INHALTLICHE QUALITÄT — STICHPROBE")
print("=" * 80)

sample_articles = [
    'gameserver-mieten-guide.html',  # known 2025 issue
    '7-days-to-die-server-hosten-2026.html',  # future date article
    'gaestebeitrag-finanz-junkie-server-kosten-investor-guide.html',  # guest post
    'vps-anbieter-vergleich-2026.html',  # comparison article
    'docker-compose-vps-guide.html',  # tutorial
    'llm-lokal-hosten-2026.html',  # AI topic with future date
    'webhosting-vserver-vergleich.html',  # old article with 2025 date
]

for sa in sample_articles:
    filepath = os.path.join(ARTICLE_DIR, sa)
    if not os.path.exists(filepath):
        print(f"\n  ❌ {sa} — Datei nicht gefunden!")
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata
    title_m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_m.group(1).strip() if title_m else "N/A"
    h1_m = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    h1 = h1_m.group(1).strip() if h1_m else "N/A"
    date_pub = extract_date_published(filepath)
    schema_wc = extract_word_count_schema(filepath)
    actual_wc = count_words_in_file(filepath)
    
    # Check for tables (comparison)
    has_tables = bool(re.search(r'<table', content))
    # Check for lists
    has_lists = bool(re.search(r'<(ul|ol)>', content))
    # Check for code blocks
    has_code = bool(re.search(r'<pre><code>', content))
    # Check for affiliate links
    has_affiliate = 'nova079-20' in content or 'amzn' in content.lower() or 'amazon' in content.lower()
    # Check for "KI generiert" markers
    has_ai_disclaimer = 'KI-generiert' in content or 'AI-generiert' in content or 'automatisch generiert' in content
    
    # Extract body length
    body_match = re.search(r'<article>(.*?)</article>', content, re.DOTALL)
    body = body_match.group(1) if body_match else content
    
    # Count sections (H2 headings)
    h2_count = len(re.findall(r'<h2[^>]*>', content))
    
    # Check if it has real substance
    word_count_estimate = len(body.split()) if body else 0
    
    print(f"\n  📄 {sa}")
    print(f"  Titel: {title}")
    print(f"  H1:    {h1}")
    print(f"  datePublished: {date_pub}")
    print(f"  wordCount Schema: {schema_wc} | Tatsächlich: {actual_wc}")
    print(f"  H2-Überschriften: {h2_count}")
    print(f"  Tabellen: {'✅' if has_tables else '❌'} | Listen: {'✅' if has_lists else '❌'} | Code: {'✅' if has_code else '❌'} | Affiliate: {'✅' if has_affiliate else '❌'}")
    
    # Quality assessment
    quality_score = 0
    quality_notes = []
    if h2_count >= 5:
        quality_score += 2
    else:
        quality_notes.append(f"Nur {h2_count} H2-Überschriften (wenig Struktur)")
    if has_tables:
        quality_score += 1
    else:
        quality_notes.append("Keine Vergleichstabellen")
    if has_lists:
        quality_score += 1
    if has_code:
        quality_score += 1
    if has_affiliate:
        quality_score += 1
    if actual_wc and actual_wc >= 1500:
        quality_score += 2
    else:
        quality_notes.append(f"Nur ~{actual_wc} Wörter (wenig Substanz)")
    
    print(f"  QualitätsScore: {quality_score}/8")
    if quality_notes:
        for note in quality_notes:
            print(f"    ⚠️  {note}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("  📊 AUDIT-ZUSAMMENFASSUNG")
print("=" * 80)

print(f"""
  KATEGORIE                         FUNDE      SCHWEREGRAD
  ───────────────────────────────────────────────────────────
  1. Datumsgenauigkeit               {len(date_issues):<3} Issues   {'🔴 KRITISCH' if any('FUTURE' in i['issue'] for i in date_issues) else '🟡 WARNUNG'}
  2. WordCount Genauigkeit           {len(wc_issues):<3} Issues   🟡 WARNUNG
  3. Fehlende Bilder                 {len(missing_images):<3} Issues   🔴 KRITISCH
  4. Kaputte interne Links           {len(link_issues):<3} Issues   🔴 KRITISCH
  5. Jahreszahl-Inkonsistenzen       {len(year_issues):<3} Issues   🟡 WARNUNG
  6. Title-Duplikate                 {len(dup_titles):<3} Issues   🟡 WARNUNG
  7. Qualität (Stichprobe)           {len(sample_articles):<3} geprüft  ℹ️  SIEHE OBEN
""")

print("  Generiert: hostazar.com Audit — " + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("=" * 80)
