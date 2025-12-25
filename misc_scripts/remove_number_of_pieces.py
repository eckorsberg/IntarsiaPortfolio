import re
from pathlib import Path

# CHANGE THIS to the directory containing her HTML files
HTML_DIR = Path(r"C:\Users\eck44\IntarsiaHtml\IntarsiaPortfolio\jane\pages")

pattern = re.compile(
    r'<p>\s*<strong>\s*Number of Pieces:.*?</p>\s*\n?',
    re.IGNORECASE | re.DOTALL
)

for html_file in HTML_DIR.glob("*.html"):
    text = html_file.read_text(encoding="utf-8")

    new_text, count = pattern.subn("", text)

    if count > 0:
        html_file.write_text(new_text, encoding="utf-8")
        print(f"Updated: {html_file.name}")
    else:
        print(f"No change: {html_file.name}")
