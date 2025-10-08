from PIL import Image
import sys
import os

def merge_images_horizontally(img1_path, img2_path, output_path):
    # Open both images
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    # Resize to same height (optional but looks cleaner)
    if img1.height != img2.height:
        new_height = min(img1.height, img2.height)
        img1 = img1.resize((int(img1.width * new_height / img1.height), new_height))
        img2 = img2.resize((int(img2.width * new_height / img2.height), new_height))

    # Create blank canvas wide enough for both
    total_width = img1.width + img2.width
    result = Image.new("RGB", (total_width, img1.height), (255, 255, 255))

    # Paste both images
    result.paste(img1, (0, 0))
    result.paste(img2, (img1.width, 0))

    # Save as JPG
    result.save(output_path, "JPEG")
    print(f"Merged image saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_side_by_side.py <image1> <image2> <output.jpg>")
    else:
        _, img1, img2, out = sys.argv
        merge_images_horizontally(img1, img2, out)
