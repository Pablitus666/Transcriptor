import os
import sys
import multiprocessing
import tkinter as tk

# Asegurar que el directorio raíz esté en el path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def main():
    # Soporte para multiprocessing
    multiprocessing.freeze_support()

    # ID de aplicación para Windows
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('mi.transcriptor.elite.v1')
    except:
        pass

    root = tk.Tk()
    root.withdraw() # Ocultar inmediatamente para evitar parpadeo
    
    try:
        from gui.main_window import TranscriptorGUI
        # La GUI se encarga de centrar y mostrar la ventana (deiconify)
        app = TranscriptorGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        # Solo mostrar si hay un error crítico
        root.deiconify()
        root.title("Error Crítico de Arranque")
        tk.Label(root, text="No se pudo iniciar la aplicación:", fg="red", font=("Arial", 12, "bold")).pack(pady=10)
        text_area = tk.Text(root, height=15, width=80)
        text_area.insert(tk.END, error_msg)
        text_area.pack(padx=20, pady=10)
        tk.Button(root, text="Cerrar", command=root.destroy).pack(pady=10)
        root.mainloop()

if __name__ == "__main__":
    main()
