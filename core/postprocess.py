# core/postprocess.py
import re

CLAVES_PSICO = [
    "soy psicólogo",
    "soy psicóloga",
    "psicologo del slim",
    "psicóloga del slim",
    "psicologo de la defensoría",
    "psicóloga de la defensoría",
    "psicologo de defensoría",
    "psicóloga de defensoría"
]

# ================= NORMALIZAR TEXTO =================
def normalizar_texto(t: str) -> str:
    return re.sub(r"\bleslim\b|\bleslín\b|\bles lim\b", "SLIM", t, flags=re.IGNORECASE)

# ================= IDENTIFICAR PSICÓLOGA =================
def identificar_psicologa(segmentos: list) -> str:
    """
    Devuelve el speaker_raw que corresponde a la psicóloga.
    """
    acum = {}
    for s in segmentos:
        acum.setdefault(s["speaker_raw"], "")
        acum[s["speaker_raw"]] += " " + s["text"].lower().strip()

    for spk, txt in acum.items():
        if any(k in txt for k in CLAVES_PSICO):
            return spk

    # Si no se encuentra, retorna el primer speaker
    return segmentos[0]["speaker_raw"]

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
