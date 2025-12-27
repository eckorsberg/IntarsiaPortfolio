import json
import shutil
from pathlib import Path

INPUT_FILE = Path("gallery.json")
BACKUP_FILE = Path("gallery.json.bak")

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"{INPUT_FILE} not found")

    # Backup original file
    shutil.copy(INPUT_FILE, BACKUP_FILE)
    print(f"Backup created: {BACKUP_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    modified = 0

    for item in data:
        if "featured" not in item:
            item["featured"] = False
            modified += 1

    with INPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Done. Added 'featured': false to {modified} entries.")

if __name__ == "__main__":
    main()
