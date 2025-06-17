import os

BASE_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(BASE_DIR, "pages")
THUMB_DIR = os.path.join(BASE_DIR, "images")
FULL_DIR = os.path.join(BASE_DIR, "images_full")

# Case-insensitive maps: base name → real filename
full_map = {os.path.splitext(f)[0].lower(): f for f in os.listdir(FULL_DIR)}
thumb_map = {}
for f in os.listdir(THUMB_DIR):
    base = os.path.splitext(f)[0]
    if base.endswith("-thumb"):
        key = base[:-6].lower()
        thumb_map[key] = f

TEMPLATE = '''<!DOCTYPE html>
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
  <p><strong>Primary Wood Types Used:</strong> {{WOODS}}</p>
  <p><strong>Number of Pieces:</strong> {{PIECES}}</p>
  <p><strong>Description:</strong> {{DESCRIPTION}}</p>
</body>
</html>'''

for filename in os.listdir(PAGES_DIR):
    if filename.endswith(".html"):
        key = os.path.splitext(filename)[0].lower()
        title = key.replace('_', ' ').title()

        full_image = full_map.get(key, key + ".jpg")
        thumb_image = thumb_map.get(key, key + "-thumb.jpg")

        html = TEMPLATE.format(
            title=title,
            full_image=full_image,
            thumb_image=thumb_image
        )

        with open(os.path.join(PAGES_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)

print("✅ Pages updated using responsive layout template.")
