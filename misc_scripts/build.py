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

# Build maps of real filenames to preserve casing
thumb_map = {os.path.splitext(f)[0].replace("-thumb", "").lower(): f for f in os.listdir(IMAGES_DIR)}
full_map = {os.path.splitext(f)[0].lower(): f for f in os.listdir(FULL_DIR)}

# Page template
PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    body {{
      font-family: sans-serif;
      font-size: clamp(1rem, 2.5vw, 1.2rem);
      padding: 1em;
      line-height: 1.6;
      max-width: 800px;
      margin: auto;
    }}
    h1 {{
      font-size: 1.8em;
      color: #2c3e50;
    }}
    .back {{
      margin-bottom: 1em;
    }}
    .back a {{
      text-decoration: none;
      color: #3498db;
    }}
    img {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 1em auto;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    p {{
      margin: 0.5em 0;
    }}
  </style>
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

# Generate index.html
INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Intarsia Portfolio</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    body {{
      font-family: system-ui, sans-serif;
      background-color: #f8f9fa;
      margin: 0;
      padding: 2rem;
    }}
    h1 {{
      text-align: center;
      margin-bottom: 2rem;
    }}
    .gallery {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
    }}
    .gallery a {{
      text-decoration: none;
      color: inherit;
    }}
    .gallery img {{
      width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      transition: transform 0.2s ease;
      display: block;
    }}
    .gallery img:hover {{
      transform: scale(1.03);
    }}
    .gallery-caption {{
      margin-top: 0.5rem;
      text-align: center;
      font-weight: bold;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      padding: 0 0.5rem;
      max-width: 100%;
    }}
  </style>
</head>
<body>
  <h1>Ed Korsberg's Intarsia Portfolio</h1>
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

print("✅ Site rebuilt: index and detail pages updated.")
