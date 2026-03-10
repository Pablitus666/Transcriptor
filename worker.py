import os
import sys
import traceback
from core.orchestrator import TranscriptorOrchestrator

# Asegurar que el proceso hijo encuentre los módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Cargar el token de Hugging Face desde las variables de entorno
HF_TOKEN = os.getenv("HF_TOKEN")

def run_transcription_process(queue, carpeta, plantilla, modelo, genero_profesional):
    """
    Punto de entrada para el proceso secundario de multiprocessing.
    Utiliza el TranscriptorOrchestrator para realizar el trabajo.
    """
    try:
        # Iniciamos el orquestador pasándole el método put de la cola para los mensajes
        orchestrator = TranscriptorOrchestrator(queue_callback=queue.put)
        
        queue.put(('log', f"\n🔹 Proceso de trabajo iniciado (PID: {os.getpid()})"))
        queue.put(('log', f"🔹 Carpeta de audios: {os.path.abspath(carpeta)}"))
        queue.put(('log', f"🔹 Plantilla DOCX: {os.path.abspath(plantilla) if plantilla else 'Básica'}"))
        queue.put(('log', f"🔹 Modelo seleccionado: {modelo}"))
        queue.put(('log', f"🔹 Género profesional: {genero_profesional}\n"))

        # Ejecutamos el procesamiento completo
        orchestrator.process_all(
            folder=carpeta,
            template=plantilla,
            model_name=modelo,
            hf_token=HF_TOKEN,
            prof_gender=genero_profesional
        )

    except Exception as e:
        error_details = traceback.format_exc()
        queue.put(('error', f"{str(e)}\n\nDetalles:\n{error_details}"))

    finally:
        queue.put(('log', "✅ Proceso de trabajo finalizado."))
