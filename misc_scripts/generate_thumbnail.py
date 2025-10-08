from PIL import Image
import os
import sys

# Usage: python generate_thumbnail.py XYZ.jpg
THUMBNAIL_HEIGHT = 200  # adjust as desired

def create_thumbnail(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    with Image.open(filename) as img:
        aspect_ratio = img.width / img.height
        new_height = THUMBNAIL_HEIGHT
        new_width = int(aspect_ratio * new_height)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        name, ext = os.path.splitext(filename)
        thumb_name = f"{name}-thumb{ext}"
        img.save(thumb_name)
        print(f"Created thumbnail: {thumb_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_thumbnail.py <filename>")
    else:
        create_thumbnail(sys.argv[1])
