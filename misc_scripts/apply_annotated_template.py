import os

# Define base path
BASE_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(BASE_DIR, "pages")
THUMB_DIR = "images"
FULL_DIR = "images_full"

# HTML template with CSS comments and structure from goldenEagle.html
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <style>
    body {{
      font-family: sans-serif;		/* Clean, modern text */
      margin: 1.5em;				/* Space around page edges */
      background-color: #fcfcfc;	/* Light background */
      line-height: 1.6;				/* Line spacing for readability */
      padding: 1em;					/* Space inside page */
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
      color: #3498db;			/* Blue text */
    }}
    p {{
      font-size: 1.1em;			/* Slightly larger paragraph text */
      margin: 0.5em 0;			/* Space above/below each paragraph */
    }}
    @media (max-width: 600px) {{
      body {{
        font-size: 1em;			/* Slightly smaller font on narrow screens */
        margin: 1em;			/* Less margin on phones */
      }}
    }}
  </style>
</head>
<body>
  <div class="back"><a href="../index.html">← Back to Gallery</a></div>
  <a href="../{full_dir}/{image_name}.jpg" target="_blank">
    <img src="../{thumb_dir}/{image_name}-thumb.jpg" alt="{title}" height="300" />
  </a>
  <h1>{title}</h1>
  <p><strong>Artist:</strong> Ed Korsberg</p>
  <p><strong>Craftsman:</strong> Ed Korsberg</p>
  <p><strong>Primary Wood Types Used:</strong> {{WOODS}}</p>
  <p><strong>Number of Pieces:</strong> {{PIECES}}</p>
  <p><strong>Description:</strong> {{DESCRIPTION}}</p>
</body>
</html>'''

# Apply template to each page
for filename in os.listdir(PAGES_DIR):
    if filename.endswith(".html"):
        image_name = os.path.splitext(filename)[0]
        title = image_name.replace('_', ' ').title()

        filled = TEMPLATE.format(
            title=title,
            image_name=image_name,
            thumb_dir=THUMB_DIR,
            full_dir=FULL_DIR
        )

        file_path = os.path.join(PAGES_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(filled)

print("✅ All pages updated using annotated style template.")
