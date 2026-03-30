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
    Carga el pipeline de diarización con lógica Offline-First.
    Si los modelos existen en cache, evita conectar a Hugging Face.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    from whisperx.diarize import DiarizationPipeline
    
    cache_path = os.path.join(MODELS_CACHE, "pyannote")
    
    # Comprobar si existe el modelo en caché para forzar modo Offline
    # El archivo 'speaker-diarization-3.1' suele estar en subcarpetas del cache
    local_only = False
    if os.path.exists(cache_path) and any(os.scandir(cache_path)):
        local_only = True

    try:
        return DiarizationPipeline(
            model_name="pyannote/speaker-diarization-3.1",
            token=hf_token,
            device=torch.device(device),
            cache_dir=cache_path
        )
    except Exception as e:
        # Si falla (por falta de red o token), intentamos carga forzada local
        if local_only:
            try:
                # Algunas versiones de la librería permiten cargar directamente desde el repo local
                return DiarizationPipeline(
                    model_name="pyannote/speaker-diarization-3.1",
                    use_auth_token=False, # Ya no pedimos token si es local
                    device=torch.device(device),
                    cache_dir=cache_path
                )
            except:
                raise e
        raise e

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
