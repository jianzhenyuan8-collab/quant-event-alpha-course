"""确保所有本地 Markdown 链接都能在仓库内打开。"""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]

class MarkdownLinkTests(unittest.TestCase):
    def test_local_links(self):
        broken=[]
        for file in ROOT.rglob('*.md'):
            for m in re.findall(r'(?<!!)(?<!\\)\[[^\]]+\]\(([^)]+)\)', file.read_text(encoding='utf8')):
                raw=m.split('#')[0]
                if not raw or raw.startswith(('http:','https:','mailto:','sandbox:')): continue
                target=(file.parent/unquote(raw)).resolve()
                if not target.exists(): broken.append((str(file.relative_to(ROOT)), raw))
        self.assertEqual(broken,[])
