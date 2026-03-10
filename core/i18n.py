import json
import locale
import os
import sys
from core import resources

_translations = {}
_current_lang = "es"

def load_translations():
    global _translations, _current_lang
    
    # 1. CARGAR IDIOMA BASE (Español) como fallback absoluto
    try:
        base_path = resources.locale_path("es")
        if os.path.exists(base_path):
            with open(base_path, "r", encoding="utf-8") as f:
                _translations = json.load(f)
    except:
        _translations = {}

    # 2. DETECTAR IDIOMA DEL SISTEMA
    try:
        # getdefaultlocale() puede fallar en algunos entornos, usamos una alternativa robusta
        lang_code = "es"
        try:
            system_lang, _ = locale.getdefaultlocale()
            if system_lang:
                lang_code = system_lang[:2].lower()
        except:
            pass
        
        # 3. CARGAR IDIOMA DETECTADO (si es diferente a español)
        if lang_code != "es":
            path = resources.locale_path(lang_code)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    # Actualizamos el diccionario base con las nuevas traducciones
                    _translations.update(json.load(f))
                    _current_lang = lang_code
            else:
                # Si el idioma no está soportado, mantenemos "es"
                _current_lang = "es"
                
    except Exception as e:
        # En caso de error crítico, nos aseguramos de no romper la app
        print(f"Error loading translations: {e}")

def _(key, **kwargs):
    """ Función de traducción tipo Gettext. """
    text = _translations.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text

# Cargar al importar el módulo
load_translations()
