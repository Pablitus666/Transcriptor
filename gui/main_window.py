import os
import sys
import multiprocessing
import queue
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageOps

# El worker se importa de forma diferida para acelerar el arranque
from gui.about_window import AboutWindow

# ===================== STYLED DIALOG =====================
class StyledDialog:
    ICONS = {
        "error": "❌",
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "question": "❓"
    }

    def __init__(self, parent, title, message, dialog_type="info", icon_path=None):
        self.BG_COLOR = "#023047"
        self.TEXT_COLOR = "white"
        self.ACCENT_COLOR = "#fcbf49"
        self.FONT_FAMILY = "Comic Sans MS"
        
        self.parent = parent
        self.dialog_type = dialog_type
        self.result = False  # El resultado por defecto es False (ej. 'No')

        self.dialog = tk.Toplevel(parent)
        self.dialog.withdraw()
        self.dialog.title(title)
        self.dialog.configure(bg=self.BG_COLOR)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        if icon_path and os.path.isfile(icon_path):
            try:
                self.dialog.iconbitmap(icon_path)
            except tk.TclError:
                print(f"No se pudo cargar el icono: {icon_path}")

        # Cargar imagen de botón pequeña para 'Sí'/'No'
        self.boton_photo_small = None
        boton_path = os.path.join(os.path.dirname(__file__), "..", "images", "boton.png")
        if os.path.exists(boton_path):
            img = Image.open(boton_path)
            small_img = img.resize((90, 35), Image.Resampling.LANCZOS)
            self.boton_photo_small = ImageTk.PhotoImage(small_img)

        self.crear_widgets(title, message, self.ICONS.get(self.dialog_type, "ℹ️"))
        self.center_popup(400, 200)
        self.dialog.deiconify()

    def crear_widgets(self, title, message, emoji):
        # Frame principal para el contenido (emoji y texto)
        frm_main = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        frm_main.pack(fill=tk.BOTH, expand=True)
        frm_main.grid_rowconfigure(1, weight=1)
        frm_main.grid_columnconfigure(1, weight=1)

        lbl_emoji = tk.Label(frm_main, text=emoji, font=(self.FONT_FAMILY, 28, "bold"), bg=self.BG_COLOR, fg=self.ACCENT_COLOR)
        lbl_emoji.grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="ns")
        
        lbl_title = tk.Label(frm_main, text=title, font=(self.FONT_FAMILY, 14, "bold"), bg=self.BG_COLOR, fg=self.ACCENT_COLOR, justify="left")
        lbl_title.grid(row=0, column=1, sticky="nw")

        lbl_msg = tk.Label(frm_main, text=message, font=(self.FONT_FAMILY, 11, "bold"), bg=self.BG_COLOR, fg=self.TEXT_COLOR, wraplength=280, justify="left")
        lbl_msg.grid(row=1, column=1, sticky="nw", pady=(5, 0))

        # Frame separado para los botones, debajo del contenido principal
        btn_frame = tk.Frame(self.dialog, bg=self.BG_COLOR)
        btn_frame.pack(pady=(0, 20))

        if self.dialog_type in ["info", "error", "success", "warning"]:
            btn_aceptar = self._create_styled_button(btn_frame, "Aceptar", self.handle_no)
            btn_aceptar.pack()
        elif self.dialog_type == "question":
            btn_si = self._create_styled_button(btn_frame, "Sí", self.handle_yes)
            btn_si.pack(side=tk.LEFT, padx=10)
            btn_no = self._create_styled_button(btn_frame, "No", self.handle_no)
            btn_no.pack(side=tk.RIGHT, padx=10)

    def _create_styled_button(self, parent, text, command):
        button = tk.Button(parent, text=text, image=self.boton_photo_small, compound="center",
                                font=(self.FONT_FAMILY, 11, "bold"), command=command,
                                bg=self.BG_COLOR, fg=self.TEXT_COLOR, bd=0, cursor="hand2",
                                highlightbackground=self.ACCENT_COLOR, highlightthickness=2,
                                activebackground=self.BG_COLOR, activeforeground=self.ACCENT_COLOR)
        button.bind("<Enter>", lambda e: button.config(fg=self.ACCENT_COLOR))
        button.bind("<Leave>", lambda e: button.config(fg=self.TEXT_COLOR))
        return button

    def handle_yes(self):
        self.result = True
        self.dialog.destroy()

    def handle_no(self):
        self.result = False
        self.dialog.destroy()

    def show(self):
        self.parent.wait_window(self.dialog)
        return self.result

    def center_popup(self, width, height):
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

# ===================== PALETA DE COLORES VENTANA PRINCIPAL =====================
BG_COLOR = "#023047"
ACCENT_COLOR = "#fcbf49"
TEXT_COLOR = "white"
FONT_FAMILY = "Comic Sans MS"

# ===================== VENTANA PRINCIPAL =====================
class TranscriptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transcriptor")
        self.root.configure(bg=BG_COLOR)

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.carpeta_var = tk.StringVar()
        self.plantilla_var = tk.StringVar()
        self.modelo_var = tk.StringVar(value="large-v3")
        self.logo_cache = {}
        self.title_cache = {}
        self.transcribiendo = False
        
        ancho, alto = 870, 670
        self.root.resizable(False, False)
        self.centrar_ventana(ancho, alto)

    def on_closing(self):
        """
        Maneja el evento de cierre de la ventana para una salida segura.
        """
        if self.transcribiendo:
            dialog = StyledDialog(self.root, "Salir", 
                                  "Hay un proceso de transcripción en curso.\n¿Estás seguro de que quieres salir?",
                                  dialog_type="question", icon_path=self.icon_path)
            if dialog.show():
                if self.proceso_hijo and self.proceso_hijo.is_alive():
                    self.proceso_hijo.terminate()
                self.root.destroy()
        else:
            self.root.destroy()

    def _create_enhanced_image(self, image_path, display_width, cache_dict, cache_key, emboss=False):
        """
        Procesa una imagen para añadirle efectos (HiDPI, sombra, relieve) y la guarda en caché.
        """
        try:
            if not os.path.exists(image_path):
                print(f"❌ No se encontró la imagen: {image_path}")
                return

            tk_scaling = self.root.tk.call('tk', 'scaling')
            render_scale = 2.5 

            base_image = Image.open(image_path).convert("RGBA")

            final_width = int(display_width * tk_scaling)
            
            hd_render_width = int(final_width * render_scale)
            ratio = hd_render_width / base_image.width
            hd_render_height = int(base_image.height * ratio)
            
            hd_image = base_image.resize((hd_render_width, hd_render_height), Image.Resampling.LANCZOS)

            if emboss:
                # --- Efecto de Relieve (Emboss) ---
                offset = int(2 * tk_scaling)
                if offset < 1: offset = 1

                # Crear una base para la composición
                composite_image = Image.new('RGBA', (hd_image.width + offset, hd_image.height + offset), (0, 0, 0, 0))
                
                # Obtener el canal alfa como máscara
                alpha_mask = hd_image.split()[-1]
                
                # Crear capa de sombra (versión oscura de la imagen) y pegarla desplazada
                shadow_layer = ImageOps.colorize(alpha_mask, black=(0,0,0,0), white=(0,0,0,70)) # Negro semitransparente
                composite_image.paste(shadow_layer, (offset, offset), alpha_mask)
                
                # Crear capa de luz (versión clara de la imagen) y pegarla desplazada
                highlight_layer = ImageOps.colorize(alpha_mask, black=(0,0,0,0), white=(255,255,255,70)) # Blanco semitransparente
                composite_image.paste(highlight_layer, (0, 0), alpha_mask)

                # Pegar la imagen original encima, centrada entre la luz y la sombra
                composite_image.paste(hd_image, (offset // 2, offset // 2), hd_image)
            
            else:
                # --- Efecto de Sombra Suave (Drop Shadow) Original ---
                shadow_offset = (int(4 * tk_scaling), int(4 * tk_scaling))
                shadow_blur_radius = 5
                
                shadow_silhouette = Image.new('RGBA', hd_image.size, (0, 0, 0, 0))
                black_image = Image.new('RGBA', hd_image.size, (0, 0, 0, 200))
                shadow_silhouette.paste(black_image, (0,0), hd_image)
                
                blurred_shadow = shadow_silhouette.filter(ImageFilter.GaussianBlur(shadow_blur_radius))

                composite_width = hd_image.width + shadow_offset[0] + shadow_blur_radius
                composite_height = hd_image.height + shadow_offset[1] + shadow_blur_radius
                composite_image = Image.new('RGBA', (composite_width, composite_height), (0, 0, 0, 0))
                
                composite_image.paste(blurred_shadow, shadow_offset, blurred_shadow)
                composite_image.paste(hd_image, (0, 0), hd_image)

            final_height = int(composite_image.height * final_width / composite_image.width)
            final_image = composite_image.resize((final_width, final_height), Image.Resampling.LANCZOS)

            cache_dict[cache_key] = ImageTk.PhotoImage(final_image)

        except Exception as e:
            print(f"❌ Error procesando imagen '{os.path.basename(image_path)}': {e}")
            try:
                img = Image.open(image_path)
                ratio = display_width / img.width
                fallback_height = int(img.height * ratio)
                img = img.resize((display_width, fallback_height), Image.Resampling.LANCZOS)
                cache_dict[cache_key] = ImageTk.PhotoImage(img)
            except Exception as e2:
                print(f"❌ Fallback de imagen también falló para '{os.path.basename(image_path)}': {e2}")
                pass


    def centrar_ventana(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        
        # Usar una cola de multiprocessing
        self.progress_queue = multiprocessing.Queue()
        self.proceso_hijo = None

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.title_path = os.path.join(self.BASE_DIR, "..", "images", "titulo.png")
        self.logo_path = os.path.join(self.BASE_DIR, "..", "images", "logo.png")
        self.icon_path = os.path.join(self.BASE_DIR, "..", "images", "icon.ico")
        
        self._load_button_images()

        try:
            self.root.iconbitmap(self.icon_path)
        except Exception as e:
            print("❌ Error cargando icono:", e)

        self.crear_widgets()
        self.about_window = AboutWindow(self.root, icon_path=self.icon_path)
        self.root.bind("<Delete>", self.limpiar_campos)
        
        # Asignar el protocolo de cierre seguro y iniciar el bucle de sondeo para la cola
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.check_queue()

    def _load_button_images(self):
        self.boton_photo_small = None
        self.boton_photo_medium = None
        self.boton_photo_large = None
        boton_path = os.path.join(self.BASE_DIR, "..", "images", "boton.png")
        if os.path.exists(boton_path):
            try:
                img = Image.open(boton_path)
                small_img = img.resize((120, 45), Image.Resampling.LANCZOS)
                self.boton_photo_small = ImageTk.PhotoImage(small_img)
                
                medium_img = img.resize((200, 65), Image.Resampling.LANCZOS) # Slightly larger for emphasis
                self.boton_photo_medium = ImageTk.PhotoImage(medium_img)

                large_img = img.resize((220, 70), Image.Resampling.LANCZOS)
                self.boton_photo_large = ImageTk.PhotoImage(large_img)
            except Exception as e:
                print(f"❌ Error cargando imagen de botón: {e}")

    def _create_image_button(self, parent, text, command, image, font_size=11):
        button = tk.Button(parent, text=text, image=image, compound="center",
                           font=(FONT_FAMILY, font_size, "bold"), command=command,
                           bg=BG_COLOR, fg=TEXT_COLOR, bd=0, cursor="hand2",
                           highlightbackground=ACCENT_COLOR, highlightthickness=2,
                           activebackground=BG_COLOR, activeforeground=ACCENT_COLOR)
        button.bind("<Enter>", lambda e: button.config(fg=ACCENT_COLOR))
        button.bind("<Leave>", lambda e: button.config(fg=TEXT_COLOR))
        return button

    def _log_message(self, message):
        if not message: return
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def check_queue(self):
        """Revisa la cola de mensajes del proceso hijo de forma periódica."""
        try:
            while True:
                message = self.progress_queue.get_nowait()
                
                if isinstance(message, tuple):
                    command, data = message
                    if command == 'log':
                        self._log_message(data)
                    elif command == 'error':
                        self.desbloquear_botones()
                        self.progreso['value'] = 0
                        StyledDialog(self.root, "Error en Transcripción", str(data), dialog_type="error", icon_path=self.icon_path)
                    elif command == 'done':
                        self.desbloquear_botones()
                        self.progreso['value'] = 100
                        StyledDialog(self.root, "Proceso Completado", str(data), dialog_type="success", icon_path=self.icon_path)
                        self.root.after(1500, lambda: self.progreso.config(value=0))
                
                elif isinstance(message, (int, float)):
                    self.progreso['value'] = message

        except queue.Empty:
            pass # La cola está vacía, no hacer nada

        # Volver a comprobar en 200ms
        self.root.after(200, self.check_queue)

    def crear_widgets(self):
        # Tamaños de imagen ajustados para un header más equilibrado
        self._create_enhanced_image(self.title_path, 280, self.title_cache, 'normal', emboss=True) # Efecto relieve
        self._create_enhanced_image(self.logo_path, 90, self.logo_cache, 'normal', emboss=True) # Efecto relieve

        # --- Frame para el header (logo y título) ---
        frm_header = tk.Frame(self.root, bg=BG_COLOR)
        frm_header.pack(fill=tk.X, pady=(8, 0), padx=20) # Reduced pady from (10, 0) to (8, 0)
        # Centrar el contenido del header
        frm_header.grid_columnconfigure(0, weight=1)
        frm_header.grid_columnconfigure(2, weight=1)

        # Contenedor para alinear logo y título
        header_content = tk.Frame(frm_header, bg=BG_COLOR)
        header_content.grid(row=0, column=1) # Colocar en la celda del medio
        
        # Centrar el contenido (logo y título) horizontalmente dentro de header_content
        header_content.grid_columnconfigure(0, weight=1) # Columna espaciadora izquierda
        header_content.grid_columnconfigure(3, weight=1) # Columna espaciadora derecha

        # Logo Izquierdo
        if 'normal' in self.logo_cache:
            logo_label_left = tk.Label(header_content, image=self.logo_cache['normal'], bg=BG_COLOR)
            logo_label_left.grid(row=0, column=1, padx=(0, 20)) # Colocar en la columna 1, con espaciado derecho
            logo_label_left.bind("<Button-1>", lambda e: self.about_window.show())
            logo_label_left.config(cursor="hand2")
        else:
            print("❌ No se pudo cargar el logo izquierdo desde la caché.")

        # Título
        if 'normal' in self.title_cache:
            title_label = tk.Label(header_content, image=self.title_cache['normal'], bg=BG_COLOR)
            title_label.grid(row=0, column=2) # Colocar en la columna 2, sin pady
        else:
            print("❌ No se pudo cargar el título desde la caché.")

        # --- Separador ---
        separator = tk.Frame(self.root, bg="#cccccc", height=1)
        separator.pack(fill='x', padx=40, pady=8) # Reduced pady from 10 to 8

        # --- Estilos para widgets TTK ---
        style = ttk.Style()
        style.theme_use('clam')

        # Estilo para el Combobox
        style.configure('Solarized.TCombobox', 
                        fieldbackground='#f0f0f0',
                        background='#f0f0f0',
                        foreground='black',
                        arrowcolor='black',
                        selectbackground='#CCCCCC',
                        selectforeground='black',
                        bordercolor='#f0f0f0')
        style.map('Solarized.TCombobox',
                  fieldbackground=[('readonly', '#f0f0f0')],
                  foreground=[('readonly', 'black')],
                  background=[('readonly', '#f0f0f0')])

        # Estilo para la Barra de Progreso (desde copia de seguridad)
        style.configure('Custom.Horizontal.TProgressbar',
                        troughcolor='#f0f0f0',      # Fondo de la barra (el "riel")
                        background='green',         # Color de la barra de progreso en sí
                        bordercolor='#f0f0f0')

        # --- Creación de Widgets ---
        frm_top = tk.Frame(self.root, bg=BG_COLOR) # No padx en el constructor
        frm_top.pack(fill=tk.X, pady=(0, 10), padx=20) # Changed pady from (0, 20) to (0, 10)

        frm_izq = tk.Frame(frm_top, bg=BG_COLOR)
        frm_izq.pack(fill=tk.BOTH, expand=True)

        # Centrar el contenido de frm_izq
        frm_izq.grid_columnconfigure(0, weight=1) # Columna espaciadora izquierda
        frm_izq.grid_columnconfigure(4, weight=1) # Columna espaciadora derecha

        tk.Label(frm_izq, text="Carpeta de audios:", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold")).grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.entry_carpeta = tk.Entry(frm_izq, textvariable=self.carpeta_var, width=55, font=(FONT_FAMILY, 11), bg="#f0f0f0", fg="black", insertbackground="black", state="readonly")
        self.entry_carpeta.grid(row=0, column=2, padx=5)
        self.btn_carpeta = self._create_image_button(frm_izq, "Examinar", self.seleccionar_carpeta, self.boton_photo_small, 10)
        self.btn_carpeta.grid(row=0, column=3)

        tk.Label(frm_izq, text="Plantilla DOCX:", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11, "bold")).grid(row=1, column=1, sticky="w", padx=(10, 0))
        self.entry_plantilla = tk.Entry(frm_izq, textvariable=self.plantilla_var, width=55, font=(FONT_FAMILY, 11), bg="#f0f0f0", fg="black", insertbackground="black", state="readonly")
        self.entry_plantilla.grid(row=1, column=2, padx=5)
        self.btn_plantilla = self._create_image_button(frm_izq, "Examinar", self.seleccionar_plantilla, self.boton_photo_small, 10)
        self.btn_plantilla.grid(row=1, column=3)

        tk.Label(frm_izq, text="Modelo Whisper:", bg=BG_COLOR, fg=TEXT_COLOR,
                 font=(FONT_FAMILY, 11, "bold")).grid(row=2, column=1, sticky="w", pady=5, padx=(10, 0))
        self.modelo_combo = ttk.Combobox(frm_izq, textvariable=self.modelo_var,
                                    values=["small", "medium", "large-v3"], state="readonly", width=30,
                                    font=(FONT_FAMILY, 11), style='Solarized.TCombobox')
        self.modelo_combo.grid(row=2, column=2, padx=5, sticky="w", pady=5)

        action_frame = tk.Frame(frm_izq, bg=BG_COLOR)
        action_frame.grid(row=3, column=1, columnspan=3, pady=15, sticky="ew") # Ajustar column y columnspan

        self.btn_transcribir = self._create_image_button(action_frame, "Transcribir", self.iniciar_transcripcion, self.boton_photo_medium, 12)
        self.btn_transcribir.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.btn_limpiar = self._create_image_button(action_frame, "Limpiar", self.limpiar_campos, self.boton_photo_medium, 12)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5, expand=True)

        self.btn_salir = self._create_image_button(action_frame, "Salir", self.on_closing, self.boton_photo_medium, 12)
        self.btn_salir.pack(side=tk.LEFT, padx=5, expand=True)

        self.progreso = ttk.Progressbar(self.root, orient="horizontal", length=830, mode="determinate", style='Custom.Horizontal.TProgressbar')
        self.progreso.pack(padx=20, pady=5)

        self.log_text = scrolledtext.ScrolledText(self.root, state="disabled", height=22, font=("Consolas", 11), bg="#002b36", fg="#F8F8F2", insertbackground="black")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20)) # Changed pady from 20 to (10, 20)

    def limpiar_campos(self, event=None):
        if self.transcribiendo: return
        self.carpeta_var.set("")
        self.plantilla_var.set("")

    def bloquear_botones(self):
        self.transcribiendo = True
        # Bloquear botones de forma visualmente agradable (sin 'state="disabled"')
        # El botón "Salir" no se bloquea intencionadamente
        for btn in [self.btn_transcribir, self.btn_carpeta, self.btn_plantilla, self.btn_limpiar]: # Removed self.btn_salir
            # Guardar el comando original si no se ha guardado ya
            if not hasattr(btn, 'original_command'):
                btn.original_command = btn.cget('command')
            
            # Desactivar funcionalidad y apariencia
            btn.config(command="", cursor="")
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
            # Cambiar el color del texto para dar una pista visual de inactividad
            btn.config(fg='#999999')

        for entry in [self.entry_carpeta, self.entry_plantilla, self.modelo_combo]:
            entry.config(state="disabled")

    def desbloquear_botones(self):
        self.transcribiendo = False
        # Reactivar botones a su estado original
        # El botón "Salir" no se bloquea, por lo que no necesita desbloquearse aquí
        for btn in [self.btn_transcribir, self.btn_carpeta, self.btn_plantilla, self.btn_limpiar]: # Removed self.btn_salir
            if hasattr(btn, 'original_command'):
                btn.config(command=btn.original_command, cursor="hand2", fg=TEXT_COLOR)
            
            # Re-vincular eventos de hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=ACCENT_COLOR))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=TEXT_COLOR))

        # Restaurar estado de los campos de entrada
        self.entry_carpeta.config(state="readonly")
        self.entry_plantilla.config(state="readonly")
        self.modelo_combo.config(state="readonly")

    def seleccionar_carpeta(self):
        if self.transcribiendo: return
        carpeta = filedialog.askdirectory(parent=self.root)
        if carpeta: self.carpeta_var.set(carpeta)

    def seleccionar_plantilla(self):
        if self.transcribiendo: return
        archivo = filedialog.askopenfilename(filetypes=[("Documentos Word", "*.docx")], parent=self.root)
        if archivo: self.plantilla_var.set(archivo)

    def iniciar_transcripcion(self):
        if self.transcribiendo:
            StyledDialog(self.root, "Información", "La transcripción ya está en ejecución.", dialog_type="info", icon_path=self.icon_path)
            return

        carpeta = self.carpeta_var.get()
        plantilla = self.plantilla_var.get()
        modelo = self.modelo_var.get()

        if not all([carpeta, os.path.isdir(carpeta)]):
            StyledDialog(self.root, "Error", "Selecciona una carpeta válida de audios", dialog_type="error", icon_path=self.icon_path)
            return
        
        # Si se proporciona una plantilla, verificar que sea un archivo válido
        if plantilla and not os.path.isfile(plantilla):
            StyledDialog(self.root, "Error", "El archivo de plantilla DOCX seleccionado no es válido.", dialog_type="error", icon_path=self.icon_path)
            return

        self.bloquear_botones()
        self.progreso['value'] = 0
        self._log_message("🚀 Iniciando proceso de transcripción...")

        # Importación diferida para no ralentizar el arranque de la GUI
        from worker import run_transcription_process

        # Lanzar el worker en un proceso separado
        self.proceso_hijo = multiprocessing.Process(
            target=run_transcription_process,
            args=(self.progress_queue, carpeta, plantilla, modelo),
            daemon=True
        )
        self.proceso_hijo.start()

# ===================== EJECUCIÓN =====================
if __name__ == "__main__":
    # Necesario para que multiprocessing funcione correctamente en Windows y macOS
    multiprocessing.freeze_support()
    
    root = tk.Tk()
    root.withdraw()
    app = TranscriptorGUI(root)
    root.deiconify()
    root.mainloop()
