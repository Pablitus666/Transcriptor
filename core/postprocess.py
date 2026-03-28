# core/postprocess.py
import re
from config.settings import CLAVES_PSICO
from utils.text import normalizar_texto

# ================= IDENTIFICAR PSICÓLOGA (Inteligente V1.0) =================
def identificar_psicologa(segmentos: list, ventana_inicio: float = 300.0) -> str:
    """
    V1.0: Busca al profesional analizando palabras clave SOLO en la ventana inicial.
    Esto evita falsos positivos en el resto del testimonio.
    """
    acum = {}
    for s in segmentos:
        # Solo analizamos segmentos que ocurren en los primeros X segundos (def: 5 min)
        if s.get("start", 0) > ventana_inicio:
            continue
            
        spk = s["speaker_raw"]
        acum.setdefault(spk, "")
        acum[spk] += " " + s["text"].lower().strip()

    for spk, txt in acum.items():
        if any(k in txt for k in CLAVES_PSICO):
            return spk

    # Fallback: Si no detecta nada en la ventana, toma el orador con más texto en esa ventana
    if acum:
        return max(acum, key=lambda k: len(acum[k]))

    return segmentos[0]["speaker_raw"] if segmentos else "Desconocido"

# ================= REFINAMIENTO DE TURNOS (NIVEL ÉLITE V1.0) =================
def refinar_turnos(segmentos_etiquetados: list, prof_label: str) -> list:
    """
    V1.0: Lógica Gramatical Refinada.
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

# ================= SUAVIZAR HABLANTES (Sincronía V1.0) =================
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

# ================= FUSIONAR SEGMENTOS (Atómica V1.0) =================
def fusionar(segmentos: list) -> list:
    """
    V1.0: Fusión ATÓMICA TOTAL.
    Unifica bloques del mismo orador sin importar el tiempo de silencio entre ellos.
    Esto garantiza que el testimonio se lea como un párrafo continuo.
    """
    if not segmentos: return []
    
    salida = []
    actual = segmentos[0].copy()
    
    # Limpiamos posibles saltos de línea en el texto inicial
    actual["text"] = actual["text"].replace("\n", " ").strip()
    
    for s in segmentos[1:]:
        # REGLA DE ORO V1.0: Si es el mismo orador, se pega SIEMPRE.
        if s["speaker"] == actual["speaker"]:
            # Agregamos el texto al bloque actual (limpiando saltos de línea)
            nuevo_texto = s["text"].replace("\n", " ").strip()
            actual["text"] += " " + nuevo_texto
            # Actualizamos el tiempo final
            if s.get("end"): actual["end"] = s["end"]
        else:
            # Cambio de orador: Guardamos el bloque actual y empezamos uno nuevo
            salida.append(actual)
            actual = s.copy()
            actual["text"] = actual["text"].replace("\n", " ").strip()
            
    # Guardamos el último bloque procesado
    salida.append(actual)
    
    return salida
