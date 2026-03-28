@echo off
REM Cambia al directorio donde se encuentra este script para evitar errores de rutas.
cd /d "%~dp0"

REM Activa el entorno virtual. 'call' es crucial para que el control regrese a este script.
call "whisper_env\Scripts\activate.bat"

REM Ejecuta la aplicación principal a través del nuevo punto de entrada.
python main.py
