#!/usr/bin/env bash
# Full build: images → HTML (with schema integrity check) → static Tailwind CSS
set -e
cd "$(dirname "$0")"
python3 build.py
npx tailwindcss -i input.css -o css/app.css --minify
echo "build complete"
