
import os
import json
from PIL import Image

# Directories
BASE_DIR = os.path.dirname(__file__)
FULL_DIR = os.path.join(BASE_DIR, 'images_full')
THUMB_DIR = os.path.join(BASE_DIR, 'images')
PAGES_DIR = os.path.join(BASE_DIR, 'pages')
GALLERY_JSON = os.path.join(BASE_DIR, 'gallery.json')

# Ensure thumbnail directory exists
os.makedirs(THUMB_DIR, exist_ok=True)

entries = []

for filename in os.listdir(FULL_DIR):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        name_no_ext = os.path.splitext(filename)[0]
        thumb_filename = name_no_ext + '-thumb.jpg'
        thumb_path = os.path.join(THUMB_DIR, thumb_filename)

        # Generate thumbnail
        try:
            with Image.open(os.path.join(FULL_DIR, filename)) as img:
                img.thumbnail((200, 150))
                img.save(thumb_path, "JPEG")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

        # Find matching detail page
        detail_file = f"{name_no_ext.lower()}.html"
        detail_path = os.path.join(PAGES_DIR, detail_file)
        if not os.path.exists(detail_path):
            print(f"Warning: No detail page found for {filename}, skipping...")
            continue

        # Create JSON entry
        entries.append({
            "file": f"pages/{detail_file}",
            "title": name_no_ext.replace('_', ' '),
            "thumbnail": f"images/{thumb_filename}"
        })

# Save updated gallery.json
with open(GALLERY_JSON, 'w', encoding='utf-8') as f:
    json.dump(entries, f, indent=2)

print(f"✅ gallery.json updated with {len(entries)} entries.")
