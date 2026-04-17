import os
import sys

# ================= BLINDAJE DE RUTAS ELITE (ARRANQUE ULTRA-TEMPRANO) =================
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas clave relativas
WHISPER_ENV_DIR = os.path.join(BASE_DIR, "whisper_env")
PYTHON_EXE = os.path.join(WHISPER_ENV_DIR, "Scripts", "pythonw.exe")
if not os.path.exists(PYTHON_EXE):
    PYTHON_EXE = os.path.join(WHISPER_ENV_DIR, "Scripts", "python.exe")

# Exportar para procesos hijos
os.environ["APP_PYTHON_EXE"] = PYTHON_EXE

SITE_PACKAGES = os.path.join(WHISPER_ENV_DIR, "Lib", "site-packages")
PYTHON_LIB_BASE = os.path.join(WHISPER_ENV_DIR, "Lib_base")
PYTHON_LIB_VENV = os.path.join(WHISPER_ENV_DIR, "Lib") # Para site-packages si fuera el caso

# Inyección inteligente de rutas (Limpieza y reconstrucción de sys.path)
# Ponemos nuestras rutas al principio para que ignoren cualquier Python instalado en el sistema
sys.path = [
    BASE_DIR,
    PYTHON_LIB_BASE,
    os.path.join(PYTHON_LIB_BASE, "lib-tk"), # Soporte Tkinter antiguo si existiera
    SITE_PACKAGES,
] + [p for p in sys.path if "site-packages" not in p and "Python311" not in p]

# Configurar variables de entorno para procesos hijos (Worker)
os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
os.environ["PATH"] = os.path.join(WHISPER_ENV_DIR, "Scripts") + os.pathsep + os.environ.get("PATH", "")

# Forzar rutas de Tcl/Tk para que la interfaz se vea en cualquier PC
os.environ["TCL_LIBRARY"] = os.path.join(WHISPER_ENV_DIR, "tcl", "tcl8.6")
os.environ["TK_LIBRARY"] = os.path.join(WHISPER_ENV_DIR, "tcl", "tk8.6")

# Ahora sÃ­, importamos lo demÃ¡s
import multiprocessing
import subprocess

# ================= SILENCIADOR GLOBAL ELITE =================
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

# Desactivar telemetría y ruidos de consola de librerías de IA
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"
os.environ["PYTHONIOENCODING"] = "utf-8"

# ================= ANCLAJE DRAG & DROP ELITE =================
tkdnd_path = os.path.join(SITE_PACKAGES, "tkinterdnd2", "tkdnd")
if os.path.exists(tkdnd_path):
    os.environ["TKDND_LIBRARY"] = tkdnd_path

def main():
    if sys.platform == "win32":
        import ctypes
        try: ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
        except: pass
    
    multiprocessing.freeze_support()

    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('pabletez.transcriptor.v1.0')
    except: pass

    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
        root.withdraw()
        
        # Cargamos la GUI (intentarÃ¡ cargar desde .pyd o .py)
        from gui.main_window import TranscriptorGUI
        app = TranscriptorGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        
        import tkinter as tk
        from tkinter import scrolledtext
        
        root_err = tk.Tk()
        root_err.title("Error CrÃ­tico de Arranque - Blindaje Activo")
        root_err.geometry("800x600")
        
        lbl = tk.Label(root_err, text="Se ha detectado un error al cargar el motor:", font=("Segoe UI", 12, "bold"))
        lbl.pack(pady=10)
        
        # Mostramos tambiÃ©n el sys.path para depuraciÃ³n
        debug_info = f"BASE_DIR: {BASE_DIR}\n"
        debug_info += f"SYS.PATH: {sys.path}\n\n"
        debug_info += f"ERROR:\n{error_msg}"
        
        txt = scrolledtext.ScrolledText(root_err, width=90, height=25)
        txt.insert(tk.END, debug_info)
        txt.pack(padx=20, pady=10)
        
        tk.Button(root_err, text="Cerrar", command=root_err.destroy, width=20).pack(pady=10)
        root_err.mainloop()

if __name__ == "__main__":
    main()
