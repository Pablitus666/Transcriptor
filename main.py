import os
import sys
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
            kwargs['creationflags'] |= 0x08000000 
        super().__init__(*args, **kwargs)
subprocess.Popen = SilentPopen

# ================= ANCLAJE DRAG & DROP ELITE =================
# Forzamos a Python a encontrar la librerÃ­a tkdnd que estÃ¡ en whisper_env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
tkdnd_path = os.path.join(BASE_DIR, "whisper_env", "Lib", "site-packages", "tkinterdnd2", "tkdnd")

if os.path.exists(tkdnd_path):
    os.environ["TKDND_LIBRARY"] = tkdnd_path

if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        try: ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
        except: pass
    multiprocessing.freeze_support()

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def main():
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('pabletez.transcriptor.v1.0')
    except: pass

    from tkinterdnd2 import TkinterDnD
    # Inicializamos la GUI con soporte extendido de Drag & Drop
    root = TkinterDnD.Tk()
    root.withdraw()
    
    try:
        from gui.main_window import TranscriptorGUI
        app = TranscriptorGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        root.deiconify()
        root.title("Error CrÃ­tico de Arranque")
        import tkinter as tk
        text_area = tk.Text(root, height=15, width=80)
        text_area.insert(tk.END, error_msg)
        text_area.pack(padx=20, pady=10)
        tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
        root.mainloop()

if __name__ == "__main__":
    main()
