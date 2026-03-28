import os
import gc
import torch
import warnings
import whisperx

# Silenciar avisos innecesarios para un entorno profesional
warnings.filterwarnings("ignore")

# ================= CONFIGURACIÓN DE PORTABILIDAD =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_CACHE = os.path.join(BASE_DIR, "models_cache")
os.makedirs(MODELS_CACHE, exist_ok=True)

os.environ["HF_HOME"] = MODELS_CACHE
os.environ["HUGGINGFACE_HUB_CACHE"] = MODELS_CACHE

def liberar_gpu():
    """Limpia la memoria VRAM de forma agresiva."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

# ================= MODELOS =================
def cargar_whisper(modelo_name: str):
    """Carga solo el modelo de WhisperX."""
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
    """
    Carga solo el pipeline de diarización.
    Optimizado para funcionamiento 100% Offline (V1.0).
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    from whisperx.diarize import DiarizationPipeline
    
    # Intentamos cargar con el token, pero priorizando el caché local
    return DiarizationPipeline(
        model_name="pyannote/speaker-diarization-3.1",
        token=hf_token,
        device=torch.device(device),
        cache_dir=os.path.join(MODELS_CACHE, "pyannote")
    )

def cargar_modelo_alineacion(idioma: str):
    """Carga el modelo de alineación fonética."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return whisperx.load_align_model(
        language_code=idioma, 
        device=device,
        model_dir=os.path.join(MODELS_CACHE, "align")
    )

# Mantener compatibilidad con firmas antiguas si es necesario (legacy)
def cargar_modelos(modelo_name: str, hf_token: str):
    """Legacy: Carga todo a la vez (No recomendado para GPUs con poca VRAM)."""
    m = cargar_whisper(modelo_name)
    d = cargar_diarizacion(hf_token)
    return m, d
