
from PIL import Image
import os

# Adjust these paths if needed
#usage
#python generate_thumbnails.py

SOURCE_DIR = "images_full"
DEST_DIR = "images"
THUMBNAIL_HEIGHT = 200  # Adjust height as desired

# Create output directory if it doesn't exist
os.makedirs(DEST_DIR, exist_ok=True)

for filename in os.listdir(SOURCE_DIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        full_path = os.path.join(SOURCE_DIR, filename)
        img = Image.open(full_path)

        # Maintain aspect ratio while resizing
        aspect_ratio = img.width / img.height
        new_height = THUMBNAIL_HEIGHT
        new_width = int(aspect_ratio * new_height)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Save thumbnail with "-thumb" suffix
        name, ext = os.path.splitext(filename)
        thumb_name = f"{name}-thumb{ext}"
        thumb_path = os.path.join(DEST_DIR, thumb_name)
        img.save(thumb_path)

        print(f"Created thumbnail: {thumb_name}")
