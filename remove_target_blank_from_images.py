"""
remove_target_blank_from_images.py

Removes target="_blank" from links that point to images_full,
so mobile users get native image viewing + pinch zoom.

Safe to run multiple times.
"""

from pathlib import Path
import re

ROOT = Path(".")
PAGE_DIRS = [ROOT / "ed" / "pages", ROOT / "jane" / "pages"]

pattern = re.compile(
    r'(<a\s+[^>]*href="[^"]*/images_full/[^"]+")\s+target="_blank"',
    re.IGNORECASE
)

for pages_dir in PAGE_DIRS:
    if not pages_dir.exists():
        continue

    for html_file in pages_dir.glob("*.html"):
        text = html_file.read_text(encoding="utf-8")

        new_text, count = pattern.subn(r"\1", text)

        if count > 0:
            html_file.write_text(new_text, encoding="utf-8")
            print(f"Updated: {html_file} ({count} change)")
