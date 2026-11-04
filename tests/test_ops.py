import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit', ROOT / 'scripts/analyze_articles.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class Gates(unittest.TestCase):
    def test_valid_and_reject_each_violation(self):
        with tempfile.TemporaryDirectory(prefix='hostazar space ') as folder:
            root = Path(folder)
            (root / 'artikel').mkdir()
            good = ('<title>' + 'T' * 50 + '</title><meta name="description" content="' + 'D' * 120 +
                    '"><main><h1 class="heading">Test</h1><a href="https://amazon.de/item" rel="nofollow sponsored">Amazon</a>')
            for slug in ('a', 'b', 'c'):
                links = ''.join(f'<a href="{other}.html">Link</a>' for other in ('a', 'b', 'c') if other != slug)
                (root / 'artikel' / (slug + '.html')).write_text(good + links + '</main>')
            self.assertEqual(audit.audit(root), 0)
            path = root / 'artikel/a.html'
            original = path.read_text()
            for old, new in [('<h1 class="heading">Test</h1>', ''), ('T' * 50, 'short'),
                             ('D' * 120, 'short'), ('nofollow sponsored', 'sponsored'),
                             ('href="b.html"', 'href="missing.html"'), ('</main>', '')]:
                path.write_text(original.replace(old, new))
                self.assertEqual(audit.audit(root), 1)
            path.write_text(original)
            self.assertEqual(audit.audit(root), 0)
    def test_empty_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(audit.audit(Path(folder)), 1)
