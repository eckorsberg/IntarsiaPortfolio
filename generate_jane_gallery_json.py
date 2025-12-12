import json
from pathlib import Path

# Where we expect things to be:
# Run this script from INSIDE jane/ directory:
#   cd jane
#   python ../generate_jane_gallery_json.py
#
# This script will scan:
#   images_full/*.jpg
#   pages/*.html
# and build gallery.json entries keyed by filename stem.

def humanize_title(stem: str) -> str:
    cleaned = stem.replace("_", " ").replace("-", " ")
    return cleaned.strip().title() or stem


def main():
    base = Path(".").resolve()           # jane/
    images_full = base / "images_full"
    pages_dir = base / "pages"
    thumbs = base / "images"

    if not images_full.is_dir():
        print(f"[!] images_full not found at {images_full}")
        return
    if not pages_dir.is_dir():
        print(f"[!] pages/ not found at {pages_dir}")
        return
    if not thumbs.is_dir():
        print(f"[!] images/ (thumbnails) not found at {thumbs}")
        return

    images = sorted([p for p in images_full.iterdir()
                     if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])

    gallery = []

    for img in images:
        stem = img.stem                           # "BabyGiraffe"
        page_file = pages_dir / f"{stem}.html"    # pages/BabyGiraffe.html
        thumb_file = thumbs / f"{stem}-thumb{img.suffix}"

        if not page_file.exists():
            print(f"[!] WARNING: Missing page for {stem}, skipping")
            continue
        if not thumb_file.exists():
            print(f"[!] WARNING: Missing thumbnail for {stem}, skipping")
            continue

        entry = {
            "file": f"pages/{page_file.name}",
            "title": humanize_title(stem),
            "thumbnail": f"images/{stem}-thumb{img.suffix}",
            "artist": "Jane Korsberg",
            "theme": "Quilt",          # placeholder category
            "type": "TBD",             # Jane can refine
            "status": "Available"      # or "TBD"
        }

        gallery.append(entry)
        print(f"[✓] Added: {stem}")

    out_path = base / "gallery.json"
    out_path.write_text(json.dumps(gallery, indent=2), encoding="utf-8")

    print(f"\n[✓] gallery.json written with {len(gallery)} entries:")
    print(f"    {out_path}")


if __name__ == "__main__":
    main()
