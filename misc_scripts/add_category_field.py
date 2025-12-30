import json
import shutil
from pathlib import Path

FILE = Path("jane/gallery.json")
BACKUP = FILE.with_suffix(".json.bak")

def main():
    if not FILE.exists():
        raise SystemExit(f"File not found: {FILE}")

    shutil.copy(FILE, BACKUP)
    print(f"Backup created: {BACKUP}")

    with FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for item in data:
        if "category" not in item:
            item["category"] = ""
            added += 1

    with FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Added category field to {added} entries.")

if __name__ == "__main__":
    main()
