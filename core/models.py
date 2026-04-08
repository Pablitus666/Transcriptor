import os
import sys
import gc
import torch
import warnings
import whisperx

# Silenciar avisos innecesarios para un entorno profesional
warnings.filterwarnings("ignore")

# ================= CONFIGURACIÓN DE PORTABILIDAD ELITE =================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    current_file = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(os.path.dirname(current_file))

MODELS_CACHE = os.path.join(BASE_DIR, "models_cache")
os.makedirs(MODELS_CACHE, exist_ok=True)

os.environ["HF_HOME"] = MODELS_CACHE
os.environ["HUGGINGFACE_HUB_CACHE"] = MODELS_CACHE

def liberar_gpu():
    """Limpia la memoria VRAM de forma agresiva y sincroniza el hardware."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    import time
    time.sleep(1.5)

# ================= MODELOS =================
def cargar_whisper(modelo_name: str):
    """Carga el modelo de WhisperX en GPU."""
    liberar_gpu()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "float32"

    return whisperx.load_model(
        modelo_name,
        device,
        compute_type=compute_type,
        language="es",
        download_root=os.path.join(MODELS_CACHE, "whisper")
    )

def cargar_diarizacion(hf_token: str):
    """Carga el motor de identificación de voces (Diarización)."""
    liberar_gpu()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    from whisperx.diarize import DiarizationPipeline
    cache_path = os.path.join(MODELS_CACHE, "pyannote")
    
    # CORRECCIÓN ÉLITE: Usamos 'token' en lugar de 'use_auth_token'
    try:
        return DiarizationPipeline(
            model_name="pyannote/speaker-diarization-3.1",
            token=hf_token,
            device=torch.device(device),
            cache_dir=cache_path
        )
    except:
        # Modo rescate offline total
        return DiarizationPipeline(
            model_name="pyannote/speaker-diarization-3.1",
            token=None,
            device=torch.device(device),
            cache_dir=cache_path
        )

def cargar_modelo_alineacion(idioma: str):
    """Carga el modelo de sincronización de palabras en GPU."""
    liberar_gpu()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_dir = os.path.join(MODELS_CACHE, "align")
    
    return whisperx.load_align_model(
        language_code=idioma,
        device=device,
        model_dir=model_dir
    )
