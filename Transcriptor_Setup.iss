#define MyAppName "Transcriptor"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Walter Pablo Tellez Ayala"
#define MyAppExeName "Transcriptor.exe"
#define MyAppIcon "assets\images\icon.ico"

[Setup]
AppId={{5C87E23A-8B6F-46D9-BA1C-7F4B2D8E9A3F}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=C:\{#MyAppName}
DisableDirPage=no
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=Transcriptor_Setup
SetupIconFile={#MyAppIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; 1. LANZADOR PRINCIPAL
Source: "Transcriptor.exe"; DestDir: "{app}"; Flags: ignoreversion

; 2. ARCHIVOS BINARIOS BLINDADOS (PYD)
Source: "*.pyd"; DestDir: "{app}"; Flags: ignoreversion

; 3. SCRIPTS DE ENTRADA
Source: "main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "worker.py"; DestDir: "{app}"; Flags: ignoreversion

; 4. CONFIGURACION Y DATOS
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "utils\*.json"; DestDir: "{app}\utils"; Flags: ignoreversion

; 5. RECURSOS (IMAGENES, LOCALES)
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; 6. ENTORNO VIRTUAL COMPLETO (whisper_env)
Source: "whisper_env\*"; DestDir: "{app}\whisper_env"; Flags: ignoreversion recursesubdirs createallsubdirs     

; 7. ESTRUCTURA DE CARPETAS INTERNAS (SOPORTE PARA IMPORTACIONES)
Source: "config\*.py"; DestDir: "{app}\config"; Flags: ignoreversion
Source: "core\*.py"; DestDir: "{app}\core"; Flags: ignoreversion
Source: "gui\*.py"; DestDir: "{app}\gui"; Flags: ignoreversion
Source: "exporters\*.py"; DestDir: "{app}\exporters"; Flags: ignoreversion
Source: "utils\*.py"; DestDir: "{app}\utils"; Flags: ignoreversion

[Dirs]
Name: "{app}\models_cache"
Name: "{app}\output"

[Icons]
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked
