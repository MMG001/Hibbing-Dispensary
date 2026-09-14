#!/usr/bin/env python3
"""Generate WebP versions of every JPG, plus 828w hero variants for large images.
Updates images/dimensions.json."""
import os, json
from PIL import Image
os.chdir(os.path.join(os.path.dirname(__file__), "images"))
dims = json.load(open("dimensions.json"))
jpgs = [f for f in sorted(os.listdir(".")) if f.endswith(".jpg")]
made_828 = made_webp = 0
# 828w variants for large (hero-capable) images
for f in list(jpgs):
    w, h = dims.get(f, Image.open(f).size)
    if w > 900 and not f.endswith(("-640.jpg", "-828.jpg")):
        name = f[:-4] + "-828.jpg"
        if name not in dims:
            im = Image.open(f); exif = im.info.get("exif")
            v = im.resize((828, round(h * 828 / w)), Image.LANCZOS)
            kw = dict(quality=80, optimize=True, progressive=True)
            if exif: kw["exif"] = exif
            v.convert("RGB").save(name, "JPEG", **kw)
            dims[name] = [828, round(h * 828 / w)]
            made_828 += 1
# webp twins for every jpg
for f in sorted(os.listdir(".")):
    if not f.endswith(".jpg"): continue
    wname = f[:-4] + ".webp"
    im = Image.open(f)
    im.convert("RGB").save(wname, "WEBP", quality=78, method=6)
    made_webp += 1
json.dump(dims, open("dimensions.json", "w"), indent=1)
jpg_kb = sum(os.path.getsize(f) for f in os.listdir(".") if f.endswith(".jpg")) / 1024
webp_kb = sum(os.path.getsize(f) for f in os.listdir(".") if f.endswith(".webp")) / 1024
print(f"made {made_828} 828w variants, {made_webp} webp files | jpg total {jpg_kb:.0f} KiB vs webp total {webp_kb:.0f} KiB")
