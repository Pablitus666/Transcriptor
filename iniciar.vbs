Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Obtener la ruta absoluta de la carpeta donde está este script
basePath = fso.GetParentFolderName(WScript.ScriptFullName)

' ================= VALIDAR ENTORNO Y COMPONENTES =================
If Not fso.FolderExists(basePath & "\whisper_env") Then
    MsgBox "No se encontró la carpeta del entorno de ejecución (whisper_env)." & vbCrLf & vbCrLf & _
           "Asegúrese de que la carpeta del programa esté completa.", 16, "Error Crítico"
    WScript.Quit
End If

' ================= ACCESO DIRECTO (Automatización) =================
' Intentar crear/actualizar el acceso directo en segundo plano (asíncrono)
ps1Path = basePath & "\instalar_acceso_directo.ps1"
If fso.FileExists(ps1Path) Then
    ' Ejecutamos PS de forma invisible y SIN esperar (False) para no retrasar el inicio
    shell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & ps1Path & """", 0, False
End If

' ================= EJECUCIÓN DE LA APLICACIÓN PRINCIPAL =================
' Ejecutamos el .bat de forma totalmente invisible (0) y asíncrona (False)
If fso.FileExists(basePath & "\ejecutar.bat") Then
    shell.Run chr(34) & basePath & "\ejecutar.bat" & chr(34), 0, False
Else
    MsgBox "No se encontró el lanzador principal (ejecutar.bat) en:" & vbCrLf & basePath, 16, "Error"
End If

Set shell = Nothing
Set fso = Nothing
