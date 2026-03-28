Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

basePath = fso.GetParentFolderName(WScript.ScriptFullName)
lockFile = basePath & "\.config_path.lock"

' ================= GESTIÓN DE UBICACIÓN INTELIGENTE =================
' En lugar de bloquear, actualizamos la ruta si ha cambiado
On Error Resume Next
Set file = fso.CreateTextFile(lockFile, True)
if Err.Number = 0 Then
    file.WriteLine basePath
    file.Close
    ' Asegurar que sea oculto
    Set lock = fso.GetFile(lockFile)
    lock.Attributes = 2 ' Hidden
End If
On Error GoTo 0

' ================= VALIDAR ENTORNO Y COMPONENTES =================
If Not fso.FolderExists(basePath & "\whisper_env") Then
    MsgBox "No se encontró la carpeta del entorno de ejecución (whisper_env)." & vbCrLf & vbCrLf & _
           "Asegúrese de que la carpeta del programa esté completa.", 16, "Error Crítico"
    WScript.Quit
End If

' ================= ACCESO DIRECTO (Automatización) =================
' Si no existe el acceso directo, intentamos crearlo automáticamente
ps1Path = basePath & "\instalar_acceso_directo.ps1"
if fso.FileExists(ps1Path) Then
    ' Ejecutar PowerShell de forma oculta para crear/actualizar el acceso directo
    shell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & ps1Path & """", 0, True
End If

' ================= EJECUCIÓN DE LA APLICACIÓN PRINCIPAL =================
' Ejecutamos el .bat de forma totalmente invisible (0)
If fso.FileExists(basePath & "\ejecutar.bat") Then
    shell.Run chr(34) & basePath & "\ejecutar.bat" & chr(34), 0, False
Else
    MsgBox "No se encontró el lanzador principal (ejecutar.bat).", 16, "Error"
End If
