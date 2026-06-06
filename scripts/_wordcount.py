#!/usr/bin/env python3
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
# Remove HTML tags
text = re.sub(r'<[^>]+>', ' ', text)
# Count words (only words with 2+ chars to filter out single letters/symbols)
words = [w for w in text.split() if len(w) > 1]
print(f'Article word count (approximate): {len(words)}')
