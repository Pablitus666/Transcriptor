import os
import sys
import traceback
import multiprocessing

# Asegurar que el proceso hijo encuentre los módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def run_transcription_process(queue, carpeta, plantilla, modelo, genero_profesional):
    """
    Punto de entrada para el proceso secundario de multiprocessing.
    Las importaciones pesadas se hacen AQUÍ adentro para no congelar la UI.
    """
    try:
        # Importaciones tardías (Lazy Imports) para eficiencia absoluta
        from core.orchestrator import TranscriptorOrchestrator
        from config import persistence
        
        # Cargar el token de Hugging Face de forma robusta
        hf_token = persistence.get_hf_token()
        
        if not hf_token:
            queue.put(('error', "❌ Error: No se ha configurado el Token de Hugging Face.\n\nVaya a Ajustes (⚙) y configure su token."))
            return

        # Iniciamos el orquestador
        orchestrator = TranscriptorOrchestrator(queue_callback=queue.put)
        
        queue.put(('log', f"🔹 Proceso de trabajo iniciado (PID: {os.getpid()})"))
        queue.put(('log', f"🔹 Modelo: {modelo} | Género: {genero_profesional}\n"))

        # Ejecutamos el procesamiento completo
        orchestrator.process_all(
            folder=carpeta,
            template=plantilla,
            model_name=modelo,
            hf_token=hf_token,
            prof_gender=genero_profesional
        )

    except Exception as e:
        error_details = traceback.format_exc()
        queue.put(('error', f"Error crítico en el proceso: {str(e)}\n\n{error_details}"))

    finally:
        queue.put(('log', "✅ Proceso de trabajo finalizado."))
