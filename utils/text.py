import re

# ================= NORMALIZACIÓN =================
def norm(t: str) -> str:
    """
    Normaliza texto para detección de patrones:
    - minúsculas
    - sin signos
    - espacios uniformes
    """
    t = t.lower().strip()
    t = re.sub(r"[^\wáéíóúñü\s]", " ", t)
    return re.sub(r"\s+", " ", t)


def normalizar_texto(t: str) -> str:
    """
    Normalización institucional mínima (NO altera literalidad)
    """
    return re.sub(
        r"\bleslim\b|\bleslín\b|\bles lim\b",
        "SLIM",
        t,
        flags=re.IGNORECASE
    )
