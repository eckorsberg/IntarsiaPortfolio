import os

pages_dir = "pages"  # Update this if the directory is elsewhere

for filename in os.listdir(pages_dir):
    if filename.endswith(".html"):
        path = os.path.join(pages_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace "Artist" with "Pattern Designer"
        updated = content.replace("Artist", "Pattern Designer")

        if updated != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated)
            print(f"Updated: {filename}")
