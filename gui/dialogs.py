import tkinter as tk
from gui.widgets import create_image_button
from core import resources
from core.i18n import _
import os

class StyledDialog:
    ICONS = {
        "error": "❌",
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "question": "❓"
    }

    def __init__(self, parent, title, message, dialog_type="info", image_manager=None):
        self.BG_COLOR = "#023047"
        self.TEXT_COLOR = "white"
        self.ACCENT_COLOR = "#fcbf49"
        self.FONT_FAMILY = "Segoe UI"
        
        self.parent = parent
        self.dialog_type = dialog_type
        self.result = False
        self.image_manager = image_manager

        self.dialog = tk.Toplevel(parent)
        self.dialog.withdraw()
        self.dialog.title(title)
        self.dialog.configure(bg=self.BG_COLOR)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Bloqueo total de redimensionamiento
        self.dialog.resizable(False, False)

        self.icon_path = resources.image_path("icon.ico")
        if os.path.isfile(self.icon_path):
            try:
                self.dialog.iconbitmap(self.icon_path)
            except:
                pass

        self.crear_widgets(title, message, self.ICONS.get(self.dialog_type, "ℹ️"))
        
        # Ajuste inteligente y centrado
        self._center_popup(420)
        self.dialog.deiconify()

    def crear_widgets(self, title, message, emoji):
        # Márgenes más compactos y profesionales
        frm_main = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=25, pady=20)
        frm_main.pack(fill=tk.BOTH, expand=True)
        
        lbl_emoji = tk.Label(frm_main, text=emoji, font=(self.FONT_FAMILY, 28), bg=self.BG_COLOR, fg=self.ACCENT_COLOR)
        lbl_emoji.pack(pady=(0, 8))
        
        lbl_title = tk.Label(frm_main, text=title, font=(self.FONT_FAMILY, 13, "bold"), bg=self.BG_COLOR, fg=self.ACCENT_COLOR, justify="center")
        lbl_title.pack(pady=(0, 10))

        lbl_msg = tk.Label(frm_main, text=message, font=(self.FONT_FAMILY, 10, "bold"), bg=self.BG_COLOR, fg=self.TEXT_COLOR, wraplength=360, justify="center")
        lbl_msg.pack(fill=tk.X, expand=True, pady=(0, 15))

        btn_frame = tk.Frame(self.dialog, bg=self.BG_COLOR)
        btn_frame.pack(side=tk.BOTTOM, pady=(0, 20))

        boton_path = resources.image_path("boton.png")

        if self.dialog_type in ["info", "error", "success", "warning"]:
            btn_aceptar = create_image_button(btn_frame, _("button.accept"), self.handle_no, self.image_manager, boton_path, (120, 38), font=(self.FONT_FAMILY, 9, "bold"))
            btn_aceptar.pack()
        elif self.dialog_type == "question":
            btn_si = create_image_button(btn_frame, _("button.yes"), self.handle_yes, self.image_manager, boton_path, (100, 38), font=(self.FONT_FAMILY, 9, "bold"))
            btn_si.pack(side=tk.LEFT, padx=8)
            btn_no = create_image_button(btn_frame, _("button.no"), self.handle_no, self.image_manager, boton_path, (100, 38), font=(self.FONT_FAMILY, 9, "bold"))
            btn_no.pack(side=tk.RIGHT, padx=8)

    def handle_yes(self):
        self.result = True
        self.dialog.destroy()

    def handle_no(self):
        self.result = False
        self.dialog.destroy()

    def show(self):
        self.parent.wait_window(self.dialog)
        return self.result

    def _center_popup(self, width):
        self.dialog.update_idletasks()
        # Obtener la altura real que Tkinter ha calculado para el contenido
        height = self.dialog.winfo_reqheight()
        
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        
        # Limitar altura máxima para que no se salga de la pantalla en errores críticos
        screen_h = self.dialog.winfo_screenheight()
        if height > screen_h * 0.8:
            height = int(screen_h * 0.8)
            
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
