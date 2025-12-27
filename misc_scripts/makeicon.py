from PIL import Image

img16  = Image.open("favicon-16x16.png").convert("RGBA")
img512 = Image.open("favicon-master256.png").convert("RGBA")

# Exact copies (no resampling)
img16.save("favicon-16x16.png")

# Downscale from large master
img512.resize((32,32),  Image.Resampling.LANCZOS).save("favicon-32x32.png")
img512.resize((48,48),  Image.Resampling.LANCZOS).save("favicon-48x48.png")
img512.resize((180,180),Image.Resampling.LANCZOS).save("apple-touch-icon.png")

# ICO uses the correct-sized images
img16.save(
    "favicon.ico",
    format="ICO",
    sizes=[(16,16),(32,32),(48,48)]
)

print("Favicons generated correctly.")
