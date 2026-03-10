import os
import tkinter as tk
from tkinter import Toplevel
from gui.widgets import create_image_button
from core import resources

# ===================== PALETA EXACTA DEL SCRIPT MUESTRA =====================
BG_COLOR = "#023047"
TEXT_COLOR = "white"
ACCENT_COLOR = "#fcbf49"
FONT_FAMILY = "Segoe UI" # Cambiado a Segoe UI para replicar Stegano exactamente

class AboutWindow(Toplevel):
    """ Réplica exacta de la ventana About de Stegano. """
    def __init__(self, parent, image_manager, icon_path=None):
        super().__init__(parent)
        self.image_manager = image_manager
        self.icon_path = icon_path
        
        # Ocultar inmediatamente para evitar flash visual
        self.withdraw()
        
        self.title("Información")
        self.geometry("370x230") 
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        if self.icon_path and os.path.exists(self.icon_path):
            try:
                self.iconbitmap(self.icon_path)
            except:
                pass
            
        self._create_widgets()
        self._center_window(370, 230)
        self.deiconify()

    def _create_widgets(self):
        # Réplica exacta de la estructura de Stegano
        frame_info = tk.Frame(self, bg=BG_COLOR)
        frame_info.pack(pady=10, padx=10, fill="both", expand=True)

        frame_info.grid_columnconfigure(0, weight=1)
        frame_info.grid_columnconfigure(1, weight=1)
        frame_info.grid_rowconfigure(0, weight=1)
        frame_info.grid_rowconfigure(1, weight=1)
        frame_info.grid_rowconfigure(2, weight=1)

        # Robot (160x160) - Tamaño exacto de Stegano, usando recursos modulares
        robot_path = resources.image_path("robot.png")
        robot_photo = self.image_manager.load(
            robot_path, 
            size=(160, 160), 
            add_shadow_effect=False, 
            add_relief_effect=False
        )
        
        if robot_photo:
            img_label = tk.Label(frame_info, image=robot_photo, bg=BG_COLOR)
            img_label.image = robot_photo
            img_label.grid(row=0, column=0, padx=(5, 10), pady=0, rowspan=3, sticky="nsew")

        # Mensaje: Réplica de Stegano (Segoe UI 14, wraplength 160)
        message = tk.Label(
            frame_info,
            text="Desarrollado por: \nPablo Téllez A.\n\nTarija - 2026.",
            justify="center",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=(FONT_FAMILY, 14, "bold"),
            wraplength=160
        )
        message.grid(row=0, column=1, rowspan=2, sticky="s", pady=(0, 10), padx=(0, 20))

        # Botón Cerrar: Estructura de Stegano con contenedor rígido
        boton_path = resources.image_path("boton.png")
        btn_normal = self.image_manager.load(
            boton_path, size=(125, 45), add_shadow_effect=True,
            add_relief_effect=False,
            shadow_offset=(2, 2), blur_radius=3, border=5
        )

        btn_holder = tk.Frame(frame_info, bg=BG_COLOR, width=135, height=55)
        btn_holder.pack_propagate(False)
        btn_holder.grid(row=2, column=1, sticky="n", pady=(10, 0))

        close_btn = tk.Button(
            btn_holder, 
            text="Cerrar", 
            image=btn_normal, 
            compound="center",
            font=(FONT_FAMILY, 12, "bold"), 
            command=self.destroy,
            relief="flat",
            bg=BG_COLOR, 
            fg=TEXT_COLOR, 
            bd=0, 
            padx=0,
            pady=0,
            cursor="hand2",
            highlightthickness=0,
            highlightbackground=BG_COLOR,
            activebackground=BG_COLOR, 
            activeforeground=ACCENT_COLOR,
            anchor="center",
            justify="center",
            takefocus=False
        )
        close_btn.place(relx=0.5, rely=0.5, anchor="center")
        
        def on_press(e):
            close_btn.place_configure(rely=0.54)
        def on_release(e):
            close_btn.place_configure(rely=0.5)

        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=ACCENT_COLOR))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg="white"))
        close_btn.bind("<Button-1>", on_press)
        close_btn.bind("<ButtonRelease-1>", on_release)

    def _center_window(self, width, height):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
