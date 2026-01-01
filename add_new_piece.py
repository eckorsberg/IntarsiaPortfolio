import sys
import os
import json
from pathlib import Path
from PIL import Image

# Resolve repo root based on this script's location so templates
# are always loaded from the top-level folder, regardless of cwd.
REPO_ROOT = Path(__file__).resolve().parent

# Constants / directories
TEMPLATE_HTML_PATH = REPO_ROOT / "template.html"
TEMPLATE_JSON_PATH = REPO_ROOT / "template.json"  # schema for new entry

# These are *per-artist* paths and are resolved relative to the
# current working directory, so you can:
#   cd ed   && python ../add_new_piece.py foo.jpg gallery
#   cd jane && python ../add_new_piece.py bar.jpg gallery
IMAGES_FULL_DIR = "./images_full/"
IMAGES_THUMB_DIR = "./images/"
PAGES_DIR = "./pages/"

# --- Full-image shrink knobs (match shrink_images_full.py) ---
MAX_SIDE = 2600               # max width or height in pixels
MAX_SIZE_BYTES = 600 * 1024   # skip if already under ~600 KB
JPEG_QUALITY = 85             # reasonable web quality

def shrink_full_image(image_name: str) -> None:
    """
    Shrink/recompress the newly-added file in ./images_full/ in-place.
    - If file is already small, skip.
    - Converts to RGB and saves as JPEG (keeps original extension, but content is JPEG).
      (If you want to preserve PNG truly, we can adjust.)
    """
    source_path = Path(IMAGES_FULL_DIR) / image_name
    if not source_path.exists():
        raise FileNotFoundError(f"Full image not found: {source_path}")

    orig_size = source_path.stat().st_size
    if orig_size <= MAX_SIZE_BYTES:
        print(f"[-] Full image already small; skipping shrink: {image_name} ({orig_size/1024:.1f} KB)")
        return

    try:
        with Image.open(source_path) as img:
            img = img.convert("RGB")

            w, h = img.size
            scale = min(MAX_SIDE / max(w, h), 1.0)
            if scale < 1.0:
                new_w = int(w * scale)
                new_h = int(h * scale)
                print(f"[~] Resizing full image {image_name}: {w}x{h} -> {new_w}x{new_h}")
                img = img.resize((new_w, new_h), Image.LANCZOS)
            else:
                print(f"[~] No resize needed for {image_name}, recompressing")

            temp_path = source_path.with_suffix(source_path.suffix + ".tmp")
            img.save(temp_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)

        new_size = temp_path.stat().st_size
        if new_size < orig_size:
            temp_path.replace(source_path)
            print(f"[✓] Shrunk full image {image_name}: {orig_size/1024:.1f} KB -> {new_size/1024:.1f} KB")
        else:
            temp_path.unlink()
            print(f"[=] Kept original full image {image_name} (shrunken not smaller)")

    except Exception as e:
        print(f"[!] Error shrinking full image {image_name}: {e}")



def create_thumbnail(image_name: str) -> None:
    base, ext = os.path.splitext(image_name)
    source_path = os.path.join(IMAGES_FULL_DIR, image_name)
    dest_path = os.path.join(IMAGES_THUMB_DIR, f"{base}-thumb{ext}")

    with Image.open(source_path) as img:
        # keep aspect ratio; cap the larger side at 300px
        img.thumbnail((300, 300))
        img.save(dest_path)
    print(f"[✓] Thumbnail created: {dest_path}")


def create_html(image_name: str) -> None:
    """
    Builds pages/<base>.html from template.html and replaces:
      - <a href="../images_full/newimage.jpg" ...>  -> uses images_full/<image_name>
      - <img src="../images/newimage-thumb.jpg" ... -> uses images/<base>-thumb<ext>
    Also updates <title>, <h1>, and img alt from 'newimage' to <base>.
    """
    base, ext = os.path.splitext(image_name)
    dest_path = os.path.join(PAGES_DIR, f"{base}.html")

    with open(TEMPLATE_HTML_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    # Exact replacements for the two lines you specified
    template = template.replace(
        '../images_full/newimage.jpg',
        f'../images_full/{image_name}',
    )
    template = template.replace(
        '../images/newimage-thumb.jpg',
        f'../images/{base}-thumb{ext}',
    )

    # Friendly extras so the page isn't stuck with "newimage"
    template = template.replace('<title>newimage</title>', f'<title>{base}</title>')
    template = template.replace('<h1>newimage</h1>', f'<h1>{base}</h1>')
    template = template.replace('alt="newimage"', f'alt="{base}"')

    # (If you ever re-introduce {{NAME}} etc., you can still replace those here.)

    os.makedirs(PAGES_DIR, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"[✓] HTML page created: {dest_path}")


def append_to_gallery_json(image_name: str, which_json: str) -> None:
    """
    Opens <which_json>.json (e.g., gallery.json or laser.json) in the
    *current* artist folder (cwd), creates a new entry from template.json,
    patches file/thumbnail (and artist), and inserts at the top.
    """
    json_file = f"{which_json}.json"
    if which_json.lower() not in {"gallery", "laser"}:
        raise ValueError("2nd parameter must be 'gallery' or 'laser'")

    # Load a fresh entry template from the repo root
    with open(TEMPLATE_JSON_PATH, "r", encoding="utf-8") as tf:
        new_entry = json.load(tf)

    base, ext = os.path.splitext(image_name)
    html_file = f"pages/{base}.html"
    thumb_file = f"images/{base}-thumb{ext}"

    new_entry["file"] = html_file
    new_entry["thumbnail"] = thumb_file

    # Optionally adjust artist based on which folder we're in.
    cwd_name = Path.cwd().name.lower()
    artist_by_folder = {
        "ed": "Ed Korsberg",
        "jane": "Jane Korsberg",
    }
    artist = artist_by_folder.get(cwd_name)
    if artist:
        new_entry["artist"] = artist

    # Read, modify, write back in the current folder
    with open(json_file, "r", encoding="utf-8") as jf:
        data = json.load(jf)

    data.insert(0, new_entry)

    with open(json_file, "w", encoding="utf-8") as jf:
        json.dump(data, jf, indent=2)

    print(f"[✓] Appended entry to {json_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python add_new_piece.py <filename.jpg|png> [gallery|laser]")
        print("       (run from within 'ed' or 'jane' for per-artist paths)")
        sys.exit(1)

    image_name = sys.argv[1]
    which_json = sys.argv[2] if len(sys.argv) >= 3 else "gallery"  # default friendly fallback

    shrink_full_image(image_name)
    create_thumbnail(image_name)
    create_html(image_name)
    append_to_gallery_json(image_name, which_json)


if __name__ == "__main__":
    main()
