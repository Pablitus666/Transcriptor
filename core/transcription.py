# core/transcription.py

import whisperx
from typing import List, Dict
import re
import torch
from core.postprocess import normalizar_texto

# ================= ASIGNACIÓN QUIRÚRGICA V1.0 =================
def asignar_texto_v1(segments_x) -> List[Dict]:
    """
    Convierte los segmentos de WhisperX (ya diarizados) al formato institucional.
    V1.0: Optimización de velocidad y limpieza de logs internos.
    """
    resultado = []
    for s in segments_x:
        text = normalizar_texto(s["text"])
        if not text: continue
        
        # WhisperX nos da el speaker en 'speaker' dentro del segmento
        speaker_raw = s.get("speaker", "SPEAKER_00")
        
        resultado.append({
            "speaker_raw": speaker_raw,
            "text": text,
            "start": s.get("start", 0),
            "end": s.get("end", 0)
        })
    return resultado
