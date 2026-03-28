# core/postprocess.py
import re
from config.settings import CLAVES_PSICO
from utils.text import normalizar_texto

# ================= IDENTIFICAR PSICÓLOGA =================
def identificar_psicologa(segmentos: list) -> str:
    """
    Busca al profesional (Psicólogo/a) analizando palabras clave.
    """
    acum = {}
    for s in segmentos:
        acum.setdefault(s["speaker_raw"], "")
        acum[s["speaker_raw"]] += " " + s["text"].lower().strip()

    for spk, txt in acum.items():
        if any(k in txt for k in CLAVES_PSICO):
            return spk

    return segmentos[0]["speaker_raw"] if segmentos else "Desconocido"

# ================= REFINAMIENTO DE TURNOS (NIVEL ÉLITE V40) =================
def refinar_turnos(segmentos_etiquetados: list, prof_label: str) -> list:
    """
    V40: Lógica Gramatical Refinada.
    """
    refinado = []
    victima_label = "Víctima"
    esperando_respuesta = False
    
    for s in segmentos_etiquetados:
        texto = s["text"]
        speaker_original = s["speaker"]
        start = s.get("start", 0)
        end = s.get("end", 0)
        
        # 1. Si hay preguntas, cortamos internamente el bloque
        if "?" in texto:
            # Dividimos por bloques que terminan en ? (incluyendo el signo)
            fragmentos = re.split(rf'([^?]*\?)', texto)
            for frag in fragmentos:
                frag = frag.strip()
                if not frag: continue
                
                if frag.endswith("?"):
                    # Es pregunta -> Siempre al Profesional
                    refinado.append({"speaker": prof_label, "text": frag, "start": start, "end": end})
                    esperando_respuesta = True
                else:
                    # Es texto plano tras una pregunta -> Probable respuesta de la Víctima
                    refinado.append({"speaker": victima_label, "text": frag, "start": start, "end": end})
                    esperando_respuesta = False
        else:
            # 2. Si no hay pregunta, pero la IA cree que es la Psico y venimos de una pregunta previa
            if esperando_respuesta and speaker_original == prof_label:
                # Reasignación forzada a Víctima (corrección de error de diarización)
                refinado.append({"speaker": victima_label, "text": texto, "start": start, "end": end})
                esperando_respuesta = False
            else:
                # Caso normal
                refinado.append(s)
                if speaker_original == victima_label:
                    esperando_respuesta = False
                    
    return refinado

# ================= SUAVIZAR HABLANTES (Sincronía V36) =================
def suavizar_hablantes(segmentos: list, umbral_breve: float = 0.5) -> list:
    """
    Filtro anti-parpadeo de oradores.
    """
    if len(segmentos) < 3: return segmentos
    resultado = []
    i = 0
    while i < len(segmentos):
        curr = segmentos[i]
        if 0 < i < len(segmentos) - 1:
            prev = resultado[-1]
            sig = segmentos[i+1]
            duracion = curr.get("end", 0) - curr.get("start", 0)
            if duracion < umbral_breve and prev["speaker"] == sig["speaker"] and curr["speaker"] != prev["speaker"]:
                prev["text"] += " " + curr["text"]
                prev["end"] = curr.get("end", prev["end"])
                i += 1
                continue
        resultado.append(curr)
        i += 1
    return resultado

# ================= FUSIONAR SEGMENTOS (Sincronía V40) =================
def fusionar(segmentos: list, max_silencio: float = 1.5) -> list:
    """
    V40: Fusión ATÓMICA.
    NUNCA permite dos párrafos seguidos del mismo orador.
    Unifica bloques del mismo orador sin importar el silencio para evitar duplicidad de etiquetas.
    """
    if not segmentos: return []
    
    salida = []
    actual = segmentos[0].copy()
    
    for s in segmentos[1:]:
        # REGLA DE ORO V40: Si es el mismo orador, se pega SÍ O SÍ.
        if s["speaker"] == actual["speaker"]:
            # Agregamos el texto al bloque actual
            actual["text"] += " " + s["text"]
            # Actualizamos el tiempo final
            if s.get("end"): actual["end"] = s["end"]
        else:
            # Cambio de orador: Guardamos el bloque actual y empezamos uno nuevo
            salida.append(actual)
            actual = s.copy()
            
    # Guardamos el último bloque procesado
    salida.append(actual)
    
    return salida
