#define MyAppName "Transcriptor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Walter Pablo Téllez Ayala"
#define MyAppExeName "transcriptor.exe"
#define MyAppIcon "assets\images\icon.ico"
#define MyAppVBS "iniciar.vbs"

[Setup]
AppId={{5C87E23A-8B6F-46D9-BA1C-7F4B2D8E9A3F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}

; --- METADATOS ---
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription="Transcriptor de Cámara Gesell"
VersionInfoTextVersion={#MyAppVersion}
VersionInfoCopyright="Copyright © 2026 Walter Pablo Téllez Ayala"

; --- ICONO EN PANEL DE CONTROL ---
UninstallDisplayIcon={app}\assets\images\icon.ico

; --- RUTA DE INSTALACION SEGURA ---
DefaultDirName=C:\Transcriptor
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=Transcriptor_Setup_V1
SetupIconFile={#MyAppIcon}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
DiskSpanning=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; LANZADORES Y MOTOR PRINCIPAL
Source: "transcriptor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "worker.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MyAppVBS}"; DestDir: "{app}"; Flags: ignoreversion
Source: "ejecutar.bat"; DestDir: "{app}"; Flags: ignoreversion

; ESTRUCTURA DE CODIGO FUENTE (RESTAURADA)
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "gui\*"; DestDir: "{app}\gui"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "exporters\*"; DestDir: "{app}\exporters"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs

; RECURSOS
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; CEREBRO (ENTORNO VIRTUAL)
Source: "whisper_env\*"; DestDir: "{app}\whisper_env"; Flags: ignoreversion recursesubdirs createallsubdirs

[Dirs]
Name: "{app}\output"
Name: "{app}\cache"
Name: "{app}\models_cache" 

[Icons]
; El acceso directo apunta al .VBS para un arranque invisible y estable
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppVBS}"; IconFilename: "{app}\{#MyAppIcon}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppVBS}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppIcon}"; WorkingDir: "{app}"

[Run]
; Lanzamos el VBS al finalizar la instalación
Filename: "wscript.exe"; Parameters: """{app}\{#MyAppVBS}"""; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
