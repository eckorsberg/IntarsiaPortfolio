import json
import sys
import os

#usage
#python addField.py gallery.json difficulty "medium"
#python addField.py gallery.json year 2025
#python addField.py gallery.json favorite true
#python addField.py gallery.json note null

def main():
    if len(sys.argv) != 4:
        print("Usage: python addField.py gallery.json NEWFIELD DEFAULT")
        return

    filename = sys.argv[1]
    new_field = sys.argv[2]
    default_value = sys.argv[3]

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return

    # Try to parse default_value as int, float, bool, or null
    try:
        parsed_default = json.loads(default_value)
    except json.JSONDecodeError:
        parsed_default = default_value  # Keep as string if JSON fails

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for item in data:
        if new_field not in item:
            item[new_field] = parsed_default
            updated += 1

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Added '{new_field}' = {repr(parsed_default)} to {updated} entries in {filename}.")

if __name__ == "__main__":
    main()
