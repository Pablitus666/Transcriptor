import sys
import os
from PIL import Image

def inspect_icon(path):
    print(f"\n--- Inspeccionando: {path} ---")
    if not os.path.exists(path):
        print(f"Error: El archivo '{path}' no existe.")
        return
    
    try:
        with Image.open(path) as img:
            print(f"Formato: {img.format}")
            
            i = 0
            while True:
                try:
                    img.seek(i)
                    width, height = img.size
                    print(f"Capa {i}: {width}x{height}")
                    i += 1
                except EOFError:
                    break
            print(f"Total de capas encontradas: {i}")
    except Exception as e:
        print(f"Error al abrir el icono: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            inspect_icon(path)
    else:
        # Fallback al archivo por defecto si no hay argumentos
        inspect_icon("assets/images/icon.ico")
