import os
from PIL import Image

folder = "ICONO_ELITE"
for file in os.listdir(folder):
    if file.endswith(".ico"):
        path = os.path.join(folder, file)
        try:
            img = Image.open(path)
            sizes = img.info.get('sizes')
            print(f"Icono: {file} - Tamaños detectados: {sizes}")
        except Exception as e:
            print(f"Error con {file}: {e}")
