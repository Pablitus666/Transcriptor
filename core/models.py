import os
import torch

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

try:
    from pyannote.audio import Pipeline
except ImportError:
    raise ImportError("pyannote is not installed. Install it using: pip install pyannote.audio")

# ================= MODELOS =================
def cargar_modelos(
    modelo: str,
    hf_token: str
):
    """
    Carga y devuelve:
    - modelo Whisper (faster-whisper)
    - pipeline de diarización (pyannote)
    """

    device = "cuda" if torch.cuda.is_available() else "cpu"

    whisper = WhisperModel(
        modelo,
        device=device,
        compute_type="float16" if device == "cuda" else "float32"
    )

    diar = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token
    ).to(torch.device(device))

    return whisper, diar
