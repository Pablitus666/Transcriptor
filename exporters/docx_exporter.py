# exporters/docx_exporter.py
from docx import Document
from docx.shared import Pt, Cm, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_page_number(paragraph):
    """
    Añade un campo de número de página a un párrafo en el pie de página.
    """
    # Crear el campo de número de página
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')

    # Añadir los elementos al párrafo
    paragraph.add_run('')._r.append(fldChar1)
    paragraph.add_run('')._r.append(instrText)
    paragraph.add_run('')._r.append(fldChar2)


def export_to_docx(segments, output_path, template_path=None):
    """
    Genera un archivo DOCX. Si se proporciona una plantilla, la utiliza.
    Si no, crea un documento básico desde cero con formato específico.
    """
    if template_path:
        # --- Lógica para usar una plantilla ---
        doc = Document(template_path)
        placeholder_found = False
        
        # Iteramos en una copia para poder modificar la lista original de párrafos
        for p in list(doc.paragraphs):
            if "{{TRANSCRIPCION}}" in p.text:
                # Obtenemos el estilo y la alineación del párrafo marcador
                style = p.style
                alignment = p.alignment
                
                # Insertamos los nuevos párrafos antes del marcador
                for i, segment in enumerate(segments):
                    # Párrafo con texto
                    text_p = p.insert_paragraph_before(f"{segment['speaker']}: {segment['text']}", style)
                    text_p.alignment = alignment

                    # Forzar la fuente a Arial 11 para cada 'run' en el párrafo
                    for run in text_p.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(11)
                    
                    # Añadir un párrafo vacío para el espacio, excepto después del último segmento
                    if i < len(segments) - 1:
                        empty_p = p.insert_paragraph_before("", style)
                        # Forzar la fuente del párrafo vacío añadiendo un run con un espacio
                        run = empty_p.add_run(' ')
                        run.font.name = 'Arial'
                        run.font.size = Pt(11)

                # Eliminamos el párrafo marcador original
                p_element = p._element
                p_element.getparent().remove(p_element)
                
                placeholder_found = True
                # No rompemos el bucle por si el marcador aparece varias veces.
        
        if not placeholder_found:
            doc.add_heading('Transcripción', level=1)
            for s in segments:
                doc.add_paragraph(f"{s['speaker']}: {s['text']}")

    else:
        # --- Lógica para crear un documento desde cero con formato específico ---
        doc = Document()

        # 1. Configuración de página y márgenes
        section = doc.sections[0]
        section.page_height = Mm(330)  # Tamaño Oficio
        section.page_width = Mm(216)   # Tamaño Oficio
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        
        # 3. Añadir numeración de página en el pie de página
        footer = section.footer
        p_footer = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT # Alineación a la derecha
        add_page_number(p_footer)

        # 4. Añadir contenido con el formato especificado
        doc.add_heading('Transcripción', level=1)
        doc.add_paragraph() # Salto de línea después del título
        
        for s in segments:
            par = doc.add_paragraph()
            run = par.add_run(f"{s['speaker']}: {s['text']}")
            run.font.name = 'Arial'
            run.font.size = Pt(11)
            par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.save(output_path)

