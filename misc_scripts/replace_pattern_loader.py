from pathlib import Path

OLD = '<script src="/js/pattern-designer-loader-laser.js"></script>'
NEW = '<script src="/js/pattern-designer-loader.js"></script>'

# Change this to wherever your laser html files live
ROOT = Path("ed/pages")   # e.g. "laser/pages" or "laser" or "."

def main():
    if not ROOT.exists():
        raise SystemExit(f"Folder not found: {ROOT.resolve()}")

    changed = 0
    scanned = 0

    for path in ROOT.rglob("*.html"):
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")

        if OLD not in text:
            continue

        new_text = text.replace(OLD, NEW)

        # Backup once per file (only if it doesn't already exist)
        bak = path.with_suffix(path.suffix + ".bak")
        if not bak.exists():
            bak.write_text(text, encoding="utf-8")

        path.write_text(new_text, encoding="utf-8")
        changed += 1
        print(f"Updated: {path}")

    print(f"\nScanned {scanned} html files.")
    print(f"Changed {changed} files.")

if __name__ == "__main__":
    main()
