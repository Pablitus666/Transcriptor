import os
import sys
import subprocess
import shutil

# --- CONFIGURACIÓN ---
WHISPER_PYTHON = os.path.join("whisper_env", "Scripts", "python.exe")
PACKAGES_TO_BLIND = ["core", "utils", "exporters", "gui", "config"]
ICON_PATH = os.path.join("assets", "images", "icon.ico")
# ----------------------

def run_cmd(cmd, description):
    print(f"\n🚀 {description}...")
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Éxito: {description}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en: {description}")
        sys.exit(1)

def main():
    if not os.path.exists(WHISPER_PYTHON):
        print(f"❌ Error: No se encontró el entorno virtual en {WHISPER_PYTHON}")
        return

    # 1. Asegurar Nuitka
    run_cmd([WHISPER_PYTHON, "-m", "pip", "install", "nuitka", "zstandard"], "Instalando Nuitka y dependencias")

    # 2. Blindar paquetes (Convertir a .pyd)
    for pkg in PACKAGES_TO_BLIND:
        if os.path.exists(pkg):
            print(f"\n🛡️  Blindando paquete: {pkg}...")
            # Usamos --module para crear un .pyd
            # --follow-imports para incluir todo lo de adentro
            # --output-dir para organizar
            cmd = [
                WHISPER_PYTHON, "-m", "nuitka",
                "--module",
                "--assume-yes-for-downloads",
                "--output-dir=blindaje_build",
                "--remove-output", # Limpia temporales
                pkg
            ]
            # Nuitka necesita ejecutarse en la carpeta donde está el paquete o especificar la ruta
            run_cmd(cmd, f"Compilando {pkg} a binario")
            
            # Mover el .pyd generado a la raíz y renombrar el original
            # Nuitka genera algo como 'core.cp311-win_amd64.pyd'
            build_dir = os.path.join("blindaje_build", pkg + ".build")
            # En realidad Nuitka deja el .pyd en la raíz de --output-dir
            for f in os.listdir("blindaje_build"):
                if f.startswith(pkg) and f.endswith(".pyd"):
                    dest_pyd = os.path.join(os.getcwd(), f)
                    if os.path.exists(dest_pyd):
                        os.remove(dest_pyd)
                    shutil.move(os.path.join("blindaje_build", f), dest_pyd)
                    print(f"✅ Módulo blindado: {f}")

    # 3. Compilar el Lanzador (El .exe final)
    print("\n📦 Generando ejecutable final: Transcriptor.exe...")
    cmd_exe = [
        WHISPER_PYTHON, "-m", "nuitka",
        "--standalone", # Para que sea independiente
        "--onefile",    # Un solo archivo (opcional, pero profesional)
        "--assume-yes-for-downloads",
        "--windows-disable-console", # Sin consola negra al abrir
        f"--windows-icon-from-ico={ICON_PATH}",
        "--output-dir=dist",
        "--remove-output",
        "Transcriptor.py"
    ]
    # Comentamos --onefile si prefieres una carpeta (a veces Hydra prefiere carpeta)
    # pero intentaremos --onefile primero para máxima portabilidad.
    run_cmd(cmd_exe, "Generando Transcriptor.exe")

    print("\n✨ ¡PROCESO DE BLINDAJE FINALIZADO! ✨")
    print("Los archivos .pyd están en la raíz. El .exe está en la carpeta 'dist'.")
    print("RECUERDA: Ahora puedes mover los archivos .py de las carpetas blindadas a una zona de respaldo.")

if __name__ == "__main__":
    main()
