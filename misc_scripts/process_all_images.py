import os
from rembg import remove
from PIL import Image

# Set your shared folder path
INPUT_DIR = '/media/sf_VboxShare'

def process_image(filepath):
    name, ext = os.path.splitext(filepath)
    if ext.lower() not in ['.jpg', '.jpeg', '.png']:
        return
    if "-white" in name:
        return  # skip already processed

    white_path = name + '-white.jpg'

    try:
        # Remove background
        with Image.open(filepath) as img:
            img = img.convert("RGBA")
            cutout = remove(img)

        # Paste onto white background
        white_bg = Image.new("RGB", cutout.size, (255, 255, 255))
        white_bg.paste(cutout, mask=cutout.split()[3])
        white_bg.save(white_path, quality=95)

        print(f"✅ Processed: {os.path.basename(white_path)}")

    except Exception as e:
        print(f"❌ Failed: {filepath} - {e}")

def process_all_images():
    for filename in os.listdir(INPUT_DIR):
        filepath = os.path.join(INPUT_DIR, filename)
        if os.path.isfile(filepath):
            process_image(filepath)

if __name__ == "__main__":
    process_all_images()
