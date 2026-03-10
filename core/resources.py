import os
import sys

def get_base_path():
    """ Obtiene la ruta base del proyecto, compatible con PyInstaller. """
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(relative_path):
    """ Retorna la ruta absoluta a un recurso. """
    return os.path.join(get_base_path(), relative_path)

def image_path(filename):
    """ 
    Helper para imágenes. Prioriza la carpeta 'png_master' para 
    obtener la máxima calidad si está disponible.
    """
    master_path = get_resource_path(os.path.join("assets", "images", "png_master", filename))
    if os.path.exists(master_path):
        return master_path
    return get_resource_path(os.path.join("assets", "images", filename))

def locale_path(lang_code):
    """ Helper para archivos de idioma. """
    return get_resource_path(os.path.join("assets", "locales", f"{lang_code}.json"))
