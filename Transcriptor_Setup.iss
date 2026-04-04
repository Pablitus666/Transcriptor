; ==============================================================================
; Script de Instalación Profesional Ligero - Inno Setup
; Proyecto: Transcriptor (Edición Élite)
; Desarrollador: Walter Pablo Tellez Ayala
; ==============================================================================

#define MyAppName "Transcriptor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Walter Pablo Tellez Ayala"
#define MyAppExeName "Transcriptor.exe"
#define MyIcon "assets\images\icon.ico"

[Setup]
AppId={{C6E2A1B0-9F3D-4D8E-B1A2-C3D4E5F6A7B8}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
SetupIconFile={#MyIcon}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\{#MyIcon}
UninstallDisplayName={#MyAppName}
OutputBaseFilename=Transcriptor_Setup_V1
; --- FIRMA NATIVA INTEGRADA ---
SignTool=signtool $f

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "Transcriptor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "worker.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "utils\*"; DestDir: "{app}\utils"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "exporters\*"; DestDir: "{app}\exporters"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "gui\*"; DestDir: "{app}\gui"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "whisper_env\*"; DestDir: "{app}\whisper_env"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
