from pathlib import Path

# Run from repo root:  python jane_suggest_names.py
# It scans jane/images_full and prints a table with suggested new names,
# and writes a bash script "jane_rename.sh" you can inspect/edit.

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}

def base_suggestion(stem: str) -> str:
    """
    Very conservative: remove spaces and parentheses, keep letters/numbers.
    You can edit the output file to improve individual names (e.g. 005 -> CampHMKBlue).
    """
    keep = []
    for ch in stem:
        if ch.isalnum():
            keep.append(ch)
        elif ch in ("_", "-"):
            keep.append(ch)
        # skip spaces, parentheses, punctuation etc.
    return "".join(keep) or stem

def main():
    repo = Path(__file__).resolve().parent
    images_full = repo / "jane" / "images_full"

    if not images_full.is_dir():
        print(f"[!] jane/images_full not found at {images_full}")
        return

    files = sorted(p for p in images_full.iterdir()
                   if p.suffix.lower() in IMAGE_EXTS and p.is_file())

    if not files:
        print("[!] No images found in jane/images_full")
        return

    rename_script = repo / "jane_rename.sh"
    lines = ["#!/usr/bin/env bash", "cd \"$(dirname \"$0\")/jane/images_full\" || exit 1", ""]

    print("Original filename  -->  Suggested new filename")
    print("-" * 60)

    for f in files:
        old_name = f.name
        stem, ext = f.stem, f.suffix
        suggested_stem = base_suggestion(stem)
        new_name = suggested_stem + ext.lower()
        print(f"{old_name:35} -> {new_name}")
        if old_name != new_name:
            # mv 'Old Name.jpg' NewName.jpg
            lines.append(f"mv '{old_name}' {new_name}")

    rename_script.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[✓] Wrote suggested rename script: {rename_script}")
    print("    Review and edit jane_rename.sh before running:")
    print("    bash jane_rename.sh")

if __name__ == "__main__":
    main()
