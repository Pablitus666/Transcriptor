import os

# ================= RUTAS =================
CARPETA = r"C:\Users\GAMT\Desktop\Transcriptor"
PLANTILLA_DOCX = os.path.join(CARPETA, "ENTREVISTA INFORMATIVA.docx")

# ================= MODELO =================
MODELO = "large-v3"
IDIOMA = "es"

# ================= HUGGINGFACE =================
HF_TOKEN = os.getenv("HF_TOKEN")

# ================= DETECCIÓN PSICÓLOGA =================
CLAVES_PSICO = [
    "soy psicólogo",
    "soy psicóloga",
    "psicologo del slim",
    "psicóloga del slim",
    "psicologo de la defensoría",
    "psicóloga de la defensoría",
    "psicologo de defensoría",
    "psicóloga de defensoría"
]

# ================= ENTORNO =================
os.environ["PYANNOTE_AUDIO_PROGRESSBAR"] = "false"
