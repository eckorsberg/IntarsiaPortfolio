import os, re

PAGES_DIR = "pages"
MISSING = []

for fname in os.listdir(PAGES_DIR):
    if not fname.endswith(".html"):
        continue
    path = os.path.join(PAGES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "Tap image to view full size" not in content:
        MISSING.append(fname)

if MISSING:
    print("⚠️ Missing line in:", *MISSING, sep="\n - ")
else:
    print("✅ All pages include the 'Tap image...' line!")
