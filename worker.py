import os
import sys
import traceback
import argparse
import subprocess
from datetime import datetime

# ================= SILENCIADOR GLOBAL ELITE =================
# Este parche intercepta todas las llamadas a subprocess.Popen en el proceso hijo
# para asegurar que herramientas como FFmpeg no disparen ventanas de consola.
import subprocess
_OriginalPopen = subprocess.Popen
class SilentPopen(_OriginalPopen):
    def __init__(self, *args, **kwargs):
        if sys.platform == "win32":
            if 'startupinfo' not in kwargs:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                si.wShowWindow = 0 
                kwargs['startupinfo'] = si
            if 'creationflags' not in kwargs:
                kwargs['creationflags'] = 0
            # CREATE_NO_WINDOW (0x08000000) + DETACHED_PROCESS (0x00000008)
            kwargs['creationflags'] |= 0x08000008
        super().__init__(*args, **kwargs)
subprocess.Popen = SilentPopen

# Desactivar telemetría y chequeos de shell de librerías
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"

# ================= BLINDAJE DE RUTAS ELITE =================
# Obtenemos la ruta absoluta del directorio de forma dinÃ¡mica
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    # Si somos un script, el BASE_DIR es donde estÃ¡ el script
    current_file = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(current_file)
    # Si worker.py estÃ¡ en una subcarpeta (raro), subimos
    if not os.path.exists(os.path.join(BASE_DIR, "whisper_env")):
        parent = os.path.dirname(BASE_DIR)
        if os.path.exists(os.path.join(parent, "whisper_env")):
            BASE_DIR = parent

# Rutas clave relativas
WHISPER_ENV_DIR = os.path.join(BASE_DIR, "whisper_env")
SITE_PACKAGES = os.path.join(WHISPER_ENV_DIR, "Lib", "site-packages")
PYTHON_LIB_BASE = os.path.join(WHISPER_ENV_DIR, "Lib_base")

# Aislamiento e InyecciÃ³n Inteligente de sys.path
# Priorizamos nuestras carpetas pero mantenemos el resto del path como fallback
sys.path = [
    BASE_DIR,
    PYTHON_LIB_BASE,
    SITE_PACKAGES,
] + [p for p in sys.path if p not in (BASE_DIR, PYTHON_LIB_BASE, SITE_PACKAGES)]

# Configurar variables de entorno para procesos hijos
os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
os.environ["PATH"] = os.path.join(WHISPER_ENV_DIR, "Scripts") + os.pathsep + os.environ.get("PATH", "")
os.environ["PYTHONIOENCODING"] = "utf-8"

# Forzar UTF-8 en los flujos de salida de Python (Blindaje definitivo contra 'charmap')
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_transcription_standalone():
    parser = argparse.ArgumentParser(description="Worker de TranscripciÃ³n Ã‰lite")
    parser.add_argument("--folder", required=True)
    parser.add_argument("--template", default="")
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--gender", default="PsicÃ³loga")
    
    args = parser.parse_args()

    try:
        # Debugging de rutas en caso de error (Solo se verÃ¡ si falla la importaciÃ³n)
        try:
            from core.orchestrator import TranscriptorOrchestrator
            from config import persistence
        except ImportError as ie:
            sys.stdout.write(f"ERROR:Fallo de importaciÃ³n: {str(ie)}\n")
            sys.stdout.write(f"LOG:BASE_DIR detectado: {BASE_DIR}\n")
            sys.stdout.write(f"LOG:SYS.PATH actual: {sys.path[:3]}...\n")
            sys.stdout.flush()
            return

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
