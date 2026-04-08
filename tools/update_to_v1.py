from docx import Document
import os

def update_identity():
    files = ["MANUAL.docx", "📘 GUÍA INSTITUCIONAL.docx"]
    
    for path in files:
        if not os.path.exists(path): continue
        doc = Document(path)
        
        for p in doc.paragraphs:
            # Reemplazo de identidad antigua por la nueva
            if "TRANSCRIPTOR ÉLITE" in p.text.upper():
                p.text = p.text.replace("TRANSCRIPTOR ÉLITE V4.0", "TRANSCRIPTOR V1.0")
                p.text = p.text.replace("Transcriptor Élite V4.0", "Transcriptor V1.0")
            
            if "Versión:" in p.text and "4.0.0" in p.text:
                p.text = "Versión: 1.0.0 (Marzo 2026)"
                
        doc.save(path)
        print(f"✅ {path} actualizado a V1.0.")

if __name__ == "__main__":
    update_identity()
