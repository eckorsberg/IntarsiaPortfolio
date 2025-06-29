import sys
import os
import json
from pathlib import Path
from PIL import Image

# Constants
template_html_path = "./template.html"
template_json_path = "./template.json"
gallery_json_path = './gallery.json'
images_full_dir = './images_full/'
images_thumb_dir = './images/'
pages_dir = './pages/'

def create_thumbnail(image_name):
    base, ext = os.path.splitext(image_name)
    source_path = os.path.join(images_full_dir, image_name)
    dest_path = os.path.join(images_thumb_dir, f"{base}-thumb{ext}")
    
    with Image.open(source_path) as img:
        img.thumbnail((300, 300))
        img.save(dest_path)
        print(f"[✓] Thumbnail created: {dest_path}")

def create_html(image_name):
    base, _ = os.path.splitext(image_name)
    dest_path = os.path.join(pages_dir, f"{base}.html")

    with open(template_html_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template.replace("{{NAME}}", base))
    
    print(f"[✓] HTML page created: {dest_path}")

def append_to_gallery_json(image_name):
    json_path = "gallery.json"
    template_json_path = "template.json"
    
    with open(template_json_path, "r", encoding="utf-8") as tf:
        new_entry = json.load(tf)

    # Replace placeholder values in template
    html_file = f"pages/{Path(image_name).stem}.html"
    thumb_file = f"images/{Path(image_name).stem}-thumb.{Path(image_name).suffix[1:]}"
    new_entry["file"] = html_file
    new_entry["thumbnail"] = thumb_file

    # Load and modify JSON list
    with open(json_path, "r", encoding="utf-8") as jf:
        data = json.load(jf)

    # Insert at top
    data.insert(0, new_entry)

    # Save updated JSON
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(data, jf, indent=2)
    
    print(f"✔ Appended entry to {json_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_new_piece.py <filename.jpg/png>")
        sys.exit(1)

    image_name = sys.argv[1]

    create_thumbnail(image_name)
    create_html(image_name)
    append_to_gallery_json(image_name)
