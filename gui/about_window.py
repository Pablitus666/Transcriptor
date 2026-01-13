import os
import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk, ImageFilter, ImageOps

# ===================== PALETA EXACTA DEL SCRIPT MUESTRA =====================
BG_COLOR = "#023047"
TEXT_COLOR = "white"
ACCENT_COLOR = "#fcbf49"
FONT_FAMILY = "Comic Sans MS"

class AboutWindow:
    def __init__(self, parent, icon_path=None):
        self.parent = parent
        self.icon_path = icon_path
        self.info_window = None
        self.boton_photo = None
        self.image_cache = {}
        
        self.robot_path = os.path.join(os.path.dirname(__file__), "..", "images", "robot.png")
        boton_path = os.path.join(os.path.dirname(__file__), "..", "images", "boton.png")
        
        if os.path.exists(boton_path):
            img = ImageTk.PhotoImage(file=boton_path)
            # Nota: PhotoImage no tiene 'width()' o 'height()', usamos el objeto Image si es necesario.
            # Aquí, la carga directa es suficiente para el botón, pero el logo/robot necesita PIL.
            # La lógica de submuestreo del botón original se mantiene por coherencia.
            temp_img = tk.PhotoImage(file=boton_path)
            self.boton_photo = temp_img.subsample(
                max(1, temp_img.width() // 125),
                max(1, temp_img.height() // 50)
            )

    def _create_robot_image(self, window):
        """
        Procesa la imagen del robot para HiDPI y efectos, y la guarda en caché.
        Solo se ejecuta una vez.
        """
        if 'robot' in self.image_cache:
            return

        try:
            tk_scaling = window.tk.call('tk', 'scaling')
            render_scale = 2.5
            
            base_robot = Image.open(self.robot_path).convert("RGBA")

            display_width = 100 
            final_width = int(display_width * tk_scaling)
            
            hd_render_width = int(final_width * render_scale)
            ratio = hd_render_width / base_robot.width
            hd_render_height = int(base_robot.height * ratio)
            
            hd_robot = base_robot.resize((hd_render_width, hd_render_height), Image.Resampling.LANCZOS)

            # --- Efecto de Relieve (Emboss) ---
            offset = int(2 * tk_scaling)
            if offset < 1: offset = 1

            # Crear una base para la composición
            composite_image = Image.new('RGBA', (hd_robot.width + offset, hd_robot.height + offset), (0, 0, 0, 0))
            
            # Obtener el canal alfa como máscara
            alpha_mask = hd_robot.split()[-1]
            
            # Crear capa de sombra (versión oscura de la imagen) y pegarla desplazada
            shadow_layer = ImageOps.colorize(alpha_mask, black=(0,0,0,0), white=(0,0,0,70)) # Negro semitransparente
            composite_image.paste(shadow_layer, (offset, offset), alpha_mask)
            
            # Crear capa de luz (versión clara de la imagen) y pegarla desplazada
            highlight_layer = ImageOps.colorize(alpha_mask, black=(0,0,0,0), white=(255,255,255,70)) # Blanco semitransparente
            composite_image.paste(highlight_layer, (0, 0), alpha_mask)

            # Pegar la imagen original encima, centrada entre la luz y la sombra
            composite_image.paste(hd_robot, (offset // 2, offset // 2), hd_robot)

            final_image = composite_image.resize((final_width, int(composite_image.height * final_width / composite_image.width)), Image.Resampling.LANCZOS)

            self.image_cache['robot'] = ImageTk.PhotoImage(final_image)

        except Exception as e:
            print(f"❌ Error procesando la imagen del robot: {e}")
            try:
                img = Image.open(self.robot_path)
                self.image_cache['robot'] = ImageTk.PhotoImage(img)
            except:
                pass


    def show(self):
        if self.info_window and self.info_window.winfo_exists():
            self.info_window.lift()
            return

        self.info_window = Toplevel(self.parent)
        self.info_window.withdraw()  # ⛔ evita parpadeo
        self.info_window.title("Información")
        self.info_window.configure(bg=BG_COLOR)
        self.info_window.resizable(False, False)
        self.info_window.transient(self.parent)

        if self.icon_path and os.path.exists(self.icon_path):
            self.info_window.iconbitmap(self.icon_path)

        self.center_popup(self.info_window, 370, 230)
        self.info_window.deiconify()  # ✅ mostrar ya centrada

        # Procesar la imagen del robot (solo se ejecuta la primera vez)
        self._create_robot_image(self.info_window)

        frame = tk.Frame(self.info_window, bg=BG_COLOR)
        frame.pack(padx=10, pady=10)

        # Cargar y mostrar la imagen del robot desde la caché
        if 'robot' in self.image_cache:
            img_label = tk.Label(frame, image=self.image_cache['robot'], bg=BG_COLOR)
            img_label.grid(row=0, column=0, rowspan=3, padx=10, pady=5)
        else:
            print("❌ No se pudo cargar la imagen del robot desde la caché.")

        # Texto EXACTO
        message = tk.Label(
            frame,
            text="Desarrollado por: \nPablo Téllez A.\n\nTarija - 2026.",
            justify="center",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, 14, "bold"),
            anchor="center"
        )
        message.grid(row=0, column=1, padx=(2, 8), pady=10, sticky="n")

        # Botón Cerrar EXACTO (texto + imagen + hover)
        close_btn = tk.Button(
            frame,
            text="Cerrar",
            image=self.boton_photo,
            compound="center",
            font=(FONT_FAMILY, 12, "bold"),
            command=self.info_window.destroy,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            bd=0,
            cursor="hand2",
            highlightbackground=ACCENT_COLOR,
            highlightthickness=2,
            activebackground=BG_COLOR,
            activeforeground=ACCENT_COLOR
        )
        close_btn.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="n")

        # Hover EXACTO
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=ACCENT_COLOR))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=TEXT_COLOR))

    def center_popup(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
