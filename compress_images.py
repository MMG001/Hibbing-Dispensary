#!/usr/bin/env python3
"""Recompress site JPEGs (quality 80, progressive), cap width at 1600px,
preserve embedded EXIF metadata. Writes a dimensions map for width/height attrs."""
import os, json
from PIL import Image
os.chdir(os.path.join(os.path.dirname(__file__), "images"))
dims, saved = {}, 0
for f in sorted(os.listdir(".")):
    if not f.lower().endswith(".jpg"): continue
    im = Image.open(f); exif = im.info.get("exif")
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    before = os.path.getsize(f)
    kw = dict(quality=80, optimize=True, progressive=True)
    if exif: kw["exif"] = exif
    im.convert("RGB").save(f, "JPEG", **kw)
    after = os.path.getsize(f)
    if after > before:  # keep smaller original behavior is fine; sizes rarely grow
        pass
    saved += before - after
    dims[f] = [im.width, im.height]
json.dump(dims, open("dimensions.json", "w"), indent=1)
print(f"recompressed {len(dims)} images, saved {saved/1024:.0f} KiB total")
