#!/bin/sh
# Validate only. Publication is handled by CI after an approved merge to main.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$ROOT"
sh scripts/analyze_articles.sh
python3 scripts/generate_discovery.py --check
echo "All quality gates passed; exitcode: 0"
