# worker.py
import os
import torch
import gc
# Cargar el token de Hugging Face desde las variables de entorno
HF_TOKEN = os.getenv("HF_TOKEN")
from core.models import cargar_modelos
from core.transcription import transcribir, asignar_texto
from core.postprocess import identificar_psicologa, fusionar
from exporters.txt_exporter import guardar_txt
from exporters.docx_exporter import export_to_docx

def run_transcription_process(queue, carpeta, plantilla, modelo):
    """
    Esta función se ejecuta en un proceso separado para realizar todo el trabajo pesado.
    """
    try:
        # Definir y asegurar que la carpeta de salida exista.
        # Esto asume que el script se ejecuta desde la raíz del proyecto.
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        queue.put(('log', f"\n🔹 Proceso de trabajo iniciado (PID: {os.getpid()})"))
        queue.put(('log', f"🔹 Carpeta de audios: {os.path.abspath(carpeta)}"))
        queue.put(('log', f"🔹 Plantilla DOCX: {os.path.abspath(plantilla)}"))
        queue.put(('log', f"🔹 Modelo seleccionado: {modelo}\n"))

        # --- 1. Cargar modelos ---
        queue.put(('log', "⏳ Cargando modelos..."))
        whisper, diar = cargar_modelos(modelo, HF_TOKEN)
        queue.put(5)
        queue.put(('log', "✅ Modelos cargados correctamente\n"))

        # --- Filtrado de archivos ya procesados ---
        queue.put(('log', "🔎 Verificando archivos ya transcritos..."))

        # Obtener lista de todos los audios en la carpeta de origen, soportando más formatos
        all_wav_files = [f for f in os.listdir(carpeta) if f.lower().endswith((".wav", ".mp3", ".flac", ".m4a"))]
        if not all_wav_files:
            queue.put(('done', "No se encontraron archivos de audio compatibles en la carpeta."))
            return

        # Obtener los nombres base (en minúsculas) de los archivos ya transcritos
        # Se considera procesado si existe el .txt O el .docx
        processed_basenames = {
            os.path.splitext(f)[0].replace('_transcrito', '').lower().strip()
            for f in os.listdir(output_dir)
            if f.lower().endswith(('_transcrito.txt', '_transcrito.docx'))
        }
        
        # Filtrar la lista de audios para procesar solo los que no han sido transcritos (comparando en minúsculas)
        wav_files_to_process = [
            wav for wav in all_wav_files 
            if os.path.splitext(wav)[0].lower().strip() not in processed_basenames
        ]

        if not wav_files_to_process:
            queue.put(('done', "✅ ¡Todos los audios en la carpeta ya han sido transcritos!"))
            return
            
        queue.put(('log', f" Mapeo finalizado. {len(wav_files_to_process)} de {len(all_wav_files)} audios serán procesados."))

        total_archivos = len(wav_files_to_process)
        for idx, wav in enumerate(wav_files_to_process, start=1):
            ruta_audio = os.path.join(carpeta, wav)
            base_name = os.path.splitext(wav)[0]
            progress_base = (idx - 1) / total_archivos * 100

            queue.put(('log', f"🎙 Procesando {wav} ({idx}/{total_archivos})..."))
            
            # --- 2. Transcripción ---
            queue.put(('log', "   - Transcribiendo audio..."))
            segmentos_whisper = transcribir(ruta_audio, whisper, idioma="es")
            queue.put(progress_base + (100 / total_archivos) * 0.4)
            queue.put(('log', f"   - Transcripción finalizada, {len(segmentos_whisper)} segmentos detectados."))

            # --- 3. Diarización ---
            queue.put(('log', "   - Diarizando audio (identificando hablantes)..."))
            diarizacion = diar(ruta_audio)
            queue.put(progress_base + (100 / total_archivos) * 0.6)
            queue.put(('log', "   - Diarización finalizada."))

            # --- 4. Post-procesamiento ---
            queue.put(('log', "   - Asignando texto a hablantes y post-procesando..."))
            texto_asignado = asignar_texto(segmentos_whisper, diarizacion)
            psicologa = identificar_psicologa(texto_asignado)
            segmentos_etiquetados = [{"speaker": "Psicóloga" if s["speaker_raw"] == psicologa else "Víctima", "text": s["text"]} for s in texto_asignado]
            segmentos_finales = fusionar(segmentos_etiquetados)
            queue.put(progress_base + (100 / total_archivos) * 0.8)
            queue.put(('log', f"   - Post-procesamiento completado, {len(segmentos_finales)} segmentos finales."))

            # --- 5. Guardar TXT ---
            ruta_txt = os.path.join(output_dir, f"{base_name}_transcrito.txt")
            queue.put(('log', "   - Guardando archivo TXT..."))
            guardar_txt(segmentos_finales, ruta_txt)
            queue.put(progress_base + (100 / total_archivos) * 0.9)
            queue.put(('log', f"✅ TXT generado: {os.path.abspath(ruta_txt)}"))

            # --- 6. Guardar DOCX ---
            ruta_docx = os.path.join(output_dir, f"{base_name}_transcrito.docx")
            
            # Mensaje dinámico según si se usa o no la plantilla
            log_msg = "   - Guardando archivo DOCX (con plantilla)..." if plantilla else "   - Guardando archivo DOCX (básico)..."
            queue.put(('log', log_msg))
            
            # La plantilla es opcional, `export_to_docx` maneja ambos casos.
            export_to_docx(segments=segmentos_finales, output_path=ruta_docx, template_path=plantilla)
            
            queue.put(progress_base + (100 / total_archivos))
            queue.put(('log', f"✅ DOCX generado: {os.path.abspath(ruta_docx)}\n"))

        queue.put(('done', "¡Transcripción completada para todos los archivos!"))

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        queue.put(('error', f"{str(e)}\n\nDetalles:\n{error_details}"))

    finally:
        # La limpieza de memoria es manejada por el sistema operativo al terminar el proceso.
        queue.put(('log', "✅ Proceso de trabajo finalizado."))
