from docx import Document
import difflib
import re

def normalize_text(text):
    # Eliminar espacios múltiples y normalizar para comparación justa
    return re.sub(r'\s+', ' ', text).strip()

def extract_only_text(file_path):
    """Extrae SOLO párrafos de texto, ignorando tablas."""
    doc = Document(file_path)
    content = []
    for p in doc.paragraphs:
        txt = normalize_text(p.text)
        # Ignoramos títulos genéricos y párrafos vacíos
        if txt and len(txt) > 2:
            content.append(txt)
    return content

def analyze_precision(script_file, corrected_file):
    print(f"--- ANÁLISIS DE PRECISIÓN (DIÁLOGOS) ---")
    script_content = extract_only_text(script_file)
    corrected_content = extract_only_text(corrected_file)
    
    script_full = "\n".join(script_content)
    corrected_full = "\n".join(corrected_content)
    
    # Calcular similitud textual neta
    similarity = difflib.SequenceMatcher(None, script_full, corrected_full).ratio()
    
    print(f"Nivel de Exactitud del Texto: {similarity*100:.2f}%")
    print(f"Bloques de texto en Script: {len(script_content)}")
    print(f"Bloques de texto en Corregido: {len(corrected_content)}")
    print("-" * 40)

    # Comparación detallada de los primeros 15 turnos
    print("Muestra de Comparación (Script vs Corregido):")
    for i in range(min(len(script_content), len(corrected_content), 15)):
        s_line = script_content[i]
        c_line = corrected_content[i]
        
        if s_line != c_line:
            print(f"\n[Turno {i+1}] ❌ DIFERENCIA DETECTADA")
            print(f"  SCRIPT: {s_line[:120]}...")
            print(f"  CORRIG: {c_line[:120]}...")
        else:
            print(f"[Turno {i+1}] ✅ COINCIDENCIA TOTAL")

if __name__ == "__main__":
    f_script = r"output/Sandra_transcrito.docx"
    f_corrected = r"output/Sandra transcrito corregido.docx"
    analyze_precision(f_script, f_corrected)
