@echo off
REM Cambia al directorio donde se encuentra este script
cd /d "%~dp0"

REM Ejecuta la aplicación usando el python del entorno virtual de forma directa.
".\whisper_env\Scripts\python.exe" main.py
