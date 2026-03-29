import re
import json
import os

# ================= LÉXICO INSTITUCIONAL DE ÉLITE =================

# --- 1. CARGOS Y TÍTULOS (Capitalización forzada) ---
TITULOS_CARGOS = {
    "Fiscal", "Investigador", "Psicólogo", "Psicóloga", "Abogado", "Abogada", 
    "Doctor", "Doctora", "Dr", "Dra", "Licenciado", "Licenciada", "Sargento", 
    "Cabo", "Teniente", "Capitán", "Mayor", "Coronel", "General"
}

# --- 2. SIGLAS INSTITUCIONALES (Siempre MAYÚSCULAS) ---
SIGLAS_INSTITUCIONALES = {
    "SLIM", "DNA", "FELCV", "FELCC", "MP", "IDIF", "CUD", "SEPDAVI", "UPAVIT", 
    "DAG", "SIJPLU", "CENVIC", "REJAP", "SIPPA", "TJA", "BOL", "EPI", "SENAC",
    "VCM", "NNA", "FATECIPOL", "UTOP", "PAC", "DAC", "MANGER", "DNNA"
}

# --- 3. ENTIDADES Y LUGARES (Núcleo estructural) ---
ENTIDADES_PROPIAS_BASE = {
    "Tarija", "Bolivia", "Ministerio Público", "Policía Boliviana",
    "Defensoría de la Niñez", "Servicio Legal Integral Municipal",
    "Puente San Martín", "Luis de Fuentes", "Juan XXIII",
    "Barrio", "Mercado", "Campesino", "Villa Abaroa", "La Loma",
    "Senac", "Miraflores", "Velasco", "Villamontes", "Bermejo", "Yacuiba"
}

# --- 4. CARGAR NOMBRES Y APELLIDOS (Desde JSON) ---
NOMBRES_REFERENCIA = set()
try:
    names_path = os.path.join(os.path.dirname(__file__), "person_names.json")
    if os.path.exists(names_path):
        with open(names_path, "r", encoding="utf-8") as f:
            nombres = json.load(f)
            NOMBRES_REFERENCIA = {n.strip() for n in nombres if n.strip()}
except Exception:
    pass

# --- 5. CARGAR CALLES DE TARIJA (Desde JSON) ---
CALLES_TARIJA = set()
STREET_PATTERN = None

try:
    json_path = os.path.join(os.path.dirname(__file__), "tarija_streets.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            calles = json.load(f)
            # Normalizamos calles: añadimos versiones cortas comunes
            extra_calles = {"Avenida Víctor Paz", "Avenida Victor Paz", "Calle Colón", "Calle Colon"}
            CALLES_TARIJA = set(calles).union(extra_calles)
            
            sorted_streets = sorted(list(CALLES_TARIJA), key=len, reverse=True)
            pattern_str = "|".join(re.escape(s) for s in sorted_streets)
            STREET_PATTERN = re.compile(rf"\b({pattern_str})\b", re.IGNORECASE)
except Exception:
    pass

# --- 6. PATRÓN DE ENTIDADES MULTI-PALABRA ---
sorted_entities = sorted(ENTIDADES_PROPIAS_BASE, key=len, reverse=True)
entity_pattern_str = "|".join(re.escape(e) for e in sorted_entities)
ENTITY_PATTERN = re.compile(rf"\b({entity_pattern_str})\b", re.IGNORECASE)

# --- 7. LÉXICO GLOBAL (Consolidado como Diccionario de Búsqueda Rápida) ---
# Mapeamos {palabra_en_minusculas: PalabraCorrectamenteCapitalizada}
LEXICO_GLOBAL_MAP = {}

def _cargar_lexico():
    global LEXICO_GLOBAL_MAP
    # Unimos todos los sets en uno solo para procesar
    union_lexico = SIGLAS_INSTITUCIONALES.union(ENTIDADES_PROPIAS_BASE).union(NOMBRES_REFERENCIA).union(TITULOS_CARGOS)
    
    # Construimos el mapa de búsqueda rápida
    for item in union_lexico:
        # Si el item ya existe (ej: "Dra" y "DRA"), priorizamos la versión con minúsculas si no es sigla
        low = item.lower()
        if low not in LEXICO_GLOBAL_MAP or item.isupper():
            LEXICO_GLOBAL_MAP[low] = item

_cargar_lexico()

# --- 8. MAPEO DE CORRECCIONES QUIRÚRGICAS (Pre-compiladas V1.0) ---
CORRECCIONES_FONETICAS_RAW = {
    r"\bfel\s+se\s+ve\b": "FELCV",
    r"\bfel\s+ce\s+ve\b": "FELCV",
    r"\bfel\s+se\s+ce\b": "FELCC",
    r"\bfel\s+ce\s+ce\b": "FELCC",
    r"\bes\s+lim\b": "SLIM",
    r"\be\s+slim\b": "SLIM",
    r"\beslim\b": "SLIM",
    r"\beslin\b": "SLIM",
    r"\be\s+slin\b": "SLIM",
    r"\bslim\s+in\b": "SLIM",
    r"\bset\s*-?up\b": "centro",
    r"\bset\s*-?u\b": "centro",
    r"\bgio[vw]ana\b": "Giovana",
    r"\bsalinas\b": "Salinas",
    r"\bberr?uga\b": "Berruga",
    r"\bnatviki\b": "snack Viki",
    r"\bparriada\b": "parrillada",
    r"¿También es cierto\?": "Tome asiento",
    r"\btome asiento\b": "Tome asiento",
    r"\bhaz\s+de\s+salteñas\b": "hacer salteñas",
    r"\bhace\s+salteñas\b": "hacer salteñas",
    r"\ba\s+césar\s+teñas\b": "hacer salteñas",
    r"\bcesar\s+teñas\b": "hacer salteñas",
    r"\bcontar[íi]n\b": "Condori",
    r"\bis\s*it\b": "",
    r"\byou\b": "",
    r"\bthank\W*you\b": "gracias",
    r"\bthe\b": "",
    r"\bokay\b": "ya",
    r"\bright\b": "bien",
    r"\bhmm+\b": "",      
    r"\[ruido\]": "",
    r"\[silencio\]": "",
    r"\bya ya\b": "ya",    
    r"\beh\b": ""
}

# Compilación única para máxima velocidad
CORRECCIONES_COMPILADAS = [
    (re.compile(p, re.IGNORECASE), r) for p, r in CORRECCIONES_FONETICAS_RAW.items()
]

STOP_WORDS_ES = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "yo", "tú", "él", "ella", 
    "nosotros", "vosotros", "ellos", "ellas", "mi", "tu", "su", "que", "y", "o", "u", 
    "e", "ni", "pero", "sino", "porque", "pues", "aunque", "si", "no", "sí", "ya", 
    "cuando", "mientras", "donde", "como", "quien", "cual", "cuyo", "para", "por", 
    "con", "sin", "sobre", "tras", "desde", "hasta", "entre", "hacia", "según", 
    "ante", "bajo", "cabe", "contra", "de", "del", "al", "esto", "eso", "aquello",
    "me", "te", "se", "nos", "os", "le", "les", "lo"
}

def capitalizacion_inteligente(texto: str) -> str:
    # 1. Primero corregimos frases completas de calles (multi-palabra)
    if STREET_PATTERN:
        def replace_street(match):
            found = match.group(0).lower()
            for original in CALLES_TARIJA:
                if original.lower() == found:
                    return original
            return match.group(0)
        texto = STREET_PATTERN.sub(replace_street, texto)

    # 2. Corregimos entidades multi-palabra (NUEVO)
    if ENTITY_PATTERN:
        def replace_entity(match):
            found = match.group(0).lower()
            for original in ENTIDADES_PROPIAS_BASE:
                if original.lower() == found:
                    return original
            return match.group(0)
        texto = ENTITY_PATTERN.sub(replace_entity, texto)

    palabras = texto.split()
    if not palabras: return ""
    resultado = []
    for i, palabra in enumerate(palabras):
        # Limpiamos puntuación para comparar
        limpia = re.sub(r"[^\wáéíóúñü]", "", palabra.lower())
        
        if limpia.upper() in SIGLAS_INSTITUCIONALES:
            resultado.append(palabra.upper())
            continue
            
        encontrado = False
        # Buscamos en el léxico global ignorando mayúsculas/minúsculas
        limpia_lower = limpia.lower()
        for lex in LEXICO_GLOBAL:
            if lex.lower() == limpia_lower:
                # Preservamos puntuación original (ej. "tarija," -> "Tarija,")
                p_final = lex + palabra[len(limpia):]
                resultado.append(p_final)
                encontrado = True
                break
        
        if encontrado: continue
        
        # Si la palabra ya venía en mayúscula (por patrones multi-palabra o Whisper), la respetamos
        if palabra and palabra[0].isupper():
            if limpia in STOP_WORDS_ES and i > 0:
                resultado.append(palabra.lower())
            else:
                resultado.append(palabra)
        else:
            resultado.append(palabra)
            
    return " ".join(resultado)

def corregir_texto(t: str) -> str:
    """Aplica correcciones fonéticas usando patrones pre-compilados."""
    for pattern, replacement in CORRECCIONES_COMPILADAS:
        t = pattern.sub(replacement, t)
    return t

def normalizar_texto(t: str) -> str:
    """
    V1.0: Normalización Forense (Reversión a la perfección).
    ELIMINA TODOS LOS PUNTOS (.) para un flujo de texto continuo.
    """
    if not t: return ""
    
    # 1. Quitamos TODOS los puntos (Whisper a veces los pone en lugares erróneos)
    t = t.replace(".", "")
    
    # 2. Correcciones fonéticas y léxicas
    t = corregir_texto(t)
    
    # 3. Limpieza de ruidos y espacios
    t = re.sub(r"\s+", " ", t).strip()
    
    # 4. Capitalización inteligente (Tarija/Cargos/Siglas)
    t = capitalizacion_inteligente(t)
    
    if t:
        # Aseguramos que empiece con mayúscula el bloque
        t = t[0].upper() + t[1:]
        
    return t
