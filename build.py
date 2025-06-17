import os
import json

BASE_DIR = os.path.dirname(__file__)
GALLERY_JSON = os.path.join(BASE_DIR, "gallery.json")
PAGES_DIR = os.path.join(BASE_DIR, "pages")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
FULL_DIR = os.path.join(BASE_DIR, "images_full")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")

# Load artwork metadata
with open(GALLERY_JSON, "r", encoding="utf-8") as f:
    gallery = json.load(f)

# Build maps of real filenames (case-sensitive matching)
thumb_map = {os.path.splitext(f)[0].replace("-thumb", "").lower(): f for f in os.listdir(IMAGES_DIR)}
full_map = {os.path.splitext(f)[0].lower(): f for f in os.listdir(FULL_DIR)}

# Page template using external CSS
PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="back"><a href="../index.html">← Back to Gallery</a></div>
  <a href="../images_full/{full_image}" target="_blank">
    <img src="../images/{thumb_image}" alt="{title}">
  </a>
  <h1>{title}</h1>
  <p><strong>Artist:</strong> Ed Korsberg</p>
  <p><strong>Craftsman:</strong> Ed Korsberg</p>
  <p><strong>Primary Wood Types Used:</strong> {woods}</p>
  <p><strong>Number of Pieces:</strong> {pieces}</p>
  <p><strong>Description:</strong> {description}</p>
</body>
</html>
'''

# Generate detail pages
for item in gallery:
    page_path = os.path.join(BASE_DIR, item["file"])
    base_key = os.path.splitext(os.path.basename(page_path))[0].lower()
    title = item["title"]
    thumb = thumb_map.get(base_key, base_key + "-thumb.jpg")
    full = full_map.get(base_key, base_key + ".jpg")

    content = PAGE_TEMPLATE.format(
        title=title,
        full_image=full,
        thumb_image=thumb,
        woods=item.get("woods", "{{WOODS}}"),
        pieces=item.get("pieces", "{{PIECES}}"),
        description=item.get("description", "{{DESCRIPTION}}")
    )

    with open(page_path, "w", encoding="utf-8") as f:
        f.write(content)

# Generate index.html using external style.css
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Intarsia Portfolio</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Ed Korsberg's Intarsia Portfolio</h1>
  <div class="intro-text">
    <p>Intarsia is a form of woodworking in which various shapes, sizes and species of wood are fitted together to create a mosaic-like picture with an illusion of depth.</p>
  </div>
  <div class="gallery">
'''

for item in gallery:
    INDEX_TEMPLATE += f'''
    <a href="{item["file"]}">
      <img src="{item["thumbnail"]}" alt="{item["title"]}">
      <div class="gallery-caption">{item["title"]}</div>
    </a>'''

INDEX_TEMPLATE += '''
  </div>
</body>
</html>
'''

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(INDEX_TEMPLATE)

print("✅ Site rebuilt: now using shared style.css for all pages.")
