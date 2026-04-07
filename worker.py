import os
import sys
import traceback
import multiprocessing
import subprocess

# ================= CLASE SILENTPOPEN ELITE (Herencia Real) =================
_OriginalPopen = subprocess.Popen

class SilentPopen(_OriginalPopen):
    def __init__(self, *args, **kwargs):
        if sys.platform == "win32":
            if 'startupinfo' not in kwargs:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                si.wShowWindow = 0 # SW_HIDE
                kwargs['startupinfo'] = si
            if 'creationflags' not in kwargs:
                kwargs['creationflags'] = 0
            kwargs['creationflags'] |= 0x08000000
        super().__init__(*args, **kwargs)

# Reemplazar la clase para que el proceso de IA herede el silencio
subprocess.Popen = SilentPopen

if sys.platform == "win32":
    try:
        import ctypes
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd: ctypes.windll.user32.ShowWindow(hWnd, 0)
    except: pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def run_transcription_process(queue, carpeta, plantilla, modelo, genero_profesional):
    try:
        from core.orchestrator import TranscriptorOrchestrator
        from config import persistence

        hf_token = persistence.get_hf_token()
        if not hf_token:
            queue.put(('error', "Error: No se ha configurado el Token de Hugging Face."))
            return

        orchestrator = TranscriptorOrchestrator(queue_callback=queue.put)
        queue.put(('log', f"Proceso de trabajo iniciado (PID: {os.getpid()})"))
        
        orchestrator.process_all(
            folder=carpeta,
            template=plantilla,
            model_name=modelo,
            hf_token=hf_token,
            prof_gender=genero_profesional
        )
    except Exception as e:
        queue.put(('error', f"Error crÃ­tico: {str(e)}\n\n{traceback.format_exc()}"))
    finally:
        queue.put(('log', "Proceso de trabajo finalizado."))
