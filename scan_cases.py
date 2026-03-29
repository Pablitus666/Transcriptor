import pandas as pd
import os
import re

# ================= MOTOR DE EXTRACCIÓN DE BIG DATA V2 =================

# --- 1. STOP WORDS DE TÍTULOS (Para ignorar ruidos) ---
TITULOS_DOCS = {
    'CASO', 'CASOS', 'ACTA', 'DECLARACION', 'CAMARA', 'GESELL', 'TARIJA', 'BOLIVIA',
    'ENTREVISTA', 'INFORMATIVA', 'VICTIMA', 'VÍCTIMA', 'RECEPCION', 'RECEPCIÓN',
    'CULMINACION', 'INFORMACTIVA', 'INDORMATIVA', 'ENTRESITA', 'ENTREVSITA',
    'TESTIMONIO', 'ANTICIPO', 'PRUEBA', 'FISCALIA', 'MINISTERIO', 'PUBLICO',
    'DNA', 'SLIM', 'DEFENSORIA', 'NIÑEZ', 'ADOLESCENCIA', 'PSICOLOGO', 'PSICOLOGA'
}

def extract_names_from_excel(path):
    names = set()
    try:
        # Cargamos el Excel y leemos TODAS las celdas
        df = pd.read_excel(path)
        for col in df.columns:
            for val in df[col].dropna():
                val_str = str(val).strip()
                # Si tiene espacios, es probable que sea un nombre completo
                if ' ' in val_str and not any(k in val_str.upper() for k in ['http', 'www', '@', '.com']):
                    # Dividimos en palabras
                    for part in re.split(r'\s+', val_str):
                        p_clean = re.sub(r'[^\wáéíóúñüÁÉÍÓÚÑÜ]', '', part)
                        if len(p_clean) > 2 and p_clean[0].isupper() and p_clean.upper() not in TITULOS_DOCS:
                            names.add(p_clean)
    except Exception as e:
        print(f"Error procesando Excel {path}: {e}")
    return names

def extract_names_from_folders(root_path):
    names = set()
    # Escaneamos los nombres de los archivos .docx (Suelen ser el nombre del caso)
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f.endswith('.docx') and not f.startswith('~$'):
                # Quitamos la extensión y años probables
                name = re.sub(r'\.docx$|\d{4}|[_\-]', ' ', f).strip()
                # Dividimos por espacios
                for part in re.split(r'\s+', name):
                    p_clean = re.sub(r'[^\wáéíóúñüÁÉÍÓÚÑÜ]', '', part)
                    if len(p_clean) > 2 and p_clean[0].isupper() and p_clean.upper() not in TITULOS_DOCS:
                        names.add(p_clean)
    return names

# --- Configuración de rutas ---
RESPALDO_PATH = r"D:\Respaldo Casos"
EXCEL_FILES = [
    r"CASOS CAMARA GESELL 2022.xlsx",
    r"CASOS CAMARA GESELL 2023.xlsx",
    r"CASOS CAMARA GESELL 2024.xlsx"
]

all_extracted_names = set()

# 1. Procesar Excels
for excel in EXCEL_FILES:
    full_path = os.path.join(RESPALDO_PATH, excel)
    if os.path.exists(full_path):
        all_extracted_names.update(extract_names_from_excel(full_path))

# 2. Procesar Carpetas de casos recientes
for folder in ["CASOS 2024", "CASOS 2025", "CASOS 2026", "CASOS SLIM -HIVAN", "Victoria SLIM"]:
    full_path = os.path.join(RESPALDO_PATH, folder)
    if os.path.exists(full_path):
        all_extracted_names.update(extract_names_from_folders(full_path))

# Imprimimos resultados ordenados
print(f"--- TOTAL DE PALABRAS ÚNICAS ENCONTRADAS: {len(all_extracted_names)} ---")
sorted_names = sorted(list(all_extracted_names))
print(sorted_names[:200]) # Ver los primeros 200 para validar
