import tkinter as tk

def create_image_button(parent, text, command, image_manager, filepath, image_size=(150, 45), font=("Comic Sans MS", 11, "bold"), bg_color="#023047", text_color="white", accent_color="#fcbf49"):
    """
    Crea un botón personalizado siguiendo la técnica exacta de Wordy:
    Solo sombra generada en la imagen, sin relieve de sistema para evitar el borde rectangular.
    """
    # Cargar imagen con la técnica de Wordy (Sombra, pero SIN relieve de sistema)
    photo = image_manager.load(
        filepath, 
        size=image_size, 
        add_shadow_effect=True,
        add_relief_effect=False, # Esto evitaba el reborde molesto
        shadow_offset=(2, 2),
        shadow_color=(0, 0, 0, 120),
        blur_radius=3,
        border=4
    )

    # Crear el botón con los parámetros de Wordy
    button = tk.Button(
        parent,
        text=text,
        image=photo,
        compound="center",
        command=command,
        relief="flat",
        bg=bg_color,
        fg=text_color,
        activebackground=bg_color,
        activeforeground=text_color,
        font=font,
        borderwidth=0,
        highlightthickness=0,
        padx=0,
        pady=0,
        takefocus=0,
        cursor="hand2"
    )

    if photo:
        button.photo = photo

    # Efecto Hover premium
    button.bind("<Enter>", lambda e: button.config(fg=accent_color))
    button.bind("<Leave>", lambda e: button.config(fg=text_color))
    
    return button
