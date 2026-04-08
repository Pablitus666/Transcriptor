import os
import sys
import traceback
import argparse
import subprocess
from datetime import datetime

# ================= BLINDAJE DE RUTAS ELITE =================
# Obtenemos la ruta absoluta del directorio de forma dinámica
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    # Si es un script o un .pyd, buscamos la raíz retrocediendo niveles
    current_file = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(current_file)
    # Si el worker.py estuviera en una subcarpeta, subiríamos un nivel (aquí está en la raíz)
    if not os.path.exists(os.path.join(BASE_DIR, "whisper_env")):
        parent = os.path.dirname(BASE_DIR)
        if os.path.exists(os.path.join(parent, "whisper_env")):
            BASE_DIR = parent

# Rutas clave relativas (INYECCIÓN DE CEREBRO)
WHISPER_ENV_DIR = os.path.join(BASE_DIR, "whisper_env")
SITE_PACKAGES = os.path.join(WHISPER_ENV_DIR, "Lib", "site-packages")
PYTHON_LIB = os.path.join(WHISPER_ENV_DIR, "Lib")

if os.path.exists(WHISPER_ENV_DIR):
    sys.path.insert(0, SITE_PACKAGES)
    sys.path.insert(0, PYTHON_LIB)
    sys.path.insert(0, BASE_DIR)

# Configurar variables de entorno para procesos hijos
os.environ["PYTHONPATH"] = BASE_DIR + os.pathsep + SITE_PACKAGES + os.pathsep + PYTHON_LIB
os.environ["PYTHONIOENCODING"] = "utf-8"

# Forzar UTF-8 en los flujos de salida de Python (Blindaje definitivo contra 'charmap')
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_transcription_standalone():
    parser = argparse.ArgumentParser(description="Worker de Transcripción Élite")
    parser.add_argument("--folder", required=True)
    parser.add_argument("--template", default="")
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--gender", default="Psicóloga")
    
    args = parser.parse_args()

    try:
        # Importación directa gracias al blindaje de rutas previo
        from core.orchestrator import TranscriptorOrchestrator
        from config import persistence

        hf_token = persistence.get_hf_token()
        if not hf_token:
            sys.stdout.write("ERROR: No se ha configurado el Token de Hugging Face.\n")
            sys.stdout.flush()
            return

        def queue_proxy(message):
            """Proxy para convertir mensajes de cola en salida de consola con blindaje de codificación."""
            try:
                if isinstance(message, tuple):
                    command, data = message
                    # Aseguramos que data sea string y manejamos posibles errores de codificación
                    safe_data = str(data).encode('utf-8', 'replace').decode('utf-8')
                    sys.stdout.write(f"{command.upper()}:{safe_data}\n")
                    sys.stdout.flush()
                elif isinstance(message, (int, float)):
                    sys.stdout.write(f"PROG:{message}\n")
                    sys.stdout.flush()
            except:
                pass # El pipeline no debe morir si falla un log

        orchestrator = TranscriptorOrchestrator(queue_callback=queue_proxy)
        sys.stdout.write(f"LOG:Proceso de trabajo iniciado (PID: {os.getpid()})\n")
        sys.stdout.flush()
        
        orchestrator.process_all(
            folder=args.folder,
            template=args.template,
            model_name=args.model,
            hf_token=hf_token,
            prof_gender=args.gender
        )
    except Exception as e:
        # Error crítico con trazado completo, blindado contra fallos de print
        try:
            err_msg = f"Error crítico: {str(e)}"
            sys.stdout.write(f"ERROR:{err_msg}\n")
            sys.stdout.flush()
        except:
            pass
    finally:
        try:
            sys.stdout.write("LOG:Proceso de trabajo finalizado.\n")
            sys.stdout.flush()
        except:
            pass

if __name__ == "__main__":
    run_transcription_standalone()
