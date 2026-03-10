# core/transcription.py

from typing import List, Dict
from core.postprocess import normalizar_texto, identificar_psicologa, fusionar


# ================= TRANSCRIPCIÓN =================
def transcribir(path, whisper, idioma: str = "es") -> List:
    """
    Transcribe el audio completo sin VAD para preservar literalidad.
    """
    segments, _ = whisper.transcribe(
        path,
        language=idioma,
        vad_filter=False,
        beam_size=5,
        word_timestamps=True
    )
    return list(segments)

# ================= IOU =================
def iou(a1, a2, b1, b2) -> float:
    """
    Calcula Intersection over Union de dos segmentos de tiempo.
    """
    inter = max(0, min(a2, b2) - max(a1, b1))
    union = max(a2, b2) - min(a1, b1)
    return inter / union if union > 0 else 0

# ================= ASIGNACIÓN TEXTO =================
def asignar_texto(segments_w, diar) -> List[Dict]:
    """
    Asigna cada segmento de Whisper al hablante correcto usando IOU.
    Si un segmento no tiene solapamiento, se asigna al hablante previo para evitar pérdida de datos.
    """
    resultado = []
    last_speaker = None

    diar_turnos = [
        (t.start, t.end, speaker)
        for t, _, speaker in diar.itertracks(yield_label=True)
    ]

    for s in segments_w:
        mejor_speaker = None
        mejor_overlap = 0

        # Si no hay turnos de diarización (ej. audio demasiado corto o silencioso), 
        # asignamos a un hablante genérico para no perder el texto.
        if not diar_turnos:
            mejor_speaker = "Hablante 0"
        else:
            for start, end, speaker in diar_turnos:
                overlap = iou(s.start, s.end, start, end)
                if overlap > mejor_overlap:
                    mejor_overlap = overlap
                    mejor_speaker = speaker

        # Lógica Robusta: Si no hay overlap claro, usar el último hablante detectado
        # (o el primero de la diarización si es el primer segmento de whisper)
        if not mejor_speaker:
            mejor_speaker = last_speaker if last_speaker else (diar_turnos[0][2] if diar_turnos else "Hablante 0")

        if s.text.strip():
            resultado.append({
                "speaker_raw": mejor_speaker,
                "text": normalizar_texto(s.text.strip())
            })
            last_speaker = mejor_speaker

    return resultado

# ================= PROCESAR COMPLETO =================
def procesar(path, whisper, diar) -> List[Dict]:
    """
    Ejecuta todo el pipeline: transcripción, diarización, asignación de texto
    y etiquetado de hablantes (Psicóloga / Víctima).
    """
    # Transcribir audio
    seg = transcribir(path, whisper, idioma="es")

    # Diarización
    diarizacion = diar(path)

    # Asignar cada segmento al hablante correspondiente
    base = asignar_texto(seg, diarizacion)

    # Identificar quién es la psicóloga
    psico = identificar_psicologa(base)

    # Etiquetado final
    etiquetados = [{
        "speaker": "Psicóloga" if s["speaker_raw"] == psico else "Víctima",
        "text": s["text"]
    } for s in base]

    # Fusionar segmentos consecutivos del mismo hablante
    return fusionar(etiquetados)
