import csv
from pathlib import Path
import json

# Run from repo root:  python jane_export_metadata.py

REPO_ROOT = Path(__file__).resolve().parent
JANE_DIR = REPO_ROOT / "jane"
GALLERY_JSON = JANE_DIR / "gallery.json"
CSV_PATH = JANE_DIR / "jane_metadata.csv"

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}


def humanize_title(stem: str) -> str:
    cleaned = stem.replace("_", " ").replace("-", " ")
    return cleaned.strip().title() or stem


def main():
    if not JANE_DIR.is_dir():
        print(f"[!] jane/ directory not found at {JANE_DIR}")
        return

    if not GALLERY_JSON.exists():
        print(f"[!] {GALLERY_JSON} not found. Generate gallery.json first.")
        return

    with GALLERY_JSON.open(encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data:
        file_html = item.get("file", "")      # e.g. "pages/EncantoQuilt.html"
        thumb = item.get("thumbnail", "")     # e.g. "images/EncantoQuilt-thumb.jpg"
        title = item.get("title") or ""
        pattern_designer = item.get("pattern_designer") or ""

        # Derive an image filename (EncantoQuilt.jpg) from thumbnail if possible
        image_file = ""
        if thumb:
            # "images/EncantoQuilt-thumb.jpg" -> "EncantoQuilt.jpg"
            parts = thumb.split("/")
            if parts:
                thumb_name = parts[-1]
                if "-thumb" in thumb_name:
                    base, ext = thumb_name.split("-thumb", 1)
                    image_file = base + ext
                else:
                    image_file = thumb_name

        # Fallback from file_html if needed
        if not image_file and file_html:
            parts = file_html.split("/")
            if parts:
                stem_html = parts[-1].rsplit(".", 1)[0]
                image_file = stem_html + ".jpg"

        # Fallback title from stem if empty
        if not title and image_file:
            stem = Path(image_file).stem
            title = humanize_title(stem)

        rows.append({
            "image_file": image_file,
            "title": title,
            # Detail-page fields Jane will fill in:
            "pattern_designer": pattern_designer,
            "fabrics": "",
            "technique": "",
            "number": "",
            "description": "",
        })

    # Write CSV
    fieldnames = [
        "image_file",
        "title",
        "pattern_designer",
        "fabrics",
        "technique",
        "number",
        "description",
    ]


    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"[✓] Wrote {CSV_PATH} with {len(rows)} rows.")
    print("    She can open this in Excel, edit, and save as CSV again.")


if __name__ == "__main__":
    main()
