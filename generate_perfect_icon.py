from PIL import Image
import os

def create_perfect_icon(source_png, output_ico):
    print(f"Generando icono maestro desde: {source_png}")
    if not os.path.exists(source_png):
        print(f"Error: No se encuentra el archivo maestro {source_png}")
        return

    # Abrimos la imagen maestra (debe ser de alta resolución, ej: 512x512 o 1024x1024)
    base_img = Image.open(source_png).convert("RGBA")
    
    # Definimos los tamaños estándar para evitar el pixelado en Windows
    # 256px es para vista de iconos muy grandes
    # 48px y 32px son para el escritorio y explorador
    # 16px es para la barra de tareas y el menú de la ventana
    icon_sizes = [256, 128, 64, 48, 32, 16]
    
    # Creamos una lista de imágenes reescaladas con alta calidad (LANCZOS)
    icon_layers = []
    for size in icon_sizes:
        # Usamos LANCZOS para que la reducción de tamaño sea nítida
        layer = base_img.resize((size, size), Image.Resampling.LANCZOS)
        icon_layers.append(layer)
    
    # Guardamos el archivo .ico incluyendo TODAS las capas generadas
    # La primera imagen de la lista es la "principal"
    icon_layers[0].save(
        output_ico, 
        format='ICO', 
        append_images=icon_layers[1:],
        bitmap_format=True # Ayuda a la compatibilidad con versiones antiguas de Windows
    )
    
    print(f"¡Éxito! Icono 'Nivel Élite' creado en: {output_ico}")
    print(f"Capas integradas: {[f'{s}x{s}' for s in icon_sizes]}")

if __name__ == "__main__":
    # Usamos el logo principal como fuente para el icono
    source = "assets/images/png_master/logo.png"
    dest = "assets/images/icon.ico"
    create_perfect_icon(source, dest)
