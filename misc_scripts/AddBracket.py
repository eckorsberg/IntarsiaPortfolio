import os
import re

PAGES_DIR = "pages"

# Match an <a> wrapping an <img>, with flexible spacing and indentation
IMG_BLOCK_PATTERN = re.compile(
    r'''(?P<indent>[ \t]*)<a\s+href="(?P<full>[^"]+)"\s+target="_blank">\s*
(?P=indent)<img\s+src="(?P<thumb>[^"]+)"\s+alt="(?P<alt>[^"]+)"\s*/?>\s*
(?P=indent)</a>''',
    re.VERBOSE
)

WRAPPER_TEMPLATE = '''{indent}<div class="image-container">
{indent}  <a href="{full}" target="_blank">
{indent}    <img src="{thumb}" alt="{alt}">
{indent}  </a>
{indent}  <p class="tap-note">Tap image to view full size</p>
{indent}</div>'''


def wrap_image_blocks_in_html():
    for filename in os.listdir(PAGES_DIR):
        if not filename.endswith(".html"):
            continue

        filepath = os.path.join(PAGES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        new_content, count = IMG_BLOCK_PATTERN.subn(lambda m: WRAPPER_TEMPLATE.format(
            indent=m.group("indent"),
            full=m.group("full"),
            thumb=m.group("thumb"),
            alt=m.group("alt")
        ), content)

        if count > 0:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_content)
            print(f"✅ Updated {filename} (wrapped {count} image block{'s' if count > 1 else ''})")
        else:
            print(f"— Skipped {filename} (no matches found)")


if __name__ == "__main__":
    wrap_image_blocks_in_html()
