#!/usr/bin/env python3
"""Inline the compiled Tailwind CSS into every page, replacing the stylesheet link.
Removes the last render-blocking request (6 KiB gzipped inline instead)."""
import glob, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
css = open("css/app.css").read().strip()
pat = re.compile(r'<link href="/css/app\.css\?v=\d+" rel="stylesheet"/>')
n = 0
for f in glob.glob("*.html"):
    html = open(f).read()
    html, c = pat.subn("<style>" + css.replace("\\", "\\\\") + "</style>", html, count=1)
    if c:
        open(f, "w").write(html); n += 1
print(f"inlined app.css into {n} pages ({len(css)/1024:.1f} KiB raw)")
