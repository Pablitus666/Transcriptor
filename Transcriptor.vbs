Set objShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' La ruta siempre se basa en donde está el script VBS (Portabilidad garantizada)
strAppPath = fso.GetParentFolderName(WScript.ScriptFullName)

strPythonExe = strAppPath & "\whisper_env\Scripts\pythonw.exe"
strScriptPath = strAppPath & "\main.py"

' Si no encuentra el Python en la ruta directa, intenta buscar un nivel arriba
If Not fso.FileExists(strPythonExe) Then
    strAppPath = fso.GetParentFolderName(strAppPath)
    strPythonExe = strAppPath & "\whisper_env\Scripts\pythonw.exe"
    strScriptPath = strAppPath & "\main.py"
End If

' Lanzamos el programa de forma invisible
If fso.FileExists(strPythonExe) Then
    objShell.Run """" & strPythonExe & """ """ & strScriptPath & """", 0, False
Else
    MsgBox "No se pudo encontrar el entorno de Python (whisper_env) en:" & vbCrLf & strAppPath, 16, "Error de Portabilidad"
End If
