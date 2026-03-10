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
        self.dialog.resizable(False, False)

        # Usar el nuevo sistema de recursos modular
        self.icon_path = resources.image_path("icon.ico")
        if os.path.isfile(self.icon_path):
            try:
                self.dialog.iconbitmap(self.icon_path)
            except:
                pass

        self.crear_widgets(title, message, self.ICONS.get(self.dialog_type, "ℹ️"))
        self._center_popup(400, 200)
        self.dialog.deiconify()

    def crear_widgets(self, title, message, emoji):
        frm_main = tk.Frame(self.dialog, bg=self.BG_COLOR, padx=20, pady=20)
        frm_main.pack(fill=tk.BOTH, expand=True)
        
        lbl_emoji = tk.Label(frm_main, text=emoji, font=(self.FONT_FAMILY, 28, "bold"), bg=self.BG_COLOR, fg=self.ACCENT_COLOR)
        lbl_emoji.grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="ns")
        
        lbl_title = tk.Label(frm_main, text=title, font=(self.FONT_FAMILY, 14, "bold"), bg=self.BG_COLOR, fg=self.ACCENT_COLOR, justify="left")
        lbl_title.grid(row=0, column=1, sticky="nw")

        lbl_msg = tk.Label(frm_main, text=message, font=(self.FONT_FAMILY, 11, "bold"), bg=self.BG_COLOR, fg=self.TEXT_COLOR, wraplength=280, justify="left")
        lbl_msg.grid(row=1, column=1, sticky="nw", pady=(5, 0))

        btn_frame = tk.Frame(self.dialog, bg=self.BG_COLOR)
        btn_frame.pack(pady=(0, 20))

        boton_path = resources.image_path("boton.png")

        if self.dialog_type in ["info", "error", "success", "warning"]:
            btn_aceptar = create_image_button(btn_frame, _("button.accept"), self.handle_no, self.image_manager, boton_path, (110, 40), font=(self.FONT_FAMILY, 10, "bold"))
            btn_aceptar.pack()
        elif self.dialog_type == "question":
            btn_si = create_image_button(btn_frame, _("button.yes"), self.handle_yes, self.image_manager, boton_path, (100, 40), font=(self.FONT_FAMILY, 10, "bold"))
            btn_si.pack(side=tk.LEFT, padx=10)
            btn_no = create_image_button(btn_frame, _("button.no"), self.handle_no, self.image_manager, boton_path, (100, 40), font=(self.FONT_FAMILY, 10, "bold"))
            btn_no.pack(side=tk.RIGHT, padx=10)

    def handle_yes(self):
        self.result = True
        self.dialog.destroy()

    def handle_no(self):
        self.result = False
        self.dialog.destroy()

    def show(self):
        self.parent.wait_window(self.dialog)
        return self.result

    def _center_popup(self, width, height):
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
