import os
import re

# Configuration: path to the folder containing your HTML files
HTML_DIR = "./pages"  # <-- Change this to your actual folder path

# HTML snippet for the pattern designer replacement
PATTERN_DESIGNER_SNIPPET = '<p><strong>Pattern Designer:</strong> <span id="patternDesigner">Loading...</span></p>'

# Script block to be inserted after Description
SCRIPT_SNIPPET = '  <script src="/js/pattern-designer-loader.js"></script>'

# Regex patterns
pattern_designer_regex = re.compile(
    r'^(\s*)<p><strong>Pattern Designer:</strong>.*?</p>\s*$', re.IGNORECASE | re.MULTILINE
)

description_regex = re.compile(
    r'(<p><strong>Description:</strong>.*?</p>)', re.IGNORECASE | re.DOTALL
)

def process_html_files(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".html"):
            file_path = os.path.join(folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            if 'id="patternDesigner"' in content:
                print(f"Already dynamic: {filename}")
                continue

            original_content = content

            # Replace Pattern Designer line, preserving indent
            match = pattern_designer_regex.search(content)
            if match:
                indent = match.group(1)
                content = pattern_designer_regex.sub(
                    f"{indent}{PATTERN_DESIGNER_SNIPPET}", content
                )
            else:
                print(f"Warning: no Pattern Designer line found in {filename}")

            # Insert script block after Description line
            content, count = description_regex.subn(
                r"\1\n\n" + SCRIPT_SNIPPET, content
            )

            if count > 0:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                print(f"Updated: {filename}")
            else:
                print(f"Skipped (no Description found): {filename}")

if __name__ == "__main__":
    process_html_files(HTML_DIR)
