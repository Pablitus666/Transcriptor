import os
import json

CONFIG_FILE = "config.json"

def load_config():
    """Carga la configuración desde config.json."""
    defaults = {
        "hf_token": "",
        "last_folder": "",
        "last_template": "",
        "model": "large-v3",
        "prof_gender": "Psicóloga"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Actualizar defaults con lo que existe para no romper si añadimos campos
                defaults.update(config)
        except:
            pass
    return defaults

def save_config(config):
    """Guarda la configuración en config.json."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except:
        pass

def get_hf_token():
    """Busca el token en variable de entorno o en el config.json. 
    Usa un fallback maestro para portabilidad institucional."""
    # 1. Prioridad: Variable de entorno
    token = os.getenv("HF_TOKEN")
    if token:
        return token

    # 2. Segunda opción: Configuración del usuario
    config = load_config()
    token = config.get("hf_token", "")
    if token and token.strip():
        return token

    # 3. Fallback: Configuración local
    return ""
