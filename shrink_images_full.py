import os
from pathlib import Path
from PIL import Image

# Run from inside 'ed' or 'jane'
BASE_DIR = Path(".").resolve()
IMAGES_FULL_DIR = BASE_DIR / "images_full"

# Tuning knobs
MAX_SIDE = 2600               # max width or height in pixels
MAX_SIZE_BYTES = 600 * 1024   # skip files already under ~600 KB
JPEG_QUALITY = 85             # reasonable web quality

def shrink_image(path: Path) -> None:
    orig_size = path.stat().st_size
    if orig_size <= MAX_SIZE_BYTES:
        print(f"[-] Skipping (already small): {path.name} ({orig_size/1024:.1f} KB)")
        return

    try:
        with Image.open(path) as img:
            img = img.convert("RGB")  # ensure JPEG-friendly

            # Resize if needed
            w, h = img.size
            scale = min(MAX_SIDE / max(w, h), 1.0)
            if scale < 1.0:
                new_w = int(w * scale)
                new_h = int(h * scale)
                print(f"[~] Resizing {path.name}: {w}x{h} -> {new_w}x{new_h}")
                img = img.resize((new_w, new_h), Image.LANCZOS)
            else:
                print(f"[~] No resize needed for {path.name}, just recompressing")

            # Save to a temporary file first to be safe
            temp_path = path.with_suffix(path.suffix + ".tmp")
            img.save(temp_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)

        new_size = temp_path.stat().st_size

        if new_size < orig_size:
            temp_path.replace(path)
            print(f"[✓] Shrunk {path.name}: {orig_size/1024:.1f} KB -> {new_size/1024:.1f} KB")
        else:
            # If recompressed version isn't smaller, keep the original
            temp_path.unlink()
            print(f"[=] Kept original for {path.name} (new file not smaller)")

    except Exception as e:
        print(f"[!] Error processing {path.name}: {e}")

def main():
    if not IMAGES_FULL_DIR.is_dir():
        print(f"images_full directory not found at: {IMAGES_FULL_DIR}")
        return

    print(f"Working in: {IMAGES_FULL_DIR}")
    for entry in sorted(IMAGES_FULL_DIR.iterdir()):
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue

        shrink_image(entry)

if __name__ == "__main__":
    main()
