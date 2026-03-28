# core/transcription.py

import whisperx
from typing import List, Dict
import re
import torch
from core.postprocess import normalizar_texto, identificar_psicologa, fusionar
from utils.text import LEXICO_GLOBAL

# ================= TRANSCRIPCIÓN ÉLITE (WHISPERX) =================
def transcribir_v30(audio_path: str, model, diar_pipeline, align_model, align_metadata, idioma: str = "es") -> List[Dict]:
    """
    Pipeline V30: Transcripción -> Alineación Fonética -> Diarización -> Asignación Word-Level.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 1. Transcribir (faster-whisper internally)
    print("DEBUG: Iniciando fase de transcripción Whisper...")
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=16, language=idioma)
    print(f"DEBUG: Transcripción Whisper finalizada ({len(result['segments'])} segmentos).")
    
    # 2. Alineación Fonética (Wav2Vec2) - Sincronía ±30ms
    print("DEBUG: Iniciando alineación fonética Wav2Vec2...")
    result = whisperx.align(result["segments"], align_model, align_metadata, audio, device, return_char_alignments=False)
    print("DEBUG: Alineación fonética finalizada.")
    
    # 3. Diarización (Usando el motor de WhisperX que ya devuelve un DataFrame)
    print("DEBUG: Iniciando diarización WhisperX...")
    diar_segments = diar_pipeline(audio_path, min_speakers=2, max_speakers=2)
    print("DEBUG: Diarización finalizada.")
    
    # 4. Asignación Word-Level (V30)
    print("DEBUG: Asignando oradores a nivel de palabra...")
    result = whisperx.assign_word_speakers(diar_segments, result)
    print("DEBUG: Asignación finalizada.")
    
    return result["segments"]

# ================= ASIGNACIÓN QUIRÚRGICA V30 =================
def asignar_texto_v30(segments_x) -> List[Dict]:
    """
    Convierte los segmentos de WhisperX (ya diarizados) al formato institucional.
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
