from PIL import Image, ImageFilter, ImageChops

def add_shadow(image: Image.Image, offset=(3, 3), shadow_color=(0, 0, 0, 100), blur_radius=4, border=5):
    """ Añade una sombra paralela profesional similar a Wordy. """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Añadir margen para la sombra y el desenfoque
    pad_x = abs(offset[0]) + border + blur_radius
    pad_y = abs(offset[1]) + border + blur_radius
    
    total_width = image.width + 2 * pad_x
    total_height = image.height + 2 * pad_y
    
    canvas = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
    
    # Crear la silueta de la sombra usando el canal alfa
    shadow_layer = Image.new('RGBA', image.size, shadow_color)
    canvas.paste(shadow_layer, (pad_x + offset[0], pad_y + offset[1]), image.getchannel('A'))
    
    # Aplicar desenfoque gaussiano para suavidad
    if blur_radius > 0:
        canvas = canvas.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Pegar la imagen original encima
    canvas.paste(image, (pad_x, pad_y), image)
    return canvas

def add_relief(image: Image.Image, intensity=2):
    """ 
    Aplica un efecto de relieve de 3 capas (Luz + Sombra + Original).
    Replica el acabado de botones y títulos de Wordy.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    width, height = image.size
    
    # Capas de luz (blanco suave) y sombra (negro suave)
    light_layer = Image.new('RGBA', (width, height), (255, 255, 255, 130))
    dark_layer = Image.new('RGBA', (width, height), (0, 0, 0, 130))

    relief_canvas = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # 1. Dibujar Sombra (desplazada abajo-derecha)
    relief_canvas.paste(dark_layer, (intensity, intensity), image.getchannel('A'))
    
    # 2. Dibujar Luz (desplazada arriba-izquierda)
    relief_canvas.paste(light_layer, (-intensity, -intensity), image.getchannel('A'))

    # 3. Dibujar Imagen Original (sin desplazamiento para efecto de elevación)
    relief_canvas.paste(image, (0, 0), image)

    return relief_canvas
