import os

BASE_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(BASE_DIR, "pages")
THUMB_DIR = os.path.join(BASE_DIR, "images")
FULL_DIR = os.path.join(BASE_DIR, "images_full")

# Build case-insensitive maps of actual filenames
thumb_map = {os.path.splitext(f)[0].lower(): f for f in os.listdir(THUMB_DIR)}
full_map = {os.path.splitext(f)[0].lower(): f for f in os.listdir(FULL_DIR)}

# Template using correct ../ paths and dynamic filename casing
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <style>
    body {{
      font-family: sans-serif;
      margin: 1.5em;
      background-color: #fcfcfc;
      line-height: 1.6;
      padding: 1em;
    }}
    h1 {{
      color: #2c3e50;
      font-size: 1.8em;
    }}
    .back {{
      margin-bottom: 1em;
    }}
    .back a {{
      text-decoration: none;
      color: #3498db;
    }}
    p {{
      font-size: 1.1em;
      margin: 0.5em 0;
    }}
    @media (max-width: 600px) {{
      body {{
        font-size: 1em;
        margin: 1em;
      }}
    }}
  </style>
</head>
<body>
  <div class="back"><a href="../index.html">← Back to Gallery</a></div>
  <a href="../images_full/{full_image}" target="_blank">
    <img src="../images/{thumb_image}" alt="{title}" height="300" />
  </a>
  <h1>{title}</h1>
  <p><strong>Artist:</strong> Ed Korsberg</p>
  <p><strong>Craftsman:</strong> Ed Korsberg</p>
  <p><strong>Primary Wood Types Used:</strong> {{WOODS}}</p>
  <p><strong>Number of Pieces:</strong> {{PIECES}}</p>
  <p><strong>Description:</strong> {{DESCRIPTION}}</p>
</body>
</html>'''

# Apply the template to each HTML file
for filename in os.listdir(PAGES_DIR):
    if filename.endswith(".html"):
        key = os.path.splitext(filename)[0].lower()
        title = key.replace('_', ' ').title()
        thumb_image = thumb_map.get(key, key + "-thumb.jpg")
        full_image = full_map.get(key, key + ".jpg")

        content = TEMPLATE.format(
            title=title,
            thumb_image=thumb_image,
            full_image=full_image
        )

        with open(os.path.join(PAGES_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content)

print("✅ All pages updated using dynamic filename casing.")
