from docx import Document
import os

def update_manual():
    path = "MANUAL.docx"
    if not os.path.exists(path): return
    doc = Document(path)
    
    # Actualizar Título y Versión
    for p in doc.paragraphs:
        if "MANUAL DE USUARIO" in p.text.upper():
            p.text = "MANUAL DE USUARIO - TRANSCRIPTOR ÉLITE V4.0"
        if "Versión" in p.text:
            p.text = "Versión: 4.0.0 (Edición Forense - Marzo 2026)"

    # Añadir sección de nuevas características Élite
    doc.add_heading('Novedades de la Versión 4.0 (Forense)', level=1)
    novedades = [
        "• Motor WhisperX V30: Alineación fonética con precisión de ±30ms.",
        "• Aceleración por GPU: Optimizado para NVIDIA CUDA 12.1 (procesamiento ultra-rápido).",
        "• Lógica Gramatical de Turnos (V40): Identificación inteligente de oradores en diálogos 'Pregunta-Respuesta'.",
        "• Fusión Atómica: Eliminación total de duplicados de etiquetas de orador.",
        "• Diccionario Geográfico: Integración de 1,120 calles de Tarija para capitalización automática."
    ]
    for n in novedades:
        doc.add_paragraph(n)

    doc.save(path)
    print(f"✅ {path} actualizado.")

def update_guia():
    path = "📘 GUÍA INSTITUCIONAL.docx"
    if not os.path.exists(path): return
    doc = Document(path)
    
    # Actualizar contenido institucional
    for p in doc.paragraphs:
        if "TRANSCRIPTOR" in p.text.upper() and "V" in p.text:
            p.text = "TRANSCRIPTOR ÉLITE V4.0 - SISTEMA DE INTELIGENCIA FORENSE"
            
    # Insertar párrafo de cumplimiento técnico
    doc.add_heading('Especificaciones Forenses V4.0', level=2)
    doc.add_paragraph(
        "La versión 4.0 integra el motor Grammatical Turn Engine V40, el cual garantiza la integridad "
        "de la diarización mediante el análisis sintáctico de las interrogaciones, asignando "
        "automáticamente las respuestas a la víctima y las preguntas al profesional psicólogo/a."
    )
    doc.add_paragraph(
        "Se incluye el Lexicón OSM Tarija para la normalización de direcciones y barrios institucionales."
    )

    doc.save(path)
    print(f"✅ {path} actualizado.")

if __name__ == "__main__":
    update_manual()
    update_guia()
