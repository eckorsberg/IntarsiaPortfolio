from PIL import Image
imgs = [Image.open("favicon-16x16.png"),
        Image.open("favicon-32x32.png"),
        Image.open("favicon-48x48.png")]
imgs[1].save("favicon.ico", sizes=[(16,16),(32,32),(48,48)])

