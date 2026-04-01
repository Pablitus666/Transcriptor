import os
import sys
import multiprocessing
import queue
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from PIL import Image, ImageTk, ImageFilter, ImageOps
from tkinterdnd2 import DND_FILES

# Importaciones de motor visual modular
from core.image_manager import ImageManager
from core import resources
from core.i18n import _
from config import persistence
from gui.widgets import create_image_button
from gui.about_window import AboutWindow
from gui.dialogs import StyledDialog

# ===================== PALETA DE COLORES VENTANA PRINCIPAL =====================
BG_COLOR = "#023047"
ACCENT_COLOR = "#fcbf49"
TEXT_COLOR = "white"
FONT_FAMILY = "Segoe UI"

# ===================== VENTANA PRINCIPAL =====================
class TranscriptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(_("app.title"))
        self.root.configure(bg=BG_COLOR)

        # Inicializar el motor visual modular e internacionalización
        self.image_manager = ImageManager(self.root)
        self.config = persistence.load_config()

        # Carpeta, plantilla y gÃ©nero profesional siempre por defecto al iniciar.
        self.carpeta_var = tk.StringVar(value="")
        self.plantilla_var = tk.StringVar(value="")
        self.genero_profesional_var = tk.StringVar(value=_("role.psychologist_f"))

        
        # Persistimos también el modelo y el token de Hugging Face
        self.modelo_var = tk.StringVar(value=self.config.get("model", "large-v3"))
        self.hf_token_var = tk.StringVar(value=self.config.get("hf_token", ""))
        self.transcribiendo = False
        
        # Rutas de assets
        self.title_path = resources.image_path("titulo.png")
        self.logo_path = resources.image_path("logo.png")
        self.icon_path = resources.image_path("icon.ico")
        self.boton_path = resources.image_path("boton.png")

        try:
            self.root.iconbitmap(self.icon_path)
        except:
            pass

        self.progress_queue = multiprocessing.Queue()
        self.proceso_hijo = None

        ancho, alto = 870, 670
        self.root.resizable(False, False)
        self.centrar_ventana(ancho, alto)

        self.crear_widgets()
        
        # Registrar Drag & Drop
        self.entry_carpeta.drop_target_register(DND_FILES)
        self.entry_carpeta.dnd_bind('<<Drop>>', self._handle_drop)
        
        self.entry_plantilla.drop_target_register(DND_FILES)
        self.entry_plantilla.dnd_bind('<<Drop>>', self._handle_template_drop)

        self.root.bind("<Delete>", self.limpiar_campos)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.check_queue()
        
        # Mostrar ventana solo cuando esté lista y centrada
        self.root.deiconify()

    def on_closing(self):
        # Guardar configuración antes de cerrar
        self.guardar_config_actual()
        if self.transcribiendo:
            dialog = StyledDialog(self.root, _("dialog.exit.title"), 
                                  _("dialog.exit.message"),
                                  dialog_type="question", image_manager=self.image_manager)
            if dialog.show():
                if self.proceso_hijo and self.proceso_hijo.is_alive():
                    self.proceso_hijo.terminate()
                self.root.destroy()
        else:
            self.root.destroy()

    def guardar_config_actual(self):
        """Sincroniza el estado de la UI con el archivo config.json."""
        # Nota: Guardamos estos valores pero el __init__ solo carga los que queremos recordar.
        self.config["last_template"] = self.plantilla_var.get()
        self.config["model"] = self.modelo_var.get()
        self.config["hf_token"] = self.hf_token_var.get()
        persistence.save_config(self.config)

    def mostrar_config_token(self):
        """Diálogo profesional para configurar el token de Hugging Face sin parpadeos."""
        if self.transcribiendo: return
        
        dialog_win = tk.Toplevel(self.root)
        dialog_win.withdraw() 
        dialog_win.title("Configuración")
        dialog_win.configure(bg=BG_COLOR)
        dialog_win.resizable(False, False)
        dialog_win.transient(self.root)
        dialog_win.grab_set()

        try:
            dialog_win.iconbitmap(self.icon_path)
        except:
            pass

        ww, wh = 450, 200
        px = self.root.winfo_x() + (self.root.winfo_width() // 2) - (ww // 2)
        py = self.root.winfo_y() + (self.root.winfo_height() // 2) - (wh // 2)
        dialog_win.geometry(f"{ww}x{wh}+{px}+{py}")

        tk.Label(dialog_win, text="Hugging Face Token (Opcional - Licencia Maestra Activa):", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold")).pack(pady=(20, 5))
        
        # Nota explicativa sutil
        tk.Label(dialog_win, text="Deje en blanco para usar el acceso maestro pre-configurado.", 
                 bg=BG_COLOR, fg="#A1D6E2", font=(FONT_FAMILY, 8, "italic")).pack(pady=(0, 10))
        
        entry = tk.Entry(dialog_win, textvariable=self.hf_token_var, width=45, font=(FONT_FAMILY, 10), bg="#f0f0f0", fg="black")
        entry.pack(pady=5, padx=20)
        entry.focus_set()

        def save_and_close():
            self.guardar_config_actual()
            dialog_win.destroy()

        btn_frame = tk.Frame(dialog_win, bg=BG_COLOR)
        btn_frame.pack(pady=15)
        create_image_button(btn_frame, "Guardar", save_and_close, self.image_manager, self.boton_path, (110, 38), font=(FONT_FAMILY, 10, "bold")).pack()

        dialog_win.deiconify()

    def centrar_ventana(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _log_message(self, message):
        if not message: return
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def check_queue(self):
        try:
            while True:
                message = self.progress_queue.get_nowait()
                if isinstance(message, tuple):
                    command, data = message
                    if command == 'log': self._log_message(data)
                    elif command == 'error':
                        self.desbloquear_botones()
                        self.progreso['value'] = 0
                        StyledDialog(self.root, _("dialog.error.title"), str(data), dialog_type="error", image_manager=self.image_manager)
                    elif command == 'done':
                        self.desbloquear_botones()
                        self.progreso['value'] = 100
                        # Pasar la carpeta actual para que el diálogo pueda abrirla
                        StyledDialog(self.root, _("dialog.done.title"), str(data), 
                                     dialog_type="success", image_manager=self.image_manager,
                                     folder_path=self.carpeta_var.get())
                elif isinstance(message, (int, float)):
                    self.progreso['value'] = message
        except queue.Empty: pass
        self.root.after(200, self.check_queue)

    def crear_widgets(self):
        title_photo = self.image_manager.load(self.title_path, size=(400, 65), add_relief_effect=True, add_shadow_effect=True)
        logo_photo = self.image_manager.load(self.logo_path, size=(115, 115), add_relief_effect=False, add_shadow_effect=False)

        frm_header = tk.Frame(self.root, bg=BG_COLOR)
        frm_header.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        frm_header.grid_columnconfigure(0, weight=1)
        frm_header.grid_columnconfigure(2, weight=1)

        header_content = tk.Frame(frm_header, bg=BG_COLOR)
        header_content.grid(row=0, column=1, pady=0) 
        
        if logo_photo:
            logo_label = tk.Label(header_content, image=logo_photo, bg=BG_COLOR)
            logo_label.image = logo_photo
            logo_label.grid(row=0, column=1, padx=(0, 20))
            logo_label.bind("<Button-1>", lambda e: AboutWindow(self.root, self.image_manager, self.icon_path))
            logo_label.config(cursor="hand2")

        if title_photo:
            title_label = tk.Label(header_content, image=title_photo, bg=BG_COLOR)
            title_label.image = title_photo
            title_label.grid(row=0, column=2)
            
        btn_config = create_image_button(frm_header, "⚙", self.mostrar_config_token, self.image_manager, self.boton_path, (45, 45), font=(FONT_FAMILY, 14, "bold"))
        btn_config.grid(row=0, column=3, sticky="e", padx=(10, 0))

        separator = tk.Frame(self.root, bg="#cccccc", height=1)
        separator.pack(fill='x', padx=40, pady=2)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Solarized.TCombobox', fieldbackground='#f0f0f0', background='#f0f0f0', foreground='black', arrowcolor='black', bordercolor='#f0f0f0')
        style.configure('Custom.Horizontal.TProgressbar', troughcolor='#f0f0f0', background='green', bordercolor='#f0f0f0')

        frm_top = tk.Frame(self.root, bg=BG_COLOR)
        frm_top.pack(fill=tk.X, pady=(0, 10), padx=20)
        frm_izq = tk.Frame(frm_top, bg=BG_COLOR)
        frm_izq.pack(fill=tk.BOTH, expand=True)
        frm_izq.grid_columnconfigure(0, weight=1)
        frm_izq.grid_columnconfigure(4, weight=1)

        tk.Label(frm_izq, text=_("label.audio_folder"), bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold")).grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.entry_carpeta = tk.Entry(frm_izq, textvariable=self.carpeta_var, width=55, font=(FONT_FAMILY, 11), bg="#f0f0f0", fg="black", state="readonly")
        self.entry_carpeta.grid(row=0, column=2, padx=5)
        self.btn_carpeta = create_image_button(frm_izq, _("button.browse"), self.seleccionar_carpeta, self.image_manager, self.boton_path, (120, 42), font=(FONT_FAMILY, 10, "bold"))
        self.btn_carpeta.grid(row=0, column=3)

        tk.Label(frm_izq, text=_("label.template_docx"), bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold")).grid(row=1, column=1, sticky="w", padx=(10, 0))
        self.entry_plantilla = tk.Entry(frm_izq, textvariable=self.plantilla_var, width=55, font=(FONT_FAMILY, 11), bg="#f0f0f0", fg="black", state="readonly")
        self.entry_plantilla.grid(row=1, column=2, padx=5)
        self.btn_plantilla = create_image_button(frm_izq, _("button.browse"), self.seleccionar_plantilla, self.image_manager, self.boton_path, (120, 42), font=(FONT_FAMILY, 10, "bold"))
        self.btn_plantilla.grid(row=1, column=3)

        tk.Label(frm_izq, text=_("label.whisper_model"), bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold")).grid(row=2, column=1, sticky="w", pady=5, padx=(10, 0))
        frm_modelo_genero = tk.Frame(frm_izq, bg=BG_COLOR)
        frm_modelo_genero.grid(row=2, column=2, columnspan=2, sticky="w", padx=5, pady=5)

        self.modelo_combo = ttk.Combobox(frm_modelo_genero, textvariable=self.modelo_var, values=["small", "medium", "large-v3"], state="readonly", width=12, font=(FONT_FAMILY, 11), style='Solarized.TCombobox')
        self.modelo_combo.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(frm_modelo_genero, text=_("label.professional"), bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        style.configure('Wild.TRadiobutton', background=BG_COLOR, foreground=TEXT_COLOR, font=(FONT_FAMILY, 10), focuscolor=BG_COLOR, focusthickness=0, borderwidth=0, relief="flat")
        style.map('Wild.TRadiobutton', background=[('active', BG_COLOR), ('pressed', BG_COLOR)], focuscolor=[('active', BG_COLOR)])
        
        self.rb_mujer = ttk.Radiobutton(frm_modelo_genero, text=_("role.psychologist_f"), variable=self.genero_profesional_var, value=_("role.psychologist_f"), style='Wild.TRadiobutton', cursor="hand2", takefocus=False)
        self.rb_mujer.pack(side=tk.LEFT, padx=(0, 10))
        self.rb_hombre = ttk.Radiobutton(frm_modelo_genero, text=_("role.psychologist_m"), variable=self.genero_profesional_var, value=_("role.psychologist_m"), style='Wild.TRadiobutton', cursor="hand2", takefocus=False)
        self.rb_hombre.pack(side=tk.LEFT)

        action_frame = tk.Frame(frm_izq, bg=BG_COLOR)
        action_frame.grid(row=3, column=1, columnspan=3, pady=5, sticky="ew")

        self.btn_transcribir = create_image_button(action_frame, _("button.transcribe"), self.iniciar_transcripcion, self.image_manager, self.boton_path, (200, 62), font=(FONT_FAMILY, 12, "bold"))
        self.btn_transcribir.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.btn_limpiar = create_image_button(action_frame, _("button.clear"), self.limpiar_campos, self.image_manager, self.boton_path, (200, 62), font=(FONT_FAMILY, 12, "bold"))
        self.btn_limpiar.pack(side=tk.LEFT, padx=5, expand=True)

        self.btn_salir = create_image_button(action_frame, _("button.exit"), self.on_closing, self.image_manager, self.boton_path, (200, 62), font=(FONT_FAMILY, 12, "bold"))
        self.btn_salir.pack(side=tk.LEFT, padx=5, expand=True)

        self.progreso = ttk.Progressbar(self.root, orient="horizontal", length=830, mode="determinate", style='Custom.Horizontal.TProgressbar')
        self.progreso.pack(padx=20, pady=5)

        self.log_text = scrolledtext.ScrolledText(self.root, state="disabled", height=22, font=("Consolas", 11), bg="#002b36", fg="#F8F8F2", insertbackground="black")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

    def limpiar_campos(self, event=None):
        if self.transcribiendo: return
        self.carpeta_var.set("")
        self.plantilla_var.set("")
        self.progreso['value'] = 0
        
        # Limpiar el Ã¡rea de logs
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state="disabled")

    def _handle_drop(self, event):
        """Maneja el evento de soltar archivos o carpetas (Drag & Drop)."""
        if self.transcribiendo: return
        
        # splitlist maneja correctamente las rutas con espacios enviadas por Windows
        files = self.root.tk.splitlist(event.data)
        if not files: return
        
        data = files[0] # Procesamos el primer elemento detectado
            
        if os.path.isdir(data):
            self.carpeta_var.set(data)
            self._log_message(f"{_('log.folder_detected')}: {data}")
        elif os.path.isfile(data):
            parent = os.path.dirname(data)
            self.carpeta_var.set(parent)
            self._log_message(f"{_('log.file_detected')}. {_('log.selecting_parent')}: {parent}")

    def _handle_template_drop(self, event):
        """Maneja el evento de soltar la plantilla DOCX (Drag & Drop)."""
        if self.transcribiendo: return
        
        files = self.root.tk.splitlist(event.data)
        if not files: return
        
        data = files[0]
        if os.path.isfile(data) and data.lower().endswith(".docx"):
            self.plantilla_var.set(data)
            self._log_message(f"{_('log.file_detected')}: {data}")
            self.guardar_config_actual()

    def bloquear_botones(self):
        self.transcribiendo = True
        for btn in [self.btn_transcribir, self.btn_carpeta, self.btn_plantilla, self.btn_limpiar]:
            btn.config(command="", cursor="")
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
        self.rb_mujer.bind("<Button-1>", lambda e: "break")
        self.rb_hombre.bind("<Button-1>", lambda e: "break")
        for entry in [self.entry_carpeta, self.entry_plantilla, self.modelo_combo]: entry.config(state="disabled")

    def desbloquear_botones(self):
        self.transcribiendo = False
        self.btn_transcribir.config(command=self.iniciar_transcripcion, cursor="hand2")
        self.btn_carpeta.config(command=self.seleccionar_carpeta, cursor="hand2")
        self.btn_plantilla.config(command=self.seleccionar_plantilla, cursor="hand2")
        self.btn_limpiar.config(command=self.limpiar_campos, cursor="hand2")
        for btn in [self.btn_transcribir, self.btn_carpeta, self.btn_plantilla, self.btn_limpiar]:
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=ACCENT_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=TEXT_COLOR))
        self.rb_mujer.unbind("<Button-1>")
        self.rb_hombre.unbind("<Button-1>")
        self.entry_carpeta.config(state="readonly")
        self.entry_plantilla.config(state="readonly")
        self.modelo_combo.config(state="readonly")

    def seleccionar_carpeta(self):
        if self.transcribiendo: return
        carpeta = filedialog.askdirectory(parent=self.root)
        if carpeta:
            self.carpeta_var.set(carpeta)
            self._log_message(f"{_('log.folder_detected')}: {carpeta}")

    def seleccionar_plantilla(self):
        if self.transcribiendo: return
        archivo = filedialog.askopenfilename(filetypes=[("Documentos Word", "*.docx")], parent=self.root)
        if archivo:
            self.plantilla_var.set(archivo)
            self._log_message(f"{_('log.file_detected')}: {archivo}")
            self.guardar_config_actual()
    def iniciar_transcripcion(self):
        if self.transcribiendo: return
        carpeta = self.carpeta_var.get()
        plantilla = self.plantilla_var.get()
        modelo = self.modelo_var.get()
        genero_profesional = self.genero_profesional_var.get()
        if not all([carpeta, os.path.isdir(carpeta)]):
            StyledDialog(self.root, _("dialog.error.title"), _("error.invalid_folder"), dialog_type="error", image_manager=self.image_manager)
            return
        self.bloquear_botones()
        self.guardar_config_actual()
        self.progreso['value'] = 0
        self._log_message(_("log.starting"))
        from worker import run_transcription_process
        self.proceso_hijo = multiprocessing.Process(target=run_transcription_process, args=(self.progress_queue, carpeta, plantilla, modelo, genero_profesional), daemon=True)
        self.proceso_hijo.start()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('mi.transcriptor.v1')
    except: pass
    root = tk.Tk()
    root.withdraw()
    app = TranscriptorGUI(root)
    root.deiconify()
    root.mainloop()
