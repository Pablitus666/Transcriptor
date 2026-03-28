$Desktop = [Environment]::GetFolderPath("Desktop")
$Target = "$PSScriptRoot\iniciar.vbs"
$ShortcutPath = "$Desktop\Transcriptor.lnk"
$IconPath = "$PSScriptRoot\images\icon.ico"

if (-Not (Test-Path $ShortcutPath)) {
    try {
        $WScriptShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = $Target
        $Shortcut.IconLocation = $IconPath
        $Shortcut.WorkingDirectory = $PSScriptRoot
        $Shortcut.Save()
    } catch {
        # No hacer nada si falla (p.ej. por permisos), para no molestar al usuario.
    }
}
