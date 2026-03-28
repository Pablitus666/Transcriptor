import os
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

# ================= MODELOS =================
def cargar_modelos(modelo_name: str, hf_token: str):
    """
    Carga el pipeline de WhisperX (transcripción + alineación) y diarización forzando CUDA.
    """
    # FORZAMOS CUDA PARA MÁXIMA VELOCIDAD
    device = "cuda"
    compute_type = "float16"
    
    # Login oficial en Hugging Face
    if hf_token:
        try:
            from huggingface_hub import login
            login(token=hf_token)
            os.environ["HUGGING_FACE_HUB_TOKEN"] = hf_token
        except:
            pass

    print(f"DEBUG: FORZANDO carga en {device} ({compute_type})")
    
    try:
        # 1. Cargar WhisperX
        print(f"DEBUG: Cargando WhisperX ({modelo_name})...")
        print(f"DEBUG: Torch Version: {torch.__version__} | CUDA: {torch.cuda.is_available()}")

        model = whisperx.load_model(
            modelo_name,
            device,
            compute_type=compute_type,
            language="es",
            download_root=os.path.join(MODELS_CACHE, "whisper")
        )
        print("DEBUG: WhisperX cargado correctamente.")
        # 2. Cargar Pipeline de Diarización vía WhisperX
        print("DEBUG: Cargando Diarización (WhisperX + Pyannote 3.1)...")
        from whisperx.diarize import DiarizationPipeline
        diar_pipeline = DiarizationPipeline(
            model_name="pyannote/speaker-diarization-3.1",
            token=hf_token,
            device=torch.device(device),
            cache_dir=os.path.join(MODELS_CACHE, "pyannote")
        )
        print("DEBUG: Diarización cargada correctamente.")

        return model, diar_pipeline
    except Exception as e:
        print(f"DEBUG ERROR en cargar_modelos: {str(e)}")
        # Solo como último recurso si CUDA falla, avisamos
        print("⚠️ ADVERTENCIA: CUDA falló, intentando con CPU (esto será lento)...")
        return whisperx.load_model(modelo_name, "cpu", compute_type="float32"), None

def cargar_modelo_alineacion(idioma: str, device: str):
    """Carga el modelo de alineación fonética forzando el dispositivo."""
    target_device = "cuda"
    print(f"DEBUG: Cargando modelo de alineación para {idioma} en {target_device}...")
    try:
        model_a, metadata = whisperx.load_align_model(
            language_code=idioma, 
            device=target_device,
            model_dir=os.path.join(MODELS_CACHE, "align")
        )
        print("DEBUG: Alineación cargada correctamente.")
        return model_a, metadata
    except Exception as e:
        print(f"DEBUG ERROR en cargar_modelo_alineacion: {str(e)}")
        raise e
