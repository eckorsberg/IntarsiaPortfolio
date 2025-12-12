import csv
import json
import html
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent
JANE_DIR = REPO_ROOT / "jane"
GALLERY_JSON = JANE_DIR / "gallery.json"
CSV_PATH = JANE_DIR / "jane_metadata.csv"
PAGES_DIR = JANE_DIR / "pages"


def html_escape(text: str) -> str:
    return html.escape(text or "", quote=True)


def load_csv_metadata():
    if not CSV_PATH.exists():
        print(f"[!] {CSV_PATH} not found. Run jane_export_metadata.py first.")
        return {}

    meta = {}
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            image_file = (row.get("image_file") or "").strip()
            if not image_file:
                continue
            meta[image_file] = {
                "title": row.get("title", "").strip(),
                "pattern_designer": row.get("pattern_designer", "").strip(),
                "fabrics": row.get("fabrics", "").strip(),
                "technique": row.get("technique", "").strip(),
                "number": row.get("number", "").strip(),
                "description": row.get("description", "").strip(),
            }

    return meta


def update_gallery_json(meta_by_image):
    if not GALLERY_JSON.exists():
        print(f"[!] {GALLERY_JSON} not found.")
        return

    with GALLERY_JSON.open(encoding="utf-8") as f:
        data = json.load(f)

    updated = 0

    for item in data:
        thumb = item.get("thumbnail", "")
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

        if not image_file or image_file not in meta_by_image:
            continue

        m = meta_by_image[image_file]

        if m["title"]:
            item["title"] = m["title"]

        updated += 1

    with GALLERY_JSON.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[✓] Updated {updated} entries in {GALLERY_JSON}")


def update_detail_pages(meta_by_image):
    if not PAGES_DIR.is_dir():
        print(f"[!] {PAGES_DIR} not found.")
        return

    updated_pages = 0

    for image_file, m in meta_by_image.items():
        stem = Path(image_file).stem
        page_path = PAGES_DIR / f"{stem}.html"
        if not page_path.exists():
            print(f"[!] Page not found for {image_file}: {page_path.name}")
            continue

        text = page_path.read_text(encoding="utf-8")

        # Title <h1>...</h1>
        if m["title"]:
            text = re.sub(
                r"<h1>.*?</h1>",
                f"<h1>{html_escape(m['title'])}</h1>",
                text,
                count=1,
                flags=re.DOTALL,
            )

        # Pattern Designer
        if m.get("pattern_designer"):
            text = re.sub(
                r'(<p><strong>Pattern Designer:</strong>\s*)(.*?)(</p>)',
                r"\1" + html_escape(m["pattern_designer"]) + r"\3",
                text,
                count=1,
                flags=re.DOTALL,
            )
        
        # Fabrics
        if m["fabrics"]:
            text = re.sub(
                r'(<p><strong>Primary Fabrics Used:</strong>\s*)(.*?)(</p>)',
                r"\1" + html_escape(m["fabrics"]) + r"\3",
                text,
                count=1,
                flags=re.DOTALL,
            )

        # Technique
        if m["technique"]:
            text = re.sub(
                r'(<p><strong>Technique:</strong>\s*)(.*?)(</p>)',
                r"\1" + html_escape(m["technique"]) + r"\3",
                text,
                count=1,
                flags=re.DOTALL,
            )

        # Number of Pieces
        if m["number"]:
            text = re.sub(
                r'(<p><strong>Number of Pieces:</strong>\s*)(.*?)(</p>)',
                r"\1" + html_escape(m["number"]) + r"\3",
                text,
                count=1,
                flags=re.DOTALL,
            )

        # Description
        if m["description"]:
            text = re.sub(
                r'(<p><strong>Description:</strong>\s*)(.*?)(</p>)',
                r"\1" + html_escape(m["description"]) + r"\3",
                text,
                count=1,
                flags=re.DOTALL,
            )

        page_path.write_text(text, encoding="utf-8")
        updated_pages += 1

    print(f"[✓] Updated {updated_pages} detail page(s) in {PAGES_DIR}")


def main():
    meta_by_image = load_csv_metadata()
    if not meta_by_image:
        print("[!] No metadata loaded from CSV; nothing to do.")
        return

    update_gallery_json(meta_by_image)
    update_detail_pages(meta_by_image)


if __name__ == "__main__":
    main()
