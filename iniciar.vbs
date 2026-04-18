' ============================================================
' Transcriptor - Lanzador Inteligente Portátil
' Garantiza ejecución invisible y detección de rutas absoluta.
' ============================================================

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener la ruta absoluta de la carpeta donde está este script
basePath = fso.GetParentFolderName(WScript.ScriptFullName)

' Definir rutas críticas de forma absoluta
pythonExe = basePath & "\whisper_env\Scripts\pythonw.exe"
mainScript = basePath & "\main.py"

' 1. Validar que Python exista
If Not fso.FileExists(pythonExe) Then
    MsgBox "Error: No se encontró el entorno de IA en:" & vbCrLf & pythonExe, 16, "Error de Instalación"
    WScript.Quit
End If

' 2. Lanzar la aplicación principal de forma TOTALMENTE INVISIBLE
command = """" & pythonExe & """ """ & mainScript & """"
shell.Run command, 0, False

Set shell = Nothing
Set fso = Nothing
