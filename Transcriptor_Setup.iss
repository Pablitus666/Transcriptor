#define MyAppName "Transcriptor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Walter Pablo TÃ©llez Ayala"
#define MyAppExeName "Transcriptor.exe"
#define MyAppIcon "ICONO_ELITE\Transcriptor_Nuevo_2026.ico"

[Setup]
AppId={{5C87E23A-8B6F-46D9-BA1C-7F4B2D8E9A3F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=Transcriptor_Setup_V1
SetupIconFile={#MyAppIcon}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

; Desactivamos el fraccionamiento ya que el instalador serÃ¡ ligero
DiskSpanning=no

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Transcriptor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "worker.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "*.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "exporters\*"; DestDir: "{app}\exporters"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "gui\*"; DestDir: "{app}\gui"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "whisper_env\*"; DestDir: "{app}\whisper_env"; Flags: ignoreversion recursesubdirs createallsubdirs
; EXCLUIMOS models_cache para distribuirlo manualmente
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "MANUAL.pdf"; DestDir: "{app}"; Flags: ignoreversion
Source: "GUIA_INSTITUCIONAL.pdf"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\output"
Name: "{app}\cache"
Name: "{app}\models_cache" 

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
