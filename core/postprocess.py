# core/postprocess.py
import re
from config.settings import CLAVES_PSICO
from utils.text import normalizar_texto

# ================= IDENTIFICAR PSICÓLOGA =================
def identificar_psicologa(segmentos: list) -> str:
    """
    Busca al profesional (Psicólogo/a) analizando palabras clave en el texto acumulado por cada hablante.
    Si no se detectan claves, devuelve el ID del primer hablante que aparece.
    """
    acum = {}
    for s in segmentos:
        acum.setdefault(s["speaker_raw"], "")
        acum[s["speaker_raw"]] += " " + s["text"].lower().strip()

    for spk, txt in acum.items():
        if any(k in txt for k in CLAVES_PSICO):
            return spk

    # Si no se encuentra ninguna coincidencia clara, asumimos que el primer hablante es el profesional.
    return segmentos[0]["speaker_raw"] if segmentos else "Desconocido"

# ================= FUSIONAR SEGMENTOS =================
def fusionar(segmentos: list) -> list:
    """
    Fusiona segmentos consecutivos del mismo speaker.
    """
    salida, actual = [], None
    for s in segmentos:
        if not actual:
            actual = s
            continue
        if s["speaker"] == actual["speaker"]:
            actual["text"] += " " + s["text"]
        else:
            salida.append(actual)
            actual = s
    if actual:
        salida.append(actual)
    return salida
