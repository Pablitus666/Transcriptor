import pandas as pd
import os
import re
import json

# ================= MOTOR DE EXTRACCIÓN DE BIG DATA (TOTAL) =================

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
        df = pd.read_excel(path)
        for col in df.columns:
            for val in df[col].dropna():
                val_str = str(val).strip()
                if ' ' in val_str:
                    for part in re.split(r'\s+', val_str):
                        p_clean = re.sub(r'[^\wáéíóúñüÁÉÍÓÚÑÜ]', '', part)
                        if len(p_clean) > 2 and p_clean[0].isupper() and p_clean.upper() not in TITULOS_DOCS:
                            names.add(p_clean.capitalize())
    except Exception:
        pass
    return names

def extract_names_from_folders(root_path):
    names = set()
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f.endswith('.docx') and not f.startswith('~$'):
                name = re.sub(r'\.docx$|\d{4}|[_\-]', ' ', f).strip()
                for part in re.split(r'\s+', name):
                    p_clean = re.sub(r'[^\wáéíóúñüÁÉÍÓÚÑÜ]', '', part)
                    if len(p_clean) > 2 and p_clean[0].isupper() and p_clean.upper() not in TITULOS_DOCS:
                        names.add(p_clean.capitalize())
    return names

RESPALDO_PATH = r"D:\Respaldo Casos"
EXCEL_FILES = [f for f in os.listdir(RESPALDO_PATH) if f.endswith('.xlsx')]

all_extracted_names = set()
for excel in EXCEL_FILES:
    all_extracted_names.update(extract_names_from_excel(os.path.join(RESPALDO_PATH, excel)))

folders = [d for d in os.listdir(RESPALDO_PATH) if os.path.isdir(os.path.join(RESPALDO_PATH, d))]
for folder in folders:
    all_extracted_names.update(extract_names_from_folders(os.path.join(RESPALDO_PATH, folder)))

# Cargar los nombres actuales para no perder nada
json_path = "utils/person_names.json"
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        all_extracted_names.update(json.load(f))

# Guardar todo
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(sorted(list(all_extracted_names)), f, ensure_ascii=False, indent=4)

print(f"Extracción TOTAL completada: {len(all_extracted_names)} nombres en el diccionario.")
