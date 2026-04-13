#define MyAppName "Transcriptor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Walter Pablo Téllez Ayala"
#define MyAppExeName "Transcriptor.exe"
#define MyAppIcon "assets\images\icon.ico"

[Setup]
AppId={{5C87E23A-8B6F-46D9-BA1C-7F4B2D8E9A3F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
; --- METADATOS LIMPIOS ---
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription="Software de TranscripciÃ³n (Instalador Base)"
VersionInfoTextVersion={#MyAppVersion}
VersionInfoCopyright="Copyright Ã‚Â© 2026 Walter Pablo TÃƒÂ©llez Ayala"
UninstallDisplayIcon={app}\{#MyAppExeName}

; --- INSTALACIÃ“N DIRECTA EN C:\ PARA EVITAR PERMISOS ---
DefaultDirName=C:\{#MyAppName}
DisableDirPage=no
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=Transcriptor_Setup
SetupIconFile={#MyAppIcon}
Compression=lzma2/ultra
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DiskSpanning=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; LANZADOR PROFESIONAL FIRMADO
Source: "Transcriptor.exe"; DestDir: "{app}"; Flags: ignoreversion

; SCRIPTS Y LÃ“GICA BLINDADA
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "worker.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "gui\*"; DestDir: "{app}\gui"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "exporters\*"; DestDir: "{app}\exporters"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs

; RECURSOS
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
; PREPARAR CARPETAS PARA EL MOTOR PESADO (A COPIAR MANUALMENTE)
Name: "{app}\whisper_env"
Name: "{app}\models_cache"
Name: "{app}\output"

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
; Nota: El lanzamiento automÃ¡tico se desactiva porque requiere copiar whisper_env primero.
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked
