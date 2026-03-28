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
    "VCM", "NNA", "FATECIPOL", "UTOP", "PAC", "DAC", "MANGER"
}

# --- 3. ENTIDADES Y LUGARES (Capitalización Correcta) ---
ENTIDADES_PROPIAS = {
    "Tarija", "Bolivia", "San Martín", "Puente San Martín", "Luis de Fuentes", 
    "Senac", "Miraflores", "Velasco", "Villamontes", "Bermejo", "Yacuiba",
    "Juan XXIII", "Erika", "Bovarín", "Vázquez", "Sandra", "Lorena", "Condori",
    "Guerrero", "Rodrigo", "Cristian", "Choque", "Torito", "Giovana", "Salinas",
    "Berruga", "Ministerio Público", "Policía Boliviana",
    "Defensoría de la Niñez", "Servicio Legal Integral Municipal", "Altamira",
    "Lourdes", "Morros", "Blanca", "Flor", "Tabladita", "Villa Abaroa", 
    "La Loma", "Padcaya", "Barrio", "Mercado", "Campesino"
}

# --- 4. APELLIDOS Y NOMBRES COMUNES (Para evitar alucinaciones) ---
NOMBRES_REFERENCIA = {
    "Mamani", "Quispe", "Condori", "Choque", "Vargas", "Guzmán", "Pinto", 
    "Sánchez", "Torres", "Flores", "Rojas", "Zeballos", "Téllez",
    "Villca", "Aruquipa", "Yucra", "Nina", "Copa", "Apaza", "Limachi",
    "Alarcón", "Antezana", "Aparicio", "Arancibia", "Aliaga", "Machicado", 
    "Corrillo", "Cuiza", "Gallardo", "Husler", "Jurado", "Valdez", "Cortez",
    "Jhoanes", "Abelina", "Adán", "Adolfo", "Alexia", "Aníbal", "Aparicio",
    "Benítez", "Cardozo", "Escalante", "Figueroa", "Gutiérrez", "Heredia",
    "Ibáñez", "Jiménez", "López", "Méndez", "Navarro", "Orozco", "Peralta",
    "Quintana", "Ramírez", "Serrano", "Ugarte", "Vaca", "Zambrana",
    "Pamela", "Obando", "Loayza", "Marcia", "Peralta", "Liliana", "Espinoza",
    "Litzi", "Villegas", "Erica", "Bobarin", "Vasquez", "Nelson", "Gareca",
    "Ruiz", "Beymar", "Vera", "Nayda", "Wilson", "Carvajal", "Romina",
    "Aramayo", "Ricaldi", "Siles", "Noelia", "Camacho", "Yandira", "Lucía"
}

# --- 5. CARGAR CALLES DE TARIJA (Desde JSON) ---
CALLES_TARIJA = set()
STREET_PATTERN = None

try:
    json_path = os.path.join(os.path.dirname(__file__), "tarija_streets.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            calles = json.load(f)
            CALLES_TARIJA = set(calles)
            # Creamos un patrón optimizado que busca cualquier calle de la lista
            # Ordenamos por longitud descendente para que 'Av. Victor Paz' coincida antes que 'Av. Victor'
            sorted_streets = sorted(calles, key=len, reverse=True)
            pattern_str = "|".join(re.escape(s) for s in sorted_streets)
            STREET_PATTERN = re.compile(rf"\b({pattern_str})\b", re.IGNORECASE)
except Exception:
    pass

# Unimos todo para el Lexico Global
LEXICO_GLOBAL = SIGLAS_INSTITUCIONALES.union(ENTIDADES_PROPIAS).union(NOMBRES_REFERENCIA).union(TITULOS_CARGOS)

# --- 6. MAPEO DE CORRECCIONES QUIRÚRGICAS (Pre-compiladas V1.0) ---
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
    # 1. Primero corregimos frases completas de calles (multi-palabra) usando el patrón optimizado
    if STREET_PATTERN:
        def replace_street(match):
            found = match.group(0).lower()
            # Buscamos la versión original con capitalización correcta en nuestro set
            for original in CALLES_TARIJA:
                if original.lower() == found:
                    return original
            return match.group(0) # Fallback (no debería pasar)
            
        texto = STREET_PATTERN.sub(replace_street, texto)

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
        for lex in LEXICO_GLOBAL:
            if lex.lower() == limpia:
                # Preservamos puntuación original
                p_final = lex + palabra[len(limpia):]
                resultado.append(p_final)
                encontrado = True
                break
        
        if encontrado: continue
        
        # Si la palabra ya venía en mayúscula, la respetamos a menos que sea stop word
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
