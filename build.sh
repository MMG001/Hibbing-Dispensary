#!/usr/bin/env bash
# Full build: HTML (with schema integrity check) → static Tailwind CSS → inline CSS
set -e
cd "$(dirname "$0")"
python3 build.py
npx tailwindcss -i input.css -o css/app.css --minify
python3 inline_css.py
echo "build complete"
