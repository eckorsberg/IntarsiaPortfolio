from pathlib import Path

# Adjust this if you name the template file differently
REPO_ROOT = Path(__file__).resolve().parent
TEMPLATE_PATH = REPO_ROOT / "jane_page_template.html"

# Safety: don't overwrite existing pages unless you flip this
OVERWRITE_EXISTING = False

# Which extensions to treat as images
IMAGE_EXTS = {".jpg", ".jpeg", ".png"}


def humanize_title(stem: str) -> str:
    """
    Turn 'baby-giraffe_01' into 'Baby Giraffe 01'
    """
    cleaned = stem.replace("_", " ").replace("-", " ")
    return cleaned.strip().title() or stem


def make_page_for_image(base_dir: Path, image_path: Path, template: str) -> None:
    """
    Create pages/<stem>.html for the given image.
    base_dir is the 'jane' folder.
    """
    stem = image_path.stem  # e.g. 'Beagle'
    pages_dir = base_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    out_path = pages_dir / f"{stem}.html"

    if out_path.exists() and not OVERWRITE_EXISTING:
        print(f"[-] Skipping existing page: {out_path.relative_to(base_dir)}")
        return

    title = humanize_title(stem)

    # Fill in placeholders
    html = template
    html = html.replace("{{NAME}}", stem)
    html = html.replace("{{ALT}}", title)
    html = html.replace("{{TITLE}}", title)

    # Basic placeholders Jane can edit later
    html = html.replace("{{FABRICS}}", "TBD")
    html = html.replace("{{TECHNIQUE}}", "TBD")
    html = html.replace("{{NUMBER}}", "TBD")
    html = html.replace("{{DESCRIPTION}}", "TBD")

    out_path.write_text(html, encoding="utf-8")
    print(f"[✓] Created page: {out_path.relative_to(base_dir)}")


def main() -> None:
    base_dir = Path(".").resolve()  # Expect to be run from inside 'jane'
    images_full_dir = base_dir / "images_full"

    if not TEMPLATE_PATH.exists():
        print(f"[!] Template not found: {TEMPLATE_PATH}")
        return

    if not images_full_dir.is_dir():
        print(f"[!] images_full directory not found at: {images_full_dir}")
        return

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    print(f"Using template: {TEMPLATE_PATH}")
    print(f"Scanning images in: {images_full_dir}")

    count = 0
    for entry in sorted(images_full_dir.iterdir()):
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in IMAGE_EXTS:
            continue
        make_page_for_image(base_dir, entry, template)
        count += 1

    print(f"\nDone. Processed {count} image(s).")


if __name__ == "__main__":
    main()
