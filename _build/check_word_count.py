#!/usr/bin/env python3
"""Check that latest posts have 1500+ words"""
import pathlib, yaml, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"
files = sorted(POSTS_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]
ok = True
for f in files:
    if f.name == "README.md":
        continue
    text = f.read_text(encoding="utf-8")
    try:
        fm = yaml.safe_load(text.split("---")[1])
        wc = fm.get("word_count", 0)
        print(f"{f.name}: {wc} words")
        if wc < 1500:
            print(f"  FAIL: {wc} < 1500")
            ok = False
    except Exception as e:
        print(f"{f.name}: error {e}")
        ok = False
if not ok:
    sys.exit(1)
print("All checked posts >=1500 words")
