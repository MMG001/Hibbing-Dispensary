#!/usr/bin/env python3
"""Embed EXIF metadata (description, artist, copyright) into site images
and write images/metadata.json used for alt text across the site."""
import json, piexif, os

BRAND = "Hibbing Dispensary"
COPYRIGHT = "© 2026 Hibbing Dispensary, Hibbing, MN. All rights reserved."

META = {
  "Hibbing-Hero.jpg": "Hibbing Dispensary counter displaying craft cannabis flower, fruit gummies, pre-rolls, concentrates, tinctures, and vape products beneath the gold pine-and-leaf logo.",
  "THC-Cannabis-Hero.jpg": "Glass jars of craft cannabis flower with a loose bud on a counter under warm golden light at Hibbing Dispensary.",
  "THC-Cannabis-101-Hero.jpg": "Cannabis education hero image introducing Cannabis 101 basics at Hibbing Dispensary.",
  "THC-Cannabis-For-Beginers-Hero.jpg": "Beginner-friendly cannabis guide hero image for first-time consumers at Hibbing Dispensary.",
  "THC-Cannabis-Strains-Hero.jpg": "A lineup of distinct cannabis strains showing varied colors and structures for strain education.",
  "CBD-vs-THC-Hero.jpg": "Three whole cannabis colas side by side illustrating the differences between CBD and THC dominant plants.",
  "Benefits-of-Cannabis-Hero.jpg": "Hero image for the benefits of cannabis education article at Hibbing Dispensary.",
  "THC-Concentrates-Hero.jpg": "Golden cannabis concentrates hero image for the concentrates category at Hibbing Dispensary.",
  "Pre-rolls-Hero.jpg": "Hand-crafted cannabis pre-rolls hero image at Hibbing Dispensary.",
  "THC-Vaporizers-Hero.jpg": "Cannabis vaporizer hardware and cartridges hero image at Hibbing Dispensary.",
  "About-Us-page.jpg": "A curated spread of cannabis products - tinctures, flower, edibles, and topicals - representing the Hibbing Dispensary collection.",
  "THC-Cannabis-01.jpg": "Three trimmed cannabis flower buds of increasing size on a soft blue studio background.",
  "THC-Cannabis-02.jpg": "Close-up of fresh trichome-rich cannabis flower buds on a white background.",
  "THC-Cannabis-Store.jpg": "Dispensary shelves stocked with sealed bags of cannabis flower under warm retail lighting.",
  "THC-Cannabis-Store-02.jpg": "A budtender assists customers behind a counter lined with labeled jars of cannabis flower.",
  "THC-Cannabis-Store-03.jpg": "A cork-topped apothecary jar of cannabis flower on a dispensary counter with warm pendant lighting.",
  "THC-Concentrates-01.jpg": "Rows of amber cannabis oil vials backlit in a production facility.",
  "THC-Concentrates-02.jpg": "Twelve labeled jars of strain-specific live rosin concentrates arranged in two rows.",
  "THC-Concentrates-03.jpg": "A dab tool lifting golden crumble concentrate from a glass jar.",
  "THC-Concentrates-04.jpg": "Assorted jars of golden cannabis extracts and concentrates on a reflective counter.",
  "THC-Edible-Gummies-01.jpg": "Sugar-dusted THC gummies in assorted fruit flavors resting on cannabis leaves.",
  "THC-Edible-Gummies-02.jpg": "Colorful sugared cannabis gummies in green, yellow, and red on a wood table.",
  "THC-Prerolls-01.jpg": "A single cannabis pre-roll beside three fresh flower buds on a white surface.",
  "THC-Vaporizer-01.jpg": "A black cannabis vaporizer with amber oil cartridge and two tincture bottles.",
  "THC-Vaporizer-02.jpg": "Colorful vaporizer devices and cannabis oil bottles on a white background.",
}

os.chdir(os.path.join(os.path.dirname(__file__), "images"))
for fname, desc in META.items():
    try:
        exif = piexif.load(fname)
    except Exception:
        exif = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    exif["0th"][piexif.ImageIFD.ImageDescription] = desc.encode()
    exif["0th"][piexif.ImageIFD.Artist] = BRAND.encode()
    exif["0th"][piexif.ImageIFD.Copyright] = COPYRIGHT.encode()
    exif["0th"][piexif.ImageIFD.XPTitle] = fname.replace("-", " ").rsplit(".", 1)[0].encode("utf-16le")
    exif["0th"][piexif.ImageIFD.XPComment] = desc.encode("utf-16le")
    exif["0th"][piexif.ImageIFD.XPKeywords] = "cannabis, dispensary, Hibbing MN, THC, CBD".encode("utf-16le")
    piexif.insert(piexif.dump(exif), fname)
    print("embedded:", fname)

with open("metadata.json", "w") as f:
    json.dump(META, f, indent=2)
print("wrote metadata.json")
