from PIL import Image
from pathlib import Path

def prepare_full(input_path, output_name):
    img = Image.open(input_path)
    max_side = 2800
    img.thumbnail((max_side, max_side))  # keeps aspect ratio
    out_path = Path("images_full") / output_name
    out_path.parent.mkdir(exist_ok=True)
    img.save(out_path, quality=85, optimize=True)
