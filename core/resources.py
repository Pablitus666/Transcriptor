import os
import sys

def get_base_path():
    """ 
    Obtiene la ruta base del proyecto de forma absoluta y dinámica.
    Garantiza portabilidad total en cualquier PC.
    """
    # 1. Si es el lanzador de PyInstaller (.exe)
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    
    # 2. Si estamos en desarrollo o modo blindado (.py / .pyd)
    # Intentamos detectar la carpeta que contiene 'assets'
    # Empezamos desde la ubicación de este archivo (core/resources.py o core/resources.pyd)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Subimos niveles hasta encontrar la carpeta raíz
    temp_dir = current_dir
    for _ in range(4):
        if os.path.exists(os.path.join(temp_dir, "assets")) or os.path.exists(os.path.join(temp_dir, "whisper_env")):
            return temp_dir
        parent = os.path.dirname(temp_dir)
        if parent == temp_dir: break
        temp_dir = parent
        
    # Último recurso: El directorio de ejecución del proceso
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def get_resource_path(relative_path):
    """ Retorna la ruta absoluta a un recurso. """
    base = get_base_path()
    return os.path.normpath(os.path.join(base, relative_path))

def image_path(filename):
    """ Helper para imágenes con priorización de alta calidad. """
    # Intentar primero en master
    master = get_resource_path(os.path.join("assets", "images", "png_master", filename))
    if os.path.exists(master): return master
    
    # Intentar en images estándar
    standard = get_resource_path(os.path.join("assets", "images", filename))
    return standard

def locale_path(lang_code):
    """ Helper para archivos de idioma. """
    return get_resource_path(os.path.join("assets", "locales", f"{lang_code}.json"))
