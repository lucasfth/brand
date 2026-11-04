#!/usr/bin/env python3
"""Verify website font assets and notices without rebuilding logo artwork."""

from pathlib import Path
import hashlib
import re

root = Path(__file__).resolve().parents[1] / "typography"
sources = sorted((root / "fonts").glob("*/SOURCE.txt"))
assert len(sources) == 3
for source in sources:
    digests = [re.fullmatch(r"([a-f0-9]{64})  (.+)", line)
               for line in source.read_text().splitlines()]
    digests = [match for match in digests if match]
    assert len(digests) >= 3, source
    for match in digests:
        digest, name = match.groups()
        assert hashlib.sha256((source.parent / name).read_bytes()).hexdigest() == digest, name
    assert "SIL OPEN FONT LICENSE" in (source.parent / "OFL.txt").read_text()
css = (root / "tokens.css").read_text()
urls = re.findall(r'url\("([^\"]+)"\)', css)
assert len(urls) == 6
for url in urls:
    assert (root / url).read_bytes()[:4] == b"wOF2", url
assert "ss01" not in css and "Masked" not in css
print("PASS: six fonts, pinned checksums, OFL notices and CSS URLs; no masking.")
