import os
import json
import re

# Define paths relative to this script
BASE_DIR = os.path.dirname(__file__)
GALLERY_JSON = os.path.join(BASE_DIR, "gallery.json")
PAGES_DIR = os.path.join(BASE_DIR, "pages")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
FULL_DIR = os.path.join(BASE_DIR, "images_full")

# Build maps of actual filenames (lowercase => actual case)
actual_pages = {f.lower(): f for f in os.listdir(PAGES_DIR)}
actual_thumbs = {f.lower(): f for f in os.listdir(IMAGES_DIR)}
actual_full = {f.lower(): f for f in os.listdir(FULL_DIR)}

# Fix gallery.json
with open(GALLERY_JSON, "r", encoding="utf-8") as f:
    gallery = json.load(f)

fixed_gallery = []
for entry in gallery:
    fixed = entry.copy()
    file_name = os.path.basename(entry["file"]).lower()
    thumb_name = os.path.basename(entry["thumbnail"]).lower()

    if file_name in actual_pages:
        fixed["file"] = f"pages/{actual_pages[file_name]}"
    else:
        print(f"[!] Missing HTML file: {entry['file']}")

    if thumb_name in actual_thumbs:
        fixed["thumbnail"] = f"images/{actual_thumbs[thumb_name]}"
    else:
        print(f"[!] Missing thumbnail: {entry['thumbnail']}")

    fixed_gallery.append(fixed)

with open(GALLERY_JSON, "w", encoding="utf-8") as f:
    json.dump(fixed_gallery, f, indent=2)
print("✅ gallery.json updated.")

# Fix image references inside HTML files
def fix_refs(text, directory, actual_map):
    def replacer(match):
        src = match.group(1)
        base = os.path.basename(src).lower()
        if base in actual_map:
            fixed = f"{directory}/{actual_map[base]}"
            return f'src="{fixed}"' if 'src=' in match.group(0) else f'href="{fixed}"'
        return match.group(0)  # Leave unchanged if not found
    text = re.sub(r'src=["\'](.*?)["\']', replacer, text)
    text = re.sub(r'href=["\'](.*?)["\']', replacer, text)
    
    return text

for fname in os.listdir(PAGES_DIR):
    path = os.path.join(PAGES_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = fix_refs(content, "images", actual_thumbs)
    content = fix_refs(content, "images_full", actual_full)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ HTML files updated with corrected image paths.")
