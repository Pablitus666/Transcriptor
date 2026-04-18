@echo off
REM Cambia al directorio donde se encuentra este script
cd /d "%~dp0"

REM Ejecuta la aplicación usando el pythonw del entorno virtual para invisibilidad total.
REM Si quieres ver errores, cambia pythonw.exe por python.exe y quita el 'start'
start "" ".\whisper_env\Scripts\pythonw.exe" main.py
