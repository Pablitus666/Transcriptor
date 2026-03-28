Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener la ruta absoluta de la carpeta donde está este script
basePath = fso.GetParentFolderName(WScript.ScriptFullName)

' Ejecutar el .bat de forma totalmente invisible (0) usando la ruta completa
If fso.FileExists(basePath & "\ejecutar.bat") Then
    shell.Run chr(34) & basePath & "\ejecutar.bat" & chr(34), 0, False
Else
    MsgBox "No se encontró el lanzador principal (ejecutar.bat) en:" & vbCrLf & basePath, 16, "Error"
End If

Set shell = Nothing
Set fso = Nothing
