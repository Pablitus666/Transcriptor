import os
import sys

def get_base_path():
    """ 
    Obtiene la ruta base del proyecto de forma dinámica y portátil.
    Compatible con PyInstaller (.exe), Nuitka (.pyd) y Scripts (.py).
    """
    # 1. Si es un ejecutable compilado (PyInstaller)
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    
    # 2. Si es ejecución desde script o módulo blindado (.py o .pyd)
    # Buscamos el archivo 'main.py' o 'Transcriptor.exe' para confirmar la raíz
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    
    # Subimos niveles hasta encontrar la carpeta 'assets' o 'whisper_env'
    # Esto nos permite ser portátiles incluso si el .pyd está en subcarpetas
    temp_dir = current_dir
    for _ in range(3): # Máximo 3 niveles de profundidad (ej: core/sub/sub/)
        if os.path.exists(os.path.join(temp_dir, "assets")) or os.path.exists(os.path.join(temp_dir, "whisper_env")):
            return temp_dir
        parent = os.path.dirname(temp_dir)
        if parent == temp_dir: break
        temp_dir = parent
        
    # Fallback: Si no detectamos nada, devolvemos el directorio actual del script principal
    return os.getcwd()

def get_resource_path(relative_path):
    """ Retorna la ruta absoluta a un recurso de forma dinámica. """
    return os.path.normpath(os.path.join(get_base_path(), relative_path))

def image_path(filename):
    """ Helper para imágenes con priorización de alta calidad. """
    master_path = get_resource_path(os.path.join("assets", "images", "png_master", filename))
    if os.path.exists(master_path):
        return master_path
    return get_resource_path(os.path.join("assets", "images", filename))

def locale_path(lang_code):
    """ Helper para archivos de idioma. """
    return get_resource_path(os.path.join("assets", "locales", f"{lang_code}.json"))
