import sys
import os
from rembg import remove
from PIL import Image

def process_image(filename):
    name, _ = os.path.splitext(filename)
    transparent_path = f"{name}-transparent.png"
    white_path = f"{name}-white.jpg"

    # Step 1: Remove background
    with Image.open(filename) as img:
        img = img.convert("RGBA")
        transparent = remove(img)
        transparent.save(transparent_path)

    # Step 2: Paste onto white background
    with Image.open(transparent_path) as img:
        white_bg = Image.new("RGB", img.size, (255, 255, 255))
        white_bg.paste(img, mask=img.split()[3])  # Use alpha channel
        white_bg.save(white_path, quality=95)

    print(f"✅ Saved: {white_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_background_add_white.py input.jpg")
    else:
        process_image(sys.argv[1])
